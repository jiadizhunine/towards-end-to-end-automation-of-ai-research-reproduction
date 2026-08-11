import hashlib
import json
from pathlib import Path

import pytest

from deepseek_autoreviewer.benchmark import BLINDING_VERSION, _binary_auroc
from deepseek_autoreviewer.ratio_report import (
    DEFAULT_BOOTSTRAP_SAMPLES,
    FREEZE_FORMAT_VERSION,
    OFFICIAL_ACCEPT_PREVALENCE,
    RatioReportError,
    _wilson_interval,
    build_real_ratio_report,
    write_real_ratio_report,
)


def _json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _build_artifacts(tmp_path: Path):
    bundle_root = tmp_path / "bundles"
    mapping_papers = []
    frozen_papers = []
    for index in range(1, 201):
        blind_id = f"B{index:03d}"
        accept = index <= 20 or 41 <= index <= 98
        prediction_accept = index % 2 == 0 if accept else index % 4 == 0
        ground_truth = "Accept" if accept else "Reject"
        decision = "Accept" if prediction_accept else "Reject"
        score = 8 if prediction_accept else 4
        blind_hash = hashlib.sha256(f"paper-{index}".encode()).hexdigest()
        bundle = {
            "input": {
                "blind_id": blind_id,
                "blind_text_sha256": blind_hash,
            },
            "individual_reviews": [
                {"review": {"Overall": score}} for _ in range(5)
            ],
            "final_review": {"Decision": decision},
        }
        bundle_payload = _json_bytes(bundle)
        bundle_dir = bundle_root / blind_id
        bundle_dir.mkdir(parents=True)
        (bundle_dir / "review_bundle.json").write_bytes(bundle_payload)
        mapping_papers.append(
            {
                "blind_id": blind_id,
                "blind_text_sha256": blind_hash,
                "ground_truth": ground_truth,
            }
        )
        frozen_papers.append(
            {
                "blind_id": blind_id,
                "blind_text_sha256": blind_hash,
                "individual_overall_scores": [score] * 5,
                "final_decision": decision,
                "review_bundle_sha256": _sha256(bundle_payload),
            }
        )

    mapping_path = tmp_path / "mapping.json"
    mapping_path.write_bytes(
        _json_bytes({"format_version": BLINDING_VERSION, "papers": mapping_papers})
    )
    frozen_path = tmp_path / "predictions.json"
    frozen_payload = _json_bytes(
        {
            "format_version": FREEZE_FORMAT_VERSION,
            "contains_ground_truth": False,
            "paper_count": 200,
            "papers": frozen_papers,
        }
    )
    frozen_path.write_bytes(frozen_payload)
    frozen_path.with_name(frozen_path.name + ".sha256").write_text(
        _sha256(frozen_payload) + "\n", encoding="ascii"
    )
    return frozen_path, mapping_path, bundle_root


def test_real_ratio_report_has_three_cohorts_and_deterministic_paper_bootstrap(
    tmp_path: Path,
):
    frozen_path, mapping_path, bundle_root = _build_artifacts(tmp_path)

    first = build_real_ratio_report(
        frozen_path,
        mapping_path,
        bundle_root,
        bootstrap_samples=64,
        bootstrap_seed=17,
    )
    second = build_real_ratio_report(
        frozen_path,
        mapping_path,
        bundle_root,
        bootstrap_samples=64,
        bootstrap_seed=17,
    )

    assert first == second
    assert first["audit"]["verified_bundle_count"] == 200
    assert first["official_decision_prevalence"]["accept_count"] == 5355
    assert first["official_decision_prevalence"]["reject_count"] == 8408
    assert {
        name: (cohort["n_papers"], cohort["n_accept"], cohort["n_reject"])
        for name, cohort in first["cohorts"].items()
    } == {
        "pilot": (40, 20, 20),
        "extension": (160, 58, 102),
        "pooled": (200, 78, 122),
    }
    pooled = first["cohorts"]["pooled"]
    assert pooled["confusion_matrix"] == {
        "labels": ["Reject", "Accept"],
        "matrix": [[91, 31], [39, 39]],
        "tn": 91,
        "fp": 31,
        "fn": 39,
        "tp": 39,
    }
    conditional = pooled["metrics"]["class_conditional"]
    assert conditional["tpr"] == 0.5
    assert conditional["tnr"] == pytest.approx(91 / 122)
    assert conditional["balanced_accuracy"] == pytest.approx((0.5 + 91 / 122) / 2)
    standardized = pooled["metrics"]["prevalence_standardized"]
    assert standardized["accuracy"] == pytest.approx(
        OFFICIAL_ACCEPT_PREVALENCE * 0.5
        + (1 - OFFICIAL_ACCEPT_PREVALENCE) * (91 / 122)
    )
    weighted_tp = OFFICIAL_ACCEPT_PREVALENCE * 0.5
    weighted_fp = (1 - OFFICIAL_ACCEPT_PREVALENCE) * (31 / 122)
    weighted_fn = OFFICIAL_ACCEPT_PREVALENCE * 0.5
    assert standardized["precision"] == pytest.approx(
        weighted_tp / (weighted_tp + weighted_fp)
    )
    assert standardized["f1"] == pytest.approx(
        2 * weighted_tp / (2 * weighted_tp + weighted_fp + weighted_fn)
    )
    assert set(pooled["bootstrap_95"]) == {
        "balanced_accuracy",
        "tpr",
        "tnr",
        "fpr",
        "fnr",
        "auroc",
        "raw_accuracy",
        "raw_precision",
        "raw_f1",
        "standardized_accuracy",
        "standardized_precision",
        "standardized_f1",
    }
    assert pooled["bootstrap"]["resampling_unit"].startswith("complete paper")


