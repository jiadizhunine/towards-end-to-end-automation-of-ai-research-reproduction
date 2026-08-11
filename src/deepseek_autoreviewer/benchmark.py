"""Local-only preparation and evaluation for retrospective review benchmarks.

This module deliberately contains no network client and never reads API keys.  It
turns a ProReviewer parquet file into two physically separated trees:

``blind/``
    Manuscript text and a manifest that contain no labels or source identifiers.

``private/``
    The seed, ground-truth decisions, and the mapping back to source records.

The preparation path is fail-closed: all requested redactions are followed by a
second, independent leakage scan before any output directory is committed.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import re
import shutil
import tempfile
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import pyarrow.parquet as pq


ACCEPT_DECISIONS = frozenset(
    {
        "Accept (Poster)",
        "Accept (Oral)",
        "Conditional Accept (Poster)",
        "Conditional Accept (Oral)",
    }
)
REJECT_DECISION = "Reject"
SELECTION_ALGORITHM = (
    "sha256(seed_utf8 + NUL + class_utf8 + NUL + paper_id_utf8), ascending"
)
BLINDING_VERSION = "proreviewer-iclr2026-v1"
REDACTION_POLICY_REVISION = "strict-identity-v2"
EXTENSION_MIXING_ALGORITHM = (
    "sha256(seed_utf8 + NUL + extension-combined + NUL + "
    "paper_id_utf8), ascending"
)


class BenchmarkError(ValueError):
    """Base class for invalid benchmark data or configuration."""


class RedactionError(BenchmarkError):
    """Raised when the post-redaction scanner finds a possible leak."""


@dataclass(frozen=True)
class BlindedPaper:
    """In-memory blinded representation before it is written to disk."""

    text: str
    raw_text_sha256: str
    blind_text_sha256: str
    redaction_counts: Dict[str, int]
    nfkc_changed: bool


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_text(value: str) -> str:
    return _sha256_bytes(value.encode("utf-8"))


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _decision(row: Mapping[str, Any]) -> str:
    value = row.get("decision")
    if isinstance(value, Mapping):
        value = value.get("decision")
    return value if isinstance(value, str) else ""


def _paper_content(row: Mapping[str, Any]) -> str:
    markdown = row.get("markdown")
    if isinstance(markdown, Mapping):
        value = markdown.get("content")
    else:
        value = markdown
    return value if isinstance(value, str) else ""


def _markdown_metadata(row: Mapping[str, Any]) -> Mapping[str, Any]:
    markdown = row.get("markdown")
    if not isinstance(markdown, Mapping):
        return {}
    metadata = markdown.get("metadata")
    return metadata if isinstance(metadata, Mapping) else {}


def read_proreviewer_parquet(path: Path) -> List[Dict[str, Any]]:
    """Read and minimally validate a ProReviewer parquet file locally."""

    source = Path(path).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(f"ProReviewer parquet not found: {source}")
    table = pq.read_table(source)
    required = {"paper_id", "title", "markdown", "decision"}
    missing = sorted(required.difference(table.column_names))
    if missing:
        raise BenchmarkError(f"Missing required parquet columns: {', '.join(missing)}")
    return table.to_pylist()


def _stable_selection_key(seed: str, class_label: str, paper_id: str) -> str:
    return _sha256_text(f"{seed}\0{class_label}\0{paper_id}")


def select_balanced_records(
    rows: Sequence[Mapping[str, Any]],
    *,
    seed: str,
    per_class: int = 20,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Select equal Accept/Reject sets using a seeded SHA-256 stable order.

    Only the four explicitly allowed Accept strings and the exact string
    ``Reject`` are eligible. Blank, withdrawn, desk-rejected, and all other
    decision values are therefore excluded rather than coerced.
    """

    if not isinstance(seed, str) or not seed:
        raise BenchmarkError("seed must be a non-empty string")
    if isinstance(per_class, bool) or not isinstance(per_class, int) or per_class < 1:
        raise BenchmarkError("per_class must be a positive integer")

    accepts: List[Dict[str, Any]] = []
    rejects: List[Dict[str, Any]] = []
    excluded = Counter()
    seen_ids = set()

    for source_row in rows:
        row = dict(source_row)
        decision = _decision(row)
        if decision not in ACCEPT_DECISIONS and decision != REJECT_DECISION:
            normalized = decision.strip().casefold()
            if not normalized:
                excluded["empty_decision"] += 1
            elif "withdraw" in normalized:
                excluded["withdrawn"] += 1
            elif "desk" in normalized and "reject" in normalized:
                excluded["desk_reject"] += 1
            else:
                excluded["other_decision"] += 1
            continue

        paper_id = row.get("paper_id")
        if not isinstance(paper_id, str) or not paper_id.strip():
            raise BenchmarkError("Every eligible record must have a non-empty paper_id")
        paper_id = unicodedata.normalize("NFKC", paper_id.strip())
        if paper_id in seen_ids:
            raise BenchmarkError(f"Duplicate eligible paper_id: {paper_id}")
        seen_ids.add(paper_id)
        row["paper_id"] = paper_id
        class_label = "Accept" if decision in ACCEPT_DECISIONS else "Reject"
        row["_selection_sha256"] = _stable_selection_key(seed, class_label, paper_id)
        (accepts if class_label == "Accept" else rejects).append(row)

    if len(accepts) < per_class or len(rejects) < per_class:
        raise BenchmarkError(
            "Not enough eligible records: "
            f"need {per_class} per class, found {len(accepts)} Accept and {len(rejects)} Reject"
        )

    order = lambda row: (row["_selection_sha256"], row["paper_id"])
    chosen_accepts = sorted(accepts, key=order)[:per_class]
    chosen_rejects = sorted(rejects, key=order)[:per_class]
    chosen = chosen_accepts + chosen_rejects

    # Mix classes before assigning opaque sequential IDs.  The second domain
    # separator prevents the file order from revealing the ground-truth class.
    chosen.sort(
        key=lambda row: (
            _sha256_text(f"{seed}\0combined\0{row['paper_id']}"),
            row["paper_id"],
        )
    )
    audit = {
        "seed": seed,
        "seed_sha256": _sha256_text(seed),
        "selection_algorithm": SELECTION_ALGORITHM,
        "eligible_counts": {"Accept": len(accepts), "Reject": len(rejects)},
        "selected_counts": {"Accept": per_class, "Reject": per_class},
        "excluded_counts": dict(sorted(excluded.items())),
    }
    return chosen, audit


def _literal_pattern(value: str) -> Optional[re.Pattern[str]]:
    """Create a case-insensitive, whitespace-tolerant exact-value pattern."""

    value = unicodedata.normalize("NFKC", value).strip()
    if not value:
        return None
    parts = re.split(r"\s+", value)
    expression = r"\s+".join(re.escape(part) for part in parts)
    return re.compile(expression, re.IGNORECASE)


def _canonical_identifier(value: str) -> str:
    """Fold Unicode and punctuation for an independent residual-name scan."""

    decomposed = unicodedata.normalize("NFKD", value).casefold()
    without_marks = "".join(
        character for character in decomposed if not unicodedata.combining(character)
    )
    return " ".join(re.findall(r"[^\W_]+", without_marks, re.UNICODE))


