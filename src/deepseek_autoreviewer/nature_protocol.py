"""Frozen Nature AutoReviewer protocol used only by explicit opt-in runs.

The paper's Supplementary Information (A.3) is authoritative for the
reviewer and Area Chair system prompts and for prompt ordering.  The complete
NeurIPS form is frozen from the authors' public implementation at the commit
recorded below.  Keeping this separate from :mod:`prompts` prevents a formal
comparison run from silently changing the repository's existing strict
JSON-only protocol.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Mapping


LEGACY_PROTOCOL_ID = "strict-json-v1"
NATURE_PROTOCOL_ID = "nature-si-a3-base-v1"
NATURE_TEMPERATURE = 0.75

NATURE_SUPPLEMENT_URL = (
    "https://media.springernature.com/original/springer-static/esm/"
    "art%3A10.1038%2Fs41586-026-10265-5/"
    "MediaObjects/41586_2026_10265_MOESM1_ESM.pdf"
)
SAKANA_SOURCE_COMMIT = "6e8260925d17e1a0f6509751c19a9e1a481035b2"
SAKANA_SOURCE_PATH = "ai_scientist/perform_llm_review.py"
SAKANA_SOURCE_SHA256 = "1dbca6776334270867703fd4f3369ceae9adb085ec8a45f07f7b191ffa20fab5"
SAKANA_SOURCE_URL = (
    "https://github.com/SakanaAI/AI-Scientist-v2/blob/"
    f"{SAKANA_SOURCE_COMMIT}/{SAKANA_SOURCE_PATH}"
)


# Supplementary Information A.3, p. 62.  Deliberately do not append the
# public implementation's additional "Be critical..." sentence: the SI's
# reported base condition contains only this sentence.
NATURE_REVIEWER_SYSTEM_PROMPT = (
    "You are an AI researcher who is reviewing a paper that was submitted "
    "to a prestigious ML venue."
)


# Supplementary Information A.3, p. 63.  Line breaks are retained from the SI
# display rather than replaced with the public implementation's compact text.
NATURE_META_REVIEWER_SYSTEM_PROMPT = """You are an Area Chair at a machine learning conference.
You are in charge of meta-reviewing a paper that was reviewed by
{reviewer_count} reviewers.
Your job is to aggregate the reviews into a single meta-review in the
same format.
Be critical and cautious in your decision, find consensus, and respect
the opinion of all the reviewers."""


# Exact Python string value from the pinned SakanaAI implementation.  Leading
# and trailing newlines are intentional and covered by the hashes below.
TEMPLATE_INSTRUCTIONS = """
Respond in the following format:

THOUGHT:
<THOUGHT>

REVIEW JSON:
```json
<JSON>
```

In <THOUGHT>, first briefly discuss your intuitions and reasoning for the evaluation.
Detail your high-level arguments, necessary choices and desired outcomes of the review.
Do not make generic comments here, but be specific to your current paper.
Treat this as the note-taking phase of your review.

In <JSON>, provide the review in JSON format with the following fields in the order:
- "Summary": A summary of the paper content and its contributions.
- "Strengths": A list of strengths of the paper.
- "Weaknesses": A list of weaknesses of the paper.
- "Originality": A rating from 1 to 4 (low, medium, high, very high).
- "Quality": A rating from 1 to 4 (low, medium, high, very high).
- "Clarity": A rating from 1 to 4 (low, medium, high, very high).
- "Significance": A rating from 1 to 4 (low, medium, high, very high).
- "Questions": A set of clarifying questions to be answered by the paper authors.
- "Limitations": A set of limitations and potential negative societal impacts of the work.
- "Ethical Concerns": A boolean value indicating whether there are ethical concerns.
- "Soundness": A rating from 1 to 4 (poor, fair, good, excellent).
- "Presentation": A rating from 1 to 4 (poor, fair, good, excellent).
- "Contribution": A rating from 1 to 4 (poor, fair, good, excellent).
- "Overall": A rating from 1 to 10 (very strong reject to award quality).
- "Confidence": A rating from 1 to 5 (low, medium, high, very high, absolute).
- "Decision": A decision that has to be one of the following: Accept, Reject.

For the "Decision" field, don't use Weak Accept, Borderline Accept, Borderline Reject, or Strong Reject. Instead, only use Accept or Reject.
This JSON will be automatically parsed, so ensure the format is precise.
"""


NEURIPS_FORM_BODY = """
## Review Form
Below is a description of the questions you will be asked on the review form for each paper and some guidelines on what to consider when answering these questions.
When writing your review, please keep in mind that after decisions have been made, reviews and meta-reviews of accepted papers and opted-in rejected papers will be made public.

