# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B091.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 2, 'Reject': 3}
- Estimated API cost: **$0.026958**

## Final Meta-review

The paper proposes ICL Activation Alignment (IA2), a self-distillation priming step before supervised fine-tuning (SFT) that aligns the hidden activations of a model performing SFT with its own activations during in-context learning (ICL). The authors show that ICL and SFT produce different activation patterns, and that IA2 priming before SFT improves accuracy and calibration on 12 benchmarks across Qwen and Llama models, using LoRA and (IA)^3 adapters, with extensive experiments including out-of-distribution evaluations and statistical significance tests.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 3 | 2.800 | 0.400 | 2-3 |
| Significance | 2 | 2.600 | 0.490 | 2-3 |
| Soundness | 2 | 2.400 | 0.490 | 2-3 |
| Presentation | 3 | 2.800 | 0.400 | 2-3 |
| Contribution | 2 | 2.400 | 0.490 | 2-3 |
| Overall | 4 | 4.600 | 0.800 | 4-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The core idea of using the model's own ICL activations as a training signal for SFT is novel and moves beyond output-level distillation.
- The empirical evaluation is very extensive: over 13,000 trained models, 12 benchmarks, two model families, multiple PEFT methods, OOD evaluations, and significance testing.
- The analysis of activation similarity and LoRA weight-subspace overlap provides a useful conceptual view and suggests IA2 explores a different region of weight space than SFT alone.
- The paper includes a reproducibility statement with code release and detailed experimental details in the appendix.

### Weaknesses

- The central activation comparison (ICL vs SFT) is confounded: ICL activations are collected with demonstrations in the prompt, while SFT activations are collected with query only, so the observed differences may be due to input context length/content rather than different adaptation mechanisms; no controlled comparisons (e.g., SFT model with demonstrations, base model with/without demos) are provided.
- Missing key baselines: the paper does not compare IA2 against standard output-level knowledge distillation from the ICL teacher nor prior context-distillation methods, so the unique benefit of activation alignment over simpler distillation is not established.
- Hyperparameter selection is potentially biased: the best learning rate is chosen per method/dataset based on validation performance, and significance tests are computed on those best-performing runs; no nested validation or correction for multiple comparisons is reported.
- Many per-dataset improvements have high variance and are not individually significant; calibration improvements are not statistically significant for larger N (N=16 and N=32 in Table 5), weakening the broad claim of calibration benefits.
- IA2-only can be much worse than SFT-only on some tasks (e.g., SciQ accuracy 6.9%), indicating the method's success depends on ICL quality and is not universally beneficial; when ICL overfits or performs poorly, IA2 can inherit those issues.
- The computational/memory overhead of collecting dense ICL activations is not quantified, and may be prohibitive for long sequences or large datasets; this is especially important because the method requires access to model internals (not applicable to black-box APIs).
- The formal objective in Equation (3) and the implementation described in Section 4 are inconsistent regarding which token positions are matched, making the method hard to reproduce from the text alone.
- The method is only evaluated with low-rank adapters (LoRA rank 8, (IA)^3) on small base models (1B-4B) and up to 128 training examples; its effectiveness for larger models, full fine-tuning, and larger data regimes is unknown.

### Questions

- How does IA2 compare to simply performing SFT on the ICL-generated responses (same pseudo-labels as IA2) without the activation MSE term? This would isolate the contribution of activation alignment from response distillation.
- What are the activation similarities between two independently trained SFT models, between SFT and the base model, and between ICL models from different random seeds? Without such controls, how can the observed ICL-SFT activation gap be attributed to the adaptation mechanism rather than the presence of demonstrations?
- What is the additional wall-clock time and GPU memory required for collecting ICL activations and running IA2 relative to standard SFT? Is storing dense activation tensors for all training samples feasible for 10k+ samples?
- How was the best learning rate selected, and do the reported significance results hold under nested validation or with fixed hyperparameters?
- Why does IA2-only collapse on SciQ multi-token? Does the variable-length generation cause instability in the activation matching objective?
- How sensitive are the results to the choice/order/number of ICL demonstrations? Does IA2 amplify harmful biases present in ICL demonstrations?
- What is the subspace overlap with a null random baseline? Is the 39% overlap statistically meaningful?

### Limitations

- The main motivation is weakened by the confounded activation comparison and lack of control experiments.
- No comparison with prior context-distillation methods (e.g., Snell et al., Chen et al.) or standard knowledge distillation baselines, so practical advantages are not demonstrated.
- The method requires access to model internals and is not applicable to black-box API models.
- The activation collection step is memory-intensive and may be impractical for long sequences or large datasets; this overhead is not quantified.
- Experiments are limited to small PEFT models (1B-4B); full fine-tuning and larger models are untested.
- The method depends on the base model's ICL capability; when ICL is unreliable (e.g., Llama-1B on SciQr), IA2 does not help or harms.
- No analysis of potential negative societal impacts or bias amplification through ICL demonstrations is provided.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 144,294
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 140,198
- Completion tokens: 26,140
- Reasoning tokens reported: 19,769
- Total tokens: 170,434
- Estimated total: $0.02695839

Full individual reviews and raw JSON responses are in `review_bundle.json`.
