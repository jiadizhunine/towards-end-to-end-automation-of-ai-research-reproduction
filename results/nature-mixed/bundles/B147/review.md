# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B147.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.022512**

## Final Meta-review

The paper introduces SPA (Self-Play Agent), a two-stage framework for improving LLM agent reinforcement learning in out-of-distribution (OOD) environments. The authors first identify that vanilla RL training in OOD environments (Sokoban, FrozenLake, Sudoku) degrades Pass@k (diversity of successful trajectories) even when Pass@1 improves, indicating narrow exploitative behavior. SPA addresses this by decomposing world modeling into (1) state estimation—converting raw observations into structured natural-language descriptions (e.g., coordinates)—and (2) transition modeling—training the model via self-play supervised fine-tuning (SFT) to predict next states. This SFT stage serves as initialization for subsequent PPO-based RL training. Experiments across four model sizes (Qwen2.5-0.5B/1.5B/3B, LLaMA3.2-1B) and three environments show consistent improvements over vanilla RL and the VAGEN baseline, with substantial gains (e.g., Sokoban Pass@1 from 25.6% to 59.8% for Qwen2.5-1.5B). The paper provides extensive ablations isolating the contributions of transition modeling, ground-truth states, initial policy quality, and SFT duration, as well as analyses of exploration-exploitation dynamics and easy-to-hard transfer.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 2.800 | 0.400 | 2-3 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 2.800 | 0.400 | 2-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 2.800 | 0.400 | 2-3 |
| Contribution | 3 | 2.800 | 0.400 | 2-3 |
| Overall | 6 | 6.000 | 0.632 | 5-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Clear problem identification: The paper empirically demonstrates the Pass@k degradation issue in OOD environments, providing a well-motivated and under-studied problem.
- Simple, effective method: The two-stage approach (SFT for world modeling, then PPO) is straightforward to implement and shows consistent improvements across all evaluated models and environments.
- Comprehensive ablations: The paper systematically isolates the contributions of each component (transition modeling, state estimation, ground truth, initial policy, SFT duration), providing strong evidence for the design choices.
- Multi-model evaluation: Results across four different model families/sizes strengthen the generalizability of the findings.
- Good analytical sections: The exploration-exploitation dynamics and easy-to-hard transfer findings provide insights beyond just reporting final numbers.
- Strong empirical results: SPA achieves substantial gains, sometimes doubling or tripling Pass@1/Pass@8 scores over baselines.

### Weaknesses

- Limited environment diversity: All environments are deterministic, fully observable text-based grid/logic games. The paper claims OOD generality but does not test stochastic, partially observable, or more realistic environments.
- Hand-crafted state representations: The state estimation component relies on manually specified coordinates for each environment, which requires domain knowledge and may not scale to less structured environments.
- Lack of statistical rigor: No error bars, multiple random seeds, or significance tests are reported, making it unclear if the improvements are robust.
- Potential unfair comparisons: The VAGEN baseline is reimplemented (originally designed for VLM agents), and the comparison with GPT-OSS-20B is zero-shot rather than fine-tuned, potentially disadvantaging these baselines.
- Limited novelty: The core idea (SFT on transition data followed by RL) is a relatively straightforward combination of existing techniques; the main contribution is more empirical than methodological.
- Misleading 'self-play' terminology: No self-competition or adversary is involved; this is standard environment interaction for data collection.
- Confounded evaluation: The SFT stage adds extra training data and compute; the improvement could partly stem from additional supervised training rather than the world-modeling objective itself, though the masked ablation partially addresses this.

### Questions

- 1. How do the results change with multiple random seeds? Can you report mean and standard deviation for the main results in Table 2, and are the improvements statistically significant?
- 2. How would SPA perform in stochastic environments (e.g., FrozenLake with slippery ice) or partially observable settings? The paper claims to address OOD but only evaluates deterministic, fully observable environments.
- 3. How was VAGEN reimplemented? What specific differences exist from the original implementation, and could these explain the performance gap?
- 4. The comparison with GPT-OSS-20B is zero-shot. Would SPA also improve GPT-OSS-20B if it were fine-tuned with the same pipeline?
- 5. What is the quality and composition of the self-play SFT data (e.g., number of trajectories, success rate, filtering criteria)? How does the amount of SFT data affect performance?
- 6. The paper shows SPA SFT alone decreases performance at step 0 (e.g., Sokoban Pass@1 drops from 16.3 to 8.3 for Qwen2.5-1.5B). Why does this initialization help RL despite being worse initially?
- 7. In Figure 7, Pass@k declines during the exploitation phase (steps 400-1000). Could this indicate training instability or policy collapse? How does SPA compare to vanilla RL at k=1024 in the later training phase?
- 8. How does the computational cost of the SFT stage compare to the RL stage? Is the total compute for SPA (SFT + RL) fairly compared to baselines that only use RL?
- 9. Does the world model learned via SFT actually get used during RL inference (e.g., for planning), or is it purely implicit initialization?
- 10. For the easy-to-hard transfer experiment, is the gain from world modeling specifically, or would SFT on the simple task without transition modeling also help?

### Limitations

- The method is only evaluated on deterministic, fully observable text-based environments; its applicability to stochastic, partially observable, or continuous environments is unknown and not addressed empirically.
- The state estimation component relies on domain-specific hand-crafted coordinates, which may not generalize to environments without clear spatial structure.
- The paper does not provide statistical significance testing, making it difficult to assess the reliability of the reported improvements.
- The comparison with VAGEN and GPT-OSS may be unfair due to reimplementation differences and zero-shot evaluation, respectively.
- The 'world model' is only a one-step transition predictor and is not used for planning during inference, potentially overstating the method's capabilities.
- Potential negative societal impacts are not discussed. While tasks are benign games, the approach could be applied to more sensitive domains (e.g., autonomous decision-making), warranting safety considerations.
- The paper does not compare against other recent LLM agent training methods (e.g., GRPO-based approaches or other model-based RL methods).

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 143,812
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 134,852
- Completion tokens: 12,883
- Reasoning tokens reported: 0
- Total tokens: 156,695
- Estimated total: $0.02251161

Full individual reviews and raw JSON responses are in `review_bundle.json`.