def _canonical_phrase_count(text: str, phrase: str) -> int:
    """Count a canonical phrase only at complete token boundaries.

    Both inputs come from :func:`_canonical_identifier`, so a word boundary on
    each side is sufficient to prevent partial-token false positives such as
    ``graph`` in ``graphs`` or the author ``Yue Yu`` spanning ``Yue,
    Yuansheng`` in a reference list.
    """

    if not phrase:
        return 0
    pattern = re.compile(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)")
    return len(pattern.findall(text))


def _flexible_identifier_pattern(value: str) -> Optional[re.Pattern[str]]:
    """Match the same identifier despite Markdown, punctuation, or line breaks."""

    tokens = re.findall(
        r"[^\W_]+", unicodedata.normalize("NFKD", value), re.UNICODE
    )
    tokens = [
        "".join(character for character in token if not unicodedata.combining(character))
        for token in tokens
    ]
    tokens = [token for token in tokens if token]
    if not tokens:
        return None
    expression = r"(?<!\w)" + r"(?:[\W_])+".join(
        re.escape(token) for token in tokens
    ) + r"(?!\w)"
    return re.compile(expression, re.IGNORECASE)


_IDENTIFIER_TOKEN = re.compile(r"[^\W_]+", re.UNICODE)


def _canonical_token(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value).casefold()
    return "".join(
        character for character in decomposed if not unicodedata.combining(character)
    )


def _redact_canonical_occurrences(text: str, value: str) -> Tuple[str, int]:
    """Redact token-equivalent spans while preserving an auditable count.

    This catches accents, Markdown emphasis, punctuation, and line-break variants
    that a literal regular expression cannot safely enumerate.
    """

    value_tokens = [
        _canonical_token(match.group()) for match in _IDENTIFIER_TOKEN.finditer(value)
    ]
    value_tokens = [token for token in value_tokens if token]
    if not value_tokens:
        return text, 0

    matches = list(_IDENTIFIER_TOKEN.finditer(text))
    text_tokens = [_canonical_token(match.group()) for match in matches]
    spans: List[Tuple[int, int]] = []
    width = len(value_tokens)
    index = 0
    while index <= len(text_tokens) - width:
        if text_tokens[index : index + width] == value_tokens:
            spans.append((matches[index].start(), matches[index + width - 1].end()))
            index += width
        else:
            index += 1
    for start, end in reversed(spans):
        text = text[:start] + "[REDACTED]" + text[end:]
    return text, len(spans)


def _title_ngram_values(value: str) -> List[str]:
    """Return highly identifying title fragments (at least 4 tokens / 60%)."""

    tokens = [
        _canonical_token(match.group()) for match in _IDENTIFIER_TOKEN.finditer(value)
    ]
    tokens = [token for token in tokens if token]
    minimum = max(4, math.ceil(len(tokens) * 0.60))
    if len(tokens) < minimum:
        return []
    fragments: List[str] = []
    for width in range(len(tokens) - 1, minimum - 1, -1):
        fragments.extend(
            " ".join(tokens[start : start + width])
            for start in range(0, len(tokens) - width + 1)
        )
    return fragments


_SENSITIVE_SECTION = re.compile(
    r"^(?:(?:appendix\s+)?(?:\d+(?:\.\d+)*|[A-Z])[\s.:)\-]+)?"
    r"(?:acknowledg(?:e)?ments?(?:\s+.*)?|"
    r"author(?:s['’])?\s+contributions?(?:\s+list)?|"
    r"contributions?\s+of\s+(?:the\s+)?authors?|"
    r"credits?\s+(?:and|&)\s+contributions?)\s*[:.]?\s*$",
    re.IGNORECASE,
)
_ATX_HEADING = re.compile(r"^(\s*)(#{1,6})\s+(.+?)\s*#*\s*$")
_LATEX_SECTION = re.compile(
    r"^\s*\\(?:sub)*section\*?\s*\{\s*"
    r"(?:(?:appendix\s+)?(?:\d+(?:\.\d+)*|[A-Z])[\s.:)\-]+)?"
    r"(acknowledg(?:e)?ments?(?:\s+.*)?|"
    r"author(?:s['’])?\s+contributions?(?:\s+list)?|"
    r"contributions?\s+of\s+(?:the\s+)?authors?|"
    r"credits?\s+(?:and|&)\s+contributions?)\s*\}\s*$",
    re.IGNORECASE,
)
_AUTHOR_ROSTER_HEADING = re.compile(
    r"^(?:(?:appendix\s+)?(?:\d+(?:\.\d+)*|[A-Z])[\s.:)\-]+)?"
    r"contributions?\s*$",
    re.IGNORECASE,
)
_AUTHOR_ROSTER_CUE = re.compile(
    r"(?im)^\s*(?:core\s+contributors?|corresponding\s+authors?|"
    r"project\s+responsibilities|authors?(?:\s+\^?\d.*)?|"
    r"affiliations?(?:\s+\^?\d.*)?|equal\s+contributions?.*)\s*:?[ \t]*$"
)
_SENSITIVE_SECTION_CONTINUATION = re.compile(
    r"(?i)\b(?:funded|funding|supported|support|award|grant|"
    r"project\s*(?:number|no\.?|#)?)\b"
)


def _strip_sensitive_sections(text: str) -> Tuple[str, int, int]:
    """Remove acknowledgement/author-contribution sections by heading scope."""

    lines = text.splitlines(keepends=True)
    kept: List[str] = []
    removed_sections = 0
    removed_lines = 0
    index = 0
    while index < len(lines):
        plain = lines[index].rstrip("\r\n")
        heading = _ATX_HEADING.match(plain)
        latex = _LATEX_SECTION.match(plain)
        if heading and _SENSITIVE_SECTION.fullmatch(heading.group(3).strip()):
            level = len(heading.group(2))
        elif (
            heading
            and _AUTHOR_ROSTER_HEADING.fullmatch(heading.group(3).strip())
            and _AUTHOR_ROSTER_CUE.search("".join(lines[index + 1 : index + 16]))
        ):
            # A generic "Contributions" heading can describe scientific
            # contributions. Treat it as identity-bearing only when the
            # immediate content explicitly introduces an author roster.
            level = len(heading.group(2))
        elif latex:
            level = 1
        else:
            # Some converters emit a bare terminal heading. Require a complete
            # heading-name match to avoid deleting technical contribution text.
            candidate = plain.strip()
            if not _SENSITIVE_SECTION.fullmatch(candidate):
                kept.append(lines[index])
                index += 1
                continue
            level = 1

        removed_sections += 1
        removed_lines += 1
        index += 1
        while index < len(lines):
            next_plain = lines[index].rstrip("\r\n")
            next_heading = _ATX_HEADING.match(next_plain)
            if (
                next_heading
                and len(next_heading.group(2)) <= level
                and not _SENSITIVE_SECTION_CONTINUATION.search(
                    next_heading.group(3)
                )
            ):
                break
            if level == 1 and re.match(r"^\s*\\section\*?\s*\{", next_plain):
                break
            removed_lines += 1
            index += 1
    return "".join(kept), removed_sections, removed_lines


