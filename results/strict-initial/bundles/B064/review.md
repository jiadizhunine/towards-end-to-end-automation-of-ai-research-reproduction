# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B064.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 2, 'Reject': 3}
- Estimated API cost: **$0.020139**

## Final Meta-review

The paper introduces StreamSplat, a fully feed-forward framework for online dynamic 3D Gaussian Splatting (3DGS) reconstruction from uncalibrated video streams. It encodes each frame into pixel-aligned 3D Gaussians in an orthographic canonical space using a probabilistic position sampling mechanism, and predicts a bidirectional deformation field with adaptive Gaussian fusion to model scene dynamics. The system operates frame-by-frame with cached embeddings, enabling online inference and rendering at arbitrary times and viewpoints. Experiments on static benchmarks (CO3Dv2, RealEstate10K) and dynamic benchmarks (DAVIS, YouTube-VOS) demonstrate strong dynamic interpolation quality and a significant speed advantage over optimization-based dynamic reconstruction baselines.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 2 | 3.000 | 0.632 | 2-4 |
| Quality | 2 | 2.400 | 0.490 | 2-3 |
| Clarity | 2 | 2.400 | 0.800 | 2-4 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 2 | 2.400 | 0.490 | 2-3 |
| Presentation | 2 | 2.200 | 0.400 | 2-3 |
| Contribution | 2 | 2.600 | 0.490 | 2-3 |
| Overall | 4 | 4.400 | 1.020 | 3-6 |
| Confidence | 4 | 3.600 | 0.490 | 3-4 |

### Strengths

- Addresses an important and underexplored problem: online, pose-free, feed-forward dynamic 3D reconstruction from uncalibrated video streams.
- The proposed probabilistic position sampling and bidirectional deformation with adaptive Gaussian fusion are well-motivated and supported by ablation studies, yielding strong dynamic interpolation results.
- The method is substantially faster than optimization-based dynamic reconstructions (1.48 s/frame vs. minutes/hours), enabling near-real-time processing with online inference.
- Comprehensive experiments across multiple static and dynamic benchmarks, including video interpolation, with comparisons to a broad set of baselines.

### Weaknesses

- The claim of 'real-time' reconstruction is not supported: 1.48 s per frame is far below typical video frame rates, and the paper inconsistently uses 'real-time' and 'near real-time' without a runtime breakdown.
- Static novel-view synthesis results are markedly inferior to static feed-forward baselines (PSNR 24.68 vs. ~28.5), undermining claims of state-of-the-art reconstruction quality.
- The method relies heavily on a pretrained monocular depth estimator (Depth Anything V2) and DINOv2 features, introducing an external prior that is noisy at discontinuities; the impact of poor depth estimates is not analyzed.
- The bidirectional deformation field is trained only on a two-frame window, limiting long-term temporal context; no quantitative analysis of error accumulation or memory growth for long streams is provided.
- Technical exposition is incomplete: the deformation equations and rendering of 'arbitrary viewpoints' under orthographic projection without camera poses are underspecified, hindering reproducibility.
- Evaluation protocols are potentially unfair: static baselines create a single world-anchored representation, while StreamSplat encodes each frame independently, leading to suspiciously high given-view PSNR (>40 dB); comparisons with related feed-forward dynamic methods (e.g., BTimer) are missing.

### Questions

- What is the exact runtime breakdown of the 1.48 s/frame inference, and does it include pseudo-depth and DINOv2 feature extraction? How does runtime scale with input resolution?
- How are novel viewpoints rendered without camera poses? Are the reported novel-view results limited to interpolated timestamps on the original trajectory, or are truly arbitrary viewpoints synthesized?
- How is the probabilistic position sampling resolved at inference (mean vs. sampled)? How does this affect temporal consistency of rendered frames?
- How does the method handle large occlusions, newly appearing objects, or topology changes that span more than two frames? Is there error accumulation over long video sequences?
- Why is BTimer, a related feed-forward dynamic reconstruction method, not included in the experimental comparisons?
- What is the memory usage for arbitrarily long video streams? Does the cache grow linearly with video length, and how is it bounded?

### Limitations

- The method depends on an external monocular depth prior, which may be unreliable in domains with depth discontinuities or unusual geometry.
- The two-frame temporal window restricts long-range dynamic modeling, potentially causing failure in fast-motion or extended occlusion scenarios.
- The orthographic canonical space and lack of explicit camera pose estimation limit novel-view synthesis, particularly for large camera motions or strong perspective effects.
- The reported inference time of 1.48 s/frame is not real-time for standard video rates (e.g., 30 FPS), limiting deployment in latency-critical applications.
- Training on dynamic datasets requires object segmentation masks; performance without mask supervision is not evaluated.
- The 'adaptive fusion' is essentially opacity modulation and does not truly merge or consolidate Gaussians across time, potentially limiting memory efficiency for long streams.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 93,672
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 89,576
- Completion tokens: 27,095
- Reasoning tokens reported: 20,960
- Total tokens: 120,767
- Estimated total: $0.02013871

Full individual reviews and raw JSON responses are in `review_bundle.json`.
