import importlib.util
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "render_nature_comparison_table.py"
)
SPEC = importlib.util.spec_from_file_location(
    "render_nature_comparison_table", SCRIPT_PATH
)
assert SPEC is not None and SPEC.loader is not None
render_module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = render_module
SPEC.loader.exec_module(render_module)


def row(label: str, suffix: str):
    return {
        "label": label,
        "balanced_accuracy": f"0.50 {suffix}",
        "accuracy": f"0.60 {suffix}",
        "f1": f"0.40 {suffix}",
        "auc": f"0.55 {suffix}",
        "fpr": f"0.20 {suffix}",
        "fnr": f"0.80 {suffix}",
    }


def comparison_spec():
    return {
        "title": "Table 1 | Two-cohort comparison",
        "groups": [
            {
                "label": "ICLR 2026 (same 200-paper cohort)",
                "rows": [
                    row("Human review aggregate", "± 0.01"),
                    row("Always reject", ""),
                    row("DeepSeek V4 Flash", "± 0.02"),
                ],
            },
            {
                "label": "Published reference",
                "rows": [
                    row("Always reject (ICLR 2025)", ""),
                    row("Automated Reviewer (ICLR 2025)", "± 0.03"),
                    row("Human (NeurIPS 2021)", ""),
                ],
            },
        ],
        "caption": (
            "Values are display strings supplied by the analysis step. Reference "
            "rows come from a different cohort and are included for context only. "
        )
        * 3,
    }


def test_render_supports_two_groups_six_rows_and_exact_columns():
    svg = render_module.render(comparison_spec())
    root = ET.fromstring(svg)

    assert root.attrib["width"] == "1310"
    assert 'fill="#fff"' in svg
    assert "font-family: Arial, Helvetica, sans-serif" in svg
    assert 'font-family="Helvetica"' in svg
    assert 'font-weight="700"' in svg
    for header in (
        "Reviewer",
        "Balanced accuracy",
        "Accuracy",
        "F1",
        "AUC",
        "FPR",
        "FNR",
    ):
        assert header in svg
    assert "ICLR 2026 (same 200-paper cohort)" in svg
    assert "Published reference" in svg
    assert "Human review aggregate" in svg
    assert "Always reject (ICLR 2025)" in svg
    assert "Automated Reviewer (ICLR 2025)" in svg
    assert "0.50 ± 0.01" in svg

    namespace = {"svg": "http://www.w3.org/2000/svg"}
    lines = root.findall("svg:line", namespace)
    assert lines
    assert all(line.attrib["y1"] == line.attrib["y2"] for line in lines)

    captions = [
        element
        for element in root.findall("svg:text", namespace)
        if element.attrib.get("class") == "caption"
    ]
    assert len(captions) >= 2


def test_validation_rejects_more_than_two_groups_or_six_rows():
    too_many_groups = comparison_spec()
    too_many_groups["groups"].append(
        {"label": "Third group", "rows": [row("Another reviewer", "")]}
    )
    with pytest.raises(ValueError, match="between 1 and 2"):
        render_module.render(too_many_groups)

    too_many_rows = comparison_spec()
    too_many_rows["groups"][1]["rows"].append(row("Seventh reviewer", ""))
    with pytest.raises(ValueError, match="at most 6 rows"):
        render_module.render(too_many_rows)


def test_metric_values_must_be_non_empty_display_strings():
    missing_metric = comparison_spec()
    del missing_metric["groups"][0]["rows"][0]["auc"]
    with pytest.raises(ValueError, match=r"rows\[0\]\.auc"):
        render_module.render(missing_metric)

    numeric_metric = comparison_spec()
    numeric_metric["groups"][0]["rows"][0]["f1"] = 0.42
    with pytest.raises(ValueError, match=r"rows\[0\]\.f1"):
        render_module.render(numeric_metric)


def test_atomic_write_defaults_to_no_overwrite(tmp_path: Path):
    svg = render_module.render(comparison_spec())
    output = tmp_path / "comparison.svg"
    render_module.write_svg(output, svg)
    assert output.read_text(encoding="utf-8") == svg

    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        render_module.write_svg(output, svg)

    replacement = svg.replace("Two-cohort", "Replacement")
    render_module.write_svg(output, replacement, overwrite=True)
    assert output.read_text(encoding="utf-8") == replacement
