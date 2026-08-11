# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B035.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.021154**

## Final Meta-review

The paper investigates robustness of multi-task model merging and identifies two under-explored failure modes: disparity in task vector norms and low confidence of source models. To address these, it proposes DisTaC, a knowledge-distillation-based preconditioning method that rescales task vectors to a common norm and sharpens source-model predictions using only unlabeled data. Experiments on eight vision tasks with CLIP ViT-B/32 and ViT-L/14 backbones, across four merging methods (task arithmetic, TIES, Consensus TA, TSVM), show that DisTaC largely recovers merging accuracy lost under these failure modes. The paper also provides practical guidelines such as shrinking long task vectors and using overconfident sources followed by post-hoc calibration.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.200 | 0.400 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Identifies two practical and previously underexplored failure modes in model merging, with clear empirical demonstrations across multiple merging methods and backbones.
- Proposes a simple, label-free preconditioning method (DisTaC) that is broadly applicable and consistently improves all tested merging algorithms.
- Experiments are reasonably extensive, covering two CLIP backbones, four merging methods, and multiple confidence-calibration techniques (label smoothing, Mixup, focal loss).
- Provides theoretical justifications for the failure modes and actionable practical guidelines for practitioners.
- The method is computationally lightweight (500 distillation steps) and does not require altering the underlying merge algorithm.

### Weaknesses

- Evaluation is limited to CLIP-based image classification on eight vision tasks; generalization to NLP, other modalities, or non-CLIP architectures is unproven.
- DisTaC requires per-task unlabeled data and task identity; this may be impractical in privacy-constrained or data-scarce settings.
- No comparison with alternative preconditioning or calibration approaches (e.g., simple norm normalization, logit temperature scaling, or equivalent-compute fine-tuning), making the relative benefit unclear.
- The paper does not evaluate the combined setting where norm mismatch and low-confidence occur simultaneously, nor does it report calibration metrics (e.g., ECE) for the final merged model.
- The theoretical analysis relies on strong simplifying assumptions (orthogonal task vectors, small displacements, quadratic approximations), and some theoretical results are not directly validated by experiments.
- Hyperparameters such as the scaling factor, temperatures, regularizer weight, and number of distillation steps are not given a clear practical recipe without using validation labels, weakening the 'unlabeled-only' claim.

### Questions

- Does DisTaC work when norm mismatch and low confidence occur simultaneously, and how are the scaling factor and temperatures chosen in that case?
- How sensitive are the results to the number of distillation steps K, the regularizer weight beta, the target norm choice, and the amount of unlabeled data?
- How does DisTaC compare to simple alternatives such as direct norm normalization followed by fine-tuning, logit temperature scaling, or self-distillation with hard labels?
- What is the calibration error of the merged model after applying DisTaC and post-hoc temperature scaling?
- Do the identified failure modes appear in non-CLIP architectures, language models, or generative models, and does DisTaC transfer there?
- An ablation isolating the norm-rescaling component from the confidence-sharpening component would help clarify the contribution of each; is that available?

### Limitations

- The empirical study is confined to eight vision classification tasks with CLIP encoders; conclusions do not necessarily extend to other domains, model families, or modalities.
- The method requires access to per-task unlabeled data; if such data is unavailable or does not match the fine-tuning distribution, DisTaC cannot be applied reliably.
- The paper introduces several hyperparameters that need tuning; the lack of a clear label-free selection procedure limits practical applicability.
- The theoretical analyses are based on idealized assumptions and are best viewed as intuition rather than rigorous proofs for realistic settings.
- DisTaC deliberately increases source-model overconfidence, and while the paper advises post-hoc calibration of the merged model, it does not experimentally verify that calibration is restored.
- No error bars or statistical significance tests are reported, so the robustness of the improvements across runs is not established.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 117,944
- Cache-hit prompt tokens: 3,840
- Cache-miss prompt tokens: 114,104
- Completion tokens: 18,460
- Reasoning tokens reported: 12,070
- Total tokens: 136,404
- Estimated total: $0.02115411

Full individual reviews and raw JSON responses are in `review_bundle.json`.
