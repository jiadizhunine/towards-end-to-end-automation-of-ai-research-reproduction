# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B057.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.018890**

## Final Meta-review

The paper investigates how supervised fine-tuning (SFT) and reinforcement learning (RL) shape exploration strategies in LLMs for multi-armed bandit tasks. It introduces two RL reward signals: a strategic regret-shaped reward (RL-STG) and an algorithmic reward that matches a UCB oracle (RL-ALG), and compares them with RL on the original bandit reward, SFT on UCB trajectories, and pretrained models. Experiments on Qwen 2.5 3B/7B show that learned policies achieve regret comparable to UCB/Thompson Sampling, generalize to 6x longer horizons and out-of-distribution bandit families, with RL-ALG and SFT being the strongest. Behavioral analysis reveals that learned policies are greedier than pretrained models, exhibit higher suffix failure, and discover exploitative variants of UCB that can outperform the teacher.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.000 | 0.000 | 6-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Systematic comparison of SFT and RL for LLM meta-bandit agents under multiple reward signals, including novel strategic and algorithmic reward designs.
- Detailed behavioral analysis using suffix failure, greedy frequency, match rates, and rationales reveals that lower regret can arise from exploitative, greedy heuristics rather than robust exploration.
- Comprehensive evaluation across model sizes (3B/7B), in- and out-of-distribution bandit families, 6x length generalization, and 10-arm tasks, with thorough implementation details.
- Uncovers concrete and interesting failure modes: SFT's arithmetic degradation on negative rewards and RL-ALG's discovery of exploitative UCB variants that outperform the teacher.

### Weaknesses

- Statistical rigor is limited: training uses a single run per configuration and only 64 evaluation episodes, with no confidence intervals or significance tests; many conclusions rely on visual inspection of boxplots.
- The strategic reward (RL-STG) requires oracle knowledge of true arm means, which is unrealistic for real-world deployment; its practical applicability is therefore limited.
- The UCB teacher uses a fixed exploration constant C=0.5 without tuning; the 'outperform teacher' result may reflect a suboptimal teacher rather than superior student strategy.
- The claim that RL generalizes more robustly than SFT is inconsistent across model sizes and reward variants, as SFT is strongest for 3B models and RL-OG/RL-STG show instabilities OOD.
- The study is confined to simple stationary MAB problems with a summarized state representation and small action spaces; findings may not transfer to contextual or more complex sequential decision-making.
- The SFT vs RL comparison is confounded: SFT uses chain-of-thought demonstrations while RL receives only reward signals, making the effect of supervision form inseparable from the learning paradigm.

### Questions

- How sensitive are the results to the UCB exploration constant C? Would a tuned C for T=300 reduce or eliminate the 'outperform teacher' effect?
- Were training runs repeated with different random seeds, and are there confidence intervals or hypothesis tests for regret comparisons in Figures 3 and 8-16?
- How should RL-STG be applied when true arm means are unknown? Does the claimed equivalence to RL-OG hold in the POMDP where the learner cannot observe mu?
- For RL-ALG with gamma_inter=0, what exactly is the policy optimizing? Is this a finite-horizon contextual bandit objective of per-step imitation error rather than a return-based exploration objective?
- What is the effect of omitting the KL penalty in PPO? Could adding a KL constraint prevent collapse to greedy policies and reduce suffix failure?
- Could the RL-ALG-discovered exploitative UCB variants be equivalent to standard UCB with a smaller exploration constant, and did the authors compare against tuned UCB baselines?

### Limitations

- Evaluation is limited to simple MAB tasks and small open models (Qwen 2.5 3B/7B), so conclusions may not transfer to frontier LLMs or to contextual/structured bandits.
- Use of privileged information (true means for RL-STG, UCB oracle for RL-ALG/SFT) limits direct applicability to real-world online decision-making.
- Learned policies show higher suffix failure and can prematurely abandon optimal arms, making them unsuitable for safety-critical or long-lived deployments.
- Only two training distributions are used; OOD coverage is limited, and no training on the Bernoulli_Delta class despite its relevance.
- No analysis of computational costs, sample efficiency, or checkpoint-selection bias is provided.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 92,272
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 88,176
- Completion tokens: 23,335
- Reasoning tokens reported: 16,989
- Total tokens: 115,607
- Estimated total: $0.01888991

Full individual reviews and raw JSON responses are in `review_bundle.json`.
