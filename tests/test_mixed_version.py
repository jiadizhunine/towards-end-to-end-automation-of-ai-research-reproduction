import hashlib
import json
import stat
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pymupdf
import pytest

from deepseek_autoreviewer.mixed_version import (
    CAMERA_PROVENANCE_FORMAT,
    FORMAT_VERSION,
    MixedVersionError,
    OFFICIAL_CAMERA_SOURCE_KIND,
    build_mixed_version_benchmark,
)


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _make_row(index: int, decision: str):
    paper_id = f"OpenReview{index:03d}"
    title = f"Identified Study {index}"
    authors = [f"Author Person {index}"]
    content = (
        f"# {title}\n\n{authors[0]}\n\n"
        f"Paper ID: {paper_id}\n\n"
        "Under review as a conference paper at ICLR 2026.\n\n"
        "This is the exact initial-submission markdown body.\n"
    )
    return {
        "paper_id": paper_id,
        "arxiv_id": f"2601.{index:05d}v1",
        "title": title,
        "markdown": {"content": content, "metadata": {"authors": authors}},
        "decision": {"decision": decision},
    }


def _write_pdf(path: Path, text: str) -> None:
    document = pymupdf.open()
    page = document.new_page()
    page.insert_textbox(
        pymupdf.Rect(50, 50, 550, 780),
        text,
        fontsize=10,
    )
    document.save(path)
    document.close()


def _make_inputs(tmp_path: Path):
    rows = [
        _make_row(1, "Accept (Poster)"),
        _make_row(2, "Reject"),
        _make_row(3, "Accept (Oral)"),
        _make_row(4, "Reject"),
    ]
    parquet_path = tmp_path / "source.parquet"
    pq.write_table(pa.Table.from_pylist(rows), parquet_path)
    parquet_hash = _sha256_bytes(parquet_path.read_bytes())

    labels = ["Accept", "Reject", "Accept", "Reject"]
    mapping_papers = []
    for index, (row, label) in enumerate(zip(rows, labels), start=1):
        raw = row["markdown"]["content"].encode()
        raw_hash = _sha256_bytes(raw)
        mapping_papers.append(
            {
                "blind_id": f"B{index:03d}",
                "paper_id": row["paper_id"],
                "arxiv_id": row["arxiv_id"],
                "title": row["title"],
                "authors": row["markdown"]["metadata"]["authors"],
                "source_decision": row["decision"]["decision"],
                "ground_truth": label,
                "selection_sha256": hashlib.sha256(
                    f"selection-{index}".encode()
                ).hexdigest(),
                "raw_text_sha256": raw_hash,
                "blind_text_sha256": hashlib.sha256(
                    f"old-blind-{index}".encode()
                ).hexdigest(),
            }
        )
    mapping = {
        "format_version": "proreviewer-iclr2026-v1",
        "source_parquet": str(parquet_path),
        "source_parquet_sha256": parquet_hash,
        "source_row_count": len(rows),
        "selection": {"seed_sha256": hashlib.sha256(b"seed").hexdigest()},
        "papers": mapping_papers,
    }
    mapping_path = tmp_path / "strict-mapping.json"
    mapping_path.write_text(json.dumps(mapping), encoding="utf-8")
    mapping_hash = _sha256_bytes(mapping_path.read_bytes())

    camera_root = tmp_path / "camera-private"
    pdf_root = camera_root / "pdfs"
    pdf_root.mkdir(parents=True)
    camera_papers = []
    for index in (1, 3):
        blind_id = f"B{index:03d}"
        pdf_path = pdf_root / f"{blind_id}.pdf"
        _write_pdf(
            pdf_path,
            (
                f"ICLR 2026 CAMERA READY PAPER {index}. "
                "This final publication contains source identifiers and final edits. "
            )
            * 8,
        )
        payload = pdf_path.read_bytes()
        camera_papers.append(
            {
                "blind_id": blind_id,
                "openreview_paper_id": rows[index - 1]["paper_id"],
                "source_kind": OFFICIAL_CAMERA_SOURCE_KIND,
                "match_mode": "openreview-id",
                "title_similarity": 1.0,
                "author_similarity": 1.0,
                "initial_title": rows[index - 1]["title"],
                "initial_authors": rows[index - 1]["markdown"]["metadata"]["authors"],
                "proceedings_hash": str(index) * 32,
                "abstract_url": f"https://proceedings.iclr.cc/paper/{index}",
                "abstract_sha256": hashlib.sha256(
                    f"abstract-{index}".encode()
                ).hexdigest(),
                "citation_title": rows[index - 1]["title"],
                "citation_authors": rows[index - 1]["markdown"]["metadata"]["authors"],
                "citation_journal_title": "International Conference on Learning Representations",
                "citation_volume": "2026",
                "citation_publication_date": "2026-04-20",
                "citation_pdf_url": f"https://proceedings.iclr.cc/paper_files/{index}.pdf",
                "pdf_file": f"pdfs/{blind_id}.pdf",
                "pdf_sha256": _sha256_bytes(payload),
                "pdf_bytes": len(payload),
                "pdf_page_count": 1,
                "first_page_conference_marker": True,
            }
        )
    provenance = {
        "format_version": CAMERA_PROVENANCE_FORMAT,
        "created_at_utc": "2026-08-11T00:00:00Z",
        "private_label_aware_preparation": True,
        "source_mapping": str(mapping_path),
        "source_mapping_sha256": mapping_hash,
        "source_parquet_sha256": parquet_hash,
        "proceedings_index_url": "https://proceedings.iclr.cc/",
        "proceedings_index_file": "index.html",
        "proceedings_index_sha256": hashlib.sha256(b"index").hexdigest(),
        "proceedings_index_paper_count": 2,
        "expected_accept_count": 2,
        "expected_reject_count": 2,
        "match_counts": {"openreview-id": 2},
        "downloaded_pdf_count": 2,
        "downloaded_pdf_bytes": sum(paper["pdf_bytes"] for paper in camera_papers),
        "camera_ready_definition": "official ICLR 2026 proceedings PDF",
        "papers": camera_papers,
    }
    provenance_path = camera_root / "provenance_manifest.json"
    provenance_path.write_text(json.dumps(provenance), encoding="utf-8")
    return rows, parquet_path, mapping_path, provenance_path


