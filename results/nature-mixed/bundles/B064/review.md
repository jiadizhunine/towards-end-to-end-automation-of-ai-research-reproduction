# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B064.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.018253**

## Final Meta-review

StreamSplat is a fully feed-forward framework for online dynamic 3D reconstruction from uncalibrated video streams. The method predicts dynamic 3D Gaussian Splatting (3DGS) representations in near real-time without requiring camera calibration or full-sequence access. Three key innovations are proposed: (1) a probabilistic position sampling mechanism that robustly predicts 3D Gaussians from uncalibrated inputs, (2) a bidirectional deformation field that provides reliable cross-frame associations and mitigates long-term error accumulation, and (3) an adaptive Gaussian fusion operation that propagates persistent Gaussians while handling emerging and vanishing ones. The method is evaluated on both dynamic (DAVIS, YouTube-VOS) and static (CO3Dv2, RE10K) benchmarks, demonstrating state-of-the-art reconstruction quality with a 1200× speedup over optimization-based methods. The framework uniquely supports online reconstruction of arbitrarily long video streams.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.800 | 0.400 | 3-4 |
| Quality | 4 | 3.800 | 0.400 | 3-4 |
| Clarity | 4 | 3.600 | 0.490 | 3-4 |
| Significance | 4 | 3.600 | 0.490 | 3-4 |
| Soundness | 4 | 3.800 | 0.400 | 3-4 |
| Presentation | 4 | 3.600 | 0.490 | 3-4 |
| Contribution | 4 | 3.600 | 0.490 | 3-4 |
| Overall | 7 | 7.400 | 0.800 | 6-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important and practical problem: online dynamic 3D reconstruction from uncalibrated video streams, with clear applications in robotics, AR/VR, and autonomous driving.
- Novel combination of probabilistic position sampling, bidirectional deformation, and adaptive Gaussian fusion, each well-motivated and validated via ablation studies.
- Comprehensive evaluation across multiple benchmarks including dynamic (DAVIS, YouTube-VOS) and static (CO3Dv2, RE10K) scenes, plus zero-shot evaluation on DyCheck and NVIDIA Dynamic Scenes.
- Strong quantitative results, particularly for dynamic scene reconstruction and frame interpolation, with a 1200× speedup over optimization-based methods enabling near real-time operation.
- Well-written with clear figures and algorithm descriptions, making the method reproducible.
- The online inference capability is a unique contribution compared to existing offline methods, and the adaptive Gaussian fusion elegantly handles topological changes without explicit matching.

### Weaknesses

- Novel view synthesis performance on static benchmarks (RE10K, CO3Dv2) is weaker than static-specific methods, though this is acknowledged and attributed to the lack of camera pose input.
- The orthographic projection assumption may limit performance on close-range scenes with strong perspective effects or significant camera rotation/zoom.
- Reliance on external pseudo-depth estimator (DepthAnythingv2) introduces potential noise and limits end-to-end training and generalization.
- Bidirectional deformation field is trained over a two-frame window, potentially limiting long-range temporal coherence in fast-motion or extended-occlusion scenarios.
- Limited analysis of failure cases, particularly for extreme motion, complex multi-object dynamics, or very long sequences.
- Missing direct comparisons with some recent feed-forward dynamic methods (e.g., Liang et al., 2024; Yang et al., 2024a), and the comparison with MonST3R is limited by methodological differences.

### Questions

- How does the method handle scenes with very large motion between consecutive frames where the velocity bound of [-1,1]^3 might be exceeded? Are there failure cases with extreme motion or camera cuts?
- What is the memory footprint of the maintained Gaussian set over long sequences (e.g., hours of video)? Is there a risk of unbounded growth or accumulation of redundant Gaussians?
- How sensitive is the method to the quality of the pseudo-depth estimator? Have the authors tested with different depth estimators (e.g., Depth Anything V1 vs V2)?
- How critical is the mask supervision from DAVIS/YouTube-VOS for dynamic scene modeling? Does the method degrade significantly without it?
- How does the method perform on videos with varying frame rates? Is there a need to adapt the deformation field to different temporal scales?
- What happens when there is significant camera motion along the optical axis (zoom) or strong perspective effects? Does the orthographic assumption cause noticeable artifacts?
- Could you provide more detailed comparisons with recent feed-forward dynamic methods like Feed-forward Bullet-time (Liang et al., 2024) or STORM (Yang et al., 2024a)?
- How does the method handle scenes with multiple independently moving objects? Are there limitations in the current bidirectional deformation formulation?

### Limitations

- The paper acknowledges reliance on pseudo-depth from an external estimator, which may introduce noise around fine-scale geometry and depth discontinuities.
- The bidirectional deformation field is trained over a two-frame window, which may lose information from earlier frames in dynamic scenes with fast motion or extended occlusions.
- The orthographic projection may introduce camera model misalignment in close-range scenes with strong perspective effects.
- The velocity bound of [-1,1]^3 limits the method's ability to handle very fast motion between frames.
- The method does not explicitly estimate camera poses, which may limit its applicability in scenarios requiring accurate camera trajectories.
- The paper does not discuss potential negative societal impacts, such as privacy concerns with real-time 3D reconstruction of environments or potential misuse for surveillance.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 119,333
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 110,373
- Completion tokens: 9,912
- Reasoning tokens reported: 0
- Total tokens: 129,245
- Estimated total: $0.01825267

Full individual reviews and raw JSON responses are in `review_bundle.json`.
