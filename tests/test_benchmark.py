import hashlib
import json
import stat
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest
import deepseek_autoreviewer.benchmark as benchmark_module

from deepseek_autoreviewer.benchmark import (
    ACCEPT_DECISIONS,
    BenchmarkError,
    blind_record,
    evaluate_metrics,
    evaluate_review_bundles,
    extend_benchmark,
    prepare_benchmark,
    scan_for_leaks,
    select_balanced_records,
)


def make_row(index: int, decision: str, *, leak_text: bool = False):
    title = f"Secret Study Number {index}"
    author = f"Researcher Person {index}"
    paper_id = f"PaperID{index:03d}"
    arxiv_id = f"2601.{index:05d}v1"
    content = (
        f"# {title}\n\n"
        f"{author}\n\n"
        "Under review as a conference paper at ICLR 2026\n\n"
        f"Paper ID: {paper_id}; arXiv: {arxiv_id}.\n\n"
        "## Abstract\n\nA method with experiments and sufficiently detailed scientific text.\n\n"
        "Code: https://github.com/example/private and DOI: 10.1234/secret.99. "
        "Discussion at OpenReview. Contact hidden@example.edu.\n\n"
        "## Acknowledgements\n\nWe thank a uniquely named colleague.\n\n"
        "## References\n\nA reference without identifying links.\n"
    )
    if leak_text:
        content += "www.example.org/final\n"
    return {
        "paper_id": paper_id,
        "arxiv_id": arxiv_id,
        "title": title,
        "markdown": {
            "content": content,
            "metadata": {
                "authors": [author],
                "title": title,
                "total_chars": len(content),
                "total_lines": len(content.splitlines()),
                "updated_at": "2026-01-01",
            },
        },
        "decision": {"decision": decision},
    }


def write_parquet(path: Path, rows):
    table = pa.Table.from_pylist(rows)
    pq.write_table(table, path)


def test_selection_exact_decisions_exclusions_and_stable_order():
    decisions = list(ACCEPT_DECISIONS)
    rows = [make_row(i, decisions[i % len(decisions)]) for i in range(25)]
    rows += [make_row(100 + i, "Reject") for i in range(25)]
    rows += [
        make_row(200, ""),
        make_row(201, "Withdrawn"),
        make_row(202, "Desk Reject"),
        make_row(203, "reject"),  # exact Reject only
    ]

    first, audit = select_balanced_records(rows, seed="published-seed", per_class=20)
    second, second_audit = select_balanced_records(
        list(reversed(rows)), seed="published-seed", per_class=20
    )
    assert [row["paper_id"] for row in first] == [row["paper_id"] for row in second]
    assert audit["seed"] == "published-seed"
    assert len(audit["seed_sha256"]) == 64
    assert audit["selected_counts"] == {"Accept": 20, "Reject": 20}
    assert audit["excluded_counts"] == {
        "desk_reject": 1,
        "empty_decision": 1,
        "other_decision": 1,
        "withdrawn": 1,
    }
    assert audit == second_audit


