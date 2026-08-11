#!/usr/bin/env python3
"""Render a JSON table specification as a Nature-style comparison SVG.

The renderer is deliberately presentation-only. Metric values are validated as
non-empty display strings and are emitted unchanged, so statistical choices stay
in the source data preparation step rather than being hidden in the figure code.
"""

from __future__ import annotations

import argparse
import json
import os
import tempfile
import textwrap
from pathlib import Path
from typing import Any, Mapping, Sequence, Tuple
from xml.sax.saxutils import escape


WIDTH = 1310
COLUMN_X = (9, 275, 485, 659, 840, 1006, 1159)
METRICS = (
    "balanced_accuracy",
    "accuracy",
    "f1",
    "auc",
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
MAX_GROUPS = 2
MAX_ROWS = 6
CAPTION_WRAP_WIDTH = 142


def _display_string(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _sequence(value: Any, *, field: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise ValueError(f"{field} must be an array")
    return value


def _validated_spec(
    spec: Mapping[str, Any],
) -> Tuple[str, Tuple[Tuple[str, Tuple[Tuple[str, ...], ...]], ...], str]:
    if not isinstance(spec, Mapping):
        raise ValueError("spec must be a JSON object")

    title = _display_string(spec.get("title"), field="title")
    groups_value = _sequence(spec.get("groups"), field="groups")
    if not 1 <= len(groups_value) <= MAX_GROUPS:
        raise ValueError(f"groups must contain between 1 and {MAX_GROUPS} entries")

    groups = []
    total_rows = 0
    for group_index, group_value in enumerate(groups_value):
        if not isinstance(group_value, Mapping):
            raise ValueError(f"groups[{group_index}] must be an object")
        group_label = _display_string(
            group_value.get("label"), field=f"groups[{group_index}].label"
        )
        rows_value = _sequence(
            group_value.get("rows"), field=f"groups[{group_index}].rows"
        )
        if not rows_value:
            raise ValueError(f"groups[{group_index}].rows must not be empty")

        rows = []
        for row_index, row_value in enumerate(rows_value):
            if not isinstance(row_value, Mapping):
                raise ValueError(
                    f"groups[{group_index}].rows[{row_index}] must be an object"
                )
            row = [
                _display_string(
                    row_value.get("label"),
                    field=f"groups[{group_index}].rows[{row_index}].label",
                )
            ]
            row.extend(
                _display_string(
                    row_value.get(metric),
                    field=(
                        f"groups[{group_index}].rows[{row_index}].{metric}"
                    ),
                )
                for metric in METRICS
            )
            rows.append(tuple(row))

        total_rows += len(rows)
        groups.append((group_label, tuple(rows)))

    if total_rows > MAX_ROWS:
        raise ValueError(f"groups may contain at most {MAX_ROWS} rows in total")

    caption_value = spec.get("caption", "")
    if caption_value is None:
        caption = ""
    elif isinstance(caption_value, str):
        caption = " ".join(caption_value.split())
    else:
        raise ValueError("caption must be a string when provided")

    return title, tuple(groups), caption


def _text(x: int, y: int, value: str, css_class: str) -> str:
    # Inline the font attributes as well as keeping the CSS classes.  PyMuPDF's
    # SVG rasterizer ignores class-based font-family declarations, otherwise the
    # PNG fallback silently becomes serif even though the browser SVG is sans.
    font_size, font_weight = {
        "title": (22, 700),
        "header": (16, 700),
        "group": (16, 400),
        "body": (16, 400),
        "caption": (15, 400),
    }[css_class]
    return (
        f'<text x="{x}" y="{y}" class="{css_class}" '
        f'font-family="Helvetica" font-size="{font_size}" '
        f'font-weight="{font_weight}">{escape(value)}</text>'
    )


def _line(y: int, *, width: float = 1.0) -> str:
    return (
        f'<line x1="0" y1="{y}" x2="{WIDTH}" y2="{y}" '
        f'stroke="#111" stroke-width="{width}"/>'
    )


def _caption_lines(caption: str) -> Tuple[str, ...]:
    if not caption:
        return ()
    return tuple(
        textwrap.wrap(
            caption,
            width=CAPTION_WRAP_WIDTH,
            break_long_words=False,
            break_on_hyphens=False,
        )
    )


def render(spec: Mapping[str, Any]) -> str:
    """Return a standalone comparison-table SVG for a validated JSON spec."""

    title, groups, caption = _validated_spec(spec)
    caption_lines = _caption_lines(caption)

    header_rule_y = 96
    block_height = 37
    current_rule_y = header_rule_y
    table_parts = []

    for group_label, rows in groups:
        group_text_y = current_rule_y + 25
        current_rule_y += block_height
        table_parts.extend(
            (
                _text(9, group_text_y, group_label, "group"),
                _line(current_rule_y),
            )
        )
        for row in rows:
            row_text_y = current_rule_y + 25
            current_rule_y += block_height
            table_parts.extend(
                _text(x, row_text_y, value, "body")
                for x, value in zip(COLUMN_X, row)
            )
            table_parts.append(_line(current_rule_y))

    caption_line_height = 23
    if caption_lines:
        caption_start_y = current_rule_y + 32
        height = caption_start_y + len(caption_lines) * caption_line_height + 18
    else:
        caption_start_y = current_rule_y
        height = current_rule_y + 18

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title>',
        (
            '<desc id="desc">Nature-style comparison table with '
            f'{sum(len(rows) for _, rows in groups)} reviewer rows in '
            f'{len(groups)} groups.</desc>'
        ),
        "<style>",
        (
            "text { fill: #111; font-family: Arial, Helvetica, sans-serif; "
            "font-variant-numeric: tabular-nums; }"
        ),
        ".title { font-size: 22px; font-weight: 700; }",
        ".header { font-size: 16px; font-weight: 700; }",
        ".group { font-size: 16px; font-weight: 400; }",
        ".body { font-size: 16px; font-weight: 400; }",
        ".caption { font-size: 15px; font-weight: 400; }",
        "</style>",
        f'<rect x="0" y="0" width="{WIDTH}" height="{height}" fill="#fff"/>',
        _line(1),
        _text(9, 36, title, "title"),
        _line(61),
    ]
    parts.extend(_text(x, 85, value, "header") for x, value in zip(COLUMN_X, HEADERS))
    parts.append(_line(header_rule_y))
    parts.extend(table_parts)
    parts.extend(
        _text(9, caption_start_y + index * caption_line_height, line, "caption")
        for index, line in enumerate(caption_lines)
    )
    parts.extend((_line(height - 1), "</svg>"))
    return "\n".join(parts) + "\n"


def write_svg(path: Path, svg: str, *, overwrite: bool = False) -> Path:
    """Atomically publish an SVG, refusing replacement unless requested."""

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
        description="Render a JSON spec as a Nature-style comparison table SVG."
    )
    parser.add_argument("spec_json", type=Path, help="input JSON table specification")
    parser.add_argument("output_svg", type=Path, help="new SVG output path")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="explicitly replace an existing output SVG",
    )
    args = parser.parse_args()

    try:
        spec = json.loads(args.spec_json.read_text(encoding="utf-8"))
        svg = render(spec)
        write_svg(args.output_svg, svg, overwrite=args.overwrite)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        parser.exit(1, f"comparison table render failed: {error}\n")


if __name__ == "__main__":
    main()
