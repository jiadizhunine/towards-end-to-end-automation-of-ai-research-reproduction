# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B104.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.017934**

## Final Meta-review

The paper introduces Dream4Drive, a 3D-aware synthetic data generation framework for improving downstream perception tasks (3D detection and tracking) in autonomous driving. The authors identify a critical flaw in prior synthetic data augmentation evaluations: prior methods train on synthetic+real data for twice the epochs (pretrain on synthetic, finetune on real) compared to real-only baselines. Under equal training epochs, prior synthetic data provides negligible or negative gains. Dream4Drive addresses this by decomposing real multi-view videos into dense 3D-aware guidance maps (depth, normal, edge, object image, mask), rendering 3D assets into these maps, and using a fine-tuned diffusion transformer with a multi-condition fusion adapter to generate photorealistic edited videos with cross-view consistency. The authors also contribute DriveObj3D, a large-scale 3D asset dataset for driving scenarios. Experiments on nuScenes show that adding less than 2% synthetic samples (420 samples) consistently improves detection (mAP, NDS) and tracking (AMOTA) across 1x, 2x, and 3x training epochs, outperforming prior augmentation baselines under fair evaluation.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.600 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.400 | 0.490 | 3-4 |
| Significance | 4 | 3.600 | 0.490 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.400 | 0.490 | 3-4 |
| Contribution | 4 | 3.600 | 0.490 | 3-4 |
| Overall | 6 | 6.400 | 0.800 | 5-7 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Identifies and clearly demonstrates an important evaluation flaw in prior synthetic data augmentation work: unequal training epochs (pretrain+finetune vs. train-only) unfairly inflate the benefits of synthetic data. This is a valuable methodological contribution.
- The proposed 3D-aware guidance map approach (depth, normal, edge, object, mask) is novel and technically sound, providing dense geometric and appearance control for video editing with better cross-view consistency than sparse controls.
- Comprehensive experiments across detection and tracking, multiple training epochs (1x, 2x, 3x), and resolutions (256x512, 512x768), with detailed ablations on insertion position, distance, asset source, trajectory speed, and scaling behavior.
- The DriveObj3D dataset is a valuable community resource, with a well-designed pipeline for automatic 3D asset generation covering diverse driving categories.
- The paper is honest about limitations (e.g., collision-free trajectories remain open, scaling shows diminishing returns) and provides detailed implementation and time-cost analysis in the appendix.
- The finding that small amounts of OOD synthetic data (<2%) can significantly improve perception, while larger amounts may hurt, is counterintuitive and practically relevant.

### Weaknesses

- Evaluation is limited to a single dataset (nuScenes) and a single perception model family (StreamPETR). Generalization to other datasets (e.g., Waymo, Argoverse) and architectures (e.g., BEVFormer, CenterPoint) is not demonstrated.
- The main comparison table (Table 1) uses different resolutions: prior methods at 256x512 while Dream4Drive is at 512x768. This is a significant fairness concern that undermines the paper's central claim of 'fair evaluation.'
- The scaling analysis (Table 8) shows that increasing from 7 to 35 scenes does not improve (and can slightly hurt) performance. This raises questions about the practical scalability of the approach and contradicts the narrative that synthetic data is broadly beneficial.
- The improvements over real-data-only baselines are modest (e.g., 0.3-0.6 mAP points at 2x/3x epochs), and no statistical significance testing is provided. The gains could be within noise.
- Comparison with prior methods is limited: only Panacea and SubjectDrive are compared in downstream perception tasks, while more recent strong generation baselines (e.g., UniScene, CoGen, DriveDream-2) are only compared on generation quality metrics, not on their effectiveness for perception augmentation.
- The synthetic data volume (420 samples) is very small, and the paper does not deeply analyze the mechanism by which such a small amount of OOD data provides significant gains.
- The synthesis pipeline still requires manual verification and orientation annotation, limiting claims of full automation and scalability.

### Questions

- In Table 1, prior methods are evaluated at 256x512 resolution while Dream4Drive is at 512x768. How much of the performance gap is due to resolution rather than the method itself? Would prior methods show similar gains if evaluated at 512x768?
- The scaling analysis shows diminishing returns with more OOD scenes. What is the mechanism behind this degradation? Is it domain shift, overfitting to synthetic distribution, or something else? Have you tried mixing different numbers of synthetic samples with real data to find the optimal ratio?
- How does Dream4Drive-generated data perform with different perception models (e.g., BEVFormer, DETR3D) rather than only StreamPETR? Would the gains generalize across architectures?
- How are the 3D bounding box annotations for inserted assets generated in the training data? Are they automatically derived from the 3D asset placement and camera calibration?
- Could you provide a direct comparison with prior editing methods (e.g., SubjectDrive) under identical resolution (512x768) and training epochs to strengthen the 'fair comparison' claim?
- What is the statistical significance of the reported improvements? Are the gains consistent across multiple random seeds?
- Would the method work on other datasets (e.g., Waymo) without significant retuning?
- The paper mentions that inserted trajectories are always straight. Have you considered more complex trajectories (e.g., lane changes, turns) and how would that affect downstream performance?

### Limitations

- The evaluation is limited to nuScenes and StreamPETR, which may not generalize to other datasets or perception architectures.
- The synthetic data generation pipeline, while partially automated, still requires human verification and manual annotation of insertion positions, which may limit practical scalability.
- The paper acknowledges that automatically ensuring collision-free trajectories remains an open challenge, limiting the generation of diverse corner cases.
- The scaling analysis suggests that the method's benefits are limited to small amounts of OOD data, which may limit its utility for large-scale data augmentation in production systems.
- The paper does not discuss potential negative societal impacts beyond a brief ethics statement, such as the risk of synthetic data being used to train surveillance systems or biases in the asset library (e.g., underrepresentation of certain vehicle types or pedestrian demographics).
- The paper does not provide a detailed analysis of failure cases of the generation model (e.g., artifacts, inconsistent shadows) or when the method fails to improve downstream performance.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 113,931
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 104,971
- Completion tokens: 11,476
- Reasoning tokens reported: 0
- Total tokens: 125,407
- Estimated total: $0.01793431

Full individual reviews and raw JSON responses are in `review_bundle.json`.
