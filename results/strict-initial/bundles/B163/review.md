# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B163.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **5/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.023019**

## Final Meta-review

The paper proposes LDC-MTL, a bilevel optimization approach for multi-task learning (MTL) that controls loss discrepancies among tasks. The lower-level problem minimizes a weighted sum of task losses where the weights come from a routing network, and the upper-level problem adjusts the routing weights to minimize gaps between (weighted) task losses. The authors design a single-loop first-order algorithm that avoids second-order gradients and inner loops, claiming O(1) time and memory overhead relative to the number of tasks. They provide theoretical convergence guarantees to stationary points of a penalized bilevel problem and, under additional assumptions, to epsilon-accurate Pareto stationary points. Experiments on CelebA, QM9, Cityscapes, and NYU-v2 report competitive accuracy and efficiency compared to scalarization and gradient manipulation baselines, along with analyses of loss concentration, gradient conflicts, and training dynamics. Reviewers agree the core idea is novel and promising, but they raise substantial concerns about the validity of the theoretical claims, the completeness of the empirical presentation, and several ambiguities in the formulation and implementation.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.000 | 0.000 | 2-2 |
| Clarity | 2 | 2.000 | 0.000 | 2-2 |
| Significance | 2 | 2.200 | 0.400 | 2-3 |
| Soundness | 2 | 2.000 | 0.000 | 2-2 |
| Presentation | 2 | 2.000 | 0.000 | 2-2 |
| Contribution | 2 | 2.000 | 0.000 | 2-2 |
| Overall | 4 | 3.800 | 0.400 | 3-4 |
| Confidence | 5 | 4.000 | 0.000 | 4-4 |

### Strengths

- The bilevel formulation for loss discrepancy control is novel and provides a principled connection between MTL weighting and Pareto stationarity.
- The proposed single-loop first-order algorithm is simple and, in reported efficiency comparisons, shows much lower overhead than gradient manipulation methods.
- The theoretical analysis provides a formal link between stationary points of the penalized bilevel problem and Pareto stationarity under standard smoothness and PL assumptions.
- The experimental evaluation covers diverse benchmarks (classification, regression, dense prediction) and includes comparisons with weight-swept linear scalarization and analyses of loss distributions, gradient conflicts, and task-weight evolution, offering insight beyond final accuracy numbers.
- The paper addresses an important scalability limitation of gradient manipulation methods by avoiding inner optimization loops and per-task gradient storage.

### Weaknesses

- The main empirical results are not fully present: multiple tables (e.g., Tables 1, 2, 6, 7) appear without numerical entries and most figures are missing, preventing verification of the claimed accuracy and efficiency improvements.
- The convergence guarantee for the simplified single-loop algorithm (Algorithm 4.3) relies critically on an unproven empirical observation that ||∇_W g(W^t,z_N^t)|| = O(ε), rather than on a rigorous assumption or bound; this undermines the theoretical contribution.
- The Pareto-stationarity guarantee is conditional on the stationary point being a local/global solution of the penalized problem, which is not guaranteed by the convergence theorem and is not established for non-convex settings.
- The routing network σ(W) is described as taking shared features (which depend on model parameters x) as input, but the mathematical formulation treats σ as depending only on W. This inconsistency affects the derivation of gradients and the exact implementation of the lower-level problem.
- The O(1) time/memory complexity claim is misleading: computing the weighted sum of losses still requires evaluating and backpropagating through all K task heads, so the per-iteration cost is O(K); the method only reduces additional overhead beyond standard scalarization, not absolute independence from K.
- The upper-level objective uses non-smooth absolute values, but the theoretical analysis assumes smoothness; the paper only mentions a soft absolute approximation without specifying its use in experiments or analyzing its effect on guarantees.
- The paper lacks a formal pseudocode for the main algorithm in the main text, and several definitions/theorems are repeated, hurting clarity and reproducibility.
- When τ=1, the upper-level objective f(W,x) does not depend on W, making it unclear how the algorithm controls loss discrepancy in that configuration; the paper does not provide the explicit gradient update for this case.

### Questions

- Can the authors provide the complete numerical tables with standard deviations for all datasets and baselines, and clarify the sign convention of Δm% for regression tasks?
- How exactly is the routing function σ(W) parameterized? Does it depend on shared features (and thus on x)? If so, how is the dependency handled when computing gradients of the lower-level objective?
- Can the assumption ||∇_W g(W^t,z_N^t)|| = O(ε) be theoretically justified or guaranteed by the algorithm design? What happens if this condition does not hold?
- What is the precise per-iteration time and memory complexity in terms of K and the model dimension? Does the O(1) claim account for the forward/backward passes through all task heads and the router network?
- When τ=1, the upper-level objective is independent of W. What is the explicit update rule for W, and how does the method reduce loss discrepancy in that setting?
- How is the non-smooth absolute value in the upper-level objective implemented in practice? Is a smooth approximation used, and if so, how is the smoothing parameter chosen and how does it affect the theory?
- Why is the upper-level objective defined as adjacent absolute differences in a fixed task order? Would using all pairwise differences or a permutation-invariant discrepancy measure change the behavior?
- How should practitioners select the penalty constant λ? Is grid search required, and how sensitive are the results to λ across datasets?

### Limitations

- The theoretical guarantees require strong assumptions (Lipschitz smoothness, PL condition) that may not hold for deep neural networks or the actual non-smooth upper-level objective.
- The simplified algorithm's convergence guarantee depends on an empirical gradient-vanishing condition that is not proven, limiting the practical applicability of the theory.
- The method introduces additional hyperparameters (penalty λ, router architecture, choice of τ and normalization) that need tuning per dataset, reducing its simplicity.
- The experiments are limited to four moderate-scale benchmarks; scalability to large-scale, real-world MTL settings is not demonstrated.
- The paper does not discuss potential negative societal impacts or broader ethical considerations, though the method itself is unlikely to pose specific ethical concerns.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 101,246
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 97,150
- Completion tokens: 33,595
- Reasoning tokens reported: 26,337
- Total tokens: 134,841
- Estimated total: $0.02301907

Full individual reviews and raw JSON responses are in `review_bundle.json`.
