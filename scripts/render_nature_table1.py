#!/usr/bin/env python3
"""Render one evaluation JSON as a Nature Table 1-style SVG.

The renderer is intentionally data-only: it draws the analytical always-reject
baseline and the single AutoReviewer row present in the supplied evaluation.
It does not invent human, random, or literature-comparison rows.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import tempfile
import textwrap
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Mapping, Optional, Tuple
from xml.sax.saxutils import escape


WIDTH = 1310
COLUMN_X = (9, 275, 485, 659, 840, 1006, 1159)
METRICS = (
    "balanced_accuracy",
    "accuracy",
    "f1",
    "auroc",
    "fpr",
    "fnr",
)
HEADERS = (
    "Reviewer",
    "Balanced accuracy",
    "Accuracy",
    "F1",
    "AUC",
    "FPR",
    "FNR",
)
DEFAULT_TITLE = "Table 1 | AutoReviewer decision performance"


def _probability(value: Any, *, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be a number in [0, 1]")
    number = float(value)
    if not math.isfinite(number) or not 0.0 <= number <= 1.0:
        raise ValueError(f"{field} must be a finite number in [0, 1]")
    return number


def _positive_integer(value: Any, *, field: str, allow_zero: bool = False) -> int:
    minimum = 0 if allow_zero else 1
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        qualifier = "non-negative" if allow_zero else "positive"
        raise ValueError(f"{field} must be a {qualifier} integer")
    return value


def _round_2(value: float) -> str:
    return str(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _estimate_with_margin(
    estimate: Any,
    interval: Mapping[str, Any],
    *,
    metric: str,
) -> str:
    point = _probability(estimate, field=f"metrics.{metric}")
    if not isinstance(interval, Mapping):
        raise ValueError(f"confidence_intervals_95.{metric} must be an object")
    lower = _probability(
        interval.get("lower"), field=f"confidence_intervals_95.{metric}.lower"
    )
    upper = _probability(
        interval.get("upper"), field=f"confidence_intervals_95.{metric}.upper"
    )
    if lower > upper:
        raise ValueError(f"confidence_intervals_95.{metric} has lower > upper")
    half_width = (upper - lower) / 2
    return f"{_round_2(point)} ± {_round_2(half_width)}"


def _class_counts(evaluation: Mapping[str, Any]) -> Tuple[int, int, int]:
    """Return positive, negative, and total counts from either supported schema."""

    candidates = []
    if "n_positive" in evaluation or "n_negative" in evaluation:
        candidates.append(
            (
                _positive_integer(evaluation.get("n_positive"), field="n_positive"),
                _positive_integer(evaluation.get("n_negative"), field="n_negative"),
            )
        )
    if "n_accept" in evaluation or "n_reject" in evaluation:
        candidates.append(
            (
                _positive_integer(evaluation.get("n_accept"), field="n_accept"),
                _positive_integer(evaluation.get("n_reject"), field="n_reject"),
            )
        )
    if not candidates:
        raise ValueError(
            "evaluation must contain n_positive/n_negative or n_accept/n_reject"
        )
    if any(value != candidates[0] for value in candidates[1:]):
        raise ValueError("positive/negative and Accept/Reject counts disagree")

    n_positive, n_negative = candidates[0]
    calculated_total = n_positive + n_negative
    if "n_papers" in evaluation:
        n_papers = _positive_integer(evaluation.get("n_papers"), field="n_papers")
        if n_papers != calculated_total:
            raise ValueError("class counts must sum to n_papers")
    else:
        n_papers = calculated_total
    return n_positive, n_negative, n_papers


def _text(x: int, y: int, value: str, css_class: str) -> str:
    return f'<text x="{x}" y="{y}" class="{css_class}">{escape(value)}</text>'


def _line(y: int, *, width: float = 1.0) -> str:
    return (
        f'<line x1="0" y1="{y}" x2="{WIDTH}" y2="{y}" '
        f'stroke="#111" stroke-width="{width}"/>'
    )


def _caption_lines(
    *,
    evaluation: Mapping[str, Any],
    n_positive: int,
    n_negative: int,
) -> Tuple[str, ...]:
    sentences = [
        (
            "AutoReviewer entries are point estimates ± the average half-width "
            "of their 95% confidence intervals; exact bounds are in the source "
            "evaluation JSON."
        ),
        (
            f"Always reject is calculated analytically from {n_positive} positive "
            f"and {n_negative} negative cases; no human or random rows are imputed."
        ),
        "AUC, area under the ROC curve; FNR, false negative rate; FPR, false positive rate.",
    ]
    bootstrap = evaluation.get("bootstrap")
    if isinstance(bootstrap, Mapping):
        samples = bootstrap.get("samples")
        method = bootstrap.get("method")
        if (
            isinstance(samples, int)
            and not isinstance(samples, bool)
            and samples > 0
            and isinstance(method, str)
            and method.strip()
        ):
            sentences.insert(1, f"Confidence interval method: {method}; {samples:,} replicates.")
    wrapped = []
    for sentence in sentences:
        wrapped.extend(textwrap.wrap(sentence, width=142, break_long_words=False))
    return tuple(wrapped)


def render(
    evaluation: Mapping[str, Any],
    *,
    reviewer: str,
    title: str = DEFAULT_TITLE,
    cohort_label: Optional[str] = None,
) -> str:
    """Return a standalone SVG containing one baseline and one measured row."""

    if not isinstance(evaluation, Mapping):
        raise ValueError("evaluation must be a JSON object")
    if not isinstance(reviewer, str) or not reviewer.strip():
        raise ValueError("reviewer must be a non-empty string")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("title must be a non-empty string")

    metrics = evaluation.get("metrics")
    intervals = evaluation.get("confidence_intervals_95")
    if not isinstance(metrics, Mapping) or not isinstance(intervals, Mapping):
        raise ValueError("evaluation must contain metrics and confidence_intervals_95")
    missing_metrics = sorted(set(METRICS) - set(metrics))
    missing_intervals = sorted(set(METRICS) - set(intervals))
    if missing_metrics or missing_intervals:
        raise ValueError(
            f"missing metrics={missing_metrics}, missing confidence intervals={missing_intervals}"
        )

    n_positive, n_negative, n_papers = _class_counts(evaluation)
    if cohort_label is None:
        cohort_label = (
            f"Evaluation cohort ({n_papers} papers; {n_positive} positive, "
            f"{n_negative} negative)"
        )
    elif not isinstance(cohort_label, str) or not cohort_label.strip():
        raise ValueError("cohort_label must be a non-empty string")

    always_reject = (
        "Always reject",
        "0.50",
        _round_2(n_negative / n_papers),
        "0.00",
        "0.50",
        "0.00",
        "1.00",
    )
    autoreviewer = (
        reviewer.strip(),
        *(
            _estimate_with_margin(metrics[name], intervals[name], metric=name)
            for name in METRICS
        ),
    )

    caption_lines = _caption_lines(
        evaluation=evaluation,
        n_positive=n_positive,
        n_negative=n_negative,
    )
    caption_start_y = 239
    caption_line_height = 23
    height = caption_start_y + len(caption_lines) * caption_line_height + 18

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title.strip())}</title>',
        (
            '<desc id="desc">Nature Table 1-style decision metrics for '
            f'{escape(reviewer.strip())}, with an analytical always-reject baseline.</desc>'
        ),
        "<style>",
        (
            "text { fill: #111; font-family: Arial, Helvetica, sans-serif; "
            "font-variant-numeric: tabular-nums; }"
        ),
        ".title { font-size: 22px; font-weight: 700; }",
        ".header { font-size: 16px; font-weight: 700; }",
        ".body { font-size: 16px; font-weight: 400; }",
        ".caption { font-size: 15px; font-weight: 400; }",
        "</style>",
        f'<rect x="0" y="0" width="{WIDTH}" height="{height}" fill="#fff"/>',
        _line(1),
        _text(9, 36, title.strip(), "title"),
        _line(61),
    ]
    parts.extend(_text(x, 85, value, "header") for x, value in zip(COLUMN_X, HEADERS))
    parts.extend(
        (
            _line(96),
            _text(9, 121, cohort_label.strip(), "body"),
            _line(133),
        )
    )

    for row_y, rule_y, row in ((158, 170, always_reject), (195, 207, autoreviewer)):
        parts.extend(_text(x, row_y, value, "body") for x, value in zip(COLUMN_X, row))
        parts.append(_line(rule_y))

    parts.extend(
        _text(9, caption_start_y + index * caption_line_height, line, "caption")
        for index, line in enumerate(caption_lines)
    )
    parts.extend((_line(height - 1), "</svg>"))
    return "\n".join(parts) + "\n"


def write_svg(path: Path, svg: str, *, overwrite: bool = False) -> Path:
    """Atomically publish an SVG, refusing replacement unless explicitly allowed."""

    requested = Path(path).expanduser()
    if requested.is_symlink():
        raise ValueError("output SVG must not be a symbolic link")
    destination = requested.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not overwrite:
        raise FileExistsError(f"refusing to overwrite existing SVG: {destination}")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(svg)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    except Exception:
        try:
            os.close(descriptor)
        except OSError:
            pass
        temporary.unlink(missing_ok=True)
        raise
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render one evaluation JSON as a Nature Table 1-style SVG."
    )
    parser.add_argument("evaluation_json", type=Path, help="input evaluation JSON")
    parser.add_argument("output_svg", type=Path, help="new SVG output path")
    parser.add_argument("--reviewer", required=True, help="measured row label")
    parser.add_argument("--title", default=DEFAULT_TITLE)
    parser.add_argument("--cohort-label")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="explicitly replace an existing output SVG",
    )
    args = parser.parse_args()

    try:
        evaluation = json.loads(args.evaluation_json.read_text(encoding="utf-8"))
        svg = render(
            evaluation,
            reviewer=args.reviewer,
            title=args.title,
            cohort_label=args.cohort_label,
        )
        write_svg(args.output_svg, svg, overwrite=args.overwrite)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        parser.exit(1, f"table render failed: {error}\n")


if __name__ == "__main__":
    main()
