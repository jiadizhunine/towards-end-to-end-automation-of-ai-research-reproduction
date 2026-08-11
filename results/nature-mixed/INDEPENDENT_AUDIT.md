# Independent audit: ICLR 2026 Nature-aligned mixed-version run

## Verdict

**PASS. No blocking integrity issue was found.**

The audit was read-only. It did not read `.env`, call the model API, access the network, or modify the run.

## Scope and result chain

- 200 papers, 78 camera-ready Accept and 122 initial-submission Reject.
- 1,000 independent Reviewer responses and 200 Area Chair responses.
- 1,200/1,200 raw responses parse successfully and equal their stored structured `review` objects.
- 1,200 globally unique response IDs.
- 1,200 application attempts; every call succeeded on its first attempt.
- 200/200 raw Area Chair `Decision` values equal `final_review.Decision` and the frozen final prediction.
- All nine numeric fields in the public-code-compatible final view equal the rounded arithmetic mean of the five Reviewer scores.
- Frozen predictions join to the private mapping on `blind_id + blind_text_sha256` for 200/200 papers, with no duplicate or unmatched keys.

## Recomputed evaluation

Confusion matrix: TN=33, FP=89, FN=6, TP=72.

| Metric | Estimate | 95% stratified paper bootstrap CI |
|---|---:|---:|
| Accuracy | 0.525000 | [0.475000, 0.580000] |
| Balanced accuracy | 0.596784 | [0.549916, 0.646490] |
| F1 | 0.602510 | [0.567797, 0.638655] |
| AUROC | 0.783575 | [0.719733, 0.845527] |
| FPR | 0.729508 | [0.647541, 0.803279] |
| FNR | 0.076923 | [0.025641, 0.141026] |

Bootstrap configuration: 5,000 replicates, seed 2026, paper-level percentile bootstrap stratified by ground truth. All estimates and interval bounds were independently recomputed and match `evaluation.json` exactly.

Supplementary diagnostics: Precision(Accept)=0.447205, TPR=0.923077, TNR=0.270492. Predictions are 161 Accept and 39 Reject.

## Usage and cost

- Prompt tokens: 27,581,482
- Cache-hit prompt tokens: 1,756,160
- Cache-miss prompt tokens: 25,825,322
- Completion tokens: 2,121,624
- Reasoning tokens: 0
- Total tokens: 29,703,106
- Cost from aggregate, unrounded usage: $4.214517048
- Sum of per-bundle eight-decimal costs: $4.21451744

The $0.000000392 difference is solely due to per-bundle rounding. Because every application call succeeded on its first attempt, this run has no unrecorded failed-attempt usage at the application layer.

## Protocol binding

- Protocol: `nature-si-a3-base-v1`
- Fingerprint: `593791d8c5435a95c06952f703409af0b64eaf3ad22bf1e47426d682ac4cd717`
- Model: `deepseek-v4-flash`
- Maximum output: 16,384 tokens
- Temperature: 0.75
- DeepSeek thinking: disabled
- Omitted request fields: `reasoning_effort`, `response_format`, `tools`
- Network policy: no browser, search, retrieval, RAG, or model tools; only model API transport is allowed.

The six frozen prompt/template hashes were recomputed from the current literals and match the protocol record. The effective-request record and the executed code path agree. The artifacts do not retain each provider-side raw HTTP request body, so this is not a supplier log audit.

## Disclosure propagation

The source manifest, run manifest, frozen predictions, and evaluation all propagate these three disclosures as `true`:

- `contains_source_identifiers`
- `contains_version_label_clues`
- `contains_input_format_label_clues`

The public source manifest explicitly records `contains_ground_truth=false` and `strictly_blinded=false`.

## Files and hashes

- Audited result-chain files before this audit report was added: 404; current total including this report: 405
- Subdirectories: 202
- Symlinks or special nodes: 0
- Files: mode 0600
- Directories: mode 0700
- Empty staging directory; no extra result files
- All 200 bundle hashes match both the run manifest and frozen predictions.

Key SHA-256 values:

- Run manifest: `88dd859b555ea69edd99bb639ded630984d0850c310fb7dd622af1649aa1ecaa`
- Source manifest: `5d16a85cf0e725fb09e65360b9c6db7be11bab32010062e4abba0445f548b91f`
- Private mapping: `87e107715187f0fd2102208303413a941384effd72cac31b8b0a867f0b49d19d`
- Frozen predictions: `5215bbcc20f08d7cf9173403dd55a9b292c1dd74473e570be3e673026ed9bc56`
- Evaluation: `d9a898c76590f640cec5f54356c8c8c17191a487e7e26075f3adda527ec54e5c`

## Non-blocking format caveat

1,196/1,200 responses used preamble text followed by fenced JSON. Three Area Chair responses returned direct JSON, and one response used THOUGHT followed by unfenced JSON. Some responses did not reproduce the literal `REVIEW JSON:` label. All 1,200 were accepted by the frozen parser and their parsed objects exactly match the stored review objects, so this is an instruction-format compliance caveat rather than a result-integrity failure.
