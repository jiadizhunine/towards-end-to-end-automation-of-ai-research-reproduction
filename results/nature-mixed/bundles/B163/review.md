# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B163.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.016998**

## Final Meta-review

This paper introduces LDC-MTL, a bilevel optimization approach for multi-task learning (MTL) that explicitly controls loss discrepancies across tasks. The lower-level problem optimizes model parameters on a weighted sum of task losses, while the upper-level problem adjusts task weights to minimize pairwise differences between normalized losses. The key algorithmic contribution is a single-loop first-order method achieving O(1) time and memory complexity by empirically dropping the inner-loop gradient term ∇_W g(W^t, z_N^t), which is observed to be orders of magnitude smaller than other gradient terms. The paper provides theoretical convergence guarantees to both stationary points of the bilevel problem and ε-accurate Pareto stationary points under assumptions including Lipschitz smoothness and PL conditions. Extensive experiments on CelebA, QM9, Cityscapes, and NYU-v2 demonstrate competitive or superior performance compared to scalarization-based and gradient manipulation baselines, with significantly reduced computational overhead. The paper also includes careful analyses of loss distribution, gradient conflicts, weight dynamics, and comparisons with weight-swept linear scalarization.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.800 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 4 | 3.600 | 0.490 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.200 | 0.400 | 3-4 |
| Overall | 6 | 6.200 | 0.400 | 6-7 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Novel bilevel optimization formulation for loss discrepancy control in MTL, providing a principled framework that connects loss balancing with Pareto optimality
- O(1) time and memory complexity is a significant practical advantage over O(K) gradient manipulation methods, enabling scalability to many-task scenarios such as CelebA with 40 tasks
- Comprehensive theoretical analysis establishing convergence to stationary points and ε-accurate Pareto stationary points, with clearly stated assumptions
- Extensive empirical evaluation across diverse datasets (classification, regression, dense prediction) with multiple baselines and careful ablations
- Empirical analysis of loss distribution, gradient conflict reduction, and comparison with weight-swept linear scalarization provides valuable insights into why the method works
- The paper honestly discusses limitations, including the trade-off between loss minimization and discrepancy control via the penalty parameter λ
- Practical efficiency demonstrated with minimal overhead compared to linear scalarization

### Weaknesses

- The key algorithmic simplification (dropping ∇_W g(W^t, z_N^t)) is justified primarily by empirical observation rather than rigorous theoretical guarantees; the additional assumption ||∇_W g(W^t, z_N^t)|| = O(ε) is not theoretically established
- The upper-level objective uses absolute values which are non-smooth; the paper mentions a soft absolute value modification but does not thoroughly analyze its impact on convergence guarantees or practical performance
- The theoretical analysis relies on the PL condition for the lower-level problem, which may not hold for general neural network settings
- The comparison with weight-swept LS is only performed on the 2-task Cityscapes dataset, limiting the strength of the claim that LDC-MTL dominates weight-swept LS in general
- The choice between τ = 1 and τ = σ(W) appears dataset-dependent without clear principled guidance for selection
- The penalty constant λ requires manual tuning per dataset, adding to the practitioner's burden
- The theoretical analysis assumes deterministic gradients and does not address the stochastic setting relevant to practical deep learning

### Questions

- Can you provide theoretical justification or broader empirical validation for the assumption ||∇_W g(W^t, z_N^t)|| = O(ε) beyond the Cityscapes experiment? Under what conditions does this term provably vanish or remain small across different architectures, datasets, and training stages?
- How does the choice of τ = 1 vs τ = σ(W) affect the theoretical guarantees? Is there a principled criterion for selecting between these options across different datasets?
- How does the soft absolute value approximation (e.g., y = sqrt(x^2 + γ)) affect the convergence guarantees? Is there a specific value of γ used in experiments, and is there a formal analysis of the approximation error?
- The weight-swept LS comparison is only on Cityscapes. Why wasn't this extended to other datasets like CelebA or QM9, where the method also shows improvements? Would such comparisons further validate the Pareto frontier claims?
- What is the sensitivity of the method to the penalty constant λ across datasets? Are there heuristics or adaptive schemes to select λ automatically without grid search?
- Does the theoretical analysis extend to the stochastic setting (e.g., mini-batch gradients)? The current analysis appears to assume deterministic gradients.
- What is the memory footprint and computational overhead of the routing function σ(W) compared to the main model, particularly for very deep architectures or very large task counts (e.g., >100 tasks)?
- The paper mentions that the training trajectory plays a key role. Could you provide more analysis on which aspects of the trajectory (e.g., early-stage weight dynamics) are most important for final performance, and whether this could be formalized?

### Limitations

- The O(1) complexity claim depends on an empirical observation that may not hold universally across all MTL scenarios, architectures, or training regimes; potential failure modes are not thoroughly discussed
- The theoretical guarantees require assumptions (Lipschitz continuity, smoothness, PL condition) that may not hold in all practical deep learning settings
- The method requires careful tuning of the penalty constant λ, which may limit its ease of use in practice
- The experimental validation is limited to supervised learning benchmarks; applicability to other MTL settings (e.g., reinforcement learning, meta-learning, federated learning) is not explored
- The paper does not deeply analyze scalability to very large-scale settings with hundreds of tasks, which would more strongly demonstrate the O(1) advantage
- Potential negative societal impact is not discussed, though the contributions are methodological and appear to have minimal direct societal implications

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 109,636
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 100,676
- Completion tokens: 10,281
- Reasoning tokens reported: 0
- Total tokens: 119,917
- Estimated total: $0.01699841

Full individual reviews and raw JSON responses are in `review_bundle.json`.
