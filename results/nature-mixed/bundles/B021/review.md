# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B021.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.016593**

## Final Meta-review

The paper proposes CCUA (Contrastive Conditional-Unconditional Alignment), a framework for class-conditional diffusion models trained on long-tailed data. Two loss functions are introduced: (1) an Unsupervised Contrastive Loss (UCL) that uses negative samples only to increase the diversity of synthetic images and mitigate mode collapse for tail classes, and (2) an Alignment Loss (AL) that aligns conditional and unconditional generation at large timesteps to facilitate knowledge sharing from head to tail classes. The method is implemented for both U-Net (DDPM) and Diffusion Transformer (SiT) architectures and evaluated on ImageNet-LT, TinyImageNet-LT, Places-LT, and CIFAR-LT datasets, consistently outperforming baselines such as DDPM, CBDM, OCLT, and Dispersive Loss across FID, sFID, KID, and Recall metrics.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 7 | 6.600 | 0.490 | 6-7 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Addresses an important and timely problem: long-tailed class-conditional image generation with diffusion models.
- The two proposed losses are simple, well-motivated, and easy to implement on both U-Net and DiT architectures.
- Comprehensive experiments across multiple datasets (ImageNet-LT, TinyImageNet-LT, Places-LT, CIFAR10/100-LT) and resolutions (32x32 to 256x256).
- The conditional-unconditional alignment at large timesteps is a novel adaptation from GAN literature to diffusion models, with a clear derivation from KL divergence.
- Good ablation studies showing the contribution of each loss and the benefit of batch resampling.
- Qualitative results (t-SNE, KDE, nearest-neighbor visualizations) clearly demonstrate mitigation of mode collapse for tail classes.
- The method does not increase inference latency.
- Honest discussion of limitations, including increased training time.
- Statistical significance analysis is provided for CIFAR100-LT.

### Weaknesses

- The Unsupervised Contrastive Loss with negative samples only is very similar to the concurrent 'dispersive loss' (Wang & He, 2025); the claimed distinction (formulation in unconditional latent space) is subtle and the novelty of UCL is limited.
- Improvements on CIFAR-LT datasets are modest (e.g., FID from 5.93 to 5.56 on CIFAR10-LT), and statistical significance is only shown on CIFAR100-LT with limited seeds.
- No empirical comparison with DiffROP (Yan et al., 2024), which is discussed in related work.
- No sensitivity analysis for hyperparameters α and γ, which are crucial for practical use.
- Batch resampling is applied inconsistently across datasets (on ImageNet-LT and TinyImageNet-LT but not on Places-LT and CIFAR-LT), complicating fair cross-dataset comparisons.
- The use of h_pos = h_anc (no augmentation) in the contrastive loss is unconventional and lacks strong theoretical justification.
- The training time overhead (1.6x for DDPM, 1.48x for SiT) is significant and not fully discussed in the main text or limitations section.
- The theoretical understanding of why the alignment loss works is limited; the paper relies on empirical observations and qualitative visualizations rather than quantitative analysis.
- No experiments with different imbalance factors (e.g., 0.05, 0.1) beyond the standard 0.01.

### Questions

- Can you provide a sensitivity analysis for the hyperparameters α and γ? How sensitive is the performance to these values across different datasets and architectures?
- Why did you not include an empirical comparison with DiffROP (Yan et al., 2024)? This would strengthen the claim that your method generalizes it.
- Can you elaborate on why formulating the unsupervised contrastive loss in the unconditional latent space (rather than conditional) leads to better performance than Dispersive Loss on ImageNet-LT?
- Why is the positive sample set to be identical to the anchor (h_pos = h_anc) in the contrastive loss? Could you provide theoretical justification or experimental results with data augmentation for positive pairs?
- How do the two losses interact during training? Does the alignment loss potentially counteract the diversity-promoting effect of the contrastive loss?
- Why is batch resampling applied only to ImageNet-LT and TinyImageNet-LT but not to Places-LT and CIFAR-LT? Would results on Places-LT improve further with batch resampling?
- What is the breakdown of the computational overhead from each loss (UCL and AL)? Could the contrastive loss be computed on a separate lightweight encoder to reduce training cost?
- How does the method perform with different imbalance factors (e.g., 0.05, 0.1) beyond the fixed 0.01 used in the paper?
- For the FIDtail metric, how are tail classes defined across different datasets? Is it consistent with the 'Tail' super-category in Table 3?
- Could the alignment loss potentially reduce class-specific details in generated images? How is the trade-off between diversity and class-controllability managed?

### Limitations

- Training time is increased by approximately 1.5-1.6x due to the two forward passes required for conditional and unconditional noise estimation; this trade-off is not fully discussed in the main text.
- The method is evaluated only on class-conditional image generation; applicability to text-to-image or other modalities (video, audio) is unexplored.
- The theoretical understanding of why the alignment loss facilitates knowledge sharing is limited; the paper relies on empirical observations.
- The contrastive loss with h_pos = h_anc may not generalize well to settings where data augmentation is needed.
- The method requires careful hyperparameter tuning of α and γ, which may vary across datasets and architectures (though this is not thoroughly explored).
- No experiments on extremely imbalanced scenarios beyond 0.01 imbalance factor.
- Potential negative societal impact: improved generation quality for tail classes could be misused to create realistic synthetic images of underrepresented groups, potentially for misinformation or deepfakes. This is not discussed in the paper.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 105,177
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 96,217
- Completion tokens: 11,063
- Reasoning tokens reported: 0
- Total tokens: 116,240
- Estimated total: $0.01659311

Full individual reviews and raw JSON responses are in `review_bundle.json`.
