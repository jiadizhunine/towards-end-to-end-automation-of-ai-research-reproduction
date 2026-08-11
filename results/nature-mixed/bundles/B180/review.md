# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B180.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.016922**

## Final Meta-review

The paper introduces MATT (Model-Aware Tokenizer Transfer), a method for adapting LLMs to new tokenizers by leveraging model internals rather than relying solely on embedding-level heuristics. The core contribution is the Attention Influence Modeling (AIM) objective, which distills inter-token communication patterns (weighted value states) from the original model into the transferred model by aligning segment-level attention representations. MATT operates as an efficient warm-up stage (a few GPU hours) before standard language modeling, freezing all parameters except new embeddings. Experiments on Gemma 3 (4B/12B) and Qwen 3 (0.6B) across six languages show MATT substantially outperforms heuristic baselines (WECHSEL, FOCUS, Transtokenizers, TokAlign), recovering a large fraction of original performance, especially on generative tasks (e.g., 60-70% BLEU recovery on Long FLORES where baselines achieve near-zero). The paper includes ablations on layer depth, initialization methods, loss functions, and convergence speed.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 4.000 | 0.000 | 4-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.200 | 0.400 | 3-4 |
| Significance | 4 | 3.600 | 0.490 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.200 | 0.400 | 3-4 |
| Contribution | 3 | 3.400 | 0.490 | 3-4 |
| Overall | 6 | 6.400 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel and well-motivated approach: AIM objective is a creative departure from embedding-only methods, using attention dynamics to guide tokenizer transfer.
- Strong empirical results: MATT consistently outperforms heuristic baselines across diverse languages and models, with particularly dramatic gains on generative tasks (translation).
- Computational efficiency: Only a few GPU hours are needed (3-5 hours), making it practical for real-world use compared to LM-based objectives.
- Comprehensive evaluation: Tests across multiple languages (Ukrainian, Arabic, German, English, Japanese, Swahili), model families (Gemma 3, Qwen 3), scales (0.6B-12B), and tasks (Belebele, MMLU, FLORES).
- Good ablation studies: Appendix includes analysis of layer depth, initialization methods, loss functions, and convergence speed, providing useful insights.
- Clear writing and helpful figures: The method is explained well, with illustrative diagrams and pseudocode for the segmentation algorithm.

### Weaknesses

- Missing comparison to language-modeling-based fine-tuning: The paper claims efficiency over LM objectives but doesn't directly compare MATT to standard LM fine-tuning with frozen layers, which is the most natural alternative baseline.
- Missing comparison to Zero-Shot Tokenizer Transfer (Minixhofer et al., 2024), a key model-aware baseline that also uses the full model. This weakens the claim of 'state-of-the-art' performance.
- Lack of continual pretraining evaluation: The paper only evaluates the initialized model, but real tokenizer transfer pipelines include continual pretraining. It's unclear if MATT's advantage persists after further training.
- Tied embeddings limitation: MATT's effectiveness is strongly dependent on tied input-output embeddings, which limits applicability to many modern models (e.g., Llama, Qwen use untied embeddings). The appendix discusses this but doesn't provide a satisfactory solution.
- No statistical significance testing: Results are reported as single point estimates without variance or significance tests across multiple runs.
- Limited task diversity: Evaluation is restricted to three benchmarks (Belebele, MMLU variants, FLORES); no other tasks like question answering or code generation are tested.
- Theoretical justification is thin: while the intuition is plausible, there is no rigorous analysis of why matching segment-level attention patterns should lead to good downstream performance.

### Questions

- 1. How does MATT compare to standard language modeling fine-tuning with frozen non-embedding parameters (e.g., training embeddings with LM loss for the same number of steps)? This comparison is crucial to validate the efficiency claim over LM objectives.
- 2. Why was Zero-Shot Tokenizer Transfer (Minixhofer et al., 2024) not included as a baseline? Given that it is the most closely related work, an experimental comparison would strengthen the claims of superiority.
- 3. What happens when MATT-initialized embeddings are followed by continual pretraining? Does the advantage over heuristic baselines persist, narrow, or widen?
- 4. For models with untied embeddings, what is the actual performance gap? The appendix mentions preliminary experiments but doesn't report numbers. Could you provide quantitative results for untied settings?
- 5. What is the variance across random seeds? Are the reported results statistically significant?
- 6. How sensitive is MATT to the choice of segmentation function (e.g., word-based vs. offset-based)? The ablation on layer depth is helpful, but a similar analysis for segmentation would strengthen the paper.
- 7. Does MATT work for encoder-only models as the limitation section suggests? Any preliminary evidence?
- 8. The paper uses 50M tokens per language for MATT but 500M for FOCUS. Is this comparison fair? Could FOCUS benefit from more data, or does the comparison control for training data?
- 9. Why does the AIM objective work better for generative tasks (e.g., FLORES) than for discriminative tasks (e.g., MMLU)? Is there a theoretical or empirical explanation?
- 10. The ablation shows that using only the last layer works best. Why do you think this is the case? Does this suggest that the AIM objective on lower layers might be harmful rather than just redundant?

### Limitations

- The method requires tied input-output embeddings for full effectiveness; models with untied embeddings (common in newer architectures) may not benefit as much, and the proposed workarounds are not fully validated.
- The paper evaluates only the initialized model, not after continual pretraining, which is the typical use case for tokenizer transfer. This limits the assessment of long-term utility.
- The segmentation algorithm's behavior in edge cases (e.g., very long tokens, languages with complex morphology) is not thoroughly analyzed, and the worst-case scenario of a single segment could make the objective ineffective.
- No theoretical analysis of why matching segment-level attention patterns should transfer well; the argument is intuitive but lacks formal grounding.
- The method has not been tested on encoder-only architectures or non-decoder transformers, limiting its generalizability.
- Potential negative societal impact: Improving tokenizer transfer could make it easier to adapt LLMs to low-resource languages, which is generally positive, but could also facilitate the deployment of models with hidden biases or errors in these languages without adequate evaluation. This is not discussed in the paper.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 107,455
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 98,495
- Completion tokens: 11,099
- Reasoning tokens reported: 0
- Total tokens: 118,554
- Estimated total: $0.01692211

Full individual reviews and raw JSON responses are in `review_bundle.json`.
