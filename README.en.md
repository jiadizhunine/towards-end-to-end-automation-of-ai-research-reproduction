<div align="center">

**English** | [简体中文](./README.md)

</div>

<div align="center">

# Towards End-to-End Automation of AI Research — Reproduction

**A 200-paper reproduction of the paper's AutoReviewer component with DeepSeek V4 Flash**

![Version](https://img.shields.io/badge/release-v0.1.1-blue)
![License](https://img.shields.io/badge/license-Apache--2.0-green)
![Python](https://img.shields.io/badge/python-3.9%2B-3776AB)
![Cohort](https://img.shields.io/badge/ICLR%202026-200%20papers-orange)

</div>

This repository reproduces the **Automated Reviewer** component described in
[*Towards end-to-end automation of AI research*](https://www.nature.com/articles/s41586-026-10265-5).
It replaces the paper's `o4-mini` reviewer with `deepseek-v4-flash` and evaluates
two 200-paper ICLR 2026 conditions.

The repository contains the runnable implementation, frozen prompt and protocol
fingerprints, 400 complete review bundles, frozen predictions, evaluation files,
independent audit reports, and publication-ready comparison tables. It does not
redistribute manuscript PDFs, extracted manuscript text, private label mappings,
or API credentials.

## What was reproduced

Each paper receives five independent structured reviews. The same model then acts
as an Area Chair and produces one meta-review and a binary Accept/Reject decision.
The formal reviewer has no browser, search, retrieval, RAG, URL-fetching, or model
tools; network access is used only to call the DeepSeek API.

| Condition | Strict all-initial | Nature-aligned mixed-version |
|---|---|---|
| Cohort | Same 200 papers: 78 Accept, 122 Reject | Same 200 papers: 78 Accept, 122 Reject |
| Accept manuscripts | Initial-submission Markdown | Official ICLR 2026 camera-ready PDF text |
| Reject manuscripts | Initial-submission Markdown | Initial-submission Markdown |
| Visible identity/version clues | Removed | Retained when visible in extracted text |
| Reviewer prompt | Local strict JSON protocol | Nature base prompt + full frozen NeurIPS form |
| DeepSeek request | Thinking enabled; `reasoning_effort=max` | Thinking disabled; `temperature=0.75` |
| Aggregation | Raw Area Chair scores and decision | Area Chair decision/text; rounded five-review means for numeric fields |

These conditions differ in more than manuscript version. Prompt, inference mode,
input format, identity clues, lifecycle clues, and numeric aggregation also change.
Their difference is therefore **not a causal estimate of the camera-ready effect**.

## Main results

| Metric | Strict all-initial | Nature-aligned mixed-version |
|---|---:|---:|
| Balanced accuracy | 0.537 [0.474, 0.601] | 0.597 [0.550, 0.646] |
| Accuracy | 0.585 [0.525, 0.645] | 0.525 [0.475, 0.580] |
| F1 (Accept) | 0.376 [0.271, 0.474] | 0.603 [0.568, 0.639] |
| AUROC | 0.586 [0.503, 0.667] | 0.784 [0.720, 0.846] |
| FPR | 0.246 [0.172, 0.328] | 0.730 [0.648, 0.803] |
| FNR | 0.679 [0.577, 0.782] | 0.077 [0.026, 0.141] |

The strict condition was strongly Reject-leaning. The mixed-version condition
ranked accepted papers more effectively but classified most rejected papers as
Accept. Neither result establishes scientific-quality judgement or human-level
peer review.

### Table 1a — strict all-initial condition

[![Strict all-initial results](assets/table1a_strict_initial.png)](assets/table1a_strict_initial.svg)

### Table 1b — Nature-aligned mixed-version condition

[![Nature-aligned mixed-version results](assets/table1b_nature_mixed.png)](assets/table1b_nature_mixed.svg)

The ICLR 2026 human row is a **rating proxy**, not an independent two-committee
human-consistency experiment. See the [AutoReviewer report](docs/AUTOREVIEW_REPORT.en.md)
for definitions, uncertainty, the Nature baselines, and interpretation limits.

## API usage and cost

The DeepSeek dashboard screenshot below is filtered to the API-key alias
`Reviewer` over the previous 30 days. It reports **CNY 65.48**, **2,484 API
requests**, and **60,964,615 tokens**. No API-key value is visible in the image.

![DeepSeek dashboard usage: CNY 65.48, 2,484 requests, 60,964,615 tokens](assets/deepseek-api-usage.png)

This dashboard total is broader than the two formal runs: it may include smoke
tests, retries, and other calls made with the same key alias. The bundle-level
usage records provide the auditable run-specific estimates:

- strict all-initial: USD 4.61247628 verifiable lower bound;
- Nature-aligned mixed-version: USD 4.214517048;
- combined formal-run estimate: approximately USD 8.82699333.

Prices are the runtime assumptions recorded in each bundle, not a promise of
current DeepSeek pricing.

## Quick start

```bash
git clone https://github.com/jiadizhunine/towards-end-to-end-automation-of-ai-research-reproduction.git
cd towards-end-to-end-automation-of-ai-research-reproduction
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
cp .env.example .env
```

Put your own key only in the local `.env` file:

```dotenv
DEEPSEEK_API_KEY=replace_with_your_key
```

Review one PDF with the five-reviewer plus Area-Chair pipeline:

```bash
deepseek-autoreviewer paper.pdf --output-dir outputs/example
```

Run a prepared label-isolated benchmark with the Nature-aligned protocol:

```bash
iclr2026-autoreviewer run prepared/label_isolated results/new-run \
  --protocol nature-si-a3-base-v1 \
  --paper-jobs 2

iclr2026-autoreviewer freeze \
  results/new-run \
  results/new-run/frozen_predictions.json \
  --expected-count 200

iclr2026-autoreviewer evaluate \
  results/new-run/frozen_predictions.json \
  prepared/private/mapping.json \
  results/new-run/evaluation.json \
  --expected-count 200 \
  --bootstrap-samples 5000 \
  --bootstrap-seed 2026
```

The labels are joined only after predictions have been frozen. Dataset preparation
and camera-ready acquisition are documented in [PROTOCOL.en.md](docs/PROTOCOL.en.md).

## Repository structure

```text
src/deepseek_autoreviewer/   reviewer, benchmark, blinding, and protocol code
scripts/                     camera-ready acquisition, human proxy, and table renderers
tests/                       deterministic unit and integration tests
results/strict-initial/      200 bundles, frozen predictions, evaluation, and audit
results/nature-mixed/        200 bundles, frozen predictions, evaluation, and audit
results/comparison/          paired statistics and table specifications
assets/                      rendered tables and API-usage screenshot
docs/                        bilingual protocol, security guidance, and summary report
```

## Data and security boundaries

- `.env` and all common credential variants are ignored.
- API keys are read from the process environment and are never serialized into
  review bundles.
- Manuscript PDFs, extracted text, parquet snapshots, and private identity/label
  mappings are not included.
- The accepted-paper fetcher uses official ICLR 2026 proceedings URLs and records
  hashes and provenance locally.
- Each result bundle records hashes rather than the full manuscript text.

Read [SECURITY.en.md](SECURITY.en.md) before running the API client or publishing a fork.

## Validation

```bash
python -m pytest -q
```

The public release was validated against all 68 tests, both rendered comparison
tables, the frozen prediction hashes, and a repository-wide secret/path scan.

## Scope and limitations

This is an independent reproduction of one component, not a reproduction of the
paper's complete AI Scientist system. The model substitution, provider adapter,
unreported original sampling details, retrospective labels, possible training-data
contamination, and mixed-version proxy clues prevent an exact reproduction claim.
Agreement with a conference decision is not equivalent to factual correctness,
reproducibility, novelty, or scientific value.

## Acknowledgements

The protocol and expanded NeurIPS review form are adapted from SakanaAI's
[AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) implementation at
commit `6e8260925d17e1a0f6509751c19a9e1a481035b2`, released under Apache-2.0.
The original Nature article and Supplementary Information remain the primary
methodological sources. This repository is not affiliated with Sakana AI,
Nature, ICLR, NeurIPS, or DeepSeek.

Repository maintainer: [@jiadizhunine](https://github.com/jiadizhunine).

## License

Licensed under the [Apache License 2.0](LICENSE). Third-party papers and datasets
retain their original rights and are not redistributed here.
