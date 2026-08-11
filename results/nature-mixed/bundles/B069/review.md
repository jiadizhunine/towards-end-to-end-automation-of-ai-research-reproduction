# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B069.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.013624**

## Final Meta-review

The paper introduces CHROMA, a feed-forward transformer-based framework for multi-view appearance harmonization in 3D reconstruction. The method predicts per-frame 3D bilateral grids that transform input images to match a selected reference frame's appearance, correcting photometric inconsistencies such as exposure, white balance, and color shifts. Key contributions include: (1) a multi-view aware transformer with alternating self and cross-attention for consistent bilateral grid prediction, (2) a reference frame selection mechanism combining photometric quality (LAB-based) and semantic representativeness (DINOv2), (3) a hybrid training strategy using synthetic paired data from DL3DV with simulated ISP variations and a self-supervised rendering loss via 3D foundation models (AnySplat) on unpaired real-world data, and (4) uncertainty-aware confidence grid prediction. The method is designed to integrate seamlessly with existing 3D reconstruction pipelines (3DGS, 2DGS, DashGS) without scene-specific optimization. Experiments on three datasets (DL3DV with ISP variations, MipNeRF360-VE with exposure changes, and BilaRF with real-world captures) demonstrate that CHROMA matches or outperforms per-scene appearance embedding methods while being significantly more efficient.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.800 | 0.400 | 3-4 |
| Quality | 3 | 3.200 | 0.400 | 3-4 |
| Clarity | 3 | 3.400 | 0.490 | 3-4 |
| Significance | 4 | 3.600 | 0.490 | 3-4 |
| Soundness | 3 | 3.200 | 0.400 | 3-4 |
| Presentation | 3 | 3.400 | 0.490 | 3-4 |
| Contribution | 4 | 3.600 | 0.490 | 3-4 |
| Overall | 7 | 7.200 | 0.400 | 7-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel decoupling of appearance harmonization from scene-specific 3D reconstruction optimization, enabling feed-forward processing without per-scene retraining and providing significant computational efficiency gains.
- Well-designed transformer architecture with alternating frame-wise and global/cross-attention that balances cross-view consistency with memory efficiency.
- Comprehensive training strategy combining supervised learning on synthetic paired data with self-supervised learning via 3D foundation models, effectively addressing the lack of paired real-world data.
- Strong experimental validation across three diverse datasets with different types of appearance variations (ISP, exposure, real-world), demonstrating consistent improvements over baselines.
- Integration with multiple 3D reconstruction backbones (3DGS, 2DGS, DashGS) shows generalizability and practical utility.
- Thoughtful reference frame selection mechanism that considers both semantic representativeness and photometric quality.
- Uncertainty-aware confidence grid prediction improves robustness in challenging regions.
- Clear and well-organized presentation with good figures illustrating the architecture and results.

### Weaknesses

- The model has 137.84M parameters, which is substantial for a preprocessing module and may limit deployment in resource-constrained settings.
- Limited analysis of failure cases, particularly for scenes with severe appearance variations, specular highlights, reflections, or dynamic content.
- The self-supervised loss depends on the quality of AnySplat, and the sensitivity to the choice of 3D foundation model is not analyzed.
- Reference frame selection uses fixed hyperparameters (α=0.5, λ values) without sensitivity analysis or adaptive weighting.
- Scalability for very large frame counts (300+ frames) is claimed but memory requirements and practical limits are not thoroughly analyzed.
- No statistical significance analysis (error bars or significance tests) is provided for the reported experimental improvements.
- Comparison with 2D harmonization baselines is limited to exposure variations, not full ISP variations with color shifts.
- Ablations do not explore sensitivity to bilateral grid resolution, guidance dimension, or number of transformer layers.

### Questions

- How does the method scale with the number of input frames? What is the memory footprint when processing 300+ frames in a single forward pass, and are there approximations or strategies for handling very large captures?
- How sensitive is the reference frame selection to the hyperparameters α, λent, λov, and λun? Have you explored adaptive or learned weighting schemes?
- How robust is the self-supervised loss to the quality of AnySplat predictions? Would alternative feed-forward models (e.g., VGGT, MapAnything) work equally well, and are there known failure cases of AnySplat that affect training?
- Can you provide statistical significance analysis (e.g., confidence intervals or paired tests) for the reported improvements?
- How does the method handle scenes with dynamic objects or transient elements, given the static scene assumption?
- What happens when the reference frame selection fails (e.g., all frames are poorly exposed)? Is there a fallback mechanism?
- Could you provide a breakdown of the computational cost between attention computation, grid slicing, and reference frame selection? Is the harmonization real-time capable?
- How does the method handle extreme appearance variations (e.g., complete darkness or overexposure where information is irrecoverably lost)?
- For the BilaRF dataset with flash illumination, are there visible artifacts in specular regions due to the smooth bilateral grid representation?
- What is the training data composition between DL3DV and WildRGB-D? What is the ratio of paired to unpaired data?

### Limitations

- The method requires training a dedicated harmonization network, which adds an upfront cost and may be prohibitive for one-off scene reconstructions.
- Bilateral grid transformations are inherently smooth and cannot model high-frequency photometric changes such as specular highlights, reflections, or strong view-dependent effects.
- The approach assumes static scenes and does not handle transient objects or dynamic content.
- The reference frame selection is heuristic and may fail in scenarios where no single frame is representative of the scene appearance.
- The self-supervised training relies on a pretrained 3D foundation model (AnySplat), which may not be available or optimal for all use cases.
- Evaluation is limited to datasets with specific characteristics; generalization to truly unconstrained photo collections (e.g., PhotoTourism-style) or extreme lighting conditions is not demonstrated.
- Potential negative societal impact: The appearance harmonization could be misused to manipulate or fabricate visual evidence in photo collections, though this is a general concern for any image editing method.
- The computational cost of training a 137M parameter transformer may limit accessibility for researchers with limited resources.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 86,627
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 77,667
- Completion tokens: 9,735
- Reasoning tokens reported: 0
- Total tokens: 96,362
- Estimated total: $0.01362427

Full individual reviews and raw JSON responses are in `review_bundle.json`.
