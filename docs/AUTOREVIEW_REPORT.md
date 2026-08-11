# AutoReviewer Reproduction Report

## Executive summary

This study evaluates a DeepSeek V4 Flash implementation of the AutoReviewer
component from *Towards end-to-end automation of AI research* on a fixed ICLR
2026 cohort of 200 papers: 78 final Accept and 122 explicit Reject decisions.

Two completed runs are reported. The strict run uses initial-submission text for
both classes and removes identity and decision-status clues. The Nature-aligned
mixed run uses official camera-ready text for accepted papers and initial text for
rejected papers while also changing the prompt and DeepSeek request policy. The
two runs therefore describe different operating conditions; they do not isolate
the effect of manuscript revision.

## Experimental conditions

| Component | Strict all-initial | Nature-aligned mixed-version |
|---|---|---|
| Paper IDs and labels | Same B001–B200; 78 Accept / 122 Reject | Same B001–B200; 78 Accept / 122 Reject |
| Accept input | ProReviewer initial-submission Markdown | Official ICLR 2026 proceedings PDF, PyMuPDF page text |
| Reject input | ProReviewer initial-submission Markdown | ProReviewer initial-submission Markdown |
| Identity and lifecycle clues | Redacted and leakage-scanned | Retained when visible in manuscript text |
| Format by class | Both Markdown-derived text | Accept PDF plain text; Reject Markdown |
| Reviewer prompt | Strict local JSON schema and isolation rules | One-sentence Nature base prompt plus full frozen NeurIPS form |
| Model | `deepseek-v4-flash` | `deepseek-v4-flash` |
| Reviewer topology | Five independent reviewers + one Area Chair | Five independent reviewers + one Area Chair |
| Inference request | Thinking enabled; `reasoning_effort=max` | Thinking disabled; `temperature=0.75`; no seed |
| Max output / attempts | 16,384 tokens / 3 attempts | 16,384 tokens / 3 attempts |
| Model tools | None | None |
| Final decision | Raw Area Chair decision | Raw Area Chair decision |
| Numeric result view | Raw Area Chair fields | Rounded arithmetic mean of five reviewers |

The Nature paper confirms the five-review ensemble, Area-Chair aggregation, base
prompt, no few-shot examples, no Reflexion, and no VLM in the selected final
condition. `temperature=0.75`, the expanded form text, and numeric mean overwrite
come from the authors' frozen public implementation or this provider adapter;
they are not all explicitly declared in the paper.

## Results

| Metric | Strict all-initial | Nature-aligned mixed-version | Mixed − strict paired delta (95% CI) |
|---|---:|---:|---:|
| Balanced accuracy | 0.537 | 0.597 | +0.059 [−0.012, +0.129] |
| Accuracy | 0.585 | 0.525 | −0.060 [−0.130, +0.010] |
| F1 (Accept) | 0.376 | 0.603 | +0.227 [+0.129, +0.328] |
| AUROC | 0.586 | 0.784 | +0.198 [+0.129, +0.269] |
| FPR | 0.246 | 0.730 | +0.484 [+0.393, +0.574] |
| FNR | 0.679 | 0.077 | −0.603 [−0.705, −0.500] |

Paired differences use 5,000 paper-level percentile bootstrap replicates,
stratified by ground truth, with seed 2026. Because the protocols and inputs
changed together, these deltas are descriptive rather than causal.

### Strict all-initial

Confusion matrix: TN=92, FP=30, FN=53, TP=25. The system predicted 55 Accept
and 145 Reject. Its principal failure was rejecting accepted papers: FNR=0.679.

![Strict all-initial table](../assets/table1a_strict_initial.png)

### Nature-aligned mixed-version

Confusion matrix: TN=33, FP=89, FN=6, TP=72. The system predicted 161 Accept
and 39 Reject. AUROC increased, but the final binary decision became strongly
Accept-leaning: FPR=0.730.

![Nature-aligned mixed-version table](../assets/table1b_nature_mixed.png)

## Human and baseline rows

The same-cohort ICLR 2026 human row is a rating proxy constructed from 775 human
ratings, with 3–5 reviews per paper. A paper-level mean rating greater than 5 is
treated as Accept; an exact mean of 5 is treated as Reject; the continuous mean
rating is used for AUROC. Against the final conference decision, this proxy gives:

| Balanced accuracy | Accuracy | F1 | AUROC | FPR | FNR |
|---:|---:|---:|---:|---:|---:|
| 0.777 | 0.815 | 0.718 | 0.874 | 0.049 | 0.397 |

