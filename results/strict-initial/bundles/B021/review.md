# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B021.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 2, 'Reject': 3}
- Estimated API cost: **$0.018456**

## Final Meta-review

The paper proposes Contrastive Conditional-Unconditional Alignment (CCUA), a training framework for class-conditional diffusion models on long-tailed data. It introduces two losses: an Unsupervised Contrastive Loss (UCL) that uses negative samples to push apart latent representations of different noisy images, increasing diversity especially for tail classes; and an Alignment Loss (AL) that minimizes the difference between conditional and unconditional noise predictions, weighted toward large timesteps so early denoising steps are class-agnostic, encouraging knowledge sharing from head to tail classes. The method is applied to both DDPM (U-Net) and SiT (Diffusion Transformer) pipelines, with optional batch resampling. Experiments on ImageNet-LT, TinyImageNet-LT, Places-LT, and CIFAR-LT show FID, KID, and Recall improvements over baselines such as DDPM, CBDM, OCLT, and Dispersive Loss, along with qualitative evidence of reduced mode collapse.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 2 | 2.600 | 0.490 | 2-3 |
| Quality | 3 | 2.600 | 0.490 | 2-3 |
| Clarity | 2 | 2.400 | 0.490 | 2-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 2 | 2.600 | 0.490 | 2-3 |
| Presentation | 2 | 2.400 | 0.490 | 2-3 |
| Contribution | 3 | 2.600 | 0.490 | 2-3 |
| Overall | 4 | 4.800 | 0.980 | 4-6 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- The proposed CCUA is simple and plug-and-play, requiring only two additional loss terms that can be integrated into standard diffusion training pipelines (DDPM and SiT) without architectural changes.
- The two losses directly target the core issues of long-tailed generation: UCL increases intra-class diversity to mitigate mode collapse, while AL facilitates knowledge sharing from head to tail classes by aligning conditional and unconditional denoising at early steps.
- Extensive experiments on multiple long-tailed benchmarks (ImageNet-LT, TinyImageNet-LT, Places-LT, CIFAR10/100-LT) demonstrate consistent improvements in FID, KID, and Recall over several strong baselines, with ablations confirming the contribution of each loss component.
- The paper provides qualitative visualizations and distribution analyses (t-SNE and KDE) showing reduced mode collapse for tail classes, and demonstrates that batch resampling, which usually hurts baseline methods, becomes beneficial when combined with UCL.
- The alignment loss is carefully weighted by timestep, focusing on the initial denoising steps where class-conditional and unconditional generation are observed to be similar, which is a reasonable extension of prior GAN-based approaches.

### Weaknesses

- The unsupervised contrastive loss with negative samples only is essentially a repulsive/dispersion loss without positive pairs; its formulation closely resembles the concurrent dispersive loss (Wang & He, 2025), and the claimed novelty is mainly the application to the unconditional latent space combined with alignment, which is not deeply justified theoretically.
- The alignment loss is derived from KL divergence but simplified to an MSE on noise predictions; the choice of linear timestep weighting t/T is heuristic, and the paper does not analyze how this alignment affects class-conditional controllability or whether it might reduce head-class diversity.
- The evaluation methodology may favor the proposed method: CFG strength is grid-searched independently per method, but the search ranges and criteria are not fully specified; moreover, DiffROP (discussed in related work) is not included in the empirical comparison.
- Training time is increased substantially (1.6x for DDPM, 1.48x for SiT), yet the paper does not discuss the computational cost-benefit trade-off or whether the gains are worth the overhead.
- The claim that head-class quality is maintained is only partially supported: in Table 3 on TinyImageNet-LT, the head-class FID of CCUA (21.32) is slightly worse than DDPM (21.27), and the paper does not report per-head-class metrics on ImageNet-LT.
- The paper lacks a sensitivity analysis for key hyperparameters (alpha, gamma, tau) and does not explore how their values affect performance.
- The writing contains typos and incomplete implementation details (e.g., exact values of alpha/gamma, augmentation choices, architecture specifics), which hinders reproducibility.
- On ImageNet-LT, the main improvement seems to come from batch resampling rather than the proposed losses alone: in Table 5, CCUA without batch resample (FID 32.25) is worse than SiT with batch resample (FID 28.05), and only the combination yields the best result. This undermines the claimed contribution of the losses.
- No comparison with recent class-imbalanced diffusion methods such as DiffROP (Yan et al., 2024), nor experiments with score-based diffusion models as claimed in the abstract.
- The theoretical justification for UCL is superficial; the claim that the loss pushes embeddings to a uniform distribution on a hypersphere is not rigorously analyzed, and the effect on diversity is not formally proven.

