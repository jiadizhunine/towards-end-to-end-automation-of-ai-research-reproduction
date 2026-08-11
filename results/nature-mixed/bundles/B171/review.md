# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B171.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.026853**

## Final Meta-review

This paper provides a theoretical convergence analysis for two momentum-based variance-reduced variants of the Muon optimizer: Muon-MVR1 (one-batch) and Muon-MVR2 (two-batch). The main contributions are: (1) establishing an O~(T^{-1/4}) iteration complexity for Muon-MVR1 in stochastic non-convex settings, (2) proving that Muon-MVR2 achieves an O~(T^{-1/3}) iteration complexity, which the authors claim is optimal, and (3) providing last-iterate convergence rates under the Polyak-Łojasiewicz (PL) condition (O~(T^{-1/2}) for MVR1 and O~(T^{-2/3}) for MVR2). Experiments on CIFAR-10 (ResNet18) and C4 (LLaMA2-130M) are included to validate the practical performance of the proposed variants.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 3 | 2.600 | 0.490 | 2-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 2.800 | 0.400 | 2-3 |
| Presentation | 3 | 2.600 | 0.490 | 2-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 5.800 | 0.980 | 4-7 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Addresses an important gap between the empirical success of Muon and its theoretical understanding.
- Provides the first claimed proof of O~(T^{-1/3}) iteration complexity for a Muon-style optimizer with variance reduction.
- Comprehensive theoretical framework covering both ergodic and non-ergodic convergence, including last-iterate guarantees under the PL condition.
- Careful identification and discussion of flaws in prior theoretical work on Muon.
- Experimental validation on both vision and language benchmarks (CIFAR-10, C4).

### Weaknesses

- The claim of 'optimal' O~(T^{-1/3}) complexity is not rigorously justified. The cited lower bound (arjevani2023lower) applies to squared gradient norm, while the paper's convergence measure is gradient norm (not squared), so the optimality claim may not directly apply to this setting with orthogonalization steps.
- Proof of Lemma E.2 (used for PL condition convergence) contains a flawed proof by contradiction; the step concluding that there must exist T_A such that G_t <= B_t for all t > T_A is not justified by the preceding argument. This undermines the rigor of Theorems 3.3 and 3.4.
- Proof of Lemma C.1 involves complex analysis of function F(t,q) with hand-wavy justification for key inequalities, making it difficult to verify.
- Experiments do not directly validate the theoretical convergence rates (e.g., no measurement of gradient norm over time to check the predicted O~(T^{-1/3}) or O~(T^{-1/4}) rates).
- Computational overhead of MVR2 (two gradient evaluations per step) and the orthogonalization step (e.g., SVD or Newton-Schulz) is acknowledged but not deeply analyzed in terms of practical trade-off.
- Presentation issues include duplicated assumptions, broken references, and incomplete sentences, which harm clarity.
- The claim that the analysis is 'free of any non-vanishing additive error term that depends on the dimension n' is misleading, as the dependence on n is standard and vanishes with diminishing step sizes.
- The theoretical analysis treats the orthogonalization step as merely a bounded-norm operation, not fully leveraging its specific properties; the proofs might work for any bounded update direction.

### Questions

- Could you clarify how the O~(T^{-1/3}) iteration complexity matches the lower bound from arjevani2023lower? The lower bound is typically stated for E[||∇f(x)||^2], but the paper's convergence measure is E[||∇f(x)||]. How does this discrepancy affect the optimality claim? Does the lower bound directly apply to Muon-style algorithms with orthogonalization constraints?
- In Lemma E.2, the proof by contradiction for the convergence of G_t is not fully rigorous. Specifically, the step 'there must exist a time T_A such that for all t>T_A, G_t <= B_t' does not follow from the preceding argument. Could you provide a more formal proof of this step?
- In Lemma C.1, the proof claims h(t) <= 0 for all t>1 without detailed justification. Could you provide a more rigorous proof of this key inequality?
- Have you considered measuring the gradient norm during training to directly validate the predicted convergence rates? If so, what were the results?
- What is the per-iteration computational cost of Muon-MVR2 compared to Muon-MVR1, including the orthogonalization step and the two gradient evaluations? How does this affect wall-clock time in practice?
- How does the orthogonalization step (computing O_t from M_t) specifically contribute to the convergence guarantees beyond just being a bounded-norm operation? Would the same proof work for any update direction with bounded norm?
- The convergence bounds depend on the matrix dimension n. For large-scale models, this dependence could be problematic. Is this dependence tight, or could it be improved?
- Could you compare with other theoretically grounded variance-reduced optimizers like STORM or MARS in the experiments?

### Limitations

- The theoretical analysis assumes smoothness and bounded variance assumptions that may not hold in practice for large language models.
- The PL condition is a strong assumption that may not hold for deep neural networks in practice.
- The computational overhead of MVR2 (two gradient evaluations per step) and the orthogonalization step is not deeply analyzed in terms of practical cost-benefit.
- Experiments are limited to relatively small-scale tasks (ResNet18 on CIFAR-10, LLaMA2-130M on C4) and do not demonstrate benefits on large-scale LLM pretraining.
- The paper does not discuss potential negative societal impacts, though this is a theory paper with limited direct societal implications.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 179,560
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 170,600
- Completion tokens: 10,515
- Reasoning tokens reported: 0
- Total tokens: 190,075
- Estimated total: $0.02685329

Full individual reviews and raw JSON responses are in `review_bundle.json`.
