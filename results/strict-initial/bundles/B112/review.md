# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B112.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 1, 'Reject': 4}
- Estimated API cost: **$0.015086**

## Final Meta-review

The paper proposes 3DScenePrompt, a framework for generating future video chunks from an arbitrary-length input video with camera control. It introduces dual spatio-temporal conditioning: temporal frames for motion continuity and spatial conditioning from a static-only 3D scene memory constructed via dynamic SLAM and a dynamic masking pipeline. The static point cloud is projected to target viewpoints as guidance. The model is built on CogVideoX and fine-tuned on RealEstate10K and OpenVid-1M, with evaluations on RealEstate10K and DynPose-100K showing improvements over baselines such as DFoT in scene consistency, camera controllability, and video quality.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 2.800 | 0.400 | 2-3 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 1 | 1.800 | 0.400 | 1-2 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 2 | 2.400 | 0.490 | 2-3 |
| Presentation | 2 | 1.800 | 0.400 | 1-2 |
| Contribution | 2 | 2.600 | 0.490 | 2-3 |
| Overall | 4 | 4.200 | 0.400 | 4-5 |
| Confidence | 4 | 3.600 | 0.490 | 3-4 |

### Strengths

- The dual spatio-temporal conditioning is a conceptually effective way to preserve long-range scene consistency without conditioning on all input frames.
- The static-only 3D scene memory via dynamic SLAM and dynamic masking is a principled solution to avoid freezing dynamic content, and the ablation confirms its importance.
- The method shows consistent quantitative improvements over DFoT and other baselines, particularly in geometric consistency (MEt3R).
- The framework minimally modifies a strong pretrained video generator (CogVideoX), leveraging its prior and limiting training cost.
- The dynamic masking pipeline is a practical multi-stage approach to separate static and dynamic content.

### Weaknesses

- The paper contains severe redactions and incomplete equations, which impede reproducibility and full comprehension.
- The evaluation lacks comparisons to closely related geometry-grounded video generation methods (e.g., Gen3C, TrajectoryCrafter, ReCamMaster, StarGen).
- The baseline comparison may be unfair: methods conditioned on a single image are compared to 3DScenePrompt, which uses 9 frames and camera information.
- The claim of handling arbitrary-length input video is not fully supported; the method uses only a fixed window of recent frames and top spatially adjacent views, with no analysis of scaling behavior.
- The dependence on multiple off-the-shelf components (SLAM, optical flow, SAM2, CoTracker3) is not analyzed for robustness, failure modes, or computational overhead.
- The technical details of how the conditioning is injected into CogVideoX's image-conditioning channel are unclear, as CogVideoX-I2V expects a single image latent.
- Only 4K fine-tuning iterations are reported; no convergence or hyperparameter sensitivity analysis is provided.

### Questions

- How are the target camera poses provided to the model? Are they used only for projecting the point cloud, or also directly conditioned into the network?
- How does the method handle target viewpoints that observe regions not covered by the static point cloud (e.g., holes, extrapolation)? What mechanisms prevent degraded generation?
- What is the computational cost of the SLAM reconstruction and dynamic masking relative to generation time, and how does the pipeline scale with input video length?
- What are the exact hyperparameters (e.g., threshold tau in dynamic masking) and how were they selected? What is the sensitivity of results to these choices?
- Why are recent geometry-grounded video generation methods (Gen3C, TrajectoryCrafter, ReCamMaster) not included in the quantitative comparison?
- How are the 'revisited viewpoints' for spatial consistency evaluation computed, and how many such pairs are used per video?

### Limitations

- The method requires offline processing of the entire input video for SLAM and dynamic masking, which limits applicability to streaming or very long sequences.
- The static scene memory assumes all non-masked content is static; lighting changes, deformable objects, or objects that stop moving may violate this and cause artifacts.
- The projected static point cloud is sparse and may contain holes, especially for novel camera trajectories, yet the paper does not discuss inpainting or handling of occlusion boundaries.
- The method is evaluated only on RealEstate10K and DynPose-100K; generalizability to diverse real-world scenarios is not demonstrated.
- The framework relies on off-the-shelf components that can fail, and no failure cases or sensitivity analysis are provided.
- Potential negative societal impact, such as misuse of camera-controllable video generation for disinformation, is not addressed.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 70,556
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 66,460
- Completion tokens: 20,609
- Reasoning tokens reported: 14,292
- Total tokens: 91,165
- Estimated total: $0.01508639

Full individual reviews and raw JSON responses are in `review_bundle.json`.
