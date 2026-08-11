# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B108.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.015166**

## Final Meta-review

The paper introduces TabINR, an auto-decoder-based implicit neural representation (INR) framework for tabular data imputation. It models each table entry as a function of learnable row and feature embeddings through a shared MLP with SIREN activations, trained on observed entries with a mixed MSE/BCE loss. At inference, new rows are handled by optimizing a fresh row embedding while freezing the network and feature embeddings. The method is evaluated on 12 UCI datasets under MCAR, MAR, and MNAR missingness at ratios 10–70%, comparing against mean/mode, KNN, MICE, MissForest, GAIN, and ReMasker, reporting NRMSE/AUROC, downstream XGBoost classification, inference time, permutation robustness, and ablations.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 2 | 2.000 | 0.000 | 2-2 |
| Quality | 2 | 2.000 | 0.000 | 2-2 |
| Clarity | 2 | 2.000 | 0.000 | 2-2 |
| Significance | 2 | 2.000 | 0.000 | 2-2 |
| Soundness | 2 | 2.000 | 0.000 | 2-2 |
| Presentation | 2 | 2.000 | 0.000 | 2-2 |
| Contribution | 2 | 2.000 | 0.000 | 2-2 |
| Overall | 4 | 4.000 | 0.000 | 4-4 |
| Confidence | 4 | 3.600 | 0.490 | 3-4 |

### Strengths

- Conceptually simple and unified framework using row/feature embeddings with an MLP and SIREN activations, naturally handling mixed continuous/categorical features.
- Broad experimental protocol covering 12 datasets, three missingness mechanisms, multiple missingness ratios, downstream classification, runtime comparison, and permutation robustness.
- Test-time latent optimization provides a principled way to adapt to unseen rows without retraining the network, which is a practical advantage.
- Permutation robustness is explicitly verified, addressing a key concern about applying coordinate-based INRs to unordered tabular data.
- Inference-time comparison shows TabINR is faster than iterative imputers such as MICE and MissForest, which is practically relevant.

### Weaknesses

- The main quantitative results are not verifiable from the submitted text: only aggregate or redacted figures are provided, with no per-dataset numerical NRMSE/AUROC tables or statistical significance tests.
- Several relevant deep imputation baselines discussed in related work (MIWAE, HI-VAE, SAINT, FT-Transformer, TabTransformer, HyperImpute) are omitted from the empirical comparison, limiting the strength of the claims.
- The reported inference time likely excludes the iterative gradient-based optimization required for each new row's embedding; details on the number of steps, learning rate, initialization, and stopping criterion are missing.
- Memory cost scales linearly with the number of rows due to storing a row embedding per training instance, conflicting with the 'memory-efficient' claim and not analyzed or compared empirically.
- The synthetic MNAR mechanism is likely invalid: adding Bernoulli masking to values left unmasked after MAR does not create missingness that depends on the missing values themselves, so the MNAR results may not reflect true MNAR settings.
- The training protocol is ambiguous: additional random masking of 10–70% of entries during training is mentioned, but its interaction with the benchmark missingness mask and the held-out evaluation mask is not clearly explained.
- Categorical imputation evaluation is underspecified: AUROC computation for multi-class one-hot features and the winner-takes-all projection are not fully detailed, and the latter discards uncertainty and may produce biased imputations.
- The ablation study uses a different default configuration (depth=4, latent=64) than the main experiments (depth=2, latent=32), making the sensitivity analysis and the choice of global defaults difficult to interpret.
- Novelty is incremental: combining learnable row/column embeddings with an MLP closely resembles neural matrix factorization or collaborative filtering, and the auto-decoder concept is borrowed from DeepSDF without sufficient differentiation.
- No code or implementation details are provided, and many experimental details (e.g., number of seeds, per-dataset hyperparameters, exact MNAR generation) are omitted, hindering reproducibility.
- A single global hyperparameter configuration is used across all datasets, which the authors acknowledge likely underestimates the model's best-case performance and limits generalizability claims.

### Questions

- How many gradient steps and what learning rate are used for test-time latent optimization, and does the reported inference time include this optimization?
- What is the exact MNAR generation procedure? How does adding Bernoulli masking to values left unmasked create missingness dependent on the missing values themselves?
- Can the authors provide per-dataset numerical NRMSE and AUROC tables with standard deviations and statistical significance tests (e.g., paired tests) for all datasets and missingness settings?
- Why are MIWAE, HI-VAE, SAINT, FT-Transformer, and TabTransformer omitted from the empirical benchmark despite being discussed as relevant prior work?
- How is AUROC computed for categorical features with more than two classes after one-hot expansion? Is it macro-averaged, micro-averaged, or per-binary-column?
- How does the memory footprint of TabINR scale with dataset size, and how does it compare with baselines on large or high-dimensional datasets?
- What is the role of the additional random masking (10–70%) during training, and how does it interact with the synthetic missingness masks used for evaluation?
- How robust is test-time latent optimization when a new row has very few observed features (e.g., 10%)? Are there failure cases or instability, and how is it initialized?

### Limitations

- Evaluation is limited to moderate-scale UCI datasets (up to ~20,000 rows and 57 features) with synthetically induced missingness; real-world missing data patterns and larger datasets are not explored.
- The MNAR experiments are likely invalid because the generated missingness mechanism does not correctly simulate missing-not-at-random data.
- Memory and test-time optimization costs are not properly analyzed, raising concerns about scalability to very large datasets and to sparse new rows.
- A single global hyperparameter configuration is used, which may understate TabINR's best-case performance and makes it unclear how much tuning is needed for new datasets.
- Categorical imputation uses a winner-takes-all projection that ignores prediction uncertainty and may produce biased or overconfident predictions for high-cardinality categories.
- No code or implementation details are provided, limiting reproducibility.
- Potential negative societal impacts include the risk that biased or inaccurate imputations in sensitive domains (e.g., healthcare, finance) could propagate into downstream decisions, though no specific new risks are identified.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 74,935
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 70,839
- Completion tokens: 18,705
- Reasoning tokens reported: 11,854
- Total tokens: 93,640
- Estimated total: $0.01516633

Full individual reviews and raw JSON responses are in `review_bundle.json`.