# These patterns intentionally operate after NFKC normalization. Replacements
# all use one neutral marker so the post-scan cannot mistake a marker for a leak.
_GENERIC_REDACTIONS: Tuple[Tuple[str, re.Pattern[str]], ...] = (
    (
        "identity_metadata_line",
        re.compile(
            r"(?im)^\s*(?:authors?|affiliations?|institutions?|"
            r"corresponding\s+authors?|contacts?|e-?mails?)"
            r"(?:\s*:.*|\s{2,}.*|\s*)$"
        ),
    ),
    (
        "identity_footnote_line",
        re.compile(
            r"(?im)^.*(?:corresponding\s+author\s*:|"
            r"work\s+(?:was\s+)?done\s+during\s+an?\s+internship\b).*$"
        ),
    ),
    (
        "identity_acknowledgement_line",
        re.compile(r"(?im)^\s*acknowledg(?:e)?ments?\s*[:.].*$"),
    ),
    (
        "sensitive_toc_entry",
        re.compile(
            r"(?im)^\s*[-*+]\s+(?:acknowledg(?:e)?ments?|"
            r"author(?:s['’])?\s+contributions?|"
            r"credits?\s+(?:and|&)\s+contributions?)\s*$"
        ),
    ),
    (
        "decision_lifecycle_line",
        re.compile(
            r"(?i)[^.!?\n]*(?:\bcamera[-\s]?ready(?:\s+version)?\b|"
            r"\b(?:upon|after)\s+(?:(?:the\s+)?(?:paper|work|submission)\s+)?"
            r"acceptance\b|\bonce\s+(?:(?:the\s+)?(?:paper|work|submission)\s+)?"
            r"(?:is\s+)?accepted\b|"
            r"\bif\s+(?:(?:the\s+)?(?:paper|work|submission)\s+is\s+)?"
            r"accepted\b)[^.!?\n]*(?:[.!?]|$)"
        ),
    ),
    (
        "asset_path",
        re.compile(r"(?im)^\s*Refer\s+to\s+caption\s*:\s*.*$"),
    ),
    (
        "reference_link_line",
        re.compile(r"(?im)^\s*(?:doi|url)\s*:?.*$"),
    ),
    (
        "conference_template",
        re.compile(
            r"(?im)^\s*(?:published|submitted|under\s+review|accepted)\s+as\s+(?:a\s+)?"
            r"(?:conference\s+)?paper\s+(?:at|to|for)\b[^\n]*$"
        ),
    ),
    (
        "conference_name",
        re.compile(
            r"(?i)(?:ICLR(?:\s*20\d{2})?|International\s+Conference\s+on\s+Learning\s+Representations)"
        ),
    ),
    (
        "latex_link",
        re.compile(r"(?is)\\(?:url|href)\s*\{[^{}]*\}(?:\s*\{[^{}]*\})?"),
    ),
    (
        "url",
        re.compile(
            r"(?i)(?:https?\s*:\s*/\s*/|ftp\s*:\s*/\s*/|www\.)"
            r"(?:[^\s<>\[\]{}]+)?"
        ),
    ),
    (
        "email",
        re.compile(
            r"(?i)(?:\{[A-Z0-9._%+\-,\s]+\}|\[REDACTED\]|"
            r"[A-Z0-9._%+-]+)@[A-Z0-9.-]+\.[A-Z]{2,}\b"
        ),
    ),
    (
        "domain",
        re.compile(
            r"(?i)(?<![@\w-])(?:[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?\.)+"
            r"(?:ai|app|cn|co|com|de|dev|edu|eu|fr|gov|info|io|jp|net|org|uk)"
            r"(?:/[^\s<>\[\]{}]*)?"
        ),
    ),
    (
        "doi",
        re.compile(r"(?i)\b(?:doi\s*:\s*)?10\.\d{4,9}/[-._;()/:A-Z0-9]+"),
    ),
    (
        "arxiv_id",
        re.compile(r"(?i)\b(?:arxiv\s*:\s*)?\d{4}\.\d{4,5}(?:v\d+)?\b"),
    ),
    ("orcid", re.compile(r"(?i)\b(?:ORCID\s*:?\s*)?\d{4}-\d{4}-\d{4}-\d{3}[\dX]\b")),
    ("openreview", re.compile(r"(?i)\bopen\s*review(?:\.net)?\b")),
    ("github", re.compile(r"(?i)\bgithub(?:\.com)?\b")),
)


def _sensitive_values(row: Mapping[str, Any]) -> Dict[str, List[str]]:
    metadata = _markdown_metadata(row)
    values: Dict[str, List[str]] = {
        "title": [],
        "author": [],
        "paper_id": [],
        "arxiv_id": [],
    }
    for candidate in (row.get("title"), metadata.get("title")):
        if isinstance(candidate, str) and candidate.strip():
            values["title"].append(candidate)
    authors = metadata.get("authors")
    if isinstance(authors, Sequence) and not isinstance(authors, (str, bytes)):
        for author in authors:
            if not isinstance(author, str) or not author.strip():
                continue
            values["author"].append(author)
            # Contribution and acknowledgement prose often omits a middle
            # name or initial, reverses East-Asian name order, or inserts a
            # missing space in CamelCase metadata. Protect those multi-token
            # aliases, but never redact a given name alone.
            name_tokens: List[str] = []
            for match in _IDENTIFIER_TOKEN.finditer(author):
                token = match.group()
                camel_parts = re.findall(
                    r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", token
                )
                name_tokens.extend(camel_parts if len(camel_parts) > 1 else [token])
            if len(name_tokens) >= 2:
                values["author"].append(" ".join(name_tokens))
                values["author"].append("".join(name_tokens))
            if len(name_tokens) == 2:
                values["author"].append(" ".join(reversed(name_tokens)))
            if len(name_tokens) >= 3:
                values["author"].append(f"{name_tokens[0]} {name_tokens[-1]}")
                values["author"].append(f"{name_tokens[-1]} {name_tokens[0]}")
                values["author"].append(f"{name_tokens[0]}{name_tokens[-1]}")
                values["author"].append(f"{name_tokens[-1]}{name_tokens[0]}")
    for field in ("paper_id", "arxiv_id"):
        candidate = row.get(field)
        if isinstance(candidate, str) and candidate.strip():
            values[field].append(candidate)

    # De-duplicate after the same normalization used on the manuscript.
    for category, candidates in values.items():
        normalized = [unicodedata.normalize("NFKC", item).strip() for item in candidates]
        values[category] = list(dict.fromkeys(item for item in normalized if item))
    return values


def scan_for_leaks(
    text: str,
    *,
    sensitive_values: Optional[Mapping[str, Sequence[str]]] = None,
) -> Dict[str, int]:
    """Return possible leak counts; an empty mapping means the scan passed."""

    normalized = unicodedata.normalize("NFKC", text)
    canonical_text = _canonical_identifier(normalized)
    findings: Counter[str] = Counter()
    for category, pattern in _GENERIC_REDACTIONS:
        count = len(pattern.findall(normalized))
        if count:
            findings[category] += count
    if sensitive_values:
        for category, values in sensitive_values.items():
            for value in values:
                pattern = _literal_pattern(value)
                if pattern is not None:
                    count = len(pattern.findall(normalized))
                    if count:
                        findings[category] += count
                canonical_value = _canonical_identifier(value)
                canonical_count = _canonical_phrase_count(
                    canonical_text, canonical_value
                )
                if canonical_count:
                    findings[f"{category}_canonical"] += canonical_count
                if category == "title":
                    for fragment in _title_ngram_values(value):
                        fragment_count = _canonical_phrase_count(
                            canonical_text, fragment
                        )
                        if fragment_count:
                            findings["title_high_coverage_ngram"] += fragment_count
    return dict(sorted(findings.items()))


