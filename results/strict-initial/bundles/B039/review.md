# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B039.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 3, 'Reject': 2}
- Estimated API cost: **$0.017785**

## Final Meta-review

The paper proposes IterSurvey, an automatic literature survey generation framework that replaces one-shot retrieval-and-outline pipelines with recurrent outline generation. A planning agent iteratively retrieves papers, distills them into structured paper cards (contributions, methods, findings), updates the outline with stability checks and keyword expansion, and stops based on completeness. Section drafting is guided by paper cards, followed by a global review-and-refine loop and automatic figure/table integration. The paper also introduces Survey-Arena, a pairwise benchmark ranking machine-generated surveys against human-written surveys. Experiments on 20 established and 8 survey-lacking topics show improved content and citation quality over baselines, and human evaluation and ablations support the main contributions.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 2.600 | 0.490 | 2-3 |
| Clarity | 3 | 2.600 | 0.490 | 2-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 2.600 | 0.490 | 2-3 |
| Presentation | 3 | 2.600 | 0.490 | 2-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 5.200 | 0.980 | 4-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Recurrent outline generation is a well-motivated shift from one-shot planning, mirroring human iterative reading behavior.
- Paper cards provide fine-grained, structured evidence that improves citation recall and grounding, as supported by ablations.
- Survey-Arena is a valuable benchmark contribution: pairwise comparisons against human surveys are more reliable than absolute scoring, and meta-evaluation shows better correlation with citation counts.
- Comprehensive evaluation protocol: multiple baselines, automatic multi-dimension scoring with three judge LLMs, citation quality via NLI, human pairwise evaluation, ablation study, and generalization test on survey-lacking topics.
- The review-and-refine loop and figure/table integration add interesting extensions to purely textual generation.

### Weaknesses

- Implementation details are underspecified: exact definitions of outline update, keyword expansion, stopping functions, similarity threshold tau, prompts, and retrieval settings are missing or redacted, hindering reproducibility.
- Reported improvements over baselines are small (e.g., content score 4.75 vs 4.66) with overlapping standard deviations; no effect sizes, p-values, or multiple-comparison corrections are provided.
- Evaluation relies heavily on LLM-as-a-judge; Survey-Arena lacks human validation, and citation counts are a weak proxy for survey quality (Spearman rho=0.410), so the benchmark's validity is not fully established.
- Human evaluation is limited to 7 experts and compares only against AutoSurvey and SurveyForge, not human-written surveys; no significance tests or confidence intervals for preference percentages are reported.
- The ablation study is limited to 5 topics, and there are inconsistencies: adding recurrent outline generation alone reduces citation recall (0.67→0.59), and full model scores differ between main and ablation tables (4.75 vs 4.82, recall 0.70 vs 0.77).
- Figure/table integration is claimed as a contribution but is not separately evaluated, and no computational cost or latency analysis is provided for the iterative process.

### Questions

- What are the exact definitions and values of the similarity function Sim, threshold tau, keyword expansion f, and stopping rule h? How sensitive are results to these hyperparameters?
- Why do the full IterSurvey scores differ between the main experiments (Table 1) and ablation (Table 5)? What explains the non-monotonic citation recall in the ablation?
- Are the Survey-Arena pairwise rankings validated against human judgments, and how do you control for LLM judge biases (e.g., position, length, formatting, self-preference)?
- What are the exact p-values and effect sizes for the main comparisons, and do they survive multiple-comparison correction?
- How were the 20 and 8 evaluation topics selected, and what criteria were used to designate them as survey-lacking?
- What is the total computational cost of IterSurvey compared to baselines in terms of API calls, tokens, and wall-clock time?
- Are the generated figures and tables factually grounded in the cited papers, and what quality checks were applied?
- Why is SurveyX excluded from the main comparison, and could its inclusion change the conclusions?

### Limitations

- The implementation relies on a large retrieval database (680K arXiv CS papers) and multiple LLM calls, but no cost/latency analysis is provided, limiting real-world usability assessment.
- The scope is limited to English-language arXiv computer science papers, especially LLM-related topics, so generalization to other domains or non-arXiv literature is unknown.
- Paper-card distillation may introduce errors that propagate; no fact-checking mechanism beyond citation precision/recall is provided.
- Survey-Arena includes only 10 topics and 5 human surveys each, which may not capture the diversity of survey-writing styles.
- No mechanism is proposed for updating surveys over time or adapting to user-specific goals.
- The system may inherit biases from the underlying LLM and retrieval database, and potential societal risks are not thoroughly discussed.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 79,660
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 75,564
- Completion tokens: 25,694
- Reasoning tokens reported: 18,853
- Total tokens: 105,354
- Estimated total: $0.01778475

Full individual reviews and raw JSON responses are in `review_bundle.json`.