1. Summary: Briefly summarize the paper and its contributions. This is not the place to critique the paper; the authors should generally agree with a well-written summary.
  - Strengths and Weaknesses: Please provide a thorough assessment of the strengths and weaknesses of the paper, touching on each of the following dimensions:
  - Originality: Are the tasks or methods new? Is the work a novel combination of well-known techniques? (This can be valuable!) Is it clear how this work differs from previous contributions? Is related work adequately cited
  - Quality: Is the submission technically sound? Are claims well supported (e.g., by theoretical analysis or experimental results)? Are the methods used appropriate? Is this a complete piece of work or work in progress? Are the authors careful and honest about evaluating both the strengths and weaknesses of their work
  - Clarity: Is the submission clearly written? Is it well organized? (If not, please make constructive suggestions for improving its clarity.) Does it adequately inform the reader? (Note that a superbly written paper provides enough information for an expert reader to reproduce its results.)
  - Significance: Are the results important? Are others (researchers or practitioners) likely to use the ideas or build on them? Does the submission address a difficult task in a better way than previous work? Does it advance the state of the art in a demonstrable way? Does it provide unique data, unique conclusions about existing data, or a unique theoretical or experimental approach?

2. Questions: Please list up and carefully describe any questions and suggestions for the authors. Think of the things where a response from the author can change your opinion, clarify a confusion or address a limitation. This can be very important for a productive rebuttal and discussion phase with the authors.

3. Limitations: Have the authors adequately addressed the limitations and potential negative societal impact of their work? If not, please include constructive suggestions for improvement.
In general, authors should be rewarded rather than punished for being up front about the limitations of their work and any potential negative societal impact. You are encouraged to think through whether any critical points are missing and provide these as feedback for the authors.

4. Ethical concerns: If there are ethical issues with this paper, please flag the paper for an ethics review. For guidance on when this is appropriate, please review the NeurIPS ethics guidelines.

5. Soundness: Please assign the paper a numerical rating on the following scale to indicate the soundness of the technical claims, experimental and research methodology and on whether the central claims of the paper are adequately supported with evidence.
  4: excellent
  3: good
  2: fair
  1: poor

6. Presentation: Please assign the paper a numerical rating on the following scale to indicate the quality of the presentation. This should take into account the writing style and clarity, as well as contextualization relative to prior work.
  4: excellent
  3: good
  2: fair
  1: poor

7. Contribution: Please assign the paper a numerical rating on the following scale to indicate the quality of the overall contribution this paper makes to the research area being studied. Are the questions being asked important? Does the paper bring a significant originality of ideas and/or execution? Are the results valuable to share with the broader NeurIPS community.
  4: excellent
  3: good
  2: fair
  1: poor

8. Overall: Please provide an "overall score" for this submission. Choices:
  10: Award quality: Technically flawless paper with groundbreaking impact on one or more areas of AI, with exceptionally strong evaluation, reproducibility, and resources, and no unaddressed ethical considerations.
  9: Very Strong Accept: Technically flawless paper with groundbreaking impact on at least one area of AI and excellent impact on multiple areas of AI, with flawless evaluation, resources, and reproducibility, and no unaddressed ethical considerations.
  8: Strong Accept: Technically strong paper with, with novel ideas, excellent impact on at least one area of AI or high-to-excellent impact on multiple areas of AI, with excellent evaluation, resources, and reproducibility, and no unaddressed ethical considerations.
  7: Accept: Technically solid paper, with high impact on at least one sub-area of AI or moderate-to-high impact on more than one area of AI, with good-to-excellent evaluation, resources, reproducibility, and no unaddressed ethical considerations.
  6: Weak Accept: Technically solid, moderate-to-high impact paper, with no major concerns with respect to evaluation, resources, reproducibility, ethical considerations.
  5: Borderline accept: Technically solid paper where reasons to accept outweigh reasons to reject, e.g., limited evaluation. Please use sparingly.
  4: Borderline reject: Technically solid paper where reasons to reject, e.g., limited evaluation, outweigh reasons to accept, e.g., good evaluation. Please use sparingly.
  3: Reject: For instance, a paper with technical flaws, weak evaluation, inadequate reproducibility and incompletely addressed ethical considerations.
  2: Strong Reject: For instance, a paper with major technical flaws, and/or poor evaluation, limited impact, poor reproducibility and mostly unaddressed ethical considerations.
  1: Very Strong Reject: For instance, a paper with trivial results or unaddressed ethical considerations

9. Confidence:  Please provide a "confidence score" for your assessment of this submission to indicate how confident you are in your evaluation. Choices:
  5: You are absolutely certain about your assessment. You are very familiar with the related work and checked the math/other details carefully.
  4: You are confident in your assessment, but not absolutely certain. It is unlikely, but not impossible, that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work.
  3: You are fairly confident in your assessment. It is possible that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.
  2: You are willing to defend your assessment, but it is quite likely that you did not understand the central parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.
  1: Your assessment is an educated guess. The submission is not in your area or the submission was difficult to understand. Math/other details were not carefully checked.
