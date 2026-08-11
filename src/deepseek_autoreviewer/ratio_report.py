"""Fail-closed cohort report for the ICLR 2026 real-ratio benchmark.

The report joins a *verified* label-free prediction freeze to the private
mapping only after checking every referenced review bundle.  Resampling is
stratified by ground-truth class and always resamples complete papers: a
paper's final decision and five-review mean score move together.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import re
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple

from .benchmark import BLINDING_VERSION, BenchmarkError


REPORT_FORMAT_VERSION = "deepseek-autoreviewer-real-ratio-report-v1"
FREEZE_FORMAT_VERSION = "deepseek-autoreviewer-frozen-predictions-v1"
OFFICIAL_ACCEPT_COUNT = 5355
OFFICIAL_REJECT_COUNT = 8408
OFFICIAL_ACCEPT_PREVALENCE = OFFICIAL_ACCEPT_COUNT / (
    OFFICIAL_ACCEPT_COUNT + OFFICIAL_REJECT_COUNT
)
DEFAULT_BOOTSTRAP_SAMPLES = 10_000
DEFAULT_BOOTSTRAP_SEED = 20260811

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_BLIND_ID = re.compile(r"^B([0-9]{3})$")
_EXPECTED_IDS = tuple(f"B{index:03d}" for index in range(1, 201))
_COHORT_IDS = {
    "pilot": frozenset(_EXPECTED_IDS[:40]),
    "extension": frozenset(_EXPECTED_IDS[40:]),
    "pooled": frozenset(_EXPECTED_IDS),
}
_EXPECTED_CLASS_COUNTS = {
    "pilot": {"Accept": 20, "Reject": 20},
    "extension": {"Accept": 58, "Reject": 102},
    "pooled": {"Accept": 78, "Reject": 122},
}


class RatioReportError(BenchmarkError):
    """Raised when an input cannot safely support the real-ratio report."""


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_real_file(path: Path, *, artifact: str) -> Tuple[Path, bytes]:
    requested = Path(path).expanduser()
    if requested.is_symlink():
        raise RatioReportError(f"{artifact} must not be a symbolic link")
    resolved = requested.resolve()
    if not resolved.is_file() or resolved.is_symlink():
        raise RatioReportError(f"{artifact} is missing or is not a real file")
    return resolved, resolved.read_bytes()


def _decode_object(payload: bytes, *, artifact: str) -> Dict[str, Any]:
    try:
        value = json.loads(payload)
    except Exception:
        raise RatioReportError(f"{artifact} is not valid JSON") from None
    if not isinstance(value, dict):
        raise RatioReportError(f"{artifact} must contain a JSON object")
    return value


def _load_verified_freeze(path: Path) -> Tuple[Dict[str, Any], str, Path]:
    freeze_path, payload = _read_real_file(path, artifact="Frozen predictions")
    sidecar_path = freeze_path.with_name(freeze_path.name + ".sha256")
    _, sidecar_payload = _read_real_file(
        sidecar_path, artifact="Frozen prediction SHA-256 sidecar"
    )
    try:
        expected_hash = sidecar_payload.decode("ascii").strip()
    except UnicodeDecodeError:
        raise RatioReportError("Frozen prediction SHA-256 sidecar is not ASCII") from None
    actual_hash = _sha256_bytes(payload)
    if not _SHA256.fullmatch(expected_hash) or expected_hash != actual_hash:
        raise RatioReportError("Frozen prediction SHA-256 verification failed")
    artifact = _decode_object(payload, artifact="Frozen predictions")
    if artifact.get("format_version") != FREEZE_FORMAT_VERSION:
        raise RatioReportError("Frozen prediction format version is unsupported")
    if artifact.get("contains_ground_truth") is not False:
        raise RatioReportError("Frozen prediction artifact is not label-free")
    papers = artifact.get("papers")
    if not isinstance(papers, list) or artifact.get("paper_count") != len(papers):
        raise RatioReportError("Frozen prediction paper_count does not match its list")
    if len(papers) != 200:
        raise RatioReportError(f"Expected 200 frozen predictions, found {len(papers)}")
    return artifact, actual_hash, freeze_path


def _load_mapping(path: Path) -> Tuple[Dict[str, Any], str, Path]:
    mapping_path, payload = _read_real_file(path, artifact="Private mapping")
    mapping = _decode_object(payload, artifact="Private mapping")
    if mapping.get("format_version") != BLINDING_VERSION:
        raise RatioReportError("Private mapping format version is unsupported")
    papers = mapping.get("papers")
    if not isinstance(papers, list) or len(papers) != 200:
        count = len(papers) if isinstance(papers, list) else "invalid"
        raise RatioReportError(f"Expected 200 private mapping entries, found {count}")
    return mapping, _sha256_bytes(payload), mapping_path


def _validated_root(path: Path) -> Path:
    requested = Path(path).expanduser()
    if requested.is_symlink():
        raise RatioReportError("Bundle root must not be a symbolic link")
    root = requested.resolve()
    if not root.is_dir() or root.is_symlink():
        raise RatioReportError("Bundle root is missing or is not a real directory")
    return root


def _parse_label(value: Any, *, field: str) -> int:
    if not isinstance(value, str):
        raise RatioReportError(f"{field} must be Accept or Reject")
    normalized = value.strip().casefold()
    if normalized == "accept":
        return 1
    if normalized == "reject":
        return 0
    raise RatioReportError(f"{field} must be Accept or Reject")


def _parse_scores(values: Any, *, blind_id: str) -> Tuple[float, ...]:
    if not isinstance(values, list) or len(values) != 5:
        raise RatioReportError(f"{blind_id} must have exactly five reviewer scores")
    parsed: List[float] = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise RatioReportError(f"{blind_id} reviewer scores must be numeric")
        score = float(value)
        if not math.isfinite(score) or not 1 <= score <= 10:
            raise RatioReportError(f"{blind_id} reviewer scores must be finite and in [1, 10]")
        parsed.append(score)
    return tuple(parsed)


def _bundle_projection(bundle: Mapping[str, Any], *, blind_id: str) -> Tuple[str, Tuple[float, ...], str]:
    input_metadata = bundle.get("input")
    if not isinstance(input_metadata, Mapping):
        raise RatioReportError(f"{blind_id} bundle has no input metadata")
    if input_metadata.get("blind_id") != blind_id:
        raise RatioReportError(f"{blind_id} bundle ID binding does not match")
    blind_hash = input_metadata.get("blind_text_sha256")
    if not isinstance(blind_hash, str) or not _SHA256.fullmatch(blind_hash):
        raise RatioReportError(f"{blind_id} bundle manuscript hash is invalid")
    reviews = bundle.get("individual_reviews")
    if not isinstance(reviews, list) or len(reviews) != 5:
        raise RatioReportError(f"{blind_id} bundle must have exactly five reviews")
    scores: List[Any] = []
    for entry in reviews:
        if not isinstance(entry, Mapping):
            raise RatioReportError(f"{blind_id} bundle contains an invalid review")
        review = entry.get("review")
        if not isinstance(review, Mapping) or "Overall" not in review:
            raise RatioReportError(f"{blind_id} bundle contains an invalid review")
        scores.append(review["Overall"])
    parsed_scores = _parse_scores(scores, blind_id=blind_id)
    final_review = bundle.get("final_review")
    if not isinstance(final_review, Mapping):
        raise RatioReportError(f"{blind_id} bundle has no final review")
    decision = final_review.get("Decision")
    _parse_label(decision, field=f"{blind_id} final decision")
    return blind_hash, parsed_scores, str(decision).strip().title()


def _join_verified_cases(
    frozen: Mapping[str, Any], mapping: Mapping[str, Any], bundle_root: Path
) -> List[Dict[str, Any]]:
    frozen_by_id: Dict[str, Mapping[str, Any]] = {}
    for paper in frozen["papers"]:
        if not isinstance(paper, Mapping):
            raise RatioReportError("Frozen predictions contain an invalid entry")
        blind_id = paper.get("blind_id")
        if not isinstance(blind_id, str) or not _BLIND_ID.fullmatch(blind_id):
            raise RatioReportError("Frozen predictions contain an invalid blind_id")
        if blind_id in frozen_by_id:
            raise RatioReportError(f"Duplicate frozen blind_id: {blind_id}")
        frozen_by_id[blind_id] = paper
    if set(frozen_by_id) != set(_EXPECTED_IDS):
        raise RatioReportError("Frozen predictions must contain exactly B001 through B200")

    mapping_by_id: Dict[str, Mapping[str, Any]] = {}
    for paper in mapping["papers"]:
        if not isinstance(paper, Mapping):
            raise RatioReportError("Private mapping contains an invalid entry")
        blind_id = paper.get("blind_id")
        if not isinstance(blind_id, str) or not _BLIND_ID.fullmatch(blind_id):
            raise RatioReportError("Private mapping contains an invalid blind_id")
        if blind_id in mapping_by_id:
            raise RatioReportError(f"Duplicate private blind_id: {blind_id}")
        mapping_by_id[blind_id] = paper
    if set(mapping_by_id) != set(_EXPECTED_IDS):
        raise RatioReportError("Private mapping must contain exactly B001 through B200")

    cases: List[Dict[str, Any]] = []
    for blind_id in _EXPECTED_IDS:
        prediction = frozen_by_id[blind_id]
        private = mapping_by_id[blind_id]
        blind_hash = prediction.get("blind_text_sha256")
        if not isinstance(blind_hash, str) or not _SHA256.fullmatch(blind_hash):
            raise RatioReportError(f"{blind_id} frozen manuscript hash is invalid")
        if private.get("blind_text_sha256") != blind_hash:
            raise RatioReportError(f"{blind_id} mapping manuscript hash does not match")
        ground_truth = _parse_label(
            private.get("ground_truth"), field=f"{blind_id} ground truth"
        )
        frozen_scores = _parse_scores(
            prediction.get("individual_overall_scores"), blind_id=blind_id
        )
        frozen_decision_value = prediction.get("final_decision")
        frozen_decision = _parse_label(
            frozen_decision_value, field=f"{blind_id} frozen decision"
        )
        bundle_hash = prediction.get("review_bundle_sha256")
        if not isinstance(bundle_hash, str) or not _SHA256.fullmatch(bundle_hash):
            raise RatioReportError(f"{blind_id} frozen bundle hash is invalid")
        bundle_path = bundle_root / blind_id / "review_bundle.json"
        resolved_bundle, bundle_payload = _read_real_file(
            bundle_path, artifact=f"{blind_id} review bundle"
        )
        if resolved_bundle.parent.name != blind_id:
            raise RatioReportError(f"{blind_id} bundle path binding does not match")
        if _sha256_bytes(bundle_payload) != bundle_hash:
            raise RatioReportError(f"{blind_id} review bundle SHA-256 does not match")
        bundle = _decode_object(bundle_payload, artifact=f"{blind_id} review bundle")
        bundle_blind_hash, bundle_scores, bundle_decision_text = _bundle_projection(
            bundle, blind_id=blind_id
        )
        if bundle_blind_hash != blind_hash:
            raise RatioReportError(f"{blind_id} bundle manuscript hash does not match")
        if bundle_scores != frozen_scores:
            raise RatioReportError(f"{blind_id} frozen scores do not match its bundle")
        if _parse_label(bundle_decision_text, field=f"{blind_id} bundle decision") != frozen_decision:
            raise RatioReportError(f"{blind_id} frozen decision does not match its bundle")
        cases.append(
            {
                "blind_id": blind_id,
                "truth": ground_truth,
                "prediction": frozen_decision,
                "mean_score": sum(frozen_scores) / 5,
            }
        )
    return cases


def _auroc(truth: Sequence[int], scores: Sequence[float]) -> float:
    """Tie-aware Mann-Whitney AUROC using average ranks."""

    positives = sum(truth)
    negatives = len(truth) - positives
    if positives == 0 or negatives == 0:
        raise RatioReportError("AUROC requires both ground-truth classes")
    ordered = sorted(zip(scores, truth), key=lambda item: item[0])
    positive_rank_sum = 0.0
    index = 0
    while index < len(ordered):
        end = index + 1
        while end < len(ordered) and ordered[end][0] == ordered[index][0]:
            end += 1
        average_rank = ((index + 1) + end) / 2
        positive_rank_sum += average_rank * sum(label for _, label in ordered[index:end])
        index = end
    return (positive_rank_sum - positives * (positives + 1) / 2) / (
        positives * negatives
    )


def _metric_values(cases: Sequence[Mapping[str, Any]], *, prevalence: float) -> Dict[str, Any]:
    truth = [int(case["truth"]) for case in cases]
    predictions = [int(case["prediction"]) for case in cases]
    scores = [float(case["mean_score"]) for case in cases]
    tp = sum(t == 1 and p == 1 for t, p in zip(truth, predictions))
    tn = sum(t == 0 and p == 0 for t, p in zip(truth, predictions))
    fp = sum(t == 0 and p == 1 for t, p in zip(truth, predictions))
    fn = sum(t == 1 and p == 0 for t, p in zip(truth, predictions))
    positives = tp + fn
    negatives = tn + fp
    if positives == 0 or negatives == 0:
        raise RatioReportError("Every cohort must contain both ground-truth classes")
    tpr = tp / positives
    tnr = tn / negatives
    fpr = fp / negatives
    fnr = fn / positives
    raw_precision_denominator = tp + fp
    raw_precision = tp / raw_precision_denominator if raw_precision_denominator else 0.0
    raw_f1_denominator = 2 * tp + fp + fn
    weighted_tp = prevalence * tpr
    weighted_fp = (1 - prevalence) * fpr
    weighted_fn = prevalence * fnr
    standardized_precision_denominator = weighted_tp + weighted_fp
    standardized_f1_denominator = 2 * weighted_tp + weighted_fp + weighted_fn
    return {
        "class_conditional": {
            "balanced_accuracy": (tpr + tnr) / 2,
            "tpr": tpr,
            "tnr": tnr,
            "fpr": fpr,
            "fnr": fnr,
            "auroc": _auroc(truth, scores),
        },
        "raw": {
            "accuracy": (tp + tn) / len(cases),
            "precision": raw_precision,
            "f1": (2 * tp / raw_f1_denominator) if raw_f1_denominator else 0.0,
        },
        "prevalence_standardized": {
            "accuracy": weighted_tp + (1 - prevalence) * tnr,
            "precision": (
                weighted_tp / standardized_precision_denominator
                if standardized_precision_denominator
                else 0.0
            ),
            "f1": (
                2 * weighted_tp / standardized_f1_denominator
                if standardized_f1_denominator
                else 0.0
            ),
        },
        "confusion_matrix": {
            "labels": ["Reject", "Accept"],
            "matrix": [[tn, fp], [fn, tp]],
            "tn": tn,
            "fp": fp,
            "fn": fn,
            "tp": tp,
        },
    }


def _wilson_interval(successes: int, total: int, *, z: float = 1.959963984540054) -> Dict[str, float]:
    if isinstance(successes, bool) or isinstance(total, bool) or total < 1 or not 0 <= successes <= total:
        raise RatioReportError("Wilson interval requires 0 <= successes <= total")
    proportion = successes / total
    denominator = 1 + z * z / total
    center = (proportion + z * z / (2 * total)) / denominator
    margin = (
        z
        * math.sqrt(proportion * (1 - proportion) / total + z * z / (4 * total * total))
        / denominator
    )
    return {"lower": max(0.0, center - margin), "upper": min(1.0, center + margin)}


def _percentile(values: Sequence[float], probability: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise RatioReportError("Cannot compute a percentile of an empty sequence")
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def _flatten_metrics(result: Mapping[str, Any]) -> Dict[str, float]:
    return {
        "balanced_accuracy": result["class_conditional"]["balanced_accuracy"],
        "tpr": result["class_conditional"]["tpr"],
        "tnr": result["class_conditional"]["tnr"],
        "fpr": result["class_conditional"]["fpr"],
        "fnr": result["class_conditional"]["fnr"],
        "auroc": result["class_conditional"]["auroc"],
        "raw_accuracy": result["raw"]["accuracy"],
        "raw_precision": result["raw"]["precision"],
        "raw_f1": result["raw"]["f1"],
        "standardized_accuracy": result["prevalence_standardized"]["accuracy"],
        "standardized_precision": result["prevalence_standardized"]["precision"],
        "standardized_f1": result["prevalence_standardized"]["f1"],
    }


def _bootstrap_intervals(
    cases: Sequence[Mapping[str, Any]],
    *,
    prevalence: float,
    samples: int,
    seed: int,
) -> Dict[str, Dict[str, float]]:
    positive = [case for case in cases if case["truth"] == 1]
    negative = [case for case in cases if case["truth"] == 0]
    if not positive or not negative:
        raise RatioReportError("Stratified bootstrap requires both classes")
    generator = random.Random(seed)
    distributions: Dict[str, List[float]] = {}
    for _ in range(samples):
        sampled = [generator.choice(positive) for _ in positive]
        sampled.extend(generator.choice(negative) for _ in negative)
        flattened = _flatten_metrics(_metric_values(sampled, prevalence=prevalence))
        if not distributions:
            distributions = {name: [] for name in flattened}
        for name, value in flattened.items():
            distributions[name].append(value)
    return {
        name: {"lower": _percentile(values, 0.025), "upper": _percentile(values, 0.975)}
        for name, values in distributions.items()
    }


def _cohort_report(
    cases: Sequence[Mapping[str, Any]],
    *,
    prevalence: float,
    bootstrap_samples: int,
    bootstrap_seed: int,
) -> Dict[str, Any]:
    values = _metric_values(cases, prevalence=prevalence)
    confusion = values.pop("confusion_matrix")
    positives = confusion["tp"] + confusion["fn"]
    negatives = confusion["tn"] + confusion["fp"]
    return {
        "n_papers": len(cases),
        "n_accept": positives,
        "n_reject": negatives,
        "blind_ids": {"first": cases[0]["blind_id"], "last": cases[-1]["blind_id"]},
        "metrics": values,
        "confusion_matrix": confusion,
        "wilson_95": {
            "tpr": _wilson_interval(confusion["tp"], positives),
            "tnr": _wilson_interval(confusion["tn"], negatives),
            "fpr": _wilson_interval(confusion["fp"], negatives),
            "fnr": _wilson_interval(confusion["fn"], positives),
        },
        "bootstrap_95": _bootstrap_intervals(
            cases,
            prevalence=prevalence,
            samples=bootstrap_samples,
            seed=bootstrap_seed,
        ),
        "bootstrap": {
            "method": "ground-truth-stratified paper-level percentile bootstrap",
            "samples": bootstrap_samples,
            "seed": bootstrap_seed,
            "confidence_level": 0.95,
            "resampling_unit": "complete paper (decision plus five-review mean score)",
        },
    }


def build_real_ratio_report(
    frozen_predictions_path: Path,
    private_mapping_path: Path,
    bundle_root: Path,
    *,
    bootstrap_samples: int = DEFAULT_BOOTSTRAP_SAMPLES,
    bootstrap_seed: int = DEFAULT_BOOTSTRAP_SEED,
) -> Dict[str, Any]:
    """Build pilot, extension, and pooled reports for exactly 200 papers.

    ``bundle_root`` is the directory containing ``B001/review_bundle.json``
    through ``B200/review_bundle.json``.  Official prevalence is fixed to the
    paired 5,355 Accept and 8,408 Reject counts in the ICLR 2026 retrospective.
    """

    if isinstance(bootstrap_samples, bool) or not isinstance(bootstrap_samples, int) or bootstrap_samples < 1:
        raise RatioReportError("bootstrap_samples must be a positive integer")
    if isinstance(bootstrap_seed, bool) or not isinstance(bootstrap_seed, int):
        raise RatioReportError("bootstrap_seed must be an integer")
    frozen, frozen_hash, frozen_path = _load_verified_freeze(frozen_predictions_path)
    mapping, mapping_hash, mapping_path = _load_mapping(private_mapping_path)
    root = _validated_root(bundle_root)
    cases = _join_verified_cases(frozen, mapping, root)

    by_id = {case["blind_id"]: case for case in cases}
    cohorts: Dict[str, Any] = {}
    for name, ids in _COHORT_IDS.items():
        cohort_cases = [by_id[blind_id] for blind_id in _EXPECTED_IDS if blind_id in ids]
        observed_counts = {
            "Accept": sum(case["truth"] == 1 for case in cohort_cases),
            "Reject": sum(case["truth"] == 0 for case in cohort_cases),
        }
        if observed_counts != _EXPECTED_CLASS_COUNTS[name]:
            raise RatioReportError(
                f"{name} class counts must be {_EXPECTED_CLASS_COUNTS[name]}, found {observed_counts}"
            )
        cohorts[name] = _cohort_report(
            cohort_cases,
            prevalence=OFFICIAL_ACCEPT_PREVALENCE,
            bootstrap_samples=bootstrap_samples,
            bootstrap_seed=bootstrap_seed,
        )

    return {
        "format_version": REPORT_FORMAT_VERSION,
        "official_decision_prevalence": {
            "accept_count": OFFICIAL_ACCEPT_COUNT,
            "reject_count": OFFICIAL_REJECT_COUNT,
            "accept_prevalence": OFFICIAL_ACCEPT_PREVALENCE,
            "denominator": "Accept + Reject only",
            "source_url": "https://blog.iclr.cc/2026/03/31/a-retrospective-on-the-iclr-2026-review-process/",
        },
        "cohorts": cohorts,
        "audit": {
            "frozen_predictions_path": str(frozen_path),
            "frozen_predictions_sha256": frozen_hash,
            "private_mapping_path": str(mapping_path),
            "private_mapping_sha256": mapping_hash,
            "bundle_root": str(root),
            "verified_bundle_count": 200,
            "join_key": "blind_id plus blind_text_sha256",
            "bundle_binding": "review_bundle_sha256 plus frozen scores and final decision",
        },
    }


def write_real_ratio_report(output_path: Path, report: Mapping[str, Any]) -> Path:
    """Atomically write an already-built report with owner-only permissions."""

    requested = Path(output_path).expanduser()
    if requested.is_symlink():
        raise RatioReportError("Report output path must not be a symbolic link")
    destination = requested.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = (
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", dir=destination.parent
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
        destination.chmod(0o600)
    except Exception:
        try:
            os.close(descriptor)
        except OSError:
            pass
        temporary.unlink(missing_ok=True)
        raise
    return destination
