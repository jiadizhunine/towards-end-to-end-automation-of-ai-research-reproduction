# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B034.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.031746**

## Final Meta-review

The paper proposes CUSAL, an active learning acquisition function that prioritizes querying samples with high estimated per-sample calibration error, using model uncertainty as a tie-breaker. It introduces a kernel-based calibration error estimator designed for the covariate shift induced by active learning, provides theoretical consistency and calibration-error bounds, and reports experiments on MNIST, FMNIST, SVHN, CIFAR-10, CIFAR-10-LT, and ImageNet comparing ECE and accuracy against multiple active learning baselines.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 1.800 | 0.400 | 1-2 |
| Clarity | 2 | 2.400 | 0.490 | 2-3 |
| Significance | 2 | 2.400 | 0.490 | 2-3 |
| Soundness | 2 | 1.800 | 0.400 | 1-2 |
| Presentation | 2 | 2.400 | 0.490 | 2-3 |
| Contribution | 2 | 2.000 | 0.000 | 2-2 |
| Overall | 4 | 3.800 | 0.400 | 3-4 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important and underexplored problem: calibration in active learning, proposing calibration error itself as an acquisition criterion.
- The lexicographic combination of calibration error and uncertainty is intuitive, and the ablation studies (frequency of calibration vs. uncertainty selection, bandwidth sensitivity, query size, combination with diversity) are useful.
- Extensive empirical evaluation across six datasets, including a long-tailed benchmark and ImageNet, showing consistent improvements in unlabeled-pool ECE and often competitive or better accuracy.
- Attempts to theoretically analyze covariate shift in calibration estimation, which is a valuable direction despite gaps.

### Weaknesses

- Theorem 4.1's consistency proof is flawed: under covariate shift, P(Y|X) invariance does not imply E_S[Y|h(X)] = E_U[Y|h(X)]; the estimator lacks importance weighting or density-ratio correction, and the MSE bound exponent is inconsistent with standard kernel smoothing rates.
- Theorem 4.2 is conditional/circular: it assumes the selected queried points have average calibration error ≤ ε and an unbiased estimator, without showing that the algorithm guarantees this; the proof also contains an inequality in the wrong direction.
- The kernel calibration estimator's O(n_t * m_t) cost per round is not analyzed and no scalable approximation is provided, making the ImageNet experiments difficult to assess; the fixed bandwidth b=0.001 is not justified.
- Empirical statistical significance is not demonstrated; many ECE differences are small with overlapping error bars, and no details of significance tests are given.
- The theoretical objective (CE_p) is not formally linked to the binned ECE reported in the experiments, creating a disconnect between theory and empirical validation.
- Presentation issues: the lexicographic order formalization is confusing and inconsistent with the implementation, duplicated theorem/definition headers appear, and code contains undefined variables.

### Questions

- What exact assumptions beyond covariate shift are needed in Theorem 4.1 to justify E_S[Y|h(X)] = E_U[Y|h(X)]? Does the estimator require importance weighting by dP_U(X)/dP_S(X)?
- In Theorem 4.2, how is the assumption that the trained model has average calibration error ≤ ε on the queried points guaranteed? Is the theorem vacuous if this is not ensured by the acquisition procedure?
- How was the kernel calibration estimator made computationally tractable on ImageNet? What is the wall-clock time overhead compared to uncertainty-based baselines?
- Since calibration-error estimates are continuous, are exact ties possible? Does the lexicographic acquisition reduce to pure calibration-error selection in practice, and how was the classification in Table 5 made?
- How do the theoretical bounds on CE_p relate to the binned ECE reported in the experiments? Could a method improve CE_p without improving ECE, or vice versa?
- What exact statistical significance test was used? Are the reported ECE/accuracy improvements significant across all datasets and query steps?

### Limitations

- The theoretical guarantees rest on unproven assumptions and do not rigorously support the claimed consistency or calibration-error bounds.
- The kernel-based estimator has computational complexity growing with both labeled and unlabeled pool sizes, limiting scalability; no efficient approximation or runtime analysis is provided.
- The empirical evaluation is confined to image classification; evidence on other modalities or regression is absent.
- Some baseline comparisons may be unfair; e.g., Least-conf-TS uses a portion of labeled data for temperature scaling, reducing training data.
- The paper does not discuss potential negative societal impacts or failure modes in high-stakes active learning settings where calibration is critical.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 173,382
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 169,286
- Completion tokens: 28,696
- Reasoning tokens reported: 22,802
- Total tokens: 202,078
- Estimated total: $0.03174639

Full individual reviews and raw JSON responses are in `review_bundle.json`.
