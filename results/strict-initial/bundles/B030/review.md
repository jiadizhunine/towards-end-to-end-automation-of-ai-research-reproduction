# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B030.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.030272**

## Final Meta-review

The paper proposes a framework for recycling pretrained Mixture-of-Experts (MoE) checkpoints by growing them into larger models. It introduces two orthogonal growth strategies: depth growth via interpositional layer copying (duplicating each layer in place) and width growth via expert duplication with injected Gaussian noise. Experiments on 3B-to-6B and 17B-to-70B models show that interposition outperforms stacking for converged checkpoints, that small noise aids expert specialization, and that final accuracy correlates positively with the sunk compute invested. The authors claim a 10.66% relative accuracy gain over a scratch-trained baseline under the same additional compute budget.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 2 | 2.400 | 0.490 | 2-3 |
| Significance | 3 | 2.600 | 0.490 | 2-3 |
| Soundness | 2 | 2.200 | 0.400 | 2-3 |
| Presentation | 2 | 2.400 | 0.490 | 2-3 |
| Contribution | 2 | 2.400 | 0.490 | 2-3 |
| Overall | 4 | 4.400 | 0.490 | 4-5 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Addresses an important and timely problem: reusing the sunk compute in pretrained MoE checkpoints instead of training from scratch.
- First systematic study of model growth specifically for well-converged MoE models, offering clear recipes for both depth and width expansion.
- Interpositional depth growth is a simple, effective alternative to stacking, validated at 3B and 17B scales and supported by layer-wise norm analysis.
- Width growth via expert duplication with small Gaussian noise is a practical and well-motivated strategy that improves downstream accuracy over exact copying.
- Large-scale demonstration from a 17B to a 70B MoE over ~1T tokens shows the approach can be applied to production-scale models.
- The timing study across checkpoints with a fixed additional budget provides actionable guidance on when to grow and suggests that more sunk cost tends to help.

### Weaknesses

- The headline 10.66% improvement over 'training from scratch' is ambiguous and likely not a like-for-like comparison: the baseline appears to be a 17B model, not a 70B model trained from scratch, and the comparison uses additional FLOPs rather than total FLOPs.
- The claimed function-preserving property of width growth is mathematically suspect: duplicating experts and router logits and doubling top-k without renormalization or scaling doubles the MoE output magnitude, and the paper does not address this.
- The growth-timing analysis is confounded: later checkpoints are already better, and the fixed learning rate after growth may unfairly disadvantage checkpoints taken from the annealing phase; no LR tuning per checkpoint was performed.
- Evaluation is narrow, covering only MMLU and six English multiple-choice QA tasks, with no open-ended generation, code, math, or multilingual benchmarks, and no significance testing.
- No comparison with existing strong model-growth methods (e.g., LiGO, LEMON, progressive stacking) is provided beyond stack vs. interposition.
- Reproducibility is limited by proprietary datasets, missing details on post-growth hyperparameters, and only a partial code fragment; no full implementation is released.
- Only one growth order (depth then width) is tested, so the claimed orthogonality and interaction effects are not fully validated.

### Questions

- What exactly is the scratch baseline used to compute the 10.66% gain? Is it a 70B model trained from scratch with the same additional FLOPs or the 17B base model? What are the exact total FLOPs for both pipelines?
- For width growth with sigmoid routing, how is the output magnitude preserved when both experts and router logits are duplicated and top-k is doubled? Is any normalization or scaling applied to keep the transformation function-preserving?
- Were post-growth learning rates tuned separately for each checkpoint? Could the observed performance of late-annealing checkpoints improve if the LR were adjusted to match their schedule phase?
- Why is it necessary to double top-k when duplicating experts? How is the increased activated-expert FLOPs accounted for in the FLOPs budget compared to scratch training?
- How does the proposed width-growth method compare to other expert-diversification schemes, such as random reinitialization of new experts or adding noise only to router logits?
- Would the conclusions change if the order of depth and width growth was swapped? Have the authors tested the interaction between the two growth strategies?
- Can the authors provide confidence intervals or multiple seeds for the key timing and noise-injection results to rule out evaluation noise?

### Limitations

- The methods are evaluated only on MoE architectures; applicability to dense Transformer models is not demonstrated.
- The pretraining data mixture is proprietary, hindering independent reproduction and external verification.
- The large-scale experiment is a single run with no repeated seeds, so the stability of the observed gains is unknown.
- The evaluation suite is restricted to English knowledge/reasoning tasks; broader model capabilities are not assessed.
- No analysis is provided on expert load balancing or routing diversity after width growth, despite these being central to MoE training.
- The theoretical understanding is heuristic (layer-wise norm trends), with no formal guarantees or causal analysis.
- The claimed efficiency benefit is not quantified in terms of total GPU-hours or environmental cost, including the base pretraining.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 188,246
- Cache-hit prompt tokens: 27,776
- Cache-miss prompt tokens: 160,470
- Completion tokens: 27,600
- Reasoning tokens reported: 20,715
- Total tokens: 215,846
- Estimated total: $0.03027157

Full individual reviews and raw JSON responses are in `review_bundle.json`.
