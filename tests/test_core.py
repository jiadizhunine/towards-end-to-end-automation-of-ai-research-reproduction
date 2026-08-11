import json
import threading
from pathlib import Path
from types import SimpleNamespace

import pymupdf
import pytest

from deepseek_autoreviewer.core import (
    ReviewerConfig,
    estimate_cost_usd,
    extract_pdf_text,
    parse_review_json,
    review_text,
)


def make_review(overall=7, decision="Accept"):
    return {
        "Summary": "The paper studies a concrete machine-learning problem.",
        "Strengths": ["The evaluation is clearly specified."],
        "Weaknesses": ["External validity is limited."],
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


class FakeCompletions:
    def __init__(self):
        self.lock = threading.Lock()
        self.calls = []

    def create(self, **kwargs):
        with self.lock:
            call_index = len(self.calls)
            self.calls.append(kwargs)
        review = make_review(overall=7 if call_index < 5 else 6)
        return SimpleNamespace(
            id=f"response-{call_index}",
            choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(review)))],
            usage={
                "prompt_tokens": 100,
                "prompt_cache_hit_tokens": 20,
                "prompt_cache_miss_tokens": 80,
                "completion_tokens": 50,
                "completion_tokens_details": {"reasoning_tokens": 30},
                "total_tokens": 150,
            },
        )


class FakeClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=FakeCompletions())


def test_parse_review_json_is_strict():
    parsed = parse_review_json(f"```json\n{json.dumps(make_review())}\n```")
    assert parsed["Decision"] == "Accept"

    invalid = make_review()
    invalid["Overall"] = 11
    with pytest.raises(ValueError, match="Overall"):
        parse_review_json(json.dumps(invalid))


def test_five_reviews_plus_meta_review_and_cost():
    client = FakeClient()
    config = ReviewerConfig(retry_base_seconds=0)
    bundle = review_text("paper text " * 200, client=client, config=config)

    assert len(bundle["individual_reviews"]) == 5
    assert len(client.chat.completions.calls) == 6
    assert bundle["meta_review_model"]["review"]["Overall"] == 6
    assert bundle["final_review"]["Overall"] == 6
    assert bundle["ensemble_summary"]["score_statistics"]["Overall"]["mean"] == 7
    assert bundle["usage"] == {
        "prompt_tokens": 600,
        "prompt_cache_hit_tokens": 120,
        "prompt_cache_miss_tokens": 480,
        "completion_tokens": 300,
        "reasoning_tokens": 180,
        "total_tokens": 900,
        "request_count": 6,
    }
    assert bundle["estimated_cost_usd"] == estimate_cost_usd(bundle["usage"], config)
    assert bundle["implementation"]["hidden_reasoning_saved"] is False
    for call in client.chat.completions.calls:
        assert call["model"] == "deepseek-v4-flash"
        assert call["reasoning_effort"] == "max"
        assert call["extra_body"] == {"thinking": {"type": "enabled"}}
        assert call["response_format"] == {"type": "json_object"}


def test_legacy_mean_score_policy_is_explicit():
    client = FakeClient()
    config = ReviewerConfig(aggregate_scores="mean", retry_base_seconds=0)
    bundle = review_text("paper text " * 200, client=client, config=config)
    assert bundle["meta_review_model"]["review"]["Overall"] == 6
    assert bundle["final_review"]["Overall"] == 7
    assert "rounded mean" in bundle["final_review_source"]


def test_pdf_extraction_records_hash_and_page_markers(tmp_path: Path):
    pdf_path = tmp_path / "sample.pdf"
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), "A compact scientific manuscript for extraction testing.")
    document.save(pdf_path)
    document.close()

    text, metadata = extract_pdf_text(pdf_path, min_characters=10)
    assert "Page 1" in text
    assert "scientific manuscript" in text
    assert metadata["page_count"] == 1
    assert len(metadata["sha256"]) == 64
    assert metadata["full_text_saved"] is False
