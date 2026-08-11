<div align="center">

**English** | [简体中文](./AUTOREVIEW_REPORT.md)

</div>

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
| Balanced accuracy | 0.54 ± 0.06 | 0.60 ± 0.05 | +0.06 ± 0.07 |
| Accuracy | 0.59 ± 0.06 | 0.53 ± 0.05 | −0.06 ± 0.07 |
| F1 (Accept) | 0.38 ± 0.10 | 0.60 ± 0.04 | +0.23 ± 0.10 |
| AUROC | 0.59 ± 0.08 | 0.78 ± 0.06 | +0.20 ± 0.07 |
| FPR | 0.25 ± 0.07 | 0.73 ± 0.08 | +0.48 ± 0.09 |
| FNR | 0.68 ± 0.10 | 0.08 ± 0.06 | −0.60 ± 0.10 |

Paired differences use 5,000 paper-level percentile bootstrap replicates,
stratified by ground truth, with seed 2026. “±” is half the width of the
corresponding 95% bootstrap interval; the exact asymmetric bounds remain in the
evaluation JSON. Because the protocols and inputs changed together, these deltas
are descriptive rather than causal.

### Strict all-initial

Confusion matrix: TN=92, FP=30, FN=53, TP=25. The system predicted 55 Accept
and 145 Reject. Its principal failure was rejecting accepted papers: FNR=0.68.

![Strict all-initial table](../assets/table1a_strict_initial.png)

### Nature-aligned mixed-version

Confusion matrix: TN=33, FP=89, FN=6, TP=72. The system predicted 161 Accept
and 39 Reject. AUROC increased, but the final binary decision became strongly
Accept-leaning: FPR=0.73.

![Nature-aligned mixed-version table](../assets/table1b_nature_mixed.png)

## Human and baseline rows

The same-cohort ICLR 2026 human row is a rating proxy constructed from 775 human
ratings, with 3–5 reviews per paper. A paper-level mean rating greater than 5 is
treated as Accept; an exact mean of 5 is treated as Reject; the continuous mean
rating is used for AUROC. Against the final conference decision, this proxy gives:

| Balanced accuracy | Accuracy | F1 | AUROC | FPR | FNR |
|---:|---:|---:|---:|---:|---:|
| 0.78 ± 0.06 | 0.82 ± 0.05 | 0.72 ± 0.09 | 0.87 ± 0.05 | 0.05 ± 0.04 | 0.40 ± 0.11 |

This is not an independent human-versus-human consistency experiment. The source
snapshot contains ratings but no independent binary decision from each reviewer
or Area Chair. Forty-one papers have a mean rating exactly equal to 5, so the tie
rule materially affects classification.

The published Nature reference rows are external comparisons:

- `Always reject (ICLR 2025)`: 0.50 / 0.56 / 0.00 / 0.50 / 0.00 / 1.00.
- `AutoReviewer (ICLR 2025)`: 0.66±0.03 / 0.63±0.09 / 0.67±0.09 /
  0.65±0.10 / 0.52±0.10 / 0.17±0.07.
- `Human (NeurIPS 2021)`: 0.66 / 0.73 / 0.49 / 0.65 / 0.17 / 0.52.

### Why the Nature NeurIPS 2021 Human row is not a matched ICLR 2025 comparison

Nature Table 1 places a NeurIPS 2021 human-consistency experiment beside its
ICLR 2025 AutoReviewer result. The metric names are the same, but the rows do
not share papers, year, venue, review assignment, or label-generation process.
The Nature Methods explicitly acknowledge the distribution shift and state that
the comparison is not exact; the authors used it as the only available modern
human-consistency reference.

The Human row can therefore give external context, but it is not evidence of a
same-task, head-to-head human-versus-AI comparison. Similar point estimates do
not establish human-level reviewing. Statistical tests describe uncertainty
within the respective samples; they cannot remove the design mismatch across
venues, years, and paper pools. The absence of a reported interval on the Human
row does not mean the estimate has no uncertainty.

## How the original Nature AutoReviewer ran

The paper's formal AutoReviewer used <code>o4-mini</code> as the Reviewer. It
supplied the visible text of a manuscript PDF, a one-sentence base role prompt,
and a detailed NeurIPS review form. Each paper received five independently
sampled structured reviews. The same model then acted as an Area Chair,
aggregated those reviews, and produced a meta-review plus a binary Accept/Reject
decision. That decision was evaluated against the final ICLR conference decision.

The selected final condition was the base prompt plus a five-review ensemble,
without VLM, few-shot examples, or Reflexion. The paper does not fully publish
every sampling detail, including the final temperature, seed, continuous AUROC
score, and every failure-handling rule; implementation choices in public code do
not automatically establish the exact paper configuration. The AutoReviewer
itself was not reported to use a browser, search, RAG, or literature-retrieval
tool. The wider AI Scientist system used web and literature tools during idea and
citation work, which is a separate component.

The paper used original submissions for rejected papers and camera-ready copies
for accepted papers. It reports raw PDF-text processing and no redaction of
titles, authors, affiliations, or publication headers. Version and visible-text
proxies may therefore affect the result; this was not a strictly blinded test of
scientific quality.

## What the workshop-paper evidence can and cannot show

The paper also describes three AI-generated manuscripts submitted to the ICLR
2025 ICBINB workshop. One received scores of 6, 7, and 6 and cleared the
workshop acceptance threshold; the other two did not. The authors manually
screened candidate outputs and checked code and formatting before submission.
They also distinguish the workshop's 70% acceptance rate from the 32% rate of
the ICLR main conference and state that none of the three met their internal
main-conference bar.

This is real but narrow external human-review evidence: in one successful case,
an AI-generated manuscript passed review in a particular workshop. It does not
by itself establish reliable main-conference-quality output, fully autonomous
research, or a general ability to judge scientific quality. The paper's broader
scaling claims rely mainly on the Automated Reviewer; any calibration or
input-clue limitations in that reviewer carry into those trends.

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
include smoke tests, retries, or other calls under the same alias.

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
- [AI Scientist ICLR 2025 Workshop Experiment](https://github.com/SakanaAI/AI-Scientist-ICLR2025-Workshop-Experiment)
- [UKPLab ProReviewer Dataset](https://huggingface.co/datasets/UKPLab/ProReviewer-Dataset)
- [ICLR 2026 proceedings](https://proceedings.iclr.cc/paper_files/paper/2026)
