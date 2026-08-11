# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B007.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.021850**

## Final Meta-review

This paper introduces LEGO (LEarning to Grasp from tOys), a framework for learning generalizable robotic grasping by training exclusively on procedurally generated 'Cézanne toys' composed of four basic shape primitives (spheres, cuboids, cylinders, rings). The key technical contribution is DetPool (detection pooling), an object-centric visual representation mechanism that uses segmentation masks (SAM 2 in real-world, ground truth in simulation) to constrain attention in a vision transformer to object patches and applies mean pooling. The method is evaluated on zero-shot grasping of YCB objects in simulation (ManiSkill) and on two real embodiments (Franka with gripper, Unitree H1-2 with dexterous hands), achieving 80% success in simulation and 67% on the real Franka with only 1,500 demonstrations, outperforming larger VLA baselines (π0-FAST, OpenVLA-OFT) that use substantially more pretraining data. The paper also provides extensive scaling studies, ablations on primitive importance, toy complexity, model size, and robustness analyses under lighting, clutter, distractors, and mask noise. The central claim is that object-centric representations induced by DetPool are key to enabling zero-shot generalization from simple synthetic toys to real-world objects.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 4.000 | 0.000 | 4-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 4 | 3.600 | 0.490 | 3-4 |
| Significance | 4 | 3.600 | 0.490 | 3-4 |
| Soundness | 3 | 3.200 | 0.400 | 3-4 |
| Presentation | 4 | 3.600 | 0.490 | 3-4 |
| Contribution | 4 | 3.600 | 0.490 | 3-4 |
| Overall | 7 | 6.600 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel and well-motivated problem framing: training on simple primitive-based toys to achieve generalization is elegantly justified by cognitive science literature on infant learning, providing a principled alternative to large-scale data collection.
- DetPool is a simple, clean, and effective technical contribution, with clear ablation evidence showing substantial improvements (22-48%) over standard pooling baselines (mean, CLS, attention pooling).
- Comprehensive evaluation across multiple settings: ManiSkill simulation, real Franka robot with gripper, and Unitree H1-2 humanoid with dexterous hands, demonstrating the approach's generality across embodiments.
- Thorough scaling studies (number of toys, demonstrations, model size) and robustness analyses (lighting, clutter, distractors, mask noise) provide deep insights into the method's behavior and data efficiency.
- Strong empirical results: 80% success in simulation and 67% on real YCB objects with only 1,500 demonstrations, outperforming much larger pretrained VLA models in the zero-shot setting.
- The paper is well-written, clearly organized, and includes detailed implementation details (3D printing, teleoperation, evaluation protocols) that support reproducibility.
- The authors are transparent about limitations (hardware issues with H1-2 hands, single-step grasping focus) and provide honest discussion of failure modes.
- Practical contributions including the 3D printed toy dataset, code, and checkpoints will be valuable to the community.

### Weaknesses

- The headline claim of 'outperforming state-of-the-art' is weakened by the fact that finetuned π0-FAST achieves higher real-world success on the Franka (76.56% vs 66.67%). While the authors provide a reasonable explanation, this undermines the strongest version of the claim.
- The comparison with VLA baselines (π0-FAST, OpenVLA-OFT) may be somewhat unfair, as these are general-purpose models not specifically optimized for grasping with limited data, and their extremely low simulation performance (4-9%) for π0-FAST raises questions about fine-tuning configuration or implementation details.
- The method relies on SAM 2 (or a trained detector) at test time for object segmentation, which adds an external dependency and computational overhead. Robustness to mask noise is only tested in simulation, not in real-world settings.
- The evaluation is limited to single-step grasping (with a push task only in the appendix); the claim of 'generalizable manipulation' is therefore somewhat narrow, and extension to long-horizon tasks is not demonstrated.
- No comparison against dedicated zero-shot grasping methods (e.g., GraspNet, Contact-GraspNet) that are standard in the grasping literature, which would provide a more direct benchmark for the grasping task.
- Failure case analysis is missing; the paper does not characterize which object types fail and why, which would strengthen understanding of the method's limitations.
- The H1-2 experiments were constrained by hardware issues (unresponsive thumb joints) and limited trials (5 per object), potentially affecting the reliability of those results.
- No statistical significance or confidence intervals are reported for real-world evaluations, and the number of trials per object is not clearly specified.

### Questions

- The finetuned π0-FAST outperforms LEGO on the real Franka (76.56% vs 66.67%). Could you elaborate on the specific factors contributing to this advantage (pretrained knowledge, in-domain DROID data, fine-tuning approach)? Would combining LEGO's DetPool with π0-FAST's architecture yield further improvements?
- The simulation results for π0-FAST are extremely low (4-9%). Could you provide more details on the fine-tuning process (learning rate, number of steps, checkpoint selection) and verify there is no bug in action space mapping or observation format?
- Could you compare against dedicated grasping methods (e.g., GraspNet, Contact-GraspNet) on the YCB benchmark to provide a more direct baseline for the grasping task?
- How is the target object specified for SAM 2 at test time? Is it manually selected or automatic? How robust is the full pipeline to SAM 2 failures (incorrect segmentation, missed detections) in real-world deployment?
- What is the failure mode distribution? For example, what percentage of failures are due to incorrect grasp pose selection vs. execution errors vs. object slipping? Are there specific YCB object categories where LEGO consistently fails?
- How does the method perform on objects with different physical properties (deformable, transparent, reflective, very small/large)? Are there known limitations?
- The scaling study shows diminishing returns with more toys. Could you provide a more quantitative analysis (fitting a curve, identifying saturation point) to guide practitioners on how many toys are needed?
- In the H1-2 experiments, how many trials were affected by the thumb joint issues, and would you consider the 50.77% success rate reliable? How would results change with fully functional hands?
- How sensitive is the method to the choice of the four primitives? Would other primitives (cones, toruses) improve or degrade performance? Is there a principled way to select primitives?
- Could the DetPool mechanism be integrated into existing VLA models (OpenVLA, π0) to improve their object-level generalization?
- What is the inference time of the full pipeline including SAM 2 mask generation compared to baselines?
- Is the vision encoder (MVP) frozen or fine-tuned during training? Does DetPool work with other vision encoders (CLIP, DINOv2)?

### Limitations

- The method is demonstrated primarily on rigid objects; performance on deformable, transparent, or articulated objects is unknown.
- The reliance on SAM 2 for real-world masks adds a complex external dependency that may not be available in all deployment scenarios and adds computational overhead.
- The approach is currently limited to single-step grasping; extension to long-horizon manipulation tasks is left for future work.
- The evaluation is limited to the YCB benchmark and a small set of everyday objects; broader generalization to more diverse real-world scenarios is not demonstrated.
- The computational cost of the model, although smaller than VLA baselines, may still be prohibitive for resource-constrained robots.
- The paper does not discuss potential negative societal impacts (e.g., automation displacing workers in manufacturing/logistics, safety in human-robot interaction).
- The environmental impact of 3D printing 250 toys is not addressed.
- The paper does not discuss the potential for overfitting to the YCB evaluation set despite OOD training data.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 140,083
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 131,123
- Completion tokens: 12,384
- Reasoning tokens reported: 0
- Total tokens: 152,467
- Estimated total: $0.02184983

Full individual reviews and raw JSON responses are in `review_bundle.json`.
