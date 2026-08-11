<div align="center">

**English** | [简体中文](./NATURE_AUTOREVIEWER_AUDIT.md)

</div>

# Nature AutoReviewer: protocol alignment and result interpretation

## Bottom line

`nature-si-a3-base-v1` is a **Nature-aligned DeepSeek adapter**. It uses the
Supplementary Information as the primary specification, fills in unexpanded
details from a pinned public implementation, and records every DeepSeek-specific
choice separately. It reproduces the central topology: five independent
Reviewers, one Area Chair, a NeurIPS-style structured form, and an Area-Chair
binary decision.

It is not a parameter-for-parameter reproduction of Nature's final experiment,
nor a mechanical copy of every public-code branch. Nature used `o4-mini` and PDF
text. This project uses `deepseek-v4-flash`; in the mixed condition, Accept
papers are extracted from PDFs while Reject papers are initial-submission
Markdown. The paper does not fully specify the final temperature, seed,
continuous AUROC score, failure policy, or provider sampling interface. Some
public-code details also differ from the ordering displayed in the supplement.

The accurate description is: **a DeepSeek reproduction aligned to the Nature
AutoReviewer core workflow**. Alignment does not establish numerical equivalence
to the paper or an exact reproduction of every reported result.

This document also explains why the published results require cautious
interpretation. These are methodological and evidential limits, not an
allegation of research misconduct.

## Evidence hierarchy

The project uses this order of authority:

1. **Article and Supplementary Information** define the formal method and final
   condition the authors report.
2. **Pinned public code** supplies the full form, output scaffold, and other
   clues that the paper does not print verbatim; it does not automatically
   override the paper.
3. **DeepSeek adapter choices** are necessary because the provider and model
   differ. They are disclosed rather than presented as Nature parameters.

The run manifest consequently separates `paper_declared`, `public_code_adapter`,
and `deepseek_adapter_choice_not_reported_by_paper`, and binds prompts and the
protocol to SHA-256 fingerprints.

## What the original Nature AutoReviewer did

The AutoReviewer is one component of the complete AI Scientist, not the whole
system. The complete system may use Semantic Scholar and web tools for
**ideation and citations**. The AutoReviewer itself is described as reviewing
manuscript content and does not report browser, search, RAG, or literature
retrieval tools.

The reported pipeline is:

1. `o4-mini` reads manuscript-PDF text with a base role prompt and NeurIPS
   review form, then returns a structured review.
2. Five reviews are independently generated for the same paper.
3. The same model acts as Area Chair, reads the five reviews, and returns a
   meta-review plus an `Accept` / `Reject` decision.
4. The decision is retrospectively compared with final ICLR conference
   decisions.

The selected condition was the base prompt plus a five-review ensemble, without
VLM, few-shot examples, or Reflexion. The Reviewer base system prompt is:

```text
You are an AI researcher who is reviewing a paper that was submitted to a prestigious ML venue.
```

The Supplementary Information also shows an Area-Chair instruction to aggregate
the reviewers, find consensus, and respect their opinions.

## Parameter-by-parameter comparison

