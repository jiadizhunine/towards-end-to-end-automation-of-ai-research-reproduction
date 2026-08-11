# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B129.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.030471**

## Final Meta-review

The paper proposes a diffusion-based probabilistic regression framework that models the full conditional distribution of the diffusion noise p_theta^epsilon(epsilon_t|x_t) instead of only its mean. It trains with strictly proper scoring rules (energy and kernel scores) and considers several parametric noise models: diagonal Gaussian, univariate Gaussian mixture, and multivariate Gaussian with low-rank/Cholesky covariance. Closed-form reverse distributions are derived for these families. The approach is evaluated on UCI regression, autoregressive PDE/weather forecasting, and monocular depth estimation, reporting improvements in RMSE/CRPS and uncertainty estimates compared to standard diffusion baselines, and also provides epistemic uncertainty estimates.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 2 | 2.200 | 0.400 | 2-3 |
| Quality | 2 | 2.000 | 0.632 | 1-3 |
| Clarity | 2 | 2.200 | 0.748 | 1-3 |
| Significance | 2 | 2.000 | 0.000 | 2-2 |
| Soundness | 2 | 2.000 | 0.632 | 1-3 |
| Presentation | 2 | 2.200 | 0.748 | 1-3 |
| Contribution | 2 | 2.000 | 0.000 | 2-2 |
| Overall | 4 | 3.800 | 0.400 | 3-4 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- The idea of parameterizing the noise distribution with closed-form families is a useful extension of Bortoli et al. (2025), reducing computational cost relative to sample-based scoring-rule diffusion.
- Extensive evaluation across diverse tasks with multiple probabilistic metrics (RMSE, CRPS, ES, NLL, coverage).
- The method is architecture-agnostic and can be integrated into existing diffusion models (e.g., Marigold for depth).
- Provides a way to obtain epistemic uncertainty estimates, which standard diffusion regression lacks.

### Weaknesses

- Limited novelty: core concept of learning noise distribution with scoring rules already exists; the paper mainly changes from nonparametric samples to parametric forms.
- Calibration is not consistently achieved; coverage is far from nominal (e.g., 1.00 on PDEs, 0.84 on T2M), and a post-hoc covariance rescaling tau is introduced in the appendix, indicating the method does not inherently produce calibrated uncertainties.
- Theoretical justification is incomplete: no analysis of why proper scoring on epsilon_t improves the final predictive distribution, and some reviewers claim Theorem 1 contains algebra errors.
- Best parameterization is task-dependent (diag/mix vs. mv), with no principled selection criterion, complicating practical use.
- Epistemic uncertainty estimates are heuristic and unvalidated against OOD detection or ground truth.
- Missing comparisons to standard probabilistic regression baselines (e.g., deep ensembles, MC dropout), and some experiments lack error bars or statistical significance.

### Questions

- How does the proposed parametric noise modeling relate to modeling the final target distribution, and is there theoretical support that minimizing scoring rules on epsilon_t improves predictive calibration?
- Why is calibration inconsistent across tasks (overconfident on PDEs, underconfident on T2M), and how should practitioners select the post-hoc rescaling tau?
- What evidence supports the epistemic uncertainty estimates, and could they be compared to established methods like ensembles?
- How should one choose among the proposed noise parameterizations and hyperparameters (K, rank, kernel bandwidth)?
- Are the reported improvements statistically significant given that some experiments are single runs and many differences are within standard deviations?

### Limitations

- No theoretical guarantee of calibration or properness of the final predictive distribution.
- The method requires the choice of noise distribution family and several hyperparameters, with limited guidance.
- Calibration often falls below nominal coverage without ad-hoc post-processing.
- Epistemic uncertainty estimation is heuristic and lacks rigorous validation.
- The multivariate covariance parameterization can be computationally expensive, and no thorough cost-benefit analysis is provided.
- The evaluation compares only diffusion-based baselines, not established non-diffusion probabilistic regression methods.
- Negative societal impacts are not discussed, though not specific to this work.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 196,780
- Cache-hit prompt tokens: 41,344
- Cache-miss prompt tokens: 155,436
- Completion tokens: 30,692
- Reasoning tokens reported: 24,515
- Total tokens: 227,472
- Estimated total: $0.03047056

Full individual reviews and raw JSON responses are in `review_bundle.json`.
