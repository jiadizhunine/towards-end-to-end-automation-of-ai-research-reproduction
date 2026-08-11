# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B146.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.025435**

## Final Meta-review

The paper proposes Smoothed Gradient Ascent (SGA), a fine-tuning-based LLM unlearning method that combines gradient ascent on forget data with gradient descent on generated 'normal' data through a tunable smoothing rate r, motivated by generalized label smoothing. The authors provide a theoretical analysis for an optimal smoothing rate, and evaluate SGA on TOFU, Harry Potter, and MUSE-News benchmarks across several base LLMs. They report improvements over standard gradient ascent on several metrics.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 2 | 2.000 | 0.000 | 2-2 |
| Quality | 2 | 2.000 | 0.000 | 2-2 |
| Clarity | 2 | 1.800 | 0.400 | 1-2 |
| Significance | 2 | 2.000 | 0.000 | 2-2 |
| Soundness | 2 | 2.000 | 0.000 | 2-2 |
| Presentation | 2 | 1.800 | 0.400 | 1-2 |
| Contribution | 2 | 2.000 | 0.000 | 2-2 |
| Overall | 4 | 3.800 | 0.400 | 3-4 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important practical problem: the instability and utility collapse of gradient ascent (GA) when used for LLM unlearning.
- The idea of mixing forget data with normal data via a smoothing rate is simple, intuitive, and easy to implement.
- Broad empirical evaluation across three benchmarks and multiple base model families/scales, with comparisons to several baselines.
- Provides a theoretical motivation for the smoothing rate, even if practical guidance is limited.

### Weaknesses

- There are serious sign inconsistencies in the mathematical formulation: GA is described as gradient ascent, but the update direction in Section 4.2 with r=0 is written as -g_f, which is gradient descent. The objective in Eq. (3) appears to minimize the forget loss, contradicting the intended ascent. This makes the actual algorithm ambiguous and undermines the theoretical derivation.
- The theoretical derivation of the optimal smoothing rate minimizes the norm of the one-step update, which is not directly connected to forgetting quality or model utility. Moreover, the derived r* is not used quantitatively; only its sign is estimated and used heuristically, with weak empirical support.
- Empirical results are mixed and often not consistently better than baselines. On TOFU, SGA's forget quality is frequently no better than GA and remains far from the retained model. On MUSE-News, model utility is severely degraded (KnowMem on D_r = 1.95 vs. 55.0 for the retained model). On Harry Potter, many smoothing-rate settings lead to astronomically high perplexities, indicating model collapse.
- The method relies on generating or selecting normal data, either from an external model (GPT-4o-mini) or from a retain set, which contradicts the stated claim of requiring only forget data and introduces additional cost, dependency, and potential privacy concerns.
- Reproducibility is incomplete: the appendix containing the prompts for normal data generation is empty, no code is provided, and the selection of the smoothing rate is based on a grid search with no clear practical procedure. No error bars or statistical significance tests are reported.
- The method introduces an additional hyperparameter (r) and an additional data-generation requirement (K normal samples per forget sample), but the paper does not discuss computational overhead or sensitivity to K.

### Questions

- In Eq. (3) and Eq. (5), what is the exact sign convention? With r=0, the update is -g_f, which is gradient descent, not gradient ascent. Please clarify the objective and update direction.
- Why is minimizing the update norm ||d(r)||^2 the right criterion for choosing the smoothing rate? How does this relate to the forgetting-quality versus model-utility trade-off?
- How is the smoothing rate r selected in practice? Is it tuned on a validation set, and are the reported results the best over a grid rather than from a single procedure? Given the large variation across r values, how would a practitioner choose r for a new task?
- On MUSE-News, SGA's KnowMem on D_r is only 1.95 versus 55.0 for the retained model. How is this acceptable in terms of utility preservation, and what does this imply about the practical usefulness of SGA?
- What exactly are the prompts and filtering criteria for GPT-4o-mini normal data generation? The appendix describing this is empty, making the method non-reproducible.
- Given that the theoretical optimal smoothing rate is dynamic during training, have the authors considered dynamically adjusting r, and would that improve results?

### Limitations

- The method requires an auxiliary model (GPT-4o-mini) or access to a retain set to generate normal data, adding cost and external dependency.
- The smoothing rate must be tuned per model and benchmark; no automatic or principled selection method is provided, and the theoretical guidance only gives a rough sign heuristic.
- Utility preservation is poor on MUSE-News and certain Harry Potter settings, with severe model degradation even in some reported 'best' configurations.
- Forgetting quality is low in absolute terms on TOFU, and no theoretical guarantees for forgetting effectiveness or utility preservation are provided.
- The paper does not discuss potential negative societal impacts, such as misuse of unlearning to evade accountability or malicious removal of safety knowledge.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 125,332
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 121,236
- Completion tokens: 30,179
- Reasoning tokens reported: 23,714
- Total tokens: 155,511
- Estimated total: $0.02543463

Full individual reviews and raw JSON responses are in `review_bundle.json`.