def test_blinding_nfkc_all_categories_sections_and_fail_closed_scan():
    row = make_row(7, "Accept (Poster)")
    # Full-width URL letters exercise NFKC-before-redaction.
    row["markdown"]["content"] += "ｈｔｔｐｓ://example.com/extra\n"
    blinded = blind_record(row)
    assert blinded.nfkc_changed is True
    assert scan_for_leaks(blinded.text, sensitive_values={
        "title": [row["title"]],
        "author": row["markdown"]["metadata"]["authors"],
        "paper_id": [row["paper_id"]],
        "arxiv_id": [row["arxiv_id"]],
    }) == {}
    lowered = blinded.text.casefold()
    for forbidden in (
        row["title"].casefold(),
        row["paper_id"].casefold(),
        "researcher person",
        "iclr",
        "openreview",
        "github",
        "acknowledg",
        "uniquely named colleague",
        "http",
        "10.1234/",
    ):
        assert forbidden not in lowered
    assert "## References" in blinded.text
    assert blinded.redaction_counts["sensitive_section"] == 1
    assert blinded.redaction_counts["url"] >= 2
    assert len(blinded.raw_text_sha256) == 64
    assert len(blinded.blind_text_sha256) == 64
    assert blinded.raw_text_sha256 != blinded.blind_text_sha256

    punctuation_variant = row.copy()
    punctuation_variant["markdown"] = dict(row["markdown"])
    punctuation_variant["markdown"]["content"] = (
        "# Secret—Study **Number** 7\n\n"
        "Researcher, Person 7\n\n"
        "A scientifically useful body remains after identifier removal. " * 20
        + "\nBare project host: models.example.org/demo. "
        + r"Repository: \url{https://code.example.dev/project}."
        + "\nhttps://PaperID007-blog.example.org/path\n"
        + "doi: 10.1234/PaperID007.secret\n"
        + "Refer to caption: figures_iclr/paper_rebuttal.png\n"
    )
    punctuation_blinded = blind_record(punctuation_variant)
    assert "secret" not in punctuation_blinded.text.casefold()
    assert "researcher" not in punctuation_blinded.text.casefold()
    assert "example.org" not in punctuation_blinded.text.casefold()
    assert "example.dev" not in punctuation_blinded.text.casefold()
    assert "https" not in punctuation_blinded.text.casefold()
    assert "doi:" not in punctuation_blinded.text.casefold()
    assert "figures_iclr" not in punctuation_blinded.text.casefold()
    assert scan_for_leaks(
        punctuation_blinded.text,
        sensitive_values={
            "title": [row["title"]],
            "author": row["markdown"]["metadata"]["authors"],
        },
    ) == {}

    ngram_variant = make_row(8, "Accept (Poster)")
    ngram_variant["title"] = "A Highly Identifying Six Token Study"
    ngram_variant["markdown"]["metadata"]["title"] = ngram_variant["title"]
    ngram_variant["markdown"]["content"] = (
        "# [TITLE REMOVED]\n\n"
        "The phrase Highly Identifying Six Token Study is repeated here.\n\n"
        + "Scientific methods and results remain reviewable. " * 30
    )
    ngram_blinded = blind_record(ngram_variant)
    assert "highly identifying six token study" not in ngram_blinded.text.casefold()

    raw_findings = scan_for_leaks(
        "ICLR 2026 https://openreview.net/forum?id=x GitHub doi:10.1234/abc "
        "arXiv:2601.12345 example.org"
    )
    assert {
        "conference_name",
        "url",
        "domain",
        "doi",
        "arxiv_id",
        "openreview",
        "github",
    }.issubset(raw_findings)


def test_leak_scan_requires_complete_canonical_token_boundaries():
    sensitive_values = {
        "title": [
            "Adversarial Attacks and Defenses on Graph-aware Large Language Models",
            "AMStraMGRAM : Adaptive Multi-cutoff Strategy Modification for ANaGRAM",
            "Towards Spatial Supersensing in Video",
        ],
        "author": ["Yue Yu"],
    }
    harmless_variants = (
        "Adversarial attacks and defenses on graphs. "
        "Adaptive Multicutoff Strategy Modification for ANaGRAM. "
        "We study spatial supersensing in videos. "
        "Xiang Yue, Yuansheng Ni, and Kai Zhang."
    )
    assert scan_for_leaks(
        harmless_variants, sensitive_values=sensitive_values
    ) == {}

    actual_leaks = scan_for_leaks(
        "Adversarial attacks and defenses on graph systems. Yue Yu.",
        sensitive_values=sensitive_values,
    )
    assert actual_leaks["title_high_coverage_ngram"] == 1
    assert actual_leaks["author_canonical"] == 1


def test_blinding_strips_identity_metadata_lifecycle_and_contribution_sections():
    row = make_row(9, "Reject")
    row["markdown"]["metadata"]["authors"] = ["Shiqi Zhang", "Alice Carter"]
    row["markdown"]["content"] = (
        "Title: [TITLE REMOVED]\n"
        "Authors: Shiqi Zhang, Alice Carter, Example University, "
        "{shiqi,alice}@example.edu\n"
        "Affiliations  ^1Tencent Youtu Lab ^2Fudan University\n"
        "(^1 Work done during an internship at Example Medical Inc.) "
        "(^2 Corresponding author: Alice Carter, Alice@intusurg.com)\n\n"
        "## Abstract\n\nA sufficiently detailed scientific method and result remains.\n\n"
        "A result before. Configurations will appear in the camera-ready version. "
        "Our code will be released upon paper acceptance. "
        "A result after.\n\n"
        "## Credits and Contributions\n\n"
        "#### Shiqi Zhang\n\n"
        "Initiated the project and held bi-weekly meetings with Shiqi.\n\n"
        "## References\n\nA non-identifying reference remains.\n"
    )

    blinded = blind_record(row)
    lowered = blinded.text.casefold()
    for forbidden in (
        "example university",
        "example medical",
        "tencent youtu",
        "fudan university",
        "intusurg",
        "camera-ready",
        "upon paper acceptance",
        "bi-weekly meetings",
        "shiqi",
        "alice",
        "@",
    ):
        assert forbidden not in lowered
    assert "## References" in blinded.text
    assert "A result before" in blinded.text
    assert "A result after" in blinded.text
    assert blinded.redaction_counts["identity_metadata_line"] == 2
    assert blinded.redaction_counts["identity_footnote_line"] == 1
    assert blinded.redaction_counts["decision_lifecycle_line"] == 2
    assert blinded.redaction_counts["sensitive_section"] == 1


