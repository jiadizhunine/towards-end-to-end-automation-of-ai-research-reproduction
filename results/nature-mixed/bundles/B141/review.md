# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B141.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.015098**

## Final Meta-review

The paper proposes RoCA, a Gaussian Process (GP)-based framework for robust cross-domain end-to-end autonomous driving. RoCA learns a codebook of basis tokens representing diverse driving scenarios, each associated with trajectory prototypes. At inference, a GP kernel computes correlations between current scene tokens and basis tokens to probabilistically infer ego and agent trajectories, providing uncertainty estimates. These uncertainties are leveraged for variance-weighted training losses (source-domain regularization), GP-based trajectory prediction, and uncertainty-guided active learning during domain adaptation. The framework supports supervised and unsupervised adaptation, as well as online adaptation. Experiments on nuScenes demonstrate consistent improvements over base models (VAD-T, SparseDrive-S) in cross-city transfer, image degradation robustness, active learning efficiency, and long-tail scenario handling.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.400 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel application of Gaussian processes to end-to-end autonomous driving for cross-domain robustness, providing principled uncertainty estimation in an underexplored area.
- Comprehensive experimental evaluation covering cross-city transfer, image degradations, active learning, and long-tail scenarios, with consistent improvements over strong baselines (VAD-T, SparseDrive-S).
- Model-agnostic design that can be applied to any tokenized E2E planner, demonstrated with two different base models, increasing potential impact.
- Multiple practical operational modes: source-domain regularization (with no extra inference cost), GP-based trajectory prediction, supervised/unsupervised adaptation, active learning via predictive variance, and online adaptation.
- Uncertainty-guided active learning is a practical and well-motivated contribution for efficient domain adaptation.
- Clean ablation study demonstrating the contribution of each loss component.
- Clear qualitative results and practical analysis of computational costs.
- Well-written and well-structured presentation with helpful figures.

### Weaknesses

- The GP formulation is somewhat heuristic: basis tokens are learned embeddings rather than strict GP training points, and the kernel operates on learned token embeddings rather than input space, weakening theoretical justification. The approach essentially reduces to a sparse GP regression with learned inducing points, and the novelty lies mainly in the application rather than the technical method.
- The GP trajectory prediction is essentially a weighted average of basis trajectories, which may limit expressiveness for complex multi-modal maneuvers; the paper does not discuss how multi-modality is handled.
- Computational scalability of GP inference (matrix inversion and latency increase of ~25% in prediction mode) is only briefly addressed and not thoroughly analyzed for real-time deployment constraints.
- Evaluation is limited to nuScenes with only two cities (Boston and Singapore); no simulation (e.g., CARLA) or real-world validation, and no comparison with diverse sensor configurations or weather conditions beyond synthetic corruptions.
- No direct comparison with LLM-based driving approaches (e.g., DriveLM, EMMA) despite motivating the work with these methods in the introduction; comparison with VLP in the appendix uses different evaluation protocols, making it unreliable.
- Lack of hyperparameter sensitivity analysis (e.g., number of basis groups, group size, kernel parameters, triplet loss design).
- Missing details on the unsupervised adaptation setting: what prevents drift or collapse without ground-truth supervision, and what exactly is used as pseudo-labels (GP predictive mean?).
- The 'no extra inference computation' claim only holds for the regularization mode; the GP trajectory prediction mode does add latency.
- No ablation on the adaptation components (e.g., effect of uncertainty weighting during adaptation) and no online adaptation experiments despite being claimed as a contribution.
- Limited analysis of failure modes or conditions where the GP approach might underperform, and no evaluation of uncertainty calibration quality.

### Questions

- What is the theoretical justification for applying a GP kernel on learned token embeddings rather than the input space? How does this differ from a simpler nearest-neighbor or attention-based lookup mechanism?
- How are basis trajectories sampled and clustered initially? What clustering algorithm is used, and how sensitive are results to this initialization?
- In the unsupervised adaptation setting, what exactly is used as pseudo-ground-truth (GP predictive mean?), and what prevents the model from drifting or collapsing without ground-truth supervision? Are there additional regularization terms?
- How sensitive is performance to hyperparameters such as the number of basis groups (N_code=48/64) and group size (C=64)? Was any sensitivity analysis performed?
- What is the computational cost of kernel matrix inversion at inference time (C×C matrices), and how does it scale with larger codebooks? What is the memory overhead of storing the codebook (112 groups × 64 tokens)?
- How does the GP handle multi-modal trajectory distributions? The current formulation seems to predict a single trajectory per token.
- Can you provide a fair comparison with VLP using the standardized evaluation protocol? Why were no LLM-based driving methods (e.g., DriveLM, EMMA) compared, given they are discussed in the introduction?
- In the active learning experiments, how does predictive variance compare to other uncertainty-based sampling methods such as entropy or MC-dropout? How is variance computed (averaged over ego and agent tokens)?
- How does RoCA compare to simpler regularization techniques such as weight decay, dropout, or feature-level noise injection?
- The paper claims online adaptation support but does not present online adaptation experiments. Can you provide results or discussion on this capability?

### Limitations

- Evaluation is limited to nuScenes with only two cities; broader validation across more diverse domains (different countries, sensor configurations, weather conditions) or simulation environments (CARLA, Waymo) is needed to strengthen cross-domain claims.
- The computational overhead of GP inference (especially in trajectory prediction mode) may limit real-time deployment on embedded systems with strict latency requirements.
- The approach requires a three-stage training pipeline (base model training, GP training, finetuning), adding complexity for practical adoption.
- The method assumes tokenized representations are available from the base E2E model, which may not be the case for all E2E architectures, limiting general applicability.
- The uncertainty estimates from the GP may not be well-calibrated, and calibration quality is not evaluated, which could affect active learning and adaptation decisions.
- The paper does not discuss potential negative societal impacts of autonomous driving systems, including safety risks in deployment, over-reliance on automated systems, or biases in training data (e.g., geographic, demographic).
- No discussion of failure cases or safety-critical conditions where GP-based predictions might be unsafe despite high confidence or vice versa.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 98,122
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 89,162
- Completion tokens: 9,252
- Reasoning tokens reported: 0
- Total tokens: 107,374
- Estimated total: $0.01509833

Full individual reviews and raw JSON responses are in `review_bundle.json`.
