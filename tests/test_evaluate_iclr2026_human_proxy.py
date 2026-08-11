import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "evaluate_iclr2026_human_proxy.py"
)
SPEC = importlib.util.spec_from_file_location(
    "evaluate_iclr2026_human_proxy", SCRIPT_PATH
)
assert SPEC is not None and SPEC.loader is not None
proxy = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = proxy
SPEC.loader.exec_module(proxy)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _build_inputs(tmp_path: Path):
    rows = []
    mapping_papers = []
    for index in range(1, 201):
        blind_id = f"B{index:03d}"
        paper_id = f"paper-{index:03d}"
        is_accept = index <= 78
        if is_accept:
            # 59 true positives, one threshold tie, and 18 other false negatives.
            rating = "6;6;6" if index <= 59 else ("4;5;6" if index == 60 else "4;4;4")
            decision = "Accept (Poster)"
        else:
            # 30 false positives and 92 true negatives.
            rating = "6;6;6" if index <= 108 else "4;4;4"
            decision = "Reject"
        rows.append(
            {
                "paper_id": paper_id,
                "scores": {"rating": rating},
                "decision": {"decision": decision},
            }
        )
        mapping_papers.append({"blind_id": blind_id, "paper_id": paper_id})

    parquet_path = tmp_path / "iclr2026-test.parquet"
    pq.write_table(pa.Table.from_pylist(rows), parquet_path)
    mapping_path = tmp_path / "mapping.json"
    mapping_path.write_text(
        json.dumps(
            {
                "format_version": proxy.MAPPING_FORMAT_VERSION,
                "source_parquet_sha256": _sha256(parquet_path),
                "source_row_count": 200,
                "papers": mapping_papers,
            }
        ),
        encoding="utf-8",
    )
    return parquet_path, mapping_path, rows, mapping_papers


def _rewrite_inputs(parquet_path, mapping_path, rows, mapping_papers):
    pq.write_table(pa.Table.from_pylist(rows), parquet_path)
    mapping_path.write_text(
        json.dumps(
            {
                "format_version": proxy.MAPPING_FORMAT_VERSION,
                "source_parquet_sha256": _sha256(parquet_path),
                "source_row_count": len(rows),
                "papers": mapping_papers,
            }
        ),
        encoding="utf-8",
    )


def test_build_report_is_deterministic_and_uses_strict_greater_than_five(tmp_path: Path):
    parquet_path, mapping_path, _, _ = _build_inputs(tmp_path)

    first = proxy.build_report(
        parquet_path, mapping_path, bootstrap_samples=32, bootstrap_seed=2026
    )
    second = proxy.build_report(
        parquet_path, mapping_path, bootstrap_samples=32, bootstrap_seed=2026
    )

    assert first == second
    assert first["n_papers"] == 200
    assert (first["n_accept"], first["n_reject"]) == (78, 122)
    assert first["mean_equal_to_5_count"] == 1
    assert first["confusion_matrix"] == {
        "labels": ["Reject", "Accept"],
        "matrix": [[92, 30], [19, 59]],
        "tn": 92,
        "fp": 30,
        "fn": 19,
        "tp": 59,
    }
    assert first["predicted_accept"] == 89
    assert set(first["metrics"]) == set(proxy.METRICS)
    assert set(first["confidence_intervals_95"]) == set(proxy.METRICS)
    assert first["metrics"]["balanced_accuracy"] == pytest.approx(
        ((59 / 78) + (92 / 122)) / 2
    )
    assert first["bootstrap"] == {
        "method": "ground-truth-stratified paper-level percentile bootstrap",
        "samples": 32,
        "seed": 2026,
        "confidence_level": 0.95,
    }
    assert "not" not in first["interpretation"]
    assert "Independent human-vs-human" in first["interpretation"]["not_valid_as"]


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("too_few_ratings", "between 3 and 5 human ratings"),
        ("missing_rating", "ratings must not be missing"),
        ("duplicate_blind_id", "Duplicate private blind_id"),
        ("wrong_class_count", "class counts must be"),
    ],
)
def test_fail_closed_invariants(tmp_path: Path, mutation: str, message: str):
    parquet_path, mapping_path, rows, mapping_papers = _build_inputs(tmp_path)
    if mutation == "too_few_ratings":
        rows[0]["scores"]["rating"] = "6;6"
    elif mutation == "missing_rating":
        rows[0]["scores"]["rating"] = "6;;6"
    elif mutation == "duplicate_blind_id":
        mapping_papers[1]["blind_id"] = "B001"
    elif mutation == "wrong_class_count":
        rows[77]["decision"]["decision"] = "Reject"
    _rewrite_inputs(parquet_path, mapping_path, rows, mapping_papers)

    with pytest.raises(proxy.HumanProxyError, match=message):
        proxy.build_report(parquet_path, mapping_path, bootstrap_samples=2)


def test_atomic_write_is_owner_only_and_refuses_overwrite(tmp_path: Path):
    destination = tmp_path / "proxy.json"
    proxy.write_report(destination, {"ok": True})
    assert json.loads(destination.read_text(encoding="utf-8")) == {"ok": True}
    assert destination.stat().st_mode & 0o777 == 0o600

    with pytest.raises(FileExistsError, match="Refusing to overwrite"):
        proxy.write_report(destination, {"ok": False})
    proxy.write_report(destination, {"ok": False}, overwrite=True)
    assert json.loads(destination.read_text(encoding="utf-8")) == {"ok": False}


def test_fixed_cli_defaults_and_bootstrap_contract():
    assert proxy.DEFAULT_BOOTSTRAP_SAMPLES == 5_000
    assert proxy.DEFAULT_BOOTSTRAP_SEED == 2026
    assert proxy._ratings("0;2;4", blind_id="B001") == (0.0, 2.0, 4.0)
    parser = proxy._parser()
    args = parser.parse_args(["--output", "result.json"])
    assert args.parquet == proxy.DEFAULT_PARQUET
    assert args.mapping == proxy.DEFAULT_MAPPING
    assert args.overwrite is False