def test_blinding_catches_grouped_and_partially_redacted_email_forms():
    row = make_row(10, "Reject")
    row["markdown"]["metadata"]["authors"] = ["Alice"]
    row["markdown"]["content"] = (
        "## Abstract\n\n"
        "Scientific methods and results remain reviewable. " * 20
        + "\nContact {alpha,beta}@example.com or Alice@intusurg.com. "
        + "Mirrors: ec.europa.eu and europarl.europa.eu.\n"
        + "Acknowledgement. Work supported by Example Foundation.\n"
    )

    blinded = blind_record(row)
    lowered = blinded.text.casefold()
    assert "@" not in blinded.text
    assert "example.com" not in lowered
    assert "intusurg.com" not in lowered
    assert "europa.eu" not in lowered
    assert "example foundation" not in lowered
    assert blinded.redaction_counts["email"] == 2
    assert blinded.redaction_counts["identity_acknowledgement_line"] == 1


def test_blinding_strips_numbered_acknowledgements_and_author_rosters():
    row = make_row(11, "Reject")
    row["markdown"]["metadata"]["authors"] = [
        "Ajmal Saeed Mian",
        "Huang Zhenqiang",
        "ChenghaoZhu",
        "WANG PIAOHONG",
    ]
    row["markdown"]["content"] = (
        "## Abstract\n\nA scientific body remains for review.\n\n"
        "Professor Ajmal Mian supervised the study.\n\n"
        "## 6 Acknowledgements\n\n"
        "This work was funded by Example University and Ajmal Mian.\n"
        "Council Discovery Early Career Researcher Award (project\n"
        "# DE230101058) funded by the Australian Government. "
        "This work is also supported by Google Research.\n\n"
        "## 7 Conclusion\n\nThe scientific conclusion remains.\n\n"
        "## 8 Contributions\n\n"
        "Core Contributors\n\nZhenqiang Huang\nChenghao Zhu\nPiaohong Wang\n\n"
        "Corresponding Authors\n\nProject Responsibilities\n\n"
        "## References\n\nA non-identifying reference remains.\n"
    )

    blinded = blind_record(row)
    lowered = blinded.text.casefold()
    for forbidden in (
        "ajmal mian",
        "example university",
        "australian government",
        "google research",
        "de230101058",
        "zhenqiang huang",
        "chenghao zhu",
        "piaohong wang",
        "project responsibilities",
    ):
        assert forbidden not in lowered
    assert "scientific conclusion remains" in lowered
    assert "## References" in blinded.text
    assert blinded.redaction_counts["sensitive_section"] == 2


def test_prepare_separates_mapping_and_enforces_private_permissions(tmp_path: Path):
    rows = [make_row(i, "Accept (Poster)") for i in range(22)]
    rows += [make_row(100 + i, "Reject") for i in range(22)]
    source = tmp_path / "proreviewer.parquet"
    write_parquet(source, rows)
    output = tmp_path / "benchmark"

    summary = prepare_benchmark(source, output, seed="iclr-2026-retro-v1", per_class=20)
    assert summary["paper_count"] == 40
    assert summary["leak_scan_passed"] is True
    assert stat.S_IMODE(output.stat().st_mode) == 0o700
    assert stat.S_IMODE((output / "blind").stat().st_mode) == 0o700
    assert stat.S_IMODE((output / "private").stat().st_mode) == 0o700

    all_files = [path for path in output.rglob("*") if path.is_file()]
    assert len([path for path in all_files if path.suffix == ".txt"]) == 40
    assert all(stat.S_IMODE(path.stat().st_mode) == 0o600 for path in all_files)

    blind_manifest = json.loads((output / "blind" / "manifest.json").read_text())
    private_mapping = json.loads((output / "private" / "mapping.json").read_text())
    assert blind_manifest["contains_ground_truth"] is False
    assert blind_manifest["contains_source_identifiers"] is False
    assert len(blind_manifest["papers"]) == 40
    assert private_mapping["selection"]["seed"] == "iclr-2026-retro-v1"
    assert {paper["ground_truth"] for paper in private_mapping["papers"]} == {
        "Accept",
        "Reject",
    }
    blind_serialized = (output / "blind" / "manifest.json").read_text()
    for private_paper in private_mapping["papers"]:
        assert private_paper["paper_id"] not in blind_serialized
        assert private_paper["title"] not in blind_serialized

    with pytest.raises(FileExistsError):
        prepare_benchmark(source, output, seed="iclr-2026-retro-v1", per_class=20)