def _build(tmp_path: Path, output_name: str = "mixed"):
    rows, parquet_path, mapping_path, provenance_path = _make_inputs(tmp_path)
    output = tmp_path / output_name
    summary = build_mixed_version_benchmark(
        mapping_path,
        parquet_path,
        provenance_path,
        output,
        expected_accept_count=2,
        expected_reject_count=2,
        min_pdf_characters=40,
    )
    return rows, mapping_path, provenance_path, output, summary


def test_builds_label_isolated_mixed_versions_with_private_provenance(tmp_path: Path):
    rows, mapping_path, _, output, summary = _build(tmp_path)

    assert summary["paper_count"] == 4
    assert summary["selected_counts"] == {"Accept": 2, "Reject": 2}
    assert summary["contains_source_identifiers"] is True
    assert summary["contains_version_label_clues"] is True
    assert summary["contains_input_format_label_clues"] is True
    assert summary["contains_ground_truth"] is False

    manifest_path = output / "label_isolated" / "manifest.json"
    private_path = output / "private" / "mapping.json"
    manifest = json.loads(manifest_path.read_text())
    private = json.loads(private_path.read_text())
    assert manifest["format_version"] == FORMAT_VERSION
    assert manifest["contains_ground_truth"] is False
    assert manifest["contains_source_identifiers"] is True
    assert manifest["contains_version_label_clues"] is True
    assert manifest["contains_input_format_label_clues"] is True
    assert manifest["strictly_blinded"] is False
    assert [paper["blind_id"] for paper in manifest["papers"]] == [
        "B001",
        "B002",
        "B003",
        "B004",
    ]
    forbidden_entry_fields = {
        "ground_truth",
        "paper_id",
        "source_version",
        "source_decision",
        "official_provenance",
        "selection_sha256",
    }
    assert all(
        forbidden_entry_fields.isdisjoint(paper)
        for paper in manifest["papers"]
    )
    public_json = manifest_path.read_text()
    assert all(row["paper_id"] not in public_json for row in rows)
    assert all(row["title"] not in public_json for row in rows)

    accept_text = (output / "label_isolated" / "B001.txt").read_text()
    assert "ICLR 2026 CAMERA READY PAPER 1" in accept_text
    assert "exact initial-submission markdown" not in accept_text
    assert (output / "label_isolated" / "B002.txt").read_bytes() == rows[1][
        "markdown"
    ]["content"].encode()

    by_id = {paper["blind_id"]: paper for paper in private["papers"]}
    assert by_id["B001"]["source_version"] == "camera-ready"
    assert by_id["B001"]["source_pdf_sha256"] == by_id["B001"][
        "official_provenance"
    ]["pdf_sha256"]
    assert by_id["B002"]["source_version"] == "initial-submission"
    assert by_id["B002"]["input_text_sha256"] == by_id["B002"][
        "source_initial_markdown_sha256"
    ]
    assert private["version_label_policy"] == {
        "visibility": "private only",
        "Accept": "official ICLR 2026 camera-ready PDF",
        "Reject": "ProReviewer initial-submission raw markdown snapshot",
    }

    assert stat.S_IMODE(output.stat().st_mode) == 0o700
    assert all(
        stat.S_IMODE(path.stat().st_mode) == 0o700
        for path in output.rglob("*")
        if path.is_dir()
    )
    assert all(
        stat.S_IMODE(path.stat().st_mode) == 0o600
        for path in output.rglob("*")
        if path.is_file()
    )
    assert _sha256_bytes(mapping_path.read_bytes()) == summary[
        "strict_source_mapping_sha256"
    ]

    with pytest.raises(FileExistsError, match="Refusing to overwrite"):
        build_mixed_version_benchmark(
            mapping_path,
            tmp_path / "source.parquet",
            tmp_path / "camera-private" / "provenance_manifest.json",
            output,
            expected_accept_count=2,
            expected_reject_count=2,
            min_pdf_characters=40,
        )


