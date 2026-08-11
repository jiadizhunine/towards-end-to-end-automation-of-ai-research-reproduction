# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B011.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.017932**

## Final Meta-review

The paper presents a systematic study of when reasoning data should be introduced in LLM training, comparing injection during pretraining versus SFT while varying scale, diversity, and quality. Using an 8B hybrid Mamba-Transformer model pretrained from scratch for 1T tokens, the authors create several base models with different reasoning corpora and then apply SFT and RLVR. They report that front-loading reasoning data into pretraining yields durable gains that SFT cannot compensate for, that pretraining benefits more from diversity/scale while SFT benefits more from quality, that high-quality pretraining data can have latent benefits unlocked after SFT, and that naive SFT scaling with mixed-quality data can harm math reasoning. The paper derives an asymmetric data-allocation principle as practical guidance.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 2.800 | 0.400 | 2-3 |
| Quality | 2 | 2.000 | 0.000 | 2-2 |
| Clarity | 2 | 2.400 | 0.490 | 2-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 2 | 2.000 | 0.000 | 2-2 |
| Presentation | 2 | 2.400 | 0.490 | 2-3 |
| Contribution | 2 | 2.400 | 0.490 | 2-3 |
| Overall | 4 | 4.000 | 0.000 | 4-4 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The research question is important and timely, directly addressing data-recipe design in the pretraining-to-post-training pipeline.
- The experiments are ambitious and large-scale, with multiple 8B models pretrained from scratch for 1T tokens and then carried through SFT and RL, which is rare in the literature.
- The fully crossed pretraining/SFT setup enables some tests of synergy, catch-up, and overfitting hypotheses across stages.
- The derived asymmetric principle (diversity in pretraining, quality in SFT) is actionable and plausible, with practical implications for the field.
- Including an RL phase demonstrates an attempt to measure downstream compounding effects of pretraining choices.

### Weaknesses

- All experiments are single runs without multiple seeds, error bars, or statistical significance tests, making the reported gains (e.g., +19%, +11%, +15%) difficult to distinguish from training noise.
- The comparisons confound multiple factors: dataset size, diversity, quality, token budget, and domain composition are not independently controlled, especially between D_SHQ and D_LDQ.
- The RL phase is applied only to M_base and M_LMQ, not to M_SHQ or M_LDQ, leaving the central asymmetric-diversity/quality claims unverified after RL.
- Potential benchmark contamination is not addressed, despite using public SFT-style and pretraining corpora that may overlap with evaluation benchmarks such as GSM8K, MATH, AIME, and MMLU.
- The manuscript has notable notation inconsistencies, undefined dataset names (e.g., D_LLQ, D_ALF'), redacted details, and unexplained numerical mismatches across tables, harming reproducibility and clarity.
- The token and sample budgets are not controlled between pretraining and SFT phases, so the conclusion that front-loading is superior could be confounded with total reasoning-token quantity.
- The notion of "quality" is operationalized via answer length or dataset source, which is a crude proxy and not independently varied from domain composition or formatting.

### Questions

- How is the total number of reasoning tokens controlled between pretraining (200B tokens) and SFT (4.8M samples) when comparing the catch-up hypothesis? Could differences in absolute quantity explain the observed advantage of front-loading?
- How do the authors isolate diversity from scale and quality when D_LDQ (336B tokens) differs from D_SHQ (1.2M samples) in all three dimensions? Would a high-quality diverse dataset of equal scale change the conclusions?
- Why is the RL phase run only on M_base and M_LMQ? Would running RL on all four pretraining variants support or refute the claim that pretraining advantages compound through RL?
- What exact decontamination procedures, if any, were used to prevent overlap between the training corpora and the evaluation benchmarks?
- Can the authors clarify the definition and construction of D_ALF' and resolve the inconsistent notation across D_LDQ/D_LLQ/D_LMQ?
- How was the 20% reasoning-data mix ratio in pretraining chosen, and how sensitive are the findings to this ratio?

### Limitations

- Only one model architecture (8B hybrid Mamba-Transformer), one pretraining scale (1T tokens), and one base corpus are used, limiting generalizability.
- No statistical significance testing, multiple seeds, or confidence intervals are provided for any central comparison.
- The pretraining and SFT data budgets are not matched, confounding phase effects with data quantity.
- Potential benchmark contamination is a serious concern given the use of large public datasets that may overlap with evaluation sets.
- Proprietary datasets, redacted implementation details, and no released code/data prevent independent replication.
- The diversity-versus-quality comparison and answer-length filtering are confounded with dataset scale and domain distribution.
- The paper lacks a limitations section and does not discuss out-of-distribution generalization, safety, or broader negative societal impacts.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 83,576
- Cache-hit prompt tokens: 3,840
- Cache-miss prompt tokens: 79,736
- Completion tokens: 24,138
- Reasoning tokens reported: 17,281
- Total tokens: 107,714
- Estimated total: $0.01793243

Full individual reviews and raw JSON responses are in `review_bundle.json`.
