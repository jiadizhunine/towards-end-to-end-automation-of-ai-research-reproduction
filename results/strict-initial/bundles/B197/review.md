# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B197.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.018543**

## Final Meta-review

The paper proposes LazyDrag, a training-free drag-based image editing method for Multi-Modal Diffusion Transformers (MM-DiTs). It replaces implicit attention-based point matching with an explicit correspondence map derived from user drags, enabling full-strength inversion without test-time optimization. The method uses winner-takes-all displacement fusion, Gaussian-noise latent initialization for inpainting regions, and attention controls (background token replacement, identity-preserving token concatenation, gated output merging). Experiments on DragBench show improvements in MD, VIEScore metrics, and human preference over existing drag-editing baselines, with ablations validating each component.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 2.800 | 0.400 | 2-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.000 | 1.095 | 4-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The core idea of replacing fragile implicit attention-based point matching with an explicit correspondence map derived from drag instructions is novel, well-motivated, and directly addresses a known instability of prior drag-based methods.
- LazyDrag is the first drag-based editing method designed for MM-DiTs and demonstrates full-strength inversion without test-time optimization, making it more practical for interactive editing.
- The technical design is thorough: WTA displacement fusion handles opposing drags, Gaussian-noise latent initialization improves inpainting of uncovered regions, and attention controls preserve background and identity while enabling text-guided semantic changes.
- Comprehensive experiments on DragBench show consistent improvements over eight baselines in MD, SC, PQ, O, and human preference, with ablations supporting the contribution of each proposed component.
- The method is training-free and TTO-free, and the ablation study includes a transfer of one component to a U-Net baseline, demonstrating some generality.

### Weaknesses

- The quantitative comparison is confounded by the base model: LazyDrag uses the strong FLUX.1 Krea-dev MM-DiT, while all baselines are U-Net-based Stable Diffusion models, so reported improvements may largely reflect the base model rather than the proposed editing mechanism; no same-backbone comparison is provided.
- The drag accuracy improvement over DragText is marginal (MD 21.49 vs 21.51, a difference of 0.02), and no statistical significance tests are provided; the claim of state-of-the-art drag accuracy is not strongly substantiated.
- Evaluation relies on GPT-4o-based VIEScore and omits standard fidelity metrics such as LPIPS/IF; the user study is limited (20 participants, 32 cases) and lacks significance testing.
- The method's dependence on the specific FLUX.1 Krea-dev model and UniEdit-Flow inversion raises concerns about generalizability to other MM-DiTs or inversion methods; no experiments on other MM-DiTs are provided.
- Despite emphasizing the TTO-free advantage, no runtime, wall-clock, or GPU memory comparisons are reported, so the efficiency benefit is not quantified.
- Some design choices (e.g., transition-region definition, activation timestep schedule, blending schedule h_t) appear ad-hoc and are not rigorously justified; the reported failure cases (overlapping targets, very small drag distances) are only placed in the appendix.

### Questions

- Can the authors provide a controlled comparison with all methods using the same base model (e.g., FLUX.1 Krea-dev or SDXL) to isolate the effect of the proposed attention controls from the backbone choice?
- Is the 0.02 MD improvement over DragText statistically significant, and what is the per-image distribution of MD across DragBench?
- What are the wall-clock inference times and GPU memory requirements of LazyDrag compared to TTO-free and TTO-based baselines?
- How is 'full-strength inversion' defined operationally, and how does it compare to the inversion strengths used by prior methods? Could a weakened-inversion variant of LazyDrag be tested to substantiate the claim?
- Why are standard fidelity metrics like LPIPS/IF omitted? Can these be reported as a sanity check, even if not the main metric?
- How sensitive are the results to the choice of inversion method (UniEdit-Flow vs. others) and to the density/placement of sampled feature points P?

### Limitations

- The evaluation does not control for base-model strength, making it difficult to attribute the performance gains solely to the proposed method.
- The method inherits limitations of the underlying VAE/latent patching, struggling with very small drag distances; overlapping target points can cause artifacts depending on the activation timestep.
- Generalization to other MM-DiT architectures, datasets beyond DragBench, or video editing is not demonstrated.
- The reliance on a proprietary base model (FLUX.1 Krea-dev) and inversion method may hinder reproducibility if no code is released.
- Potential negative societal impacts of more capable drag-based editing (e.g., creation of misleading photorealistic images) are not discussed or mitigated.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 88,426
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 84,330
- Completion tokens: 24,020
- Reasoning tokens reported: 17,734
- Total tokens: 112,446
- Estimated total: $0.01854327

Full individual reviews and raw JSON responses are in `review_bundle.json`.
