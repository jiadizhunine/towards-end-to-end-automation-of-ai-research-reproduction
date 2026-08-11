# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B129.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.032183**

## Final Meta-review

This paper introduces a diffusion-based framework for probabilistic regression that models the full distribution of the diffusion noise, rather than just its conditional mean. The authors propose several parametric noise models (univariate Gaussian, univariate Gaussian mixture, multivariate Gaussian with low-rank/Cholesky covariance) and train them using strictly proper scoring rules (energy score, kernel score). They derive a closed-form expression for the backward diffusion distribution when the noise is a Gaussian mixture (Theorem 1). The framework is evaluated on diverse regression tasks: UCI benchmarks, autoregressive prediction (Burgers', Kuramoto-Sivashinsky, weather), and monocular depth estimation. Results show consistent improvements over a deterministic diffusion baseline, particularly in probabilistic metrics like CRPS and coverage, and the framework also provides a way to estimate epistemic uncertainty.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.600 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.632 | 2-4 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.200 | 0.400 | 3-4 |
| Presentation | 3 | 3.000 | 0.632 | 2-4 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 7 | 6.600 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel and practical approach: The paper proposes a principled way to enhance uncertainty quantification in diffusion-based regression by learning the noise distribution via scoring rules, offering a computationally efficient alternative to the sample-based method of Bortoli et al. (2025).
- Theoretical contribution: Theorem 1 provides a closed-form backward distribution for Gaussian mixture noise, enabling efficient sampling without expensive Monte Carlo estimates.
- Comprehensive evaluation: The experimental validation spans a wide range of tasks (low-dimensional UCI, high-dimensional PDEs, weather, and depth estimation), demonstrating versatility and consistent improvements over the baseline, especially in CRPS and coverage.
- Clear practical value: The framework can be easily integrated into existing diffusion architectures (e.g., Marigold) with minimal modification, making it a practical tool for uncertainty-aware prediction.
- Transparent discussion of limitations: The paper openly discusses the task-dependent choice of parameterization and over-conservative uncertainty estimates, with proposed remedies in the appendix.

### Weaknesses

- Incremental novelty relative to prior work: The core idea of using proper scoring rules to learn the noise distribution is largely inherited from Bortoli et al. (2025); the primary contribution is the parametric noise model, which is a relatively straightforward extension.
- Limited theoretical depth: The theoretical justification is mostly a re-derivation of known results (Gaussian marginalization). The proposed epistemic uncertainty estimation is heuristic and lacks rigorous theoretical or empirical validation.
- Experimental rigor concerns: Some experiments lack crucial statistical details (e.g., T2M is a single run, depth estimation lacks standard deviations). Performance gains are often marginal in RMSE, and the best parameterization is inconsistent across tasks, suggesting the advantage is not always clear-cut.
- Calibration issues: Coverage metrics frequently show C_0.95 = 1.00, indicating overconfident predictions. The proposed rescaling fix (tau) is ad-hoc, introduces an extra hyperparameter, and is not fully integrated into the main method or theoretical framework.
- Incomplete comparison with baselines: The comparison with the sample-based energy-score method (Bortoli et al.) is limited and not always favorable. The paper does not compare against standard non-diffusion UQ methods (e.g., deep ensembles, mixture density networks), leaving relative performance unclear.

### Questions

- How can a practitioner choose the best noise parameterization (diag, mix, mv) before training? Are there heuristics based on data characteristics (e.g., dimensionality, multimodality) or computational budget?
- Given that RMSE gains are often marginal, in what specific scenarios do you expect the proposed method to significantly improve point prediction accuracy over the standard diffusion baseline?
- The epistemic uncertainty estimates are qualitatively promising. Have you considered a quantitative evaluation, such as using them for out-of-distribution detection or comparing them against the variance of an ensemble of deterministic diffusion models?
- Could you provide a comparison against classical probabilistic regression methods, such as deep ensembles or mixture density networks, on the UCI benchmarks to contextualize the gains in UQ?
- In Appendix E, the covariance rescaling parameter tau is introduced to improve calibration. Is this applied only at inference or also during training? How is the optimal tau selected in practice?
- Your framework uses the CRPS/energy score. Have you explored the impact of the kernel bandwidth gamma for the Gaussian kernel score on the final performance and uncertainty estimates?
- How sensitive are the results to the number of diffusion steps T? Does the advantage of the proposed method diminish with more steps?
- For the T2M task, the coverage for the proposed methods is notably worse (0.83-0.84 vs 0.97 for the baseline). Why is this not addressed more prominently, and does the rescaling fix (tau) help here?
- What is the computational cost of sampling at inference time for the different parameterizations, especially the multivariate Gaussian with low-rank covariance?
- The sample-based method (Bortoli et al., 2025) is not evaluated on the T2M and depth estimation tasks. What were the computational or practical constraints that prevented this comparison?
- For the multivariate Gaussian parameterization, how was the rank r of the low-rank approximation chosen for the depth estimation task? Was there a sensitivity analysis performed?
- In the main experiments, what specific scoring rule (energy or kernel) and hyperparameters (e.g., beta for energy, gamma for kernel) were used for each of the proposed parameterizations?

### Limitations

- The choice of noise parameterization is task-dependent and requires manual selection; there is no principled guidance for selecting the best variant, limiting practical deployment.
- The proposed epistemic uncertainty estimates are heuristic and not rigorously validated (e.g., no out-of-distribution detection or comparison with ensemble methods).
- The method can lead to overconfident predictions (coverage near 1.0), and the proposed rescaling fix is not theoretically grounded or fully integrated into the main analysis.
- The computational cost increases with the complexity of the noise model (e.g., mixture or full covariance), which may limit scalability to very high-dimensional problems.
- The paper does not compare against strong non-diffusion UQ baselines (e.g., deep ensembles, MC-dropout), leaving the relative performance unclear.
- Potential negative societal impact is not discussed; given the safety-critical applications (weather forecasting, depth estimation), miscalibrated uncertainty estimates could lead to poor decision-making in high-stakes scenarios.
- The paper does not address potential biases in the training data or fairness of the uncertainty estimates across different population subgroups.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 216,099
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 207,139
- Completion tokens: 11,279
- Reasoning tokens reported: 0
- Total tokens: 227,378
- Estimated total: $0.03218267

Full individual reviews and raw JSON responses are in `review_bundle.json`.
