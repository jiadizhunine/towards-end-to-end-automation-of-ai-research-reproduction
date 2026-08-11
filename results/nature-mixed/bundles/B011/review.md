# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B011.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.017495**

## Final Meta-review

This paper presents a systematic study of how reasoning data, varying in scale, diversity, and quality, affects LLM performance when introduced at different training stages (pretraining vs. SFT). The authors pretrain 8B-parameter hybrid Mamba-Transformer models from scratch on 1T tokens with different reasoning data configurations (large diverse, small high-quality, mixed), then apply SFT and RLVR. Key findings include: (1) front-loading reasoning data into pretraining creates durable advantages (+19% on expert benchmarks) that SFT cannot fully replicate; (2) an asymmetric data allocation principle where diversity matters most in pretraining while quality dominates in SFT; (3) naive scaling of SFT data with mixed-quality data can be harmful; and (4) high-quality pretraining data can have latent effects only activated after SFT. The study includes extensive ablations on data ratios, model scale (1.2B), and instruction-following trade-offs, providing actionable guidance for data allocation across training pipelines.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 2.800 | 0.400 | 2-3 |
| Significance | 3 | 3.400 | 0.490 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 2.800 | 0.400 | 2-3 |
| Contribution | 3 | 3.400 | 0.490 | 3-4 |
| Overall | 7 | 6.800 | 0.400 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Systematic, large-scale experimental design with fully crossed pretraining × SFT conditions and controlled token budgets
- Clear, actionable findings that challenge conventional separation of pretraining and reasoning, with practical implications for data allocation
- Comprehensive evaluation across math, science, code, and instruction-following benchmarks
- The 'latent effect' discovery (high-quality pretraining data showing benefits only after SFT) is novel and interesting
- Multiple ablations (data ratio sensitivity, model scale generalization, length-filtered data) strengthen the main claims
- Results are consistent across training phases (pretraining → SFT → RL), showing compounding benefits of early reasoning injection
- Transparent about architecture and hyperparameters, aiding reproducibility within the constraints of proprietary data

### Weaknesses

- The distinction between 'diversity' and 'quality' is confounded with dataset scale (DLDQ has 268M samples vs. DSHQ's 1.2M), making it difficult to isolate the effect of any single factor
- The RL phase only compares two models (Mbase vs. MLMQ), limiting conclusions about interactions between pretraining strategy and RL
- No variance estimates or statistical significance testing are reported, so the robustness of key differences (e.g., the 'latent effect') is uncertain
- The definition of 'quality' relies on answer length as a proxy, which is not independently validated
- Potential benchmark contamination is not addressed, given the use of open web corpora that may contain reasoning examples similar to evaluation sets
- The claim of being the 'first systematic study' may be overstated given related work on mid-training with reasoning data
- The 20% reasoning token ratio in pretraining is unrealistically high for practical scenarios, and compute costs are not thoroughly discussed
- Only one main model scale (8B) and a single architecture family are used; the 1.2B ablation is limited in scope

### Questions

- Can you disentangle the effects of data diversity from data scale? Would a downsampled diverse dataset (e.g., 10M samples from DLDQ) still show the same pretraining advantages over DSHQ?
- How exactly is the small DSHQ dataset repeated during pretraining to reach the 80B token budget? Does repetition cause overfitting or memorization that could explain the results?
- Why were RL experiments only conducted on two configurations? Would the findings hold for other combinations like MLDQ+SFTSHQ or MSHQ+SFTSHQ?
- Could you provide variance estimates across multiple seeds for key results, especially the 'latent effect' claim?
- How do you define and validate 'quality' beyond answer length? Have you confirmed that longer answers correlate with better reasoning quality through human evaluation or other means?
- What is the token-level duplication rate between the pretraining corpora and evaluation benchmarks? Could contamination explain the large gains on GSM8K and MATH-500?
- How sensitive are the conclusions to the specific choice of DSHQ as the 'high-quality' dataset? Would similar results hold with other high-quality reasoning datasets?
- What is the compute cost breakdown for each phase, and how should practitioners trade off pretraining vs. SFT compute given your findings?
- How do your findings relate to the mid-training literature (e.g., OctoThinker, Essential AI)? Would conclusions change if reasoning data were introduced in a separate mid-training phase?
- The SFT results show dramatic performance drops with large diverse SFT data. Could this be due to data quality, format mismatch, or the diversity itself? How is this disentangled from the pretraining-SFT interaction?

### Limitations

- The study uses proprietary NVIDIA datasets and a specific hybrid architecture, limiting generalizability to other models and data sources
- Only one main model scale (8B) is used; the 1.2B ablation is limited and does not cover all configurations
- The RL phase is restricted to two models, so the interaction between pretraining data choice and RL effectiveness is not fully explored
- The paper does not report computational costs in detail, which is important for practitioners assessing feasibility
- Potential benchmark contamination from pretraining corpora is not addressed
- The paper does not discuss potential negative societal impacts, such as the concentration of compute resources or potential misuse of improved reasoning capabilities
- The 'quality' of reasoning data is operationalized through dataset source and answer length, which may not capture all dimensions of data quality

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 115,254
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 106,294
- Completion tokens: 9,247
- Reasoning tokens reported: 0
- Total tokens: 124,501
- Estimated total: $0.01749541

Full individual reviews and raw JSON responses are in `review_bundle.json`.
