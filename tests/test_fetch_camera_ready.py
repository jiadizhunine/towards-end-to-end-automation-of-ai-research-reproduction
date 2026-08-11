import hashlib
import importlib.util
import io
import json
import stat
import sys
from pathlib import Path

import pymupdf
import pytest

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "fetch_camera_ready.py"
SPEC = importlib.util.spec_from_file_location("fetch_camera_ready", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
fetch_module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = fetch_module
SPEC.loader.exec_module(fetch_module)

from fetch_camera_ready import (  # noqa: E402
    CAMERA_READY_MARKER,
    PROCEEDINGS_INDEX_URL,
    CameraReadyError,
    FetchResponse,
    ProceedingsPaper,
    fetch_camera_ready,
    match_accepts,
    parse_proceedings_index,
)


def proceedings_index(records):
    rows = []
    for title, authors, digest in records:
        rows.append(
            '<li class="conference"><div class="paper-content">'
            f'<a title="paper title" href="/paper_files/paper/2026/hash/{digest}'
            f'-Abstract-Conference.html">{title}</a>'
            f'<span class="paper-authors">{", ".join(authors)}</span>'
            "</div></li>"
        )
    return ("<html><body>" + "".join(rows) + "</body></html>").encode()


def abstract_page(title, authors, digest):
    author_meta = "".join(
        f'<meta name="citation_author" content="{author}">' for author in authors
    )
    pdf_url = (
        "https://proceedings.iclr.cc/paper_files/paper/2026/file/"
        f"{digest}-Paper-Conference.pdf"
    )
    return (
        "<html><head>"
        f'<meta name="citation_title" content="{title}">'
        f"{author_meta}"
        '<meta name="citation_journal_title" '
        'content="International Conference on Learning Representations">'
        '<meta name="citation_volume" content="2026">'
        '<meta name="citation_publication_date" content="2026-04-20">'
        f'<meta name="citation_pdf_url" content="{pdf_url}">'
        "</head></html>"
    ).encode()


def make_pdf(*, valid_marker=True):
    document = pymupdf.open()
    page = document.new_page()
    text = (
        "Published as a conference paper at ICLR 2026"
        if valid_marker
        else "Draft manuscript"
    )
    page.insert_text((72, 72), text)
    payload = document.tobytes()
    document.close()
    return payload


def write_mapping(path: Path):
    mapping = {
        "source_parquet_sha256": "a" * 64,
        "papers": [
            {
                "blind_id": "B001",
                "paper_id": "OpenReviewA",
                "ground_truth": "Accept",
                "title": "Exact Camera Paper",
                "authors": ["Alice Example", "Bob Person"],
            },
            {
                "blind_id": "B002",
                "paper_id": "OpenReviewR",
                "ground_truth": "Reject",
                "title": "Rejected Paper",
                "authors": ["Reject Author"],
            },
            {
                "blind_id": "B003",
                "paper_id": "OpenReviewB",
                "ground_truth": "Accept",
                "title": "Short Initial Title",
                "authors": ["Carol Researcher", "Deyu Chen"],
            },
        ],
    }
    path.write_text(json.dumps(mapping), encoding="utf-8")
    return mapping


class FakeNetwork:
    def __init__(self, payloads):
        self.payloads = payloads
        self.requested = []

    def __call__(self, url, timeout):
        del timeout
        self.requested.append(url)
        try:
            content_type, payload = self.payloads[url]
        except KeyError as error:
            raise AssertionError(f"Unexpected URL: {url}") from error
        return FetchResponse(
            stream=io.BytesIO(payload),
            status=200,
            content_type=content_type,
            content_length=len(payload),
        )


def fixture_network(*, second_pdf_marker=True):
    digest_a = "1" * 32
    digest_b = "2" * 32
    title_a = "Exact Camera Paper"
    title_b = "Short Initial Title v2"
    authors_a = ["Alice Example", "Bob Person"]
    authors_b = ["Carol Researcher", "Deyu Chen"]
    index = proceedings_index(
        [
            (title_a, authors_a, digest_a),
            (title_b, authors_b, digest_b),
        ]
    )
    base = "https://proceedings.iclr.cc/paper_files/paper/2026"
    payloads = {
        PROCEEDINGS_INDEX_URL: ("text/html", index),
        f"{base}/hash/{digest_a}-Abstract-Conference.html": (
            "text/html",
            abstract_page(title_a, ["Example, Alice", "Person, Bob"], digest_a),
        ),
        f"{base}/hash/{digest_b}-Abstract-Conference.html": (
            "text/html",
            abstract_page(title_b, ["Researcher, Carol", "Chen, Deyu"], digest_b),
        ),
        f"{base}/file/{digest_a}-Paper-Conference.pdf": (
            "application/pdf",
            make_pdf(),
        ),
        f"{base}/file/{digest_b}-Paper-Conference.pdf": (
            "application/pdf",
            make_pdf(valid_marker=second_pdf_marker),
        ),
    }
    return FakeNetwork(payloads)


def test_parse_and_match_exact_plus_camera_ready_title_change():
    digest_a = "1" * 32
    digest_b = "2" * 32
    payload = proceedings_index(
        [
            ("Exact Camera Paper", ["Alice Example", "Bob Person"], digest_a),
            (
                "Short Initial Title v2",
                ["Carol Researcher", "Deyu Chen"],
                digest_b,
            ),
        ]
    )
    proceedings = parse_proceedings_index(payload)
    accepts = [
        {
            "blind_id": "B001",
            "title": "Exact Camera Paper",
            "authors": ["Alice Example", "Bob Person"],
        },
        {
            "blind_id": "B003",
            "title": "Short Initial Title",
            "authors": ["Carol Researcher", "Deyu Chen"],
        },
    ]
    matches = match_accepts(accepts, proceedings)
    assert [match.match_mode for match in matches] == [
        "title_exact",
        "title_changed_author_match",
    ]
    assert matches[1].title_similarity >= 0.80
    assert matches[1].author_similarity >= 0.90


def test_match_fails_closed_on_ambiguous_changed_title():
    private = {
        "blind_id": "B001",
        "title": "A Shared Initial Title",
        "authors": ["Alice Example"],
    }
    proceedings = [
        ProceedingsPaper(
            title=f"A Shared Initial Title Camera Version {suffix}",
            authors=("Alice Example",),
            abstract_path=f"/paper_files/paper/2026/hash/{suffix * 32}-Abstract-Conference.html",
            proceedings_hash=suffix * 32,
        )
        for suffix in ("1", "2")
    ]
    with pytest.raises(CameraReadyError, match="Expected one title-change match"):
        match_accepts([private], proceedings)


def test_exact_title_still_requires_matching_authors():
    private = {
        "blind_id": "B001",
        "title": "Exact Shared Title",
        "authors": ["Alice Example"],
    }
    proceedings = [
        ProceedingsPaper(
            title="Exact Shared Title",
            authors=("Completely Different",),
            abstract_path=(
                "/paper_files/paper/2026/hash/"
                + "1" * 32
                + "-Abstract-Conference.html"
            ),
            proceedings_hash="1" * 32,
        )
    ]
    with pytest.raises(CameraReadyError, match="author mismatch"):
        match_accepts([private], proceedings)


def test_dry_run_only_fetches_index_and_writes_nothing(tmp_path):
    mapping_path = tmp_path / "mapping.json"
    write_mapping(mapping_path)
    output = tmp_path / "camera-ready"
    network = fixture_network()

    result = fetch_camera_ready(
        mapping_path,
        output,
        download=False,
        open_url=network,
        expected_accepts=2,
        expected_rejects=1,
    )

    assert result["match_counts"] == {
        "title_exact": 1,
        "title_changed_author_match": 1,
    }
    assert network.requested == [PROCEEDINGS_INDEX_URL]
    assert not output.exists()


def test_download_validates_and_atomically_publishes_private_artifacts(tmp_path):
    mapping_path = tmp_path / "mapping.json"
    mapping = write_mapping(mapping_path)
    output = tmp_path / "camera-ready"
    network = fixture_network()

    result = fetch_camera_ready(
        mapping_path,
        output,
        download=True,
        open_url=network,
        expected_accepts=2,
        expected_rejects=1,
    )

    assert result["downloaded"] is True
    assert result["downloaded_pdf_count"] == 2
    assert stat.S_IMODE(output.stat().st_mode) == 0o700
    manifest_path = output / "provenance_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["format_version"] == "iclr2026-camera-ready-provenance-v1"
    assert manifest["source_mapping_sha256"] == hashlib.sha256(
        mapping_path.read_bytes()
    ).hexdigest()
    assert manifest["source_parquet_sha256"] == mapping["source_parquet_sha256"]
    assert manifest["downloaded_pdf_count"] == 2
    assert len(manifest["papers"]) == 2
    for record in manifest["papers"]:
        assert record["source_kind"] == (
            "official_iclr2026_proceedings_camera_ready"
        )
        pdf = output / record["pdf_file"]
        assert pdf.is_file()
        assert stat.S_IMODE(pdf.stat().st_mode) == 0o600
        assert record["pdf_sha256"] == hashlib.sha256(pdf.read_bytes()).hexdigest()
        assert record["pdf_page_count"] == 1
        assert record["first_page_conference_marker"] is True
        assert record["citation_volume"] == "2026"
        assert record["citation_publication_date"] == "2026-04-20"
    assert not list(tmp_path.glob(".camera-ready.staging-*"))


def test_failure_leaves_no_published_or_staging_directory(tmp_path):
    mapping_path = tmp_path / "mapping.json"
    write_mapping(mapping_path)
    output = tmp_path / "camera-ready"
    network = fixture_network(second_pdf_marker=False)

    with pytest.raises(CameraReadyError, match="conference-paper marker"):
        fetch_camera_ready(
            mapping_path,
            output,
            download=True,
            open_url=network,
            expected_accepts=2,
            expected_rejects=1,
        )

    assert not output.exists()
    assert not list(tmp_path.glob(".camera-ready.staging-*"))
