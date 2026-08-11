# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B173.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.030265**

## Final Meta-review

The paper introduces MENLO, a framework and dataset for evaluating and improving the native-like response quality of LLMs across 47 language varieties. The framework operationalizes native-like quality into four dimensions (fluency, tone, localized tone, localized factuality) grounded in sociolinguistic audience design theory. The dataset consists of 6,423 human-annotated prompt-response preference pairs (81,014 annotations) with high inter-annotator agreement (Krippendorff's α = 0.84). The paper systematically evaluates zero-shot LLM judges, finding that pairwise evaluation significantly outperforms pointwise scoring, and that detailed grading rubrics provide additional benefits. Through fine-tuning with RL (GRPO), reward shaping, and multi-task learning, the authors train judges (Qwen3-4B and Llama4-Scout) that approach human-level agreement. Finally, they demonstrate that RL-trained judges can serve as generative reward models to improve policy model quality through post-training, though LLM judges tend to overestimate improvements compared to human raters. The dataset and framework are released publicly.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 4.000 | 0.000 | 4-4 |
| Quality | 3 | 3.400 | 0.490 | 3-4 |
| Clarity | 3 | 3.400 | 0.490 | 3-4 |
| Significance | 4 | 3.800 | 0.400 | 3-4 |
| Soundness | 3 | 3.400 | 0.490 | 3-4 |
| Presentation | 3 | 3.400 | 0.490 | 3-4 |
| Contribution | 4 | 3.800 | 0.400 | 3-4 |
| Overall | 7 | 7.400 | 0.490 | 7-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Large-scale, high-quality dataset: 47 language varieties, 6,423 pairs, 81,014 annotations, with high inter-annotator agreement (α = 0.84), significantly advancing prior multilingual evaluation resources.
- Theoretically grounded framework: the use of audience design principles from sociolinguistics provides a principled and novel operationalization of native-like quality, going beyond simple naturalness metrics.
- Comprehensive evaluation of judge setups: systematic comparisons of pointwise vs. pairwise evaluation and the impact of rubrics yield clear, actionable findings (pairwise > pointwise, rubrics help).
- Thorough training investigation: clear ablations of reward components (binary, smoothing, preference bonus), SFT vs. RL, and multi-task vs. single-task training provide valuable insights for the community.
- Practical utility demonstrated: trained judges used as reward models improve policy model quality, validated by both LLM and human evaluation, unifying evaluation and optimization.
- Statistical rigor: bootstrap confidence intervals for key comparisons strengthen the reliability of the claims.
- Well-structured paper with extensive appendices covering annotation guidelines, per-language results, and additional experiments.
- Dataset and framework released publicly, enabling further research in multilingual evaluation.

### Weaknesses

- Prompts are translated/localized from English templates rather than independently authored in each language, which may not fully capture native discourse structures and introduces potential English-centric biases; this is acknowledged only in the appendix.
- Human validation for the post-training experiment is limited to 10 high-resource languages, leaving uncertainty about generalizability to lower-resource varieties.
- The Localized Factuality dimension consistently shows poor performance (Macro-F1 ~25.9 for the best model) and limited improvement from training, yet the paper does not deeply investigate the causes or propose effective solutions (e.g., retrieval augmentation).
- LLM judges systematically overestimate improvements compared to human raters (+0.5 to +0.6 on average), which is acknowledged but not deeply analyzed or mitigated.
- Cross-language performance varies widely (e.g., tr-TR at 82.1% vs. bn-BD at 37.9% preference accuracy), but the paper provides limited analysis of the causes of these disparities or correlations with language resources/typology.
- The claim that RL-trained judges are 'on par with human annotators' could benefit from more rigorous statistical justification, as comparing model-human agreement with human-human agreement is not a direct comparison of the same quantity.
- The paper does not compare against alternative approaches such as existing multilingual reward models (e.g., M-REWARDBENCH) or translation-based evaluation methods.

### Questions

- How do you ensure that the 'native-like' target is not biased toward a particular register, age group, or regional dialect within each language variety? Could the high inter-annotator agreement partly reflect shared biases among annotators selected from similar backgrounds?
- For the Localized Factuality dimension, what specific challenges did you identify? Why does RL training not help? Could you provide examples of typical failure modes and discuss whether retrieval-augmented generation or tool use might be more effective?
- The human validation subset covers only 10 high-resource languages. How representative is this subset of the full 47 languages, and are there plans to extend human validation to lower-resource varieties?
- LLM judges overestimate improvements by +0.5 to +0.6 compared to human raters. Do you have hypotheses about why this occurs (e.g., calibration, stylistic preferences)? How might this be mitigated?
- Can you provide more analysis on why certain languages (e.g., bn-BD, ru-RU) consistently underperform? Is this due to model capabilities, annotation quality, prompt complexity, or language resource levels?
- How sensitive are the judge performance results to the specific LLMs used to generate responses in the dataset? Would rankings change with different response generators?
- What is the distribution of preferences in the dataset (A vs. B wins, ties)? How does this relate to judge behavior and positional bias mitigation?
- Have you compared your RL-trained judges against existing multilingual reward models to better contextualize your improvements?
- How do the four quality dimensions correlate with each other? Are they truly orthogonal, or do they capture overlapping aspects of response quality?

### Limitations

- Prompts are derived from English templates and localized rather than natively authored, which may limit the authenticity of 'native-like' quality assessment and introduce English-centric biases.
- Human validation of the policy improvement experiment is limited to 10 high-resource languages, leaving uncertainty about effectiveness in lower-resource settings.
- LLM judges tend to overestimate the magnitude of improvements compared to human raters, suggesting that automated evaluation may not fully capture nuanced quality differences.
- The Localized Factuality dimension shows limited improvement from training, indicating that current approaches may be insufficient for this dimension and may require fundamentally different methods (e.g., retrieval).
- The dataset covers 47 language varieties but may not be representative of all dialects and sociolects within each variety, and the annotation guidelines may encode specific cultural assumptions.
- The potential negative societal impact of optimizing for 'native-like' quality is not discussed; this could reinforce linguistic prescriptivism or marginalize non-standard varieties and non-native speakers.
- Annotator compensation is mentioned, but details on working conditions, data privacy, and long-term impact on annotators are sparse.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 201,218
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 192,258
- Completion tokens: 11,869
- Reasoning tokens reported: 0
- Total tokens: 213,087
- Estimated total: $0.03026453

Full individual reviews and raw JSON responses are in `review_bundle.json`.