"""


NATURE_NEURIPS_FORM = NEURIPS_FORM_BODY + TEMPLATE_INSTRUCTIONS

NATURE_REVIEW_USER_SUFFIX_TEMPLATE = """
Here is the paper you are asked to review:
```
{paper}
```"""
NATURE_META_REVIEW_BLOCK_TEMPLATE = """Review {index}/{reviewer_count}:
```
{review_json}
```"""

TEMPLATE_INSTRUCTIONS_SHA256 = "6b87f348d08954f46f2c4c0b22766f7a4b8c794c7a376d82a099cb357e551961"
NATURE_NEURIPS_FORM_SHA256 = "41493738fed244dca9ec241875f3ea41d0fb8eaac6cd5f8cdf58b35a0dc3ffd2"


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _canonical_sha256(value: Mapping[str, Any]) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def protocol_record_fingerprint(record: Mapping[str, Any]) -> str:
    """Recompute a record fingerprint without trusting its stored digest."""

    material = dict(record)
    material.pop("fingerprint_sha256", None)
    return _canonical_sha256(material)


def validate_nature_protocol_record(record: Mapping[str, Any]) -> None:
    """Validate the self-hash and frozen static components of a run record."""

    if record.get("protocol_id") != NATURE_PROTOCOL_ID:
        raise ValueError("Nature protocol id mismatch")
    stored = record.get("fingerprint_sha256")
    if stored != protocol_record_fingerprint(record):
        raise ValueError("Nature protocol record fingerprint mismatch")
    prompt_hashes = record.get("prompt_sha256")
    if not isinstance(prompt_hashes, Mapping):
        raise ValueError("Nature protocol prompt hashes are missing")
    if prompt_hashes.get("template_instructions") != TEMPLATE_INSTRUCTIONS_SHA256:
        raise ValueError("Nature template instructions hash mismatch")
    if (
        prompt_hashes.get("neurips_form_with_output_instructions")
        != NATURE_NEURIPS_FORM_SHA256
    ):
        raise ValueError("Nature NeurIPS form hash mismatch")
    expected_static_hashes = {
        "reviewer_system": _sha256_text(NATURE_REVIEWER_SYSTEM_PROMPT),
        "area_chair_system_template": _sha256_text(
            NATURE_META_REVIEWER_SYSTEM_PROMPT
        ),
        "review_user_suffix_template": _sha256_text(
            NATURE_REVIEW_USER_SUFFIX_TEMPLATE
        ),
        "area_chair_review_block_template": _sha256_text(
            NATURE_META_REVIEW_BLOCK_TEMPLATE
        ),
    }
    if any(prompt_hashes.get(key) != value for key, value in expected_static_hashes.items()):
        raise ValueError("Nature static prompt template hash mismatch")
    sources = record.get("sources")
    if not isinstance(sources, Mapping) or sources.get(
        "frozen_source_file_sha256"
    ) != SAKANA_SOURCE_SHA256:
        raise ValueError("Nature frozen source provenance mismatch")
    pipeline = record.get("pipeline")
    if not isinstance(pipeline, Mapping) or pipeline.get("independent_reviewers") != 5:
        raise ValueError("Nature protocol must contain five independent reviewers")
    if pipeline.get("area_chair_meta_reviews") != 1:
        raise ValueError("Nature protocol must contain one Area Chair meta-review")
    request = record.get("effective_request")
    if not isinstance(request, Mapping):
        raise ValueError("Nature effective request is missing")
    if request.get("temperature") != NATURE_TEMPERATURE:
        raise ValueError("Nature adapter temperature mismatch")
    if request.get("extra_body") != {"thinking": {"type": "disabled"}}:
        raise ValueError("Nature adapter thinking policy mismatch")
    if request.get("omitted_fields") != [
        "reasoning_effort",
        "response_format",
        "tools",
    ]:
        raise ValueError("Nature adapter omitted-field policy mismatch")


def validate_frozen_prompt_hashes() -> None:
    """Fail closed if a prompt literal changes without a protocol revision."""

    if _sha256_text(TEMPLATE_INSTRUCTIONS) != TEMPLATE_INSTRUCTIONS_SHA256:
        raise RuntimeError("Frozen Nature template_instructions hash mismatch")
    if _sha256_text(NATURE_NEURIPS_FORM) != NATURE_NEURIPS_FORM_SHA256:
        raise RuntimeError("Frozen Nature NeurIPS form hash mismatch")


def build_nature_review_prompt(paper_text: str) -> str:
    """Build the SI base-condition prompt; few-shot examples are empty."""

    validate_frozen_prompt_hashes()
    return NATURE_NEURIPS_FORM + NATURE_REVIEW_USER_SUFFIX_TEMPLATE.format(
        paper=paper_text
    )


def build_nature_meta_review_prompt(reviews: List[Dict[str, Any]]) -> str:
    """Build the SI Area Chair user prompt (reviews first, then form)."""

    validate_frozen_prompt_hashes()
    blocks = []
    for index, review in enumerate(reviews, start=1):
        blocks.append(
            NATURE_META_REVIEW_BLOCK_TEMPLATE.format(
                index=index,
                reviewer_count=len(reviews),
                review_json=json.dumps(review, ensure_ascii=False),
            )
        )
    return "\n\n".join(blocks) + "\n\n" + NATURE_NEURIPS_FORM


def nature_protocol_record(
    *,
    model: str,
    max_output_tokens: int,
    max_attempts: int,
    ensemble_size: int,
    parallelism: int,
) -> Dict[str, Any]:
    """Return the hash-bound protocol and effective non-message request fields."""

    validate_frozen_prompt_hashes()
    record: Dict[str, Any] = {
        "protocol_id": NATURE_PROTOCOL_ID,
        "claim_scope": (
            "Nature-aligned DeepSeek adapter; not an exact reproduction of "
            "unreported Nature sampling parameters"
        ),
        "evidence_classification": {
            "paper_declared": [
                "base-condition reviewer system prompt",
                "reviewer user-prompt structure with NeurIPS guidelines and no few-shot examples",
                "five independent reviews plus one Area Chair meta-review",
                "raw Area Chair Decision is the final binary decision",
                "base condition uses no few-shot, Reflexion, or VLM",
            ],
            "public_code_adapter": [
                "expanded NeurIPS form text and visible THOUGHT/REVIEW JSON contract",
                "temperature=0.75",
                "rounded reviewer mean overwrites final numerical score fields",
            ],
            "deepseek_adapter_choice_not_reported_by_paper": [
                "thinking disabled",
                "reasoning_effort, response_format, and tools omitted",
                "five independent HTTP requests instead of an undocumented provider batch sampler",
                f"max_output_tokens={max_output_tokens}",
                f"max_attempts_per_call={max_attempts}",
                f"reviewer_parallelism={parallelism}",
            ],
            "not_set": ["random seed"],
        },
        "sources": {
            "supplementary_information": NATURE_SUPPLEMENT_URL,
            "frozen_form_implementation": SAKANA_SOURCE_URL,
            "frozen_form_commit": SAKANA_SOURCE_COMMIT,
            "frozen_form_path": SAKANA_SOURCE_PATH,
            "frozen_source_file_sha256": SAKANA_SOURCE_SHA256,
            "normalization": "exact Python string value, UTF-8, no newline normalization",
        },
        "prompt_sha256": {
            "reviewer_system": _sha256_text(NATURE_REVIEWER_SYSTEM_PROMPT),
            "area_chair_system_template": _sha256_text(
                NATURE_META_REVIEWER_SYSTEM_PROMPT
            ),
            "template_instructions": TEMPLATE_INSTRUCTIONS_SHA256,
            "neurips_form_with_output_instructions": NATURE_NEURIPS_FORM_SHA256,
            "review_user_suffix_template": _sha256_text(
                NATURE_REVIEW_USER_SUFFIX_TEMPLATE
            ),
            "area_chair_review_block_template": _sha256_text(
                NATURE_META_REVIEW_BLOCK_TEMPLATE
            ),
        },
        "prompt_policy": {
            "base_prompt": True,
            "few_shot_examples": 0,
            "reflexion_revision_passes": 0,
            "area_chair_user_order": "five reviews then full NeurIPS form",
            "visible_thought_then_review_json": True,
        },
        "pipeline": {
            "independent_reviewers": ensemble_size,
            "area_chair_meta_reviews": 1,
            "numeric_aggregation": "rounded arithmetic mean of five reviewers",
            "text_and_decision_source": "Area Chair meta-review",
        },
        "effective_request": {
            "model": model,
            "max_tokens": max_output_tokens,
            "temperature": NATURE_TEMPERATURE,
            "extra_body": {"thinking": {"type": "disabled"}},
            "omitted_fields": ["reasoning_effort", "response_format", "tools"],
        },
        "execution": {
            "max_attempts_per_call": max_attempts,
            "parallelism": parallelism,
            "complete_ensemble_required": True,
        },
    }
    record["fingerprint_sha256"] = protocol_record_fingerprint(record)
    return record


validate_frozen_prompt_hashes()
