# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B091.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.022502**

## Final Meta-review

This paper investigates the functional differences between In-Context Learning (ICL) and Supervised Fine-Tuning (SFT) in language models, showing that they produce distinct internal activation patterns. Based on this observation, the authors propose ICL Activation Alignment (IA2), a self-distillation technique that aligns a model's activations during SFT with those produced during ICL, used as a priming step before standard SFT. The method is evaluated across 12 benchmarks, two model families (Llama and Qwen), multiple model sizes (1B-4B), and both single-token classification and multi-token generation tasks. Results show consistent improvements in accuracy and calibration over SFT-only training, particularly in few-shot settings, with analysis of activation similarity, weight subspace overlap, and comparisons with knowledge distillation baselines.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.400 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Clear motivation and well-posed research question about the functional relationship between ICL and SFT
- Extensive empirical validation: 13,000+ trained models, 12 benchmarks, multiple model sizes and families, and both single- and multi-token settings
- The proposed IA2 method consistently improves over SFT in terms of accuracy and calibration, with statistical significance testing provided
- Good analysis of activation similarity and weight subspace overlap that provides mechanistic evidence for why the method works
- Simple and practical method requiring only a one-time activation collection step, with inference as cheap as standard SFT
- Includes useful ablations (LoRA parameters, (IA)3 vs LoRA) and comparison with knowledge distillation baselines
- Honest discussion of limitations, including cases where IA2 underperforms ICL
- Reproducibility: code and detailed experimental setup are provided

### Weaknesses

- Experiments limited to relatively small models (1B-4B); scaling behavior to larger models is unknown
- The technical novelty is somewhat limited—activation-level distillation has been explored in prior work; the contribution is primarily in applying it to ICL-to-SFT transfer
- The paper lacks a deeper mechanistic analysis of WHY activation alignment helps; the explanation remains at a high level ('ICL activations contain rich information')
- High variance in some results (standard deviations of 10-20 accuracy points), raising questions about robustness and practical significance in certain settings
- Comparison with knowledge distillation is limited to only two datasets, weakening the claim that activation alignment is superior to output-level distillation
- In multi-token settings, IA2→SFT sometimes underperforms ICL, and this gap is not fully investigated
- The IA2+SFT joint training results are inconsistent, and the explanation for this inconsistency is not fully developed
- The paper does not explore the impact of ICL demonstration order or quality on the collected activations, which could affect reproducibility
- The computational overhead of the activation collection step is mentioned but not quantified

### Questions

- How does IA2 perform with larger models (e.g., 7B-70B)? The paper only tests 1B-4B models.
- Can you provide quantitative estimates of the computational overhead for the activation collection step in IA2, and how does this scale with model size and dataset size?
- The paper claims ICL activations are 'information-rich'—can you provide more mechanistic evidence for why this is the case beyond the activation similarity analysis?
- How sensitive is IA2 to the choice of ICL demonstrations used for collecting target activations? Does the order or quality of demonstrations matter?
- In Figure 3, the scatter plot shows that extreme activation similarity can hurt accuracy—what is the optimal level of alignment and how can it be achieved reliably?
- Could you provide more details on the IA2+SFT loss weighting? Specifically, how sensitive are the results to the β parameter, and how was the range determined for each model family?
- In the multi-token setting where IA2→SFT underperforms ICL, would increasing LoRA rank or using full fine-tuning close this gap? Have you tested this hypothesis?
- Can IA2 be combined with other fine-tuning approaches beyond SFT, such as RLHF or DPO?
- How does IA2 compare to other activation-level distillation methods (e.g., Aguilar et al., 2020) in terms of performance? The paper only compares against soft-label KD.
- Did you investigate the effect of the number of ICL demonstrations used to generate target activations? Does the quality of IA2 degrade with fewer/more demonstrations?

### Limitations

- Experiments are limited to relatively small models (1B-4B), and scaling behavior is unknown
- The method requires a one-time inference pass over training data to collect ICL activations, which adds computational overhead that is not precisely quantified
- The comparison with knowledge distillation is limited to only two datasets, which may not be representative
- The paper does not deeply analyze which layers are most important for alignment or whether selective layer alignment could be more effective
- The paper does not explore the impact of IA2 on other model properties such as diversity of generations, robustness to adversarial inputs, or catastrophic forgetting
- The method's benefits are primarily demonstrated in few-shot settings; its value in data-rich scenarios is less clear
- The paper does not address potential negative societal impacts, such as the risk of amplifying biases present in ICL demonstrations into the fine-tuned weights (though the work itself is benign)
- The paper does not provide a theoretical framework for understanding when and why activation alignment works, limiting generalizability of the findings

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 150,820
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 141,860
- Completion tokens: 9,346
- Reasoning tokens reported: 0
- Total tokens: 160,166
- Estimated total: $0.02250237

Full individual reviews and raw JSON responses are in `review_bundle.json`.
