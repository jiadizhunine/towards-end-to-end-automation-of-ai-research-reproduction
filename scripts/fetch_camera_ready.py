#!/usr/bin/env python3
"""Fetch the accepted-paper camera-ready PDFs from the official ICLR proceedings.

This program is deliberately label-aware and must only be used during private
benchmark preparation.  It never reads environment variables.  By default it
performs a dry run; ``--download`` is required to create an output directory.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import stat
import tempfile
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, BinaryIO, Callable, Mapping, Sequence
from urllib.request import Request, urlopen

import pymupdf


PROCEEDINGS_INDEX_URL = "https://proceedings.iclr.cc/paper_files/paper/2026"
PROCEEDINGS_ORIGIN = "https://proceedings.iclr.cc"
ABSTRACT_PATH_RE = re.compile(
    r"^/paper_files/paper/2026/hash/(?P<hash>[0-9a-f]{32})-Abstract-Conference\.html$"
)
CAMERA_READY_MARKER = "published as a conference paper at iclr 2026"
EXPECTED_ACCEPTS = 78
EXPECTED_REJECTS = 122
MAX_INDEX_BYTES = 8 * 1024 * 1024
MAX_ABSTRACT_BYTES = 2 * 1024 * 1024
MAX_PDF_BYTES = 100 * 1024 * 1024
USER_AGENT = "deepseek-autoreviewer-camera-ready-fetch/1.0"


class CameraReadyError(RuntimeError):
    """Raised when a source or validation invariant fails."""


@dataclass(frozen=True)
class ProceedingsPaper:
    title: str
    authors: tuple[str, ...]
    abstract_path: str
    proceedings_hash: str

    @property
    def abstract_url(self) -> str:
        return f"{PROCEEDINGS_ORIGIN}{self.abstract_path}"

    @property
    def pdf_url(self) -> str:
        return (
            f"{PROCEEDINGS_ORIGIN}/paper_files/paper/2026/file/"
            f"{self.proceedings_hash}-Paper-Conference.pdf"
        )


@dataclass(frozen=True)
class Match:
    private_paper: Mapping[str, Any]
    proceedings_paper: ProceedingsPaper
    match_mode: str
    title_similarity: float
    author_similarity: float


@dataclass(frozen=True)
class FetchResponse:
    stream: BinaryIO
    status: int
    content_type: str
    content_length: int | None

    def close(self) -> None:
        self.stream.close()

    def __enter__(self) -> "FetchResponse":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


OpenUrl = Callable[[str, float], FetchResponse]


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalize_text(value: str) -> str:
    return re.sub(
        r"[^\w]+",
        "",
        unicodedata.normalize("NFKC", value).casefold(),
        flags=re.UNICODE,
    )


def _normalize_author(value: str) -> str:
    ascii_value = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    return re.sub(r"[^a-z0-9]+", "", ascii_value.casefold())


def _mean_author_similarity(source: Sequence[str], candidate: Sequence[str]) -> float:
    if len(source) != len(candidate) or not source:
        return 0.0
    scores = (
        SequenceMatcher(None, _normalize_author(left), _normalize_author(right)).ratio()
        for left, right in zip(source, candidate)
    )
    return sum(scores) / len(source)


class _IndexParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._href: str | None = None
        self._title_parts: list[str] = []
        self._awaiting_authors = False
        self._author_parts: list[str] = []
        self.papers: list[ProceedingsPaper] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "a" and attributes.get("title") == "paper title":
            href = attributes.get("href")
            if href and ABSTRACT_PATH_RE.fullmatch(href):
                self._href = href
                self._title_parts = []
        elif (
            tag == "span"
            and attributes.get("class") == "paper-authors"
            and self._awaiting_authors
        ):
            self._author_parts = []

    def handle_data(self, data: str) -> None:
        if self._href is not None and not self._awaiting_authors:
            self._title_parts.append(data)
        elif self._awaiting_authors:
            self._author_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href is not None and not self._awaiting_authors:
            self._awaiting_authors = True
        elif tag == "span" and self._href is not None and self._awaiting_authors:
            title = html.unescape("".join(self._title_parts)).strip()
            authors_text = html.unescape("".join(self._author_parts)).strip()
            match = ABSTRACT_PATH_RE.fullmatch(self._href)
            if title and authors_text and match:
                self.papers.append(
                    ProceedingsPaper(
                        title=title,
                        authors=tuple(
                            part.strip() for part in authors_text.split(",") if part.strip()
                        ),
                        abstract_path=self._href,
                        proceedings_hash=match.group("hash"),
                    )
                )
            self._href = None
            self._title_parts = []
            self._author_parts = []
            self._awaiting_authors = False


class _MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: dict[str, list[str]] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "meta":
            return
        attributes = dict(attrs)
        name = attributes.get("name", "")
        content = attributes.get("content")
        if name.startswith("citation_") and content is not None:
            self.values.setdefault(name, []).append(html.unescape(content))


def parse_proceedings_index(payload: bytes) -> list[ProceedingsPaper]:
    parser = _IndexParser()
    parser.feed(payload.decode("utf-8", errors="strict"))
    if not parser.papers:
        raise CameraReadyError("Official proceedings index contains no paper records")
    hashes = [paper.proceedings_hash for paper in parser.papers]
    if len(hashes) != len(set(hashes)):
        raise CameraReadyError("Official proceedings index contains duplicate paper hashes")
    return parser.papers


def parse_citation_metadata(payload: bytes) -> dict[str, list[str]]:
    parser = _MetaParser()
    parser.feed(payload.decode("utf-8", errors="strict"))
    return parser.values


def _load_private_mapping(
    path: Path,
    *,
    expected_accepts: int = EXPECTED_ACCEPTS,
    expected_rejects: int = EXPECTED_REJECTS,
) -> tuple[dict[str, Any], list[Mapping[str, Any]]]:
    requested = path.expanduser()
    if requested.is_symlink() or not requested.is_file():
        raise CameraReadyError("Private mapping must be a regular, non-symlink file")
    try:
        mapping = json.loads(requested.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CameraReadyError(f"Cannot read private mapping: {error}") from error
    if not isinstance(mapping, dict) or not isinstance(mapping.get("papers"), list):
        raise CameraReadyError("Private mapping has no paper list")
    papers = mapping["papers"]
    accepts = [paper for paper in papers if paper.get("ground_truth") == "Accept"]
    rejects = [paper for paper in papers if paper.get("ground_truth") == "Reject"]
    if len(accepts) != expected_accepts or len(rejects) != expected_rejects:
        raise CameraReadyError(
            "Private mapping class counts differ from the frozen cohort: "
            f"Accept={len(accepts)}, Reject={len(rejects)}"
        )
    blind_ids = [paper.get("blind_id") for paper in papers]
    if any(not isinstance(value, str) or not value for value in blind_ids):
        raise CameraReadyError("Every private paper needs a blind_id")
    if len(blind_ids) != len(set(blind_ids)):
        raise CameraReadyError("Private mapping contains duplicate blind_id values")
    for paper in accepts:
        if not isinstance(paper.get("title"), str) or not paper["title"].strip():
            raise CameraReadyError(f"Accepted paper {paper['blind_id']} has no title")
        authors = paper.get("authors")
        if not isinstance(authors, list) or not all(
            isinstance(author, str) and author.strip() for author in authors
        ):
            raise CameraReadyError(f"Accepted paper {paper['blind_id']} has invalid authors")
        if not isinstance(paper.get("paper_id"), str) or not paper["paper_id"].strip():
            raise CameraReadyError(f"Accepted paper {paper['blind_id']} has no paper_id")
    return mapping, accepts


def match_accepts(
    accepts: Sequence[Mapping[str, Any]],
    proceedings: Sequence[ProceedingsPaper],
) -> list[Match]:
    by_title: dict[str, list[ProceedingsPaper]] = {}
    for paper in proceedings:
        by_title.setdefault(_normalize_text(paper.title), []).append(paper)

    matches: list[Match] = []
    used_hashes: set[str] = set()
    for private in accepts:
        title = str(private["title"])
        authors = tuple(str(value) for value in private["authors"])
        exact = by_title.get(_normalize_text(title), [])
        if len(exact) > 1:
            raise CameraReadyError(
                f"Ambiguous exact proceedings title for {private['blind_id']}"
            )
        if len(exact) == 1:
            candidate = exact[0]
            mode = "title_exact"
            title_similarity = 1.0
            author_similarity = _mean_author_similarity(authors, candidate.authors)
            if author_similarity < 0.90:
                raise CameraReadyError(
                    f"Exact-title proceedings author mismatch for {private['blind_id']}"
                )
        else:
            ranked: list[tuple[float, float, ProceedingsPaper]] = []
            for candidate_value in proceedings:
                title_score = SequenceMatcher(
                    None, title.casefold(), candidate_value.title.casefold()
                ).ratio()
                if title_score < 0.80:
                    continue
                author_score = _mean_author_similarity(authors, candidate_value.authors)
                if author_score >= 0.90:
                    ranked.append((title_score, author_score, candidate_value))
            ranked.sort(
                key=lambda value: (
                    value[0],
                    value[1],
                    value[2].proceedings_hash,
                ),
                reverse=True,
            )
            if len(ranked) != 1:
                raise CameraReadyError(
                    f"Expected one title-change match for {private['blind_id']}, found {len(ranked)}"
                )
            title_similarity, author_similarity, candidate = ranked[0]
            mode = "title_changed_author_match"

        if candidate.proceedings_hash in used_hashes:
            raise CameraReadyError("Two private papers matched the same proceedings paper")
        used_hashes.add(candidate.proceedings_hash)
        matches.append(
            Match(
                private_paper=private,
                proceedings_paper=candidate,
                match_mode=mode,
                title_similarity=title_similarity,
                author_similarity=author_similarity,
            )
        )
    return matches


def _default_open_url(url: str, timeout: float) -> FetchResponse:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    raw = urlopen(request, timeout=timeout)
    status_value = getattr(raw, "status", None)
    if status_value is None:
        status_value = raw.getcode()
    status = int(status_value)
    content_type = raw.headers.get_content_type()
    content_length_value = raw.headers.get("Content-Length")
    content_length = int(content_length_value) if content_length_value else None
    return FetchResponse(raw, status, content_type, content_length)


def _read_bounded(
    response: FetchResponse,
    *,
    expected_type: str,
    max_bytes: int,
) -> bytes:
    if response.status != 200:
        raise CameraReadyError(f"Unexpected HTTP status {response.status}")
    if response.content_type != expected_type:
        raise CameraReadyError(
            f"Expected {expected_type}, received {response.content_type or 'unknown'}"
        )
    if response.content_length is not None and response.content_length > max_bytes:
        raise CameraReadyError("Response exceeds configured size limit")
    payload = bytearray()
    while True:
        chunk = response.stream.read(1024 * 1024)
        if not chunk:
            break
        payload.extend(chunk)
        if len(payload) > max_bytes:
            raise CameraReadyError("Response exceeds configured size limit")
    if response.content_length is not None and len(payload) != response.content_length:
        raise CameraReadyError("Response length differs from Content-Length")
    return bytes(payload)


def _fetch_bytes(
    url: str,
    *,
    expected_type: str,
    max_bytes: int,
    timeout: float,
    open_url: OpenUrl,
) -> bytes:
    try:
        with open_url(url, timeout) as response:
            return _read_bounded(
                response, expected_type=expected_type, max_bytes=max_bytes
            )
    except CameraReadyError:
        raise
    except Exception as error:
        raise CameraReadyError(f"Failed to fetch {url}: {error}") from error


def _download_pdf(
    url: str,
    destination: Path,
    *,
    max_bytes: int,
    timeout: float,
    open_url: OpenUrl,
) -> tuple[str, int]:
    partial = destination.with_suffix(destination.suffix + ".part")
    digest = hashlib.sha256()
    size = 0
    try:
        with open_url(url, timeout) as response:
            if response.status != 200 or response.content_type != "application/pdf":
                raise CameraReadyError(
                    f"Invalid PDF response: status={response.status}, "
                    f"content_type={response.content_type}"
                )
            if response.content_length is not None and response.content_length > max_bytes:
                raise CameraReadyError("PDF exceeds configured size limit")
            with partial.open("xb") as handle:
                while True:
                    chunk = response.stream.read(1024 * 1024)
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > max_bytes:
                        raise CameraReadyError("PDF exceeds configured size limit")
                    digest.update(chunk)
                    handle.write(chunk)
                handle.flush()
                os.fsync(handle.fileno())
            if response.content_length is not None and size != response.content_length:
                raise CameraReadyError("PDF length differs from Content-Length")
        with partial.open("rb") as handle:
            signature = handle.read(5)
        if size < 5 or signature != b"%PDF-":
            raise CameraReadyError("Downloaded payload has no PDF signature")
        os.chmod(partial, stat.S_IRUSR | stat.S_IWUSR)
        os.replace(partial, destination)
        return digest.hexdigest(), size
    except CameraReadyError:
        partial.unlink(missing_ok=True)
        raise
    except Exception as error:
        partial.unlink(missing_ok=True)
        raise CameraReadyError(f"Failed to download {url}: {error}") from error


def _validate_pdf(path: Path) -> tuple[int, bool]:
    try:
        with pymupdf.open(path) as document:
            page_count = document.page_count
            if page_count < 1:
                raise CameraReadyError("Downloaded PDF has no pages")
            first_page = " ".join(document[0].get_text("text").casefold().split())
    except CameraReadyError:
        raise
    except Exception as error:
        raise CameraReadyError(f"Cannot parse downloaded PDF: {error}") from error
    marker_found = CAMERA_READY_MARKER in first_page
    if not marker_found:
        raise CameraReadyError("First page lacks the ICLR 2026 conference-paper marker")
    return page_count, marker_found


def _single_metadata_value(
    metadata: Mapping[str, list[str]], name: str, *, expected: str | None = None
) -> str:
    values = metadata.get(name, [])
    if len(values) != 1:
        raise CameraReadyError(f"Expected one {name} metadata value")
    value = values[0]
    if expected is not None and value != expected:
        raise CameraReadyError(f"Unexpected {name}: {value}")
    return value


def _validate_abstract_metadata(
    payload: bytes, match: Match
) -> dict[str, Any]:
    metadata = parse_citation_metadata(payload)
    proceedings = match.proceedings_paper
    citation_title = _single_metadata_value(metadata, "citation_title")
    if _normalize_text(citation_title) != _normalize_text(proceedings.title):
        raise CameraReadyError("Abstract page citation title differs from the index")
    citation_pdf_url = _single_metadata_value(
        metadata, "citation_pdf_url", expected=proceedings.pdf_url
    )
    journal = _single_metadata_value(
        metadata,
        "citation_journal_title",
        expected="International Conference on Learning Representations",
    )
    volume = _single_metadata_value(metadata, "citation_volume", expected="2026")
    publication_date = _single_metadata_value(
        metadata, "citation_publication_date"
    )
    citation_authors = metadata.get("citation_author", [])
    if not citation_authors:
        raise CameraReadyError("Abstract page has no citation authors")
    return {
        "citation_title": citation_title,
        "citation_authors": citation_authors,
        "citation_journal_title": journal,
        "citation_volume": volume,
        "citation_publication_date": publication_date,
        "citation_pdf_url": citation_pdf_url,
    }


def _write_json_private(path: Path, value: Mapping[str, Any]) -> None:
    payload = (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode(
        "utf-8"
    )
    with path.open("xb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)


def fetch_camera_ready(
    mapping_path: Path,
    output_dir: Path,
    *,
    download: bool = False,
    timeout: float = 60.0,
    max_pdf_bytes: int = MAX_PDF_BYTES,
    open_url: OpenUrl = _default_open_url,
    expected_accepts: int = EXPECTED_ACCEPTS,
    expected_rejects: int = EXPECTED_REJECTS,
) -> dict[str, Any]:
    mapping, accepts = _load_private_mapping(
        mapping_path,
        expected_accepts=expected_accepts,
        expected_rejects=expected_rejects,
    )
    index_payload = _fetch_bytes(
        PROCEEDINGS_INDEX_URL,
        expected_type="text/html",
        max_bytes=MAX_INDEX_BYTES,
        timeout=timeout,
        open_url=open_url,
    )
    proceedings = parse_proceedings_index(index_payload)
    matches = match_accepts(accepts, proceedings)
    if len(matches) != expected_accepts:
        raise CameraReadyError("Not every accepted paper received a proceedings match")
    match_counts: dict[str, int] = {}
    for value in matches:
        match_counts[value.match_mode] = match_counts.get(value.match_mode, 0) + 1

    summary = {
        "accept_count": len(matches),
        "reject_count": expected_rejects,
        "proceedings_index_paper_count": len(proceedings),
        "proceedings_index_sha256": _sha256_bytes(index_payload),
        "match_counts": match_counts,
        "downloaded": False,
    }
    if not download:
        return summary

    destination = output_dir.expanduser()
    if destination.exists() or destination.is_symlink():
        raise CameraReadyError("Output directory must be new and must not be a symlink")
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=f".{destination.name}.staging-", dir=destination.parent)
    )
    os.chmod(staging, stat.S_IRWXU)
    try:
        pdf_dir = staging / "pdfs"
        pdf_dir.mkdir(mode=stat.S_IRWXU)
        index_path = staging / "proceedings_index.html"
        with index_path.open("xb") as handle:
            handle.write(index_payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(index_path, stat.S_IRUSR | stat.S_IWUSR)

        records: list[dict[str, Any]] = []
        total_pdf_bytes = 0
        for match in sorted(matches, key=lambda value: value.private_paper["blind_id"]):
            private = match.private_paper
            proceedings_paper = match.proceedings_paper
            abstract_payload = _fetch_bytes(
                proceedings_paper.abstract_url,
                expected_type="text/html",
                max_bytes=MAX_ABSTRACT_BYTES,
                timeout=timeout,
                open_url=open_url,
            )
            citation = _validate_abstract_metadata(abstract_payload, match)
            pdf_path = pdf_dir / f"{private['blind_id']}.pdf"
            pdf_sha256, pdf_bytes = _download_pdf(
                proceedings_paper.pdf_url,
                pdf_path,
                max_bytes=max_pdf_bytes,
                timeout=timeout,
                open_url=open_url,
            )
            page_count, marker_found = _validate_pdf(pdf_path)
            total_pdf_bytes += pdf_bytes
            records.append(
                {
                    "blind_id": private["blind_id"],
                    "openreview_paper_id": private["paper_id"],
                    "source_kind": "official_iclr2026_proceedings_camera_ready",
                    "match_mode": match.match_mode,
                    "title_similarity": match.title_similarity,
                    "author_similarity": match.author_similarity,
                    "initial_title": private["title"],
                    "initial_authors": private["authors"],
                    "proceedings_hash": proceedings_paper.proceedings_hash,
                    "abstract_url": proceedings_paper.abstract_url,
                    "abstract_sha256": _sha256_bytes(abstract_payload),
                    **citation,
                    "pdf_file": f"pdfs/{private['blind_id']}.pdf",
                    "pdf_sha256": pdf_sha256,
                    "pdf_bytes": pdf_bytes,
                    "pdf_page_count": page_count,
                    "first_page_conference_marker": marker_found,
                }
            )

        mapping_source = mapping_path.expanduser().resolve()
        manifest = {
            "format_version": "iclr2026-camera-ready-provenance-v1",
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "private_label_aware_preparation": True,
            "source_mapping": str(mapping_source),
            "source_mapping_sha256": _sha256_file(mapping_source),
            "source_parquet_sha256": mapping.get("source_parquet_sha256"),
            "proceedings_index_url": PROCEEDINGS_INDEX_URL,
            "proceedings_index_file": "proceedings_index.html",
            "proceedings_index_sha256": _sha256_bytes(index_payload),
            "proceedings_index_paper_count": len(proceedings),
            "expected_accept_count": expected_accepts,
            "expected_reject_count": expected_rejects,
            "match_counts": match_counts,
            "downloaded_pdf_count": len(records),
            "downloaded_pdf_bytes": total_pdf_bytes,
            "camera_ready_definition": (
                "Official ICLR 2026 published conference paper from proceedings.iclr.cc"
            ),
            "papers": records,
        }
        manifest_path = staging / "provenance_manifest.json"
        _write_json_private(manifest_path, manifest)
        summary.update(
            {
                "downloaded": True,
                "output_dir": str(destination.resolve()),
                "downloaded_pdf_count": len(records),
                "downloaded_pdf_bytes": total_pdf_bytes,
                "provenance_manifest_sha256": _sha256_file(manifest_path),
            }
        )
        # Publishing is a single atomic rename and the final fallible operation.
        # Any earlier failure removes the staging tree, so no partial formal
        # camera-ready dataset can appear at the requested destination.
        os.replace(staging, destination)
        return summary
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Match accepted papers to the official ICLR 2026 proceedings and "
            "optionally fetch camera-ready PDFs into a new private directory."
        )
    )
    parser.add_argument("private_mapping", type=Path)
    parser.add_argument("output_dir", type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="validate the mapping and official index without writing output (default)",
    )
    mode.add_argument(
        "--download",
        action="store_true",
        help="download, validate, and atomically publish all accepted-paper PDFs",
    )
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--max-pdf-bytes", type=int, default=MAX_PDF_BYTES)
    args = parser.parse_args()
    try:
        summary = fetch_camera_ready(
            args.private_mapping,
            args.output_dir,
            download=args.download,
            timeout=args.timeout,
            max_pdf_bytes=args.max_pdf_bytes,
        )
    except CameraReadyError as error:
        parser.exit(1, f"camera-ready fetch failed: {error}\n")
    print(json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
