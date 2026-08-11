# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B189.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.034832**

## Final Meta-review

The paper introduces GeoSplat, a geometry-constrained optimization framework for Gaussian splatting that integrates first-order (normals, tangents) and second-order (curvature) geometric priors throughout the training pipeline. The framework applies curvature-guided initialization, truncated gradient updates and shape regularization during optimization, and curvature-regularized densification. It also proposes two noise-robust dynamic estimation methods: a manifold-based approach using heat kernel/Laplacian techniques and a varifold-based approach from geometric measure theory. Experiments on Replica and ICL datasets show consistent improvements over 3DGS and GeoGaussian baselines, with larger gains in sparse-view settings. Ablation studies validate each component, though on a limited number of scenes.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.800 | 0.400 | 3-4 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 3 | 2.600 | 0.490 | 2-3 |
| Significance | 3 | 3.400 | 0.490 | 3-4 |
| Soundness | 3 | 2.800 | 0.400 | 2-3 |
| Presentation | 3 | 2.600 | 0.490 | 2-3 |
| Contribution | 3 | 3.200 | 0.400 | 3-4 |
| Overall | 6 | 6.200 | 0.748 | 5-7 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Novel incorporation of second-order geometric information (curvature) into Gaussian splatting, which is largely underexplored in prior work that focuses on normals.
- Comprehensive integration of geometric priors across initialization, optimization, and densification stages, providing a holistic framework rather than a single ad-hoc regularization.
- Two complementary estimation methods (manifold-based and varifold-based) are theoretically well-grounded and address the limitation of static, noise-sensitive priors in prior methods.
- Consistent experimental improvements over strong baselines across multiple datasets and settings, particularly notable in low-resource scenarios.
- Detailed appendix derivations connecting Gaussian primitives to differential geometry and geometric measure theory, making the approach self-contained.
- The use of mean absolute curvature (MAC) for identifying flat regions is a thoughtful and justified improvement over mean curvature.

### Weaknesses

- Experimental evaluation is limited to indoor scenes (Replica, ICL); generalization to outdoor, unbounded, or more diverse datasets (e.g., Mip-NeRF 360, Tanks and Temples) is not demonstrated.
- Comparison with recent geometry-regularized methods such as SAGS (which also uses curvature) is missing, weakening the claim of outperforming prior curvature-based approaches.
- The appendix contains incomplete proofs (empty 'Proof' placeholders) and duplicated definitions in the main text, suggesting insufficient preparation and undermining theoretical credibility.
- The computational overhead of the dynamic geometric estimation is not quantified (e.g., total training time or memory usage comparisons), despite claims of efficiency.
- Ablation studies are conducted on only two scenes, limiting the statistical power and generalizability of component-wise conclusions.
- The claimed noise robustness of the estimation methods is not quantitatively validated through experiments with varying noise levels.
- The varifold-based method appears to depend on the manifold-based method for initial normal/tangent estimates, so it is not fully independent as presented.
- Absolute improvements over GeoGaussian are modest (typically 1-3% PSNR), and the paper does not deeply analyze when or why the method provides larger gains.

### Questions

- Can you provide quantitative experiments demonstrating the noise robustness of the proposed estimation methods compared to local PCA or other baselines, e.g., by adding noise to Gaussian centers and measuring estimation accuracy?
- Why are the proof placeholders left empty in the appendix? Are these proofs available elsewhere? If not, this significantly affects the credibility of the theoretical contributions.
- Why is SAGS (Ververas et al., 2025) not included in the main experimental comparison? A direct comparison would be important given its use of curvature.
- What is the additional training time and memory overhead of the geometric estimation and regularization components compared to vanilla 3DGS? Please provide a breakdown.
- Could you evaluate the method on outdoor or unbounded scenes (e.g., Mip-NeRF 360, Tanks and Temples) to demonstrate broader applicability?
- Under what specific conditions or scene characteristics does the varifold-based method outperform the manifold-based approach? The paper mentions 'in some cases' without specifying.
- How sensitive is performance to hyperparameters such as ξ_min, ξ_max, and the number of nearest neighbors? Please provide sensitivity analysis.
- How is the Laplacian operator estimated in practice for the manifold-based method (kernel bandwidth, handling of non-uniform point distributions)?
- In the varifold-based method, how are the varifold masses m_j computed and are they updated during training? Is the method truly independent of the manifold-based method?

### Limitations

- The evaluation is restricted to indoor, bounded scenes; performance on outdoor or unbounded environments is unknown and not discussed.
- The paper claims noise robustness but does not provide quantitative evidence; this property needs experimental validation.
- The varifold-based method's dependence on the manifold method for initial estimates limits its applicability as a standalone approach.
- The paper does not discuss potential failure cases, such as scenes with complex topology, thin structures, or large textureless regions.
- Hyperparameters (ξ_min, ξ_max, number of neighbors) are not justified with sensitivity analysis.
- The computational cost of the geometric estimation is not analyzed in detail, which is important for practical deployment.
- Potential negative societal impacts are not discussed, though the technology could be used in surveillance or deepfake creation contexts.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 238,663
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 229,703
- Completion tokens: 9,459
- Reasoning tokens reported: 0
- Total tokens: 248,122
- Estimated total: $0.03483203

Full individual reviews and raw JSON responses are in `review_bundle.json`.