This is not an independent human-versus-human consistency experiment. The source
snapshot contains ratings but no independent binary decision from each reviewer
or Area Chair. Forty-one papers have a mean rating exactly equal to 5, so the tie
rule materially affects classification.

The published Nature reference rows are external comparisons:

- `Always reject (ICLR 2025)`: 0.50 / 0.56 / 0.00 / 0.50 / 0.00 / 1.00.
- `AutoReviewer (ICLR 2025)`: 0.66±0.03 / 0.63±0.09 / 0.67±0.09 /
  0.65±0.10 / 0.52±0.10 / 0.17±0.07.
- `Human (NeurIPS 2021)`: 0.66 / 0.73 / 0.49 / 0.65 / 0.17 / 0.52.

The NeurIPS human row and ICLR AutoReviewer row come from different conferences,
years, paper pools, and evaluation structures. The Nature Methods explicitly
acknowledge the distribution shift and state that this comparison is not exact.
The absence of a reported interval on the human row does not mean the estimate
has no uncertainty.

## API usage and cost

### Auditable formal-run records

| Run | Successful responses | Application attempts | Recorded tokens | Estimated cost |
|---|---:|---:|---:|---:|
| Strict all-initial | 1,200 | 1,212 | 29,178,389 successful-response tokens | USD 4.61247628 lower bound |
| Nature-aligned mixed | 1,200 | 1,200 | 29,703,106 | USD 4.214517048 |

The strict estimate excludes usage from failed attempts because those responses
did not persist usage records. The mixed run had no application-level retries.

### Provider dashboard

![DeepSeek dashboard usage](../assets/deepseek-api-usage.png)

The dashboard screenshot covers the previous 30 days for the key alias
`Reviewer`: CNY 65.48, 2,484 API requests, and 60,964,615 tokens. It is a useful
billing cross-check but is not identical to the formal-run sum because it may
include smoke tests, retries, or other calls under the same alias. The screenshot
does not contain the API-key value.

## Input leakage and interpretation

The mixed-version condition is intentionally closer to the manuscript-version
policy reported by Nature, but it exposes label-correlated proxies:

- accepted papers use final proceedings PDFs and rejected papers use initial text;
- accepted and rejected inputs have different extraction formats;
- camera-ready text may contain authors, affiliations, conference markers, titles,
  and other lifecycle clues;
- these clues are correlated with the outcome by construction.

Nature reports processing raw PDF text and does not report a redaction step. Its
public benchmark code also extracts PDF text without removing visible title,
author, affiliation, or publication-status strings. Therefore neither Nature's
original mixed-version experiment nor this reproduction should be interpreted as
a strictly blinded scientific-quality test.

## Integrity controls

- Prediction bundles were generated without access to the private labels.
- Predictions were frozen and SHA-256 committed before label joining.
- Each run contains 1,000 reviewer responses and 200 Area-Chair responses.
- The mixed run's 1,200 raw responses all parse to their stored structured objects.
- The raw Area-Chair decision equals the final and frozen decision for all papers.
- Paper input text is represented by SHA-256 rather than redistributed text.
- The formal review client exposes no browser, search, RAG, or tool call.

See each run's `INDEPENDENT_AUDIT.md`, `run_manifest.json`,
`frozen_predictions.json`, and `evaluation.json` under `results/`.

## Conclusion

DeepSeek V4 Flash did not show stable, human-equivalent peer-review performance.
The strict run showed strong Reject bias. The mixed run improved ranking and
Accept recall but produced a very high false-positive rate. The large behavior
change demonstrates sensitivity to prompt and input conditions, not a validated
camera-ready effect. The system is suitable as a research prototype or structured
feedback generator, not as an autonomous acceptance or rejection authority.

## Primary sources

- [Nature article and Methods](https://www.nature.com/articles/s41586-026-10265-5)
- [Nature Supplementary Information](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10265-5/MediaObjects/41586_2026_10265_MOESM1_ESM.pdf)
- [SakanaAI AI-Scientist-v2 frozen reviewer implementation](https://github.com/SakanaAI/AI-Scientist-v2/blob/6e8260925d17e1a0f6509751c19a9e1a481035b2/ai_scientist/perform_llm_review.py)
- [UKPLab ProReviewer Dataset](https://huggingface.co/datasets/UKPLab/ProReviewer-Dataset)
- [ICLR 2026 proceedings](https://proceedings.iclr.cc/paper_files/paper/2026)