def blind_record(row: Mapping[str, Any]) -> BlindedPaper:
    """NFKC-normalize, redact, and independently verify one manuscript."""

    raw_text = _paper_content(row)
    if not raw_text.strip():
        raise BenchmarkError("Eligible record has empty markdown content")
    normalized = unicodedata.normalize("NFKC", raw_text)
    text, section_count, section_lines = _strip_sensitive_sections(normalized)
    counts: Counter[str] = Counter()
    if section_count:
        counts["sensitive_section"] += section_count
        counts["sensitive_section_lines"] += section_lines

    sensitive = _sensitive_values(row)
    for category, values in sensitive.items():
        for value in sorted(values, key=len, reverse=True):
            pattern = _literal_pattern(value)
            if pattern is not None:
                text, count = pattern.subn("[REDACTED]", text)
                counts[category] += count
            flexible_pattern = _flexible_identifier_pattern(value)
            if flexible_pattern is not None:
                text, count = flexible_pattern.subn("[REDACTED]", text)
                counts[f"{category}_flexible"] += count
            text, count = _redact_canonical_occurrences(text, value)
            counts[f"{category}_canonical"] += count
            if category == "title":
                for fragment in _title_ngram_values(value):
                    text, count = _redact_canonical_occurrences(text, fragment)
                    counts["title_high_coverage_ngram"] += count

    for category, pattern in _GENERIC_REDACTIONS:
        text, count = pattern.subn("[REDACTED]", text)
        counts[category] += count

    # Normalize excessive whitespace created by whole-section/line removal but
    # otherwise preserve the source markdown exactly for scientific review.
    text = re.sub(r"\n{4,}", "\n\n\n", text).strip() + "\n"
    if not text.strip():
        raise RedactionError("Redaction removed the entire manuscript")

    leaks = scan_for_leaks(text, sensitive_values=sensitive)
    if leaks:
        categories = ", ".join(f"{key}={value}" for key, value in leaks.items())
        raise RedactionError(f"Post-redaction leakage scan failed ({categories})")

    return BlindedPaper(
        text=text,
        raw_text_sha256=_sha256_text(raw_text),
        blind_text_sha256=_sha256_text(text),
        redaction_counts=dict(sorted((key, value) for key, value in counts.items() if value)),
        nfkc_changed=normalized != raw_text,
    )


def _write_private_file(path: Path, payload: bytes) -> None:
    """Create a mode-0600 file without following/overwriting an existing path."""

    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        raise
    path.chmod(0o600)


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def prepare_benchmark(
    parquet_path: Path,
    output_root: Path,
    *,
    seed: str,
    per_class: int = 20,
) -> Dict[str, Any]:
    """Prepare a blinded, balanced benchmark and return a non-sensitive summary.

    The final directory is published only after every selected paper passes the
    leakage scan. The caller must choose a new/non-existent output directory.
    """

    source = Path(parquet_path).expanduser().resolve()
    destination = Path(output_root).expanduser().resolve()
    if destination.exists():
        raise FileExistsError(f"Refusing to overwrite benchmark output: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)

    rows = read_proreviewer_parquet(source)
    selected, selection_audit = select_balanced_records(rows, seed=seed, per_class=per_class)

    # Redact everything in memory before creating the externally visible tree.
    prepared: List[Tuple[Dict[str, Any], BlindedPaper]] = []
    for row in selected:
        prepared.append((row, blind_record(row)))

    staging = Path(tempfile.mkdtemp(prefix=f".{destination.name}.staging-", dir=destination.parent))
    try:
        staging.chmod(0o700)
        blind_dir = staging / "blind"
        private_dir = staging / "private"
        blind_dir.mkdir(mode=0o700)
        private_dir.mkdir(mode=0o700)
        blind_dir.chmod(0o700)
        private_dir.chmod(0o700)

        blind_entries: List[Dict[str, Any]] = []
        private_entries: List[Dict[str, Any]] = []
        for index, (row, blinded) in enumerate(prepared, start=1):
            blind_id = f"B{index:03d}"
            filename = f"{blind_id}.txt"
            _write_private_file(blind_dir / filename, blinded.text.encode("utf-8"))
            blind_entries.append(
                {
                    "blind_id": blind_id,
                    "filename": filename,
                    "raw_text_sha256": blinded.raw_text_sha256,
                    "blind_text_sha256": blinded.blind_text_sha256,
                    "redaction_counts": blinded.redaction_counts,
                    "nfkc_changed": blinded.nfkc_changed,
                    "leak_scan": {"passed": True, "findings": {}},
                }
            )
            decision = _decision(row)
            metadata = _markdown_metadata(row)
            private_entries.append(
                {
                    "blind_id": blind_id,
                    "paper_id": row.get("paper_id", ""),
                    "arxiv_id": row.get("arxiv_id", ""),
                    "title": row.get("title", ""),
                    "authors": metadata.get("authors", []),
                    "source_decision": decision,
                    "ground_truth": "Accept" if decision in ACCEPT_DECISIONS else "Reject",
                    "selection_sha256": row["_selection_sha256"],
                    "raw_text_sha256": blinded.raw_text_sha256,
                    "blind_text_sha256": blinded.blind_text_sha256,
                }
            )

        blind_manifest = {
            "format_version": BLINDING_VERSION,
            "redaction_policy_revision": REDACTION_POLICY_REVISION,
            "paper_count": len(blind_entries),
            "contains_ground_truth": False,
            "contains_source_identifiers": False,
            "reviewer_network_policy": (
                "browser/search/retrieval/tools disabled; only the DeepSeek API transport "
                "is permitted during review"
            ),
            "papers": blind_entries,
        }
        private_mapping = {
            "format_version": BLINDING_VERSION,
            "redaction_policy_revision": REDACTION_POLICY_REVISION,
            "source_parquet": str(source),
            "source_parquet_sha256": _sha256_file(source),
            "source_row_count": len(rows),
            "selection": selection_audit,
            "papers": private_entries,
        }
        _write_private_file(blind_dir / "manifest.json", _json_bytes(blind_manifest))
        _write_private_file(private_dir / "mapping.json", _json_bytes(private_mapping))

        # Rename is atomic on the same filesystem. Re-assert modes after rename
        # because the parent umask is not trusted.
        staging.rename(destination)
        destination.chmod(0o700)
        (destination / "blind").chmod(0o700)
        (destination / "private").chmod(0o700)
        for file_path in destination.rglob("*"):
            if file_path.is_file():
                file_path.chmod(0o600)
            elif file_path.is_dir():
                file_path.chmod(0o700)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise

    return {
        "output_root": str(destination),
        "paper_count": len(prepared),
        "selected_counts": selection_audit["selected_counts"],
        "seed_sha256": selection_audit["seed_sha256"],
        "source_parquet_sha256": _sha256_file(source),
        "leak_scan_passed": True,
    }


def _read_json_object(path: Path, *, description: str) -> Dict[str, Any]:
    source = Path(path).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(f"{description} not found: {source}")
    try:
        value = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise BenchmarkError(f"Invalid {description}: {source}") from error
    if not isinstance(value, dict):
        raise BenchmarkError(f"{description} must contain a JSON object")
    return value


def _eligible_record_pools(
    rows: Sequence[Mapping[str, Any]],
) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, Dict[str, Any]], Counter[str]]:
    """Index the two exact decision classes without silently merging records."""

    pools: Dict[str, List[Dict[str, Any]]] = {"Accept": [], "Reject": []}
    by_id: Dict[str, Dict[str, Any]] = {}
    excluded: Counter[str] = Counter()
    for source_row in rows:
        row = dict(source_row)
        decision = _decision(row)
        if decision not in ACCEPT_DECISIONS and decision != REJECT_DECISION:
            normalized = decision.strip().casefold()
            if not normalized:
                excluded["empty_decision"] += 1
            elif "withdraw" in normalized:
                excluded["withdrawn"] += 1
            elif "desk" in normalized and "reject" in normalized:
                excluded["desk_reject"] += 1
            else:
                excluded["other_decision"] += 1
            continue

        paper_id = row.get("paper_id")
        if not isinstance(paper_id, str) or not paper_id.strip():
            raise BenchmarkError("Every eligible record must have a non-empty paper_id")
        paper_id = unicodedata.normalize("NFKC", paper_id.strip())
        if paper_id in by_id:
            raise BenchmarkError(f"Duplicate eligible paper_id: {paper_id}")
        row["paper_id"] = paper_id
        class_label = "Accept" if decision in ACCEPT_DECISIONS else "Reject"
        row["_class_label"] = class_label
        pools[class_label].append(row)
        by_id[paper_id] = row
    return pools, by_id, excluded


