# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B087.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **3/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.018330**

## Final Meta-review

The paper introduces StatsMerging, a model merging framework for vision models that predicts merging coefficients (task-wise or layer-wise) using weight distribution statistics (mean, variance, magnitude, and top-3 singular values from SVD). A lightweight MLP (StatsMergeLearner) is trained to map these statistics to coefficients, using a Task-Specific Teacher Distillation paradigm that avoids ground-truth labels by using individual task models' predictions as pseudo-labels. The paper also proposes an extension to heterogeneous architectures by distilling models with different backbones (e.g., ViT to ResNet) into a unified architecture before merging. Experiments on eight image classification tasks (ViT-B/32 backbone) show StatsMerging++ achieves 94.5% average accuracy, outperforming baselines like AdaMerging (81.1%) and WEMoE (89.4%). The paper also demonstrates generalization to unseen tasks, robustness to image corruptions, and heterogeneous architecture merging.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.800 | 2-4 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 2 | 2.400 | 0.490 | 2-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 3 | 2.800 | 0.400 | 2-3 |
| Presentation | 2 | 2.400 | 0.490 | 2-3 |
| Contribution | 3 | 2.800 | 0.400 | 2-3 |
| Overall | 6 | 5.800 | 0.980 | 4-7 |
| Confidence | 3 | 3.400 | 0.490 | 3-4 |

### Strengths

- Novel use of weight distribution statistics, particularly SVD singular values, to guide merging coefficient prediction, distinguishing the approach from prior optimization-based or heuristic methods.
- Strong empirical results: StatsMerging++ (layer-wise) achieves 94.5% average accuracy on 8 tasks, outperforming the previous state-of-the-art WEMoE by 5.1%, with consistent improvements across task-wise and layer-wise settings.
- The Task-Specific Teacher Distillation paradigm provides a practical label-free training approach, avoiding the need for manually annotated data.
- The extension to heterogeneous architectures via distillation is a valuable contribution, addressing a gap in prior model merging work.
- The StatsMergeLearner is lightweight (10.99M parameters, 2.95 GFLOPs), adding minimal overhead to the merging pipeline.
- Comprehensive evaluation includes multi-task merging, generalization to unseen tasks, robustness to corruptions, and ablations on statistical features and loss functions.

### Weaknesses

- The distinction between StatsMerging and StatsMerging++ is unclear; the paper only states that the latter is 'trained on more validation data' without specifying the exact amounts or quantifying the impact, which raises concerns about fairness in comparisons with baselines.
- The theoretical justification for why weight statistics, especially SVD singular values, should predict optimal merging coefficients is heuristic and lacks rigorous analysis.
- The claim of being the 'first heterogeneous architectural merging method' is overstated, as cross-architecture knowledge distillation for merging has been explored in prior work.
- The ablation study is limited to four tasks, and the sensitivity to SVD rank (fixed at 3) is not explored.
- The main comparison table omits several recent baselines (e.g., ZipIt, Pareto Merging, C2M3) cited in the related work, weakening the state-of-the-art claim.
- The paper contains numerous typos, grammatical errors, and notation inconsistencies (e.g., 'weights' vs 'weights', 'VI' vs 'VT'), detracting from clarity and reproducibility.
- The evaluation is limited to image classification; no experiments on detection, segmentation, or NLP tasks are provided, limiting generalizability claims.
- The robustness evaluation is confined to three corruption types and four tasks, which is relatively narrow.
- The paper does not report statistical significance or variance across multiple runs, making it difficult to assess the reliability of improvements.
- The computational cost comparison with baselines (e.g., training time for AdaMerging vs StatsMerging) is not adequately discussed.

### Questions

- Can you specify the exact amount of validation data used for StatsMerging vs StatsMerging++? Is the comparison with AdaMerging controlled for the same validation data budget?
- Why is SVD rank 3 chosen? Have you explored other ranks, and what is the trade-off between rank and performance?
- How is the method's performance affected by the number of tasks? Have you evaluated merging more than 8 tasks, and what are the scalability limitations?
- How does the method handle tasks with very different numbers of classes (e.g., SUN397 with 397 classes vs MNIST with 10)?
- In the heterogeneous architecture experiments, why only 3 tasks and a single architecture pair (ViT to ResNet)? Would the approach generalize to other pairs or directions?
- Can you provide a quantitative analysis of the coefficient patterns (Figure 3) and their relation to task performance?
- What is the training time for StatsMerging on the full 8-task setup compared to baselines like AdaMerging?
- The paper mentions 'test-time adaptability' in Table 1 but does not demonstrate it. Can you provide experiments or clarify this capability?
- How sensitive is the method to the choice of validation set split? Is there a risk of overfitting to the validation set during StatsMergeLearner training?
- Why does the soft pseudo-label (KL-divergence) approach perform worse than hard pseudo-labels (cross-entropy)? Is this related to class distribution in the aggregated dataset?

### Limitations

- The method is evaluated only on image classification tasks; extension to object detection, segmentation, and NLP is not demonstrated.
- The heterogeneous architecture merging requires a distillation step to a common backbone, which may lose information and adds computational overhead; the cost is not discussed.
- The method requires access to validation data (albeit unlabeled) from each task, which may not be available in privacy-constrained scenarios.
- No analysis is provided on scaling to very large numbers of tasks or models, which could be a practical concern.
- The theoretical understanding of why weight statistics guide merging is limited; the paper relies on intuition rather than formal analysis.
- Potential negative societal impacts are not discussed, though model merging could facilitate unauthorized reuse of proprietary models.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 115,964
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 107,004
- Completion tokens: 11,873
- Reasoning tokens reported: 0
- Total tokens: 127,837
- Estimated total: $0.01833009

Full individual reviews and raw JSON responses are in `review_bundle.json`.
