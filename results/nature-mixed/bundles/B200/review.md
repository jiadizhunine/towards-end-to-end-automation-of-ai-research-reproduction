# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B200.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.022030**

## Final Meta-review

This paper introduces Diffusion-DFL, the first decision-focused learning (DFL) approach that leverages diffusion probabilistic models to capture uncertainty in stochastic optimization problems. The authors propose two training methods: (1) a reparameterization estimator that differentiates through the diffusion sampling process, and (2) a lightweight score function estimator that approximates gradients using the ELBO as a surrogate for the log-likelihood score, avoiding backpropagation through sampling. The score function method reduces GPU memory from 60.75 GB to 0.13 GB while achieving comparable decision quality. The authors evaluate their approach on synthetic product allocation, power scheduling, and stock portfolio optimization tasks, demonstrating consistent improvements over deterministic and Gaussian DFL baselines, as well as two-stage methods and offline contextual bandits.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.800 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 4 | 3.800 | 0.400 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 4 | 3.800 | 0.400 | 3-4 |
| Overall | 7 | 6.800 | 0.400 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel contribution: First paper to integrate diffusion models into decision-focused learning for stochastic optimization, addressing a clear gap in DFL methods that rely on deterministic point predictions or simple parametric distributions.
- Two complementary gradient estimators (reparameterization and score function) with clear computational trade-offs, providing practical flexibility.
- The score function estimator provides significant computational savings (460x GPU memory reduction) while maintaining decision quality, making the method more practically applicable.
- Theoretical justification for the ELBO gradient approximation (Proposition 5.1) with a bound based on KL divergence, providing some grounding for the heuristic.
- Comprehensive experimental evaluation across three diverse tasks (synthetic, power scheduling, portfolio optimization) with strong baseline comparisons including deterministic DFL, Gaussian DFL, two-stage methods, and offline contextual bandits.
- Consistent improvements over baselines across all tasks, with good ablation studies on sample size, variance reduction, and problem dimensionality.
- Open-source code provided for reproducibility.

### Weaknesses

- The ELBO gradient approximation (Eq. 8) is heuristic; the error bound in Proposition 5.1 depends on assumptions (bounded score functions and small KL divergence) that may not hold in practice, and no empirical verification of these quantities is provided.
- Missing comparison with Gen-DFL (Wang et al., 2025), the most closely related work using normalizing flows for generative DFL, which weakens the claim of being the first and best generative DFL approach.
- The empirical validation of the ELBO gradient approximation (Figure 2) uses a simplified linear model, not the actual non-linear diffusion models used in the main experiments.
- Some figure references are broken (e.g., '??' in Section 7.2), indicating incomplete editing and reducing clarity.
- The importance sampling variance reduction strategy is directly borrowed from Improved DDPM without novel adaptation or thorough analysis specific to the DFL setting.
- No wall-clock training time comparison between reparameterization and score function methods; only memory usage is reported.
- Experiments are limited to decision dimensions up to 100, so scalability to larger problems is not fully demonstrated.
- The comparison to offline contextual bandits is limited to a single policy-based implementation without considering pessimistic or conservative approaches.

### Questions

- How sensitive is the score function estimator to the choice of k (number of sampled diffusion timesteps)? Is there a theoretical or empirical guideline for selecting k?
- What is the actual KL divergence between forward and reverse processes during training? Is the bound in Proposition 5.1 meaningful in practice?
- Why was Gen-DFL (Wang et al., 2025) not included as a baseline, given it is the most closely related work? How does Diffusion-DFL compare against normalizing flow-based generative DFL approaches?
- What is the wall-clock training time per epoch for the reparameterization method compared to the score function method?
- How is the importance sampling distribution pt ∝ sqrt(E[||∇θ(ELBOt)||²]) estimated in practice? Is it computed once or updated periodically?
- For the stock portfolio task, how would performance compare if using a Gaussian predictor with a full covariance matrix instead of a diagonal covariance?
- Could the authors provide a comparison case where the true distribution is unimodal to show whether diffusion DFL still provides benefits over Gaussian DFL in such settings?
- How does the score function estimator's performance degrade with increasing decision dimension d? Does the method scale to problems beyond 100 dimensions?
- What exactly is the 'small regularizer' mentioned in Appendix A.10, and how was it chosen?

### Limitations

- The theoretical analysis assumes bounded score functions and small KL divergence between forward and reverse processes, which may not hold during early training stages, potentially leading to biased gradient estimates.
- The method requires solving a KKT system at each training step, which may become computationally prohibitive for very large-scale optimization problems.
- The method is derived for affine constraints; extension to general convex constraints is mentioned but not fully developed or empirically validated.
- The synthetic experiment lacks contextual features, limiting the demonstration of conditional diffusion modeling capabilities.
- The paper does not discuss potential negative societal impacts, particularly for the financial portfolio application where the method could potentially be used for high-frequency trading or other activities with systemic risks.
- The empirical validation of the ELBO gradient approximation is limited to a simple linear model case, not the full neural network diffusion models used in experiments.
- The paper does not address the calibration between decision quality and distributional accuracy of the diffusion model.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 144,543
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 135,583
- Completion tokens: 10,799
- Reasoning tokens reported: 0
- Total tokens: 155,342
- Estimated total: $0.02203043

Full individual reviews and raw JSON responses are in `review_bundle.json`.
