# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B185.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.060423**

## Final Meta-review

The paper introduces ExpertLongBench, a multi-disciplinary benchmark for evaluating LLMs on expert-level long-form generation tasks. It comprises 11 tasks across 9 domains (law, education, health, chemistry, biology, finance, cybersecurity, materials science) with 1050 samples, featuring inputs up to 200K tokens and outputs exceeding 5K tokens. The key methodological contribution is CLEAR (CheckList-based Expert-level Assessment with Rubric), an evaluation framework that uses expert-designed rubrics to extract checklists from both model outputs and reference answers, then performs item-level semantic comparison to compute precision, recall, and F1 scores. The authors benchmark 15 LLMs (open-weight and proprietary) and find that the best model (Gemini-2.5-Pro) achieves only 33.4 F1, indicating significant room for improvement. They also validate that open-weight models (Qwen2.5-72B) can serve as effective checklist mappers and evaluators, enabling reproducible and low-cost evaluation. Additional analyses include skill decomposition, reasoning difficulty assessment, and comparison with existing benchmarks (MMLU, GPQA, LMArena) showing divergent model rankings.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.800 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.400 | 0.490 | 3-4 |
| Significance | 4 | 3.800 | 0.400 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.400 | 0.490 | 3-4 |
| Contribution | 4 | 3.800 | 0.400 | 3-4 |
| Overall | 7 | 7.200 | 0.400 | 7-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses a clear and important gap: existing expert benchmarks (MMLU, GPQA) use short-form QA, while real expert work involves long-form generation. The tasks are realistic, end-to-end, and span diverse domains.
- Expert-designed rubrics are a significant contribution, providing fine-grained, domain-specific evaluation criteria validated by professionals across multiple disciplines.
- CLEAR provides a grounded, item-level evaluation approach that goes beyond holistic scoring, with careful validation of pipeline components (checklist mapper, judge) including human-LLM agreement studies (91-92% accuracy).
- Comprehensive benchmarking across 15 models from diverse families (open-weight and proprietary) with detailed task-wise results and error analysis.
- The finding that models achieve high checklist coverage but low F1 (i.e., producing content that appears expert-aligned but is incorrect) is an important and actionable insight, with safety implications for high-stakes domains.
- Demonstrates that open-weight models can substitute for proprietary models in evaluation components, enhancing reproducibility, accessibility, and cost-effectiveness.
- Skill decomposition and difficulty-level analysis provide deeper understanding of model strengths and weaknesses beyond aggregate scores.
- Careful consideration of data licensing, privacy (private test sets), and contamination concerns, with public/private data splits.
- Detailed appendices provide complete task descriptions, rubrics, prompts, and experimental settings for reproducibility.

### Weaknesses

- Reliance on LLM-based evaluation (GPT-4o as judge, Qwen2.5-72B as mapper) introduces potential biases; human validation is limited to a small subset of tasks (250 instances across 2 tasks).
- Sample size per task (100) is relatively small, which may limit statistical power for fine-grained model comparisons and generalizability.
- Several tasks have relatively short reference outputs (e.g., T3: 125 tokens, T4: 60 tokens), which may not fully represent the 'long-form' generation claim.
- The finding that providing ground-truth rubrics dramatically improves performance (T2: F1 from 6.2 to 32.5) raises the question of whether the benchmark measures prompt adherence rather than inherent expert capability.
- Four tasks (T2, T5, T9, T10) use private data, limiting full reproducibility for the community.
- The RAG experiment is limited to two tasks and one model (GPT-5), so the conclusion that RAG doesn't help may not generalize.
- The skill decomposition analysis relies on LLM-based annotation without human validation, which may introduce systematic biases.
- The comparison with existing benchmarks (Table 63) shows ranking divergence but lacks deep analysis of why this divergence occurs.
- Limited analysis of specific failure modes—the paper identifies high coverage/low F1 but does not deeply categorize the types of errors (e.g., hallucination vs. omission vs. format issues).

### Questions

