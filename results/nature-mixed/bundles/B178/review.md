# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B178.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.017423**

## Final Meta-review

The paper proposes a score-based diffusion model for unconditional human motion and shape generation using SMPL parameters. It introduces three main contributions: (1) structure-preserving feature normalization for SMPL rotations using expected magnitude instead of z-score, (2) a theoretically motivated re-weighting of the L2 score-matching loss based on gradient analysis of uncertainty weighting, and (3) per-feature-group uncertainty weighting combined with dimensionality balancing via magnitude-preserving concatenation. The method builds on EDM/EDM2, generates SMPL parameters directly (including shape), avoids auxiliary losses, and maintains PF-ODE compatibility for likelihood computation and deterministic sampling. Ablations show each component improves performance, and the model achieves results comparable to MDM and MLD with only 31 NFEs.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 3.200 | 0.400 | 3-4 |
| Clarity | 3 | 3.200 | 0.400 | 3-4 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 3 | 3.200 | 0.400 | 3-4 |
| Presentation | 3 | 3.200 | 0.400 | 3-4 |
| Contribution | 3 | 2.800 | 0.400 | 2-3 |
| Overall | 6 | 6.200 | 0.748 | 5-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Clear theoretical motivation for each design choice, grounded in EDM/EDM2 framework analysis with detailed derivations in appendices.
- Systematic cumulative ablations (Table 1) demonstrating each component's contribution to performance improvement.
- Direct SMPL parameter generation including shape, avoiding slow and error-prone post-hoc shape recovery from joints.
- PF-ODE compatibility enables tractable likelihood computation and deterministic sampling, which is lost with auxiliary losses.
- Efficient sampling with only 31 NFEs compared to 1000 for MDM.
- Novel gradient analysis identifying a flaw in the original EDM2 uncertainty weighting, leading to an improved weighting scheme.
- Structure-preserving normalization for rotations that respects the geometric properties of rotation representations.
- Good evaluation with multiple complementary metrics (FID, Diversity, Foot skating, Limb σ) and honest discussion of limitations.
- Good reproducibility with hyperparameters, pseudo-code, and network implementation in the appendix.

### Weaknesses

- Limited comparison set: only MDM and MLD are compared, missing more recent and potentially stronger baselines (e.g., MotionDiffuse, PhysDiff, or 2024-2025 methods).
- FID score of 1.81 is worse than MLD's 1.17, making the 'on par with state-of-the-art' claim somewhat overstated.
- Foot skating metric for the SMPL-parameterized model (16.31%) is notably worse than MDM (8.58%) and the root-relative variant (7.97%), indicating a trade-off between FID and physical quality.
- The paper only addresses unconditional generation, limiting practical applicability compared to conditional methods (text-to-motion, action-to-motion).
- Ablations are cumulative only; the individual contribution of each component in isolation is not fully disentangled.
- Evaluation uses only one dataset (AMASS subset from HumanML3D), limiting generalizability claims.
- The baseline FID of 6.23 in ablations seems high, potentially inflating the apparent benefit of the proposed components.
- No comparison with methods that also generate shape directly, making it hard to assess shape generation quality.
- Best-of-3-runs evaluation protocol may inflate reported metrics compared to mean ± std reporting.

### Questions

- Why were only MDM and MLD chosen for comparison? Can you provide comparisons with more recent state-of-the-art methods such as MotionDiffuse, PhysDiff, or other 2024-2025 approaches?
- The FID score of MLD (1.17) is notably better than your SMPL model (1.81). How do you reconcile the claim of 'on par with state-of-the-art' with this gap?
- The ablations are cumulative. Could you provide results for each component in isolation (e.g., only input normalization, only gradient-based weighting, only per-group weighting, only dimensionality balancing) to better isolate each contribution?
- How does the method perform on conditional generation tasks (e.g., text-to-motion)? The paper claims the principles could extend, but no experiments are shown.
- What is the training computational cost (e.g., GPU hours) compared to MDM and MLD?
- The foot skating metric is notably worse for the SMPL-parameterized model. Could this be addressed by adding foot-contact-related features without violating the minimal representation philosophy?
- How sensitive are the results to hyperparameters like P_mean, P_std, and the cosine decay learning rate schedule? Were these tuned specifically for the motion domain?
- The paper reports best-of-3-runs metrics. Would the conclusions change if mean ± std were reported instead?
- How does the generated shape distribution compare to the training distribution? Are there any artifacts in the generated shapes?
- Have you considered evaluating on other datasets (e.g., HumanAct12, BABEL) to demonstrate generalizability?

### Limitations

- Foot skating remains a significant issue for the SMPL-parameterized model, suggesting some auxiliary information (like foot contact) may still be valuable.
- Self-intersections in generated meshes are occasionally observed, though present in the training data as well.
- Stair-walking motions do not always maintain height after upward steps, indicating limitations in modeling vertical translation in non-flat environments.
- The method is only evaluated on unconditional generation; the claimed applicability to conditional tasks is not demonstrated.
- The comparison set is limited to two prior methods, potentially missing stronger or more recent baselines.
- The best-of-3-runs evaluation protocol may not reflect typical expected performance.
- Potential negative societal impact: Human motion generation could be used for creating deepfakes or misleading content, though the paper does not discuss this explicitly.
- The paper does not address potential biases in the training data (e.g., AMASS may not represent diverse body shapes or motion styles across populations).

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 113,684
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 104,724
- Completion tokens: 9,774
- Reasoning tokens reported: 0
- Total tokens: 123,458
- Estimated total: $0.01742317

Full individual reviews and raw JSON responses are in `review_bundle.json`.