def test_one_tampered_camera_pdf_causes_zero_publication(tmp_path: Path):
    _, parquet_path, mapping_path, provenance_path = _make_inputs(tmp_path)
    pdf_path = provenance_path.parent / "pdfs" / "B003.pdf"
    pdf_path.write_bytes(pdf_path.read_bytes() + b"tampered")
    output = tmp_path / "must-not-exist"

    with pytest.raises(MixedVersionError, match="size mismatch|hash mismatch"):
        build_mixed_version_benchmark(
            mapping_path,
            parquet_path,
            provenance_path,
            output,
            expected_accept_count=2,
            expected_reject_count=2,
            min_pdf_characters=40,
        )
    assert not output.exists()
    assert not list(tmp_path.glob(".must-not-exist.staging-*"))


def test_incomplete_or_wrongly_bound_camera_manifest_causes_zero_publication(
    tmp_path: Path,
):
    _, parquet_path, mapping_path, provenance_path = _make_inputs(tmp_path)
    provenance = json.loads(provenance_path.read_text())
    provenance["source_mapping_sha256"] = "0" * 64
    provenance_path.write_text(json.dumps(provenance), encoding="utf-8")
    output = tmp_path / "must-not-exist"

    with pytest.raises(MixedVersionError, match="mapping hash mismatch"):
        build_mixed_version_benchmark(
            mapping_path,
            parquet_path,
            provenance_path,
            output,
            expected_accept_count=2,
            expected_reject_count=2,
            min_pdf_characters=40,
        )
    assert not output.exists()


def test_reject_camera_entry_is_rejected_before_publication(tmp_path: Path):
    _, parquet_path, mapping_path, provenance_path = _make_inputs(tmp_path)
    provenance = json.loads(provenance_path.read_text())
    provenance["papers"][1]["blind_id"] = "B002"
    provenance["papers"][1]["openreview_paper_id"] = "OpenReview002"
    provenance_path.write_text(json.dumps(provenance), encoding="utf-8")
    output = tmp_path / "must-not-exist"

    with pytest.raises(MixedVersionError, match="unexpectedly includes rejected"):
        build_mixed_version_benchmark(
            mapping_path,
            parquet_path,
            provenance_path,
            output,
            expected_accept_count=2,
            expected_reject_count=2,
            min_pdf_characters=40,
        )
    assert not output.exists()


def test_final_atomic_rename_failure_leaves_no_output_or_staging(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    _, parquet_path, mapping_path, provenance_path = _make_inputs(tmp_path)
    output = tmp_path / "must-not-exist"
    original_rename = Path.rename

    def fail_publication(self: Path, target: Path):
        if self.name.startswith(".must-not-exist.staging-"):
            raise OSError("injected rename failure")
        return original_rename(self, target)

    monkeypatch.setattr(Path, "rename", fail_publication)
    with pytest.raises(OSError, match="injected rename failure"):
        build_mixed_version_benchmark(
            mapping_path,
            parquet_path,
            provenance_path,
            output,
            expected_accept_count=2,
            expected_reject_count=2,
            min_pdf_characters=40,
        )
    assert not output.exists()
    assert not list(tmp_path.glob(".must-not-exist.staging-*"))
