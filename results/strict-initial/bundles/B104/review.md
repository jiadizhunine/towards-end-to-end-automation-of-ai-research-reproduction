# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B104.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **3/5**
- Independent decisions: {'Accept': 3, 'Reject': 2}
- Estimated API cost: **$0.021116**

## Final Meta-review

Dream4Drive proposes a synthetic-data generation framework for autonomous driving perception. It inserts 3D assets into multi-view driving videos via dense 3D-aware guidance maps (depth, normal, edge, object image, mask) and a fine-tuned diffusion transformer. The paper argues that prior synthetic-augmentation evaluations are unfair because they use double training epochs (pretrain on synthetic, finetune on real). Under matched epochs, adding fewer than 420 synthetic samples (less than 2% of real data) reportedly improves downstream detection and tracking on nuScenes. The authors also introduce DriveObj3D, a large-scale 3D asset dataset for driving scenarios.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.400 | 0.490 | 2-3 |
| Clarity | 2 | 2.600 | 0.490 | 2-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 2 | 2.400 | 0.490 | 2-3 |
| Presentation | 2 | 2.600 | 0.490 | 2-3 |
| Contribution | 3 | 2.800 | 0.400 | 2-3 |
| Overall | 4 | 5.200 | 0.980 | 4-6 |
| Confidence | 3 | 3.400 | 0.490 | 3-4 |

### Strengths

- Identifies a meaningful evaluation pitfall in synthetic data augmentation: prior methods often use twice the training epochs, which can inflate their apparent benefit; the paper attempts to compare under matched epochs.
- Proposes a novel 3D-aware video editing pipeline using dense guidance maps and a fine-tuned DiT world model, enabling instance-level, multi-view consistent object insertion.
- Introduces DriveObj3D, a large-scale 3D asset dataset for driving scenes, which could support future research.
- Demonstrates that with only 420 synthetic samples, downstream detection and tracking can improve under multiple training epoch settings, with largest gains on rare classes and at higher resolution.
- Includes extensive experiments on nuScenes covering resolutions, epochs, insertion positions, distances, and asset sources, plus generation-quality comparisons (FVD/FID).

### Weaknesses

- The 'fair comparison' claim is not fully supported: prior methods' numbers are taken from their original papers rather than re-trained under the same detector, resolution, and training schedule; the synthetic data volume and training iterations are not matched.
- The 'same epoch' setup does not equate to matched training iterations or compute: adding 420 samples increases gradient updates per epoch, and no control with +420 real samples or matched total steps is provided.
- The downstream perception model used for the main detection/tracking tables is not specified (StreamPETR is only mentioned in an appendix), hampering reproducibility.
- Architectural details of the multi-condition fusion adapter, spatial view attention, and 3D embedders are missing, so an expert cannot easily reproduce the method.
- No statistical significance tests or multiple seeds are reported; observed gains (e.g., +0.3 mAP) may be within run-to-run noise.
- Evaluation is limited to nuScenes; cross-dataset generalization, closed-loop/planning evaluation, and comparisons with established augmentation techniques (e.g., copy-paste) are absent.
- The training data construction for the inpainting model is underspecified: the target edited videos used in the diffusion, mask, and LPIPS losses are not clearly described.
- DriveObj3D is described as large-scale but lacks quantitative statistics and asset-quality evaluation.
- The computational cost of the full pipeline (3D asset generation, rendering, fine-tuning the world model) is not reported.

### Questions

- What exact downstream detection/tracking models and training configurations are used in Tables 1–4? Are the reported metrics averaged over multiple random seeds with standard deviations?
- How were the numbers for prior methods (Panacea, SubjectDrive, etc.) obtained? Were they re-trained with the same detector and resolution, or taken from original papers? What synthetic data budgets and training schedules were used?
- In the 1x/2x/3x epoch comparisons, is the total number of gradient updates exactly matched between Real-only and Real+420? Would adding 420 real samples produce a similar gain?
- What are the target images in Eqs. (5)-(8)? Are they naive composites of 3D assets into real frames, or something else?
- How were the 420 inserted samples selected, and how sensitive are the downstream results to this selection?
- What are the size, category distribution, and quality metrics of DriveObj3D?
- Does the method generalize to other driving datasets such as Waymo, or to other perception models beyond StreamPETR?
- What is the total GPU time required for the full Dream4Drive pipeline, including 3D asset generation and world-model fine-tuning?

### Limitations

- Only evaluated on nuScenes; generalization to other datasets/cities remains unknown.
- Inserted trajectories are not automatically checked for drivability or collision avoidance, limiting fully automatic corner-case generation.
- The asset generation pipeline depends on proprietary or external models (Qwen-Image, Hunyuan3D, Grounding-SAM, Depth Anything), which may limit reproducibility and introduce domain-specific biases.
- The modest perception gains may not be statistically significant due to the absence of multiple seeds or error bars.
- No human evaluation of photorealism or physical plausibility is provided; perception metrics may not capture dangerous artifacts.
- Potential negative societal impacts of generating realistic driving videos (e.g., fake footage) are not discussed.
- The computational and financial cost of building DriveObj3D and fine-tuning the inpainting model is not disclosed, hindering adoption and reproducibility.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 90,165
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 86,069
- Completion tokens: 32,340
- Reasoning tokens reported: 25,606
- Total tokens: 122,505
- Estimated total: $0.02111633

Full individual reviews and raw JSON responses are in `review_bundle.json`.
