# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B125.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.022521**

## Final Meta-review

This paper proposes training vision-language critic models via reinforcement learning (RL) on preference-labeled data reformulated into a verifiable task, rather than the standard supervised fine-tuning (SFT) approach. The resulting model, LLaVA-Critic-R1, surprisingly emerges as both a strong critic (evaluator) and a competitive policy model (generator), improving over its base model (Qwen-2.5-VL-7B) by +5.7% on average across 26 benchmarks. Applying this approach to an existing reasoning VLM (ThinkLite-VL-7B) yields LLaVA-Critic-R1+, which further improves policy performance while maintaining critic quality. The enhanced critic ability enables effective test-time self-critique scaling, yielding +13.8% improvement on five reasoning tasks. The paper includes extensive ablations on data utilization strategies, training order, and the correlation between critic and policy abilities.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.800 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.200 | 0.400 | 3-4 |
| Significance | 4 | 3.600 | 0.490 | 3-4 |
| Soundness | 3 | 3.200 | 0.400 | 3-4 |
| Presentation | 3 | 3.200 | 0.400 | 3-4 |
| Contribution | 4 | 3.600 | 0.490 | 3-4 |
| Overall | 6 | 6.400 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel and surprising finding: RL training on critic data improves both critic and policy capabilities simultaneously, challenging the conventional separation of these roles.
- Comprehensive evaluation across 26 diverse benchmarks (perception, reasoning, chart, video, agent, reward), providing strong empirical evidence for the policy improvement claim.
- Well-designed ablation studies, particularly those isolating format reward vs. preference reward and comparing training strategies (mixed, critic-then-policy, policy-then-critic).
- The test-time scaling results with self-critique are compelling and demonstrate clear practical benefits over majority voting and external critics.
- Generality demonstrated across multiple base models (Qwen-2.5-VL, Mimo-VL, LLaMA-3.2-Vision), increasing confidence in the approach's robustness.
- The paper is honest about limitations, including the gap to the ground-truth oracle in test-time scaling and trade-offs between critic and policy ability.
- Clear writing and well-organized presentation, with code and models released for reproducibility.

### Weaknesses

- The central claim that 'critic training improves policy' may be confounded with general RL-on-verifiable-tasks effects. A comparison with RL on an equivalent amount of standard verifiable VQA or reasoning data would strengthen the causal claim.
- Statistical significance of improvements is not reported; many gains are small (e.g., +0.2 on MMBench) and may not be robust.
- The analysis of why critic data specifically helps policy is somewhat superficial. The 'enhanced visual perception' hypothesis is plausible but not directly tested (e.g., via hallucination-specific subsets or perception probes).
- The test-time scaling uses Best-of-128 with recursive pairwise comparison, which is computationally expensive; the paper does not discuss compute cost vs. benefit or compare with simpler scaling methods.
- The comparison with existing reasoning VLMs may not be entirely fair, as those models were trained with different objectives and potentially different inference procedures.
- The correlation between critic and policy ability (Figure 3) is based on a single training run, and the claim of a 'strong positive correlation' is not statistically supported.
- The VLM Agent results are based on only two tasks, limiting the generalizability of findings about agent capabilities.
- The paper does not discuss potential negative societal impacts, such as bias amplification in automated evaluation or misuse of self-improving models.

### Questions

- To what extent is the policy improvement due to RL on any verifiable task, rather than the critic data specifically? Have you compared with RL on an equivalent amount of standard VQA or reasoning data with verifiable answers?
- Can you provide statistical significance tests (e.g., confidence intervals) for the reported improvements, especially for smaller gains?
- What is the computational cost (GPU hours) for training LLaVA-Critic-R1? How does the performance gain compare to simply fine-tuning on more policy data or using a larger model?
- Can you provide more direct evidence for the 'enhanced visual perception' hypothesis? For example, how does the model perform on hallucination-specific subsets or perception-specific probes before and after critic training?
- How does LLaVA-Critic-R1 compare to a model trained via SFT on the same 40k critic data without GPT rationales? This would isolate the benefit of RL over SFT with identical data.
- In the test-time scaling experiments, how does the recursive pairwise comparison method compare to directly asking the critic to score all n responses or using a score threshold?
- Have you tested the test-time self-critique scaling on the Mimo-VL and LLaMA-3.2 based models? Does the correlation between critic and policy ability hold across different base models?
- How sensitive are the results to the choice of alpha (the reward balance hyperparameter)? Have you explored other values?
- The paper shows that policy training degrades critic ability. Can you elaborate on why this happens and whether there are ways to mitigate it?
- Have you considered using a process reward model or step-wise verification for the critic training, rather than just the final preference label?

### Limitations

- The paper does not fully isolate the effect of critic data from general RL-on-verifiable-tasks effects, making the causal claim about critic data less certain.
- The test-time scaling approach is computationally expensive (128 generations per question), which may limit practical applicability.
- The analysis of the relationship between critic and policy ability is based on limited evidence (one training run, correlation not statistically tested).
- The VLM Agent evaluation is limited to two benchmarks, and findings may not generalize to other agent tasks.
- The paper does not discuss potential negative societal impacts, such as bias amplification in automated evaluation pipelines or the risk of self-improving models producing overconfident but incorrect judgments.
- The experiments are limited to 7B-scale models; the generalizability of the findings to larger models is not demonstrated.
- The training data is limited to 40k examples from a specific source; robustness to different data sources is not fully explored.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 147,758
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 138,798
- Completion tokens: 10,944
- Reasoning tokens reported: 0
- Total tokens: 158,702
- Estimated total: $0.02252113

Full individual reviews and raw JSON responses are in `review_bundle.json`.