def test_selection_rejects_short_classes_and_duplicate_ids():
    with pytest.raises(BenchmarkError, match="Not enough eligible"):
        select_balanced_records(
            [make_row(1, "Accept (Poster)"), make_row(2, "Reject")],
            seed="s",
            per_class=2,
        )
    duplicate = make_row(1, "Reject")
    with pytest.raises(BenchmarkError, match="Duplicate"):
        select_balanced_records(
            [make_row(1, "Accept (Poster)"), duplicate], seed="s", per_class=1
        )


def test_extend_preserves_prior_40_and_continues_rank_to_real_ratio(
    tmp_path: Path,
):
    rows = [make_row(i, "Accept (Poster)") for i in range(90)]
    rows += [make_row(1000 + i, "Reject") for i in range(140)]
    source = tmp_path / "proreviewer.parquet"
    write_parquet(source, rows)
    seed = "frozen-original-seed"
    prior = tmp_path / "prior"
    prepare_benchmark(source, prior, seed=seed, per_class=20)

    prior_mapping = json.loads((prior / "private" / "mapping.json").read_text())
    prior_manifest = json.loads((prior / "blind" / "manifest.json").read_text())
    prior_file_bytes = {
        f"B{index:03d}.txt": (prior / "blind" / f"B{index:03d}.txt").read_bytes()
        for index in range(1, 41)
    }
    output = tmp_path / "extended"
    summary = extend_benchmark(
        source,
        prior / "private" / "mapping.json",
        prior / "blind" / "manifest.json",
        prior / "blind",
        output,
        seed=seed,
        target_accept=78,
        target_reject=122,
    )

    assert summary["paper_count"] == 200
    assert summary["retained_paper_count"] == 40
    assert summary["added_paper_count"] == 160
    assert summary["selected_counts"] == {"Accept": 78, "Reject": 122}
    assert summary["added_counts"] == {"Accept": 58, "Reject": 102}
    assert summary["prior_blind_hashes_preserved"] is True

    extended_mapping = json.loads((output / "private" / "mapping.json").read_text())
    extended_manifest = json.loads((output / "blind" / "manifest.json").read_text())
    assert extended_mapping["papers"][:40] == prior_mapping["papers"]
    assert extended_manifest["papers"][:40] == prior_manifest["papers"]
    assert [paper["blind_id"] for paper in extended_mapping["papers"]] == [
        f"B{index:03d}" for index in range(1, 201)
    ]
    assert len({paper["paper_id"] for paper in extended_mapping["papers"]}) == 200
    assert {
        label: sum(
            paper["ground_truth"] == label for paper in extended_mapping["papers"]
        )
        for label in ("Accept", "Reject")
    } == {"Accept": 78, "Reject": 122}
    for filename, prior_bytes in prior_file_bytes.items():
        assert (output / "blind" / filename).read_bytes() == prior_bytes

    def selection_key(class_label, paper_id):
        value = f"{seed}\0{class_label}\0{paper_id}".encode()
        return hashlib.sha256(value).hexdigest(), paper_id

    prior_ids = {paper["paper_id"] for paper in prior_mapping["papers"]}
    expected_new = []
    for class_label, target in (("Accept", 78), ("Reject", 122)):
        class_rows = [
            row
            for row in rows
            if (class_label == "Accept")
            == (row["decision"]["decision"] in ACCEPT_DECISIONS)
        ]
        ranked = sorted(
            class_rows,
            key=lambda row: selection_key(class_label, row["paper_id"]),
        )
        assert {row["paper_id"] for row in ranked[:20]}.issubset(prior_ids)
        expected_new.extend(ranked[20:target])
    expected_new.sort(
        key=lambda row: (
            hashlib.sha256(
                f"{seed}\0extension-combined\0{row['paper_id']}".encode()
            ).hexdigest(),
            row["paper_id"],
        )
    )
    assert [paper["paper_id"] for paper in extended_mapping["papers"][40:]] == [
        row["paper_id"] for row in expected_new
    ]

    blind_serialized = (output / "blind" / "manifest.json").read_text()
    assert seed not in blind_serialized
    for field in ("ground_truth", "paper_id", "title", "authors", "source_decision"):
        assert all(field not in paper for paper in extended_manifest["papers"])
    assert extended_manifest["contains_ground_truth"] is False
    assert extended_manifest["contains_source_identifiers"] is False
    assert stat.S_IMODE(output.stat().st_mode) == 0o700
    assert all(
        stat.S_IMODE(path.stat().st_mode) == 0o600
        for path in output.rglob("*")
        if path.is_file()
    )


