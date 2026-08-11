# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B117.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.022537**

## Final Meta-review

The paper introduces GHOST, a fully automatic pipeline for generating images that induce object hallucination in multimodal large language models (MLLMs). GHOST optimizes a CLIP image embedding to maximize the target MLLM's probability of answering 'Yes' to the presence of an absent object, while applying regularizers to stay close to the original image and avoid encoding the target object. A learned mapper projects the optimized embedding into the MLLM's vision-token space, and Stable Diffusion unCLIP renders natural-looking edited images. Experiments on Qwen2.5-VL, LLaVA-v1.6, and GLM-4.1V-Thinking show high hallucination success rates, cross-model transferability including to GPT-4o, human-verified object absence, and a fine-tuning mitigation study that reduces hallucination.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 2 | 2.600 | 0.490 | 2-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 2 | 2.600 | 0.490 | 2-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 5.800 | 0.400 | 5-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel decoupled optimization framework: optimizing in CLIP embedding space with a learned mapper avoids backpropagation through the diffusion model and MLLM, making the pipeline efficient and generator-agnostic.
- Fully automatic and model-specific: GHOST directly incorporates feedback from the target MLLM, enabling discovery of model-specific and unanticipated hallucination triggers.
- Strong empirical results: high success rates on three open-source MLLMs and transferability to closed models like GPT-4o at 66.5%.
- Multi-faceted evaluation: includes OWLv2 object-absence filtering, human evaluation, ablations, and class-wise breakdowns, strengthening the claim that generated images are natural and object-free.
- Demonstrates practical value beyond diagnosis: fine-tuning on GHOST images reduces hallucination on transferred attacks and improves POPE scores, suggesting use as a robustness-improvement tool.

### Weaknesses

- The comparison with DASH is not apples-to-apples: DASH is designed for web-scale retrieval over ReLAION-5B, not for per-image maximization on a curated COCO pool; reporting raw counts/success rates unfairly favors GHOST, and the 'orders of magnitude' claim is unsubstantiated.
- The success-rate definition is ambiguous: it likely reflects per-initial-image rather than per-generated-attempt; images that fail during generation or are filtered are excluded, so the per-generated-image success may be lower.
- The mapper is a lossy projection (GPT-judge relative scores as low as 54.5% for LLaVA), and the paper does not analyze how mapper inaccuracies affect optimization reliability or how out-of-distribution optimized embeddings behave.
- Object absence is verified primarily by OWLv2, which may have false negatives, and human raters still report seeing the target object in 11-14% of images, so the method does not guarantee truly object-free outputs.
- FID is used as a 'semantic fidelity' metric, but FID is a distribution-level measure and does not capture per-image preservation; paired perceptual metrics like LPIPS or SSIM would be more appropriate.
- The fine-tuning mitigation is a small proof-of-concept (one model, LoRA, limited classes) and does not demonstrate scaling, statistical significance, or robustness across diverse tasks.

### Questions

- What exactly is the denominator for the reported success rates—initial input images, generated images, or successful after filtering? Please report success per generated image.
- What is the end-to-end computational cost (GPU-hours per successful image) compared to DASH, and is the method feasible for large-scale stress-testing?
- How does the mapper's approximation error propagate to optimization quality, and how often do optimized embeddings fall outside the mapper's training distribution?
- What is the recall/false-negative rate of OWLv2 on the 10 target classes, and how does human evaluation compare with OWLv2 on the same GHOST samples?
- Could GHOST work without CLIP-based sorting? The appendix suggests it can, but with different hyperparameters; is there a principled way to choose these hyperparameters?
- For transferability experiments on closed models, were evaluations done through official APIs with consistent prompts and decoding settings, and how many samples were used?

### Limitations

- Evaluated on only 10 COCO object classes and three main MLLMs; generalization to rare, abstract, or context-dependent objects and other model families is unknown.
- Requires training a mapper for each target MLLM, relying on access to the model's vision encoder and paired CLIP-MLLM embeddings; this may be impractical for proprietary or fully black-box models.
- Object absence verification is imperfect (OWLv2 false negatives and human 'Yes' responses in 11-14% of images), so some successful samples may contain ambiguous or partial target-object cues.
- The optimization-to-diffusion pipeline has a moderate success rate (~28-40%), meaning many optimization attempts fail, possibly requiring high computational cost to collect sufficient samples.
- Dual-use potential: GHOST-generated images could be used to maliciously induce hallucinations in deployed MLLMs, though the paper also proposes defensive fine-tuning; no responsible disclosure or safeguards are discussed.
- The fine-tuning mitigation is a toy demonstration and does not provide evidence of scalability, stability across models, or long-term effects on general capabilities.

### Ethics

Ethical concerns flagged: **True**

## Usage and Cost

- Requests: 6
- Prompt tokens: 111,248
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 107,152
- Completion tokens: 26,872
- Reasoning tokens reported: 20,246
- Total tokens: 138,120
- Estimated total: $0.02253691

Full individual reviews and raw JSON responses are in `review_bundle.json`.