| Item | Explicit in the Nature paper / supplement | Clue from pinned public code | This project's Nature-aligned mixed condition | Interpretation |
|---|---|---|---|---|
| Reviewer model | `o4-mini` | public implementation is not a complete proof of final service configuration | `deepseek-v4-flash` | **Different model; not an o4-mini numerical replication** |
| Manuscript source | both classes are described as raw PDF text; Reject = original, Accept = camera-ready | benchmark retrieves OpenReview PDFs | Accept = official ICLR 2026 proceedings PDF + PyMuPDF; Reject = pinned ProReviewer initial Markdown | **Version policy is close; class-specific input format differs** |
| Visible clues | no reported redaction of title, author, affiliation, header, or status | benchmark/text loader does not remove visible text | visible extracted-text clues retained | **Close to a non-blinded setting, not proof of identical per-paper clues** |
| Reviewer base prompt | one role sentence | some code paths add caution / rejection wording | exact Supplementary-Information sentence, without extra text | **Paper first; not every code branch copied** |
| Review form | detailed NeurIPS guidelines, structured fields, no few-shot | complete form, field ranges, output template | frozen form, UTF-8 SHA-256 `41493738…3ffd2` | **Code-aligned form; the paper does not print it verbatim** |
| Output | structured JSON; visible reasoning is not a paper requirement | `THOUGHT` followed by `REVIEW JSON` | same scaffold; parser also accepts direct valid JSON | **Code alignment, not a claim that Nature required saved reasoning** |
| Reviewer count | five independent reviews | five-review ensemble | five independent HTTP Reviewer requests per paper | **Core topology aligned; provider sampling is unpublished** |
| Area Chair | same model aggregates five reviews into meta-review | explicit prompt and construction logic | Supplementary-Information order: five reviews, then full form | **Paper-first; differs from some code ordering** |
| Final binary decision | Area-Chair `Decision` | meta decision retained | raw Area-Chair `Decision` is the prediction | **Aligned** |
| Numeric scores | no statement that Area-Chair scores are overwritten | code overwrites numeric fields with review means while retaining meta text/decision | retains Area-Chair text/decision; numeric view uses rounded five-review means | **Public-code compatibility, not paper-confirmed final setting** |
| Temperature / seed | final temperature and seed not reported | five-sample path includes `temperature=0.75` | `temperature=0.75`; no seed | **Temperature is a code clue, not paper-confirmed** |
| DeepSeek thinking | not applicable | not applicable | thinking explicitly disabled; no `reasoning_effort` | **Provider adapter, not a Nature parameter** |
| Output cap / retries / parallelism | not fully reported | legacy fallback behavior is not a paper specification | 16,384 output tokens; three attempts maximum; complete five-review ensemble required; parallelism five | **Engineering choices, not Nature-alignment claims** |
| Tools / retrieval | Reviewer does no explicit literature search | no reviewer tool interface | no browser, search, RAG, URL fetch, or model tools | **Aligned at Reviewer layer; distinct from the full AI Scientist** |
| VLM / few-shot / Reflexion | none in final condition | corresponding ablation paths exist | none used | **Aligned** |
| Statistics | bootstrap CIs reported, but not all resampling details fixed | code is not a complete statistics specification | 5,000 paper-level, class-stratified percentile bootstrap; seed 2026 | **Reproducible project choice, not a parameter-for-parameter copy** |
| AUROC score | final continuous score is not fully specified | historical binary path does not establish final paper definition | mean raw `Overall` across five reviewers | **Project operationalization; not claimed identical to Nature** |

### Is it aligned with the original code?

**The core is aligned; the complete configuration is “paper first + code
completion + DeepSeek adapter”, not 100% code-aligned.**

- **Explicitly shared by paper and this project:** five independent reviews,
  one Area Chair, NeurIPS-style structured review, base prompt, no
  VLM/few-shot/Reflexion, an Area-Chair final decision, and no external Reviewer
  retrieval tools.
- **Completed from pinned public code:** full form text, the `THOUGHT`/JSON
  scaffold, `temperature=0.75`, and numeric mean overwrite.
- **Not aligned or not claimable as aligned:** `o4-mini` versus DeepSeek,
  Reject Markdown, DeepSeek thinking policy, HTTP concurrency/retry/output cap,
  seed, final AUROC score, and unreported Nature service-side sampling details.

The supplement and public implementation do not form one unique, fully
executable specification. For example, the supplement displays one Area-Chair
input order while some public code constructs messages differently; the paper
does not make the full form or temperature a final-run specification. This
project therefore prioritizes the Supplementary Information and uses code as
traceable supplementary evidence.

## Why the Nature results need cautious interpretation

None of the following shows the results are necessarily false. They show a
substantial gap between the reported evidence and stronger claims such as
“reliably human-equivalent reviewing” or “generally reliable end-to-end
automated science”.

| Observed boundary | Why it matters | Known mitigation or explanation | What would resolve it |
|---|---|---|---|
| `Human (NeurIPS 2021)` beside `AutoReviewer (ICLR 2025)` | no shared papers, year, conference, reviewer assignment, or label construction; common metric names do not create a paired human-versus-AI match | paper acknowledges the distribution shift and says it was the only available modern human-consistency comparator | parallel model and independent-human committees on the same manuscripts, metrics frozen in advance |
| Accept = camera-ready; Reject = original submission | version is label-related; revision, authorship, affiliation, headers, and venue status may be proxy signals | supplement acknowledges the bias; revisions may also genuinely improve papers | same-version, same-format, blinded/unblinded crossed conditions |
| no reported redaction of visible PDF text | a model may learn status/version proxies rather than scientific quality | direct PDF extraction is transparent, but does not eliminate confounding | per-paper redaction audit and raw-versus-redacted comparison |
| retrospective agreement with conference decisions | a conference decision is not a truth label for correctness, reproducibility, novelty, or long-term value | it is a large-scale real-world label | freeze predictions before outcomes and add factual/reproducibility evaluation |
| one successful paper among three workshop submissions | very small sample; candidate selection and code/format checks were manual; workshop acceptance was higher than main-conference acceptance | paper reports 1/3 and says it does not yet meet top-tier or even workshop standards consistently | preregistered repeated rounds, full candidate sets, consistent thresholds, independent review, external replications |
| downstream model/compute-quality trends measured by the same AutoReviewer | evaluator bias or calibration error can propagate into downstream curves | ensemble reduces random sampling variance, not necessarily systematic bias | cross-check with independent humans, other models, and blinded settings |
| key implementation/statistical details not fully frozen in paper | temperature, seed, retry, continuous AUROC score, and paper-code differences make exact replication/attribution difficult | paper, supplement, and code provide substantial but incomplete information | release final manifests, request parameters, recomputable statistics, de-identified predictions |
| 2025 set after knowledge cutoff | calendar split is a useful contamination check, not a direct training-data audit | paper reports a post-cutoff performance decline | timestamped data exclusion, training-data evidence, or a genuinely prospective cohort |

