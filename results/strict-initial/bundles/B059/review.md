# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B059.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.021920**

## Final Meta-review

The paper proposes an automatic step-size tuning scheme for unadjusted Hamiltonian Monte Carlo (HMC), underdamped Langevin Monte Carlo (LMC), and Microcanonical Langevin Monte Carlo (MCLMC). The method targets a user-specified asymptotic bias tolerance by controlling the energy-error variance per dimension (EEVPD). For Gaussian targets, the authors prove analytic bounds linking EEVPD to covariance-matrix bias and Wasserstein distance. They empirically test the bound on non-Gaussian Bayesian benchmarks, provide a practical adaptation algorithm, and compare unadjusted versus adjusted samplers and NUTS, reporting substantial speedups in many cases.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 4 | 3.400 | 0.490 | 3-4 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 3 | 2.800 | 0.400 | 2-3 |
| Presentation | 4 | 3.400 | 0.490 | 3-4 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.600 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important practical gap: automatic step-size selection for unadjusted samplers, which previously required manual tuning.
- Provides rigorous analytic results for Gaussian targets, showing that EEVPD upper-bounds asymptotic bias and Wasserstein distance, with sharp bounds.
- The proposed tuning algorithm is simple, computationally cheap, and demonstrated to work on a range of benchmark problems.
- Broad empirical comparison includes NUTS and adjusted/unadjusted variants of LMC and MCLMC, showing significant speedups in several realistic settings.
- The paper is well-written and provides practical guidance for setting bias tolerance via EEVPD.

### Weaknesses

- The theoretical guarantee is only proven for Gaussian targets; for non-Gaussian targets the relationship is empirical and the paper includes a counterexample (Brownian motion) where the bound under-estimates bias by about a factor of 1.5.
- The step-size adaptation algorithm is heuristic and lacks convergence guarantees, especially during the non-stationary burn-in phase.
- The claim that unadjusted methods 'significantly and consistently outperform' is not fully supported by the paper's own tables: for example, uLMC is worse than aLMC on Stochastic Volatility (Table 2) and worse on Brownian motion for b_cov (Table 3).
- The recommended bias-allocation rule (Bias^2 = RMSE^2/5) is derived from a one-dimensional Gaussian example and may not transfer to high-dimensional or non-Gaussian targets.
- The experimental setup uses NUTS to obtain a preconditioning matrix, so the unadjusted samplers are not entirely black-box, and the comparison may be somewhat favorable to them.
- The method still requires the user to specify the desired EEVPD (or bias tolerance) and the momentum decoherence length L, which may require problem-specific knowledge and tuning.

### Questions

- How should practitioners verify that the Gaussian-based EEVPD bound applies to a given non-Gaussian target, given that Brownian motion violates it?
- Can the step-size adaptation algorithm be shown to converge to the target EEVPD under reasonable assumptions, and what happens when the chain is far from stationarity during adaptation?
- How do the authors reconcile the abstract's claim of consistent improvement with the Stochastic Volatility (Table 2) and Brownian motion (Table 3) results where uLMC underperforms aLMC?
- Is the one-fifth bias-allocation rule robust across the tested benchmarks? Would a different allocation improve performance for cases where unadjusted methods underperform?
- How sensitive are the results to the use of NUTS for preconditioning, and would the tuning scheme work with a fully unadjusted warm-up?
- How is the momentum decoherence length L automatically selected in practice, and how sensitive is performance to L?

### Limitations

- Theoretical guarantees are limited to Gaussian targets; non-Gaussian extensions are only empirical and not universally reliable.
- The adaptation algorithm does not have formal convergence guarantees.
- The bias-variance trade-off heuristic is based on a simple 1D Gaussian analysis, which may be inaccurate in complex problems.
- The evaluation, while broad, does not cover all potential failure modes such as heavy-tailed or strongly multimodal distributions.
- Users are advised to validate with smaller step sizes, but the paper does not provide a fully automatic validation procedure.
- The paper does not address the choice of trajectory length for HMC or the noise scale for LMC beyond mentioning a momentum decoherence length.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 122,022
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 117,926
- Completion tokens: 19,282
- Reasoning tokens reported: 13,553
- Total tokens: 141,304
- Estimated total: $0.02192007

Full individual reviews and raw JSON responses are in `review_bundle.json`.
