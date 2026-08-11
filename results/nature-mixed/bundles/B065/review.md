# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B065.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.019374**

## Final Meta-review

DexMan is an automated framework that converts monocular RGB videos of human bimanual manipulation into bimanual dexterous robot skills for humanoid robots in simulation. The pipeline consists of four stages: (1) 3D object reconstruction using SAM2 and Trellis, (2) hand and object pose estimation using HaMeR, VGGT, FoundationPose, and SpatialTracker with trajectory regularization, (3) motion retargeting from human to a Unitree G1 humanoid with Shadow Hands using staged IK solvers, and (4) residual RL policy training guided by a novel contact-prior attraction reward that establishes correspondence between hand keypoints and object surface vertices. The framework requires no ground-truth annotations, camera calibration, depth sensors, or 3D object assets. The authors evaluate on TACO for pose estimation, OakInk-v2 for RL policy performance, and both real and synthetic (Veo3) videos for end-to-end skill acquisition, achieving state-of-the-art results on the first two benchmarks and demonstrating the first end-to-end pipeline from uncalibrated monocular RGB inputs for bimanual humanoid manipulation.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 3.000 | 0.632 | 2-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.000 | 0.632 | 2-4 |
| Overall | 6 | 6.000 | 0.632 | 5-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important and timely problem: scaling dexterous manipulation skill acquisition from readily available human videos without expensive motion capture, depth sensors, or manual annotation.
- The contact-prior attraction reward is a novel and well-motivated contribution that provides object-centric correspondence rather than simple proximity or world-space matching, addressing known limitations in prior work like MANIPTRANS and DexMachina.
- The pipeline is complete and well-engineered, handling practical challenges such as unstable reconstructed meshes, depth scale inconsistencies, and noisy pose estimates from in-the-wild videos.
- The use of point trajectories (SpatialTracker) to regularize FoundationPose is a simple yet effective insight that improves temporal consistency and robustness.
- Demonstrates the first framework capable of transferring from both real and synthetic (Veo3) videos, suggesting potential for large-scale data generation.
- Comprehensive evaluation across three settings: pose estimation, benchmark RL, and end-to-end video-to-robot acquisition.
- The paper is generally well-written with clear organization, and the authors are transparent about limitations and failure cases.
- Full humanoid control (not just floating hands) is a more realistic and challenging setting than prior work.

### Weaknesses

- The success rates on real videos are quite low (27.4% on TACO), raising questions about the practical utility of the approach. While the framework works, the high failure rate limits its immediate applicability.
- The comparison with MANIPTRANS on OakInk-v2 may not be entirely fair. DexMan controls a full humanoid robot while MANIPTRANS uses simplified floating hands, making the comparison apples-to-oranges. The paper acknowledges this but doesn't provide a controlled comparison with the same embodiment.
- The evaluation is entirely in simulation with no sim-to-real validation. Given the authors' claims about scalability and practical utility, this is a significant gap.
- The 'no ground-truth' claim for TACO is somewhat misleading. While DexMan doesn't use ground-truth annotations directly, TACO videos are derived from motion capture with clean, controlled scenes (fixed camera, good lighting, minimal occlusion), which may not represent truly in-the-wild conditions.
- The ablation study doesn't fully isolate the key novelty of the contact reward (object-centric correspondence) against simpler baselines. For example, comparing against a reward that simply encourages touching the nearest object surface would better demonstrate the value of the correspondence mechanism.
- The paper doesn't compare against other recent video-to-robot pipelines (e.g., OKAMI, DexMachina) in the end-to-end setting, citing that DexMan is the first to do this. While this may be true, providing comparisons on the OakInk-v2 benchmark with other methods using the same embodiment would strengthen the claims.
- The selection of only 50 TACO sequences from 244 is not justified, and no analysis is provided on how these were chosen, introducing potential selection bias.
- The contact reward has a known failure mode (demonstrated in the shoe-picking case) where it converges to incorrect contact surfaces, suggesting the reward is not fully robust to object geometry.
- The reward design includes many hyperparameters without sensitivity analysis, raising questions about robustness and generalizability.

### Questions

- Could you provide a comparison with MANIPTRANS using the same robot embodiment (e.g., floating hands) to isolate the benefit of the full humanoid setup? This would clarify whether the 19% improvement is due to the contact reward or the embodiment choice.
- In the ablation study, have you considered comparing your contact reward against a simpler baseline that rewards proximity to the nearest object surface (similar to MANIPTRANS but with your other rewards)? This would better isolate the value of the object-centric correspondence.
- The success rates on TACO (27.4%) are notably lower than on synthetic videos (39.0%). Could you analyze why real videos are harder, and what specific failure modes dominate?
- How sensitive is the pipeline to the quality of the reconstructed 3D mesh? Have you tested with higher-quality meshes (e.g., from depth sensors or CAD models) to understand the bottleneck?
- The paper uses state-based RL with no visual observations. How would the approach extend to vision-based policies, which would be necessary for real-world deployment?
- What is the computational cost of the full pipeline (pose estimation, retargeting, RL training) per video? This is important for assessing scalability to large-scale datasets.
- The contact reward uses fixed thresholds for keypoint-vertex distances. How sensitive are the results to these thresholds? Have you tried adaptive or learned thresholds?
- How were the 50 TACO sequences selected from the 244 available? Was there any filtering based on task difficulty or video quality?
- In the OakInk-v2 comparison, does MANIPTRANS use the same evaluation protocol (entire episode vs intermediate frames)? This could significantly affect the reported success rates.
- How does the performance on OakInk-v2 change if you use the estimated poses from your video pipeline instead of ground-truth annotations? This would provide a more consistent evaluation of the full pipeline.
- How robust is the object pose estimation when the object is heavily occluded by hands during manipulation?
- The contact reward extracts contact priors offline from estimated hand poses. How sensitive is the final performance to errors in hand pose estimation?
- What is the sensitivity of the contact reward to the hyperparameters τ_j, λ_c, and the keypoint weights? Have you performed any sensitivity analysis?

### Limitations

- The framework is evaluated only in simulation; the substantial sim-to-real gap is acknowledged but not addressed.
- The system assumes single-human demonstrations with rigid tabletop objects, excluding deformable or articulated objects common in real-world tasks.
- The end-effector control parameterization ignores full arm posture, which is important for collision avoidance and coordinated multi-arm manipulation.
- The sequential pose estimation pipeline (hand and object separately) may compromise contact reasoning consistency.
- The current success rates (27-39%) are low, limiting practical applicability.
- The system prioritizes task completion over motion naturalness, resulting in robot trajectories that deviate from human movements.
- The use of synthetic videos (Veo3) introduces potential biases and physical inconsistencies that are not fully addressed.
- Potential negative societal impact: the technology could be used for surveillance or unauthorized replication of human manipulation skills, though this is speculative and not a major concern.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 123,921
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 114,961
- Completion tokens: 11,622
- Reasoning tokens reported: 0
- Total tokens: 135,543
- Estimated total: $0.01937379

Full individual reviews and raw JSON responses are in `review_bundle.json`.