def test_extend_reblinds_retained_papers_when_redaction_policy_tightens(
    tmp_path: Path, monkeypatch,
):
    rows = [make_row(i, "Accept (Poster)") for i in range(22)]
    rows += [make_row(100 + i, "Reject") for i in range(22)]
    for row in rows:
        row["markdown"]["content"] += (
            "\nWe will publish artifacts in the camera-ready version.\n"
        )
    source = tmp_path / "source.parquet"
    write_parquet(source, rows)
    seed = "policy-revision-seed"
    prior = tmp_path / "prior"
    current_redactions = benchmark_module._GENERIC_REDACTIONS
    prior_redactions = tuple(
        item for item in current_redactions if item[0] != "decision_lifecycle_line"
    )
    monkeypatch.setattr(benchmark_module, "_GENERIC_REDACTIONS", prior_redactions)
    prepare_benchmark(source, prior, seed=seed, per_class=20)
    prior_hashes = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in (prior / "blind").glob("B*.txt")
    }
    monkeypatch.setattr(benchmark_module, "_GENERIC_REDACTIONS", current_redactions)

    output = tmp_path / "strict"
    summary = extend_benchmark(
        source,
        prior / "private" / "mapping.json",
        prior / "blind" / "manifest.json",
        prior / "blind",
        output,
        seed=seed,
        target_accept=20,
        target_reject=20,
    )

    assert summary["prior_blind_hashes_preserved"] is False
    assert summary["retained_blind_hash_changed_count"] == 40
    assert summary["retained_blind_hash_changed_ids"] == [
        f"B{index:03d}" for index in range(1, 41)
    ]
    assert all(
        hashlib.sha256((output / "blind" / filename).read_bytes()).hexdigest()
        != old_hash
        for filename, old_hash in prior_hashes.items()
    )
    strict_mapping = json.loads((output / "private" / "mapping.json").read_text())
    retained_redaction = strict_mapping["selection"]["retained_redaction"]
    assert retained_redaction["policy_revision"] == "strict-identity-v2"
    assert retained_redaction["changed_count"] == 40


