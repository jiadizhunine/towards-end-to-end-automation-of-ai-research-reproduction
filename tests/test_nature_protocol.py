import hashlib
import json
import threading
from types import SimpleNamespace

import pytest

from deepseek_autoreviewer.core import ReviewerConfig, review_text
from deepseek_autoreviewer.nature_protocol import (
    NATURE_META_REVIEWER_SYSTEM_PROMPT,
    NATURE_NEURIPS_FORM,
    NATURE_NEURIPS_FORM_SHA256,
    NATURE_PROTOCOL_ID,
    NATURE_REVIEWER_SYSTEM_PROMPT,
    TEMPLATE_INSTRUCTIONS,
    TEMPLATE_INSTRUCTIONS_SHA256,
    build_nature_meta_review_prompt,
    nature_protocol_record,
)


def make_review(overall=7, decision="Accept"):
    return {
        "Summary": "The paper studies a concrete machine-learning problem.",
        "Strengths": ["The experimental protocol is clearly specified."],
        "Weaknesses": ["External validity remains limited."],
        "Originality": 3,
        "Quality": 3,
        "Clarity": 3,
        "Significance": 3,
        "Questions": ["How stable are the results across seeds?"],
        "Limitations": ["Only one benchmark family is studied."],
        "Ethical Concerns": False,
        "Soundness": 3,
        "Presentation": 3,
        "Contribution": 3,
        "Overall": overall,
        "Confidence": 4,
        "Decision": decision,
    }


class ThoughtCompletions:
    def __init__(self):
        self.calls = []
        self.lock = threading.Lock()

    def create(self, **kwargs):
        with self.lock:
            index = len(self.calls)
            self.calls.append(kwargs)
        if index < 5:
            review = make_review(overall=(2, 4, 6, 8, 10)[index])
        else:
            review = make_review(overall=1, decision="Reject")
        content = (
            "THOUGHT:\nA paper-specific visible review note.\n\n"
            "REVIEW JSON:\n```json\n"
            f"{json.dumps(review)}\n```"
        )
        return SimpleNamespace(
            id=f"nature-{index}",
            choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
            usage={
                "prompt_tokens": 100,
                "completion_tokens": 50,
                "total_tokens": 150,
            },
        )


class ThoughtClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=ThoughtCompletions())


def nature_config(**overrides):
    values = {
        "protocol": NATURE_PROTOCOL_ID,
        "aggregate_scores": "mean",
        "reasoning_effort": "none",
        "retry_base_seconds": 0,
    }
    values.update(overrides)
    return ReviewerConfig(**values)


def test_frozen_full_form_hashes_and_si_prompt_text():
    assert hashlib.sha256(TEMPLATE_INSTRUCTIONS.encode("utf-8")).hexdigest() == (
        TEMPLATE_INSTRUCTIONS_SHA256
    )
    assert hashlib.sha256(NATURE_NEURIPS_FORM.encode("utf-8")).hexdigest() == (
        NATURE_NEURIPS_FORM_SHA256
    )
    assert len(TEMPLATE_INSTRUCTIONS.encode("utf-8")) == 1825
    assert len(NATURE_NEURIPS_FORM.encode("utf-8")) == 8896
    assert NATURE_REVIEWER_SYSTEM_PROMPT == (
        "You are an AI researcher who is reviewing a paper that was submitted "
        "to a prestigious ML venue."
    )
    assert "Be critical" not in NATURE_REVIEWER_SYSTEM_PROMPT


def test_nature_request_prompt_parsing_and_score_aggregation():
    client = ThoughtClient()
    bundle = review_text("paper text " * 200, client=client, config=nature_config())

    calls = client.chat.completions.calls
    assert len(calls) == 6
    for call in calls:
        assert call["temperature"] == 0.75
        assert call["extra_body"] == {"thinking": {"type": "disabled"}}
        assert "reasoning_effort" not in call
        assert "response_format" not in call
        assert "tools" not in call

    for call in calls[:5]:
        assert call["messages"][0]["content"] == NATURE_REVIEWER_SYSTEM_PROMPT
        user_prompt = call["messages"][1]["content"]
        assert user_prompt.startswith("\n## Review Form")
        assert "THOUGHT:\n<THOUGHT>" in user_prompt
        assert "Here is the paper you are asked to review:" in user_prompt

    meta_call = calls[5]
    assert meta_call["messages"][0]["content"] == (
        NATURE_META_REVIEWER_SYSTEM_PROMPT.format(reviewer_count=5)
    )
    meta_prompt = meta_call["messages"][1]["content"]
    assert meta_prompt.startswith("Review 1/5:")
    assert meta_prompt.index("Review 5/5:") < meta_prompt.index("## Review Form")

    assert bundle["meta_review_model"]["review"]["Overall"] == 1
    assert bundle["meta_review_model"]["review"]["Decision"] == "Reject"
    assert bundle["final_review"]["Overall"] == 6
    assert bundle["final_review"]["Decision"] == "Reject"
    assert bundle["nature_result_views"] == {
        "authoritative_binary_decision_path": "meta_review_model.review.Decision",
        "authoritative_binary_decision": "Reject",
        "raw_area_chair_review_path": "meta_review_model.review",
        "public_code_rounded_mean_numeric_view_path": "final_review",
        "numeric_fields_overwritten_in_final_review": [
            "Originality",
            "Quality",
            "Clarity",
            "Significance",
            "Soundness",
            "Presentation",
            "Contribution",
            "Overall",
            "Confidence",
        ],
        "area_chair_text_fields_overwritten": False,
        "area_chair_decision_overwritten": False,
    }
    assert bundle["implementation"]["visible_thought_scaffold_saved"] is True
    assert bundle["protocol"]["fingerprint_sha256"] == nature_protocol_record(
        model="deepseek-v4-flash",
        max_output_tokens=16384,
        max_attempts=3,
        ensemble_size=5,
        parallelism=5,
    )["fingerprint_sha256"]
    assert "temperature=0.75" in bundle["protocol"]["evidence_classification"][
        "public_code_adapter"
    ]


def test_nature_meta_prompt_keeps_raw_reviews_before_full_form():
    prompt = build_nature_meta_review_prompt([make_review(), make_review()])
    assert prompt.startswith("Review 1/2:")
    assert prompt.index("Review 2/2:") < prompt.index("## Review Form")
    assert prompt.endswith(TEMPLATE_INSTRUCTIONS)


def test_nature_protocol_rejects_drifted_ensemble_or_aggregation():
    with pytest.raises(ValueError, match="exactly five"):
        nature_config(ensemble_size=4).validate()
    with pytest.raises(ValueError, match="rounded-mean"):
        nature_config(aggregate_scores="meta").validate()
