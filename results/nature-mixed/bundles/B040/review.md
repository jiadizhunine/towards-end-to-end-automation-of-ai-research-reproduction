# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B040.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.012744**

## Final Meta-review

The paper presents Surf3R, a feedforward neural network for pose-free 3D surface reconstruction from sparse multi-view RGB images. The method eliminates the need for camera calibration and pose estimation (SfM) by employing a multi-branch decoding architecture where multiple reference views collaboratively guide reconstruction through cross-view attention (Feature-Refine blocks) and cross-reference fusion (Cross-Reference Fusion blocks). The model predicts per-pixel 3D Gaussian parameters and introduces a D-Normal regularization strategy that couples surface normals with geometric parameters for joint optimization. Experiments on ScanNet++ and Replica datasets demonstrate state-of-the-art surface reconstruction performance (F1-score 78.71 on ScanNet++) with reconstruction in under 10 seconds, and zero-shot generalization to unseen scenes.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 2.800 | 0.400 | 2-3 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 2.800 | 0.400 | 2-3 |
| Contribution | 3 | 3.200 | 0.400 | 3-4 |
| Overall | 6 | 6.200 | 0.400 | 6-7 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Addresses a practically important problem: eliminating time-consuming SfM preprocessing (1-2 hours per scene) enables rapid 3D reconstruction, a significant deployment bottleneck
- Novel multi-branch architecture with cross-reference fusion effectively handles wide-baseline multi-view scenarios where single-reference approaches fail
- D-Normal regularization grounded in 3D Gaussian representation is technically sound and shows clear improvements in ablation studies (F1-score improvement from 30.96 to 41.92 on Replica)
- Strong quantitative results with significant margins over per-scene optimization baselines (F1-score 78.71 vs 36.12 for SuGaR on ScanNet++)
- Demonstrates zero-shot generalization to unseen datasets (Replica), indicating robustness across different indoor environments
- Comprehensive ablation studies isolating the contribution of each component (multi-branch, scale loss, normal loss, D-Normal loss)
- Excellent efficiency: reconstruction in under 10 seconds, approximately 180x faster than per-scene optimization methods
- Well-written with clear motivation and thorough evaluation of architectural choices

### Weaknesses

- Unfair comparison protocol: per-scene methods (NeuS, 2DGS, SuGaR, PGSR) are evaluated on only 8 ScanNet++ validation scenes while feedforward methods including Surf3R are evaluated on all 50 scenes, potentially inflating the reported performance gap
- Missing quantitative comparison with recent directly comparable feedforward pose-free methods (MASt3R, VGGT, FLARE) that are cited in related work but not included in experiments
- The view ablation shows performance degradation with more input views, attributed to 'accumulated pose estimation errors' which is confusing for a pose-free method and requires clarification
- The 'under 10 seconds' claim lacks specification of hardware, resolution, and whether it includes data loading and mesh extraction
- Limited analysis of failure cases and limitations (e.g., reflective surfaces, textureless regions, occlusions, dynamic scenes)
- High training cost (32 H800 GPUs for 40 hours) may limit reproducibility for smaller research groups
- Evaluation at 224x224 resolution may not reflect real-world deployment scenarios requiring higher detail
- Novel view synthesis results are relatively weak (PSNR 15-18) and only compared against DUSt3R, not more recent generalizable methods
- Several typos and grammatical errors throughout the paper (e.g., 'susrface', 'Muliti-view', 'high idelity')

### Questions

- Why are per-scene methods evaluated on only 8 validation scenes while feedforward methods use all 50? Could you provide results for per-scene methods on the full 50 scenes or justify this choice? How would the performance gap change?
- Can you provide quantitative comparisons with MASt3R, VGGT, and FLARE on surface reconstruction metrics? These are the most directly comparable feedforward pose-free methods and their exclusion is a significant gap.
- In the view ablation (Table 4), why does performance degrade with more input views? The explanation about 'accumulated pose estimation errors' is unclear for a pose-free method. Could this be due to the overlap-based view sampling or TSDF fusion process?
- What exactly does the 'under 10 seconds' reconstruction time include (data loading, inference, mesh extraction)? What GPU hardware and resolution are used?
- How sensitive is the method to the choice of reference views? Are there heuristics for selecting good reference views, or is random selection sufficient? What happens with M=2 or M=8?
- How is the sparse 3D point cloud generated from the fused multi-view features? Is it a separate prediction head or derived from per-view pointmap predictions?
- For mesh extraction, what depth map resolution and TSDF truncation distance are used? Are depth maps rendered from the predicted Gaussians?
- Could you provide qualitative comparisons on challenging scenes (e.g., reflective surfaces, thin structures, textureless regions) and discuss failure cases?
- What is the memory footprint during inference? How does the multi-branch architecture scale to larger numbers of input views?

### Limitations

- The comparison with per-scene optimization methods uses different evaluation protocols (8 vs 50 scenes), which could overstate the reported improvements and should be controlled or justified
- The method is evaluated only on indoor scenes (ScanNet++, Replica); performance on outdoor scenes, object-level reconstruction, or scenes with complex topology is not demonstrated
- The paper does not discuss limitations regarding dynamic scenes, reflective/transparent surfaces, extreme lighting changes, or very large-scale environments
- The training requires substantial computational resources (32 H800 GPUs for 40 hours), limiting reproducibility for smaller research groups
- The method relies on ground-truth depth and normal supervision, which may not be available in all application scenarios
- Potential negative societal impacts are not discussed; high-quality 3D reconstruction from sparse images could be misused for unauthorized surveillance or privacy violations
- The fixed 224x224 resolution may not capture fine surface details needed for high-quality reconstruction in real applications

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 78,683
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 69,723
- Completion tokens: 10,563
- Reasoning tokens reported: 0
- Total tokens: 89,246
- Estimated total: $0.01274395

Full individual reviews and raw JSON responses are in `review_bundle.json`.
