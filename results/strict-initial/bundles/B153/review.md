# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B153.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.016147**

## Final Meta-review

The paper analyzes the split and clone operations in 3D Gaussian Splatting (3DGS) densification, arguing that splits control global spatial spread while clones refine local details. Based on this, it proposes a global-to-local densification strategy (split-first, then clone), an energy-aware coarse-to-fine multi-resolution training schedule, and adaptive opacity pruning. Experiments on MipNeRF-360, Deep Blending, and Tanks & Temples report roughly 2x training speedup over an accelerated 3DGS baseline, with fewer Gaussian primitives and comparable or slightly better PSNR/SSIM, but consistently worse LPIPS.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 2 | 2.400 | 0.490 | 2-3 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 2 | 2.000 | 0.000 | 2-2 |
| Significance | 2 | 2.400 | 0.490 | 2-3 |
| Soundness | 2 | 2.200 | 0.400 | 2-3 |
| Presentation | 2 | 2.000 | 0.000 | 2-2 |
| Contribution | 2 | 2.200 | 0.400 | 2-3 |
| Overall | 4 | 4.000 | 0.000 | 4-4 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Provides an empirical analysis of split versus clone operations, showing that split-dominated Gaussians exhibit larger spatial displacement (global spread) while clones dominate densification counts (local refinement), which motivates the phased densification strategy.
- The global-to-local densification idea is simple and easy to implement, and the combination with energy-guided multi-resolution training and adaptive pruning yields a substantial training-time reduction across three standard datasets.
- The paper includes extensive experiments with multiple recent acceleration baselines (3DGS-accel, Mini-splatting, EDC, DashGaussian) and ablation studies isolating each proposed component, as well as hyperparameter sensitivity analyses.
- The adaptive opacity pruning effectively reduces Gaussian counts and training time while preserving most of the reconstruction quality, contributing to the overall speedup.

### Weaknesses

- The claimed 'superior reconstruction performance' is not consistently supported: LPIPS is worse than the accelerated 3DGS baseline and often worse than other baselines on all three datasets, indicating a perceptual quality trade-off that is not adequately acknowledged.
- The split/clone analysis is partly tautological and confounded: splits create new Gaussians around the original distribution while clones duplicate at the same position, so displacement differences may reflect initial scale and threshold behavior rather than intrinsic roles. No controlled experiment or statistical significance test is provided.
- The energy-aware multi-resolution scheduler is poorly specified: Equation (6) is ambiguous about whether T_r is cumulative or per-resolution, the boundary condition T_{K+1} is undefined, and no concrete resolution schedule or pseudocode is given, hampering reproducibility.
- Ablation results show that global-to-local densification alone degrades quality (e.g., SSIM drops from 0.8213 to 0.8066), and adding it to coarse-to-fine also reduces SSIM/PSNR compared to coarse-to-fine alone, casting doubt on the necessity of the central contribution.
- Comparisons with baselines are not fully apples-to-apples: differences in base code versions, iteration budgets, and hyperparameters are not controlled, and no error bars or multiple-run statistics are reported.
- The paper is not fully reproducible: exact positional learning rate schedules, phase-boundary selection, and code release are missing, and the presentation has numerous typos, broken cross-references, and inconsistent terminology.

### Questions

- In Equation (6), is T_r the total number of iterations allocated to resolution r or a cumulative endpoint? Could you provide a concrete example of T_r values for a MipNeRF-360 scene with K=8, including how T_{K+1} is defined?
- How are split_count and clone_count propagated when a cloned Gaussian is later split (or vice versa)? Does the classification into split-dominated/clone-dominated use inherited counts from the parent chain, and how sensitive are the displacement results to the threshold chosen?
- Why does the global-to-local densification alone substantially reduce SSIM (0.8066 vs 0.8213 in the ablation)? How is the phase boundary T_2 selected in practice, and is there an optimal boundary?
- How is the energy ratio E_r/E_1 computed per scene? Is it based on a single representative image or averaged over all training views, and does the scheduler adapt if scene content changes?
- What is the exact resolution schedule used in the multi-resolution training (number of iterations per resolution) for each dataset, and how does it compare to a simple fixed coarse-to-fine schedule under the same total budget?
- Why is LPIPS consistently worse after applying the proposed method, even though PSNR/SSIM are maintained? Is there a perceptual quality trade-off, and could different pruning or resolution settings mitigate it?
- How much computational overhead is added by computing the Fourier energy spectrum for each image, and how are training times with and without the scheduler computed?
- What are the memory usage and rendering speed of the final model compared to baselines, and are the reported timing differences statistically significant across multiple runs?

### Limitations

- The method consistently yields worse LPIPS than the accelerated 3DGS baseline and often worse than other baselines, indicating a perceptual quality degradation that is not thoroughly analyzed.
- The energy-guided resolution schedule is heuristic and lacks theoretical backing or comparison to simpler fixed schedules; it may not generalize to scenes with different frequency statistics.
- The analysis and experiments are limited to three static scene datasets; dynamic scenes, outdoor large-scale scenes, and object-level reconstruction are not evaluated.
- The method does not address the inherent blur problem of 3DGS caused by large Gaussians, as acknowledged in the conclusion.
- No code or trained models are released, limiting reproducibility and adoption.
- The method relies on several hyperparameters (K, p, tau_u, T_densify) that require per-scene tuning, and the sensitivity analysis suggests quality drops for aggressive settings.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 70,180
- Cache-hit prompt tokens: 3,840
- Cache-miss prompt tokens: 66,340
- Completion tokens: 24,460
- Reasoning tokens reported: 17,988
- Total tokens: 94,640
- Estimated total: $0.01614715

Full individual reviews and raw JSON responses are in `review_bundle.json`.
