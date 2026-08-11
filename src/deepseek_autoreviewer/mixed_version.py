"""Build the label-isolated mixed-version manuscript set used by Nature.

This module is deliberately local-only.  It never imports a network client,
loads an environment file, or calls a model.  It combines the already frozen
200-paper selection with two manuscript sources:

* accepted papers: official camera-ready PDFs, extracted page-by-page with
  PyMuPDF;
* rejected papers: the original ProReviewer markdown snapshot.

Unlike :mod:`deepseek_autoreviewer.benchmark`, the resulting manuscripts are
*not* strictly blinded.  Source identifiers and version clues are therefore
declared explicitly in the label-isolated manifest.  The rule connecting a
version to a decision label, the source identifiers, and official provenance
remain confined to ``private/mapping.json``.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple

import pymupdf

from .benchmark import ACCEPT_DECISIONS, REJECT_DECISION, read_proreviewer_parquet


FORMAT_VERSION = "deepseek-autoreviewer-nature-mixed-version-v1"
CAMERA_PROVENANCE_FORMAT = "iclr2026-camera-ready-provenance-v1"
OFFICIAL_CAMERA_SOURCE_KIND = "official_iclr2026_proceedings_camera_ready"
PDF_EXTRACTION_POLICY = "pymupdf-page-get-text-default-order-concatenated-v1"
EXPECTED_ACCEPT_COUNT = 78
EXPECTED_REJECT_COUNT = 122

_BLIND_ID = re.compile(r"^B[0-9]{3}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_PROCEEDINGS_ID = re.compile(r"^[0-9a-f]{32}$")


class MixedVersionError(ValueError):
    """Raised when an input cannot support a fail-closed mixed-version build."""


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _require_sha256(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        raise MixedVersionError(f"{field} must be a lowercase SHA-256 digest")
    return value


def _require_proceedings_id(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or _PROCEEDINGS_ID.fullmatch(value) is None:
        raise MixedVersionError(f"{field} must be a 32-character lowercase hex ID")
    return value


def _require_nonempty_string(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MixedVersionError(f"{field} must be a non-empty string")
    return value


def _read_json_object(path: Path, *, description: str) -> Tuple[Dict[str, Any], str]:
    requested = Path(path).expanduser()
    if requested.is_symlink():
        raise MixedVersionError(f"{description} must not be a symbolic link")
    source = requested.resolve()
    if not source.is_file():
        raise FileNotFoundError(f"{description} not found: {source}")
    try:
        value = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise MixedVersionError(f"Invalid {description}: {source}") from error
    if not isinstance(value, dict):
        raise MixedVersionError(f"{description} must contain a JSON object")
    return value, _sha256_file(source)


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


def _markdown_authors(row: Mapping[str, Any]) -> Any:
    markdown = row.get("markdown")
    if not isinstance(markdown, Mapping):
        return []
    metadata = markdown.get("metadata")
    if not isinstance(metadata, Mapping):
        return []
    authors = metadata.get("authors", [])
    return authors if isinstance(authors, list) else []


def _validate_real_input_file(path: Path, *, description: str) -> Path:
    requested = Path(path).expanduser()
    if requested.is_symlink():
        raise MixedVersionError(f"{description} must not be a symbolic link")
    resolved = requested.resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"{description} not found: {resolved}")
    return resolved


def _safe_pdf_path(camera_root: Path, value: Any, *, blind_id: str) -> Path:
    filename = _require_nonempty_string(value, field=f"{blind_id}.pdf_file")
    relative = Path(filename)
    if relative.is_absolute() or ".." in relative.parts:
        raise MixedVersionError(f"Unsafe camera-ready PDF path for {blind_id}")
    candidate = camera_root / relative
    if candidate.is_symlink() or not candidate.is_file():
        raise MixedVersionError(f"Missing or linked camera-ready PDF for {blind_id}")
    resolved = candidate.resolve()
    try:
        resolved.relative_to(camera_root)
    except ValueError:
        raise MixedVersionError(
            f"Camera-ready PDF path escapes its private directory for {blind_id}"
        ) from None
    return resolved


def _extract_pdf_text(
    path: Path,
    *,
    expected_pages: int,
    min_characters: int,
) -> Tuple[str, Dict[str, Any]]:
    """Extract deterministic full-document plain text in physical page order."""

    try:
        document = pymupdf.open(path)
    except Exception as error:
        raise MixedVersionError(f"Could not open camera-ready PDF: {path.name}") from error
    try:
        if document.needs_pass:
            raise MixedVersionError(f"Encrypted camera-ready PDF: {path.name}")
        if document.page_count != expected_pages:
            raise MixedVersionError(
                f"Camera-ready PDF page-count mismatch for {path.name}"
            )
        page_texts: List[str] = []
        for page in document:
            # Nature describes feeding raw text extracted with PyMuPDF.  The
            # default page.get_text() order is therefore kept, and no synthetic
            # page labels are inserted into the manuscript seen by the model.
            page_texts.append(page.get_text().strip())
        text = "\n\n".join(page_texts).strip()
    except MixedVersionError:
        raise
    except Exception as error:
        raise MixedVersionError(
            f"Could not extract camera-ready PDF text: {path.name}"
        ) from error
    finally:
        document.close()

    if len(text) < min_characters:
        raise MixedVersionError(
            f"Only {len(text)} characters were extracted from {path.name}; "
            "the PDF may require OCR"
        )
    return text, {
        "pdf_sha256": _sha256_file(path),
        "pdf_bytes": path.stat().st_size,
        "pdf_page_count": expected_pages,
        "extracted_characters": len(text),
        "extraction_policy": PDF_EXTRACTION_POLICY,
        "text_sha256": _sha256_bytes(text.encode("utf-8")),
    }


def _write_private_file(path: Path, payload: bytes) -> None:
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


def _mapping_hash_from_provenance(manifest: Mapping[str, Any]) -> str:
    direct = manifest.get("source_mapping_sha256")
    if isinstance(direct, str):
        return _require_sha256(direct, field="source_mapping_sha256")
    source_mapping = manifest.get("source_mapping")
    if isinstance(source_mapping, Mapping):
        for key in ("sha256", "mapping_sha256", "source_mapping_sha256"):
            value = source_mapping.get(key)
            if isinstance(value, str):
                return _require_sha256(value, field=f"source_mapping.{key}")
    raise MixedVersionError(
        "Camera-ready provenance does not bind the frozen source mapping hash"
    )


def _validate_camera_provenance(
    manifest: Mapping[str, Any],
    *,
    mapping_sha256: str,
    source_parquet_sha256: str,
    expected_accept_count: int,
    expected_reject_count: int,
) -> List[Dict[str, Any]]:
    if manifest.get("format_version") != CAMERA_PROVENANCE_FORMAT:
        raise MixedVersionError("Unsupported camera-ready provenance format_version")
    if manifest.get("private_label_aware_preparation") is not True:
        raise MixedVersionError(
            "Camera-ready provenance must declare private label-aware preparation"
        )
    if _mapping_hash_from_provenance(manifest) != mapping_sha256:
        raise MixedVersionError("Camera-ready provenance source mapping hash mismatch")
    if manifest.get("source_parquet_sha256") != source_parquet_sha256:
        raise MixedVersionError("Camera-ready provenance source parquet hash mismatch")
    if manifest.get("expected_accept_count") != expected_accept_count:
        raise MixedVersionError("Camera-ready provenance Accept count mismatch")
    if manifest.get("expected_reject_count") != expected_reject_count:
        raise MixedVersionError("Camera-ready provenance Reject count mismatch")
    if manifest.get("downloaded_pdf_count") != expected_accept_count:
        raise MixedVersionError("Camera-ready provenance PDF count mismatch")
    index_url = manifest.get("proceedings_index_url")
    if not isinstance(index_url, str) or not index_url.startswith(
        "https://proceedings.iclr.cc/"
    ):
        raise MixedVersionError("Camera-ready provenance has a non-official index URL")
    _require_sha256(
        manifest.get("proceedings_index_sha256"),
        field="proceedings_index_sha256",
    )
    match_counts = manifest.get("match_counts")
    if (
        not isinstance(match_counts, Mapping)
        or any(
            isinstance(value, bool) or not isinstance(value, int) or value < 0
            for value in match_counts.values()
        )
        or sum(match_counts.values()) != expected_accept_count
    ):
        raise MixedVersionError("Camera-ready provenance match counts are incomplete")
    papers = manifest.get("papers")
    if not isinstance(papers, list) or len(papers) != expected_accept_count:
        raise MixedVersionError("Camera-ready provenance papers list is incomplete")
    values: List[Dict[str, Any]] = []
    for index, paper in enumerate(papers):
        if not isinstance(paper, Mapping):
            raise MixedVersionError(
                f"Camera-ready provenance paper {index} must be an object"
            )
        values.append(dict(paper))
    declared_bytes = manifest.get("downloaded_pdf_bytes")
    record_bytes = [paper.get("pdf_bytes") for paper in values]
    if (
        isinstance(declared_bytes, bool)
        or not isinstance(declared_bytes, int)
        or declared_bytes < 1
        or any(
            isinstance(value, bool) or not isinstance(value, int) or value < 1
            for value in record_bytes
        )
        or sum(record_bytes) != declared_bytes
    ):
        raise MixedVersionError("Camera-ready provenance PDF byte total mismatch")
    return values


def build_mixed_version_benchmark(
    strict_private_mapping_path: Path,
    parquet_path: Path,
    camera_ready_provenance_path: Path,
    output_root: Path,
    *,
    expected_accept_count: int = EXPECTED_ACCEPT_COUNT,
    expected_reject_count: int = EXPECTED_REJECT_COUNT,
    min_pdf_characters: int = 1000,
) -> Dict[str, Any]:
    """Atomically build a new Nature-style mixed-version input tree.

    All 200 frozen selections and all camera-ready artifacts are checked before
    the destination becomes visible.  ``output_root`` must be a brand-new path.
    The existing strict benchmark is read-only and is never copied over or
    modified.
    """

    for value, field in (
        (expected_accept_count, "expected_accept_count"),
        (expected_reject_count, "expected_reject_count"),
        (min_pdf_characters, "min_pdf_characters"),
    ):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise MixedVersionError(f"{field} must be a positive integer")
    if expected_accept_count + expected_reject_count > 999:
        raise MixedVersionError("At most 999 papers are supported")

    strict_mapping_path = _validate_real_input_file(
        strict_private_mapping_path, description="strict private mapping"
    )
    source = _validate_real_input_file(parquet_path, description="source parquet")
    provenance_path = _validate_real_input_file(
        camera_ready_provenance_path,
        description="camera-ready provenance manifest",
    )
    camera_root = provenance_path.parent
    if camera_root.is_symlink() or not camera_root.is_dir():
        raise MixedVersionError("Camera-ready private directory must be a real directory")

    destination_requested = Path(output_root).expanduser()
    if destination_requested.is_symlink() or os.path.lexists(destination_requested):
        raise FileExistsError(
            f"Refusing to overwrite mixed-version output: {destination_requested}"
        )
    destination = destination_requested.resolve()

    strict_mapping, strict_mapping_sha256 = _read_json_object(
        strict_mapping_path, description="strict private mapping"
    )
    provenance, provenance_sha256 = _read_json_object(
        provenance_path, description="camera-ready provenance manifest"
    )
    source_sha256 = _sha256_file(source)
    if strict_mapping.get("source_parquet_sha256") != source_sha256:
        raise MixedVersionError("Strict mapping does not match the source parquet hash")

    rows = read_proreviewer_parquet(source)
    if strict_mapping.get("source_row_count") != len(rows):
        raise MixedVersionError("Strict mapping does not match the source row count")
    source_by_id: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        paper_id = row.get("paper_id")
        if not isinstance(paper_id, str) or not paper_id:
            continue
        if paper_id in source_by_id:
            raise MixedVersionError(f"Duplicate source paper_id: {paper_id}")
        source_by_id[paper_id] = dict(row)

    private_values = strict_mapping.get("papers")
    paper_count = expected_accept_count + expected_reject_count
    if not isinstance(private_values, list) or len(private_values) != paper_count:
        raise MixedVersionError("Strict mapping does not contain the expected paper count")
    strict_papers: List[Dict[str, Any]] = []
    expected_ids = [f"B{index:03d}" for index in range(1, paper_count + 1)]
    for index, value in enumerate(private_values):
        if not isinstance(value, Mapping):
            raise MixedVersionError(f"Strict mapping paper {index} must be an object")
        strict_papers.append(dict(value))
    if [paper.get("blind_id") for paper in strict_papers] != expected_ids:
        raise MixedVersionError("Strict mapping IDs must be contiguous and ordered")

    labels = Counter(paper.get("ground_truth") for paper in strict_papers)
    if labels != Counter(
        {"Accept": expected_accept_count, "Reject": expected_reject_count}
    ):
        raise MixedVersionError("Strict mapping class counts do not match the protocol")

    camera_values = _validate_camera_provenance(
        provenance,
        mapping_sha256=strict_mapping_sha256,
        source_parquet_sha256=source_sha256,
        expected_accept_count=expected_accept_count,
        expected_reject_count=expected_reject_count,
    )
    camera_by_id: Dict[str, Dict[str, Any]] = {}
    for paper in camera_values:
        blind_id = paper.get("blind_id")
        if not isinstance(blind_id, str) or _BLIND_ID.fullmatch(blind_id) is None:
            raise MixedVersionError("Camera-ready provenance has an invalid blind_id")
        if blind_id in camera_by_id:
            raise MixedVersionError(
                f"Duplicate camera-ready provenance blind_id: {blind_id}"
            )
        camera_by_id[blind_id] = paper

    # Prepare every payload in memory.  Nothing under destination exists yet.
    prepared_files: List[Tuple[str, bytes]] = []
    public_entries: List[Dict[str, Any]] = []
    private_entries: List[Dict[str, Any]] = []
    seen_source_ids = set()
    accept_ids = set()
    for strict_paper in strict_papers:
        blind_id = _require_nonempty_string(
            strict_paper.get("blind_id"), field="blind_id"
        )
        label = strict_paper.get("ground_truth")
        paper_id = _require_nonempty_string(
            strict_paper.get("paper_id"), field=f"{blind_id}.paper_id"
        )
        if paper_id in seen_source_ids:
            raise MixedVersionError(f"Duplicate selected source paper_id: {paper_id}")
        seen_source_ids.add(paper_id)
        selection_sha256 = _require_sha256(
            strict_paper.get("selection_sha256"),
            field=f"{blind_id}.selection_sha256",
        )
        prior_raw_hash = _require_sha256(
            strict_paper.get("raw_text_sha256"),
            field=f"{blind_id}.raw_text_sha256",
        )
        prior_blind_hash = _require_sha256(
            strict_paper.get("blind_text_sha256"),
            field=f"{blind_id}.blind_text_sha256",
        )
        source_row = source_by_id.get(paper_id)
        if source_row is None:
            raise MixedVersionError(f"Selected source record is missing for {blind_id}")
        source_decision = _decision(source_row)
        expected_label = "Accept" if source_decision in ACCEPT_DECISIONS else (
            "Reject" if source_decision == REJECT_DECISION else ""
        )
        if expected_label != label:
            raise MixedVersionError(f"Source label mismatch for {blind_id}")
        if strict_paper.get("source_decision") != source_decision:
            raise MixedVersionError(f"Source decision mismatch for {blind_id}")
        if strict_paper.get("title", "") != source_row.get("title", ""):
            raise MixedVersionError(f"Source title mismatch for {blind_id}")
        if strict_paper.get("arxiv_id", "") != source_row.get("arxiv_id", ""):
            raise MixedVersionError(f"Source arXiv ID mismatch for {blind_id}")
        if strict_paper.get("authors", []) != _markdown_authors(source_row):
            raise MixedVersionError(f"Source authors mismatch for {blind_id}")
        source_markdown = _paper_content(source_row)
        if not source_markdown:
            raise MixedVersionError(f"Source markdown is empty for {blind_id}")
        source_markdown_bytes = source_markdown.encode("utf-8")
        if _sha256_bytes(source_markdown_bytes) != prior_raw_hash:
            raise MixedVersionError(f"Source raw markdown hash mismatch for {blind_id}")

        source_binding: Dict[str, Any]
        if label == "Accept":
            accept_ids.add(blind_id)
            camera = camera_by_id.get(blind_id)
            if camera is None:
                raise MixedVersionError(
                    f"Missing camera-ready provenance for accepted paper {blind_id}"
                )
            if camera.get("openreview_paper_id") != paper_id:
                raise MixedVersionError(
                    f"Camera-ready source paper ID mismatch for {blind_id}"
                )
            if camera.get("source_kind") != OFFICIAL_CAMERA_SOURCE_KIND:
                raise MixedVersionError(
                    f"Camera-ready provenance source_kind mismatch for {blind_id}"
                )
            if camera.get("initial_title") != strict_paper.get("title", ""):
                raise MixedVersionError(
                    f"Camera-ready provenance initial title mismatch for {blind_id}"
                )
            if camera.get("initial_authors") != strict_paper.get("authors", []):
                raise MixedVersionError(
                    f"Camera-ready provenance initial authors mismatch for {blind_id}"
                )
            _require_proceedings_id(
                camera.get("proceedings_hash"),
                field=f"{blind_id}.proceedings_hash",
            )
            _require_sha256(
                camera.get("abstract_sha256"),
                field=f"{blind_id}.abstract_sha256",
            )
            abstract_url = camera.get("abstract_url")
            if not isinstance(abstract_url, str) or not abstract_url.startswith(
                "https://proceedings.iclr.cc/"
            ):
                raise MixedVersionError(
                    f"Camera-ready provenance lacks an official abstract URL for {blind_id}"
                )
            citation_title = camera.get("citation_title")
            if not isinstance(citation_title, str) or not citation_title.strip():
                raise MixedVersionError(
                    f"Camera-ready citation title is missing for {blind_id}"
                )
            citation_authors = camera.get("citation_authors")
            if not isinstance(citation_authors, list) or not citation_authors:
                raise MixedVersionError(
                    f"Camera-ready citation authors are missing for {blind_id}"
                )
            pdf_url = camera.get("citation_pdf_url")
            if (
                not isinstance(pdf_url, str)
                or not pdf_url.startswith("https://proceedings.iclr.cc/")
                or not pdf_url.casefold().endswith(".pdf")
            ):
                raise MixedVersionError(
                    f"Camera-ready provenance lacks an official PDF URL for {blind_id}"
                )
            if camera.get("first_page_conference_marker") is not True:
                raise MixedVersionError(
                    f"Camera-ready conference marker was not verified for {blind_id}"
                )
            expected_pdf_hash = _require_sha256(
                camera.get("pdf_sha256"), field=f"{blind_id}.pdf_sha256"
            )
            expected_pdf_bytes = camera.get("pdf_bytes")
            expected_pdf_pages = camera.get("pdf_page_count")
            if (
                isinstance(expected_pdf_bytes, bool)
                or not isinstance(expected_pdf_bytes, int)
                or expected_pdf_bytes < 1
            ):
                raise MixedVersionError(f"Invalid camera-ready size for {blind_id}")
            if (
                isinstance(expected_pdf_pages, bool)
                or not isinstance(expected_pdf_pages, int)
                or expected_pdf_pages < 1
            ):
                raise MixedVersionError(f"Invalid camera-ready page count for {blind_id}")
            pdf_path = _safe_pdf_path(camera_root, camera.get("pdf_file"), blind_id=blind_id)
            if pdf_path.stat().st_size != expected_pdf_bytes:
                raise MixedVersionError(f"Camera-ready PDF size mismatch for {blind_id}")
            if _sha256_file(pdf_path) != expected_pdf_hash:
                raise MixedVersionError(f"Camera-ready PDF hash mismatch for {blind_id}")
            text, extraction = _extract_pdf_text(
                pdf_path,
                expected_pages=expected_pdf_pages,
                min_characters=min_pdf_characters,
            )
            if extraction["pdf_sha256"] != expected_pdf_hash:
                raise MixedVersionError(
                    f"Camera-ready PDF changed during extraction for {blind_id}"
                )
            payload = text.encode("utf-8")
            source_binding = {
                "source_version": "camera-ready",
                "input_format": "pymupdf-plain-text",
                "source_initial_markdown_sha256": prior_raw_hash,
                "source_pdf_sha256": expected_pdf_hash,
                "source_pdf_bytes": expected_pdf_bytes,
                "source_pdf_page_count": expected_pdf_pages,
                "input_text_sha256": extraction["text_sha256"],
                "input_characters": extraction["extracted_characters"],
                "pdf_extraction_policy": extraction["extraction_policy"],
                "official_provenance": dict(camera),
            }
        else:
            if blind_id in camera_by_id:
                raise MixedVersionError(
                    f"Camera-ready provenance unexpectedly includes rejected paper {blind_id}"
                )
            payload = source_markdown_bytes
            source_binding = {
                "source_version": "initial-submission",
                "input_format": "proreviewer-raw-markdown",
                "source_initial_markdown_sha256": prior_raw_hash,
                "input_text_sha256": prior_raw_hash,
                "input_characters": len(source_markdown),
            }

        input_hash = _sha256_bytes(payload)
        if input_hash != source_binding["input_text_sha256"]:
            raise MixedVersionError(f"Internal input-text hash mismatch for {blind_id}")
        filename = f"{blind_id}.txt"
        prepared_files.append((filename, payload))
        public_entries.append(
            {
                "blind_id": blind_id,
                "filename": filename,
                # Kept for compatibility with the hash-bound benchmark runner;
                # the top-level manifest states that these texts are not blinded.
                "blind_text_sha256": input_hash,
                "input_text_sha256": input_hash,
                "characters": len(payload.decode("utf-8")),
            }
        )
        private_entry = dict(strict_paper)
        private_entry.update(
            {
                "selection_sha256": selection_sha256,
                "prior_raw_text_sha256": prior_raw_hash,
                "prior_blind_text_sha256": prior_blind_hash,
                "raw_text_sha256": input_hash,
                "blind_text_sha256": input_hash,
                **source_binding,
            }
        )
        private_entries.append(private_entry)

    if set(camera_by_id) != accept_ids:
        extras = sorted(set(camera_by_id).difference(accept_ids))
        missing = sorted(accept_ids.difference(camera_by_id))
        raise MixedVersionError(
            "Camera-ready provenance does not exactly cover the accepted cohort "
            f"(missing={len(missing)}, extra={len(extras)})"
        )

    label_isolated_manifest = {
        "format_version": FORMAT_VERSION,
        "paper_count": paper_count,
        "contains_ground_truth": False,
        "contains_source_identifiers": True,
        "contains_version_label_clues": True,
        "contains_input_format_label_clues": True,
        "strictly_blinded": False,
        "version_policy_disclosed_here": False,
        "source_identifiers_location": "manuscript text only; source mapping is private",
        "reviewer_network_policy": (
            "browser/search/retrieval/tools disabled; only the configured model API "
            "transport is permitted during review"
        ),
        "papers": public_entries,
    }
    private_mapping = {
        "format_version": FORMAT_VERSION,
        "source_parquet": str(source),
        "source_parquet_sha256": source_sha256,
        "source_row_count": len(rows),
        "strict_source_mapping": str(strict_mapping_path),
        "strict_source_mapping_sha256": strict_mapping_sha256,
        "strict_source_format_version": strict_mapping.get("format_version"),
        "camera_ready_provenance": str(provenance_path),
        "camera_ready_provenance_sha256": provenance_sha256,
        "camera_ready_provenance_format_version": provenance.get("format_version"),
        "selection": strict_mapping.get("selection"),
        "version_label_policy": {
            "visibility": "private only",
            "Accept": "official ICLR 2026 camera-ready PDF",
            "Reject": "ProReviewer initial-submission raw markdown snapshot",
        },
        "papers": private_entries,
    }

    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.staging-", dir=destination.parent
        )
    )
    try:
        staging.chmod(0o700)
        label_isolated = staging / "label_isolated"
        private = staging / "private"
        label_isolated.mkdir(mode=0o700)
        private.mkdir(mode=0o700)
        for filename, payload in prepared_files:
            _write_private_file(label_isolated / filename, payload)
        _write_private_file(
            label_isolated / "manifest.json", _json_bytes(label_isolated_manifest)
        )
        _write_private_file(private / "mapping.json", _json_bytes(private_mapping))
        # Apply every permission before publication so the atomic rename is the
        # final fallible operation.  A failure above leaves no formal output.
        staging.chmod(0o700)
        for path in staging.rglob("*"):
            path.chmod(0o600 if path.is_file() else 0o700)
        staging.rename(destination)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise

    return {
        "output_root": str(destination),
        "paper_count": paper_count,
        "selected_counts": {
            "Accept": expected_accept_count,
            "Reject": expected_reject_count,
        },
        "source_parquet_sha256": source_sha256,
        "strict_source_mapping_sha256": strict_mapping_sha256,
        "camera_ready_provenance_sha256": provenance_sha256,
        "contains_source_identifiers": True,
        "contains_version_label_clues": True,
        "contains_input_format_label_clues": True,
        "contains_ground_truth": False,
    }