def _require_sha256(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise BenchmarkError(f"{field} must be a lowercase SHA-256 digest")
    return value


def _validate_positive_target(value: Any, *, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise BenchmarkError(f"{field} must be a positive integer")
    return value


def extend_benchmark(
    parquet_path: Path,
    prior_private_mapping_path: Path,
    prior_blind_manifest_path: Path,
    prior_blind_dir: Path,
    output_root: Path,
    *,
    seed: str,
    target_accept: int,
    target_reject: int,
) -> Dict[str, Any]:
    """Extend the frozen 40-paper benchmark while preserving ``B001``-``B040``.

    The prior source rows, labels, raw/blind hashes, and blind files are all
    verified before new records are selected. Retained records are then
    re-blinded under the current policy, with any changed hashes recorded
    explicitly instead of silently reusing stale text. New records
    continue each class's original ``seed``-based SHA-256 ranking, then are mixed
    before receiving IDs from ``B041``. The function verifies that the retained
    records are exactly the top 20 of each original class ranking.
    Labels and source identifiers remain confined to ``private/mapping.json``.

    The output directory is atomically published only after every invariant and
    leakage check passes. It must not already exist.
    """

    if not isinstance(seed, str) or not seed:
        raise BenchmarkError("seed must be a non-empty string")
    target_accept = _validate_positive_target(target_accept, field="target_accept")
    target_reject = _validate_positive_target(target_reject, field="target_reject")
    if target_accept + target_reject > 999:
        raise BenchmarkError("At most 999 papers are supported by the B001 ID format")

    source = Path(parquet_path).expanduser().resolve()
    prior_mapping_path = Path(prior_private_mapping_path).expanduser().resolve()
    prior_manifest_path = Path(prior_blind_manifest_path).expanduser().resolve()
    prior_blind = Path(prior_blind_dir).expanduser().resolve()
    destination = Path(output_root).expanduser().resolve()
    if destination.exists():
        raise FileExistsError(f"Refusing to overwrite benchmark output: {destination}")
    if not prior_blind.is_dir():
        raise FileNotFoundError(f"Prior blind directory not found: {prior_blind}")
    if prior_manifest_path.parent != prior_blind:
        raise BenchmarkError("Prior blind manifest must be inside prior_blind_dir")

    rows = read_proreviewer_parquet(source)
    pools, source_by_id, excluded = _eligible_record_pools(rows)
    source_sha256 = _sha256_file(source)
    prior_mapping = _read_json_object(
        prior_mapping_path, description="prior private mapping"
    )
    prior_manifest = _read_json_object(
        prior_manifest_path, description="prior blind manifest"
    )

    if prior_mapping.get("format_version") != BLINDING_VERSION:
        raise BenchmarkError("Prior private mapping has an unsupported format_version")
    if prior_manifest.get("format_version") != BLINDING_VERSION:
        raise BenchmarkError("Prior blind manifest has an unsupported format_version")
    if prior_mapping.get("source_parquet_sha256") != source_sha256:
        raise BenchmarkError("Prior private mapping does not match the source parquet hash")
    if prior_mapping.get("source_row_count") != len(rows):
        raise BenchmarkError("Prior private mapping does not match the source row count")
    if prior_manifest.get("contains_ground_truth") is not False:
        raise BenchmarkError("Prior blind manifest must explicitly exclude ground truth")
    if prior_manifest.get("contains_source_identifiers") is not False:
        raise BenchmarkError("Prior blind manifest must explicitly exclude source identifiers")

    private_entries_value = prior_mapping.get("papers")
    blind_entries_value = prior_manifest.get("papers")
    if not isinstance(private_entries_value, list) or not isinstance(
        blind_entries_value, list
    ):
        raise BenchmarkError("Prior mapping and manifest must each contain a papers list")
    if prior_mapping.get("selection") is None or not isinstance(
        prior_mapping["selection"], Mapping
    ):
        raise BenchmarkError("Prior private mapping has no valid selection audit")
    if prior_manifest.get("paper_count") != 40:
        raise BenchmarkError("Prior blind manifest must contain exactly B001-B040")
    if len(private_entries_value) != 40 or len(blind_entries_value) != 40:
        raise BenchmarkError("Prior mapping and manifest must each contain 40 papers")

    expected_ids = [f"B{index:03d}" for index in range(1, 41)]
    private_entries: List[Dict[str, Any]] = []
    blind_entries: List[Dict[str, Any]] = []
    for value in private_entries_value:
        if not isinstance(value, Mapping):
            raise BenchmarkError("Every prior private paper entry must be an object")
        private_entries.append(dict(value))
    for value in blind_entries_value:
        if not isinstance(value, Mapping):
            raise BenchmarkError("Every prior blind paper entry must be an object")
        blind_entries.append(dict(value))
    if [entry.get("blind_id") for entry in private_entries] != expected_ids:
        raise BenchmarkError("Prior private mapping IDs must be contiguous B001-B040")
    if [entry.get("blind_id") for entry in blind_entries] != expected_ids:
        raise BenchmarkError("Prior blind manifest IDs must be contiguous B001-B040")

    prior_seed = prior_mapping["selection"].get("seed")
    if not isinstance(prior_seed, str) or not prior_seed:
        raise BenchmarkError("Prior selection seed must be a non-empty string")
    if seed != prior_seed:
        raise BenchmarkError("seed must exactly match the frozen prior selection seed")
    prior_counts: Counter[str] = Counter()
    selected_paper_ids = set()
    retained_blind_files: List[Tuple[str, bytes]] = []
    regenerated_private_entries: List[Dict[str, Any]] = []
    regenerated_blind_entries: List[Dict[str, Any]] = []
    retained_blind_hash_changes: List[Dict[str, str]] = []
    for blind_id, private_entry, blind_entry in zip(
        expected_ids, private_entries, blind_entries
    ):
        if private_entry.get("blind_id") != blind_id or blind_entry.get("blind_id") != blind_id:
            raise BenchmarkError(f"Prior entry order mismatch at {blind_id}")
        filename = blind_entry.get("filename")
        if filename != f"{blind_id}.txt":
            raise BenchmarkError(f"Unsafe or unexpected prior filename for {blind_id}")
        for forbidden_field in (
            "ground_truth",
            "paper_id",
            "arxiv_id",
            "title",
            "authors",
            "source_decision",
            "selection_sha256",
        ):
            if forbidden_field in blind_entry:
                raise BenchmarkError(
                    f"Prior blind manifest leaks {forbidden_field} for {blind_id}"
                )
        leak_scan = blind_entry.get("leak_scan")
        if not isinstance(leak_scan, Mapping) or leak_scan.get("passed") is not True:
            raise BenchmarkError(f"Prior blind leak scan did not pass for {blind_id}")
        if leak_scan.get("findings") not in ({}, None):
            raise BenchmarkError(f"Prior blind leak scan has findings for {blind_id}")

        paper_id = private_entry.get("paper_id")
        if not isinstance(paper_id, str) or paper_id not in source_by_id:
            raise BenchmarkError(f"Prior paper {blind_id} is absent from the source parquet")
        if paper_id in selected_paper_ids:
            raise BenchmarkError(f"Duplicate prior paper_id: {paper_id}")
        selected_paper_ids.add(paper_id)
        source_row = source_by_id[paper_id]
        source_decision = _decision(source_row)
        source_label = source_row["_class_label"]
        if private_entry.get("source_decision") != source_decision:
            raise BenchmarkError(f"Source decision mismatch for {blind_id}")
        if private_entry.get("ground_truth") != source_label:
            raise BenchmarkError(f"Ground-truth label mismatch for {blind_id}")
        if private_entry.get("title") != source_row.get("title", ""):
            raise BenchmarkError(f"Source title mismatch for {blind_id}")
        if private_entry.get("arxiv_id", "") != source_row.get("arxiv_id", ""):
            raise BenchmarkError(f"Source arXiv ID mismatch for {blind_id}")
        source_authors = _markdown_metadata(source_row).get("authors", [])
        if private_entry.get("authors", []) != source_authors:
            raise BenchmarkError(f"Source authors mismatch for {blind_id}")

        raw_hash = _require_sha256(
            private_entry.get("raw_text_sha256"),
            field=f"{blind_id}.raw_text_sha256",
        )
        blind_hash = _require_sha256(
            private_entry.get("blind_text_sha256"),
            field=f"{blind_id}.blind_text_sha256",
        )
        if blind_entry.get("raw_text_sha256") != raw_hash:
            raise BenchmarkError(f"Raw-text hash mismatch between prior files for {blind_id}")
        if blind_entry.get("blind_text_sha256") != blind_hash:
            raise BenchmarkError(f"Blind-text hash mismatch between prior files for {blind_id}")
        if _sha256_text(_paper_content(source_row)) != raw_hash:
            raise BenchmarkError(f"Source raw-text hash mismatch for {blind_id}")
        regenerated = blind_record(source_row)
        if regenerated.raw_text_sha256 != raw_hash:
            raise BenchmarkError(f"Regenerated raw-text hash mismatch for {blind_id}")

        expected_selection_hash = _stable_selection_key(prior_seed, source_label, paper_id)
        if private_entry.get("selection_sha256") != expected_selection_hash:
            raise BenchmarkError(f"Prior selection hash mismatch for {blind_id}")
        blind_path = prior_blind / filename
        if not blind_path.is_file():
            raise FileNotFoundError(f"Prior blind paper not found: {blind_path}")
        file_bytes = blind_path.read_bytes()
        if _sha256_bytes(file_bytes) != blind_hash:
            raise BenchmarkError(f"Prior blind file hash mismatch for {blind_id}")
        try:
            file_text = file_bytes.decode("utf-8")
        except UnicodeDecodeError as error:
            raise BenchmarkError(f"Prior blind file is not UTF-8 for {blind_id}") from error
        if regenerated.blind_text_sha256 == blind_hash and file_text != regenerated.text:
            raise BenchmarkError(f"Prior blind file content mismatch for {blind_id}")

        current_private_entry = dict(private_entry)
        current_private_entry["raw_text_sha256"] = regenerated.raw_text_sha256
        current_private_entry["blind_text_sha256"] = regenerated.blind_text_sha256
        regenerated_private_entries.append(current_private_entry)
        current_blind_entry = dict(blind_entry)
        current_blind_entry.update(
            {
                "raw_text_sha256": regenerated.raw_text_sha256,
                "blind_text_sha256": regenerated.blind_text_sha256,
                "redaction_counts": regenerated.redaction_counts,
                "nfkc_changed": regenerated.nfkc_changed,
                "leak_scan": {"passed": True, "findings": {}},
            }
        )
        regenerated_blind_entries.append(current_blind_entry)
        retained_blind_files.append((filename, regenerated.text.encode("utf-8")))
        if regenerated.blind_text_sha256 != blind_hash:
            retained_blind_hash_changes.append(
                {
                    "blind_id": blind_id,
                    "prior_blind_text_sha256": blind_hash,
                    "current_blind_text_sha256": regenerated.blind_text_sha256,
                }
            )
        prior_counts[source_label] += 1

    if prior_counts != Counter({"Accept": 20, "Reject": 20}):
        raise BenchmarkError("Prior benchmark must contain 20 Accept and 20 Reject papers")
    expected_prior_rows: List[Dict[str, Any]] = []
    ranked_by_class: Dict[str, List[Dict[str, Any]]] = {}
    for class_label in ("Accept", "Reject"):
        ranked = sorted(
            pools[class_label],
            key=lambda row: (
                _stable_selection_key(seed, class_label, row["paper_id"]),
                row["paper_id"],
            ),
        )
        ranked_by_class[class_label] = ranked
        expected_prior_rows.extend(ranked[:20])
    expected_prior_rows.sort(
        key=lambda row: (
            _sha256_text(f"{seed}\0combined\0{row['paper_id']}"),
            row["paper_id"],
        )
    )
    if [entry["paper_id"] for entry in private_entries] != [
        row["paper_id"] for row in expected_prior_rows
    ]:
        raise BenchmarkError(
            "Prior B001-B040 are not exactly the frozen top-20-per-class sample"
        )

    if target_accept < prior_counts["Accept"] or target_reject < prior_counts["Reject"]:
        raise BenchmarkError(
            "Target class counts cannot be smaller than the retained prior counts "
            f"({prior_counts['Accept']} Accept, {prior_counts['Reject']} Reject)"
        )
    added_counts = {
        "Accept": target_accept - prior_counts["Accept"],
        "Reject": target_reject - prior_counts["Reject"],
    }

    selected_new: List[Dict[str, Any]] = []
    remaining_counts: Dict[str, int] = {}
    for class_label in ("Accept", "Reject"):
        ranked = ranked_by_class[class_label]
        remaining_counts[class_label] = len(ranked) - 20
        needed = added_counts[class_label]
        if len(ranked) < 20 + needed:
            raise BenchmarkError(
                f"Not enough unselected {class_label} records: "
                f"need {needed}, found {len(ranked) - 20}"
            )
        continuation = ranked[20 : 20 + needed]
        for row in continuation:
            row["_selection_sha256"] = _stable_selection_key(
                seed, class_label, row["paper_id"]
            )
        selected_new.extend(continuation)

    selected_new.sort(
        key=lambda row: (
            _sha256_text(
                f"{seed}\0extension-combined\0{row['paper_id']}"
            ),
            row["paper_id"],
        )
    )
    if len({row["paper_id"] for row in selected_new}) != len(selected_new):
        raise BenchmarkError("Duplicate paper_id in extension selection")
    if selected_paper_ids.intersection(row["paper_id"] for row in selected_new):
        raise BenchmarkError("Extension selection overlaps the retained benchmark")

    prepared_new: List[Tuple[Dict[str, Any], BlindedPaper]] = [
        (row, blind_record(row)) for row in selected_new
    ]
    final_blind_entries = regenerated_blind_entries
    final_private_entries = regenerated_private_entries
    new_blind_files: List[Tuple[str, bytes]] = []
    for index, (row, blinded) in enumerate(prepared_new, start=41):
        blind_id = f"B{index:03d}"
        filename = f"{blind_id}.txt"
        new_blind_files.append((filename, blinded.text.encode("utf-8")))
        final_blind_entries.append(
            {
                "blind_id": blind_id,
                "filename": filename,
                "raw_text_sha256": blinded.raw_text_sha256,
                "blind_text_sha256": blinded.blind_text_sha256,
                "redaction_counts": blinded.redaction_counts,
                "nfkc_changed": blinded.nfkc_changed,
                "leak_scan": {"passed": True, "findings": {}},
            }
        )
        decision = _decision(row)
        metadata = _markdown_metadata(row)
        final_private_entries.append(
            {
                "blind_id": blind_id,
                "paper_id": row["paper_id"],
                "arxiv_id": row.get("arxiv_id", ""),
                "title": row.get("title", ""),
                "authors": metadata.get("authors", []),
                "source_decision": decision,
                "ground_truth": row["_class_label"],
                "selection_sha256": row["_selection_sha256"],
                "raw_text_sha256": blinded.raw_text_sha256,
                "blind_text_sha256": blinded.blind_text_sha256,
            }
        )

    target_counts = {"Accept": target_accept, "Reject": target_reject}
    if len(final_private_entries) != target_accept + target_reject:
        raise BenchmarkError("Internal error: final paper count does not match targets")
    if len({entry["paper_id"] for entry in final_private_entries}) != len(
        final_private_entries
    ):
        raise BenchmarkError("Duplicate paper_id in final benchmark")

    final_blind_manifest = dict(prior_manifest)
    final_blind_manifest.update(
        {
            "redaction_policy_revision": REDACTION_POLICY_REVISION,
            "paper_count": len(final_blind_entries),
            "contains_ground_truth": False,
            "contains_source_identifiers": False,
            "papers": final_blind_entries,
        }
    )
    extension_audit = {
        "strategy": "retain-B001-B040-plus-stable-hash-extension",
        "seed": seed,
        "seed_sha256": _sha256_text(seed),
        "selection_algorithm": SELECTION_ALGORITHM,
        "mixing_algorithm": EXTENSION_MIXING_ALGORITHM,
        "eligible_counts": {
            "Accept": len(pools["Accept"]),
            "Reject": len(pools["Reject"]),
        },
        "prior_counts": dict(prior_counts),
        "target_counts": target_counts,
        "selected_counts": target_counts,
        "added_counts": added_counts,
        "remaining_unselected_counts_before_extension": remaining_counts,
        "excluded_counts": dict(sorted(excluded.items())),
        "prior": {
            "paper_count": 40,
            "private_mapping_sha256": _sha256_file(prior_mapping_path),
            "blind_manifest_sha256": _sha256_file(prior_manifest_path),
            "selection": dict(prior_mapping["selection"]),
        },
        "retained_redaction": {
            "policy_revision": REDACTION_POLICY_REVISION,
            "changed_count": len(retained_blind_hash_changes),
            "hash_changes": retained_blind_hash_changes,
        },
    }
    final_private_mapping = {
        "format_version": BLINDING_VERSION,
        "redaction_policy_revision": REDACTION_POLICY_REVISION,
        "source_parquet": str(source),
        "source_parquet_sha256": source_sha256,
        "source_row_count": len(rows),
        "selection": extension_audit,
        "papers": final_private_entries,
    }

    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=f".{destination.name}.staging-", dir=destination.parent)
    )
    try:
        staging.chmod(0o700)
        blind_dir = staging / "blind"
        private_dir = staging / "private"
        blind_dir.mkdir(mode=0o700)
        private_dir.mkdir(mode=0o700)
        blind_dir.chmod(0o700)
        private_dir.chmod(0o700)
        for filename, payload in retained_blind_files + new_blind_files:
            _write_private_file(blind_dir / filename, payload)
        _write_private_file(
            blind_dir / "manifest.json", _json_bytes(final_blind_manifest)
        )
        _write_private_file(
            private_dir / "mapping.json", _json_bytes(final_private_mapping)
        )
        staging.rename(destination)
        destination.chmod(0o700)
        for path in destination.rglob("*"):
            path.chmod(0o600 if path.is_file() else 0o700)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise

    return {
        "output_root": str(destination),
        "paper_count": target_accept + target_reject,
        "retained_paper_count": 40,
        "added_paper_count": len(prepared_new),
        "selected_counts": target_counts,
        "added_counts": added_counts,
        "seed_sha256": _sha256_text(seed),
        "source_parquet_sha256": source_sha256,
        "prior_blind_hashes_preserved": not retained_blind_hash_changes,
        "retained_blind_hash_changed_count": len(retained_blind_hash_changes),
        "retained_blind_hash_changed_ids": [
            item["blind_id"] for item in retained_blind_hash_changes
        ],
        "leak_scan_passed": True,
    }


