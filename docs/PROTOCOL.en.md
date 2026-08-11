<div align="center">

**English** | [简体中文](./PROTOCOL.md)

</div>

# Reproduction protocol

## Scope

This protocol covers the AutoReviewer component only. It does not reproduce the
idea generation, experiment execution, manuscript generation, or workshop
submission components of the full AI Scientist system.

## Fixed cohort

- Conference snapshot: ICLR 2026 test split from the ProReviewer dataset.
- Source parquet SHA-256:
  `c9cb7de219be6e4455fcb594ec8be39f8c0bdf5dcfc575d588774d33fd73e10b`.
- Eligible labels: explicit Accept tiers and exact Reject only.
- Excluded labels: Withdrawn, Desk Reject, blank, and all other statuses.
- Fixed cohort: 200 papers, 78 Accept and 122 Reject.
- Selection and input hashes are committed in the run manifests and frozen
  prediction files. Source manuscripts and private mappings are not redistributed.

## Review topology

1. Five independent Reviewer calls use the same manuscript and review condition.
2. Every response must parse into the complete structured review schema.
3. The five structured reviews are provided to one Area Chair call.
4. The raw Area Chair `Decision` is the authoritative binary prediction.
5. The run is frozen without labels.
6. Evaluation separately joins `blind_id + blind_text_sha256` to the private label
   mapping and computes metrics.

## Nature-aligned protocol record

- Protocol ID: `nature-si-a3-base-v1`.
- Fingerprint:
  `593791d8c5435a95c06952f703409af0b64eaf3ad22bf1e47426d682ac4cd717`.
- Model: `deepseek-v4-flash`.
- Reviewer calls: 5 independent HTTP requests.
- Area Chair calls: 1.
- Temperature: `0.75`.
- DeepSeek thinking: disabled.
- Omitted request fields: `reasoning_effort`, `response_format`, `tools`.
- Max output tokens: 16,384.
- Max attempts per call: 3.
- Reviewer parallelism: 5.
- Few-shot examples: 0.
- Reflexion passes: 0.
- VLM passes: 0.
- Final binary decision: raw Area Chair `Decision`.
- Published-code-compatible numeric view: rounded arithmetic mean of the five
  Reviewer scores, preserving Area Chair text and decision.

The run manifest separates paper-declared details, frozen-public-code details,
and DeepSeek adapter choices. This distinction is required because the Nature
article does not publish every sampling and provider parameter.

## Manuscript conditions

### Strict all-initial

Both classes use the ProReviewer initial-submission Markdown snapshot. A strict
redaction pass removes titles, authors, affiliations, paper/forum IDs, arXiv IDs,
conference/decision status, URLs, domains, DOI, email, ORCID, acknowledgements,
author contributions, institutions, and lifecycle clues. The formal run uses the
older strict JSON protocol with DeepSeek thinking enabled and
`reasoning_effort=max`.

### Nature-aligned mixed-version

Accepted papers use official ICLR 2026 proceedings PDFs. The acquisition script
matches the fixed accepted cohort to the official proceedings index, validates
title and author evidence, downloads only official PDF URLs, checks MIME, length,
PDF magic, SHA-256, page count, and first-page conference marker, and records a
private provenance manifest. PyMuPDF extracts visible text page by page.

Rejected papers retain ProReviewer initial-submission Markdown. No redaction is
applied to this mixed-version condition. The public input manifest explicitly
records:

```json
{
  "contains_source_identifiers": true,
  "contains_version_label_clues": true,
  "contains_input_format_label_clues": true,
  "strictly_blinded": false
}
```

The accepted and rejected inputs therefore differ in both version and format.

## Camera-ready acquisition

The repository does not include the 78 PDFs. With an authorized local private
mapping, validate matches without writing:

```bash
python scripts/fetch_camera_ready.py \
  /path/to/private/mapping.json \
  /path/to/camera-ready-private \
  --dry-run
```

Explicitly replace `--dry-run` with `--download` only when the official PDF
download is intended. The builder fails closed and publishes the destination
atomically after validation.

The mixed input tree is constructed in Python with
`deepseek_autoreviewer.mixed_version.build_mixed_version_benchmark`. It requires
the strict private mapping, pinned source parquet, camera-ready provenance
manifest, and a new output directory.

## Metrics

- Positive class: Accept.
- Binary prediction: raw Area Chair decision.
- Balanced accuracy: `(TPR + TNR) / 2`.
- AUROC score: arithmetic mean of the five independent Reviewer `Overall` scores.
- Main uncertainty: paper-level percentile bootstrap stratified by the true class.
- Strict evaluation: 10,000 replicates, seed 20260811.
- Mixed evaluation and paired comparison: 5,000 replicates, seed 2026.

Nature does not fully specify the continuous AUROC score, bootstrap seed,
stratification, provider batch semantics, or every failure-handling detail. These
are frozen operational choices rather than claims of exact parameter replication.

## Reproduction boundary

An exact causal manuscript-version comparison would require rerunning both
all-initial and mixed-version inputs under the same prompt, extraction format,
identity treatment, model request, and aggregation policy. The two released runs
do not satisfy that requirement and must not be described as a camera-ready
ablation.
