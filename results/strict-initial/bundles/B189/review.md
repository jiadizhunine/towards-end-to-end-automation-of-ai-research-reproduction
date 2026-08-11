# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B189.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.038283**

## Final Meta-review

The paper proposes GeoSplat, a geometry-constrained optimization framework for 3D Gaussian splatting that integrates first-order (normals/tangents) and second-order (curvature) geometric priors into initialization, gradient updates, shape regularization, and densification. It also presents two dynamic geometric estimation methods (manifold-based and varifold-based) intended to provide noise-robust priors. Experiments on Replica and ICL datasets report consistent improvements over 3DGS and GeoGaussian, especially in low-resource settings, with ablations supporting each component.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.000 | 0.000 | 2-2 |
| Clarity | 2 | 1.800 | 0.400 | 1-2 |
| Significance | 2 | 2.400 | 0.490 | 2-3 |
| Soundness | 2 | 2.000 | 0.000 | 2-2 |
| Presentation | 2 | 1.800 | 0.400 | 1-2 |
| Contribution | 2 | 2.400 | 0.490 | 2-3 |
| Overall | 4 | 3.800 | 0.400 | 3-4 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- The incorporation of curvature (second-order geometric information) into Gaussian splatting optimization is a novel and sensible extension beyond normal-only regularizations.
- The framework integrates geometric priors into multiple stages (initialization, optimization, and densification) in a systematic manner, with ablations showing each component contributes.
- Two estimation methods (manifold-based and varifold-based) are proposed, grounding the approach in differential geometry and geometric measure theory.
- Consistent improvements are demonstrated over strong baselines across multiple indoor scenes, including a low-resource setting where gains are larger.
- The use of mean absolute curvature for flat-region detection is a well-motivated improvement.

### Weaknesses

- A key quantitative table (Table 1) contains an impossible LPIPS value of 0.971 for the varifold-based model, which undermines the credibility of the reported results.
- The claimed noise-robustness is not directly validated: there are no experiments with noisy inputs, no comparisons of estimated normals/curvatures to ground truth, and no evaluation under controlled noise or sparsity.
- The computational overhead of the dynamic estimation is not measured; runtime, memory usage, and estimation frequency are not reported despite the claim of efficiency.
- Reproducibility is significantly hindered by duplicate definitions/theorems, inconsistent notation, missing implementation details (kernel functions, bandwidths, KNN sizes, update schedules), and garbled equations.
- The local manifold or varifold assumption may be violated in complex real-world scenes with thin structures, transparency, or non-manifold geometry, yet no analysis of failure cases is provided.
- Improvements over GeoGaussian are often modest (around 1-3% PSNR) and not consistently significant across all metrics; no error bars or statistical tests are shown.
- Evaluation is limited to indoor Replica and ICL datasets; no results on outdoor, unbounded, or object-centric scenes, limiting generality.
- Few comparisons to recent geometry-aware Gaussian splatting methods beyond GeoGaussian (e.g., SAGS) despite mentioning them in related work.

### Questions

- What is the correct LPIPS value for the varifold-based model in Table 1? Is the reported 0.971 a typo?
- What are the exact kernel functions, bandwidths, and approximation scales used in the manifold-based and varifold-based estimators? How are these parameters chosen?
- Where do the normal vectors and tangent planes used in the varifold-based formula come from? Is the varifold-based estimator independent of the manifold-based estimator?
- How often are the geometric priors updated during training, and what is the total wall-clock overhead compared to vanilla 3DGS and GeoGaussian?
- Can the authors provide quantitative evidence of noise robustness by comparing estimated normals/curvatures to ground truth on synthetic surfaces with varying noise levels, and by comparing against local PCA or other baselines?
- How sensitive are the results to key hyperparameters such as xi_min, xi_max, KNN size, and estimation frequency? Is a sensitivity analysis available?
- Why is SAGS (Ververas et al., 2025) not included in the experimental comparisons despite being discussed?
- How does the method handle scenes with thin structures, severe occlusions, or non-manifold geometry where the local manifold assumption may fail?

### Limitations

- The evaluation is restricted to indoor Replica and ICL datasets; performance on outdoor, unbounded, or diverse real-world scenes is not demonstrated.
- The local manifold and varifold assumptions may not hold for scenes with significant volumetric effects, transparency, or complex topology, and failure cases are not discussed.
- The claimed noise-robustness is not validated experimentally; no direct comparison of estimated geometric quantities to ground truth is provided.
- The computational overhead and scalability of the dynamic estimation are not quantified, leaving uncertainty about practical use on large scenes.
- Several hyperparameters require tuning, but no sensitivity analysis is given, making it unclear how generalizable the method is to new datasets.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 227,661
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 223,565
- Completion tokens: 24,903
- Reasoning tokens reported: 18,869
- Total tokens: 252,564
- Estimated total: $0.03828341

Full individual reviews and raw JSON responses are in `review_bundle.json`.
