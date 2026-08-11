# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B153.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 3, 'Reject': 2}
- Estimated API cost: **$0.012388**

## Final Meta-review

The paper analyzes the roles of split and clone operations during 3D Gaussian Splatting (3DGS) densification, showing that split operations primarily drive global spatial diffusion while clone operations contribute to local refinement. Based on this analysis, the authors propose a global-to-local densification strategy that decouples these operations across training phases, an energy-guided coarse-to-fine multi-resolution training framework, and adaptive opacity pruning. Experiments on MipNeRF-360, Deep Blending, and Tanks & Temples show approximately 2x training speedup over the 3DGS-accel baseline with fewer Gaussian primitives, though quality results are mixed (improved PSNR/SSIM on some datasets but consistently worse LPIPS).

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 2 | 2.400 | 0.490 | 2-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 2 | 2.400 | 0.490 | 2-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 5.600 | 0.490 | 5-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The systematic analysis of split vs. clone operations is novel and provides useful insight into 3DGS training dynamics that prior work has not explicitly examined.
- The global-to-local densification strategy is conceptually clean and well-motivated by the empirical analysis.
- The energy-guided multi-resolution scheduling is an interesting approach that adaptively allocates training iterations based on image content complexity.
- Comprehensive experiments on three standard datasets with multiple baselines and thorough ablation studies for each component.
- Achieves meaningful training acceleration (~2x speedup) with reduced Gaussian primitive counts.
- Good qualitative results showing improved reconstruction of small and distant objects.
- The paper is honest about limitations, including the LPIPS trade-off and the inherent blur problem in 3DGS.

### Weaknesses

- The claim of 'superior reconstruction performance' is not supported: LPIPS is consistently worse than the 3DGS-accel baseline across all datasets (e.g., 0.2136 vs 0.2095 on MipNeRF-360), indicating perceptual quality degradation.
- The ablation shows that the global-to-local strategy alone degrades quality significantly (SSIM drops from 0.8213 to 0.8066), and the final quality improvement is driven primarily by the coarse-to-fine (C2F) component, which is less novel. The paper lacks a clear explanation for this interaction.
- The energy-based resolution scheduling lacks strong theoretical justification; the connection between image frequency energy and optimal iteration allocation is heuristic.
- Comparison with DashGaussian shows similar training times but worse LPIPS on all datasets, weakening the claim of overall superiority.
- Missing comparison with Speedy-Splat and other recent 3DGS acceleration methods that are cited in related work.
- The analysis of split/clone operations relies on displacement statistics that may be partially tautological (splits create new positions by definition) and lacks deeper investigation of optimization dynamics.
- The paper does not provide code or detailed implementation specifics for reproducibility.
- Writing quality issues include grammatical errors, formatting problems, and unclear figure references.

### Questions

- Why does the global-to-local strategy alone degrade quality so significantly (SSIM from 0.8213 to 0.8066), and how does combining it with the coarse-to-fine framework recover most of this loss? Can you provide more analysis of the interaction between these two components?
- The LPIPS metric is consistently worse than the baseline across all datasets. Can you explain why perceptual quality degrades despite PSNR improvements, and is this trade-off acceptable for the reported speedup?
- How is the energy-based iteration allocation (Eq. 6) derived? Is there empirical evidence that energy ratios correspond to optimal iteration counts, or is this a heuristic? Have you compared against simpler fixed or uniform resolution schedules?
- How does the method compare to Speedy-Splat, which is cited but not evaluated? Would it outperform your reported speed and quality?
- What is the computational overhead of computing FFT-based energy density for each scene? Does this overhead diminish the reported training speedup?
- The paper mentions keeping the positional learning rate constant during downsampled training. What is the rationale, and how does this interact with the resolution switching schedule?
- How sensitive is the method to the choice of K (max scale factor) and other hyperparameters (pruning ratio, upper limit)? Is K=8 optimal across all datasets?
- How does the method perform when initialized from different point cloud densities (e.g., COLMAP with different quality settings)?

### Limitations

- The paper acknowledges it does not address the inherent blur problem in 3DGS from insufficient gradient accumulation for large Gaussians, which is a significant limitation for practical applications.
- The consistently worse LPIPS suggests potential perceptual quality loss that may limit real-world applicability.
- The method is evaluated only on static scene reconstruction; applicability to dynamic scenes or other 3DGS extensions is not explored.
- The energy-based scheduling may be dataset-dependent and requires per-scene computation of Fourier transforms, adding preprocessing overhead not fully accounted for in training time.
- The method requires tuning multiple hyperparameters (pruning ratio, upper limit, max scale factor), which may limit practical applicability.
- The analysis of split/clone roles is based on displacement distances, which may not fully capture the complexity of densification dynamics.
- Potential negative societal impact is not discussed, though this is typical for scene reconstruction papers (e.g., privacy concerns with reconstructing spaces without consent).

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 78,047
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 69,087
- Completion tokens: 9,608
- Reasoning tokens reported: 0
- Total tokens: 87,655
- Estimated total: $0.01238751

Full individual reviews and raw JSON responses are in `review_bundle.json`.
