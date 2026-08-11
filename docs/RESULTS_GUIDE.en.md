<div align="center">

**English** | [简体中文](./RESULTS_GUIDE.md)

</div>

# Read the two result tables this way first

The two tables evaluate the same 200 ICLR 2026 papers (78 Accept and 122
Reject), but they are not a camera-ready-only ablation. `0.54 ± 0.06` means a
point estimate of 0.54 and half the width of its 95% bootstrap interval. It is
not a percentage and not run-to-run variation.

| Condition | Accept input | Reject input | Redaction | Other changes made at the same time |
|---|---|---|---|---|
| Table 1a: strict all-initial | Initial-submission Markdown | Initial-submission Markdown | Identity, version, and decision clues removed | Local strict JSON protocol; DeepSeek thinking enabled |
| Table 1b: Nature-aligned mixed-version | Official camera-ready PDF text | Initial-submission Markdown | None | Nature base prompt, full NeurIPS form, thinking disabled, the public-code-derived temperature=0.75, input format, and numeric aggregation also differ |

The difference between Table 1b and Table 1a is therefore a difference between
two operating conditions. It is not an estimate of how much camera-ready
revision alone improved the model.

## What “Always reject” means

It is not a tunable parameter. It is a deliberately non-learning baseline that
returns Reject for every manuscript, regardless of content. Since this cohort has
122 Reject decisions out of 200, it produces:

| Balanced accuracy | Accuracy | F1 (Accept) | AUROC | FPR | FNR |
|---:|---:|---:|---:|---:|---:|
| 0.50 | 0.61 | 0.00 | 0.50 | 0.00 | 1.00 |

Its 0.61 accuracy merely gets the majority Reject class right; it finds no
accepted paper. This baseline prevents a superficially reasonable accuracy under
class imbalance from being mistaken for reviewing ability. A useful Reviewer
should beat it on balanced accuracy, F1, or AUROC rather than succeed by always
rejecting.

## What the ICLR 2026 Human row is

The ICLR 2026 Human row is a same-cohort rating proxy built from 775 human
ratings, with 3–5 ratings per paper. A mean score above 5 is classified as
Accept, while a score exactly equal to 5 is classified as Reject. It is useful
context for this repository's two tables, but it is **not** a consistency study
between independent human committees or a reconstruction of the final Area Chair
decision.

## How to read Nature's 2021 Human row and 2025 AI row

Nature Table 1 places `Human (NeurIPS 2021)` beside `AutoReviewer (ICLR 2025)`,
but the rows do not share papers, year, venue, review assignment, or the process
that created labels. The Nature Methods state that the comparison is not exact.
It can provide external context, but it is not a same-paper human-versus-AI
contest, and similar numbers do not establish human-level reviewing.

This repository keeps those rows in the lower half of its tables so the original
paper's references remain visible, not because they form a same-cohort ICLR 2026
comparison.

## How the original Nature AutoReviewer actually ran

1. It supplied visible manuscript-PDF text, a base role prompt, and a full
   NeurIPS review form to `o4-mini`.
2. It generated five independent structured reviews per paper.
3. The same model served as Area Chair, aggregated the five reviews, and returned
   a meta-review and binary decision.
4. It evaluated that decision against final ICLR conference decisions.

The selected final condition was the base prompt plus a five-review ensemble,
without VLM, few-shot examples, or Reflexion. The paper does not fully disclose
the final temperature, seed, continuous AUROC score, or all failure handling.
Public-code details are therefore implementation clues, not a complete
parameter-level specification of the paper.

The AutoReviewer itself was not reported to use a browser, search, RAG, or a
literature-retrieval tool. Web and literature tools used elsewhere in the full AI
Scientist system belong to the idea and citation components. The Nature study
also used initial submissions for Reject and camera-ready copies for Accept,
processed raw PDF text, and did not report redaction. Visible cues such as
version, author, affiliation, or publication headers may therefore influence the
result.

## The boundary of the workshop evidence

Nature reports three AI-generated manuscripts submitted to the ICLR 2025 ICBINB
workshop. One achieved scores of 6, 7, and 6 and cleared the workshop threshold;
the other two did not. Candidate outputs were manually screened and code and
formatting were checked before submission. The paper also distinguishes the
workshop's 70% acceptance rate from the ICLR main conference's 32% rate and says
that none of the three met the authors' internal main-conference bar.

This supports one narrow claim: in one specific workshop setting, an AI-generated
manuscript passed human review. It does not by itself establish reliable
main-conference-quality output, fully autonomous research, or general scientific
quality judgement. The broader scaling claims rely mainly on the Automated
Reviewer, whose human comparison is not a matched same-cohort experiment.

More precisely, the paper's narrative has two evidence streams: one successful
workshop paper supplies an external human-review example, while the Automated
Reviewer supplies the scalable trend metrics. The first has a narrow evidentiary
scope, and the second depends on an automated reviewer without a matched human
baseline. Together they do not independently establish stable end-to-end
automated research. It is therefore inaccurate to say that every conclusion rests
only on one paper, but reasonable to regard that paper as the most conspicuous
external human-review evidence.

## Bottom line

The cautious reading of these two tables is that DeepSeek AutoReviewer is highly
sensitive to manuscript version, text format, and protocol. Agreement metrics
against conference decisions can change, but they do not directly measure
scientific-quality judgement or establish human-level peer review.

## Sources

- [Nature article and Methods](https://www.nature.com/articles/s41586-026-10265-5)
- [Nature Supplementary Information](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10265-5/MediaObjects/41586_2026_10265_MOESM1_ESM.pdf)
- [AI Scientist ICLR 2025 Workshop Experiment](https://github.com/SakanaAI/AI-Scientist-ICLR2025-Workshop-Experiment)
- [Full AutoReviewer report](./AUTOREVIEW_REPORT.en.md)
