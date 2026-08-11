import hashlib
import json
import stat
import threading
from pathlib import Path
from types import SimpleNamespace

import pytest

from deepseek_autoreviewer import benchmark_cli
from deepseek_autoreviewer.core import ReviewerConfig
from deepseek_autoreviewer.nature_protocol import NATURE_PROTOCOL_ID


def make_review(overall=7, decision="Accept"):
    return {
        "Summary": "The paper studies a concrete machine-learning problem.",
        "Strengths": ["The experimental protocol is clearly specified."],
        "Weaknesses": ["External validity remains limited."],
        "Originality": 3,
        "Quality": 3,
        "Clarity": 3,
        "Significance": 3,
        "Questions": ["How stable are the results across seeds?"],
        "Limitations": ["Only one benchmark family is studied."],
        "Ethical Concerns": False,
        "Soundness": 3,
        "Presentation": 3,
        "Contribution": 3,
        "Overall": overall,
        "Confidence": 4,
        "Decision": decision,
    }


class FakeCompletions:
    def __init__(self):
        self.calls = []
        self.lock = threading.Lock()

    def create(self, **kwargs):
        with self.lock:
            index = len(self.calls)
            self.calls.append(kwargs)
        return SimpleNamespace(
            id=f"fake-{index}",
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content=json.dumps(make_review()))
                )
            ],
            usage={
                "prompt_tokens": 100,
                "prompt_cache_hit_tokens": 0,
                "prompt_cache_miss_tokens": 100,
                "completion_tokens": 50,
                "total_tokens": 150,
            },
        )


class FakeClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=FakeCompletions())
        self.closed = 0

    def close(self):
        self.closed += 1


