# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B020.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.020108**

## Final Meta-review

This paper introduces DEAS (DEtached value learning with Action Sequence), an offline RL framework that uses fixed-length action sequences as inputs to value functions to reduce the effective planning horizon in long-horizon tasks. The method combines IQL-style detached value learning (decoupling critic training from the actor) with distributional RL (classification-based HL-Gaussian) and dual discount factors (γ1 for within-sequence rewards, γ2 for cross-sequence discounting) to avoid value overestimation in high-dimensional action spaces. DEAS is compatible with various policy extraction methods (best-of-N, DPG, AWR, flow-matching) and is evaluated on 30 OGBench tasks, RoboCasa Kitchen simulation tasks with VLA backbones (GR00T N1.5, π0), and real-world Franka manipulation tasks. The method consistently outperforms strong baselines including FQL, n-step FQL, QC-FQL, CQN-AS, and Filtered BC, with ablations and value calibration analyses supporting the design choices.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 3.400 | 0.490 | 3-4 |
| Clarity | 4 | 3.600 | 0.490 | 3-4 |
| Significance | 3 | 3.400 | 0.490 | 3-4 |
| Soundness | 3 | 3.400 | 0.490 | 3-4 |
| Presentation | 4 | 3.600 | 0.490 | 3-4 |
| Contribution | 3 | 3.400 | 0.490 | 3-4 |
| Overall | 7 | 7.200 | 0.748 | 6-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses a significant practical challenge in offline RL: value overestimation when using action sequences with actor-critic methods
- Novel and well-motivated combination of action sequences (from Q-chunking) with IQL-style detached value learning, distributional RL, and dual discount factors
- Comprehensive empirical evaluation across multiple benchmarks: 30 OGBench tasks, RoboCasa Kitchen simulation with VLA models, and real-world robot manipulation
- Consistent improvements over strong baselines with good ablation studies isolating key design choices (action sequence length, network size, objectives, discount factors)
- Value calibration analysis provides insight into why detached value learning reduces overestimation
- Practical applicability demonstrated with large-scale VLAs (GR00T N1.5, π0), showing real-world relevance
- Compatibility with multiple policy extraction methods enhances practical utility
- Scaling analysis across dataset sizes and robustness to data quality strengthen empirical claims
- Clear writing with detailed implementation details for reproducibility

### Weaknesses

- Theoretical contribution is limited; the proof in Appendix E directly extends IQL's analysis to action sequences without new insights into action-sequence-specific challenges (e.g., bias-variance tradeoffs, convergence guarantees)
- Significant hyperparameter sensitivity: action sequence length H, dual discount factors γ1/γ2, and distributional support ranges (vmin/vmax) require task-specific tuning, with limited practical guidance for selection
- No empirical comparison with CO-RFT, the most related VLA-specific offline RL method mentioned in the related work section
- Real-world experiments are limited to relatively simple pick-and-place tasks with small demonstration counts (5 demos, 25 rollouts), limiting statistical power and generalizability claims
- Limited analysis of when action sequences are beneficial versus harmful (e.g., dense rewards, short horizons, or tasks where single-step actions suffice)
- The comparison to QC-FQL may be affected by hyperparameter tuning advantages; the extent of tuning and fairness of comparison could be more transparent
- Some baseline results (e.g., CQN-AS) are extremely low, raising questions about baseline configuration for OGBench tasks
- Computational overhead compared to baselines is not discussed in detail

### Questions

- How should practitioners select the action sequence length H and dual discount factors (γ1, γ2) for new tasks? Is there a principled method based on task properties (e.g., horizon, reward sparsity), or is per-task tuning required?
- Why was CO-RFT not included as an empirical baseline in the RoboCasa Kitchen experiments, given its close relation to the approach? What differences in performance would be expected?
- How sensitive is DEAS to the choice of H relative to network capacity? The ablation shows H=8 with a smaller actor outperforms H=16 with a larger actor—is there a general scaling principle?
- In the real-world experiments, with only 5 demonstrations and 25 rollouts, how statistically significant are the reported improvements? Would confidence intervals or additional trials change the conclusions?
- How does DEAS compare to simply using n-step TD updates with IQL (without explicit action sequences)? This would help isolate the benefit of action sequences versus multi-step returns.
- How were the dual discount factors γ1 and γ2 selected for the VLA experiments? Were they tuned per task or kept fixed? What is the theoretical justification for the dual discount scheme?
- What is the computational overhead of DEAS compared to FQL and QC-FQL, particularly in the VLA experiments?
- Could the value calibration analysis be supported with quantitative metrics (e.g., rank correlation coefficients) to complement the visual comparison?
- Why does QC show such degraded performance in real-world experiments (39.6% vs 64% for the base model)? Is this due to implementation details or small dataset size?
- How does DEAS handle tasks with varying reward scales? What are the trade-offs between data-centric and universal support types for distributional RL?

### Limitations

- Fixed action sequence lengths across tasks; optimal sequence length varies with task complexity, and adaptive or hierarchical sequence lengths are not explored
- Scaling to large-scale multi-task value functions (hundreds/thousands of tasks) remains an open challenge; the method currently trains reward models on only 3-4 tasks simultaneously
- Sensitivity to distributional RL hyperparameters (vmin, vmax, number of bins) could limit robustness across domains
- Real-world validation is limited to simple pick-and-place tasks with small demonstration counts and trial numbers, limiting the strength of scalability and generalizability claims
- The theoretical analysis is limited to extending IQL's results to action sequences, without new insights into the benefits of action sequences for horizon reduction or the interaction with distributional RL
- Potential negative societal impact is not discussed; while the focus is robotic manipulation, broader deployment in safety-critical domains should be considered (e.g., labor displacement, safety in autonomous systems)

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 129,879
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 120,919
- Completion tokens: 11,265
- Reasoning tokens reported: 0
- Total tokens: 141,144
- Estimated total: $0.02010795

Full individual reviews and raw JSON responses are in `review_bundle.json`.
