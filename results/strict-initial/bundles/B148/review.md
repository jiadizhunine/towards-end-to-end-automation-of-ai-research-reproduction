# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B148.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.041818**

## Final Meta-review

The paper introduces CAMA, a test-time, cohort-level active modality acquisition setting: under a fixed budget, select which samples in a cohort should receive an additional costly modality to maximize a global performance metric such as AUROC or AUPRC. The authors propose acquisition functions that combine a discriminative late-fusion classifier with generative imputation models (DDPMs or BC-VAEs) to estimate counterfactual scores, and define oracle and upper-bound heuristics as benchmarks. They evaluate on four multimodal datasets, including a large-scale UK Biobank cohort with 15 modalities and 100k samples, and report that an imputation-based KL-Divergence strategy often outperforms simpler baselines.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 2.800 | 0.400 | 2-3 |
| Quality | 2 | 2.000 | 0.000 | 2-2 |
| Clarity | 2 | 2.400 | 0.800 | 1-3 |
| Significance | 2 | 2.600 | 0.490 | 2-3 |
| Soundness | 2 | 2.000 | 0.000 | 2-2 |
| Presentation | 2 | 2.400 | 0.800 | 1-3 |
| Contribution | 2 | 2.200 | 0.400 | 2-3 |
| Overall | 4 | 4.000 | 0.000 | 4-4 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The problem formulation is novel and practically relevant: cohort-level, test-time acquisition of entire modalities under budget constraints, clearly distinguished from active learning, active feature acquisition, and active modality acquisition.
- The empirical evaluation is broad and includes diverse real-world datasets, with a large-scale UK Biobank scenario demonstrating scalability to 100k samples and 15 modalities.
- The paper provides a structured taxonomy of acquisition strategies (oracle, upper-bound, imputation-based, baselines, random) and introduces a normalized gain metric (G_full) that facilitates comparisons across tasks and budgets.
- The inclusion of oracle and upper-bound heuristics offers useful performance references, and the insight that selective acquisition can outperform full-multimodal performance is interesting and non-obvious.
- The ablation of DDPM vs. BC-VAE imputers and efficiency analysis provides practical architectural trade-offs and implementation insights.

### Weaknesses

- The central claim that imputation-based KL-Divergence consistently and significantly outperforms all non-oracle methods is not supported by the reported results: simple baselines such as uncertainty, probability, or even random selection are often comparable or better across several tasks and datasets, and no statistical significance tests are provided.
- The evaluation protocol excludes tasks/splits where the multimodal model underperforms the unimodal baseline (negative gain), which biases results and limits real-world applicability where acquisition may be harmful.
- The proposed methods are not compared to existing active feature acquisition (AFA) or active modality acquisition (AMA) methods, such as EDDI, Icebreaker, or Kossen et al., so the claimed advance over prior art is not established.
- The upper-bound heuristics are not true bounds: imputation-based strategies sometimes exceed them, indicating that the bounds are either invalid or that evaluation noise is substantial; this undermines the interpretability of comparisons.
- There is a train/test distribution shift: the classifier is trained solely on real available modality embeddings but at inference receives imputed embeddings from the generative model to compute counterfactual scores; this shift is not analyzed or mitigated.
- The problem formulation is ambiguous regarding multiple missing modalities: Equation 3 suggests upgrading selected samples to full scores, while the text says 'an additional modality'; it is unclear how the framework decides which modality to acquire for a sample missing more than one.
- The theoretical grounding is heuristic; the proposed acquisition functions are not formally derived from AUROC/AUPRC marginal gains, despite the paper's claim of a theoretical framework.
- Computational cost is significant: a separate generative imputer (e.g., DDPM) is required for each missing-modality configuration, and 100 imputation samples per test sample may be prohibitive for large cohorts or time-critical applications.
- The paper has presentation issues, including a missing main table, broken cross-references, incomplete hyperparameter reporting, and some appendix tables with high SEM or missing values, making it difficult to assess reproducibility.

### Questions

- How do the proposed methods compare to existing AFA/AMA methods such as EDDI, Icebreaker, or Kossen et al. when adapted to the CAMA setting?
- How does the framework handle samples with multiple missing modalities, and can it choose which single modality to acquire for each sample?
- Why do imputation-based strategies sometimes outperform the true upper-bound heuristics? Is this due to evaluation noise, imputation artifacts, or flawed bound definitions?
- What is the exact protocol for excluding negative-gain tasks at the split level, and how sensitive are the reported results to this exclusion?
- Are the observed differences between imputation-based KL-Divergence and baseline strategies statistically significant under paired tests across folds or runs?
- How does the train/test distribution shift caused by feeding imputed embeddings to a classifier trained on real embeddings affect acquisition performance and calibration?
- What are the exact final hyperparameters for each dataset and configuration, given that only search ranges are provided?

### Limitations

- No comparison to state-of-the-art active feature or modality acquisition methods, so the relative contribution is not demonstrated.
- Selective exclusion of tasks with negative gain may inflate the reported effectiveness and does not reflect real-world deployment scenarios.
- The oracle and upper-bound heuristics are not guaranteed to be true bounds for the full subset-selection problem, as they are based on greedy selection.
- The method requires costly generative imputation models and is not analyzed for multi-round or dynamic acquisition settings.
- Fairness and bias implications of prioritizing patients for additional medical testing are only mentioned qualitatively; no empirical fairness analysis is provided.
- The framework assumes a fixed model and does not address model retraining or adaptation after acquiring additional modalities.

### Ethics

Ethical concerns flagged: **True**

## Usage and Cost

- Requests: 6
- Prompt tokens: 257,567
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 253,471
- Completion tokens: 22,575
- Reasoning tokens reported: 15,498
- Total tokens: 280,142
- Estimated total: $0.04181841

Full individual reviews and raw JSON responses are in `review_bundle.json`.
