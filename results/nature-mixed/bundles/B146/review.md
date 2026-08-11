# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B146.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 1, 'Reject': 4}
- Estimated API cost: **$0.020916**

## Final Meta-review

The paper proposes Smoothed Gradient Ascent (SGA), a fine-tuning-based LLM unlearning method that extends standard Gradient Ascent (GA) by incorporating semantically related 'normal' data through a tunable smoothing rate r. SGA combines gradient ascent on the forget set with gradient descent on safe data to mitigate GA's divergence problem while preserving model utility. The authors provide a theoretical analysis of the optimal smoothing rate, and evaluate SGA on three benchmarks (TOFU, Harry Potter, MUSE-News) across multiple base LLMs (Llama2-7B, OPT-2.7B, Phi-1.5B). Results show SGA consistently outperforms GA and achieves competitive performance against other baselines when r is properly tuned.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 2 | 2.400 | 0.490 | 2-3 |
| Significance | 2 | 2.400 | 0.490 | 2-3 |
| Soundness | 2 | 2.200 | 0.400 | 2-3 |
| Presentation | 2 | 2.400 | 0.490 | 2-3 |
| Contribution | 2 | 2.200 | 0.400 | 2-3 |
| Overall | 4 | 4.400 | 0.800 | 4-6 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Addresses a relevant and practical problem: the instability of standard Gradient Ascent in LLM unlearning.
- The core idea is simple, intuitive, and novel—applying generalized label smoothing to combine forget and normal data.
- Comprehensive empirical evaluation across three diverse benchmarks (entity, copyright, news) and three base models.
- Consistently outperforms the GA baseline across most metrics and benchmarks, demonstrating the value of incorporating normal data.
- Theoretical analysis provides some qualitative guidance on the sign and feasible range of the smoothing rate.
- Ablation studies on normal data generation methods add useful depth.

### Weaknesses

- The theoretical analysis is heuristic: minimizing the update norm does not directly correspond to optimal unlearning quality, and the connection is not rigorously justified.
- The optimal smoothing rate r is highly data/model-dependent and requires extensive grid search; no practical selection method is provided, limiting real-world applicability.
- Empirical gains over GA are often marginal (e.g., TOFU FQ differences are tiny), and statistical significance is not reported.
- On Harry Potter, many SGA configurations still produce astronomically high PPL (e.g., 6.27e72), indicating the divergence problem is not fully resolved.
- On MUSE-News, SGA only marginally improves KnowMem on Dr (from 0 to 1.95 vs. retained model's 55.0), and most r values fail the criterion—suggesting high sensitivity and limited practical utility.
- The method requires generating or selecting normal data (via embeddings or GPT-4o-mini), adding complexity and computational cost not present in simpler baselines.
- Missing comparison with recent strong baselines (e.g., RULE, SimPO, DRAGON) limits the assessment of its state-of-the-art positioning.
- Some presentation issues: malformed equations, empty appendix sections, and figures/tables not well integrated into the text.

### Questions

- How does minimizing the update norm relate to optimal forgetting quality and utility preservation? Could a larger update with a better direction lead to better unlearning?
- The optimal r is found via grid search. Is there a heuristic or adaptive method to select r in practice without extensive tuning? Could the sign of gradient alignment be estimated cheaply?
- On Harry Potter, several SGA settings still produce catastrophic PPL values (e.g., 6.27e72). How is this considered successful unlearning? What is the practical utility of such models?
- On TOFU, FQ values are extremely low across all methods. How should these be interpreted? Are the differences statistically significant (e.g., confidence intervals, multiple seeds)?
- The normal data generation differs across benchmarks (embedding similarity vs. GPT-4o-mini). How does the quality and nature of normal data affect the optimal r and final performance? What prompts were used for GPT generation (Appendix D appears empty)?
- Why is SGA not compared with RULE and SimPO, which are mentioned in related work? How does it fare against these more recent methods?
- What is the computational overhead of generating normal data and training on it, compared to simpler baselines like GA or FLAT?
- In the ablation study, the optimal r shifts depending on the normal data source. How should practitioners choose between embedding-based and GPT-based generation?

### Limitations

- The optimal smoothing rate is model/task-dependent and fixed during training; dynamic adjustment is left as future work, limiting the method's potential.
- The reliance on generated normal data (especially GPT-4o-mini) adds computational cost and external dependencies, raising reproducibility concerns.
- Extreme smoothing rates still cause divergence, so the method does not fully eliminate GA's instability.
- The paper does not discuss potential negative societal impacts in depth, such as misuse of unlearning to evade content moderation or accountability.
- Evaluation is limited to English-language benchmarks; generalizability to other languages or modalities is unexplored.
- The theoretical analysis covers only a single gradient step and does not account for multi-step training dynamics.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 136,300
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 127,340
- Completion tokens: 10,942
- Reasoning tokens reported: 0
- Total tokens: 147,242
- Estimated total: $0.02091645

Full individual reviews and raw JSON responses are in `review_bundle.json`.
