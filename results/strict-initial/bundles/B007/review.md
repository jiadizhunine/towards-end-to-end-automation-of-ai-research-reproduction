# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B007.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.022027**

## Final Meta-review

The paper introduces LEGO, a framework for learning generalizable robotic grasping from randomly assembled 'Cézanne toys' composed of four basic shape primitives (spheres, cuboids, cylinders, rings). The key technical contribution is DetPool, an object-centric visual representation that uses segmentation masks to restrict a ViT's attention to the target object and mean-pools object patches. Using behavior cloning with 250 simulated toy objects and 2,500 demonstrations (or 1,500 real demonstrations), the method achieves 67% zero-shot grasping success on 64 YCB objects in real-world Franka evaluations, outperforming large VLA baselines (zero-shot) while using much less data and compute. Ablations show the importance of DetPool, and scaling analyses reveal the relationship between performance and data/toy diversity.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 3 | 2.800 | 0.400 | 2-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 2.800 | 0.400 | 2-3 |
| Presentation | 3 | 2.800 | 0.400 | 2-3 |
| Contribution | 3 | 2.800 | 0.400 | 2-3 |
| Overall | 6 | 5.600 | 0.800 | 4-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The idea of training grasping policies on random compositions of simple shape primitives is novel and well-motivated by cognitive science, providing a principled way to generate out-of-distribution training data.
- DetPool is a simple and effective mechanism: ablations show substantial gains (22–48% in simulation) over standard mean/CLS/attention pooling, highlighting the value of object-centric representations.
- The method achieves strong zero-shot generalization to unseen YCB objects in both simulation and real-world experiments, despite being trained on only 1,500 demonstrations and 86M parameters, outperforming much larger VLA baselines that use substantially more pretraining data.
- The paper validates the approach on two robot embodiments (Franka with a gripper and Unitree H1-2 with dexterous hands), demonstrating practical generalizability.
- The systematic scaling studies provide useful insights: demonstrations matter more than toy diversity, the sphere primitive is most critical, and model size saturates at ViT-B.

### Weaknesses

- The claim of 'outperforming state-of-the-art approaches' is overstated: in the real Franka experiment, finetuned π0-FAST achieves 76.56% success while LEGO achieves 66.67%; LEGO only outperforms zero-shot baselines, not the strongest finetuned baseline.
- DetPool relies on an external object mask at inference time, which is a privileged source of information not available to baselines; the mask detector is trained on only 200 toy images, and no analysis of mask quality or robustness is provided, making the comparison with VLA baselines unfair and limiting practical applicability.
- Simulation baseline comparisons may be unfair: the success threshold is lowered from 0.3m to 0.15m for OpenVLA-OFT, and LEGO uses ground-truth masks while baselines do not; this conflates the effect of DetPool with privileged object segmentation.
- The evaluation lacks statistical rigor: no confidence intervals, no multiple seeds, and no significance tests are reported; the H1-2 results use only 5 trials per object and are further compromised by malfunctioning thumb joints.
- Several technical details are ambiguous, including whether the attention mask is applied at every ViT layer, how the real-world mask detector generalizes to YCB objects, and the exact training setups for baselines in Table 2.
- The scaling experiment is unclear about whether total demonstrations are held constant across toy counts, which affects the interpretation of toy-diversity effects.

### Questions

- How does LEGO's performance vary with the quality of the segmentation mask? What is the detection accuracy of the Faster R-CNN detector on YCB objects, and how does mask noise impact grasping success?
- Why was the success threshold lowered from 0.3m to 0.15m for OpenVLA-OFT in simulation? How does the comparison change if a uniform threshold is used for all baselines?
- Could the authors report confidence intervals or standard errors for the success rates, especially for the H1-2 experiments with only 5 trials per object?
- How does LEGO compare to finetuned π0-FAST at the same demonstration count as LEGO's 1,500 demos? The paper reports finetuned π0-FAST at 1,500 demos but LEGO only outperforms zero-shot versions.
- Does DetPool's benefit come primarily from attention masking or from object-centric mean-pooling? A baseline that uses global attention with the same object-centric pooling would clarify this.
- What is the effect of using only the two tabletop cameras versus adding a wrist camera, which baselines used? Could LEGO improve with additional camera views?

### Limitations

- The method requires an accurate object segmentation mask at inference, which may be difficult to obtain in cluttered or dynamic scenes; this dependency is not included in the model parameter count or training pipeline.
- The training and evaluation focus on rigid objects composed of basic primitives; generalization to deformable, articulated, transparent, or highly textured objects is not demonstrated.
- The policy is limited to single-step tabletop grasping of one object at a time; long-horizon manipulation, multi-object scenes, and dynamic grasping are not addressed.
- Real-world evaluations are limited in scale: 64 YCB objects on a Franka (with a fixed grid placement) and 13 everyday objects on H1-2 with only 5 trials per object, and hardware issues with the dexterous hands reduce reliability.
- The paper does not provide failure analysis or error decomposition, so it is unclear whether failures stem from perception, representation, policy learning, or control.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 112,023
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 107,927
- Completion tokens: 24,664
- Reasoning tokens reported: 17,649
- Total tokens: 136,687
- Estimated total: $0.02202717

Full individual reviews and raw JSON responses are in `review_bundle.json`.