def make_blind_tree(tmp_path: Path, count: int = 3):
    blind = tmp_path / "blind"
    blind.mkdir(mode=0o700)
    papers = []
    hashes = {}
    for index in range(1, count + 1):
        blind_id = f"B{index:03d}"
        filename = f"{blind_id}.txt"
        text = (f"Blinded scientific manuscript {index}. " * 80).strip() + "\n"
        path = blind / filename
        path.write_text(text, encoding="utf-8")
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        hashes[blind_id] = digest
        papers.append(
            {
                "blind_id": blind_id,
                "filename": filename,
                "blind_text_sha256": digest,
            }
        )
    manifest = {
        "paper_count": count,
        "contains_ground_truth": False,
        "contains_source_identifiers": False,
        "papers": papers,
    }
    (blind / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return blind, hashes


def test_run_is_resumable_max_papers_and_freeze_evaluate_are_separate(
    tmp_path: Path, monkeypatch, capsys
):
    blind, hashes = make_blind_tree(tmp_path)
    run_output = tmp_path / "run"
    frozen = tmp_path / "frozen" / "predictions.json"
    evaluation_path = tmp_path / "evaluation" / "metrics.json"
    private_mapping = tmp_path / "private-mapping.json"
    private_mapping.write_text(
        json.dumps(
            {
                "papers": [
                    {
                        "blind_id": "B001",
                        "blind_text_sha256": hashes["B001"],
                        "ground_truth": "Accept",
                    },
                    {
                        "blind_id": "B002",
                        "blind_text_sha256": hashes["B002"],
                        "ground_truth": "Reject",
                    },
                    {
                        "blind_id": "B003",
                        "blind_text_sha256": hashes["B003"],
                        "ground_truth": "Reject",
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    client = FakeClient()
    monkeypatch.setenv("DEEPSEEK_API_KEY", "unit-test-key")
    monkeypatch.setattr(
        benchmark_cli, "create_deepseek_client", lambda **kwargs: client
    )

    assert (
        benchmark_cli.main(
            [
                "run",
                str(blind),
                str(run_output),
                "--max-papers",
                "2",
                "--paper-jobs",
                "2",
            ]
        )
        == 0
    )
    assert len(client.chat.completions.calls) == 12  # 2 papers x (5 reviewers + meta)
    assert sorted(path.parent.name for path in (run_output / "bundles").glob("*/review_bundle.json")) == [
        "B001",
        "B002",
    ]
    run_manifest = json.loads((run_output / "run_manifest.json").read_text())
    assert run_manifest["contains_ground_truth"] is False
    assert run_manifest["smoke_test_limited"] is True
    assert run_manifest["paper_count"] == 2

    # A second invocation validates and reuses complete hash-bound bundles.
    assert (
        benchmark_cli.main(
            ["run", str(blind), str(run_output), "--max-papers", "2"]
        )
        == 0
    )
    assert len(client.chat.completions.calls) == 12
    assert json.loads((run_output / "run_manifest.json").read_text())["resumed_count"] == 2

    # The default full-run gate is 40, and a smoke freeze must opt into two.
    assert benchmark_cli.main(["freeze", str(run_output), str(frozen)]) == 1
    assert not frozen.exists()
    assert (
        benchmark_cli.main(
            [
                "freeze",
                str(run_output),
                str(frozen),
                "--expected-count",
                "2",
            ]
        )
        == 0
    )
    frozen_payload = json.loads(frozen.read_text())
    assert frozen_payload["contains_ground_truth"] is False
    assert frozen_payload["paper_count"] == 2
    assert all("ground_truth" not in paper for paper in frozen_payload["papers"])
    assert (frozen.parent / "predictions.json.sha256").is_file()

    assert (
        benchmark_cli.main(
            [
                "evaluate",
                str(frozen),
                str(private_mapping),
                str(evaluation_path),
                "--expected-count",
                "2",
                "--bootstrap-samples",
                "20",
                "--bootstrap-seed",
                "7",
            ]
        )
        == 0
    )
    evaluation = json.loads(evaluation_path.read_text())
    assert evaluation["n_papers"] == 2
    assert evaluation["metrics"]["accuracy"] == 0.5
    assert len(evaluation["audit"]["frozen_predictions_sha256"]) == 64
    assert evaluation["audit"]["source_input_disclosures"] == {
        "contains_source_identifiers": False
    }
    assert evaluation["audit"]["protocol_fingerprint_sha256"] is None

    for directory in (
        run_output,
        run_output / "bundles",
        run_output / "bundles" / "B001",
        frozen.parent,
        evaluation_path.parent,
    ):
        assert stat.S_IMODE(directory.stat().st_mode) == 0o700
    for file_path in (
        run_output / "run_manifest.json",
        run_output / "bundles" / "B001" / "review_bundle.json",
        run_output / "bundles" / "B001" / "review.md",
        frozen,
        frozen.parent / "predictions.json.sha256",
        evaluation_path,
    ):
        assert stat.S_IMODE(file_path.stat().st_mode) == 0o600

    output = capsys.readouterr()
    assert "unit-test-key" not in output.out + output.err


def test_manifest_hash_is_checked_before_review(tmp_path: Path):
    blind, _ = make_blind_tree(tmp_path, count=1)
    (blind / "B001.txt").write_text("tampered" * 200, encoding="utf-8")
    client = FakeClient()

    with pytest.raises(benchmark_cli.BenchmarkCLIError, match="hash mismatch"):
        benchmark_cli.run_blind_benchmark(
            blind,
            tmp_path / "run",
            client=client,
            max_papers=1,
        )
    assert client.chat.completions.calls == []


def test_arbitrary_review_error_does_not_leak_secret(
    tmp_path: Path, monkeypatch, capsys
):
    blind, _ = make_blind_tree(tmp_path, count=1)
    secret = "deepseek-secret-must-not-appear"
    client = FakeClient()
    monkeypatch.setenv("DEEPSEEK_API_KEY", secret)
    monkeypatch.setattr(
        benchmark_cli, "create_deepseek_client", lambda **kwargs: client
    )

    def fail_review(*args, **kwargs):
        raise RuntimeError(f"upstream body contains {secret}")

    monkeypatch.setattr(benchmark_cli, "review_text", fail_review)
    assert (
        benchmark_cli.main(
            ["run", str(blind), str(tmp_path / "run"), "--max-papers", "1"]
        )
        == 1
    )
    captured = capsys.readouterr()
    assert secret not in captured.out + captured.err
    assert "RuntimeError" in captured.err


def test_frozen_hash_tampering_blocks_private_join(tmp_path: Path, monkeypatch):
    blind, hashes = make_blind_tree(tmp_path, count=2)
    run_output = tmp_path / "run"
    client = FakeClient()
    benchmark_cli.run_blind_benchmark(
        blind,
        run_output,
        client=client,
        max_papers=2,
    )
    frozen = tmp_path / "predictions.json"
    benchmark_cli.freeze_predictions(run_output, frozen, expected_count=2)
    frozen.write_bytes(frozen.read_bytes() + b" ")
    private_mapping = tmp_path / "mapping.json"
    private_mapping.write_text(
        json.dumps(
            {
                "papers": [
                    {
                        "blind_id": "B001",
                        "blind_text_sha256": hashes["B001"],
                        "ground_truth": "Accept",
                    },
                    {
                        "blind_id": "B002",
                        "blind_text_sha256": hashes["B002"],
                        "ground_truth": "Reject",
                    },
                ]
            }
        ),
        encoding="utf-8",
    )
    called = False

    def should_not_evaluate(*args, **kwargs):
        nonlocal called
        called = True

    monkeypatch.setattr(benchmark_cli, "evaluate_review_bundles", should_not_evaluate)
    with pytest.raises(benchmark_cli.BenchmarkCLIError, match="SHA-256"):
        benchmark_cli.evaluate_frozen_predictions(
            frozen,
            private_mapping,
            tmp_path / "metrics.json",
            expected_count=2,
        )
    assert called is False


def test_freeze_checks_run_manifest_bundle_hash(tmp_path: Path):
    blind, _ = make_blind_tree(tmp_path, count=1)
    run_output = tmp_path / "run"
    benchmark_cli.run_blind_benchmark(
        blind,
        run_output,
        client=FakeClient(),
        max_papers=1,
    )
    bundle_path = run_output / "bundles" / "B001" / "review_bundle.json"
    bundle = json.loads(bundle_path.read_text())
    bundle["final_review"]["Decision"] = "Reject"
    bundle_path.write_text(json.dumps(bundle), encoding="utf-8")

    with pytest.raises(benchmark_cli.BenchmarkCLIError, match="bundle hash"):
        benchmark_cli.freeze_predictions(
            run_output,
            tmp_path / "predictions.json",
            expected_count=1,
        )


def test_run_parser_has_no_private_mapping_input():
    parser = benchmark_cli.build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(
            ["run", "blind", "output", "--private-mapping", "labels.json"]
        )


def test_nature_protocol_manifest_resume_and_tamper_binding(tmp_path: Path):
    blind, _ = make_blind_tree(tmp_path, count=1)
    run_output = tmp_path / "nature-run"
    client = FakeClient()
    config = ReviewerConfig(
        protocol=NATURE_PROTOCOL_ID,
        aggregate_scores="mean",
        reasoning_effort="none",
        retry_base_seconds=0,
    )

    manifest = benchmark_cli.run_blind_benchmark(
        blind,
        run_output,
        client=client,
        config=config,
        max_papers=1,
    )
    assert len(client.chat.completions.calls) == 6
    protocol = manifest["protocol"]
    assert protocol["protocol_id"] == NATURE_PROTOCOL_ID
    assert protocol["effective_request"] == {
        "model": "deepseek-v4-flash",
        "max_tokens": 16384,
        "temperature": 0.75,
        "extra_body": {"thinking": {"type": "disabled"}},
        "omitted_fields": ["reasoning_effort", "response_format", "tools"],
    }
    bundle_path = run_output / "bundles" / "B001" / "review_bundle.json"
    bundle = json.loads(bundle_path.read_text())
    assert bundle["protocol"] == protocol

    resumed = benchmark_cli.run_blind_benchmark(
        blind,
        run_output,
        client=client,
        config=config,
        max_papers=1,
    )
    assert resumed["resumed_count"] == 1
    assert len(client.chat.completions.calls) == 6

    bundle["protocol"]["fingerprint_sha256"] = "0" * 64
    bundle_path.write_text(json.dumps(bundle), encoding="utf-8")
    with pytest.raises(benchmark_cli.BenchmarkCLIError, match="fingerprint"):
        benchmark_cli.run_blind_benchmark(
            blind,
            run_output,
            client=client,
            config=config,
            max_papers=1,
        )
    assert len(client.chat.completions.calls) == 6


def test_nature_protocol_changed_effective_request_blocks_resume(tmp_path: Path):
    blind, _ = make_blind_tree(tmp_path, count=1)
    run_output = tmp_path / "nature-run"
    client = FakeClient()
    config = ReviewerConfig(
        protocol=NATURE_PROTOCOL_ID,
        aggregate_scores="mean",
        reasoning_effort="none",
        retry_base_seconds=0,
    )
    benchmark_cli.run_blind_benchmark(
        blind,
        run_output,
        client=client,
        config=config,
        max_papers=1,
    )
    changed = ReviewerConfig(
        protocol=NATURE_PROTOCOL_ID,
        aggregate_scores="mean",
        reasoning_effort="none",
        max_output_tokens=8192,
        retry_base_seconds=0,
    )
    with pytest.raises(benchmark_cli.BenchmarkCLIError, match="protocol binding"):
        benchmark_cli.run_blind_benchmark(
            blind,
            run_output,
            client=client,
            config=changed,
            max_papers=1,
        )
    assert len(client.chat.completions.calls) == 6


def test_only_nature_protocol_allows_and_propagates_version_disclosures(
    tmp_path: Path,
):
    blind, _ = make_blind_tree(tmp_path, count=1)
    manifest_path = blind / "manifest.json"
    source_manifest = json.loads(manifest_path.read_text())
    source_manifest["contains_source_identifiers"] = True
    source_manifest["contains_version_label_clues"] = True
    source_manifest["contains_input_format_label_clues"] = True
    manifest_path.write_text(json.dumps(source_manifest), encoding="utf-8")

    legacy_client = FakeClient()
    with pytest.raises(benchmark_cli.BenchmarkCLIError, match="source identifiers"):
        benchmark_cli.run_blind_benchmark(
            blind,
            tmp_path / "legacy-run",
            client=legacy_client,
            max_papers=1,
        )
    assert legacy_client.chat.completions.calls == []

    nature_client = FakeClient()
    config = ReviewerConfig(
        protocol=NATURE_PROTOCOL_ID,
        aggregate_scores="mean",
        reasoning_effort="none",
        retry_base_seconds=0,
    )
    run_output = tmp_path / "nature-run"
    run_manifest = benchmark_cli.run_blind_benchmark(
        blind,
        run_output,
        client=nature_client,
        config=config,
        max_papers=1,
    )
    assert run_manifest["contains_source_identifiers"] is True
    assert run_manifest["contains_version_label_clues"] is True
    assert run_manifest["contains_input_format_label_clues"] is True

    frozen_path = tmp_path / "frozen.json"
    benchmark_cli.freeze_predictions(run_output, frozen_path, expected_count=1)
    frozen = json.loads(frozen_path.read_text())
    assert frozen["contains_source_identifiers"] is True
    assert frozen["contains_version_label_clues"] is True
    assert frozen["contains_input_format_label_clues"] is True
    assert frozen["protocol"] == run_manifest["protocol"]
    assert frozen["papers"][0]["final_decision"] == (
        json.loads(
            (run_output / "bundles" / "B001" / "review_bundle.json").read_text()
        )["meta_review_model"]["review"]["Decision"]
    )
