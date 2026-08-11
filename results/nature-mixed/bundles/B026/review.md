# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B026.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.022747**

## Final Meta-review

This paper introduces NEO, a family of native (monolithic, encoder-free) vision-language models designed to compete with modular VLMs. The key contributions are: (1) Native-RoPE, a rotary position embedding that decouples height, width, and temporal dimensions with separate base frequencies and head channels; (2) Multi-Head Native Attention (MHNA) with mixed masking (bidirectional for image tokens, causal for text tokens); and (3) a pre-Buffer/post-LLM training paradigm where a randomly initialized pre-Buffer learns visual encoding while the pretrained LLM is partially frozen, with the partition dissolving in later training stages. The models are trained on ~345-390M image-text pairs across three stages (pre-training, mid-training, SFT). Experiments at 2B and 9B scales show NEO substantially outperforms prior native VLMs and approaches the performance of modular VLMs on several benchmarks. Extensive ablations isolate the contributions of the proposed components, and the pre-Buffer is demonstrated to be reusable as a standalone visual encoder.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.600 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.200 | 0.400 | 3-4 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.200 | 0.400 | 3-4 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 7 | 6.600 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Well-motivated architectural innovations: Native-RoPE with fully decoupled T/H/W dimensions and additional Q/K head channels is a principled solution to the frequency mismatch between pretrained LLMs and visual inputs.
- The pre-Buffer/post-LLM training strategy is novel and practical, enabling visual learning from scratch while preserving linguistic knowledge, and is shown to be reusable across different post-LLM backbones.
- Comprehensive empirical evaluation across multiple benchmarks at two model scales, with thorough ablation studies that isolate the contribution of each design choice.
- Controlled comparisons (e.g., against EVE variants under identical conditions) strengthen the claim that gains come from architectural choices rather than data or backbone differences.
- Strong performance against existing native VLMs, significantly narrowing the gap with modular counterparts despite using less training data.
- Clear writing and commitment to releasing code and models for reproducibility.

### Weaknesses

- Performance gaps remain significant on knowledge-heavy (MMMU) and OCR-heavy (TextVQA, InfoVQA) benchmarks compared to top modular VLMs, limiting the strength of the 'narrowing the gap' claim.
- Inconsistent scaling behavior: NEO-9B underperforms NEO-2B on DocVQA and InfoVQA, raising concerns about reliable scaling or data quality issues that are not deeply investigated.
- Comparison with modular VLMs uses somewhat dated baselines (e.g., Qwen2-VL, InternVL2.5); newer models like Qwen3-VL or InternVL3.5 are not included.
- Evaluation is limited to image understanding; claims of extensibility to video, generation, and embodied AI are not backed by any experiments.
- Training data composition is not fully specified (exact mix, filtering, language distribution), limiting reproducibility.
- The additional ~10% parameters from extra Q/K heads are mentioned but computational overhead, inference efficiency, and memory implications are not analyzed.
- The reusable pre-Buffer is only demonstrated under limited training conditions; its scalability and cross-backbone transferability are not thoroughly explored.
- The paper overstates 'first principles' and 'cornerstone' positioning given that contributions are incremental refinements of existing techniques (e.g., M-RoPE, Video-RoPE).

### Questions

- How does NEO perform when using the same base LLM (e.g., Qwen2.5-7B) as comparison methods like EVEv2 or VoRA, to better isolate architectural contributions?
- What is the total computational cost (GPU-hours, FLOPs) of the full three-stage training pipeline, and how does it compare to training a modular VLM of similar scale?
- Can the pre-Buffer be transferred to different post-LLM backbones (e.g., Llama, InternLM)? Have the authors tested cross-backbone transferability?
- Why does NEO-9B underperform NEO-2B on DocVQA and InfoVQA? Is this a data distribution issue, optimization challenge, or scaling limitation?
- The paper claims video support through temporal indexing. Are there any preliminary results or plans to evaluate NEO on video benchmarks?
- How was the 3:7 text-to-multimodal data ratio determined? Was it tuned, and what is its impact on performance?
- What is the training trajectory of the zero-initialized K weights for H/W dimensions? Do they converge to patterns resembling visual encoder weights?
- How does the optimal pre-Buffer depth (L1) scale with model size? The ablation shows saturation at 8 layers for the 1.7B model, but would this hold for the 9B model?

### Limitations

- Training data scale and quality are limited compared to state-of-the-art modular VLMs, particularly for knowledge-intensive and OCR tasks, and the paper does not provide a clear roadmap for addressing these gaps.
- The evaluation focuses on image-text understanding; no video, generation, or multimodal reasoning beyond standard benchmarks is shown, despite architectural claims of extensibility.
- The reusable pre-Buffer concept is demonstrated in only one configuration; its generalizability to different LLM families and larger training budgets is speculative.
- No analysis of robustness, fairness, safety, or bias is provided beyond a brief generic societal impact statement.
- The paper does not report the environmental cost or carbon footprint of training the models.
- The computational cost of the additional Q/K head dimensions is not analyzed in terms of inference speed or memory usage.
- Some comparisons with modular VLMs may be unfair due to differences in training data scale and quality, though the controlled EVE comparison partially mitigates this.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 148,263
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 139,303
- Completion tokens: 11,498
- Reasoning tokens reported: 0
- Total tokens: 159,761
- Estimated total: $0.02274695

Full individual reviews and raw JSON responses are in `review_bundle.json`.
