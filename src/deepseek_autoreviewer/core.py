"""Core implementation of the five-review AutoReviewer pipeline."""

import copy
import hashlib
import json
import math
import re
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pymupdf

from .prompts import (
    META_REVIEWER_SYSTEM_PROMPT,
    REVIEWER_SYSTEM_PROMPT,
    build_meta_review_prompt,
    build_review_prompt,
)
from .client import validate_official_base_url
from .nature_protocol import (
    LEGACY_PROTOCOL_ID,
    NATURE_META_REVIEWER_SYSTEM_PROMPT,
    NATURE_PROTOCOL_ID,
    NATURE_REVIEWER_SYSTEM_PROMPT,
    NATURE_TEMPERATURE,
    build_nature_meta_review_prompt,
    build_nature_review_prompt,
    nature_protocol_record,
)


NUMERIC_RANGES: Dict[str, Tuple[int, int]] = {
    "Originality": (1, 4),
    "Quality": (1, 4),
    "Clarity": (1, 4),
    "Significance": (1, 4),
    "Soundness": (1, 4),
    "Presentation": (1, 4),
    "Contribution": (1, 4),
    "Overall": (1, 10),
    "Confidence": (1, 5),
}
LIST_FIELDS = ("Strengths", "Weaknesses", "Questions", "Limitations")
REQUIRED_FIELDS = (
    "Summary",
    *LIST_FIELDS,
    *NUMERIC_RANGES.keys(),
    "Ethical Concerns",
    "Decision",
)


@dataclass(frozen=True)
class ReviewerConfig:
    """Runtime settings and explicit price assumptions."""

    model: str = "deepseek-v4-flash"
    base_url: str = "https://api.deepseek.com"
    ensemble_size: int = 5
    parallelism: int = 5
    reasoning_effort: str = "max"
    max_output_tokens: int = 16384
    max_attempts: int = 3
    retry_base_seconds: float = 1.0
    aggregate_scores: str = "meta"
    cache_hit_usd_per_million: float = 0.0028
    cache_miss_usd_per_million: float = 0.14
    output_usd_per_million: float = 0.28
    protocol: str = LEGACY_PROTOCOL_ID

    def validate(self) -> None:
        validate_official_base_url(self.base_url)
        if self.ensemble_size < 1:
            raise ValueError("ensemble_size must be at least 1")
        if self.parallelism < 1:
            raise ValueError("parallelism must be at least 1")
        if self.max_output_tokens < 512:
            raise ValueError("max_output_tokens must be at least 512")
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if self.aggregate_scores not in {"meta", "mean"}:
            raise ValueError("aggregate_scores must be 'meta' or 'mean'")
        if self.protocol not in {LEGACY_PROTOCOL_ID, NATURE_PROTOCOL_ID}:
            raise ValueError(f"Unsupported reviewer protocol: {self.protocol}")
        if self.protocol == NATURE_PROTOCOL_ID:
            if self.ensemble_size != 5:
                raise ValueError("Nature protocol requires exactly five reviewers")
            if self.reasoning_effort != "none":
                raise ValueError(
                    "Nature protocol requires reasoning_effort='none' because the "
                    "field is omitted from the effective request"
                )
            if self.aggregate_scores != "mean":
                raise ValueError(
                    "Nature protocol requires rounded-mean numerical aggregation"
                )


def get_protocol_record(config: ReviewerConfig) -> Optional[Dict[str, Any]]:
    """Return the formal run binding for an opt-in protocol.

    Legacy strict runs deliberately return ``None`` so their bundle and
    manifest compatibility remains unchanged.
    """

    if config.protocol != NATURE_PROTOCOL_ID:
        return None
    return nature_protocol_record(
        model=config.model,
        max_output_tokens=config.max_output_tokens,
        max_attempts=config.max_attempts,
        ensemble_size=config.ensemble_size,
        parallelism=config.parallelism,
    )