def _as_binary_label(value: Any, *, field: str) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int) and value in {0, 1}:
        return value
    if isinstance(value, str):
        normalized = value.strip().casefold()
        if normalized == "accept":
            return 1
        if normalized == "reject":
            return 0
    raise BenchmarkError(f"{field} values must be Accept/Reject or 1/0")


def _scalar_metrics(y_true: Sequence[int], y_pred: Sequence[int], scores: Sequence[float]) -> Dict[str, float]:
    if not (len(y_true) == len(y_pred) == len(scores)) or not y_true:
        raise BenchmarkError("y_true, y_pred, and scores must have the same non-zero length")
    tp = sum(truth == 1 and prediction == 1 for truth, prediction in zip(y_true, y_pred))
    tn = sum(truth == 0 and prediction == 0 for truth, prediction in zip(y_true, y_pred))
    fp = sum(truth == 0 and prediction == 1 for truth, prediction in zip(y_true, y_pred))
    fn = sum(truth == 1 and prediction == 0 for truth, prediction in zip(y_true, y_pred))
    positives = tp + fn
    negatives = tn + fp
    if positives == 0 or negatives == 0:
        raise BenchmarkError("Both Accept and Reject ground-truth classes are required")
    tpr = tp / positives
    tnr = tn / negatives
    f1_denominator = 2 * tp + fp + fn
    return {
        "balanced_accuracy": (tpr + tnr) / 2,
        "accuracy": (tp + tn) / len(y_true),
        "f1": (2 * tp / f1_denominator) if f1_denominator else 0.0,
        "auroc": _binary_auroc(y_true, scores),
        "fpr": fp / negatives,
        "fnr": fn / positives,
    }


