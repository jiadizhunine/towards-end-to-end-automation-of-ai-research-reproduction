# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B180.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.017765**

## Final Meta-review

The paper introduces MATT, a tokenizer-transfer method for large language models that initializes new input embeddings by aligning segment-level attention influence patterns (weighted value states) between the original model and a model with an extended tokenizer. The proposed Attention Influence Modeling (AIM) objective trains only the input embeddings after a FOCUS-based heuristic initialization, keeping all other parameters frozen. Experiments on Gemma 3 (4B/12B) and Qwen 3 (0.6B) across multiple languages show that MATT outperforms embedding-only heuristic baselines on Belebele, Global MMLU, MMMLU, and Long FLORES, while requiring only a few GPU hours. The paper also provides ablations on loss variants, layer depth, initialization methods, and freezing strategies.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 3 | 2.800 | 0.400 | 2-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 2.800 | 0.400 | 2-3 |
| Overall | 6 | 5.600 | 0.800 | 4-6 |
| Confidence | 4 | 3.600 | 0.490 | 3-4 |

### Strengths

- Novel use of attention dynamics (weighted value states) rather than only embedding similarity for tokenizer transfer, which is well-motivated and goes beyond prior heuristics.
- Efficient training: only input embeddings are trained, with optional depth restriction, enabling strong performance recovery in a few GPU hours and lower VRAM usage compared to full-model adaptation.
- Comprehensive evaluation across multiple model families, scales, and typologically diverse languages, demonstrating consistent improvements over heuristic baselines, particularly on generative tasks.
- Useful ablations on loss function, layer depth, initialization, and freezing strategy, providing insights into the method's behavior.
- The offset-based segmentation algorithm is a practical and principled solution to tokenizer mismatch, and MATT is orthogonal to heuristic initialization methods, allowing combination with FOCUS or Transtokenizers.

### Weaknesses

- No comparison to strong model-aware baselines such as Zero-Shot Tokenizer Transfer (Minixhofer et al., 2024) or to compute-equivalent language-modeling/embedding fine-tuning, so the claim of state-of-the-art is not fully substantiated.
- All main results appear to come from single runs without reported variance, standard deviations, or statistical significance tests, making it difficult to assess robustness of the improvements.
- The evaluation stops at the initialized model and does not include continual pretraining, which is the ultimate intended use case, so the long-term practical benefit remains unclear.
- The method relies on tied input-output embeddings to fully exploit the learned input embeddings; for untied models, performance gains are reduced and only preliminary mitigations are provided.
- The choice of aligning only the last attention layer is not fully justified, and the reason why deeper layers saturate around one-third of model depth is not analyzed.
- Paper omits some technical details needed for reproduction, such as the full pseudocode for segmentation and exact optimization settings for all experiments.

### Questions

- How does MATT compare against Zero-Shot Tokenizer Transfer (Minixhofer et al., 2024) in terms of final performance and total compute, under matched budgets?
- Are the reported performance differences statistically significant across multiple seeds or data samples? What is the run-to-run variance, especially for the smaller Qwen 3 0.6B model?
- What is the isolated contribution of the AIM objective relative to FOCUS initialization alone? A direct FOCUS + no-AIM warm-up vs FOCUS + AIM would clarify this.
- After a fixed continual-pretraining budget, do MATT-initialized models remain better than heuristic-initialized models, or does the advantage diminish?
- How does MATT perform for models with untied embeddings, and can the proposed mitigation be improved to achieve results comparable to tied-embedding settings?
- Can the offset-based segmentation algorithm be described more precisely, and how does it handle languages with complex morphology or no spaces (e.g., Japanese)?
- Why does applying AIM to all layers consistently underperform using only the last layer? Is there a principled criterion for selecting the attention layer depth?
- In Table 1, copying original embeddings of overlapping tokens sometimes hurts heuristic baselines (e.g., WECHSEL, Transtokenizers). Can the authors explain this counter-intuitive result?

### Limitations

- The method requires tied input-output embeddings for full benefit; many modern LLMs use untied embeddings, limiting applicability.
- No continual pretraining experiments are performed, so the ultimate utility of MATT as a warm-up remains unquantified.
- No comparison to recent strong baselines such as Zero-Shot Tokenizer Transfer or standard LM-based embedding tuning.
- Only decoder-only models are tested; encoder-only and encoder-decoder architectures are not covered.
- The absence of variance estimates and multiple seeds limits confidence in the magnitude of reported improvements.
- The paper does not discuss potential negative societal impacts, though none are immediately apparent.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 91,907
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 87,811
- Completion tokens: 19,501
- Reasoning tokens reported: 13,556
- Total tokens: 111,408
- Estimated total: $0.01776529

Full individual reviews and raw JSON responses are in `review_bundle.json`.
