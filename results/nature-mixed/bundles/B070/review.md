# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B070.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.020533**

## Final Meta-review

The paper introduces mmBERT, a modern multilingual encoder-only language model pretrained on ~2.9-3T tokens across 1833 languages. Key contributions include: (1) an inverse mask ratio schedule that progressively lowers masking during training, (2) an inverse temperature sampling ratio for language mixture that becomes more uniform over time, and (3) a Cascaded Annealed Language Learning (ALL) approach that starts with 60 high-resource languages and progressively adds languages, including 1723 low-resource languages only during the final 100B token decay phase. The model uses a ModernBERT-inspired architecture with the Gemma 2 tokenizer. Results show improvements over existing multilingual encoders (XLM-R, mGTE, EuroBERT) on GLUE, XTREME, MTEB v2, and CoIR benchmarks, with particularly strong performance on low-resource languages added during the decay phase. The models, data, and checkpoints are open-sourced.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 4 | 3.800 | 0.400 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.200 | 0.400 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses a clear and important gap: the lack of modern multilingual encoder-only models since XLM-R (2019)
- Novel training techniques (inverse mask scheduling, cascading annealed language learning, inverse temperature sampling) are clearly described and show empirical benefits
- Comprehensive evaluation across multiple benchmarks (GLUE, XTREME, MTEB v2, CoIR) covering classification, retrieval, and structured prediction
- Strong empirical results showing consistent improvements over existing multilingual baselines across all benchmarks
- Demonstrates that adding low-resource languages only during the decay phase can dramatically boost performance, a practical insight for resource-constrained training
- Open-sources models, data, and checkpoints, enabling reproducibility and further research
- Efficiency improvements over previous multilingual encoders through modern architecture choices
- Good contextualization within the encoder-only model revival literature

### Weaknesses

- Limited ablation studies: the inverse mask schedule is only ablated in the decay phase, not during full pre-training, making it unclear if this contributes to the main results
- Low-resource language evaluation is limited to only two languages (Tigrinya and Faroese), which is insufficient to draw broad conclusions about the approach's effectiveness across the 1700+ added languages
- The comparison to decoder models like o3 and Gemini 2.5 Pro is somewhat misleading and potentially unfair given different training objectives, scales, and evaluation setups; only two low-resource QA tasks are used
- The model merging approach (TIES-merging) appears ad hoc and is not well-validated; its ineffectiveness for the small model suggests limited generalizability
- Discrepancy between claimed 3T tokens and ~2.9T shown in training data tables
- The inverse temperature schedule is not thoroughly analyzed - it's unclear how sensitive results are to the specific temperature values chosen
- The benchmark evaluation methodology uses oracle hyperparameter selection, which may inflate results and makes comparisons less reliable
- No comparison with more recent multilingual models beyond EuroBERT, and the comparison with decoder models is limited to only one small model (Gemma 3 270M)
- The training recipe is extremely complex with many design choices (mask ratios, temperatures, language sets, data mixtures) that are not individually validated
- The paper does not thoroughly address potential negative societal impacts or environmental costs of training large models

### Questions

- Could you provide more detailed ablations for the inverse mask ratio schedule? Specifically, how does performance compare when using a fixed mask rate (e.g., 15% or 30%) vs. the progressive schedule during the full pre-training phase?
- Can you elaborate on why only 2 languages (Tigrinya and Faroese) were used for evaluating low-resource performance? Are there other low-resource languages with suitable evaluation datasets that could strengthen this analysis?
- How sensitive are the results to the specific temperature values (0.7, 0.5, 0.3) used in the inverse temperature sampling? Did you try other schedules?
- Could you provide more analysis of the model merging approach? How much does TIES-merging improve over simply using the best individual decay checkpoint, and why was TIES chosen over simpler approaches like weight averaging?
- The paper mentions that mmBERT small had to lower LR/WD after 1.2T tokens due to plateauing - could you elaborate on this and whether similar issues were encountered with the base model?
- Have you considered evaluating on additional low-resource language tasks beyond question answering, such as NER or POS tagging, to demonstrate broader improvements?
- Could you clarify the exact token count - the abstract says 3T but the training data table sums to ~2.9T tokens?
- How does the model perform on languages that were not included in any training stage? Is there any zero-shot transfer capability to completely unseen languages?
- What is the effect of the temperature annealing independent of the language addition? Would keeping a fixed temperature but adding languages achieve similar results?
- Why was the oracle hyperparameter selection used for evaluation? How robust are the results to different hyperparameter choices?

### Limitations

- The paper acknowledges that many languages still have very small amounts of data or none at all, particularly for high-quality filtered data
- The evaluation of low-resource languages is limited to only 2 languages, which may not be representative of the full range of 1833 languages included in training
- The comparison with decoder models is somewhat limited and potentially unfair given different training objectives and scales
- The paper does not thoroughly analyze potential negative societal impacts, such as potential biases in multilingual models or environmental costs of training large models
- The model merging approach adds complexity without clear evidence that it provides significant benefits over simpler approaches
- The paper does not discuss potential issues with the Gemma 2 tokenizer for certain scripts or languages
- The training recipe is computationally expensive (40 days on 8xH100 for base), which may limit reproducibility for other research groups
- The paper does not address potential issues with using Wikipedia as a data source for low-resource languages or the risk of amplifying biases in web-crawled multilingual data

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 133,909
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 124,949
- Completion tokens: 10,768
- Reasoning tokens reported: 0
- Total tokens: 144,677
- Estimated total: $0.02053299

Full individual reviews and raw JSON responses are in `review_bundle.json`.