def test_extend_fails_closed_on_seed_prior_hash_label_and_top20_mismatch(
    tmp_path: Path,
):
    rows = [make_row(i, "Accept (Poster)") for i in range(30)]
    rows += [make_row(100 + i, "Reject") for i in range(30)]
    source = tmp_path / "source.parquet"
    write_parquet(source, rows)
    seed = "frozen-seed"
    prior = tmp_path / "prior"
    prepare_benchmark(source, prior, seed=seed, per_class=20)
    arguments = (
        source,
        prior / "private" / "mapping.json",
        prior / "blind" / "manifest.json",
        prior / "blind",
    )

    with pytest.raises(BenchmarkError, match="match the frozen prior"):
        extend_benchmark(
            *arguments,
            tmp_path / "wrong-seed-output",
            seed="different-seed",
            target_accept=25,
            target_reject=25,
        )
    assert not (tmp_path / "wrong-seed-output").exists()

    blind_path = prior / "blind" / "B001.txt"
    original_bytes = blind_path.read_bytes()
    blind_path.write_bytes(original_bytes + b"tampered")
    with pytest.raises(BenchmarkError, match="blind file hash mismatch"):
        extend_benchmark(
            *arguments,
            tmp_path / "hash-output",
            seed=seed,
            target_accept=25,
            target_reject=25,
        )
    assert not (tmp_path / "hash-output").exists()
    blind_path.write_bytes(original_bytes)

    bad_mapping = json.loads((prior / "private" / "mapping.json").read_text())
    bad_mapping["papers"][0]["ground_truth"] = (
        "Reject" if bad_mapping["papers"][0]["ground_truth"] == "Accept" else "Accept"
    )
    bad_mapping_path = tmp_path / "bad-mapping.json"
    bad_mapping_path.write_text(json.dumps(bad_mapping))
    with pytest.raises(BenchmarkError, match="Ground-truth label mismatch"):
        extend_benchmark(
            source,
            bad_mapping_path,
            prior / "blind" / "manifest.json",
            prior / "blind",
            tmp_path / "label-output",
            seed=seed,
            target_accept=25,
            target_reject=25,
        )
    assert not (tmp_path / "label-output").exists()

    other_prior = tmp_path / "other-prior"
    prepare_benchmark(source, other_prior, seed="other-seed", per_class=20)
    not_top20 = json.loads((other_prior / "private" / "mapping.json").read_text())
    not_top20["selection"]["seed"] = seed
    not_top20["selection"]["seed_sha256"] = hashlib.sha256(seed.encode()).hexdigest()
    for paper in not_top20["papers"]:
        paper["selection_sha256"] = hashlib.sha256(
            f"{seed}\0{paper['ground_truth']}\0{paper['paper_id']}".encode()
        ).hexdigest()
    not_top20_path = tmp_path / "not-top20-mapping.json"
    not_top20_path.write_text(json.dumps(not_top20))
    with pytest.raises(BenchmarkError, match="not exactly the frozen top-20"):
        extend_benchmark(
            source,
            not_top20_path,
            other_prior / "blind" / "manifest.json",
            other_prior / "blind",
            tmp_path / "top20-output",
            seed=seed,
            target_accept=25,
            target_reject=25,
        )
    assert not (tmp_path / "top20-output").exists()


def test_metrics_exact_values_auroc_and_reproducible_stratified_bootstrap():
    # Truth A,A,R,R; final predictions A,R,A,R -> one of each confusion outcome.
    # Mean scores 9,7,6,2 rank every Accept above every Reject => AUROC 1.0.
    truth = ["Accept", "Accept", "Reject", "Reject"]
    scores = [[9] * 5, [7] * 5, [6] * 5, [2] * 5]
    predictions = ["Accept", "Reject", "Accept", "Reject"]
    first = evaluate_metrics(
        truth,
        scores,
        predicted_decisions=predictions,
        bootstrap_samples=200,
        bootstrap_seed=31415,
    )
    second = evaluate_metrics(
        truth,
        scores,
        predicted_decisions=predictions,
        bootstrap_samples=200,
        bootstrap_seed=31415,
    )
    assert first == second
    assert first["metrics"] == {
        "balanced_accuracy": 0.5,
        "accuracy": 0.5,
        "f1": 0.5,
        "auroc": 1.0,
        "fpr": 0.5,
        "fnr": 0.5,
    }
    assert first["confusion_matrix"] == {
        "labels": ["Reject", "Accept"],
        "matrix": [[1, 1], [1, 1]],
        "tn": 1,
        "fp": 1,
        "fn": 1,
        "tp": 1,
    }
    assert first["bootstrap"]["method"] == "stratified paper-level percentile bootstrap"
    assert first["bootstrap"]["seed"] == 31415


def test_metric_threshold_fallback_ties_and_bundle_shape():
    cases = []
    for truth, values in (
        ("Accept", [6, 6, 6, 6, 6]),
        ("Accept", [5, 5, 5, 5, 5]),
        ("Reject", [6, 6, 6, 6, 6]),
        ("Reject", [2, 2, 2, 2, 2]),
    ):
        cases.append(
            {
                "ground_truth": truth,
                "individual_reviews": [
                    {"review": {"Overall": score}} for score in values
                ],
            }
        )
    result = evaluate_review_bundles(cases, bootstrap_samples=50, bootstrap_seed=9)
    assert result["prediction_source"] == "five-review mean Overall >= 6"
    assert result["metrics"]["accuracy"] == 0.5
    # Positive scores [6,5], negative [6,2]: 3 wins / 4 with a half-tie = 0.625.
    assert result["metrics"]["auroc"] == 0.625

    with pytest.raises(BenchmarkError, match="exactly five"):
        evaluate_metrics(["Accept", "Reject"], [[7] * 4, [3] * 5], bootstrap_samples=2)
