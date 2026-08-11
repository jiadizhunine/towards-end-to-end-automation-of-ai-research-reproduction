# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B117.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.020007**

## Final Meta-review

The paper introduces GHOST (Generating Hallucinations via Optimizing Stealth Tokens), a method for actively generating images that induce object hallucinations in Multimodal Large Language Models (MLLMs). GHOST optimizes CLIP image embeddings to mislead target MLLMs while regularizing against encoding the target object, then uses Stable Diffusion unCLIP conditioned on the optimized embedding to generate natural-looking images. A learned mapper network bridges the CLIP embedding space and the MLLM's vision encoder space, enabling efficient optimization without backpropagating through the full pipeline. The method achieves hallucination success rates of 28-32% across multiple MLLMs (Qwen2.5-VL, LLaVA-v1.6, GLM-4.1V-Thinking), significantly outperforming prior work DASH (0.1%). The paper demonstrates strong cross-model transferability (up to 66.5% on GPT-4o), verifies image quality through FID/SSIM and human evaluation, and shows that fine-tuning on GHOST images can mitigate hallucination while preserving general capabilities. The work positions GHOST as both a diagnostic and corrective tool for building more reliable multimodal systems.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 4.000 | 0.000 | 4-4 |
| Quality | 3 | 3.400 | 0.490 | 3-4 |
| Clarity | 4 | 3.600 | 0.490 | 3-4 |
| Significance | 4 | 3.800 | 0.400 | 3-4 |
| Soundness | 3 | 3.400 | 0.490 | 3-4 |
| Presentation | 4 | 3.600 | 0.490 | 3-4 |
| Contribution | 4 | 3.600 | 0.490 | 3-4 |
| Overall | 7 | 6.800 | 0.748 | 6-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel and efficient decoupled optimization approach using a learned mapper between CLIP and MLLM embedding spaces, avoiding expensive end-to-end backpropagation
- Strong empirical results with hallucination success rates of 28-32%, orders of magnitude higher than prior work DASH
- Comprehensive evaluation across multiple open-source and closed-source models, including reasoning models, with transferability analysis
- Dual utility demonstrated as both a diagnostic and corrective tool via fine-tuning experiments
- Thorough ablation studies on key hyperparameters and extensions to attribute/relation hallucinations
- Well-written and well-organized paper with detailed appendices supporting reproducibility

### Weaknesses

- The comparison with DASH may be unfair, as DASH was designed for web-scale dataset search (ReLAION-5B) rather than maximizing hallucination count on COCO
- Mapper quality concerns: GPT-4-based evaluation shows relatively low relative scores (54.5-76%), suggesting potential semantic information loss that could affect attack effectiveness
- Limited analysis of failure cases and the types of misleading cues that trigger hallucinations
- Fine-tuning mitigation experiments are small-scale proof-of-concept with limited generalizability claims
- Human evaluation uses a limited pool of 'peers' rather than trained annotators, which may introduce bias
- Hyperparameter choices appear somewhat model-specific, potentially limiting generalizability to new MLLMs

### Questions

- How does the mapper reconstruction quality impact the final attack success rate? Would improving the mapper lead to higher hallucination success rates?
- Why was COCO chosen for the DASH comparison when DASH was designed for web-scale datasets? How would results compare on ReLAION-5B?
- Could the success of GHOST be partly attributed to distribution shift from the diffusion model rather than the specific optimization targeting hallucination? What control experiments were done to isolate this?
- How sensitive is GHOST to the choice of diffusion model? Would other embedding-conditioned generative models work equally well?
- What characterizes the images that fail to induce hallucination? Is there a pattern in terms of content, object category, or optimization trajectory?
- For the fine-tuning mitigation, how much of the improvement is due to hallucination-inducing images versus synthetic images in general?
- How does the CLIP-sorting of initial images affect the reported success rates? Would random sampling produce different results?
- What is the false positive rate of OWLv2 in detecting target objects, and how does detector performance affect reported success rates?

### Limitations

- Reliance on diffusion models supporting embedding-level conditioning (unCLIP), limiting applicability to other diffusion architectures
- Primary focus on object-centric hallucinations, with attribute/relation hallucinations only preliminarily explored
- Computational cost remains significant (~10 seconds per sample), limiting scalability to very large datasets
- The method requires access to the target MLLM's internal representations, which may not be available for closed-source models
- Potential for misuse in generating misleading content that exploits MLLM vulnerabilities, though the diagnostic and corrective framing partially mitigates this
- Evaluation primarily on COCO and ObjectNet; broader dataset coverage would strengthen generalizability claims

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 131,278
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 122,318
- Completion tokens: 10,205
- Reasoning tokens reported: 0
- Total tokens: 141,483
- Estimated total: $0.02000701

Full individual reviews and raw JSON responses are in `review_bundle.json`.