### Questions

- How does CCUA compare empirically to DiffROP (Yan et al., 2024), which also uses contrastive learning for long-tailed diffusion models? The related work discusses it, but no experiments are shown.
- Is the improvement of CCUA over Dispersive Loss (Wang & He, 2025) consistent on other datasets beyond ImageNet-LT, or is it specific to that setup?
- How sensitive are the results to the hyperparameters alpha, gamma, and tau? Are the same values used across all datasets and architectures, and were they tuned via validation?
- Does the alignment loss reduce the distinguishability of different classes in the early denoising steps? For a fixed noise, are the generated images for different classes still clearly separated after the initial steps?
- What is the criterion for applying batch resampling only on certain datasets (ImageNet-LT and TinyImageNet-LT) and not on Places-LT or CIFAR-LT? How does it interact with the alignment loss in those cases?
- How is the unsupervised contrastive loss computed when samples within a batch have different timesteps t? Do you standardize the noise level across the batch or use a time-aware normalization?
- Are the latent embeddings h normalized before computing the contrastive loss? If not, how does the scale of h affect the temperature parameter tau and the loss dynamics?
- Algorithm 1 is mentioned in the text but not included in the provided submission. Can the full training procedure be described in the appendix?
- What is the effect of the alignment loss on head classes? Does it reduce class-specific fidelity or harm controllability? The paper shows improved FID for head/body/tail, but no analysis of CFG guidance or class separation.
- How does the proposed method compare to DiffROP (Yan et al., 2024)? The related work mentions it, but no experimental comparison is provided.

### Limitations

- The method requires two forward passes (conditional and unconditional) during training, leading to about 1.5x training time overhead; inference latency is unchanged, but the cost is non-trivial.
- The evaluation is limited to low-to-moderate resolutions (up to 256x256); the scalability to higher resolutions commonly used in modern diffusion models (e.g., 512x512) is not demonstrated.
- The paper does not analyze potential over-dispersion caused by the contrastive loss, which could harm intra-class structure or fidelity for some classes, especially if the loss weight alpha is too high.
- The alignment loss is designed for class-conditioned generation and may not generalize to text-conditioned generation, which is a more common setting; no experiments with text prompts are provided.
- No theoretical analysis is given for how the two losses interact or why the combination should not degrade head-class generation; the paper relies solely on empirical evidence.
- The method introduces additional hyperparameters (alpha, gamma, tau, batch resample re-balanced factor) that require tuning; no automated selection or sensitivity analysis is provided.
- The paper does not evaluate the impact of the method on the diversity or fidelity of head classes individually, only on overall metrics and coarse head/body/tail categories.
- Statistical significance analysis is limited to three seeds on CIFAR100-LT only, and no confidence intervals are reported for ImageNet-LT.
- The performance gap between the proposed method and the balanced upper bound remains substantial, especially on TinyImageNet-LT, indicating that long-tailed generation is still far from solved.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 94,815
- Cache-hit prompt tokens: 9,856
- Cache-miss prompt tokens: 84,959
- Completion tokens: 23,336
- Reasoning tokens reported: 16,242
- Total tokens: 118,151
- Estimated total: $0.01845594

Full individual reviews and raw JSON responses are in `review_bundle.json`.