def _binary_auroc(y_true: Sequence[int], scores: Sequence[float]) -> float:
    """Tie-aware Mann-Whitney AUROC without a scikit-learn dependency."""

    positives = [score for truth, score in zip(y_true, scores) if truth == 1]
    negatives = [score for truth, score in zip(y_true, scores) if truth == 0]
    if not positives or not negatives:
        raise BenchmarkError("AUROC requires both ground-truth classes")
    wins = 0.0
    for positive in positives:
        for negative in negatives:
            if positive > negative:
                wins += 1.0
            elif positive == negative:
                wins += 0.5
    return wins / (len(positives) * len(negatives))


def _percentile(values: Sequence[float], probability: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise BenchmarkError("Cannot compute a percentile of an empty sequence")
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def evaluate_metrics(
    y_true: Sequence[Any],
    reviewer_overall_scores: Sequence[Sequence[Any]],
    *,
    predicted_decisions: Optional[Sequence[Any]] = None,
    decision_threshold: float = 6.0,
    bootstrap_samples: int = 5000,
    bootstrap_seed: int = 2026,
) -> Dict[str, Any]:
    """Evaluate one five-review ensemble score per paper.

    AUROC is pre-specified to use the arithmetic mean of the five independent
    reviewers' ``Overall`` scores. Classification metrics use the supplied final
    decisions when present; otherwise the same mean score is thresholded at 6.
    Confidence intervals use stratified *paper-level* bootstrap resampling.
    """

    truth = [_as_binary_label(value, field="y_true") for value in y_true]
    if len(truth) != len(reviewer_overall_scores) or not truth:
        raise BenchmarkError("One reviewer score list is required for every paper")
    if isinstance(bootstrap_samples, bool) or not isinstance(bootstrap_samples, int) or bootstrap_samples < 1:
        raise BenchmarkError("bootstrap_samples must be a positive integer")
    if isinstance(bootstrap_seed, bool) or not isinstance(bootstrap_seed, int):
        raise BenchmarkError("bootstrap_seed must be an integer")

    mean_scores: List[float] = []
    for paper_index, values in enumerate(reviewer_overall_scores):
        if len(values) != 5:
            raise BenchmarkError(
                f"Paper {paper_index} must have exactly five reviewer Overall scores"
            )
        parsed: List[float] = []
        for value in values:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise BenchmarkError("Reviewer Overall scores must be numeric")
            numeric = float(value)
            if not math.isfinite(numeric) or not 1 <= numeric <= 10:
                raise BenchmarkError("Reviewer Overall scores must be finite and in [1, 10]")
            parsed.append(numeric)
        mean_scores.append(sum(parsed) / 5)

    if predicted_decisions is None:
        predictions = [int(score >= decision_threshold) for score in mean_scores]
        prediction_source = f"five-review mean Overall >= {decision_threshold:g}"
    else:
        if len(predicted_decisions) != len(truth):
            raise BenchmarkError("predicted_decisions must match y_true length")
        predictions = [
            _as_binary_label(value, field="predicted_decisions") for value in predicted_decisions
        ]
        prediction_source = "supplied final reviewer decision"

    point = _scalar_metrics(truth, predictions, mean_scores)
    tp = sum(t == 1 and p == 1 for t, p in zip(truth, predictions))
    tn = sum(t == 0 and p == 0 for t, p in zip(truth, predictions))
    fp = sum(t == 0 and p == 1 for t, p in zip(truth, predictions))
    fn = sum(t == 1 and p == 0 for t, p in zip(truth, predictions))

    positive_indices = [index for index, value in enumerate(truth) if value == 1]
    negative_indices = [index for index, value in enumerate(truth) if value == 0]
    if not positive_indices or not negative_indices:
        raise BenchmarkError("Both Accept and Reject ground-truth classes are required")
    generator = random.Random(bootstrap_seed)
    distributions: Dict[str, List[float]] = {name: [] for name in point}
    for _ in range(bootstrap_samples):
        sampled_indices = [generator.choice(positive_indices) for _ in positive_indices]
        sampled_indices.extend(generator.choice(negative_indices) for _ in negative_indices)
        sampled = _scalar_metrics(
            [truth[index] for index in sampled_indices],
            [predictions[index] for index in sampled_indices],
            [mean_scores[index] for index in sampled_indices],
        )
        for name, value in sampled.items():
            distributions[name].append(value)

    confidence_intervals = {
        name: {
            "lower": _percentile(values, 0.025),
            "upper": _percentile(values, 0.975),
        }
        for name, values in distributions.items()
    }
    return {
        "n_papers": len(truth),
        "n_accept": sum(truth),
        "n_reject": len(truth) - sum(truth),
        "positive_class": "Accept",
        "prediction_source": prediction_source,
        "auroc_score_source": "arithmetic mean of exactly five reviewer Overall scores",
        "metrics": point,
        "confidence_intervals_95": confidence_intervals,
        "confusion_matrix": {
            "labels": ["Reject", "Accept"],
            "matrix": [[tn, fp], [fn, tp]],
            "tn": tn,
            "fp": fp,
            "fn": fn,
            "tp": tp,
        },
        "bootstrap": {
            "method": "stratified paper-level percentile bootstrap",
            "samples": bootstrap_samples,
            "seed": bootstrap_seed,
            "confidence_level": 0.95,
        },
        "paper_mean_overall_scores": mean_scores,
    }


def evaluate_review_bundles(
    cases: Sequence[Mapping[str, Any]],
    *,
    decision_threshold: float = 6.0,
    bootstrap_samples: int = 5000,
    bootstrap_seed: int = 2026,
) -> Dict[str, Any]:
    """Evaluate saved AutoReviewer-like bundles with ground-truth labels.

    Each case needs ``ground_truth``, five ``individual_reviews``, and may have
    ``final_review.Decision``. Individual entries may either be review objects
    directly or wrapper objects with a ``review`` member, matching ``core.py``.
    """

    truth: List[Any] = []
    scores: List[List[Any]] = []
    predictions: List[Any] = []
    all_have_final = True
    for case_index, case in enumerate(cases):
        truth.append(case.get("ground_truth"))
        reviews = case.get("individual_reviews")
        if not isinstance(reviews, Sequence) or isinstance(reviews, (str, bytes)):
            raise BenchmarkError(f"Case {case_index} has no individual_reviews list")
        paper_scores: List[Any] = []
        for review_entry in reviews:
            review = review_entry.get("review") if isinstance(review_entry, Mapping) and "review" in review_entry else review_entry
            if not isinstance(review, Mapping) or "Overall" not in review:
                raise BenchmarkError(f"Case {case_index} has an invalid individual review")
            paper_scores.append(review["Overall"])
        scores.append(paper_scores)
        final_review = case.get("final_review")
        if isinstance(final_review, Mapping) and "Decision" in final_review:
            predictions.append(final_review["Decision"])
        else:
            all_have_final = False

    if not all_have_final:
        predictions_argument: Optional[Sequence[Any]] = None
    else:
        predictions_argument = predictions
    return evaluate_metrics(
        truth,
        scores,
        predicted_decisions=predictions_argument,
        decision_threshold=decision_threshold,
        bootstrap_samples=bootstrap_samples,
        bootstrap_seed=bootstrap_seed,
    )
