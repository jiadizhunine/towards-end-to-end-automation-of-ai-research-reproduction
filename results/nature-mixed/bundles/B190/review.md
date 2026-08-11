# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B190.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.013092**

## Final Meta-review

This paper introduces GEM, a cryo-EM reconstruction framework based on 3D Gaussian Splatting (3DGS). Instead of representing protein density with voxel grids (Fourier-based methods) or neural fields (NeRF-based approaches), GEM models density as a compact set of 3D Gaussians (11 parameters each), enabling efficient real-space reconstruction. The method leverages closed-form projection of Gaussians to 2D, applies CTF in Fourier space, and restricts gradient computation to contributing Gaussians. Experiments on four cryo-EM datasets (EMPIAR-10005, 10028, 10049, 10076) demonstrate substantial efficiency gains (up to 48x faster training, 12x lower memory) and improved resolution (GSFSC, local resolution, FSLC) compared to CryoSPARC, CryoDRGN, and CryoNeRF baselines. An ablation study confirms the importance of per-Gaussian rotation and anisotropic scaling.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 4.000 | 0.000 | 4-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 3.400 | 0.490 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.400 | 0.490 | 3-4 |
| Overall | 6 | 6.400 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel and creative application of 3DGS to cryo-EM reconstruction, representing a meaningful transfer of computer vision techniques to structural biology
- Elegant mathematical formulation with closed-form 2D projection of 3D Gaussians, avoiding expensive 3D volume instantiation
- Efficient gradient computation strategy that restricts updates to contributing Gaussians, significantly reducing memory footprint
- Comprehensive evaluation on four standard datasets with multiple complementary metrics (GSFSC, local resolution, FSLC)
- Ablation study provides useful insights into the importance of rotation and anisotropic scaling parameters
- Consistent improvements over baselines in both efficiency and reconstruction quality
- Clear motivation and well-structured presentation of the method

### Weaknesses

- The claimed '48x faster' speedup is misleading - Table 1 shows only ~2x speedup over CryoDRGN, and the 48x figure appears to be against CryoNeRF which OOMs on some datasets
- Incomplete comparison with CryoNeRF - it OOMs on EMPIAR-10028, and the resolution tables only show CryoSPARC and CryoDRGN, making it difficult to verify the claimed advantages over CryoNeRF
- No comparison with RELION, the gold standard Fourier-space method in cryo-EM, limiting the practical significance of the results
- Limited to homogeneous reconstruction only, with no discussion of extension to heterogeneous cases which are common in real cryo-EM datasets
- Insufficient details on Gaussian initialization (number, placement, density threshold for pruning) which are critical for reproducibility
- No analysis of hyperparameter sensitivity, particularly for the threshold tau in Equation 3.8 and the initial Gaussian count
- No code availability is mentioned, which is critical for reproducibility and adoption by the structural biology community
- Potential unfairness in comparison with CryoSPARC if GEM uses pre-computed poses from external tools

### Questions

- Can you provide a clear breakdown of the 48x speedup claim? Table 1 shows varying speedups across datasets and baselines - what is the specific comparison point for this headline number?
- Does GEM require pre-computed particle poses (rotations, translations) or does it jointly optimize them during training? If poses are pre-computed from external tools like CryoSPARC, how does this affect the fairness of comparison with baselines?
- How are the 3D Gaussians initialized? What is the initial number of Gaussians M, and how is this determined for each dataset? Is there an adaptive densification/pruning strategy?
- How sensitive is the method to the threshold tau in Equation 3.8? Is there a principled way to set this hyperparameter?
- Can you provide resolution comparisons with CryoNeRF on datasets where it doesn't OOM? The resolution tables only show CryoSPARC and CryoDRGN.
- Given that EMPIAR-10049 and EMPIAR-10076 are known to exhibit heterogeneity, how does the homogeneous reconstruction assumption of GEM affect the interpretation of the reported resolutions?
- How does the number of 3D Gaussians scale with protein size, and what is the relationship between Gaussian count and reconstruction quality?
- Have you considered extending GEM to heterogeneous reconstruction (multiple conformational states)?
- How does the method handle datasets with lower SNR or larger proteins? Any failure cases?
- What is the total training time and number of iterations for each dataset? The efficiency comparison reports speed (it/s) but not total training time.
- Can you clarify the notational inconsistencies in Appendix A.2 where indices i and j are sometimes used interchangeably?
- Are there any plans to release the code and trained models for reproducibility?

### Limitations

- The method is limited to homogeneous reconstruction and does not address heterogeneity, which is common in real cryo-EM datasets
- The paper lacks a thorough analysis of hyperparameter sensitivity, particularly for the Gaussian thresholding parameter and initial Gaussian count
- Reproducibility is limited by insufficient details on the initialization and optimization schedule
- The comparison with CryoNeRF is incomplete due to OOM issues, potentially limiting the strength of efficiency claims
- No comparison with RELION, limiting the practical relevance for the cryo-EM community
- The claimed speedup factors are somewhat overstated given the actual comparisons in Table 1
- The method's performance on larger proteins or datasets with strong preferred orientation is not explored
- No discussion of potential negative societal impacts, though cryo-EM research is generally beneficial; the efficiency gains could democratize access to high-resolution structural biology

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 83,186
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 74,226
- Completion tokens: 9,556
- Reasoning tokens reported: 0
- Total tokens: 92,742
- Estimated total: $0.01309241

Full individual reviews and raw JSON responses are in `review_bundle.json`.