The supplement also uses both “mean class recall” and “randomly downsample the
larger class” language for balanced accuracy. Under class imbalance they are not
necessarily identical. The safest practice is to release an exact formula,
fixed implementation, and resampling script—not just a metric name.

### What the workshop evidence does—and does not—show

The strong factual claim is limited: three AI-generated manuscripts were sent to
the ICLR 2025 ICBINB workshop; one received scores of 6, 7, and 6, then was
withdrawn under a pre-established protocol. Reviewers knew that some papers were
AI generated but not which. The paper also says candidates were manually filtered
before submission, only one of three reached the workshop bar, and the authors'
team judged none of the three at the main-ICLR standard.

This is valuable but narrow external human-review evidence: **in a specific
workshop, topic, and selection process, one AI-generated paper achieved scores
above the acceptance threshold.** It does not establish reliable main-conference
output or generally reliable end-to-end automated science. The article's own
limitations make that distinction.

The broader narrative relies mainly on AutoReviewer scale metrics, while the
AutoReviewer's human comparison is not a matched same-cohort experiment. The
evidence supports “an interesting system demonstration with limited external
human evidence”, not a matched-baseline proof of general research quality.

## What this project's two tables can and cannot answer

### They can answer

- On the same 200 ICLR 2026 papers, strict all-initial and Nature-aligned mixed
  conditions lead to substantially different DeepSeek behavior.
- In the mixed condition, AUROC is `0.78 ± 0.06` but binary-decision FPR is
  `0.73 ± 0.08`; better ranking does not make it suitable for autonomous
  acceptance decisions.
- In the strict, redacted, all-initial condition, the model is Reject-leaning:
  FNR is `0.68 ± 0.10`.

### They cannot answer

- The table difference is not a causal camera-ready effect: version, format,
  prompt, thinking, numeric aggregation, and visible clues change together.
- The Nature-aligned mixed condition is not a parameter-exact reproduction of
  Nature's `o4-mini` result.
- Agreement with conference decisions does not establish correctness, novelty,
  reproducibility, or human-equivalent review.
- A single workshop success does not establish stable end-to-end research
  automation.

The most informative follow-up is a preregistered crossed design: fix model,
prompt, extraction format, and statistics; vary only manuscript version and
redaction; then freeze predictions on papers whose decisions are not yet public.
That separates version from label-related clues and is more informative than a
retrospective decision-agreement test.

## Reproducible artefacts

- Protocol definition: `src/deepseek_autoreviewer/nature_protocol.py`.
- Each Nature-aligned `run_manifest.json` contains the protocol, prompt hashes,
  effective request, and the three evidence classes.
- Each `review_bundle.json` preserves five Reviewer calls, the Area Chair,
  raw response, structured result, usage, and input-text hash; labels are joined
  only after predictions are frozen.
- Numbers, cost, and paired comparisons are in the
  [full AutoReviewer report](./AUTOREVIEW_REPORT.en.md); the shorter explanation
  is in the [plain-language guide](./RESULTS_GUIDE.en.md).

## Sources

- [Nature article and Methods](https://www.nature.com/articles/s41586-026-10265-5)
- [Nature Supplementary Information, section A.3](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10265-5/MediaObjects/41586_2026_10265_MOESM1_ESM.pdf)
- [Pinned SakanaAI AI-Scientist-v2 reviewer implementation](https://github.com/SakanaAI/AI-Scientist-v2/blob/6e8260925d17e1a0f6509751c19a9e1a481035b2/ai_scientist/perform_llm_review.py)
- [Pinned original SakanaAI ICLR benchmark script](https://github.com/SakanaAI/AI-Scientist/blob/d6576a38237c03205ba5ae0d4cc5aa7eae038577/review_iclr_bench/iclr_analysis.py)
- [AI Scientist ICLR 2025 Workshop Experiment](https://github.com/SakanaAI/AI-Scientist-ICLR2025-Workshop-Experiment)
