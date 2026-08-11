# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B192.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.012578**

## Final Meta-review

The paper introduces Dynamic Guidance, a method to mitigate hallucinations in diffusion models by adaptively selecting the guidance target class at each denoising step. Unlike static classifier guidance which fixes a condition from the start, Dynamic Guidance uses a noisy-sample classifier to identify the most likely mode given the current noisy state, and applies classifier guidance toward that dynamically selected class. This selectively sharpens the score function along hallucination-inducing directions while preserving valid semantic interpolations. The method is evaluated on a 2D Gaussian toy dataset, controlled shape datasets (Single/Mixed Shapes), a hands dataset, and ImageNet. Results show substantial hallucination reduction in controlled settings and improvements in proxy metrics (precision, Inception Score) on ImageNet, particularly with few-step DDIM sampling, outperforming static classifier guidance and variance filtering baselines.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.800 | 2-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.200 | 0.400 | 3-4 |
| Significance | 3 | 3.000 | 0.632 | 2-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.200 | 0.400 | 3-4 |
| Contribution | 3 | 3.000 | 0.632 | 2-4 |
| Overall | 6 | 6.000 | 0.632 | 5-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important and timely problem: hallucinations in diffusion models, with a novel approach that intervenes during sampling rather than post-hoc detection.
- Simple and conceptually clear method: dynamically selecting guidance targets based on the current noisy sample is an elegant improvement over static guidance.
- Comprehensive evaluation across multiple settings from toy data to large-scale ImageNet, demonstrating broad applicability.
- Provides insightful mechanistic analysis using β-VAE latents to visualize score function sharpening, supporting the intuition behind the method.
- Works with practical few-step DDIM sampling, addressing a real deployment concern.
- Clear improvements over static classifier guidance and variance filtering baselines in most settings.
- Authors honestly acknowledge limitations such as class bias and the need for a noisy-sample classifier.

### Weaknesses

- The definition of 'hallucination' is dataset-specific and somewhat ad-hoc, making the evaluation methodology hard to generalize to open-domain generation.
- ImageNet evaluation relies on proxy metrics (precision, Inception Score) rather than direct hallucination measurement, weakening claims in that setting.
- The method introduces class bias, leading to over-representation of certain classes; the balanced correction in the appendix is post-hoc and not fully integrated.
- Requires a trained classifier on noisy samples, which may not be available or easily trainable in all settings (e.g., text-to-image).
- Comparison with variance filtering is somewhat unfair since it is a detection method, not a prevention method.
- Hands dataset evaluation uses only 100 samples with manual labeling, which is statistically limited.
- No formal theoretical justification for why dynamic class selection should outperform static guidance, beyond intuition and empirical results.
- Limited comparison to recent hallucination mitigation methods or guidance interval techniques (e.g., Kynkäänniemi et al. 2024).

### Questions

- How sensitive is Dynamic Guidance to the quality of the noisy-sample classifier? Have you tested with classifiers of varying accuracy or calibration?
- Can Dynamic Guidance be extended to classifier-free guidance or text-to-image settings where no explicit classifier is available?
- The class bias issue on ImageNet seems significant. How severe is it in practice, and what mitigation strategies beyond stratified sampling could be employed?
- What is the computational overhead of Dynamic Guidance compared to static classifier guidance?
- How should practitioners choose the guidance interval [T1, T2]? Is there a heuristic or sensitivity analysis?
- Have you considered using the classifier's full probability distribution or uncertainty estimates instead of hard argmax selection?
- For the hands dataset, why only 100 samples? Would a larger evaluation with automated metrics be more convincing?
- How does Dynamic Guidance affect diversity beyond recall metrics? Are certain modes over-represented?
- Could the method be extended to text-guided generation where hallucinations are also prevalent?

### Limitations

- The method requires a classifier trained on noisy samples, which adds training overhead and may not be available in all applications.
- Classifier bias can propagate to sampling trajectories, leading to class preference and skewed generation distributions.
- Hallucination definitions are dataset-specific and may not generalize to real-world scenarios or open-domain generation.
- ImageNet evaluation relies on proxy metrics that may not directly measure hallucination reduction.
- The method does not address hallucinations arising from text-image misalignment.
- Evaluation on the hands dataset is limited to 100 samples with manual labeling.
- Potential negative societal impact: biased generation could reinforce stereotypes if classifiers are biased, and improved generation could be used to create more convincing deepfakes or misleading content.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 79,957
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 70,997
- Completion tokens: 9,334
- Reasoning tokens reported: 0
- Total tokens: 89,291
- Estimated total: $0.01257819

Full individual reviews and raw JSON responses are in `review_bundle.json`.
