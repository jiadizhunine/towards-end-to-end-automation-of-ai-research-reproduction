# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B034.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.027483**

## Final Meta-review

The paper proposes CUSAL (Calibrated Uncertainty Sampling for Active Learning), a novel acquisition function that estimates per-sample calibration error on the unlabeled pool using a kernel-based estimator adapted for the covariate shift inherent in active learning. The method uses lexicographic ordering to prioritize querying samples with the highest estimated calibration error before falling back to uncertainty-based sampling. The authors provide theoretical guarantees: (1) consistency and MSE bounds for the calibration estimator under covariate shift, and (2) bounds on the expected calibration error of the learned classifier on both the unlabeled pool and unseen test data. Empirically, CUSAL is evaluated on MNIST, F-MNIST, SVHN, CIFAR-10, CIFAR-10-LT, and ImageNet, consistently achieving lower ECE and competitive or better accuracy compared to standard AL baselines (random, least-confidence, margin, BALD, Coreset, BADGE). The paper also includes thorough ablations on estimator quality, lexicographic ordering, bandwidth sensitivity, and comparisons with post-hoc recalibration and other calibration-aware methods.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.800 | 0.400 | 3-4 |
| Quality | 3 | 3.400 | 0.490 | 3-4 |
| Clarity | 4 | 3.800 | 0.400 | 3-4 |
| Significance | 3 | 3.400 | 0.490 | 3-4 |
| Soundness | 3 | 3.400 | 0.490 | 3-4 |
| Presentation | 4 | 3.800 | 0.400 | 3-4 |
| Contribution | 3 | 3.400 | 0.490 | 3-4 |
| Overall | 7 | 6.800 | 0.748 | 6-8 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Addresses an important and under-explored problem: the interplay between calibration and acquisition function effectiveness in active learning.
- Novel and well-motivated approach: using estimated per-sample calibration error as a primary acquisition criterion via lexicographic ordering is a fresh perspective.
- Solid theoretical contributions: provides consistency guarantees for the calibration estimator under the covariate shift of AL, and bounds on expected calibration error for the unlabeled pool and test data.
- Comprehensive empirical evaluation across six datasets of varying complexity (from MNIST to ImageNet) with multiple strong baselines, run with multiple seeds for statistical reliability.
- Clear writing and well-organized structure, with code and a demo notebook provided for reproducibility.
- Thorough ablation studies isolating the contribution of each component (lexicographic ordering, estimator quality, bandwidth sensitivity, comparison with post-hoc recalibration).

### Weaknesses

- The theoretical results rely on assumptions (e.g., unbiased calibration error estimator, bounded calibration error function) that may be hard to verify in practice.
- The computational cost of the kernel-based estimator (O(n*m) per round) is not deeply analyzed and could be prohibitive for very large unlabeled pools; no mitigation strategies are provided.
- Accuracy improvements over baselines are sometimes modest (e.g., on CIFAR-10), with the primary benefit being calibration rather than accuracy.
- The comparison with post-hoc recalibration (Least-conf-TS) is somewhat unfair as the baseline splits training data for temperature scaling, which reduces accuracy; a fairer comparison would use a separate validation set.
- Limited guidance on selecting the Dirichlet kernel bandwidth b in practice, though the ablation shows some robustness.
- The method focuses on inductive AL and image classification; extension to other settings (e.g., transductive AL, regression, NLP, tabular data) is not discussed.

### Questions

- How does the computational cost of the kernel calibration estimator scale with the size of the unlabeled pool and the labeled set? Could you provide runtime comparisons with baselines, especially on ImageNet?
- The theorem assumes an unbiased calibration error estimator. How sensitive are the results to violations of this assumption? Could the bound be relaxed for biased estimators?
- How was the bandwidth b=0.001 chosen? Is there a principled way to select b automatically, given the O(b^2) bias term in Theorem 4.1?
- In Theorem 4.2, the proof of the bound on the unlabeled pool (Eq. 34-35) appears to use the fact that selecting top-k highest calibration error samples bounds the average over the remaining pool. Could you provide a more detailed justification? Does this rely on specific properties of the calibration error distribution?
- For the comparison with post-hoc recalibration (Least-conf-TS), have you considered using a separate validation set (e.g., from the warmup set) for temperature scaling to make the comparison fairer?
- How does CUSAL perform when the model is severely miscalibrated initially or when the warm-up set is very small? Does the method degrade gracefully compared to uncertainty sampling?
- The CIFAR-10-LT results show Cluster-Ours significantly outperforms the base method. Should diversity be integrated more explicitly into the main algorithm rather than as an extension?
- Could you discuss potential failure modes or scenarios where CUSAL might not outperform uncertainty sampling (e.g., when the calibration error estimate is noisy or near-uniform)?

### Limitations

- The computational complexity of the kernel estimator is acknowledged but not deeply analyzed; this could be a significant barrier for very large-scale active learning applications. Approximations or subsampling strategies would be valuable.
- The theoretical bounds rely on several assumptions (e.g., unbiased estimator, bounded calibration error) that may not hold exactly in practice, limiting the strength of the guarantees.
- The method is evaluated primarily on image classification datasets; performance on other modalities (e.g., text, tabular) and on regression tasks is unexplored.
- The paper does not discuss potential negative societal impacts. While the work aims to improve model reliability, which is generally positive, biased calibration error estimates could lead to unfair query selection in certain subgroups; this is not addressed.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 185,019
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 176,059
- Completion tokens: 10,033
- Reasoning tokens reported: 0
- Total tokens: 195,052
- Estimated total: $0.02748259

Full individual reviews and raw JSON responses are in `review_bundle.json`.
