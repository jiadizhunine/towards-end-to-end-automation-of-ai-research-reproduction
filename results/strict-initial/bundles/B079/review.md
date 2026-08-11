# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B079.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 3, 'Reject': 2}
- Estimated API cost: **$0.032004**

## Final Meta-review

The paper proposes BEMA, a bias-corrected exponential moving average for stabilizing language model fine-tuning. It frames stabilizer design as estimating the minimizer of an Ornstein-Uhlenbeck process, derives the MLE, and instantiates it as a practical two-line-change EMA variant. Experiments on 1B-scale models (Qwen2.5-1.5B, Gemma3-1B, Llama3.2-1B) fine-tuned on Tulu-3-SFT show improved convergence and downstream generation performance over vanilla training and EMA in several settings.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.600 | 0.490 | 2-3 |
| Clarity | 2 | 2.200 | 0.400 | 2-3 |
| Significance | 2 | 2.600 | 0.490 | 2-3 |
| Soundness | 2 | 2.600 | 0.490 | 2-3 |
| Presentation | 2 | 2.200 | 0.400 | 2-3 |
| Contribution | 2 | 2.600 | 0.490 | 2-3 |
| Overall | 4 | 5.200 | 0.980 | 4-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel statistical framing of stabilizer design as estimation in an OU process, yielding a clean MLE with optimality properties in the quadratic model.
- BEMA is memory-efficient and conceptually simple, described as a drop-in replacement for EMA.
- Extensive empirical study covering multiple models, benchmarks, and ablations (hyperparameters, batch size, update frequency, learning-rate decay, comparisons with OUEMA/DEMA).
- Evaluation on generation-based tasks (BoolQ, GSM8K, MMLU-HS) is relevant to closed-loop error amplification.

### Weaknesses

- The practical BEMA algorithm is not specified completely: Algorithm 1 is only a caption, and the exact discrete-time update rule is not given in the text, hindering reproducibility.
- The connection between the theory (continuous-time OU, known Hessian A, flat average) and the practical method (AdamW, isotropic A=alpha_t I, polynomial EMA, burn-in, sparse updates) is heuristic; no end-to-end theoretical guarantee covers the actual algorithm.
- Empirical evidence is limited to 1B-1.5B models, a single SFT dataset, two seeds, and small evaluation subsets, with no confidence intervals or significance tests; results on Llama3.2-1B are mixed, with vanilla training sometimes outperforming both BEMA and EMA.
- BEMA introduces additional hyperparameters (eta, kappa, phi, rho) that materially affect performance; too-small eta can cause performance collapse, and no principled selection strategy is provided, weakening the 'drop-in' claim.
- Baseline comparisons omit common averaging methods such as SWA or LAWA, and the paper does not report wall-clock or memory overhead relative to standard EMA.
- Presentation issues include typos in key equations, duplicated theorem labels, redacted figures, and unclear references, reducing clarity.

### Questions

- What is the exact discrete-time BEMA update rule, including how beta_t, alpha_t, eta, kappa, phi, and rho are used?
- How does BEMA reduce to standard EMA in the limit, and can the theoretical optimality be extended to discrete-time SGD or AdamW?
- How should practitioners set eta and other hyperparameters without tuning on the evaluation benchmarks, given that eta=0.1 can cause collapse?
- Are the reported improvements statistically significant; can confidence intervals or more seeds be provided?
- Why does vanilla training sometimes outperform BEMA/EMA on Llama3.2-1B, and under what conditions is BEMA beneficial?
- What is the additional wall-clock time and memory usage of BEMA when storing theta_0 and updating every phi steps?

### Limitations

- The theoretical results rely on a continuous-time quadratic (OU) approximation and known Hessian, which do not capture nonconvex transformer training, AdamW, momentum, or learning-rate decay.
- Empirical validation is restricted to 1B-parameter models and supervised fine-tuning on Tulu-3-SFT; results may not generalize to larger models, RLHF/GRPO, or other post-training paradigms.
- BEMA introduces extra hyperparameters and memory overhead (storing theta_0), which may limit practicality in memory-constrained settings.
- The evaluation uses fixed small prompt subsets with formatting constraints; improvements may partially reflect instruction-following rather than core optimization quality.
- No assessment of negative societal impacts or potential harms from improved LM fine-tuning is provided.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 182,925
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 178,829
- Completion tokens: 24,844
- Reasoning tokens reported: 18,369
- Total tokens: 207,769
- Estimated total: $0.03200385

Full individual reviews and raw JSON responses are in `review_bundle.json`.
