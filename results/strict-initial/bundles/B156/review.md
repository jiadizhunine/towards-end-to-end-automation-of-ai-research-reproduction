# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B156.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 1, 'Reject': 4}
- Estimated API cost: **$0.021479**

## Final Meta-review

The paper proposes Gradient Inversion Transcript (GIT), a generative model for reconstructing training data from leaked gradients in federated/distributed learning. GIT derives an architecture inspired by backpropagation to map gradients to input data, with an Exact-GIT variant and a more practical Coarse-GIT variant that uses shallow MLPs recursively. The method can be used directly or as a prior for optimization-based inversion. Experiments on CIFAR-10, ImageNet, and facial datasets with LeNet, ResNet, and ViT report improved performance over some baselines and robustness to noisy gradients, distribution shift, and parameter discrepancies.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 2 | 2.400 | 0.490 | 2-3 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 2 | 2.000 | 0.000 | 2-2 |
| Significance | 2 | 2.400 | 0.490 | 2-3 |
| Soundness | 2 | 2.200 | 0.400 | 2-3 |
| Presentation | 2 | 2.000 | 0.000 | 2-2 |
| Contribution | 2 | 2.400 | 0.490 | 2-3 |
| Overall | 4 | 4.400 | 0.800 | 4-6 |
| Confidence | 4 | 3.600 | 0.490 | 3-4 |

### Strengths

- The idea of adapting the generative model's architecture to the target model via backpropagation equations is novel and distinct from fixed-architecture generative attacks like LTI.
- Comprehensive experiments across multiple datasets, model architectures, and realistic robustness scenarios (noisy/pruned gradients, distribution shift, parameter discrepancies) generally show improved reconstruction in many settings.
- The hybrid approach (GIT+IG) demonstrates that GIT can accelerate convergence and improve reconstruction quality when used as a prior for optimization-based methods.
- GIT is efficient at inference after offline training, making it practical for real-time reconstruction compared to iterative optimization methods.
- The paper evaluates against both generative-based (LTI, GIAS) and optimization-based (DLG, IG) methods in a unified framework.

### Weaknesses

- The theoretical derivation, particularly Equation (3), is not rigorous: it uses Moore-Penrose inverses and term cancellations without clear conditions, and the equations appear dimensionally inconsistent or heuristically justified.
- Implementation details are severely underspecified: Algorithm 1 is missing, training procedures for Coarse-GIT (layerwise vs. joint, loss functions, hyperparameters) are unclear, and the estimation of initial output logits is not fully explained.
- Experiments are limited to batch size 1; no results for larger mini-batches common in federated learning, and the method's handling of label-dependent gradients is not analyzed.
- Performance gains are inconsistent: GIT underperforms LTI in LPIPS on CIFAR-10/LeNet (0.2663 vs 0.2202) and GIT+IG has lower SSIM than GIAS+IG on ImageNet/ViT, contradicting claims of consistent superiority.
- No ablation isolates the benefit of the adaptive architecture: it is unclear whether improvement comes from the backpropagation-inspired design or simply from using additional gradient inputs in a generic MLP.
- Exact-GIT is not quantitatively evaluated in the main experiments, and Coarse-GIT is not compared against a fixed-architecture MLP with the same inputs, weakening the theoretical contribution.
- Comparisons with recent strong baselines (e.g., DGGI) are missing, and no standard deviations or statistical significance tests are reported.
- The paper contains numerous typos (e.g., 'pune rate') and unclear notation, hurting readability and reproducibility.

### Questions

- What exact batch sizes were used in Tables 2, 3, 5, and 6? How does GIT perform with batch sizes larger than 1, and can it reconstruct individual samples from averaged gradients?
- Can the full training and inference procedures for Coarse-GIT (and Exact-GIT) be provided, including how the shallow MLPs are trained, how input features are selected, and how the initial output activations are estimated?
- In Equation (3), what are the conditions for the Moore-Penrose inverse manipulation, and is the inversion exact for simple linear networks?
- How are labels handled during reconstruction? Does GIT require known labels, and what is label reconstruction accuracy?
- Why does GIT underperform LTI on LPIPS for CIFAR-10/LeNet? Is there an MSE-perceptual quality trade-off that is not discussed?
- Are the reported improvements statistically significant? How many random seeds were used, and why are no confidence intervals provided?
- How does GIT perform under stronger defenses such as differential privacy with larger noise scales, secure aggregation, or advanced gradient compression?

### Limitations

- The attack assumes the attacker can inject data into a compromised client and has access to a public dataset similar to the target data, which may not hold in many federated learning deployments.
- The method requires knowledge of the target model architecture and, for some settings, output activations; this may not always be available to an attacker.
- The offline training cost is high (thousands of seconds), and no analysis of the computational cost vs. benefit is provided.
- Only image data are evaluated; the effectiveness for text, tabular, or other modalities is unexplored.
- The method's robustness degrades under distribution shift and parameter discrepancies, and it does not address advanced defenses or secure aggregation.
- The ethical implications and potential societal harms of the proposed privacy attack are not discussed.

### Ethics

Ethical concerns flagged: **True**

## Usage and Cost

- Requests: 6
- Prompt tokens: 111,942
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 107,846
- Completion tokens: 22,745
- Reasoning tokens reported: 16,169
- Total tokens: 134,687
- Estimated total: $0.02147851

Full individual reviews and raw JSON responses are in `review_bundle.json`.
