# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B035.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **8/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.021199**

## Final Meta-review

This paper addresses robustness issues in multi-task model merging by identifying two critical failure modes: (1) task vector norm disparity, where differences in fine-tuning hyperparameters lead to task vectors of vastly different magnitudes, and (2) low confidence of source models, produced by techniques like label smoothing, Mixup, or focal loss. The authors provide theoretical analysis for both phenomena and propose DisTaC (Distillation for Task vector Conditioning), a knowledge distillation-based method that pre-conditions task vectors before merging by rescaling their norms and increasing model confidence using only unlabeled data. The method is evaluated on eight vision tasks with CLIP ViT-B-32/L-14 backbones and four NLP tasks with RoBERTa and Llama2, across seven merging methods, consistently improving post-merge accuracy, often restoring performance to levels comparable to idealized settings. The paper also provides practical guidelines for practitioners (shrink longer task vectors, make models overconfident before merging, apply post-hoc calibration) and demonstrates computational efficiency (~3.2 seconds for 500 steps on ViT-B-32).

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 4.000 | 0.000 | 4-4 |
| Quality | 4 | 4.000 | 0.000 | 4-4 |
| Clarity | 4 | 4.000 | 0.000 | 4-4 |
| Significance | 4 | 4.000 | 0.000 | 4-4 |
| Soundness | 4 | 4.000 | 0.000 | 4-4 |
| Presentation | 4 | 4.000 | 0.000 | 4-4 |
| Contribution | 4 | 4.000 | 0.000 | 4-4 |
| Overall | 8 | 8.000 | 0.000 | 8-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Identifies two important and under-explored failure modes in model merging (norm disparity and low confidence) that are highly relevant to real-world deployment scenarios
- Proposes a simple, elegant, and computationally efficient solution (DisTaC) that addresses both failure modes simultaneously using only unlabeled data
- Comprehensive experimental evaluation across multiple architectures (ViT-B-32, ViT-L-14, RoBERTa-base/large, Llama2-7b), seven merging methods, and both vision and NLP domains
- Provides theoretical justifications (Propositions 1 and 2) supporting the empirical findings
- Demonstrates robustness of DisTaC to limited data size and data quality degradation
- Clear practical guidelines for practitioners (shrink vs. stretch, calibration strategy)
- Well-written with clear organization, helpful visualizations, and thorough ablation studies

### Weaknesses

- Evaluation is limited to classification tasks; extension to generation tasks is acknowledged but not explored
- Requires access to unlabeled data from each task's distribution, which may be challenging in some real-world scenarios
- Hyperparameter selection (temperature pair Ttcr/Tstu, scaling factor κt, regularization weight β) is not deeply analyzed and lacks clear automatic selection guidance
- Theoretical analysis relies on simplifying assumptions (task vector orthogonality, small norms, positive-definite Hessians) that may not hold in all practical settings
- Some mixed results in NLP experiments (e.g., TIES-merging on Llama2-7b occasionally degrades with DisTaC), with limited analysis of why
- Limited comparison with alternative pre-conditioning approaches (e.g., simple norm scaling alone) in main results

### Questions

- How sensitive is DisTaC to the choice of temperature pair (Ttcr, Tstu)? Is there a principled way to select these values for new tasks or domains?
- How is the scaling factor κt determined in practice, especially when norm disparities are complex or multiple task vectors have high norms? Could adaptive or learned scaling factors improve results?
- How does DisTaC perform when both norm disparity and low confidence occur simultaneously? Is there an interaction effect requiring different hyperparameter choices?
- How does DisTaC handle severe distribution shifts in the unlabeled data (beyond Gaussian blur), such as out-of-domain or adversarial perturbations?
- In the NLP experiments, why does DisTaC sometimes degrade TIES-merging performance on Llama2-7b? What are the underlying reasons and does this suggest limitations at very large scales?
- The paper mentions DisTaC can occasionally surpass teacher performance. Could you provide more analysis on when and why this happens?
- How does post-hoc calibration interact with DisTaC-conditioned sources? Does DisTaC affect calibration of the final merged model, and how much does temperature scaling recover?
- Would combining DisTaC with other preprocessing methods (e.g., weight normalization or orthogonalization) yield further improvements?

### Limitations

- The method is primarily evaluated on classification tasks; extending to generation tasks (e.g., LLM text generation, image generation) is identified as future work
- DisTaC requires access to unlabeled data from each task's distribution, which may pose challenges in privacy-sensitive or resource-constrained scenarios
- The theoretical analysis relies on simplifying assumptions (orthogonality of task vectors, small perturbation assumptions, NTK approximation) that may not fully capture real-world complexity
- The paper focuses on two specific failure modes and does not exhaustively explore other potential sources of task interference in model merging
- Hyperparameter selection (temperatures, scaling factor, regularization weight) requires per-scenario tuning without a fully automatic procedure
- The overconfidence induced by DisTaC may raise reliability concerns, though post-hoc calibration is suggested as a remedy
- Potential negative societal impact is not discussed in detail, though the method itself appears benign and does not introduce new ethical concerns beyond standard model merging practices

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 143,749
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 134,789
- Completion tokens: 8,225
- Reasoning tokens reported: 0
- Total tokens: 151,974
- Estimated total: $0.02119855

Full individual reviews and raw JSON responses are in `review_bundle.json`.
