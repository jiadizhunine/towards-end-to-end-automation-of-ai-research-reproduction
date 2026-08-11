import importlib.util
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "render_nature_table1.py"
SPEC = importlib.util.spec_from_file_location("render_nature_table1", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
render_module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = render_module
SPEC.loader.exec_module(render_module)


def evaluation(*, use_positive_names: bool = True):
    value = {
        "n_papers": 10,
        "metrics": {
            "balanced_accuracy": 0.537,
            "accuracy": 0.61,
            "f1": 0.376,
            "auroc": 0.586,
            "fpr": 0.246,
            "fnr": 0.679,
        },
        "confidence_intervals_95": {
            "balanced_accuracy": {"lower": 0.47, "upper": 0.61},
            "accuracy": {"lower": 0.52, "upper": 0.70},
            "f1": {"lower": 0.28, "upper": 0.48},
            "auroc": {"lower": 0.50, "upper": 0.67},
            "fpr": {"lower": 0.18, "upper": 0.33},
            "fnr": {"lower": 0.57, "upper": 0.77},
        },
        "bootstrap": {
            "method": "stratified paper-level percentile bootstrap",
            "samples": 5000,
        },
    }
    if use_positive_names:
        value.update(n_positive=4, n_negative=6)
    else:
        value.update(n_accept=4, n_reject=6)
    return value


def test_render_has_only_real_rows_nature_columns_and_computed_baseline():
    svg = render_module.render(
        evaluation(),
        reviewer="DeepSeek V4 Flash AutoReviewer",
        title="Table 1 | Mixed-version evaluation",
    )

    ET.fromstring(svg)
    assert 'fill="#fff"' in svg
    assert "Reviewer" in svg
    assert "Balanced accuracy" in svg
    assert "Accuracy" in svg
    assert "F1" in svg
    assert "AUC" in svg
    assert "FPR" in svg
    assert "FNR" in svg
    assert "Always reject" in svg
    assert "DeepSeek V4 Flash AutoReviewer" in svg
    assert "Human" not in svg
    assert "Random" not in svg

    # Always reject: BA=.50, accuracy=6/10=.60, F1=0, AUC=.50,
    # FPR=0, and FNR=1. AutoReviewer BA: .537 +/- (.61-.47)/2.
    assert "0.60" in svg
    assert "0.54 ± 0.07" in svg
    assert "0.59 ± 0.09" in svg
    assert "5,000 replicates" in svg

    # Nature-style rules are horizontal only; no vertical grid is emitted.
    root = ET.fromstring(svg)
    namespace = {"svg": "http://www.w3.org/2000/svg"}
    lines = root.findall("svg:line", namespace)
    assert lines
    assert all(line.attrib["y1"] == line.attrib["y2"] for line in lines)


def test_accept_reject_count_schema_and_atomic_no_overwrite(tmp_path: Path):
    svg = render_module.render(
        evaluation(use_positive_names=False), reviewer="Strict all-initial run"
    )
    output = tmp_path / "table.svg"
    render_module.write_svg(output, svg)
    assert output.read_text(encoding="utf-8") == svg
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        render_module.write_svg(output, svg)


def test_invalid_interval_or_conflicting_counts_fail_closed():
    invalid_interval = evaluation()
    invalid_interval["confidence_intervals_95"]["fpr"] = {
        "lower": 0.9,
        "upper": 0.1,
    }
    with pytest.raises(ValueError, match="lower > upper"):
        render_module.render(invalid_interval, reviewer="AutoReviewer")

    conflicting_counts = evaluation()
    conflicting_counts.update(n_accept=5, n_reject=5)
    with pytest.raises(ValueError, match="counts disagree"):
        render_module.render(conflicting_counts, reviewer="AutoReviewer")
