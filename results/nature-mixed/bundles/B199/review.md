# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B199.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.020224**

## Final Meta-review

This paper investigates the mechanisms underlying reinforcement learning (RL) in large language models (LLMs) for reasoning tasks. The authors propose that RL training leads to an emergent hierarchical reasoning structure, where models first consolidate low-level procedural skills (e.g., arithmetic, formatting) and then shift to exploring high-level strategic planning (e.g., deduction, branching, backtracing). They introduce a functional proxy called 'Strategic Grams' (SGs) to identify planning tokens and demonstrate a consistent two-phase learning dynamic across eight LLM and VLM models. Based on this insight, they propose HICRA (Hierarchy-Aware Credit Assignment), which amplifies the advantage signal for planning tokens during policy gradient updates. Experiments on multiple math reasoning benchmarks (AIME, Math500, etc.) and multimodal benchmarks show that HICRA consistently outperforms standard GRPO and entropy-based baselines. The paper also provides a unified explanation for phenomena like 'aha moments' and 'length scaling' through the lens of strategic exploration.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.600 | 0.490 | 3-4 |
| Quality | 3 | 3.200 | 0.400 | 3-4 |
| Clarity | 3 | 3.400 | 0.490 | 3-4 |
| Significance | 3 | 3.400 | 0.490 | 3-4 |
| Soundness | 3 | 3.200 | 0.400 | 3-4 |
| Presentation | 3 | 3.400 | 0.490 | 3-4 |
| Contribution | 3 | 3.400 | 0.490 | 3-4 |
| Overall | 7 | 7.000 | 0.894 | 6-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel analytical framework: The paper provides a unified explanation for several previously puzzling RL phenomena (aha moments, length scaling, entropy dynamics) under a single 'emergent hierarchical reasoning' hypothesis, grounded in cognitive science.
- Thorough empirical analysis: The training dynamics are analyzed across 8 different models (LLMs and VLMs), with multiple metrics (relative perplexity, token entropy, semantic entropy) providing a comprehensive view.
- Well-validated methodology: The SG identification pipeline includes human annotation (86% precision vs 12% for random n-grams) and sensitivity analysis (dropping 30% of SGs doesn't change results).
- Practical algorithm: HICRA is simple, easy to implement, and shows consistent improvements over GRPO and entropy-based baselines across multiple benchmarks and model families.
- Good baseline comparisons: The paper compares against relevant baselines including entropy regularization, high-entropy advantage, and placebo HICRA, demonstrating the importance of semantic-level credit assignment.
- Clear writing and organization: The paper is well-structured, with clear takeaways and a logical flow from analysis to algorithm design.
- Honest discussion of boundary conditions: The paper acknowledges cases where HICRA fails (e.g., Llama-3.1-Instruct) and provides analysis of when the approach works and when it doesn't.

### Weaknesses

- Causal claims are correlational: The claim that the learning frontier shifts from procedural to strategic is based on correlational evidence between semantic entropy and accuracy. The paper lacks direct causal interventions to prove that strategic exploration drives performance gains.
- Limited exploration of hyperparameters: The amplification coefficient α=0.2 is fixed without sensitivity analysis. The paper doesn't explore how different α values affect performance or training dynamics.
- The SG pipeline is heuristic: While well-validated, the SG identification relies on several arbitrary hyperparameters (n-gram size, clustering algorithm, top 20% threshold). The sensitivity analysis only tests random SG removal, not systematic variations in the pipeline.
- The two-phase dynamic is not consistently observed across all models: Several models (e.g., Qwen3-4B-Instruct, VLMs) skip or have very brief procedural consolidation phase, weakening the universality of the central claim.
- Limited domain generalization: The analysis and experiments focus exclusively on mathematical reasoning. The paper doesn't demonstrate that the findings generalize to other reasoning domains (e.g., code generation, agentic tasks).
- Missing comparison with recent methods: The paper doesn't compare against more recent token-level credit assignment methods or other RL algorithms beyond GRPO variants.
- Lack of statistical significance testing: Improvements on some benchmarks are negative or negligible, and the paper does not report variance across runs or confidence intervals.
- HICRA underperforms on some models and benchmarks: On Llama-3.1-8B-Instruct, HICRA shows mixed results, and on Olympiad for Qwen3-4B-Instruct, HICRA performs worse than GRPO. The paper acknowledges this but doesn't provide a deep analysis of when and why HICRA fails.

### Questions

- How sensitive is HICRA's performance to the choice of α? Have you tried other values (e.g., 0.1, 0.5, 1.0) and how do they affect the training dynamics and final performance? Would an adaptive α that increases over training as procedural skills consolidate be more effective?
- The SG identification pipeline uses a fixed set of hyperparameters (n-gram size 3-5, top 20% cluster DF, specific clustering algorithm). How sensitive are the main findings to these choices? Have you tested variations in the clustering approach or threshold?
- For the Llama-3.1-8B case where HICRA underperforms, would a curriculum approach (start with GRPO, then switch to HICRA after procedural consolidation) help? This would directly test your two-phase theory.
- How does HICRA perform on non-mathematical reasoning tasks such as code generation or agentic tool use? The paper mentions this as future work, but providing preliminary evidence would strengthen the generalizability claims.
- The paper claims HICRA improves 'strategic exploration' but this is only shown through semantic entropy curves. Could you provide direct evidence through rollout analysis, e.g., showing that HICRA generates more diverse planning strategies or more frequent backtracing?
- What is the computational overhead of identifying planning tokens using SGs during RL training? Does this add significant latency to the training loop?
- The human annotation study shows 86% precision for SGs. What about the recall? How many actual planning tokens are missed by the SG-based approach, and could this affect the HICRA results? What was the inter-annotator agreement (e.g., Cohen's kappa)?
- The paper claims the two-phase dynamic is 'emergent' and 'consistent across models.' However, the appendix shows some models skip the procedural consolidation phase. How do you reconcile this with the claim of a universal two-phase dynamic? Could the initial phase be too short to detect rather than absent?
- For the error type analysis (Figure 3), how reliable is the GPT-4o-based classification? Did you validate this against human annotations?
- How does HICRA interact with the dynamic filtering mechanism (clip-higher) used in the experiments? Is the α amplification applied before or after the clipping?
- The paper mentions 'semantic entropy' as a better diagnostic than token entropy. Could you provide more quantitative evidence (e.g., correlation coefficients) linking semantic entropy to validation accuracy across different models and training stages?
- The paper does not report training compute or wall-clock time comparisons between HICRA and baselines. Does HICRA require additional computational overhead for SG identification or advantage computation?

### Limitations

- The analysis is limited to mathematical reasoning tasks; the generalizability to other reasoning domains (code, agents, scientific reasoning) is not validated.
- The SG identification pipeline may not transfer well to other languages or domains with different reasoning structures and strategic language patterns.
- The paper doesn't discuss potential negative societal impacts of focusing RL on 'strategic planning' tokens, which could lead to more deceptive or manipulative reasoning patterns if applied to harmful tasks.
- The two-phase learning dynamic is a post-hoc interpretation; the paper doesn't provide a mechanistic model or theoretical proof of why this should occur.
- HICRA's effectiveness depends on the quality of the SG identification, which is a heuristic process. In domains where SGs are harder to identify, the method may not be applicable.
- HICRA's effectiveness is conditional on the base model having a reasonable level of procedural competence (as acknowledged for Llama-3.1). This limits its applicability to very weak base models.
- The human annotation study for SG validation uses Amazon Mechanical Turk, which may have quality control issues. The inter-annotator agreement is described as 'substantial' but no exact kappa value is provided.
- The experiments use relatively small models (4B-8B parameters); scaling behavior to larger models is not assessed.
- The paper does not provide statistical significance tests or confidence intervals for the reported benchmark improvements, which limits the strength of the empirical claims.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 129,931
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 120,971
- Completion tokens: 11,655
- Reasoning tokens reported: 0
- Total tokens: 141,586
- Estimated total: $0.02022443

Full individual reviews and raw JSON responses are in `review_bundle.json`.
