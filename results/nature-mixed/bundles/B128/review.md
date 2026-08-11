# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B128.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.052951**

## Final Meta-review

The paper introduces HydraFake, a new large-scale benchmark dataset for deepfake detection that simulates real-world challenges through a hierarchical evaluation protocol (In-Domain, Cross-Model, Cross-Forgery, Cross-Domain). It also proposes VERITAS, an MLLM-based deepfake detector that uses pattern-aware reasoning (fast judgment, planning, reasoning, self-reflection, conclusion) to improve generalization and transparency. The training pipeline consists of two stages: (1) pattern-guided cold-start with SFT and a novel Mixed Preference Optimization (MiPO) to align reasoning, and (2) Pattern-Aware GRPO (P-GRPO) with a pattern-aware reward to incentivize adaptive planning and self-reflection. Experiments on HydraFake show that VERITAS significantly outperforms existing detectors, especially on unseen forgeries and data domains, while providing transparent and faithful detection outputs.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 4.000 | 0.000 | 4-4 |
| Quality | 3 | 3.200 | 0.400 | 3-4 |
| Clarity | 3 | 3.400 | 0.490 | 3-4 |
| Significance | 4 | 4.000 | 0.000 | 4-4 |
| Soundness | 3 | 3.400 | 0.490 | 3-4 |
| Presentation | 3 | 3.400 | 0.490 | 3-4 |
| Contribution | 4 | 4.000 | 0.000 | 4-4 |
| Overall | 7 | 7.400 | 0.490 | 7-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The HydraFake dataset is a comprehensive and timely contribution that addresses the gap between academic benchmarks and industrial practice, with a well-designed hierarchical evaluation protocol covering unseen models, forgeries, and domains.
- VERITAS is a novel method that applies human-like reasoning patterns (planning, self-reflection) to deepfake detection via MLLMs, which is a promising direction with clear empirical gains.
- The two-stage training pipeline is well-motivated, with MiPO addressing memorization issues and P-GRPO incentivizing adaptive reasoning.
- Extensive and well-designed experiments: comparisons with 10+ SOTA detectors, multiple MLLMs, and MLLM-based forgery detectors; comprehensive ablations on training stages, reasoning patterns, reward functions, and base models; robustness and cross-benchmark evaluations.
- The paper provides detailed appendices with dataset construction details, annotation pipeline, prompts, and qualitative examples, enhancing reproducibility.
- The paper is well-contextualized within the existing literature and clearly identifies the limitations of current approaches.

### Weaknesses

- The design of the five reasoning patterns (fast, planning, reasoning, reflection, conclusion) appears somewhat ad-hoc and lacks a principled justification beyond empirical gains.
- The P-GRPO reward function is hand-crafted with arbitrary weights and relies on an external MLLM for reflection quality evaluation; sensitivity analysis is limited.
- Reasoning quality is evaluated primarily via MLLM-as-a-Judge (GPT-4o, Gemini-2.5-Pro), which can be biased; no detailed human evaluation of the final model's reasoning quality is provided.
- The training pipeline is complex and computationally intensive, requiring multiple stages and large MLLMs, which may be a barrier for wider adoption and reproducibility.
- The model's performance on low-resolution images (e.g., DeepFaceLab, FFIW) remains weak, which is a practical limitation in real-world scenarios.
- The comparison with other MLLM-based detectors is somewhat limited by differences in training data and objectives, although the VERITAS-MINI variant partially addresses this.
- The reliance on automated MLLM annotation for SFT data may introduce biases or errors that are not fully analyzed.

### Questions

- Can you provide a more principled justification for the specific five reasoning patterns? Did you experiment with other pattern structures (e.g., only planning, only reflection) and find these to be optimal?
- How sensitive is the final performance to the exact reward weights in P-GRPO (e.g., 2.0 vs 1.5 for correct+planning)? Have you performed a detailed sensitivity analysis?
- Could you provide more details on the human evaluation of reasoning quality? How many human annotators were used, and what was the inter-annotator agreement?
- For the VERITAS-MINI comparison, how does its performance change when trained on the full HydraFake training set? Is the gap between VERITAS and VERITAS-MINI mainly due to data scale?
- Considering the high computational cost, can you comment on the practical feasibility of deploying VERITAS in real-time deepfake detection systems? Are there any plans to distill the reasoning capabilities into smaller models?
- In the failure cases (e.g., IC-Light), the model identifies suspicious clues but still gives the wrong answer. How could the reasoning process be improved to better weigh these clues?
- How do you ensure the quality and reliability of the automatically generated SFT annotations, given the reliance on MLLMs? What was the human verification process?
- In the Cross-Domain split, real images come from unseen datasets. How do you ensure that the model's performance is not confounded by the resolution or quality of these real images?

### Limitations

- The dataset is limited to image modality; video-based deepfakes are not covered, which is a growing concern given the rise of video generation models.
- The model struggles with low-resolution images, which are common in real-world scenarios (e.g., social media).
- The training pipeline is computationally intensive and may not be accessible to all researchers.
- The reliance on MLLMs for data annotation and reward modeling could introduce systematic biases that are not fully addressed.
- The reasoning process can be verbose and sometimes hallucinate artifacts, which may not always be faithful to the actual image content.
- The potential negative societal impact is not deeply discussed, such as the dual-use nature of the dataset or the possibility of using the reasoning traces to improve deepfake generation.
- The paper focuses primarily on facial deepfakes, and the generalization to other types of AI-generated content is not fully explored.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 367,021
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 358,061
- Completion tokens: 9,991
- Reasoning tokens reported: 0
- Total tokens: 377,012
- Estimated total: $0.05295111

Full individual reviews and raw JSON responses are in `review_bundle.json`.
