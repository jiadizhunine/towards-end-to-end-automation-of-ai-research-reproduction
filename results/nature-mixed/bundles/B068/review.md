# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B068.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.023454**

## Final Meta-review

The paper introduces Bidirectional Spike-based Distillation (BSD), a biologically plausible learning algorithm that jointly trains feedforward (stimuli-to-concept) and backward (concept-to-stimuli) spiking neural networks through mutual distillation of spiking feature representations. The authors extend three existing biological plausibility criteria (asymmetric weights, local errors, non-two-stage training) with two new ones (spiking neuron models, unsigned error signals) and demonstrate that BSD satisfies all five. The method uses a Relaxed Contrastive (ReCo) loss to align basal and apical voltages within pyramidal neurons. Extensive experiments across image classification (MNIST, FashionMNIST, SVHN, CIFAR-10/100, Tiny-ImageNet), sequential regression (text prediction, time-series forecasting), and image generation (autoencoders) show performance approaching backpropagation while maintaining biological plausibility. The paper includes thorough ablation studies on loss functions, batch size, timesteps, and firing thresholds.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.600 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.200 | 0.400 | 3-4 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.200 | 0.400 | 3-4 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 5.800 | 0.400 | 5-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel bidirectional distillation framework inspired by the brain's perception-recall architecture, combining feedforward and backward spiking networks in a coherent manner.
- Clear extension of biological plausibility criteria from three to five, with the addition of spiking neurons (C4) and unsigned error signals (C5) being well-motivated.
- Comprehensive empirical evaluation across diverse tasks (classification, sequential regression, generation) and architectures (MLP, CNN, RNN, autoencoder), demonstrating general applicability.
- Thorough ablation studies (loss functions, batch size, timesteps, batch normalization, firing thresholds, lambda) provide useful insights into the method's behavior.
- Well-written and organized paper with detailed appendices covering implementation details, gradient derivations, and additional experiments.
- The use of ReCo loss to satisfy unsigned error signals is a clever and well-justified design choice.
- Analysis of weight alignment dynamics confirms that forward and backward weights remain asymmetric (C1 satisfied) throughout training.

### Weaknesses

- The claim of 'performance comparable to backpropagation' is somewhat overstated. Consistent performance gaps exist on complex tasks: CIFAR-100 (53.48% vs 57.75% for CNN), Tiny-ImageNet (35.34% vs 41.07%), and image generation FID scores (168.12 vs 127.34 on CIFAR-10).
- Biological plausibility claims are partially weakened by the use of surrogate gradients, detach() operations to enforce local learning, batch normalization, and a global cross-entropy loss at the top layer, which are not fully biologically grounded.
- The C5 (unsigned error signals) criterion is debatable since gradients used for weight updates still carry signed information implicitly through the optimization process, and the top-layer cross-entropy loss uses signed errors.
- Training computational overhead is substantial (memory nearly doubles at batch size 128: 5034 MB vs 3324 MB), which is only briefly acknowledged in the main text.
- The method shows significant sensitivity to batch size (performance drops with smaller batches) and hyperparameters (e.g., lambda), limiting practical applicability in memory-constrained settings.
- Lack of theoretical analysis on convergence properties or conditions under which the method might fail.
- Missing comparisons to more recent biologically plausible methods (e.g., Forward-Forward algorithm, improved predictive coding variants, target propagation with spiking neurons).
- The role of the backward network during inference is unclear; it is not used at deployment time, raising questions about its necessity and the true contribution of the bidirectional architecture.
- Scalability to larger models (e.g., ResNet-scale, transformers) and datasets (e.g., ImageNet) is not demonstrated.

### Questions

- The paper claims BSD satisfies C5 (unsigned error signals) through the ReCo loss. However, the gradients used for weight updates still have signs that indicate direction. Could you clarify how the unsigned nature of the loss translates to unsigned weight updates? Does the top-layer cross-entropy loss (which uses signed errors) violate C5?
- What is the precise definition of 'comparable to backpropagation'? On CIFAR-100, BSD is ~4 percentage points lower (53.48% vs 57.75%), and on image generation FID is 40 points worse (168 vs 127). What would be an acceptable threshold for 'comparable'?
- The detach() operation truncates the computational graph between layers. How is this biologically justified? Does this not break the continuous flow of information that biological neurons experience?
- Batch normalization is used in CNN and RNN architectures. What is the biological interpretation of batch normalization, and does its use contradict the local learning criterion (C2)?
- The ReCo loss uses cosine similarity between voltages from different samples in a batch. How does this align with biological learning, where neurons typically only have access to their own activity and local inputs? The batch-level comparison seems to require global information.
- The method requires large batch sizes (128) for good performance. How does this affect scalability to larger models or datasets with limited memory? Are there ways to mitigate this?
- How is the backward network used during inference? The paper states only the feedforward path is used for classification. If so, what is the role of the backward network during deployment, and could it be removed after training?
- Have you compared BSD against more recent biologically plausible methods beyond DLL and CCL, such as Forward-Forward, predictive coding variants, or target propagation with spiking neurons?
- The generation results show FID scores significantly worse than backpropagation (e.g., 168 vs 127 on CIFAR-10). Is this acceptable for a 'comparable' performance claim? Why is the gap larger for generation compared to classification?
- What is the sensitivity of the method to the choice of lambda in the ReCo loss across different tasks? The ablation shows lambda=0.6 is optimal for SVHN, but is this consistent across datasets?
- The training memory consumption is significantly higher than BP (e.g., 5034 MB vs 3324 MB for batch size 128). How does this trade-off affect the practical usability of the method for real-world applications?
- Can you provide theoretical justification for why the bidirectional distillation converges? The paper only provides empirical convergence curves.

### Limitations

- The method has been evaluated only on relatively small-scale datasets and conventional architectures (MLP, CNN, RNN, autoencoder); scalability to modern deep architectures (e.g., ResNet, Transformers) and larger datasets (e.g., ImageNet) is unclear.
- Biological plausibility claims are partially based on abstract analogies (e.g., three-compartment neurons) rather than direct neurophysiological evidence. The use of surrogate gradients, detach() operations, batch normalization, and global loss at the top layer are not fully biologically grounded.
- The performance gaps on complex datasets (CIFAR-100, Tiny-ImageNet) and generation tasks (FID scores) are more significant than the paper's 'comparable performance' claim suggests, which may limit practical adoption.
- The training computational overhead (dual pathways, O(B^2) affinity matrix computation) could be prohibitive for large-scale applications.
- The method's sensitivity to batch size and hyperparameters (lambda, firing thresholds) is not thoroughly discussed in the main text and may limit practical applicability.
- The backward network's role during inference is unclear, and it is not used at deployment time, which raises questions about the necessity of the bidirectional architecture.
- The paper does not discuss potential negative societal impacts beyond a brief ethics statement, though the work appears to have minimal risk.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 152,219
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 143,259
- Completion tokens: 12,045
- Reasoning tokens reported: 0
- Total tokens: 164,264
- Estimated total: $0.02345395

Full individual reviews and raw JSON responses are in `review_bundle.json`.
