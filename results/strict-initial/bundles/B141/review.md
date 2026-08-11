# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B141.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.019309**

## Final Meta-review

The paper proposes RoCA, a Gaussian process (GP)-based framework for robust cross-domain end-to-end autonomous driving. RoCA learns a codebook of basis tokens and associated trajectories, enabling probabilistic inference of ego/agent tokens and future trajectories. It uses GP uncertainty for loss weighting and active learning, and can be applied on top of existing token-based E2E planners. Evaluations on nuScenes demonstrate improvements in same-domain, cross-city, degraded-image, long-tail, and active-learning settings over VAD-T and SparseDrive-S baselines.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.000 | 0.000 | 2-2 |
| Clarity | 2 | 1.800 | 0.400 | 1-2 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 2 | 2.000 | 0.000 | 2-2 |
| Presentation | 2 | 1.800 | 0.400 | 1-2 |
| Contribution | 3 | 2.600 | 0.490 | 2-3 |
| Overall | 4 | 4.000 | 0.000 | 4-4 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Addresses a timely and important problem: cross-domain generalization and adaptation for end-to-end autonomous driving.
- Novel idea of combining a learned codebook of trajectory basis tokens with Gaussian-process-based uncertainty estimation, avoiding LLM-based costly adaptation.
- Practical, modular framework that can be applied to multiple token-based E2E planners; regularization mode adds no inference cost.
- Explores multiple adaptation settings (supervised, unsupervised, active learning) and shows consistent improvements over strong baselines across a range of scenarios (cross-city, image degradations, long-tail).
- Uncertainty-based active learning selection consistently outperforms random sampling.
- Ablation studies and latency/parameter analysis are provided.

### Weaknesses

- The GP formulation is mathematically questionable and not rigorously derived: equations mix joint distributions over tokens and trajectories, omit noise terms, and confuse covariance and precision; the predictive mean resembles kernel smoothing more than standard GP regression.
- Many implementation details are missing: how basis groups are chosen/clustered, how the classification MLP is trained, how triplet positive/negative classes are selected, how scalar variances weight vector losses, and how hyperparameters (e.g., number of groups, jitter) are set—this hinders reproducibility.
- Evaluation is limited to the nuScenes dataset (two cities) and open-loop metrics; no cross-dataset transfer (e.g., Waymo, CARLA) or closed-loop validation is provided, weakening cross-domain claims.
- The claimed online adaptation capability is never experimentally evaluated.
- No statistical significance tests or error bars are reported; some improvement margins are small and may not be reliable.
- Comparisons to existing domain adaptation or uncertainty-based methods are insufficient; the only direct comparison (VLP) appears in the appendix under a different protocol.
- The GP-based trajectory prediction mode, which yields the best results, adds non-trivial inference latency (16-34 ms) and parameters, contradicting the emphasis on no-extra-cost regularization.
- Several typos and unclear notations throughout the paper further impede clarity and reproducibility.

### Questions

- What is the exact probabilistic model in Eq. (1)? Are e and B jointly Gaussian random variables, and how are the GP input/output dimensions defined? Is there a principled derivation from GP regression?
- How are the basis trajectories sampled and clustered? Are they from the source city only in cross-city experiments to avoid target-domain data leakage?
- How is the classification MLP that maps kernel distances to group probabilities trained, and is it jointly optimized with basis tokens?
- How are positive and negative classes for the triplet loss determined, and are they fixed during training?
- Why does the variance weighting in Eq. (5) down-weight high-variance samples when the paper claims it emphasizes uncertain predictions?
- Are the improvements in Tables 1-4 statistically significant (e.g., across multiple seeds)?
- In unsupervised adaptation, how are pseudo-labels generated, and what prevents overfitting to the GP teacher?
- How does RoCA's active learning compare to other acquisition functions (e.g., entropy, MC dropout)?
- Can the method generalize to non-token-based planners or to datasets with fundamentally different trajectory distributions?

### Limitations

- The method requires explicit ego/agent tokens from the base E2E model, limiting applicability to models without such representations.
- The codebook is built from source-domain trajectories; if target domains exhibit novel maneuvers or traffic patterns, the GP may fail without codebook adaptation, which is not explored.
- The multi-stage training pipeline is computationally expensive (~37 hours on 2 A100s) and has many hyperparameters, which may reduce practical adoption.
- The uncertainty estimates are not calibrated, and their quality or downstream safety impact is not assessed.
- Evaluation is restricted to open-loop planning on nuScenes; no closed-loop or safety-critical metrics (e.g., comfort, collisions) are reported.
- Potential safety implications of deploying uncertain models in autonomous driving are not discussed.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 90,190
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 86,094
- Completion tokens: 25,873
- Reasoning tokens reported: 19,709
- Total tokens: 116,063
- Estimated total: $0.01930907

Full individual reviews and raw JSON responses are in `review_bundle.json`.
