# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B020.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 1, 'Reject': 4}
- Estimated API cost: **$0.016567**

## Final Meta-review

The paper proposes DEAS, an offline RL method that learns value functions over fixed-length action sequences treated as options in an SMDP framework, reducing the effective planning horizon without goal conditioning. To mitigate value overestimation, it combines IQL-style detached value learning with distributional classification and dual discount factors. The policy can be extracted using arbitrary methods such as weighted BC, flow matching, or best-of-N sampling. Experiments on 30 OGBench tasks, RoboCasa Kitchen with a VLA, and real-robot manipulation tasks show improved performance over several baselines.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 2 | 2.200 | 0.400 | 2-3 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 2 | 2.200 | 0.400 | 2-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 2 | 2.400 | 0.490 | 2-3 |
| Presentation | 2 | 2.200 | 0.400 | 2-3 |
| Contribution | 2 | 2.200 | 0.400 | 2-3 |
| Overall | 4 | 4.400 | 0.800 | 4-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important and timely problem of scaling offline RL to long-horizon tasks and fine-tuning VLAs with suboptimal data.
- The combination of action-sequence options, detached value learning, and distributional RL is simple, effective, and policy-agnostic, allowing integration with expressive policies such as large VLAs.
- Provides extensive experimental evaluation across diverse benchmarks (OGBench, RoboCasa Kitchen, real-robot) and demonstrates strong aggregate improvements over baselines.
- The paper includes practical implementation details and open-source release, supporting reproducibility.

### Weaknesses

- Novelty is largely incremental: the core components (IQL-style detached value learning, action chunking/options, distributional RL) are drawn from prior work, and the option/SMDP framing is primarily a reformulation without new theoretical insight.
- Several key ablation tables and figures referenced in the text (e.g., effect of action sequence length, network size, training objective, dual discount factors, scaling analysis) are missing from the submission, making central empirical claims unverifiable.
- The dual discount factors (gamma1 != gamma2) are introduced as a heuristic with no theoretical justification or proof that the modified objective preserves optimality for the original MDP.
- Equation (3) appears to contain a notation error in the construction of the Q-value target distribution, potentially undermining the correctness of the distributional update as written.
- The claim of consistently outperforming baselines is overstated: per-task results show QC-FQL and FQL occasionally match or beat DEAS (e.g., cube-triple task4, puzzle-4x4 task2, cube-quadruple task4).
- The real-robot and some simulation experiments lack confidence intervals or statistical significance tests, and the real-robot evaluation uses very few demonstrations and rollouts.
- Baseline comparisons are incomplete or potentially unfair: IQL is absent from OGBench experiments, CO-RFT is not considered in VLA experiments, and CQN-AS may be disadvantaged by applying it to state-based tasks or modifying its training.
- The method introduces several sensitive hyperparameters (action sequence length H, expectile, distributional support range, dual discounts) with no quantitative sensitivity analysis, and fixed H is unlikely to be optimal across tasks.

### Questions

- In Equation (3), should the target distribution use V(s_{t+H}) rather than V(s_t)? Please clarify the exact Q-learning update used in the implementation.
- Can the authors provide the missing ablation tables and figures (effect of action sequence length, network size, training objective, dual discount factors, scaling analysis) to support the claimed benefits of each component?
- How does DEAS compare to CO-RFT, a recent chunked offline RL method for VLAs, and why is it not included as a baseline in the VLA experiments?
- What are the confidence intervals or standard errors for the real-robot and RoboCasa results, and are the reported improvements statistically significant?
- Why is IQL not evaluated on OGBench, and how does the detached value learning with action sequences compare to n-step IQL with the same horizon reduction?
- Is there any theoretical justification for using dual discount factors gamma1 and gamma2 in the SMDP update, and how does this affect the optimal policy relative to the original MDP?
- How are v_min and v_max chosen for the distributional support in each domain, and how sensitive are the results to these choices?

### Limitations

- The action sequence length H is fixed and task-specific; there is no adaptive mechanism to select H based on task complexity.
- The dual discount factor convention and expectile value learning lack formal guarantees for convergence or overestimation avoidance in continuous action-sequence spaces.
- The method is sensitive to distributional support ranges and discount factors, requiring per-domain tuning.
- Real-robot validation is limited to a small number of demonstrations and rollouts, with no statistical analysis or cross-task generalization evidence.
- Scaling to large-scale unified multi-task value functions is not explored.
- The paper does not discuss potential negative societal impacts of real-world robot learning and deployment.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 111,850
- Cache-hit prompt tokens: 48,256
- Cache-miss prompt tokens: 63,594
- Completion tokens: 26,888
- Reasoning tokens reported: 20,712
- Total tokens: 138,738
- Estimated total: $0.01656692

Full individual reviews and raw JSON responses are in `review_bundle.json`.
