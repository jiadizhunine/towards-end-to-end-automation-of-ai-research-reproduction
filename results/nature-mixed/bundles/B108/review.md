# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B108.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **5/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 2, 'Reject': 3}
- Estimated API cost: **$0.013420**

## Final Meta-review

The paper introduces TabINR, an implicit neural representation (INR) framework for tabular data imputation. The method models each table cell as a function of learnable row and feature embeddings via a shared MLP, trained only on observed entries using a mixed MSE/BCE loss for numerical and categorical features. Test-time adaptation via latent optimization handles unseen rows with partial observations. The authors evaluate TabINR on 12 UCI datasets across three missingness mechanisms (MCAR, MAR, MNAR) and multiple missingness rates (10-70%), comparing against classical (KNN, MICE, MissForest) and deep learning (GAIN, ReMasker) baselines. Results show competitive or superior imputation accuracy, with the clearest gains on high-dimensional datasets. The paper also includes downstream classification experiments, permutation robustness analysis, and ablation studies.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 2 | 2.200 | 0.400 | 2-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 2 | 2.400 | 0.490 | 2-3 |
| Overall | 5 | 5.400 | 0.490 | 5-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel application of implicit neural representations to tabular data imputation, a relatively unexplored area
- Conceptually clean formulation with learnable row/feature embeddings and auto-decoder-style optimization
- Comprehensive evaluation across 12 datasets, 3 missingness mechanisms, and 4 missingness rates
- Test-time adaptation for unseen rows is a practical contribution for real-world deployment
- Permutation invariance is properly addressed and empirically verified
- Mixed loss function elegantly handles heterogeneous feature types
- Memory-efficient architecture compared to GAN and transformer-based approaches

### Weaknesses

- Empirical gains over baselines are modest and inconsistent; TabINR often ties with rather than clearly outperforms existing methods
- Missing comparison with strong modern baselines such as MIWAE, HI-VAE, and HyperImpute
- Inference time claims are misleading as they exclude the per-row latent optimization cost for new instances
- MNAR simulation is simplistic (MAR plus additional Bernoulli masking), limiting the validity of MNAR performance claims
- No statistical significance testing (e.g., Wilcoxon signed-rank test) across the many dataset/mechanism/rate combinations
- Global default hyperparameter configuration likely underestimates the method's best-case performance
- Scalability to very large datasets (millions of rows) or high-cardinality categorical features is not adequately addressed
- The random masking during training (10-70%) adds another hyperparameter whose sensitivity is not fully explored

### Questions

- How does TabINR's inference-time per-row optimization cost scale with the number of new rows? The reported per-dataset times may hide significant overhead when many new instances need imputation.
- Why were MIWAE, HI-VAE, and HyperImpute not included in the comparison? These are standard baselines in the imputation literature.
- Can you provide statistical significance testing (e.g., Wilcoxon signed-rank test) across the 12 datasets to support the claim of superiority over baselines?
- How is AUROC computed for categorical features when the target variable itself is imputed? Please clarify the evaluation protocol.
- The MNAR mechanism is implemented as MAR plus additional Bernoulli masking. How does this relate to real MNAR scenarios, and does this limitation affect the generalizability of the MNAR results?
- What is the memory footprint of TabINR compared to transformer-based methods like ReMasker? The claim of being 'memory-efficient' is not backed by concrete measurements.
- Could you report per-row inference times for test-time adaptation, especially for datasets with many new rows?
- How sensitive is the method to the initialization of the new row embedding during test-time optimization?
- How does the method handle new features (columns) that were not seen during training? The current formulation only supports test-time adaptation for new rows.
- Why does TabINR perform better on high-dimensional datasets? Is there a theoretical or empirical analysis explaining this phenomenon?

### Limitations

- Experiments are limited to moderate-scale UCI datasets with synthetically induced missingness; real-world missingness patterns may differ substantially
- The method requires storing per-row embeddings, which may limit scalability to very large datasets
- Test-time optimization for new rows adds computational overhead not clearly accounted for in the inference time comparison
- The global default hyperparameter configuration likely underestimates the method's best-case performance but also makes results less actionable for practitioners
- No analysis of the method's behavior when the missingness mechanism is misspecified or when there are systematic biases in the data
- The paper does not address potential negative societal impacts, though the application domain (medical, financial) could have downstream consequences from poor imputation

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 83,333
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 74,373
- Completion tokens: 10,654
- Reasoning tokens reported: 0
- Total tokens: 93,987
- Estimated total: $0.01342043

Full individual reviews and raw JSON responses are in `review_bundle.json`.
