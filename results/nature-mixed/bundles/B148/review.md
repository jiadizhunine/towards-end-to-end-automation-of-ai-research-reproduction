# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B148.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 2, 'Reject': 3}
- Estimated API cost: **$0.039321**

## Final Meta-review

The paper introduces Cohort-based Active Modality Acquisition (CAMA), a new test-time problem setting where, given a cohort of samples with some available modalities and a budget to acquire additional modalities for a subset of samples, the goal is to select which samples to acquire to maximize a global cohort-level performance metric (e.g., AUROC, AUPRC). The authors formalize the problem, derive acquisition functions from these metrics, and propose several strategies: oracle and upper-bound heuristics for benchmarking, and imputation-based strategies that use generative models (DDPMs, BC-VAEs) to estimate the counterfactual benefit of acquiring a missing modality. The imputation-based KL-Divergence strategy is highlighted as the most effective. The framework is evaluated on four multimodal datasets (UKBB, MIMIC Symile, MIMIC HAIM, MOSEI) with up to 15 modalities and 100k samples, showing that the proposed method can outperform simpler baselines like uncertainty sampling and random selection in many settings.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.600 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 5.600 | 0.800 | 5-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The CAMA problem setting is novel and practically relevant, clearly distinguishing itself from individual-level active learning and active feature acquisition paradigms.
- The paper provides a comprehensive framework, including a formal problem formulation, theoretical derivation of acquisition functions from standard metrics (AUROC, AUPRC), and a clear taxonomy of strategies.
- The evaluation is extensive, covering diverse datasets (healthcare, emotion recognition), varying modality counts (up to 15), and a large-scale real-world UK Biobank cohort (100k samples).
- Inclusion of oracle strategies and upper-bound heuristics provides useful performance ceilings for benchmarking.
- The paper is generally well-written and organized, with detailed appendices for reproducibility.
- The finding that imputation-based KL-Divergence can outperform simpler baselines is an actionable and interesting contribution.

### Weaknesses

- The central claim that the imputation-based KL-Divergence strategy 'consistently and significantly outperforms all other non-oracle methods' is not fully supported by the results. On MIMIC HAIM and some MOSEI tasks, simpler baselines (e.g., Probability, Random) perform comparably or better.
- The evaluation excludes tasks where the multimodal model underperforms the unimodal baseline (negative gains), which introduces selection bias and limits the generalizability of the conclusions. The proportion of excluded tasks and the impact on results are not adequately discussed.
- The experimental results are noisy and lack rigorous statistical significance testing (e.g., pairwise comparisons with confidence intervals). Some tables show high standard errors, making comparisons unreliable.
- The computational cost of the DDPM-based imputation (K=100 samples per test sample) is significant, and the paper does not provide a thorough cost-benefit analysis versus the faster BC-VAE variant.
- The novelty is incremental: while the cohort-level setting is new, the acquisition functions are largely adaptations of existing active learning principles (uncertainty, KL-divergence) to this new context.
- The paper does not compare against more sophisticated baselines from the Active Modality Acquisition literature, such as reinforcement learning-based approaches (e.g., Kossen et al., 2023).

### Questions

- 1. What is the proportion of excluded tasks (with negative gain) per dataset? How would the overall results and conclusions change if these tasks were included? This is crucial for assessing the generalizability of the proposed method.
- 2. The oracle strategies can achieve G_full > 1, indicating that a mix of unimodal and multimodal samples outperforms the fully multimodal cohort. What are the characteristics of samples the oracle does NOT acquire? Does this suggest the multimodal model is poorly calibrated or overfits to certain modalities?
- 3. The imputation-based KL-Divergence strategy sometimes slightly outperforms its corresponding upper-bound heuristic (True KL-Div). Can the authors explain this surprising result? Is it due to the averaging over K samples acting as a form of regularization?
- 4. On MIMIC HAIM, why do simple baselines (e.g., Probability, Random) often perform comparably or better than the proposed imputation-based methods? What are the dataset/task characteristics that make the proposed strategy less effective?
- 5. How sensitive are the results to the quality of the imputation model? Have the authors tested with degraded imputation performance (e.g., fewer DDPM samples, a weaker generative model)?
- 6. What happens when the acquisition budget is very small (e.g., 1-5% of the cohort)? Are there differences in the ranking of strategies compared to larger budgets?
- 7. The paper focuses on binary classification. How would the acquisition functions need to be adapted for multi-class or regression settings?
- 8. How does the method generalize to scenarios where multiple modalities are missing and the decision involves choosing which modality to acquire for each sample, rather than a single fixed target modality?

### Limitations

- The evaluation excludes tasks with negative gains, which biases results toward favorable scenarios and limits applicability to cases where the additional modality's benefit is unknown.
- The computational cost of the DDPM-based imputation is high, potentially limiting practical deployment in real-time or very large cohort settings.
- The paper focuses on binary classification; extension to multi-class or regression is not addressed.
- Fairness and equity concerns in healthcare applications are acknowledged but not empirically analyzed or mitigated. The strategic acquisition of costly medical tests could exacerbate health inequities if not carefully deployed.
- The evaluation uses synthetically created missing modalities for most datasets, which may not fully capture real-world missingness patterns.
- The paper assumes a single model f that can process any subset of modalities, which may not hold in all practical settings.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 267,718
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 258,758
- Completion tokens: 10,964
- Reasoning tokens reported: 0
- Total tokens: 278,682
- Estimated total: $0.03932113

Full individual reviews and raw JSON responses are in `review_bundle.json`.
