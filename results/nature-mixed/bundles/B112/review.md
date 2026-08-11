# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B112.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.017408**

## Final Meta-review

This paper presents 3DScenePrompt, a framework for scene-consistent camera-controllable video generation from arbitrary-length input videos. The key contribution is a dual spatio-temporal conditioning strategy that separates temporal continuity (using the last few frames) from spatial consistency (using a static-only 3D scene memory constructed via dynamic SLAM). The authors introduce a three-stage dynamic masking pipeline (pixel-level flow difference detection, CoTracker3 backward tracking, and SAM2 propagation) to extract static geometry while excluding dynamic elements. The static point cloud is projected to target viewpoints as spatial prompts, which are concatenated with temporal frames and fed into a fine-tuned CogVideoX-I2V-5B model. Extensive experiments on RealEstate10K, DynPose-100K, and DAVIS demonstrate significant improvements over existing baselines in scene consistency, camera controllability, and video quality.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 4.000 | 0.000 | 4-4 |
| Quality | 3 | 3.200 | 0.400 | 3-4 |
| Clarity | 3 | 3.400 | 0.490 | 3-4 |
| Significance | 4 | 4.000 | 0.000 | 4-4 |
| Soundness | 3 | 3.200 | 0.400 | 3-4 |
| Presentation | 3 | 3.400 | 0.490 | 3-4 |
| Contribution | 4 | 3.800 | 0.400 | 3-4 |
| Overall | 7 | 7.200 | 0.400 | 7-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel and well-motivated problem formulation: extending camera-controllable video generation to handle arbitrary-length input videos while maintaining scene consistency, which is clearly differentiated from single-frame or short-clip conditioning approaches
- Elegant dual spatio-temporal conditioning paradigm that rethinks the notion of adjacency in video, recognizing both temporal and spatial proximity, and addresses the memory bottleneck of processing long videos
- Comprehensive dynamic masking pipeline with three stages that is thoroughly ablated, showing each component's contribution to clean static geometry extraction
- Strong experimental results across multiple metrics and datasets, with significant improvements over baselines (e.g., 77% reduction in MEt3R error compared to DFoT)
- Modular design that allows swapping SLAM components (e.g., MegaSAM vs. DepthAnything v3) at inference time without retraining, demonstrating practical flexibility
- Minimal architectural changes to the base diffusion model, preserving pretrained video priors while enabling efficient fine-tuning (4K iterations, 48 hours on 4 H100s)
- Comprehensive ablations on key hyperparameters (number of spatial frames, temporal window size, dynamic masking stages)
- Clear writing with good contextualization of related work, including discussion of concurrent works

### Weaknesses

- Limited direct baseline comparison for scene consistency evaluation - only DFoT is compared quantitatively, while concurrent works like SPMem and WorldMem are acknowledged but not compared due to code unavailability
- Evaluation protocol for 'revisited viewpoints' is not clearly specified, and the potential for selection bias (e.g., only easy revisits) is not discussed
- High computational overhead with MegaSAM (~9 minutes total inference time), though the DepthAnything v3 replacement mitigates this
- The dynamic masking pipeline's robustness to challenging scenarios (fast-moving objects, severe occlusions, complex multi-object scenes) is not deeply analyzed
- The claim of 'arbitrary-length' input support is not fully validated - experiments primarily use videos of ~100 frames, and the long-video extension in the appendix shows error accumulation
- No perceptual user study is conducted; VBench++ is used as a proxy, but human evaluation of scene consistency would add confidence
- Training data is relatively small (50K videos) for fine-tuning a 5B parameter model, which may limit generalization
- Some architectural details are underspecified, such as the exact mechanism for concatenating temporal and spatial conditions

### Questions

- How are the 'revisited viewpoints' trajectories generated for the scene consistency evaluation? Is there any filtering or selection bias (e.g., only trajectories with sufficient overlap)?
- Have you considered comparing against SPMem or WorldMem quantitatively? Even without public code, could you provide a more detailed qualitative comparison or discuss expected performance differences?
- What are the failure modes of the dynamic masking pipeline? Could you provide examples where the mask fails (e.g., fast-moving objects, heavy occlusion, objects that move after appearing static) and how this affects generation quality?
- How does the method handle scenarios where the target camera trajectory explores regions far beyond the spatial coverage of the input video? Are there failure modes or artifacts in such extrapolation scenarios?
- How does the method perform when the input video has significant camera shake, low-quality frames, or lighting changes? Does the SLAM-based reconstruction degrade gracefully?
- In the long-video generation extension, how does error accumulation affect camera controllability over 180+ frames? Are there specific drift patterns observed?
- The ablation on the number of spatial frames n shows performance saturates around n=7. Could you explain why more spatial frames do not help further? Is there a trade-off between spatial context and computational cost?
- For the temporal window w=9, how were the 9 frames selected? Are they the last 9 consecutive frames, or are they subsampled? Does the choice affect motion continuity?
- How sensitive is the performance to the threshold τ in the pixel-level motion detection? What happens in failure cases where the masking fails to capture all dynamic content?
- How does the method compare to simply increasing the temporal window size w to cover more context? Could you quantify the memory/computation trade-off more concretely?

### Limitations

- The reliance on SLAM (MegaSAM) introduces computational overhead (~4 min per video), and while DepthAnything v3 reduces this, the dynamic masking stage still takes ~1 minute, which may be prohibitive for real-time applications
- The quality of dynamic masks directly affects generation fidelity; failures in mask estimation (e.g., for small or fast-moving objects, objects that move after appearing static) can degrade spatial conditioning
- Autoregressive long-video generation suffers from temporal error accumulation, which is acknowledged but not fully addressed
- The framework inherits limitations from the base model (CogVideoX), such as resolution and frame count constraints
- The method is evaluated on a limited set of datasets (RealEstate10K, DynPose-100K, DAVIS); generalization to diverse real-world scenarios (e.g., indoor scenes with complex lighting, outdoor scenes with weather effects) is not fully explored
- Potential negative societal impacts include misuse for generating misleading or deceptive video content, though this is common to all generative video models and not specifically addressed in the paper
- The computational cost of fine-tuning a 5B model may limit accessibility for researchers with fewer resources

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 110,282
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 101,322
- Completion tokens: 11,420
- Reasoning tokens reported: 0
- Total tokens: 121,702
- Estimated total: $0.01740777

Full individual reviews and raw JSON responses are in `review_bundle.json`.
