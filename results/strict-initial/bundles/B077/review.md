# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B077.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.030328**

## Final Meta-review

The paper proposes SISL, a skill-based meta-reinforcement learning framework designed to be robust to noisy offline demonstrations in long-horizon tasks. SISL introduces a decoupled skill-improvement policy, a prioritized online buffer, and a maximum-return relabeling mechanism to progressively refine skills from noisy offline data while interacting with the environment during meta-training. Experiments on Kitchen, Office, Maze2D, and AntMaze across multiple noise levels report improvements over several non-meta and meta-RL baselines, with ablations and additional robustness analyses.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.000 | 0.000 | 2-2 |
| Clarity | 2 | 2.000 | 0.000 | 2-2 |
| Significance | 2 | 2.600 | 0.490 | 2-3 |
| Soundness | 2 | 2.000 | 0.000 | 2-2 |
| Presentation | 2 | 2.000 | 0.000 | 2-2 |
| Contribution | 2 | 2.200 | 0.400 | 2-3 |
| Overall | 4 | 4.000 | 0.000 | 4-4 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important and under-explored problem: robustness of skill-based meta-RL to noisy or suboptimal offline demonstrations.
- The proposed mechanisms (decoupled skill-improvement policy and maximum-return relabeling) are well motivated and individually ablated.
- Broad empirical evaluation across four long-horizon environments, multiple noise levels, and additional robustness tests (limited data, random noise injection, suboptimal datasets).
- Reproducibility is supported by pseudocode, hyperparameter details, and code references.

### Weaknesses

- The main results table (Table 1) is malformed/incomplete for noisy conditions, with missing entries for key baselines and SISL itself, making the central claim of improved robustness unverifiable.
- There is a direct contradiction about the online buffer initialization: Section 4.2 says B_on is initialized with B_off, while Appendix F.4 states B_on contains only online trajectories; this also affects what data the reward model sees.
- Several key hyperparameters (e.g., lambda_imp, prioritization temperature T) are tuned per environment and per noise level, suggesting possible overfitting to benchmark noise levels and weakening the practical robustness claim.
- The baseline comparison is incomplete: no comparison to recent skill-based meta-RL methods or methods explicitly designed for noisy/suboptimal offline data, and non-meta baselines are given far fewer training iterations.
- The method requires online interaction during meta-training and does not support purely offline or zero-shot meta-RL; this limitation is not clearly positioned.
- The reward-model-based relabeling may be biased when offline trajectories come from heterogeneous task distributions or reward scales, and this issue is not systematically analyzed.
- Multiple presentation issues, including typos, inconsistent notation, and unclear figures/tables, were noted by several reviewers.

### Questions

- Can the authors provide a complete, properly formatted version of Table 1 that includes SISL and all baselines for every noise level?
- Is B_on initialized with B_off or not? Resolve the contradiction between Section 4.2 and Appendix F.4, and clarify exactly what data the reward model is trained on.
- How are noise-specific hyperparameters (e.g., lambda_imp^kld) selected in practice without oracle knowledge of the noise level? Are the reported results selected using test-noise-level information?
- Does the maximum-return relabeling over training tasks with heterogeneous reward scales introduce bias? Can an experiment with non-uniform reward scales demonstrate robustness?
- Could SISL be adapted to a purely offline setting or a setting with no online reward signals during meta-training?
- Why are non-meta baselines limited to 0.5K iterations while meta-RL methods receive far more training? Would SAC with comparable environment interaction time close the gap?

### Limitations

- SISL requires online environment interaction and reward signals during meta-training, so it does not apply to fully offline settings.
- The method incurs about 16% additional computation per iteration and still requires meta-test fine-tuning.
- Hyperparameters are sensitive to environment and noise level, requiring per-setting tuning.
- The reward model may be biased for tasks with complex or multi-scale reward structures.
- Evaluation is confined to simulated benchmarks with synthetic Gaussian/random noise; real-world noisy demonstration data are not considered.
- No theoretical analysis or convergence guarantees are provided.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 165,035
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 160,939
- Completion tokens: 27,803
- Reasoning tokens reported: 21,636
- Total tokens: 192,838
- Estimated total: $0.03032777

Full individual reviews and raw JSON responses are in `review_bundle.json`.
