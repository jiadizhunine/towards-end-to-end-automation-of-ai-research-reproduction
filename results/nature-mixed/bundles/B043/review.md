# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B043.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.028100**

## Final Meta-review

This paper investigates the optimal allocation of compute between full-precision (FP) pretraining and quantization-aware training (QAT) for language models. Through extensive experiments across model sizes (86M to 2.2B parameters), QAT bit widths (1, 2, 4, 6 bits), and token budgets, the authors demonstrate that the optimal QAT fraction increases with total compute, contradicting prior assumptions of a fixed optimal fraction. They propose a unified loss scaling law predicting final loss as a function of model size, FP/QAT token counts, and bit width, achieving R² > 0.98 and generalizing to a 2.2B model not used in fitting. The scaling law enables practical predictions including optimal bit-width under memory constraints and when QAT matches FP accuracy. Additionally, they introduce a QAT & Learning Rate Cooldown Fusion technique showing consistent improvements for 4-bit and 6-bit settings. The work provides practical guidelines for efficient QAT planning and quantifies potential compute waste from suboptimal allocation.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 3.200 | 0.400 | 3-4 |
| Clarity | 4 | 3.600 | 0.490 | 3-4 |
| Significance | 3 | 3.400 | 0.490 | 3-4 |
| Soundness | 3 | 3.200 | 0.400 | 3-4 |
| Presentation | 4 | 3.600 | 0.490 | 3-4 |
| Contribution | 3 | 3.400 | 0.490 | 3-4 |
| Overall | 7 | 6.800 | 0.400 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses a practically important and under-explored problem: optimal compute allocation between FP training and QAT for LLMs
- Extensive experimental scale: 757 QAT experiments across diverse configurations (model sizes, bit widths, token counts)
- Novel finding that optimal QAT fraction increases with total compute, contradicting prior fixed-fraction assumptions
- Unified loss scaling law with excellent fit (R² > 0.98) and validation on held-out 2.2B models and a different dataset (SlimPajama)
- Practical implications: bit-width selection under memory constraints, quantification of wasted compute, and cooldown fusion technique
- Thorough uncertainty analysis with bootstrap parameter significance testing
- Good reproducibility with detailed hyperparameters and experimental configurations in appendices
- Clear writing and helpful takeaway boxes summarizing key findings

### Weaknesses

- The loss scaling law has 13-16+ fitted parameters with an ad hoc functional form, raising concerns about overfitting despite bootstrap analysis; no comparison against simpler alternative forms is provided
- Limited generality: results are from a single architecture (Llama-style transformer), a single QAT method (ParetoQ), and primarily one dataset (DCLM)
- The QAT & Cooldown Fusion technique shows inconsistent benefits: it hurts 1-bit and some 2-bit cases, and improvements are small in absolute perplexity terms (0.06-1.72%), with limited mechanistic analysis
- Optimal QAT fraction prediction has relatively high MAE (0.074-0.102), and the practical cost of this error is not quantified
- The 'tokens-per-parameter-byte' statistic lacks strong theoretical justification for its specific functional form
- The 'wasted tokens' metric is derived from the same scaling law, creating potential circularity in evaluating cooldown fusion benefits
- No comparison against alternative QAT strategies (e.g., progressive quantization, mixed-precision training, knowledge distillation) or downstream task evaluation

### Questions

- How sensitive is the optimal QAT fraction to the choice of QAT algorithm (e.g., LSQ, GPTQ-based QAT)? Would different methods yield different optimal fractions?
- Can you provide more analysis on the overfitting risk of the scaling law? How does the held-out 2.2B prediction compare with a simpler model (e.g., per-bit-width fits or fewer parameters)?
- Why does QAT & Cooldown Fusion consistently help 4-6 bit but hurt 1-2 bit? Is this related to quantization noise dominating learning dynamics?
- What is the practical loss cost of a 10% deviation from the predicted optimal QAT fraction for a concrete example?
- Why was tokens-per-parameter-byte chosen over alternatives like tokens-per-parameter or FLOPs-based measures? Was an empirical search conducted over other normalizations?
- How would the optimal QAT fraction change if evaluated on downstream tasks (e.g., MMLU, GSM8K) rather than perplexity?
- Could the scaling law be simplified by removing interaction terms without significant loss of fit quality?
- What is the variance of optimal fraction predictions across random initializations for the scaling law fit?
- Does the scaling law predict a plateau or continued divergence for 1-2 bit at high token counts?
- How would results change with untied embeddings, which are common in larger models?

### Limitations

- The study is limited to a single architecture (Llama-2 style decoder-only transformer) and a single quantization method (ParetoQ); generality to other architectures (e.g., MoE), quantization schemes, or training objectives is unknown
- The scaling law is purely empirical and may not extrapolate beyond tested ranges of model sizes, token counts, and bit widths
- Cooldown fusion shows negative results for 1-bit and 2-bit QAT, limiting its applicability for very low precision
- The analysis treats token count as a direct proxy for compute; QAT overhead is only briefly discussed for a specific hardware setup
- The paper does not explore interactions with post-training techniques (e.g., SFT, RLHF) or downstream task performance
- Potential societal impacts of more efficient QAT (e.g., enabling on-device deployment with privacy implications, or environmental benefits) are not discussed, though these are likely minor for efficiency-focused work
- The computational cost of conducting 757 experiments is not discussed, which may be a practical barrier for replication

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 186,526
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 177,566
- Completion tokens: 11,485
- Reasoning tokens reported: 0
- Total tokens: 198,011
- Estimated total: $0.02810013

Full individual reviews and raw JSON responses are in `review_bundle.json`.
