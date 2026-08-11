# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B059.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.019888**

## Final Meta-review

The paper proposes an automatic step-size tuning scheme for unadjusted Hamiltonian Monte Carlo (HMC), underdamped Langevin Monte Carlo (LMC), and Microcanonical Langevin Monte Carlo (MCLMC) samplers. The key idea is to control the asymptotic bias of these samplers by monitoring the Energy Error Variance Per Dimension (EEVPD), which can be estimated online during sampling. For Gaussian targets, the authors prove rigorous upper bounds relating EEVPD to covariance matrix bias and Wasserstein distance (Theorem 4.2). They empirically demonstrate that this relationship approximately extends to non-Gaussian targets on standard Bayesian benchmarks. Based on this, they construct a practical adaptation algorithm that automatically selects step sizes to achieve a user-specified bias tolerance, making unadjusted samplers black-box usable. Comprehensive experiments show that unadjusted samplers with this tuning scheme outperform their adjusted counterparts and the No-U-Turn Sampler (NUTS) on several benchmark problems, particularly in high dimensions.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.800 | 0.400 | 3-4 |
| Quality | 3 | 3.200 | 0.400 | 3-4 |
| Clarity | 4 | 3.800 | 0.400 | 3-4 |
| Significance | 4 | 3.600 | 0.490 | 3-4 |
| Soundness | 3 | 3.200 | 0.400 | 3-4 |
| Presentation | 4 | 3.800 | 0.400 | 3-4 |
| Contribution | 4 | 3.600 | 0.490 | 3-4 |
| Overall | 7 | 7.200 | 0.400 | 7-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses a significant practical gap: automatic step-size selection for unadjusted samplers, which are known to be more efficient in high dimensions but lacked practical tuning methods.
- Provides rigorous theoretical analysis for Gaussian targets, with sharp bounds relating EEVPD to both covariance matrix bias and Wasserstein distance, supported by complete proofs.
- Comprehensive empirical validation across diverse Bayesian benchmark problems of varying dimensionality, with careful comparisons against adjusted samplers and NUTS.
- The proposed tuning scheme is practical and makes unadjusted samplers usable in a black-box manner, potentially broad impact on scientific applications.
- Clear practical guidance for selecting EEVPD targets (Table 1) based on desired bias tolerance.
- Well-written and well-organized paper with clear explanations of the methodology and honest discussion of limitations.

### Weaknesses

- Theoretical guarantees are only proven for Gaussian targets; the extension to non-Gaussian targets is purely empirical, and the Brownian motion example shows the bound can be off by a factor of ~1.5.
- The choice of EEVPD target values relies on a heuristic derived from a 1D Gaussian analysis (Appendix C), and its general applicability across different targets and quantities of interest is not well-justified.
- The step-size adaptation algorithm itself lacks convergence guarantees, as acknowledged by the authors.
- The comparison with NUTS may be somewhat unfair since NUTS requires no user-specified tolerances (or uses its own defaults), while the proposed method requires the user to provide a bias tolerance.
- Limited discussion of potential failure modes for multimodal or heavy-tailed targets, where the relationship between EEVPD and bias may break down.
- The paper does not fully explore the interaction between the momentum decoherence length L and the step-size adaptation, nor does it address full preconditioning scenarios.

### Questions

- How sensitive is the performance of the adaptation algorithm to the choice of forgetting factor γ and log-normal penalty σξ? Is there a principled way to select these hyperparameters?
- For non-Gaussian targets where the bound can be violated (e.g., Brownian motion), what properties of the target cause this violation, and is there a practical way to detect when the bound is likely to be violated?
- How robust is the 1/5 bias-to-RMSE ratio heuristic across different target distributions and different expectation functions of interest?
- How does the proposed scheme perform on multimodal or heavy-tailed targets, and does EEVPD control still provide meaningful bias bounds in such cases?
- Could the proposed scheme be extended to jointly adapt the momentum decoherence length L, rather than treating it as fixed?
- How does the performance comparison change if NUTS is given the same preconditioning information (e.g., diagonal preconditioning) as the unadjusted samplers?

### Limitations

- The theoretical bias bounds are proven only for Gaussian targets; for non-Gaussian targets, the relationship between EEVPD and bias is empirical and may not hold universally (as demonstrated by the Brownian motion example).
- The recommended EEVPD target values are based on a heuristic from a specific 1D Gaussian analysis and may not be optimal for all problems; different problems may require different values (e.g., Stochastic Volatility).
- The adaptation algorithm does not have convergence guarantees, and its hyperparameters require manual selection.
- The method requires the user to specify a bias tolerance, which may be difficult for practitioners without domain expertise.
- Potential issues with multimodal distributions, heavy tails, and time-varying targets are not addressed.
- The comparison with NUTS may not be fully fair due to differences in tuning requirements and preconditioning.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 131,886
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 122,926
- Completion tokens: 9,477
- Reasoning tokens reported: 0
- Total tokens: 141,363
- Estimated total: $0.01988829

Full individual reviews and raw JSON responses are in `review_bundle.json`.
