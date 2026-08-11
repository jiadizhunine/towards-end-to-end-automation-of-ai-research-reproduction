# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B114.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.017890**

## Final Meta-review

Omni-View is a unified multimodal model for 3D scene understanding and generation from multiview images. The core contribution is extending the 'generation facilitates understanding' paradigm to 3D by decomposing the generation model into a texture module (novel view synthesis) and a geometry module (depth and camera pose estimation), both interacting with the understanding model during training. A two-stage training strategy is proposed: Stage 1 jointly trains understanding and generation with a dense-to-sparse (D2S) curriculum for reference images to improve 3D understanding; Stage 2 freezes the understanding model and fine-tunes generation modules for better 3D scene generation. The model achieves state-of-the-art performance on VSI-Bench (55.4), strong results on SQA3D and ScanQA, and competitive novel view synthesis quality, with extensive ablations validating each design choice.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 2.800 | 0.400 | 2-3 |
| Significance | 3 | 3.400 | 0.490 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 2.800 | 0.400 | 2-3 |
| Contribution | 3 | 3.200 | 0.400 | 3-4 |
| Overall | 6 | 6.400 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel and well-motivated exploration of the 'generation facilitates understanding' paradigm specifically for 3D scenes, which is underexplored compared to 2D unified models
- Clean architectural design that decomposes generation into separate texture and geometry modules, allowing specialized spatiotemporal and geometric modeling with clear connections to the understanding model
- Comprehensive evaluation across multiple tasks (3D QA, spatial reasoning, localization, NVS, scene generation) with multiple benchmarks, demonstrating versatility and strong results on VSI-Bench
- Thorough ablation studies that isolate the contributions of the texture module, geometry module, autoregressive generation, D2S curriculum, and stage 2 training
- Two-stage training strategy with a dense-to-sparse curriculum is an interesting and effective approach for progressively teaching the model to handle sparse views
- Open-source code and models for reproducibility, with honest discussion of limitations including grounding gaps and outdoor scene failures

### Weaknesses

- The mechanism by which generation improves understanding is not deeply analyzed; the activation visualization is suggestive but not conclusive, and the paper lacks probing or intervention experiments to explain the transfer
- The geometry module relies on synthetic depth maps from the Voyager pipeline, which may limit the accuracy and generalizability of geometric understanding
- Generation performance improvements over specialized baselines are modest (e.g., PSNR gains of ~0.1-0.2), raising questions about the practical significance of the generation capabilities
- The paper does not compare with the most recent unified 3D understanding and generation models (e.g., Hermes is mentioned but not compared), and the related work section could be more comprehensive
- Several technical details are unclear, including the cross-attention mechanism between the understanding model and geometry module, the exact D2S schedule, and the selection of the final checkpoint given camera pose loss instability
- The 'generation in grid' approach presented in the appendix appears to be a significant improvement but is not integrated into the main results, creating ambiguity about its status
- The paper contains numerous typos and formatting errors (e.g., 'understandimg', 'optimizion') that detract from professionalism
- The comparison with 3D-input methods is somewhat unfair since those methods have access to richer geometric information, and the grounding gap remains significant (e.g., ScanRefer 50.8 vs 62.6)

### Questions

- Can you provide more rigorous analysis of why generation helps understanding? Have you considered probing internal representations, conducting intervention experiments, or ablating with a simpler reconstruction-only objective (e.g., masked image modeling) to isolate the effect of autoregressive generation?
- How sensitive are the understanding improvements to the quality of the synthetic depth maps from Voyager? Have you experimented with ground-truth depths (e.g., from ScanNet) for geometry training?
- What is the exact schedule for the dense-to-sparse (D2S) curriculum? How many iterations are spent at each density level, and was the schedule optimized?
- Why is the 'generation in grid' approach only used in Stage 2 and not in the main NVS experiments? Would it affect understanding performance if used in Stage 1?
- How does the model perform with varying numbers of input views (e.g., 4, 8, 16 vs 32)? Is there a minimum number of views required for the generation modules to provide meaningful benefits?
- The camera pose loss shows spikes during training. How were these handled, and how was the final checkpoint selected? Is the model sensitive to random seed or training order?
- What is the computational overhead of running both texture and geometry modules during inference for understanding tasks?
- Have you compared with Hermes or other unified 3D understanding and generation models? The paper mentions Hermes but does not include it in comparisons.

### Limitations

- The paper acknowledges limitations in 3D grounding compared to methods with explicit 3D input, limiting applicability to precise spatial localization tasks
- The reliance on synthetic depth maps from the Voyager pipeline may not generalize well to real-world scenes with different depth distributions
- The generation model lacks long-range world generation capability and struggles with large camera movements in outdoor scenes, as shown in the failure case
- The mechanism for how generation improves understanding is not fully explained, and the paper would benefit from more detailed analysis (e.g., probing experiments, attention analysis)
- The computational cost of training (32 H100 GPUs for ~200 hours) is substantial and not discussed in terms of accessibility or environmental impact
- The evaluation focuses primarily on indoor scenes; generalization to diverse scene types beyond the training distribution is not thoroughly evaluated
- Potential negative societal impact of 3D scene generation (e.g., deceptive scene fabrication) is mentioned but could be expanded with more concrete examples and mitigation strategies
- The paper does not discuss potential biases in the training data (e.g., scene types, object categories) that could affect real-world deployment

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 113,782
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 104,822
- Completion tokens: 11,394
- Reasoning tokens reported: 0
- Total tokens: 125,176
- Estimated total: $0.01789049

Full individual reviews and raw JSON responses are in `review_bundle.json`.
