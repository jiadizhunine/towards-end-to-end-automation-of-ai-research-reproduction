#!/usr/bin/env python3
"""Evaluate an ICLR 2026 paper-level human-rating proxy, locally only.

This is deliberately separate from the AutoReviewer evaluator.  It selects the
same B001--B200 papers through the private mapping, uses the arithmetic mean of
each paper's 3--5 ``scores.rating`` values as a continuous score, and predicts
Accept only when that mean is strictly greater than 5.  A mean equal to 5 is
therefore Reject.

The resulting row is a retrospective paper-level proxy against the final
conference decision.  It is *not* an independent human-vs-human agreement or
reviewer-reliability estimate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import re
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple

import pyarrow.parquet as pq


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PARQUET = PROJECT_ROOT / "data/source/proreviewer/iclr2026-test.parquet"
DEFAULT_MAPPING = (
    PROJECT_ROOT
    / "data/benchmark/iclr2026-realratio-200-v2/private/mapping.json"
)
FORMAT_VERSION = "iclr2026-human-rating-proxy-v1"
MAPPING_FORMAT_VERSION = "proreviewer-iclr2026-v1"
DEFAULT_BOOTSTRAP_SAMPLES = 5_000
DEFAULT_BOOTSTRAP_SEED = 2026
EXPECTED_IDS = tuple(f"B{index:03d}" for index in range(1, 201))
EXPECTED_CLASS_COUNTS = {"Accept": 78, "Reject": 122}
ACCEPT_DECISIONS = frozenset(
    {
        "Accept (Poster)",
        "Accept (Oral)",
        "Conditional Accept (Poster)",
        "Conditional Accept (Oral)",
    }
)
REJECT_DECISION = "Reject"
METRICS = (
    "balanced_accuracy",
    "accuracy",
    "f1",
    "auroc",
    "fpr",
    "fnr",
)
_BLIND_ID = re.compile(r"^B[0-9]{3}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class HumanProxyError(ValueError):
    """Raised when an input cannot safely support the fixed proxy analysis."""


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _real_file(path: Path, *, artifact: str) -> Path:
    requested = Path(path).expanduser()
    if requested.is_symlink():
        raise HumanProxyError(f"{artifact} must not be a symbolic link")
    resolved = requested.resolve()
    if not resolved.is_file() or resolved.is_symlink():
        raise HumanProxyError(f"{artifact} is missing or is not a real file")
    return resolved


def _read_mapping(path: Path) -> Tuple[Dict[str, Any], Path, str]:
    source = _real_file(path, artifact="Private mapping")
    payload = source.read_bytes()
    try:
        value = json.loads(payload)
    except Exception:
        raise HumanProxyError("Private mapping is not valid JSON") from None
    if not isinstance(value, dict):
        raise HumanProxyError("Private mapping must contain a JSON object")
    if value.get("format_version") != MAPPING_FORMAT_VERSION:
        raise HumanProxyError("Private mapping format_version is unsupported")
    return value, source, hashlib.sha256(payload).hexdigest()


def _paper_id(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise HumanProxyError(f"{field} must be a non-empty string")
    return value.strip()


def _mapping_index(mapping: Mapping[str, Any]) -> List[Tuple[str, str]]:
    papers = mapping.get("papers")
    if not isinstance(papers, list) or len(papers) != 200:
        count = len(papers) if isinstance(papers, list) else "invalid"
        raise HumanProxyError(f"Private mapping must contain 200 papers, found {count}")

    by_id: Dict[str, str] = {}
    seen_paper_ids = set()
    for index, entry in enumerate(papers):
        if not isinstance(entry, Mapping):
            raise HumanProxyError(f"Private mapping paper {index} is not an object")
        blind_id = entry.get("blind_id")
        if not isinstance(blind_id, str) or not _BLIND_ID.fullmatch(blind_id):
            raise HumanProxyError(f"Private mapping paper {index} has an invalid blind_id")
        if blind_id in by_id:
            raise HumanProxyError(f"Duplicate private blind_id: {blind_id}")
        source_id = _paper_id(entry.get("paper_id"), field=f"{blind_id} paper_id")
        if source_id in seen_paper_ids:
            raise HumanProxyError(f"Duplicate private paper_id for {blind_id}")
        by_id[blind_id] = source_id
        seen_paper_ids.add(source_id)

    if set(by_id) != set(EXPECTED_IDS):
        raise HumanProxyError("Private mapping must contain exactly B001 through B200")
    return [(blind_id, by_id[blind_id]) for blind_id in EXPECTED_IDS]


def _ratings(value: Any, *, blind_id: str) -> Tuple[float, ...]:
    if isinstance(value, str):
        parts: Sequence[Any] = value.split(";")
    elif isinstance(value, (list, tuple)):
        parts = value
    else:
        raise HumanProxyError(f"{blind_id} scores.rating must be a rating array")
    if not 3 <= len(parts) <= 5:
        raise HumanProxyError(f"{blind_id} must have between 3 and 5 human ratings")

    parsed: List[float] = []
    for item in parts:
        if isinstance(item, bool):
            raise HumanProxyError(f"{blind_id} ratings must be numeric")
        if isinstance(item, str):
            item = item.strip()
            if not item:
                raise HumanProxyError(f"{blind_id} ratings must not be missing")
        try:
            number = float(item)
        except (TypeError, ValueError):
            raise HumanProxyError(f"{blind_id} ratings must be numeric") from None
        if not math.isfinite(number) or not 0 <= number <= 10:
            raise HumanProxyError(
                f"{blind_id} ratings must be finite values in [0, 10]"
            )
        parsed.append(number)
    return tuple(parsed)


def _ground_truth(value: Any, *, blind_id: str) -> int:
    if not isinstance(value, Mapping):
        raise HumanProxyError(f"{blind_id} decision must be an object")
    decision = value.get("decision")
    if decision in ACCEPT_DECISIONS:
        return 1
    if decision == REJECT_DECISION:
        return 0
    raise HumanProxyError(
        f"{blind_id} decision.decision must be an eligible Accept or exact Reject"
    )


def _load_cases(
    parquet_path: Path, mapping_path: Path
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    parquet = _real_file(parquet_path, artifact="ICLR 2026 parquet")
    parquet_hash = _sha256_file(parquet)
    mapping, mapping_file, mapping_hash = _read_mapping(mapping_path)

    expected_hash = mapping.get("source_parquet_sha256")
    if not isinstance(expected_hash, str) or not _SHA256.fullmatch(expected_hash):
        raise HumanProxyError("Private mapping source_parquet_sha256 is invalid")
    if expected_hash != parquet_hash:
        raise HumanProxyError("Private mapping does not match the source parquet hash")

    try:
        table = pq.read_table(parquet, columns=["paper_id", "scores", "decision"])
    except Exception as error:
        raise HumanProxyError(
            "Could not read paper_id, scores, and decision from the source parquet"
        ) from error
    if mapping.get("source_row_count") != table.num_rows:
        raise HumanProxyError("Private mapping does not match the source parquet row count")

    source_by_id: Dict[str, Mapping[str, Any]] = {}
    for index, row in enumerate(table.to_pylist()):
        if not isinstance(row, Mapping):
            raise HumanProxyError(f"Source parquet row {index} is invalid")
        source_id = _paper_id(row.get("paper_id"), field=f"Source row {index} paper_id")
        if source_id in source_by_id:
            raise HumanProxyError(f"Duplicate source parquet paper_id: {source_id}")
        source_by_id[source_id] = row

    cases: List[Dict[str, Any]] = []
    for blind_id, source_id in _mapping_index(mapping):
        row = source_by_id.get(source_id)
        if row is None:
            raise HumanProxyError(f"{blind_id} paper_id is missing from the source parquet")
        scores = row.get("scores")
        if not isinstance(scores, Mapping):
            raise HumanProxyError(f"{blind_id} scores must be an object")
        values = _ratings(scores.get("rating"), blind_id=blind_id)
        mean_score = sum(values) / len(values)
        truth = _ground_truth(row.get("decision"), blind_id=blind_id)
        cases.append(
            {
                "blind_id": blind_id,
                "truth": truth,
                "prediction": int(mean_score > 5.0),
                "score": mean_score,
                "rating_count": len(values),
            }
        )

    if len(cases) != 200 or len({case["blind_id"] for case in cases}) != 200:
        raise HumanProxyError("Joined cohort must contain 200 unique papers")
    class_counts = {
        "Accept": sum(case["truth"] == 1 for case in cases),
        "Reject": sum(case["truth"] == 0 for case in cases),
    }
    if class_counts != EXPECTED_CLASS_COUNTS:
        raise HumanProxyError(
            f"Joined cohort class counts must be {EXPECTED_CLASS_COUNTS}, found {class_counts}"
        )
    audit = {
        "source_parquet_path": str(parquet),
        "source_parquet_sha256": parquet_hash,
        "source_row_count": table.num_rows,
        "private_mapping_path": str(mapping_file),
        "private_mapping_sha256": mapping_hash,
        "join_key": "private mapping paper_id to source parquet paper_id",
        "verified_paper_count": 200,
    }
    return cases, audit


def _binary_auroc(truth: Sequence[int], scores: Sequence[float]) -> float:
    """Tie-aware Mann-Whitney AUROC using average ranks."""

    if len(truth) != len(scores) or not truth:
        raise HumanProxyError("AUROC inputs must have the same non-zero length")
    positives = sum(truth)
    negatives = len(truth) - positives
    if positives == 0 or negatives == 0:
        raise HumanProxyError("AUROC requires both ground-truth classes")

    ordered = sorted(zip(scores, truth), key=lambda item: item[0])
    positive_rank_sum = 0.0
    index = 0
    while index < len(ordered):
        end = index + 1
        while end < len(ordered) and ordered[end][0] == ordered[index][0]:
            end += 1
        average_rank = ((index + 1) + end) / 2
        positive_rank_sum += average_rank * sum(
            label for _, label in ordered[index:end]
        )
        index = end
    return (
        positive_rank_sum - positives * (positives + 1) / 2
    ) / (positives * negatives)


def _metrics(cases: Sequence[Mapping[str, Any]]) -> Tuple[Dict[str, float], Dict[str, Any]]:
    if not cases:
        raise HumanProxyError("At least one paper is required")
    truth = [int(case["truth"]) for case in cases]
    predictions = [int(case["prediction"]) for case in cases]
    scores = [float(case["score"]) for case in cases]
    tp = sum(t == 1 and p == 1 for t, p in zip(truth, predictions))
    tn = sum(t == 0 and p == 0 for t, p in zip(truth, predictions))
    fp = sum(t == 0 and p == 1 for t, p in zip(truth, predictions))
    fn = sum(t == 1 and p == 0 for t, p in zip(truth, predictions))
    positives = tp + fn
    negatives = tn + fp
    if positives == 0 or negatives == 0:
        raise HumanProxyError("Metrics require both ground-truth classes")
    tpr = tp / positives
    tnr = tn / negatives
    f1_denominator = 2 * tp + fp + fn
    values = {
        "balanced_accuracy": (tpr + tnr) / 2,
        "accuracy": (tp + tn) / len(cases),
        "f1": 2 * tp / f1_denominator if f1_denominator else 0.0,
        "auroc": _binary_auroc(truth, scores),
        "fpr": fp / negatives,
        "fnr": fn / positives,
    }
    confusion = {
        "labels": ["Reject", "Accept"],
        "matrix": [[tn, fp], [fn, tp]],
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
    }
    return values, confusion


def _percentile(values: Sequence[float], probability: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise HumanProxyError("Cannot compute a percentile of an empty sequence")
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def _bootstrap(
    cases: Sequence[Mapping[str, Any]], *, samples: int, seed: int
) -> Dict[str, Dict[str, float]]:
    if isinstance(samples, bool) or not isinstance(samples, int) or samples < 1:
        raise HumanProxyError("bootstrap samples must be a positive integer")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise HumanProxyError("bootstrap seed must be an integer")
    positives = [case for case in cases if case["truth"] == 1]
    negatives = [case for case in cases if case["truth"] == 0]
    if not positives or not negatives:
        raise HumanProxyError("Stratified bootstrap requires both classes")

    generator = random.Random(seed)
    distributions: Dict[str, List[float]] = {name: [] for name in METRICS}
    for _ in range(samples):
        sampled = [generator.choice(positives) for _ in positives]
        sampled.extend(generator.choice(negatives) for _ in negatives)
        values, _ = _metrics(sampled)
        for name in METRICS:
            distributions[name].append(values[name])
    return {
        name: {
            "lower": _percentile(distributions[name], 0.025),
            "upper": _percentile(distributions[name], 0.975),
        }
        for name in METRICS
    }


def build_report(
    parquet_path: Path,
    mapping_path: Path,
    *,
    bootstrap_samples: int = DEFAULT_BOOTSTRAP_SAMPLES,
    bootstrap_seed: int = DEFAULT_BOOTSTRAP_SEED,
) -> Dict[str, Any]:
    """Build the fixed 200-paper proxy report without writing it."""

    cases, audit = _load_cases(parquet_path, mapping_path)
    point, confusion = _metrics(cases)
    intervals = _bootstrap(cases, samples=bootstrap_samples, seed=bootstrap_seed)
    rating_counts = {
        str(count): sum(case["rating_count"] == count for case in cases)
        for count in range(3, 6)
    }
    return {
        "format_version": FORMAT_VERSION,
        "analysis_name": "ICLR 2026 paper-level human-rating proxy",
        "interpretation": {
            "valid_use": (
                "Retrospective consistency of a paper-level mean human rating proxy "
                "with the final conference decision on the fixed B001-B200 cohort."
            ),
            "not_valid_as": (
                "Independent human-vs-human agreement, inter-rater reliability, or a "
                "causal estimate of reviewer quality."
            ),
        },
        "method": {
            "human_score_source": (
                "arithmetic mean of each paper's 3-5 scores.rating values"
            ),
            "binary_prediction": "Accept iff mean rating > 5; mean rating == 5 is Reject",
            "ground_truth_source": "source parquet decision.decision only",
            "positive_class": "Accept",
            "resampling_unit": "complete paper",
        },
        "n_papers": 200,
        "n_accept": EXPECTED_CLASS_COUNTS["Accept"],
        "n_reject": EXPECTED_CLASS_COUNTS["Reject"],
        "predicted_accept": sum(case["prediction"] == 1 for case in cases),
        "predicted_reject": sum(case["prediction"] == 0 for case in cases),
        "mean_equal_to_5_count": sum(case["score"] == 5.0 for case in cases),
        "rating_count_distribution": rating_counts,
        "metrics": point,
        "confidence_intervals_95": intervals,
        "confusion_matrix": confusion,
        "bootstrap": {
            "method": "ground-truth-stratified paper-level percentile bootstrap",
            "samples": bootstrap_samples,
            "seed": bootstrap_seed,
            "confidence_level": 0.95,
        },
        "audit": audit,
    }


def write_report(
    output_path: Path, report: Mapping[str, Any], *, overwrite: bool = False
) -> Path:
    """Atomically write JSON; refuse overwrite unless explicitly requested."""

    requested = Path(output_path).expanduser()
    if requested.is_symlink():
        raise HumanProxyError("Output file must not be a symbolic link")
    destination = requested.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing output: {destination}")
    if destination.exists() and not destination.is_file():
        raise HumanProxyError("Output path must be a file")
    payload = (
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", dir=destination.parent
    )
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
        temporary.unlink(missing_ok=True)
        raise
    return destination


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--parquet",
        type=Path,
        default=DEFAULT_PARQUET,
        help=f"fixed ICLR 2026 ProReviewer parquet (default: {DEFAULT_PARQUET})",
    )
    parser.add_argument(
        "--mapping",
        type=Path,
        default=DEFAULT_MAPPING,
        help=f"private B001-B200 mapping (default: {DEFAULT_MAPPING})",
    )
    parser.add_argument("--output", type=Path, required=True, help="new JSON output path")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="explicitly replace an existing output file",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        report = build_report(args.parquet, args.mapping)
        destination = write_report(args.output, report, overwrite=args.overwrite)
    except (HumanProxyError, FileExistsError) as error:
        parser.exit(2, f"error: {error}\n")
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
