"""Isolated command line workflow for the blinded ICLR benchmark.

The three stages are intentionally separate:

``run``
    Sees only a blind directory and writes resumable review bundles.
``freeze``
    Converts completed bundles into an immutable, label-free prediction file.
``evaluate``
    Verifies the frozen-file hash before joining predictions to private labels.

This separation is a guardrail, not a claim of kernel-level network isolation.
The review client itself enforces the official DeepSeek API endpoint.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from dotenv import load_dotenv

from .benchmark import evaluate_review_bundles
from .client import create_deepseek_client
from .core import (
    NUMERIC_RANGES,
    ReviewerConfig,
    get_protocol_record,
    review_text,
    write_outputs,
)
from .nature_protocol import (
    LEGACY_PROTOCOL_ID,
    NATURE_PROTOCOL_ID,
    validate_nature_protocol_record,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUN_FORMAT_VERSION = "deepseek-autoreviewer-blind-run-v1"
FREEZE_FORMAT_VERSION = "deepseek-autoreviewer-frozen-predictions-v1"
_BLIND_ID = re.compile(r"^B[0-9]{3,}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class BenchmarkCLIError(ValueError):
    """A controlled error whose message is safe to show to the user."""


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _secure_directory(path: Path) -> Path:
    requested = Path(path).expanduser()
    if requested.is_symlink():
        raise BenchmarkCLIError("Output directory must not be a symbolic link")
    resolved = requested.resolve()
    resolved.mkdir(parents=True, exist_ok=True, mode=0o700)
    if not resolved.is_dir() or resolved.is_symlink():
        raise BenchmarkCLIError("Output path must be a real directory")
    resolved.chmod(0o700)
    return resolved


def _atomic_secure_write(path: Path, payload: bytes, *, overwrite: bool) -> None:
    requested = Path(path).expanduser()
    if requested.is_symlink():
        raise BenchmarkCLIError("Output file must not be a symbolic link")
    destination = requested.resolve()
    parent = _secure_directory(destination.parent)
    if not overwrite and destination.exists():
        raise BenchmarkCLIError("Refusing to overwrite a frozen output artifact")
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.", dir=parent)
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
        destination.chmod(0o600)
    except Exception:
        try:
            os.close(descriptor)
        except OSError:
            pass
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def _read_json_object(path: Path, *, artifact: str) -> Dict[str, Any]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw)
    except Exception as exc:
        raise BenchmarkCLIError(f"Could not read a valid {artifact} JSON object") from None
    if not isinstance(value, dict):
        raise BenchmarkCLIError(f"{artifact} must be a JSON object")
    return value


def _safe_manifest_filename(root: Path, filename: Any) -> Path:
    if not isinstance(filename, str) or not filename or Path(filename).name != filename:
        raise BenchmarkCLIError("Blind manifest contains an unsafe filename")
    candidate = root / filename
    if candidate.is_symlink() or not candidate.is_file():
        raise BenchmarkCLIError("Blind manifest references a missing or linked manuscript")
    resolved = candidate.resolve()
    if resolved.parent != root:
        raise BenchmarkCLIError("Blind manifest filename escapes the blind directory")
    return resolved


def load_blind_manifest(
    blind_dir: Path,
    *,
    protocol: str = LEGACY_PROTOCOL_ID,
) -> Tuple[Path, List[Dict[str, Any]], str, Dict[str, bool]]:
    """Load a label-free manifest and verify every manuscript hash."""

    requested_root = Path(blind_dir).expanduser()
    if requested_root.is_symlink():
        raise BenchmarkCLIError("Blind directory is missing or is a symbolic link")
    root = requested_root.resolve()
    if not root.is_dir():
        raise BenchmarkCLIError("Blind directory is missing or is a symbolic link")
    manifest_path = root / "manifest.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise BenchmarkCLIError("Blind manifest is missing or is a symbolic link")
    manifest = _read_json_object(manifest_path, artifact="blind manifest")
    if manifest.get("contains_ground_truth") is not False:
        raise BenchmarkCLIError("Blind manifest does not explicitly exclude ground truth")
    contains_source_identifiers = manifest.get("contains_source_identifiers")
    if protocol == LEGACY_PROTOCOL_ID:
        if contains_source_identifiers is not False:
            raise BenchmarkCLIError(
                "Blind manifest does not explicitly exclude source identifiers"
            )
    elif protocol == NATURE_PROTOCOL_ID:
        if not isinstance(contains_source_identifiers, bool):
            raise BenchmarkCLIError(
                "Nature protocol input must declare contains_source_identifiers"
            )
    else:
        raise BenchmarkCLIError("Unsupported protocol for blind manifest loading")
    contains_version_label_clues = manifest.get("contains_version_label_clues")
    if contains_version_label_clues is not None and not isinstance(
        contains_version_label_clues, bool
    ):
        raise BenchmarkCLIError("Blind manifest has an invalid version-clue declaration")
    contains_input_format_label_clues = manifest.get(
        "contains_input_format_label_clues"
    )
    if contains_input_format_label_clues is not None and not isinstance(
        contains_input_format_label_clues, bool
    ):
        raise BenchmarkCLIError(
            "Blind manifest has an invalid input-format clue declaration"
        )
    papers = manifest.get("papers")
    if not isinstance(papers, list) or not papers:
        raise BenchmarkCLIError("Blind manifest has no paper list")
    if manifest.get("paper_count") != len(papers):
        raise BenchmarkCLIError("Blind manifest paper_count does not match its paper list")

    verified: List[Dict[str, Any]] = []
    seen_ids = set()
    seen_filenames = set()
    for index, paper in enumerate(papers):
        if not isinstance(paper, dict):
            raise BenchmarkCLIError(f"Blind manifest paper {index} is not an object")
        blind_id = paper.get("blind_id")
        if not isinstance(blind_id, str) or not _BLIND_ID.fullmatch(blind_id):
            raise BenchmarkCLIError(f"Blind manifest paper {index} has an invalid blind_id")
        if blind_id in seen_ids:
            raise BenchmarkCLIError("Blind manifest contains duplicate blind_id values")
        seen_ids.add(blind_id)
        filename = paper.get("filename")
        if not isinstance(filename, str):
            raise BenchmarkCLIError(f"Blind manifest paper {blind_id} has an invalid filename")
        if filename in seen_filenames:
            raise BenchmarkCLIError("Blind manifest contains duplicate filenames")
        seen_filenames.add(filename)
        manuscript = _safe_manifest_filename(root, filename)
        expected_hash = paper.get("blind_text_sha256")
        if not isinstance(expected_hash, str) or not _SHA256.fullmatch(expected_hash):
            raise BenchmarkCLIError(f"Blind manifest paper {blind_id} has an invalid hash")
        actual_hash = _sha256_file(manuscript)
        if actual_hash != expected_hash:
            raise BenchmarkCLIError(f"Blind manuscript hash mismatch for {blind_id}")
        verified.append(
            {
                "blind_id": blind_id,
                "filename": filename,
                "path": manuscript,
                "blind_text_sha256": expected_hash,
            }
        )
    input_disclosure = {
        "contains_source_identifiers": contains_source_identifiers,
    }
    if contains_version_label_clues is not None:
        input_disclosure["contains_version_label_clues"] = contains_version_label_clues
    if contains_input_format_label_clues is not None:
        input_disclosure["contains_input_format_label_clues"] = (
            contains_input_format_label_clues
        )
    return root, verified, _sha256_file(manifest_path), input_disclosure


def _read_verified_manuscript(paper: Mapping[str, Any]) -> str:
    path = paper["path"]
    payload = path.read_bytes()
    if _sha256_bytes(payload) != paper["blind_text_sha256"]:
        raise BenchmarkCLIError(f"Blind manuscript changed before review: {paper['blind_id']}")
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError:
        raise BenchmarkCLIError(f"Blind manuscript is not UTF-8: {paper['blind_id']}") from None


def _validate_nature_result_binding(bundle: Mapping[str, Any]) -> None:
    """Bind the final decision to raw AC output and numbers to the code view."""

    meta_entry = bundle.get("meta_review_model")
    raw_meta = meta_entry.get("review") if isinstance(meta_entry, Mapping) else None
    final_review = bundle.get("final_review")
    reviews = bundle.get("individual_reviews")
    if not isinstance(raw_meta, Mapping) or not isinstance(final_review, Mapping):
        raise BenchmarkCLIError("Nature bundle is missing raw or final review views")
    if not isinstance(reviews, list) or len(reviews) != 5:
        raise BenchmarkCLIError("Nature bundle must contain five reviewer score views")
    if final_review.get("Decision") != raw_meta.get("Decision"):
        raise BenchmarkCLIError("Nature final Decision is not bound to raw Area Chair output")
    for field, raw_value in raw_meta.items():
        if field not in NUMERIC_RANGES and final_review.get(field) != raw_value:
            raise BenchmarkCLIError(
                "Nature final text fields are not bound to raw Area Chair output"
            )
    for field, (lower, upper) in NUMERIC_RANGES.items():
        raw_score = raw_meta.get(field)
        if (
            isinstance(raw_score, bool)
            or not isinstance(raw_score, int)
            or not lower <= raw_score <= upper
        ):
            raise BenchmarkCLIError("Nature raw Area Chair numerical score is invalid")
        values = []
        for entry in reviews:
            review = entry.get("review") if isinstance(entry, Mapping) else None
            value = review.get(field) if isinstance(review, Mapping) else None
            if (
                isinstance(value, bool)
                or not isinstance(value, int)
                or not lower <= value <= upper
            ):
                raise BenchmarkCLIError("Nature reviewer numerical score is invalid")
            values.append(value)
        expected = int(round(sum(values) / len(values)))
        if final_review.get(field) != expected:
            raise BenchmarkCLIError(
                "Nature rounded-mean numerical result view does not match"
            )
    result_views = bundle.get("nature_result_views")
    if not isinstance(result_views, Mapping):
        raise BenchmarkCLIError("Nature bundle is missing explicit result-view provenance")
    if result_views.get("area_chair_decision_overwritten") is not False:
        raise BenchmarkCLIError("Nature Area Chair decision provenance is invalid")


def _validate_bundle_binding(
    bundle: Mapping[str, Any],
    paper: Mapping[str, Any],
    config: Optional[ReviewerConfig] = None,
) -> None:
    input_metadata = bundle.get("input")
    if not isinstance(input_metadata, Mapping):
        raise BenchmarkCLIError("Review bundle is missing blind input metadata")
    if input_metadata.get("blind_id") != paper["blind_id"]:
        raise BenchmarkCLIError("Review bundle blind_id binding does not match")
    if input_metadata.get("blind_text_sha256") != paper["blind_text_sha256"]:
        raise BenchmarkCLIError("Review bundle manuscript hash binding does not match")
    reviews = bundle.get("individual_reviews")
    if not isinstance(reviews, list) or len(reviews) != 5:
        raise BenchmarkCLIError("Review bundle must contain exactly five independent reviews")
    for entry in reviews:
        review = entry.get("review") if isinstance(entry, Mapping) else None
        score = review.get("Overall") if isinstance(review, Mapping) else None
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not 1 <= score <= 10:
            raise BenchmarkCLIError("Review bundle contains an invalid Overall score")
    final_review = bundle.get("final_review")
    if not isinstance(final_review, Mapping) or final_review.get("Decision") not in {
        "Accept",
        "Reject",
    }:
        raise BenchmarkCLIError("Review bundle contains an invalid final decision")
    if config is not None:
        bundle_config = bundle.get("config")
        if not isinstance(bundle_config, Mapping):
            raise BenchmarkCLIError("Review bundle is missing reviewer config")
        actual_protocol_id = bundle_config.get("protocol", LEGACY_PROTOCOL_ID)
        if actual_protocol_id != config.protocol:
            raise BenchmarkCLIError("Review bundle protocol binding does not match")
        expected_protocol = get_protocol_record(config)
        actual_protocol = bundle.get("protocol")
        if expected_protocol is not None and actual_protocol != expected_protocol:
            raise BenchmarkCLIError("Review bundle protocol fingerprint does not match")
        if expected_protocol is None and actual_protocol is not None:
            raise BenchmarkCLIError("Legacy run cannot resume a protocol-bound bundle")
        if expected_protocol is not None:
            _validate_nature_result_binding(bundle)


def _existing_bundle(
    bundle_path: Path,
    paper: Mapping[str, Any],
    config: ReviewerConfig,
) -> Optional[Dict[str, Any]]:
    if not bundle_path.exists():
        return None
    if bundle_path.is_symlink() or not bundle_path.is_file():
        return None
    bundle = _read_json_object(bundle_path, artifact="review bundle")
    _validate_bundle_binding(bundle, paper, config)
    markdown_path = bundle_path.with_name("review.md")
    if markdown_path.is_symlink() or not markdown_path.is_file():
        return None
    return bundle


def _publish_bundle(bundle: Dict[str, Any], output_root: Path, blind_id: str) -> Path:
    bundles_root = _secure_directory(output_root / "bundles")
    destination = _secure_directory(bundles_root / blind_id)
    staging_root = _secure_directory(output_root / ".staging")
    temporary = Path(tempfile.mkdtemp(prefix=f".{blind_id}.", dir=staging_root))
    temporary.chmod(0o700)
    try:
        json_path, markdown_path = write_outputs(bundle, temporary)
        os.replace(json_path, destination / "review_bundle.json")
        os.replace(markdown_path, destination / "review.md")
        (destination / "review_bundle.json").chmod(0o600)
        (destination / "review.md").chmod(0o600)
    finally:
        shutil.rmtree(temporary, ignore_errors=True)
    return destination / "review_bundle.json"


def _review_one_paper(
    paper: Mapping[str, Any],
    *,
    output_root: Path,
    client: Any,
    config: ReviewerConfig,
) -> Tuple[str, bool, str]:
    bundle_path = output_root / "bundles" / paper["blind_id"] / "review_bundle.json"
    existing = _existing_bundle(bundle_path, paper, config)
    if existing is not None:
        return paper["blind_id"], True, _sha256_file(bundle_path)

    text = _read_verified_manuscript(paper)
    try:
        bundle = review_text(text, client=client, config=config)
    except Exception as exc:
        raise BenchmarkCLIError(
            f"Review failed for {paper['blind_id']} ({type(exc).__name__})"
        ) from None
    bundle["input"] = {
        "blind_id": paper["blind_id"],
        "filename": paper["filename"],
        "blind_text_sha256": paper["blind_text_sha256"],
        "characters": len(text),
        "full_text_saved": False,
    }
    _validate_bundle_binding(bundle, paper, config)
    published = _publish_bundle(bundle, output_root, paper["blind_id"])
    return paper["blind_id"], False, _sha256_file(published)


def run_blind_benchmark(
    blind_dir: Path,
    output_dir: Path,
    *,
    client: Any,
    config: Optional[ReviewerConfig] = None,
    max_papers: Optional[int] = None,
    paper_jobs: int = 1,
) -> Dict[str, Any]:
    """Review verified blind manuscripts without accepting any label path."""

    if isinstance(paper_jobs, bool) or not isinstance(paper_jobs, int) or paper_jobs < 1:
        raise BenchmarkCLIError("paper_jobs must be a positive integer")
    if max_papers is not None and (
        isinstance(max_papers, bool) or not isinstance(max_papers, int) or max_papers < 1
    ):
        raise BenchmarkCLIError("max_papers must be a positive integer")

    config = config or ReviewerConfig()
    config.validate()
    if config.ensemble_size != 5:
        raise BenchmarkCLIError("The benchmark requires exactly five independent reviewers")
    blind_root, papers, manifest_hash, input_disclosure = load_blind_manifest(
        blind_dir, protocol=config.protocol
    )
    output_root = Path(output_dir).expanduser().resolve()
    if (
        output_root == blind_root
        or output_root in blind_root.parents
        or blind_root in output_root.parents
    ):
        raise BenchmarkCLIError("Run output and blind input must be separate directory trees")
    output_root = _secure_directory(output_root)
    selected = papers[:max_papers] if max_papers is not None else papers
    protocol_record = get_protocol_record(config)
    existing_manifest_path = output_root / "run_manifest.json"
    if existing_manifest_path.exists():
        if existing_manifest_path.is_symlink() or not existing_manifest_path.is_file():
            raise BenchmarkCLIError("Existing run manifest is not a real file")
        existing_manifest = _read_json_object(
            existing_manifest_path, artifact="run manifest"
        )
        if existing_manifest.get("source_blind_manifest_sha256") != manifest_hash:
            raise BenchmarkCLIError("Existing run manifest blind input binding does not match")
        existing_protocol = existing_manifest.get("protocol")
        if existing_protocol != protocol_record:
            raise BenchmarkCLIError("Existing run manifest protocol binding does not match")

    results: Dict[str, Tuple[bool, str]] = {}
    with ThreadPoolExecutor(max_workers=min(paper_jobs, len(selected))) as executor:
        futures = {
            executor.submit(
                _review_one_paper,
                paper,
                output_root=output_root,
                client=client,
                config=config,
            ): paper["blind_id"]
            for paper in selected
        }
        for future in as_completed(futures):
            blind_id = futures[future]
            try:
                completed_id, resumed, bundle_hash = future.result()
            except BenchmarkCLIError:
                raise
            except Exception as exc:
                raise BenchmarkCLIError(
                    f"Review worker failed for {blind_id} ({type(exc).__name__})"
                ) from None
            results[completed_id] = (resumed, bundle_hash)

    paper_records = [
        {
            "blind_id": paper["blind_id"],
            "blind_text_sha256": paper["blind_text_sha256"],
            "review_bundle_sha256": results[paper["blind_id"]][1],
        }
        for paper in selected
    ]
    run_manifest = {
        "format_version": RUN_FORMAT_VERSION,
        "contains_ground_truth": False,
        "contains_source_identifiers": input_disclosure[
            "contains_source_identifiers"
        ],
        "source_blind_manifest_sha256": manifest_hash,
        "paper_count": len(selected),
        "full_manifest_paper_count": len(papers),
        "smoke_test_limited": max_papers is not None,
        "paper_jobs": paper_jobs,
        "resumed_count": sum(resumed for resumed, _ in results.values()),
        "completed_or_verified_count": len(results),
        "papers": paper_records,
    }
    if "contains_version_label_clues" in input_disclosure:
        run_manifest["contains_version_label_clues"] = input_disclosure[
            "contains_version_label_clues"
        ]
    if "contains_input_format_label_clues" in input_disclosure:
        run_manifest["contains_input_format_label_clues"] = input_disclosure[
            "contains_input_format_label_clues"
        ]
    if protocol_record is not None:
        run_manifest["protocol"] = protocol_record
    _atomic_secure_write(
        output_root / "run_manifest.json", _json_bytes(run_manifest), overwrite=True
    )
    return run_manifest


def _collect_bundle_predictions(
    run_output_dir: Path,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    requested_root = Path(run_output_dir).expanduser()
    if requested_root.is_symlink():
        raise BenchmarkCLIError("Run output directory must not be a symbolic link")
    root = requested_root.resolve()
    run_manifest_path = root / "run_manifest.json"
    if run_manifest_path.is_symlink() or not run_manifest_path.is_file():
        raise BenchmarkCLIError("Run output has no real run manifest")
    run_manifest = _read_json_object(run_manifest_path, artifact="run manifest")
    if run_manifest.get("format_version") != RUN_FORMAT_VERSION:
        raise BenchmarkCLIError("Run manifest format version is unsupported")
    if run_manifest.get("contains_ground_truth") is not False:
        raise BenchmarkCLIError("Run manifest is not label-free")
    contains_source_identifiers = run_manifest.get("contains_source_identifiers")
    if not isinstance(contains_source_identifiers, bool):
        raise BenchmarkCLIError("Run manifest has no valid source-identifier disclosure")
    contains_version_label_clues = run_manifest.get("contains_version_label_clues")
    if contains_version_label_clues is not None and not isinstance(
        contains_version_label_clues, bool
    ):
        raise BenchmarkCLIError("Run manifest has an invalid version-clue disclosure")
    contains_input_format_label_clues = run_manifest.get(
        "contains_input_format_label_clues"
    )
    if contains_input_format_label_clues is not None and not isinstance(
        contains_input_format_label_clues, bool
    ):
        raise BenchmarkCLIError(
            "Run manifest has an invalid input-format clue disclosure"
        )
    manifest_papers = run_manifest.get("papers")
    if not isinstance(manifest_papers, list) or run_manifest.get("paper_count") != len(
        manifest_papers
    ):
        raise BenchmarkCLIError("Run manifest paper_count does not match its paper list")
    manifest_records: Dict[str, Mapping[str, Any]] = {}
    manifest_protocol = run_manifest.get("protocol")
    if manifest_protocol is not None:
        if not isinstance(manifest_protocol, Mapping):
            raise BenchmarkCLIError("Run manifest contains an invalid protocol binding")
        try:
            validate_nature_protocol_record(manifest_protocol)
        except ValueError:
            raise BenchmarkCLIError("Run manifest protocol fingerprint is invalid") from None
    for record in manifest_papers:
        if not isinstance(record, Mapping):
            raise BenchmarkCLIError("Run manifest contains an invalid paper entry")
        blind_id = record.get("blind_id")
        if not isinstance(blind_id, str) or blind_id in manifest_records:
            raise BenchmarkCLIError("Run manifest contains an invalid or duplicate blind_id")
        manifest_records[blind_id] = record

    bundles_root = root / "bundles"
    if not bundles_root.is_dir() or bundles_root.is_symlink():
        raise BenchmarkCLIError("Run output has no real bundles directory")
    bundle_paths = sorted(bundles_root.glob("*/review_bundle.json"))
    predictions: List[Dict[str, Any]] = []
    seen_ids = set()
    for path in bundle_paths:
        if path.is_symlink() or not path.is_file() or path.parent.is_symlink():
            raise BenchmarkCLIError("Bundle tree contains a symbolic link or invalid file")
        bundle = _read_json_object(path, artifact="review bundle")
        input_metadata = bundle.get("input")
        if not isinstance(input_metadata, Mapping):
            raise BenchmarkCLIError("Review bundle is missing blind input metadata")
        paper = {
            "blind_id": input_metadata.get("blind_id"),
            "blind_text_sha256": input_metadata.get("blind_text_sha256"),
        }
        blind_id = paper["blind_id"]
        blind_hash = paper["blind_text_sha256"]
        if not isinstance(blind_id, str) or not _BLIND_ID.fullmatch(blind_id):
            raise BenchmarkCLIError("Review bundle contains an invalid blind_id")
        if path.parent.name != blind_id or blind_id in seen_ids:
            raise BenchmarkCLIError("Bundle path and unique blind_id binding do not match")
        seen_ids.add(blind_id)
        if not isinstance(blind_hash, str) or not _SHA256.fullmatch(blind_hash):
            raise BenchmarkCLIError("Review bundle contains an invalid manuscript hash")
        _validate_bundle_binding(bundle, paper)
        bundle_protocol = bundle.get("protocol")
        if bundle_protocol != manifest_protocol:
            raise BenchmarkCLIError(
                f"Run manifest protocol binding does not match {blind_id}"
            )
        bundle_config = bundle.get("config")
        if not isinstance(bundle_config, Mapping):
            raise BenchmarkCLIError("Review bundle is missing reviewer config")
        expected_protocol_id = (
            manifest_protocol.get("protocol_id")
            if isinstance(manifest_protocol, Mapping)
            else LEGACY_PROTOCOL_ID
        )
        if bundle_config.get("protocol", LEGACY_PROTOCOL_ID) != expected_protocol_id:
            raise BenchmarkCLIError(
                f"Run manifest protocol id does not match {blind_id}"
            )
        if manifest_protocol is not None:
            _validate_nature_result_binding(bundle)
        scores = [entry["review"]["Overall"] for entry in bundle["individual_reviews"]]
        record = manifest_records.get(blind_id)
        bundle_hash = _sha256_file(path)
        if record is None:
            raise BenchmarkCLIError(f"Run manifest has no bundle record for {blind_id}")
        if record.get("blind_text_sha256") != blind_hash:
            raise BenchmarkCLIError(f"Run manifest manuscript hash does not match {blind_id}")
        if record.get("review_bundle_sha256") != bundle_hash:
            raise BenchmarkCLIError(f"Run manifest bundle hash does not match {blind_id}")
        if manifest_protocol is not None:
            final_decision = bundle["meta_review_model"]["review"]["Decision"]
        else:
            final_decision = bundle["final_review"]["Decision"]
        prediction = {
            "blind_id": blind_id,
            "blind_text_sha256": blind_hash,
            "individual_overall_scores": scores,
            "final_decision": final_decision,
            "review_bundle_sha256": bundle_hash,
        }
        if manifest_protocol is not None:
            prediction["protocol_fingerprint_sha256"] = manifest_protocol[
                "fingerprint_sha256"
            ]
        predictions.append(prediction)
    if seen_ids != set(manifest_records):
        raise BenchmarkCLIError("Run manifest and completed bundle sets do not match")
    disclosures: Dict[str, Any] = {
        "contains_source_identifiers": contains_source_identifiers,
        "protocol": manifest_protocol,
    }
    if contains_version_label_clues is not None:
        disclosures["contains_version_label_clues"] = contains_version_label_clues
    if contains_input_format_label_clues is not None:
        disclosures["contains_input_format_label_clues"] = (
            contains_input_format_label_clues
        )
    return sorted(predictions, key=lambda item: item["blind_id"]), disclosures


def freeze_predictions(
    run_output_dir: Path,
    frozen_path: Path,
    *,
    expected_count: int = 40,
) -> Dict[str, Any]:
    """Write a label-free prediction artifact plus an external SHA-256 sidecar."""

    if isinstance(expected_count, bool) or not isinstance(expected_count, int) or expected_count < 1:
        raise BenchmarkCLIError("expected_count must be a positive integer")
    predictions, disclosures = _collect_bundle_predictions(run_output_dir)
    if len(predictions) != expected_count:
        raise BenchmarkCLIError(
            f"Expected {expected_count} completed bundles, found {len(predictions)}"
        )
    artifact = {
        "format_version": FREEZE_FORMAT_VERSION,
        "contains_ground_truth": False,
        "contains_source_identifiers": disclosures["contains_source_identifiers"],
        "paper_count": len(predictions),
        "papers": predictions,
    }
    if "contains_version_label_clues" in disclosures:
        artifact["contains_version_label_clues"] = disclosures[
            "contains_version_label_clues"
        ]
    if "contains_input_format_label_clues" in disclosures:
        artifact["contains_input_format_label_clues"] = disclosures[
            "contains_input_format_label_clues"
        ]
    if disclosures["protocol"] is not None:
        artifact["protocol"] = disclosures["protocol"]
    requested_destination = Path(frozen_path).expanduser()
    if requested_destination.is_symlink():
        raise BenchmarkCLIError("Frozen prediction path must not be a symbolic link")
    destination = requested_destination.resolve()
    sidecar = destination.with_name(destination.name + ".sha256")
    if destination.exists() or sidecar.exists():
        raise BenchmarkCLIError("Refusing to overwrite a frozen prediction or hash file")
    payload = _json_bytes(artifact)
    digest = _sha256_bytes(payload)
    _atomic_secure_write(destination, payload, overwrite=False)
    try:
        _atomic_secure_write(
            sidecar, f"{digest}\n".encode("ascii"), overwrite=False
        )
    except Exception:
        # Avoid leaving a prediction file that appears frozen but has no hash.
        try:
            destination.unlink()
        except FileNotFoundError:
            pass
        raise
    return {
        "frozen_path": str(destination),
        "sha256_path": str(sidecar),
        "predictions_sha256": digest,
        "paper_count": len(predictions),
    }


def _load_verified_frozen_predictions(path: Path) -> Tuple[Dict[str, Any], str]:
    requested_path = Path(path).expanduser()
    if requested_path.is_symlink():
        raise BenchmarkCLIError("Frozen predictions and hash must not be symbolic links")
    prediction_path = requested_path.resolve()
    sidecar = prediction_path.with_name(prediction_path.name + ".sha256")
    if prediction_path.is_symlink() or sidecar.is_symlink():
        raise BenchmarkCLIError("Frozen predictions and hash must not be symbolic links")
    try:
        payload = prediction_path.read_bytes()
        sidecar_text = sidecar.read_text(encoding="ascii").strip()
    except Exception:
        raise BenchmarkCLIError("Frozen prediction or SHA-256 sidecar is missing") from None
    digest = _sha256_bytes(payload)
    if sidecar_text != digest:
        raise BenchmarkCLIError("Frozen prediction SHA-256 verification failed")
    try:
        artifact = json.loads(payload)
    except Exception:
        raise BenchmarkCLIError("Frozen prediction file is not valid JSON") from None
    if not isinstance(artifact, dict):
        raise BenchmarkCLIError("Frozen prediction file must contain a JSON object")
    if artifact.get("format_version") != FREEZE_FORMAT_VERSION:
        raise BenchmarkCLIError("Frozen prediction format version is unsupported")
    if artifact.get("contains_ground_truth") is not False:
        raise BenchmarkCLIError("Frozen prediction artifact is not label-free")
    return artifact, digest


def evaluate_frozen_predictions(
    frozen_path: Path,
    private_mapping_path: Path,
    output_path: Path,
    *,
    expected_count: int = 40,
    decision_threshold: float = 6.0,
    bootstrap_samples: int = 5000,
    bootstrap_seed: int = 2026,
) -> Dict[str, Any]:
    """Join a verified frozen artifact to labels and run the existing evaluator."""

    if isinstance(expected_count, bool) or not isinstance(expected_count, int) or expected_count < 1:
        raise BenchmarkCLIError("expected_count must be a positive integer")
    artifact, prediction_hash = _load_verified_frozen_predictions(frozen_path)
    source_input_disclosures: Dict[str, bool] = {}
    for disclosure_key in (
        "contains_source_identifiers",
        "contains_version_label_clues",
        "contains_input_format_label_clues",
    ):
        disclosure_value = artifact.get(disclosure_key)
        if disclosure_value is not None:
            if not isinstance(disclosure_value, bool):
                raise BenchmarkCLIError(
                    f"Frozen prediction has an invalid {disclosure_key} disclosure"
                )
            source_input_disclosures[disclosure_key] = disclosure_value
    frozen_protocol = artifact.get("protocol")
    if frozen_protocol is not None:
        if not isinstance(frozen_protocol, Mapping):
            raise BenchmarkCLIError("Frozen prediction has an invalid protocol binding")
        try:
            validate_nature_protocol_record(frozen_protocol)
        except ValueError:
            raise BenchmarkCLIError(
                "Frozen prediction protocol fingerprint is invalid"
            ) from None
    predictions = artifact.get("papers")
    if not isinstance(predictions, list) or artifact.get("paper_count") != len(predictions):
        raise BenchmarkCLIError("Frozen prediction paper_count does not match its paper list")
    if len(predictions) != expected_count:
        raise BenchmarkCLIError(
            f"Expected {expected_count} frozen predictions, found {len(predictions)}"
        )

    requested_mapping_path = Path(private_mapping_path).expanduser()
    if requested_mapping_path.is_symlink():
        raise BenchmarkCLIError("Private mapping is missing or is a symbolic link")
    mapping_path = requested_mapping_path.resolve()
    if not mapping_path.is_file():
        raise BenchmarkCLIError("Private mapping is missing or is a symbolic link")
    mapping = _read_json_object(mapping_path, artifact="private mapping")
    mapping_papers = mapping.get("papers")
    if not isinstance(mapping_papers, list):
        raise BenchmarkCLIError("Private mapping has no paper list")
    labels: Dict[str, Mapping[str, Any]] = {}
    for paper in mapping_papers:
        if not isinstance(paper, Mapping):
            raise BenchmarkCLIError("Private mapping contains an invalid paper entry")
        blind_id = paper.get("blind_id")
        if not isinstance(blind_id, str) or blind_id in labels:
            raise BenchmarkCLIError("Private mapping contains an invalid or duplicate blind_id")
        labels[blind_id] = paper

    cases: List[Dict[str, Any]] = []
    joined_ids = set()
    for prediction in predictions:
        if not isinstance(prediction, Mapping):
            raise BenchmarkCLIError("Frozen prediction contains an invalid paper entry")
        blind_id = prediction.get("blind_id")
        if not isinstance(blind_id, str) or blind_id in joined_ids:
            raise BenchmarkCLIError("Frozen predictions contain an invalid or duplicate blind_id")
        joined_ids.add(blind_id)
        private = labels.get(blind_id)
        if private is None:
            raise BenchmarkCLIError(f"Private mapping has no label for {blind_id}")
        if private.get("blind_text_sha256") != prediction.get("blind_text_sha256"):
            raise BenchmarkCLIError(f"Private mapping hash does not match {blind_id}")
        scores = prediction.get("individual_overall_scores")
        if not isinstance(scores, list):
            raise BenchmarkCLIError(f"Frozen prediction scores are invalid for {blind_id}")
        cases.append(
            {
                "ground_truth": private.get("ground_truth"),
                "individual_reviews": [
                    {"review": {"Overall": score}} for score in scores
                ],
                "final_review": {"Decision": prediction.get("final_decision")},
            }
        )

    try:
        evaluation = evaluate_review_bundles(
            cases,
            decision_threshold=decision_threshold,
            bootstrap_samples=bootstrap_samples,
            bootstrap_seed=bootstrap_seed,
        )
    except Exception as exc:
        raise BenchmarkCLIError(f"Evaluation failed ({type(exc).__name__})") from None
    evaluation["audit"] = {
        "expected_count": expected_count,
        "frozen_predictions_sha256": prediction_hash,
        "private_mapping_sha256": _sha256_file(mapping_path),
        "join_key": "blind_id plus blind_text_sha256",
        "source_input_disclosures": source_input_disclosures,
        "protocol_fingerprint_sha256": (
            frozen_protocol.get("fingerprint_sha256")
            if isinstance(frozen_protocol, Mapping)
            else None
        ),
    }
    _atomic_secure_write(Path(output_path), _json_bytes(evaluation), overwrite=True)
    return evaluation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run, freeze, and evaluate a label-isolated AutoReviewer benchmark."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run", help="review only blinded manuscripts")
    run.add_argument("blind_dir", type=Path)
    run.add_argument("output_dir", type=Path)
    run.add_argument("--max-papers", type=int)
    run.add_argument("--paper-jobs", type=int, default=1)
    run.add_argument("--model", default="deepseek-v4-flash")
    run.add_argument(
        "--reasoning-effort",
        choices=("none", "minimal", "low", "medium", "high", "max"),
        default="max",
    )
    run.add_argument("--max-output-tokens", type=int, default=16384)
    run.add_argument("--max-attempts", type=int, default=3)
    run.add_argument(
        "--protocol",
        choices=(LEGACY_PROTOCOL_ID, NATURE_PROTOCOL_ID),
        default=LEGACY_PROTOCOL_ID,
        help=(
            "strict-json-v1 keeps the existing default; nature-si-a3-base-v1 "
            "opts into the frozen Nature-aligned prompt and request policy"
        ),
    )

    freeze = subparsers.add_parser("freeze", help="freeze label-free bundle predictions")
    freeze.add_argument("run_output_dir", type=Path)
    freeze.add_argument("frozen_path", type=Path)
    freeze.add_argument("--expected-count", type=int, default=40)

    evaluate = subparsers.add_parser("evaluate", help="join frozen predictions to labels")
    evaluate.add_argument("frozen_path", type=Path)
    evaluate.add_argument("private_mapping", type=Path)
    evaluate.add_argument("output_path", type=Path)
    evaluate.add_argument("--expected-count", type=int, default=40)
    evaluate.add_argument("--decision-threshold", type=float, default=6.0)
    evaluate.add_argument("--bootstrap-samples", type=int, default=5000)
    evaluate.add_argument("--bootstrap-seed", type=int, default=2026)
    return parser


def _run_from_args(args: argparse.Namespace) -> Dict[str, Any]:
    load_dotenv(PROJECT_ROOT / ".env")
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise BenchmarkCLIError("DEEPSEEK_API_KEY is unavailable")
    config = ReviewerConfig(
        model=args.model,
        reasoning_effort=(
            "none" if args.protocol == NATURE_PROTOCOL_ID else args.reasoning_effort
        ),
        max_output_tokens=args.max_output_tokens,
        max_attempts=args.max_attempts,
        aggregate_scores=(
            "mean" if args.protocol == NATURE_PROTOCOL_ID else "meta"
        ),
        protocol=args.protocol,
    )
    client = create_deepseek_client(api_key=api_key, base_url=config.base_url)
    try:
        return run_blind_benchmark(
            args.blind_dir,
            args.output_dir,
            client=client,
            config=config,
            max_papers=args.max_papers,
            paper_jobs=args.paper_jobs,
        )
    finally:
        close = getattr(client, "close", None)
        if callable(close):
            close()


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "run":
            result = _run_from_args(args)
        elif args.command == "freeze":
            result = freeze_predictions(
                args.run_output_dir,
                args.frozen_path,
                expected_count=args.expected_count,
            )
        else:
            result = evaluate_frozen_predictions(
                args.frozen_path,
                args.private_mapping,
                args.output_path,
                expected_count=args.expected_count,
                decision_threshold=args.decision_threshold,
                bootstrap_samples=args.bootstrap_samples,
                bootstrap_seed=args.bootstrap_seed,
            )
    except BenchmarkCLIError as exc:
        print(f"Benchmark {args.command} failed: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        # Do not render arbitrary exception strings: SDK errors can contain
        # headers or request bodies. The exception type is sufficient for logs.
        print(
            f"Benchmark {args.command} failed ({type(exc).__name__})",
            file=sys.stderr,
        )
        return 1

    if args.command == "run":
        print(
            f"Reviewed or verified {result['paper_count']} blinded papers "
            f"({result['resumed_count']} resumed)."
        )
    elif args.command == "freeze":
        print(
            f"Frozen {result['paper_count']} predictions; "
            f"SHA-256 {result['predictions_sha256']}"
        )
    else:
        metrics = result["metrics"]
        print(
            f"Evaluated {result['n_papers']} papers; "
            f"balanced accuracy={metrics['balanced_accuracy']:.4f}, "
            f"AUROC={metrics['auroc']:.4f}."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