def extract_pdf_text(pdf_path: Path, min_characters: int = 1000) -> Tuple[str, Dict[str, Any]]:
    """Extract raw text with PyMuPDF, matching the paper's described input path."""
    pdf_path = Path(pdf_path).expanduser().resolve()
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    digest = hashlib.sha256()
    with pdf_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    document = pymupdf.open(pdf_path)
    try:
        page_texts = []
        for index, page in enumerate(document, start=1):
            text = page.get_text("text", sort=True).strip()
            page_texts.append(f"\n\n--- Page {index} ---\n\n{text}")
        paper_text = "".join(page_texts).strip()
        page_count = document.page_count
    finally:
        document.close()

    if len(paper_text) < min_characters:
        raise ValueError(
            f"Only {len(paper_text)} characters were extracted. "
            "The PDF may be scanned or image-only; OCR it before reviewing."
        )

    metadata = {
        "path": str(pdf_path),
        "filename": pdf_path.name,
        "sha256": digest.hexdigest(),
        "size_bytes": pdf_path.stat().st_size,
        "page_count": page_count,
        "extracted_characters": len(paper_text),
        "full_text_saved": False,
    }
    return paper_text, metadata


def parse_review_json(content: str) -> Dict[str, Any]:
    """Parse a direct JSON response, with a fenced-object fallback."""
    if not isinstance(content, str) or not content.strip():
        raise ValueError("Model returned an empty response")

    candidates = [content.strip()]
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", content, re.DOTALL | re.IGNORECASE)
    if fence:
        candidates.append(fence.group(1))
    first = content.find("{")
    last = content.rfind("}")
    if first >= 0 and last > first:
        candidates.append(content[first : last + 1])

    last_error: Optional[Exception] = None
    for candidate in candidates:
        try:
            value = json.loads(candidate)
            if not isinstance(value, dict):
                raise ValueError("Top-level JSON value must be an object")
            return validate_review(value)
        except (json.JSONDecodeError, ValueError) as exc:
            last_error = exc
    raise ValueError(f"Could not parse a valid review JSON object: {last_error}")


def validate_review(review: Dict[str, Any]) -> Dict[str, Any]:
    """Validate without silently coercing or clipping model scores."""
    missing = [field for field in REQUIRED_FIELDS if field not in review]
    if missing:
        raise ValueError(f"Missing review fields: {', '.join(missing)}")
    if not isinstance(review["Summary"], str) or not review["Summary"].strip():
        raise ValueError("Summary must be a non-empty string")
    for field in LIST_FIELDS:
        value = review[field]
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ValueError(f"{field} must be a list of strings")
    for field, (lower, upper) in NUMERIC_RANGES.items():
        value = review[field]
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{field} must be an integer")
        if not lower <= value <= upper:
            raise ValueError(f"{field} must be in [{lower}, {upper}], got {value}")
    if not isinstance(review["Ethical Concerns"], bool):
        raise ValueError("Ethical Concerns must be a boolean")
    if review["Decision"] not in {"Accept", "Reject"}:
        raise ValueError("Decision must be exactly Accept or Reject")
    return review


def normalize_usage(response: Any) -> Dict[str, int]:
    """Normalize DeepSeek/OpenAI-compatible usage fields."""
    usage = getattr(response, "usage", None)
    if usage is None:
        return {
            "prompt_tokens": 0,
            "prompt_cache_hit_tokens": 0,
            "prompt_cache_miss_tokens": 0,
            "completion_tokens": 0,
            "reasoning_tokens": 0,
            "total_tokens": 0,
        }
    if hasattr(usage, "model_dump"):
        raw = usage.model_dump()
    elif isinstance(usage, dict):
        raw = dict(usage)
    else:
        raw = vars(usage)

    prompt_tokens = int(raw.get("prompt_tokens") or 0)
    hit_tokens = int(raw.get("prompt_cache_hit_tokens") or 0)
    miss_tokens = int(raw.get("prompt_cache_miss_tokens") or 0)
    if prompt_tokens and not hit_tokens and not miss_tokens:
        miss_tokens = prompt_tokens
    completion_tokens = int(raw.get("completion_tokens") or 0)
    details = raw.get("completion_tokens_details") or {}
    if hasattr(details, "model_dump"):
        details = details.model_dump()
    reasoning_tokens = int(details.get("reasoning_tokens") or 0) if isinstance(details, dict) else 0
    return {
        "prompt_tokens": prompt_tokens,
        "prompt_cache_hit_tokens": hit_tokens,
        "prompt_cache_miss_tokens": miss_tokens,
        "completion_tokens": completion_tokens,
        "reasoning_tokens": reasoning_tokens,
        "total_tokens": int(raw.get("total_tokens") or prompt_tokens + completion_tokens),
    }


