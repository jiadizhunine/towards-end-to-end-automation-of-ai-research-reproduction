# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B169.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **5/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 3, 'Reject': 2}
- Estimated API cost: **$0.027348**

## Final Meta-review

The paper proposes EvA, an evolutionary attack for graph structure perturbations in node classification. It directly optimizes the discrete attack objective via genetic algorithms, avoiding gradient relaxation, and introduces sparse encoding, targeted mutation, and divide-and-conquer for scalability. EvA demonstrates consistent accuracy drops over PRBCD across multiple datasets and extends to non-differentiable objectives such as robustness certificates and conformal prediction. Reviewers acknowledge the novelty and strong empirical results but raise concerns about computational cost fairness, presentation, and lack of statistical rigor.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 2 | 2.000 | 0.632 | 1-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 2 | 2.000 | 0.632 | 1-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 5 | 5.600 | 0.490 | 5-6 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Directly optimizes the true discrete attack objective without gradient relaxation.
- Consistent empirical superiority over gradient-based attacks across datasets and threat models.
- Black-box and objective-agnostic design enables attacks on non-differentiable goals (certificates, conformal).
- Provides scalable techniques (sparse encoding, stacked inference, divide-and-conquer).
- Ablations show contributions of individual components.

### Weaknesses

- Very high query complexity (population×iterations forward passes) and no explicit query-budget comparison with baselines, undermining fairness.
- Approximate adaptive sampling for certificate attacks may bias search; final evaluation uses proper MC only.
- No paired statistical significance tests; some results overlap with baselines.
- Presentation is poor: typos, redacted references, mislabeled tables, garbled abstract text, hindering reproducibility.
- Targeted attacks still rely on differentiable margin proxy and are worse than PRBCD at low budget.
- Local-constrained variant is significantly weaker, indicating a trade-off.
- No theoretical grounding or convergence guarantees.
- Many hyperparameters without sensitivity analysis; D&C is ad hoc.
- Novel objectives lack simple baselines (e.g., random edge flips) for context.

### Questions

- What is the total number of forward passes used by EvA vs PRBCD in each experiment and how are compute budgets made comparable?
- Does EvA maintain its advantage under a strict query budget (e.g., 1k-10k forward passes) typical of real black-box attacks?
- Does the approximate adaptive sampling for certificate attacks bias the search toward perturbations that fail to reduce certified ratio under full MC evaluation?
- Are differences between EvA and PRBCD statistically significant when using paired tests across splits and seeds?
- For conformal attack, how sensitive are results to calibration set choice and exchangeability violations?
- How are D&C subset sizes and budget splits chosen, can global budget be exceeded?
- How sensitive is EvA to hyperparameters like population size, mutation rate, crossover count?
- Can EvA work with hard-label only, or does it need a differentiable proxy for targeted attacks?

### Limitations

- Extremely query-hungry, impractical for query-limited adversaries.
- Certificate attack search uses statistically biased approximation.
- D&C relaxation may miss cross-subset interactions and is ad hoc.
- Local-constrained variant suffers reduced effectiveness.
- No experiments on very large graphs beyond Ogbn-Arxiv (which is medium) or heterogeneous graphs.
- No discussion of defenses against evolutionary attacks or transferability.
- Potential for misuse, though standard in adversarial ML.
- No theoretical analysis of convergence or optimality.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 152,628
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 148,532
- Completion tokens: 23,364
- Reasoning tokens reported: 17,489
- Total tokens: 175,992
- Estimated total: $0.02734787

Full individual reviews and raw JSON responses are in `review_bundle.json`.
