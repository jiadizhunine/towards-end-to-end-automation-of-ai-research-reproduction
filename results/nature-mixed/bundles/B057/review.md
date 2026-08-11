# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B057.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.024993**

## Final Meta-review

This paper systematically studies how Supervised Fine-Tuning (SFT) and Reinforcement Learning (RL) shape exploration strategies of Large Language Models (LLMs) in multi-armed bandit (MAB) tasks. The authors train Qwen 2.5 3B/7B models using SFT on UCB expert trajectories and RL with three reward signals: original bandit rewards (RL-OG), strategic regret-shaped rewards (RL-STG), and algorithmic rewards providing binary imitation signals from a UCB oracle (RL-ALG). Evaluation covers in-distribution and out-of-distribution bandit environments, including generalization to longer horizons (6×) and larger action spaces. Key findings: (1) trained agents achieve performance comparable to UCB/Thompson Sampling baselines; (2) RL-ALG and SFT consistently outperform reward-only RL; (3) RL policies generalize more robustly than SFT in several settings; (4) behavioral analysis reveals an emergent exploitation bias—learned policies become greedier, with higher suffix failure rates and premature abandonment of exploration; (5) RL-ALG agents discover exploitative UCB variants that can outperform their teacher; (6) SFT policies show fragile OOD generalization due to arithmetic degradation. The paper advocates for tailored reward design and evaluation beyond average regret to promote robust exploration.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 4 | 3.600 | 0.490 | 3-4 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 4 | 3.600 | 0.490 | 3-4 |
| Contribution | 3 | 3.200 | 0.400 | 3-4 |
| Overall | 7 | 6.600 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Comprehensive systematic comparison of SFT and multiple RL reward designs (original, strategic, algorithmic) across two model sizes and diverse bandit environments
- Novel reward designs—regret-shaped strategic reward and algorithmic (UCB-imitation) reward—are well-motivated and show practical benefits
- Behavioral analysis goes beyond aggregate regret to reveal mechanism-level differences (greedy tendencies, suffix failures, bimodal best-arm distributions), providing important insights into failure modes of trained LLM agents
- Demonstration that RL-ALG agents can discover exploitative UCB variants and outperform their teacher, with supporting rationale analysis
- Robust evaluation including length generalization, OOD distribution shifts, scaling to larger action spaces, and multiple environment parameterizations
- Clear presentation of the two-level MDP formulation for token-level PPO and detailed reproducibility information in appendices
- Honest and nuanced discussion of limitations, including contextual bandit caveats and small-model failures

### Weaknesses

- Lack of statistical significance testing—only boxplots with medians/IQRs are shown, no confidence intervals or hypothesis tests, and only 64 evaluation episodes per setting
- Behavioral analysis relies heavily on qualitative inspection of LLM rationales, which may not fully reflect the actual policy decision-making process
- The emergent exploitation bias is identified but not deeply mechanistically explained, and no mitigation strategies are proposed
- The contextual bandit experiment (MovieLens) is limited, acknowledges memorization issues, and somewhat undermines generalizability claims
- The claim that 'RL policies generalize more robustly than SFT' is nuanced and not consistently supported across all environments; in some cases SFT is competitive or better
- The variance-reduction benefit of the strategic reward (RL-STG) is claimed but not directly quantified, and RL-STG shows unstable OOD performance
- Limited to Qwen models (3B/7B) and simple MAB tasks; generalizability to other architectures and more complex sequential decision-making is unclear
- Analysis of the discovered UCB variants is qualitative; more rigorous quantitative analysis (e.g., how often the policy follows the stated formula) would strengthen the claims

### Questions

- How statistically significant are the performance differences between methods (e.g., RL-ALG vs SFT vs RL-STG)? Have you considered reporting confidence intervals or performing significance tests (e.g., bootstrap) on the regret comparisons?
- The paper shows RL-ALG agents discover a UCB variant with exploration term sqrt(log(N_t(a)+1)/N_t(a)). What is the theoretical regret of this variant? Does it have known sublinear regret guarantees, or could it suffer linear regret in some cases?
- How sensitive are the results to the UCB exploration constant C=0.5 used for the teacher? Would a more exploratory teacher (e.g., C=1.0 or C=2.0) change the observed exploitation bias or the relative performance of learned policies?
- Could you quantify the diversity and stability of the discovered UCB variants across different random seeds or training runs?
- For the SFT arithmetic failure on negative rewards—is this specific to Qwen models, or have you tested other base models? Could mixed training data with negative rewards alleviate this?
- The 3B model fails to learn with RL-OG/RL-STG but succeeds with RL-ALG. Is this purely a credit assignment issue, or could it be due to optimization instability (e.g., value function divergence)? Have you analyzed value loss or advantage estimates during training?
- Have you considered interventions to mitigate the emergent greediness (e.g., re-weighting exploration rewards, curriculum learning, or adding exploration bonuses)? Any preliminary results?
- Can you provide quantitative evidence (e.g., training reward variance, learning curves) that RL-STG reduces variance compared to RL-OG, as claimed?
- How does the choice of prompt summary (sufficient statistics vs. raw history) interact with the training paradigms? Would the exploitation bias be reduced with a different observation format?
- With only 64 evaluation episodes, what are the standard errors of the regret estimates? Are the boxplot differences robust to this sample size?

### Limitations

- The study is limited to simple MAB tasks; conclusions may not generalize to more complex sequential decision-making problems (e.g., contextual bandits with rich features, RLHF-style tasks)
- Only Qwen 2.5 3B/7B models are evaluated; results may not transfer to other LLM architectures or larger scales
- The contextual bandit experiment is acknowledged as limited due to memorization concerns, which limits the scope of the claims
- The paper identifies the exploitation bias but does not propose concrete solutions or mitigation strategies, limiting practical impact
- The behavioral analysis relies on surrogate metrics (suffix failures, match rates) and LLM-generated rationales, which may not fully capture exploration quality
- The computational cost of training (500 PPO iterations with 64 parallel environments) may be prohibitive for many practitioners, and efficiency trade-offs are not discussed
- Potential negative societal impact is not explicitly discussed: if these training methods are applied to real-world LLM agents (e.g., recommendation systems, autonomous decision-making), the emergent exploitation bias could lead to premature abandonment of exploration and suboptimal long-term outcomes, potentially causing harm in high-stakes applications

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 162,080
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 153,120
- Completion tokens: 12,612
- Reasoning tokens reported: 0
- Total tokens: 174,692
- Estimated total: $0.02499325

Full individual reviews and raw JSON responses are in `review_bundle.json`.