def aggregate_usage(call_results: List[Dict[str, Any]]) -> Dict[str, int]:
    keys = (
        "prompt_tokens",
        "prompt_cache_hit_tokens",
        "prompt_cache_miss_tokens",
        "completion_tokens",
        "reasoning_tokens",
        "total_tokens",
    )
    totals = {key: 0 for key in keys}
    for result in call_results:
        for key in keys:
            totals[key] += int(result["usage"].get(key, 0))
    totals["request_count"] = len(call_results)
    return totals


def estimate_cost_usd(usage: Dict[str, int], config: ReviewerConfig) -> Dict[str, float]:
    divisor = 1_000_000
    hit = usage["prompt_cache_hit_tokens"] * config.cache_hit_usd_per_million / divisor
    miss = usage["prompt_cache_miss_tokens"] * config.cache_miss_usd_per_million / divisor
    output = usage["completion_tokens"] * config.output_usd_per_million / divisor
    return {
        "cache_hit_input_usd": round(hit, 8),
        "cache_miss_input_usd": round(miss, 8),
        "output_usd": round(output, 8),
        "total_usd": round(hit + miss + output, 8),
    }


def summarize_ensemble(reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
    scores: Dict[str, Any] = {}
    for field in NUMERIC_RANGES:
        values = [review[field] for review in reviews]
        scores[field] = {
            "values": values,
            "mean": round(statistics.mean(values), 3),
            "rounded_mean": int(round(statistics.mean(values))),
            "population_sd": round(statistics.pstdev(values), 3),
            "min": min(values),
            "max": max(values),
        }
    accepts = sum(review["Decision"] == "Accept" for review in reviews)
    rejects = len(reviews) - accepts
    return {
        "decision_counts": {"Accept": accepts, "Reject": rejects},
        "unanimous_decision": accepts == 0 or rejects == 0,
        "score_statistics": scores,
    }


def _create_completion(
    client: Any,
    config: ReviewerConfig,
    system_prompt: str,
    user_prompt: str,
    call_label: str,
) -> Dict[str, Any]:
    last_error: Optional[Exception] = None
    for attempt in range(1, config.max_attempts + 1):
        try:
            request: Dict[str, Any] = {
                "model": config.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": config.max_output_tokens,
            }
            if config.protocol == NATURE_PROTOCOL_ID:
                request.update(
                    {
                        "temperature": NATURE_TEMPERATURE,
                        "extra_body": {"thinking": {"type": "disabled"}},
                    }
                )
            else:
                request.update(
                    {
                        "reasoning_effort": config.reasoning_effort,
                        "response_format": {"type": "json_object"},
                        "extra_body": {"thinking": {"type": "enabled"}},
                    }
                )
            response = client.chat.completions.create(
                **request,
            )
            content = response.choices[0].message.content or ""
            review = parse_review_json(content)
            return {
                "label": call_label,
                "review": review,
                "raw_response": content,
                "usage": normalize_usage(response),
                "attempts": attempt,
                "response_id": getattr(response, "id", None),
            }
        except Exception as exc:  # API and schema failures share the bounded retry policy.
            last_error = exc
            if attempt < config.max_attempts and config.retry_base_seconds > 0:
                time.sleep(config.retry_base_seconds * math.pow(2, attempt - 1))
    error_type = type(last_error).__name__ if last_error is not None else "UnknownError"
    status_code = getattr(last_error, "status_code", None)
    request_id = getattr(last_error, "request_id", None)
    safe_details = [error_type]
    if status_code is not None:
        safe_details.append(f"HTTP {status_code}")
    if request_id:
        safe_details.append(f"request_id={request_id}")
    raise RuntimeError(
        f"{call_label} failed after {config.max_attempts} attempts ({', '.join(safe_details)})"
    ) from last_error


def review_text(paper_text: str, client: Any, config: Optional[ReviewerConfig] = None) -> Dict[str, Any]:
    """Run independent reviews, then one Area Chair meta-review."""
    config = config or ReviewerConfig()
    config.validate()
    if not isinstance(paper_text, str) or len(paper_text.strip()) < 1000:
        raise ValueError("paper_text must contain at least 1000 non-whitespace characters")

    started = time.monotonic()
    if config.protocol == NATURE_PROTOCOL_ID:
        reviewer_system_prompt = NATURE_REVIEWER_SYSTEM_PROMPT
        review_prompt = build_nature_review_prompt(paper_text)
    else:
        reviewer_system_prompt = REVIEWER_SYSTEM_PROMPT
        review_prompt = build_review_prompt(paper_text)
    indexed_results: Dict[int, Dict[str, Any]] = {}
    worker_count = min(config.parallelism, config.ensemble_size)
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = {
            executor.submit(
                _create_completion,
                client,
                config,
                reviewer_system_prompt,
                review_prompt,
                f"reviewer_{index}",
            ): index
            for index in range(1, config.ensemble_size + 1)
        }
        for future in as_completed(futures):
            index = futures[future]
            indexed_results[index] = future.result()

    individual_results = [indexed_results[index] for index in sorted(indexed_results)]
    individual_reviews = [result["review"] for result in individual_results]
    if config.protocol == NATURE_PROTOCOL_ID:
        meta_system_prompt = NATURE_META_REVIEWER_SYSTEM_PROMPT.format(
            reviewer_count=len(individual_reviews)
        )
        meta_user_prompt = build_nature_meta_review_prompt(individual_reviews)
    else:
        meta_system_prompt = META_REVIEWER_SYSTEM_PROMPT.format(
            reviewer_count=len(individual_reviews)
        )
        meta_user_prompt = build_meta_review_prompt(individual_reviews)
    meta_result = _create_completion(
        client,
        config,
        meta_system_prompt,
        meta_user_prompt,
        "area_chair_meta_review",
    )

    summary = summarize_ensemble(individual_reviews)
    final_review = copy.deepcopy(meta_result["review"])
    if config.aggregate_scores == "mean":
        for field in NUMERIC_RANGES:
            final_review[field] = summary["score_statistics"][field]["rounded_mean"]

    all_calls = individual_results + [meta_result]
    usage = aggregate_usage(all_calls)
    cost = estimate_cost_usd(usage, config)
    bundle = {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "implementation": {
            "name": "deepseek-autoreviewer",
            "version": "0.1.0",
            "pipeline": "five independent reviews plus one Area Chair meta-review",
            "calibration_status": (
                "Uncalibrated model substitution: Nature validated o4-mini, not DeepSeek V4 Flash."
            ),
            "hidden_reasoning_saved": False,
            "visible_thought_scaffold_saved": config.protocol == NATURE_PROTOCOL_ID,
        },
        "config": asdict(config),
        "individual_reviews": individual_results,
        "ensemble_summary": summary,
        "meta_review_model": meta_result,
        "final_review": final_review,
        "final_review_source": (
            "Area Chair model output"
            if config.aggregate_scores == "meta"
            else "Area Chair text/decision with rounded mean numerical scores"
        ),
        "usage": usage,
        "price_assumptions_usd_per_million_tokens": {
            "cache_hit_input": config.cache_hit_usd_per_million,
            "cache_miss_input": config.cache_miss_usd_per_million,
            "output": config.output_usd_per_million,
        },
        "estimated_cost_usd": cost,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    protocol_record = get_protocol_record(config)
    if protocol_record is not None:
        bundle["protocol"] = protocol_record
        bundle["nature_result_views"] = {
            "authoritative_binary_decision_path": (
                "meta_review_model.review.Decision"
            ),
            "authoritative_binary_decision": meta_result["review"]["Decision"],
            "raw_area_chair_review_path": "meta_review_model.review",
            "public_code_rounded_mean_numeric_view_path": "final_review",
            "numeric_fields_overwritten_in_final_review": list(NUMERIC_RANGES),
            "area_chair_text_fields_overwritten": False,
            "area_chair_decision_overwritten": False,
        }
    return bundle


def review_pdf(pdf_path: Path, client: Any, config: Optional[ReviewerConfig] = None) -> Dict[str, Any]:
    paper_text, input_metadata = extract_pdf_text(Path(pdf_path))
    bundle = review_text(paper_text, client, config)
    bundle["input"] = input_metadata
    return bundle


def render_markdown(bundle: Dict[str, Any]) -> str:
    """Create a readable companion while keeping JSON as the source of truth."""
    review = bundle["final_review"]
    ensemble = bundle["ensemble_summary"]
    usage = bundle["usage"]
    cost = bundle["estimated_cost_usd"]
    input_meta = bundle.get("input", {})

    lines = [
        "# AutoReviewer Report",
        "",
        "> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes ",
        "> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.",
        "",
        f"- Paper: {input_meta.get('filename', 'text input')}",
        f"- Model: {bundle['config']['model']}",
        f"- Final decision: **{review['Decision']}**",
        f"- Overall: **{review['Overall']}/10**",
        f"- Confidence: **{review['Confidence']}/5**",
        f"- Independent decisions: {ensemble['decision_counts']}",
        f"- Estimated API cost: **${cost['total_usd']:.6f}**",
        "",
        "## Final Meta-review",
        "",
        review["Summary"],
        "",
        "### Scores",
        "",
        "| Dimension | Final | Five-review mean | SD | Range |",
        "|---|---:|---:|---:|---:|",
    ]
    for field in NUMERIC_RANGES:
        stat = ensemble["score_statistics"][field]
        lines.append(
            f"| {field} | {review[field]} | {stat['mean']:.3f} | "
            f"{stat['population_sd']:.3f} | {stat['min']}-{stat['max']} |"
        )

    for heading, field in (
        ("Strengths", "Strengths"),
        ("Weaknesses", "Weaknesses"),
        ("Questions", "Questions"),
        ("Limitations", "Limitations"),
    ):
        lines.extend(["", f"### {heading}", ""])
        values = review[field] or ["None stated."]
        lines.extend(f"- {value}" for value in values)

    lines.extend(
        [
            "",
            "### Ethics",
            "",
            f"Ethical concerns flagged: **{review['Ethical Concerns']}**",
            "",
            "## Usage and Cost",
            "",
            f"- Requests: {usage['request_count']}",
            f"- Prompt tokens: {usage['prompt_tokens']:,}",
            f"- Cache-hit prompt tokens: {usage['prompt_cache_hit_tokens']:,}",
            f"- Cache-miss prompt tokens: {usage['prompt_cache_miss_tokens']:,}",
            f"- Completion tokens: {usage['completion_tokens']:,}",
            f"- Reasoning tokens reported: {usage['reasoning_tokens']:,}",
            f"- Total tokens: {usage['total_tokens']:,}",
            f"- Estimated total: ${cost['total_usd']:.8f}",
            "",
            "Full individual reviews and raw JSON responses are in `review_bundle.json`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(bundle: Dict[str, Any], output_dir: Path) -> Tuple[Path, Path]:
    output_dir = Path(output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_dir.chmod(0o700)
    json_path = output_dir / "review_bundle.json"
    markdown_path = output_dir / "review.md"
    json_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    markdown_path.write_text(render_markdown(bundle), encoding="utf-8")
    json_path.chmod(0o600)
    markdown_path.chmod(0o600)
    return json_path, markdown_path
