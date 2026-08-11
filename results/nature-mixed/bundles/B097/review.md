# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B097.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.030249**

## Final Meta-review

This paper studies system identification for general nonlinear dynamical systems with partial observations, non-Gaussian control inputs, and correlated, nonzero-mean adversarial disturbances. The authors reformulate the input-output mapping as a linear combination of basis functions applied to a truncated input history of length τ. They prove that an ℓ2-norm estimator achieves an estimation error of O(ρ^τ) for identifying the true parameter matrix G*, provided the attack probability at each time is less than 1/(2τ). They also provide a matching lower bound of Ω(ρ^τ), demonstrating optimality. The work significantly broadens the assumptions compared to prior literature, which typically requires Gaussian inputs, i.i.d. disturbances, or zero-mean disturbances. Numerical experiments validate the theoretical findings, showing the ℓ2-norm estimator outperforms least-squares and other ℓα-norm estimators under adversarial attacks.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 5.800 | 0.400 | 5-6 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- The problem setting is significantly broader than prior work, relaxing assumptions on inputs (non-Gaussian, nonzero-mean allowed) and disturbances (correlated, nonzero-mean, adversarial allowed).
- Provides both matching upper and lower bounds on estimation error, demonstrating optimality of the ℓ2-norm estimator with respect to the memory length τ.
- Rigorous theoretical analysis with detailed proofs in the appendix, including sub-Gaussian concentration arguments and covering number techniques.
- Numerical experiments support the theoretical results, showing the ℓ2-norm estimator's robustness to adversarial attacks and consistency with the predicted error scaling.
- Clear comparison table (Table 1) situating the work relative to existing literature.

### Weaknesses

- The attack probability constraint p < 1/(2τ) is restrictive and creates a trade-off: increasing τ (for accuracy) reduces the allowable attack probability, limiting practical applicability.
- The estimation error does not decay with the time horizon T, meaning the estimator cannot converge to the true G* even with infinite data.
- The lower bound proof relies on specially designed nonlinear basis functions (the β function construction), and it is unclear whether the bound holds for linear systems or more natural basis function choices.
- The assumption of sub-Gaussian disturbances with potentially nonzero mean and unbounded support may be inconsistent with a truly adversarial disturbance model.
- The numerical experiments are limited to a single system type (tanh or log activation with random matrices) and do not explore a wide range of system configurations or basis function choices.
- The sample complexity in Theorem 3.1 scales polynomially with ν^8, which could be very large in practice, though this is not highlighted as a practical concern.

### Questions

- How sensitive is the estimation error bound to the choice of basis functions Φ? The paper assumes they satisfy Lipschitzness and excitation conditions but does not provide guidance on how to select them in practice for optimal performance or how the approximation error ε_t scales with M.
- In the lower bound proof, σ_w is chosen as (1/ρ)^Ω(τ log(T/δ)), which grows with T. Is this a realistic adversarial model? What happens if σ_w is required to be uniformly bounded over all T? Could the lower bound be improved in that case?
- Can the analysis be extended to handle unknown or time-varying attack probability p? The current assumption requires p to be known and constant.
- The paper discusses trade-offs in choosing τ but does not provide a concrete method for selecting τ optimally. Could you provide practical guidance, perhaps based on the trade-off between estimation error and recovery time?
- In Experiment 1, the least-squares estimator fails dramatically. Could you comment on whether any robust variant of least-squares (e.g., Huber loss) could also work in this setting, and how it compares to the ℓ2-norm estimator?
- What is the computational complexity of solving the ℓ2-norm minimization problem (12) in practice, particularly for large M and T? Are there efficient algorithms for this non-smooth convex problem?

### Limitations

- The restrictive attack probability assumption p < 1/(2τ) may not hold in many real-world adversarial scenarios where attacks could be more frequent or correlated.
- The estimation error bound is a positive constant that does not vanish with T, meaning the method cannot achieve arbitrarily accurate identification even with infinite data.
- The lower bound construction uses specially designed nonlinear basis functions, and it remains unclear whether the optimality result extends to more natural basis function choices or linear systems.
- The paper does not discuss the computational complexity of solving the ℓ2-norm minimization problem (12) in practice, particularly for large M and T.
- The paper does not address potential negative societal impacts of the work, though this is a theoretical paper with no immediate societal implications.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 203,811
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 194,851
- Completion tokens: 10,518
- Reasoning tokens reported: 0
- Total tokens: 214,329
- Estimated total: $0.03024927

Full individual reviews and raw JSON responses are in `review_bundle.json`.