- How is 'N/A' handled in the F1 computation? If a model outputs 'N/A' for an item where the reference has content, is that scored as incorrect? If the reference has 'N/A' and the model outputs content, how is that scored? This could significantly affect precision/recall.
- The paper shows that providing the ground-truth rubric in the prompt improves performance significantly (T2: F1 from 6.2 to 32.5). Does this suggest that the benchmark primarily measures the ability to follow explicit instructions rather than inherent domain expertise? How would results change if all models were given the full rubric?
- For the 5 tasks adapted from existing datasets, what specific value does ExpertLongBench add beyond the original datasets? Could you provide a more detailed comparison with evaluations on the original datasets?
- How robust is the checklist-based evaluation to variations in the checklist mapper model? You validated Qwen2.5-72B, but what happens if a significantly weaker or stronger mapper is used—do model rankings remain stable? What is the per-task correlation between Qwen2.5-72B and GPT-4o for evaluation?
- Have you analyzed the error propagation from the checklist mapper (Qwen2.5-72B)? Since the mapper has ~90% F1 on mapping, how does this error rate affect the downstream evaluation scores and model rankings?
- For the coverage analysis (Figure 2), have you considered that the negative correlation might be partially driven by task-specific factors (e.g., tasks with naturally higher coverage requirements) rather than a general model behavior?
- The human evaluation for CLEAR was conducted on only 2 tasks (T7, T8) with 250 instances. How representative is this of the other 9 tasks, especially the more complex ones like T1 and T2? Do you have plans to extend this?
- For tasks with short references (e.g., T3: 125 tokens, T4: 60 tokens), how do you ensure the checklist items are meaningful and not trivial? Could the low F1 scores on these tasks reflect the evaluation granularity rather than model capability?
- For the RAG experiment, only GPT-5 was used with a simple retrieval approach. Would different retrieval strategies, models, or more sophisticated agentic workflows (e.g., multi-hop retrieval, tool use) potentially change the conclusion?
- The skill decomposition analysis assigns skills and difficulty levels to checklist items using GPT-4o. What is the inter-annotator agreement between GPT-4o and human experts on these assignments?
- How sensitive are the final results to the choice of judge model (GPT-4o vs. Qwen2.5-72B)? The correlation is high (0.88) on average, but are there tasks where rankings diverge significantly?
- Did you consider evaluating models with different decoding strategies (e.g., nucleus sampling, temperature > 0) beyond greedy decoding? Would this affect the conclusions?
- For the private test sets, what specific mechanisms are in place to prevent contamination and ensure fair evaluation over time? How will you handle models that have been trained on public portions of the benchmark?
- The high coverage but low F1 finding is interesting. Could you provide a more detailed error analysis categorizing the types of errors (e.g., hallucination, partial information, wrong details, format issues) across different tasks?
- What is the correlation between model performance on ExpertLongBench and other long-context benchmarks like LongBench or L-Eval? The comparison in Appendix H focuses on short-form QA benchmarks.
- The paper mentions that LLM-generated rubrics are inferior to expert rubrics (Appendix I.2). Could you quantify this difference more concretely with examples? What specific capabilities would be needed for LLMs to approach expert-level rubric design?

### Limitations

- The benchmark is limited to English-language tasks, not covering multilingual expert applications.
- The analysis focuses on off-the-shelf LLM performance, not exploring complex prompting strategies, tool use, or agentic workflows that are increasingly common in applied research.
- The sample size per task (100) may limit the statistical power for detecting small but meaningful performance differences between closely-ranked models.
- The evaluation framework's reliance on LLM-based extraction and comparison, while validated, may not be perfectly aligned with human expert judgment in all cases.
- The benchmark covers only a small fraction of real-world expert applications despite spanning 9 domains.
- The private nature of some datasets (T2, T5, T9, T10) limits full reproducibility and community verification of results.
- The paper does not propose concrete strategies for improving model performance on these tasks, limiting its direct utility for model development.
- Potential negative societal impact: the finding that models can generate content that appears expert-aligned but is incorrect could lead to over-reliance on LLMs in high-stakes domains like law and medicine. The paper discusses this in the broader impacts section but could emphasize this risk more prominently in the main text.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 405,162
- Cache-hit prompt tokens: 0
- Cache-miss prompt tokens: 405,162
- Completion tokens: 13,214
- Reasoning tokens reported: 0
- Total tokens: 418,376
- Estimated total: $0.06042260

Full individual reviews and raw JSON responses are in `review_bundle.json`.