def test_real_ratio_report_fails_closed_on_sidecar_or_bundle_tampering(tmp_path: Path):
    frozen_path, mapping_path, bundle_root = _build_artifacts(tmp_path)
    sidecar = frozen_path.with_name(frozen_path.name + ".sha256")
    sidecar.write_text("0" * 64 + "\n", encoding="ascii")
    with pytest.raises(RatioReportError, match="SHA-256 verification failed"):
        build_real_ratio_report(
            frozen_path, mapping_path, bundle_root, bootstrap_samples=2
        )

    frozen_payload = frozen_path.read_bytes()
    sidecar.write_text(_sha256(frozen_payload) + "\n", encoding="ascii")
    bundle_path = bundle_root / "B001" / "review_bundle.json"
    bundle_path.write_bytes(bundle_path.read_bytes() + b" ")
    with pytest.raises(RatioReportError, match="review bundle SHA-256 does not match"):
        build_real_ratio_report(
            frozen_path, mapping_path, bundle_root, bootstrap_samples=2
        )


def test_real_ratio_report_rejects_wrong_cohort_class_counts(tmp_path: Path):
    frozen_path, mapping_path, bundle_root = _build_artifacts(tmp_path)
    mapping = json.loads(mapping_path.read_text())
    mapping["papers"][0]["ground_truth"] = "Reject"
    mapping_path.write_bytes(_json_bytes(mapping))

    with pytest.raises(RatioReportError, match="pilot class counts"):
        build_real_ratio_report(
            frozen_path, mapping_path, bundle_root, bootstrap_samples=2
        )


def test_wilson_interval_and_default_bootstrap_contract():
    assert DEFAULT_BOOTSTRAP_SAMPLES == 10_000
    interval = _wilson_interval(5, 10)
    assert interval["lower"] == pytest.approx(0.2365930905)
    assert interval["upper"] == pytest.approx(0.7634069095)
    zero = _wilson_interval(0, 10)
    assert zero["lower"] == 0.0
    assert 0 < zero["upper"] < 1


def test_tie_aware_auroc_matches_existing_benchmark_metric(tmp_path: Path):
    frozen_path, mapping_path, bundle_root = _build_artifacts(tmp_path)
    report = build_real_ratio_report(
        frozen_path, mapping_path, bundle_root, bootstrap_samples=2
    )
    pooled = report["cohorts"]["pooled"]
    truth = [1] * 78 + [0] * 122
    # The synthetic fixture assigns score 8 to predicted Accept and 4 to Reject.
    scores = [8] * 39 + [4] * 39 + [8] * 31 + [4] * 91
    assert pooled["metrics"]["class_conditional"]["auroc"] == pytest.approx(
        _binary_auroc(truth, scores)
    )


def test_write_real_ratio_report_is_json_and_owner_only(tmp_path: Path):
    destination = write_real_ratio_report(tmp_path / "report.json", {"ok": True})
    assert json.loads(destination.read_text()) == {"ok": True}
    assert destination.stat().st_mode & 0o777 == 0o600
