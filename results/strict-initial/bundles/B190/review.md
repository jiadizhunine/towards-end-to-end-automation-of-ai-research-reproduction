# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B190.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.017852**

## Final Meta-review

The paper proposes GEM, a homogeneous cryo-EM reconstruction method based on 3D Gaussian Splatting. The density is represented as a set of anisotropic 3D Gaussians, with closed-form projection to 2D images, CTF modulation, and MSE loss. It reports speed and memory improvements over NeRF-based CryoNeRF, and improved resolution metrics over CryoSPARC/CryoDRGN on four EMPIAR datasets, with ablations on rotation and anisotropic scaling.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 2 | 2.000 | 0.632 | 1-3 |
| Significance | 2 | 2.400 | 0.490 | 2-3 |
| Soundness | 2 | 2.200 | 0.400 | 2-3 |
| Presentation | 2 | 2.000 | 0.632 | 1-3 |
| Contribution | 2 | 2.400 | 0.490 | 2-3 |
| Overall | 4 | 3.800 | 0.400 | 3-4 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel and timely adaptation of 3D Gaussian Splatting to cryo-EM reconstruction, offering an explicit compact real-space representation.
- Closed-form projection of Gaussian mixtures avoids explicit dense volume sampling and could reduce memory/compute.
- Significant reported speedups and memory reductions compared to CryoNeRF.
- Evaluation on four EMPIAR datasets with GSFSC, local resolution, and FSLC.
- Ablation confirms importance of per-Gaussian rotation and anisotropic scaling.

### Weaknesses

- The closed-form projection derivation appears mathematically incorrect: the normalization/parameter transformation is not properly derived; e.g., covariance transform W Sigma W^T is dropped, and an extra factor is missing in Eq. 3.6/Appendix.
- Z-sorting and 'influential Gaussians' accumulation is unjustified for additive line integrals; order should not matter, suggesting confusion with alpha compositing.
- CryoNeRF, the main real-space baseline, is excluded from resolution comparisons (GSFSC/local resolution/FSLC); therefore the claim that GEM surpasses real-space SOTA in quality is unsupported.
- The headline numbers (48x speedup, 12x memory, 38.8% local resolution) are not directly substantiated by the tables and contain inconsistencies (e.g., text reports 2.28 Å vs 2.58 Å in Table 3 for EMPIAR-10005).
- The paper lacks reproducibility-critical details: number/initialization of Gaussians, threshold tau, optimizer, learning rate, half-set splitting, masking and voxelization procedure, etc.; no code is released.
- The method assumes known poses and CTFs and only does homogeneous reconstruction; no pose/CTF refinement or heterogeneity handling.
- Evaluation is incomplete: no comparison with other recent real-space/fourier-space methods, no comparison with deposited/ground-truth structures, no statistical significance tests.
- Many typographical and notation errors undermine clarity and credibility.

### Questions

- Can the authors provide the correct closed-form projection derivation, including normalization and covariance transformation for rotated Gaussians?
- Why is CryoNeRF not evaluated in GSFSC/local resolution/FSLC? What are its resolution numbers, and how does GEM compare in quality?
- What are the exact training details (number of Gaussians, initialization, threshold tau, densification, optimizer, learning rate, half-set splits, masking, voxelization) needed for reproduction?
- How are the headline claims (48x speedup, 12x memory, 38.8% local resolution) computed, and why do they not match the tables?
- Does the z-sorting affect the projection result? If not, what is its purpose?
- Can GEM be extended to heterogeneous reconstruction and joint pose/CTF refinement?

### Limitations

- Only homogeneous reconstruction with known poses/CTFs; no heterogeneity or pose/CTF refinement.
- Method not compared with several recent baselines; missing real-space SOTA quality comparison.
- No code or detailed hyperparameters, limiting reproducibility.
- Potential overfitting to noise with simple MSE loss not discussed; no ground-truth structure comparison.
- Mathematical errors/ambiguities in projection and FSC evaluation protocol.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 75,544
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 71,448
- Completion tokens: 27,991
- Reasoning tokens reported: 21,211
- Total tokens: 103,535
- Estimated total: $0.01785167

Full individual reviews and raw JSON responses are in `review_bundle.json`.
