# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B192.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 3, 'Reject': 2}
- Estimated API cost: **$0.014842**

## Final Meta-review

The paper proposes Dynamic Guidance, a sampling-time method to mitigate hallucinations in diffusion models. At each denoising step, a noisy-sample classifier selects the most probable class, and classifier guidance is applied toward that dynamically chosen class, selectively sharpening the score function along hallucination-prone directions while preserving benign variations. The method is evaluated on a 2D Gaussian toy dataset, controlled shape datasets, a hands dataset, and ImageNet, showing hallucination reduction in controlled settings and improvements in precision and Inception Score on ImageNet.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 2 | 2.400 | 0.490 | 2-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 2 | 2.400 | 0.490 | 2-3 |
| Contribution | 3 | 2.800 | 0.400 | 2-3 |
| Overall | 4 | 5.200 | 0.980 | 4-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The idea of dynamically selecting the guidance target at each timestep is novel, simple, and well motivated by the mode-interpolation view of hallucinations.
- The paper provides a convincing analysis of score-function sharpening using a beta-VAE, showing that Dynamic Guidance affects hallucination-related latent dimensions while leaving others intact.
- Experiments on controlled datasets demonstrate substantial hallucination reduction, especially with few-step DDIM sampling, which is practically relevant.
- The approach is the first to address hallucinations at generation time rather than through post-hoc filtering, avoiding wasted computation.
- The method is simple to implement on top of existing classifier guidance and requires no training at generation time.

### Weaknesses

- The method relies on a noisy-sample classifier with class labels that align with hallucination directions, which is unavailable in many applications such as unconditional and text-to-image generation.
- On ImageNet, the claimed hallucination reduction is based solely on proxy metrics (precision, Inception Score) that are sensitive to class distribution; the observed class imbalance and reduced recall suggest improvements may stem from distribution bias rather than genuine hallucination reduction.
- The comparison set is narrow: only variance filtering and static classifier guidance are considered. Recent guidance methods (e.g., Karras et al., Kynkäänniemi et al.) are not empirically compared, weakening the claim of outperforming baselines.
- The hands dataset evaluation uses only 100 manually labeled samples with no inter-annotator reliability or statistical significance, making the results subjective and non-reproducible.
- The paper lacks rigorous theoretical justification for why dynamic label selection prevents hallucination; the explanation is heuristic.
- Presentation issues, including missing figures, inconsistent table references, and unclear hyperparameter choices (guidance interval, guidance scale), hinder reproducibility.
- Dynamic Guidance can introduce class bias and reduce sample diversity, especially at high guidance scales; the proposed stratified sampling is a post-hoc fix rather than an inherent property.

### Questions

- How are the guidance interval boundaries T1 and T2 chosen, and how sensitive are the results to these hyperparameters?
- On ImageNet, how much of the precision and Inception Score improvement is due to class distribution shift rather than genuine hallucination reduction? Could class-balanced metrics or per-class precision/recall be reported?
- How does Dynamic Guidance compare to other adaptive guidance or interval-based guidance methods, such as limited-interval guidance?
- Can Dynamic Guidance be extended to text-to-image models where class labels are not predefined?
- What happens when the classifier is uncertain or inaccurate? Does dynamic selection cause oscillation or mode hopping during sampling?
- What is the computational overhead of Dynamic Guidance compared to standard classifier guidance?
- How does the choice of the guidance scale λ affect the balance between hallucination reduction and diversity? Are there ablations?

### Limitations

- Requires a pre-trained noisy-sample classifier and a label space that meaningfully aligns with hallucination directions, limiting applicability to class-conditional settings.
- Introduces class imbalance and can reduce diversity, as observed in ImageNet experiments.
- Evaluation on natural images relies on proxy metrics; direct hallucination detection is not performed, so actual hallucination reduction at scale is unverified.
- The hand dataset evaluation is small-scale and subjective, with no detailed annotation protocol.
- Hyperparameters (guidance scale, interval) require per-dataset tuning; no automatic selection method is provided.
- The method does not address hallucinations arising from text conditioning or prompt misalignment.
- Potential negative societal impacts include amplification of classifier biases and potential misuse for generating more convincing deepfakes.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 70,829
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 66,733
- Completion tokens: 19,599
- Reasoning tokens reported: 14,039
- Total tokens: 90,428
- Estimated total: $0.01484181

Full individual reviews and raw JSON responses are in `review_bundle.json`.
