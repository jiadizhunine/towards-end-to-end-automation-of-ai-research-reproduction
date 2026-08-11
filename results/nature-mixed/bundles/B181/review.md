# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B181.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 1, 'Reject': 4}
- Estimated API cost: **$0.022453**

## Final Meta-review

The paper proposes OFMU, a penalty-based bi-level optimization framework for machine unlearning. It formulates unlearning as a hierarchical optimization problem where the inner loop maximizes the forget-set loss with a similarity-aware penalty to decorrelate forget and retain gradients, and the outer loop minimizes the retain-set loss to preserve utility. A two-loop algorithm with a penalty-based reformulation is developed, and convergence guarantees are provided for both convex and non-convex settings. The method is evaluated on TOFU, WMDP, CIFAR-10, and CIFAR-100 across multiple architectures (LLaMA-2-7B, LLaMA-3.2-1B, Zephyr-7B, ResNet), with comparisons to gradient ascent, NPO, RMU, and other baselines. The paper includes ablations, robustness analyses, and a computational complexity study.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 3 | 2.800 | 0.400 | 2-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 2 | 2.200 | 0.400 | 2-3 |
| Presentation | 3 | 2.800 | 0.400 | 2-3 |
| Contribution | 2 | 2.400 | 0.490 | 2-3 |
| Overall | 4 | 4.400 | 0.800 | 4-6 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Addresses an important and timely problem in machine unlearning for large language models.
- The bi-level optimization formulation is conceptually well-motivated and explicitly prioritizes forgetting over utility, addressing limitations of scalarized multi-objective approaches.
- The similarity-aware penalty for gradient decorrelation is a novel mechanism to mitigate destructive interference between forgetting and retention objectives.
- Provides convergence analysis in both convex and non-convex settings, which is relatively rare in the unlearning literature.
- Comprehensive empirical evaluation across multiple benchmarks, model architectures, and forgetting scenarios (class-wise, random, hard in-scope).
- Includes useful ablations, hyperparameter sensitivity analyses, and robustness checks that strengthen the empirical claims.

### Weaknesses

- The theoretical analysis is not rigorous. Lemma 1's proof is hand-wavy and appears to assume the conclusion. The non-convex convergence bound (equation 35) contains a constant term (2G^2_r) that does not vanish as iterations increase, undermining the claimed convergence to a stationary point. The convex case analysis also has unclear dependencies and potential inconsistencies.
- Empirical gains over strong baselines are modest in several settings (e.g., WMDP improvements of only 1-2 points over RMU, FQ differences of 0.04-0.08 on TOFU). The claim of state-of-the-art performance is not convincingly demonstrated.
- The computational overhead is significant (2.85x-4.22x runtime compared to gradient ascent), and this cost is not adequately justified by the relatively small improvements.
- Missing comparisons with recent state-of-the-art unlearning methods (e.g., RULE, UNDIAL, KL-divergence-based approaches) that are cited in related work but not included in experiments.
- The evaluation methodology has issues: the overall performance score normalization by maximum across methods can be misleading when metrics have vastly different scales (e.g., FQ values ranging from 1e-239 to 1.0). Some results appear inconsistent (e.g., Retrain achieving 100% Retain Accuracy on CIFAR-10 random forgetting, and MIA-Efficacy values differing dramatically between scenarios).
- The relationship between the penalty-based reformulation and the actual two-loop algorithm is not rigorously established. Convergence to a stationary point of the penalty objective does not necessarily correspond to solving the original bi-level problem.
- The inner objective includes a cosine similarity term involving gradients, which introduces second-order derivatives (Hessians). The paper does not adequately address the computational feasibility and theoretical treatment of this term for large models.
- Hyperparameter sensitivity (e.g., β, ρ schedule, number of inner steps T) is not thoroughly analyzed, and practical guidance for setting these parameters is lacking.

### Questions

- Can you provide a rigorous proof of Lemma 1? The current proof appears to assume the conclusion and lacks formal justification.
- In the non-convex analysis, the bound E[||∇F||²] ≤ 2G²r + 8ρ²H²·E[||∇Φ||²] includes a constant term 2G²r that does not vanish as K→∞. How does this align with the claimed convergence to an ε-stationary point? Please clarify the derivation and the interpretation of this term.
- In the convex case, the convergence rate is O(1/K) + O(K/T²). If K = O(1/ε) and T = O(1/ε), the second term becomes O(ε), which is acceptable. However, this requires T to grow with K, increasing inner-loop cost. Can you clarify the trade-off and the exact complexity in terms of ε?
- How is the gradient of the similarity term Sim(∇L_f, ∇L_r) computed in the inner loop? This involves third-order derivatives (Hessians of both L_f and L_r), which seems computationally prohibitive for large models. How is this handled in practice, and what is the additional computational cost?
- In the CIFAR-10 random forgetting results, OFMU achieves 7.71% UA while retraining achieves 6.79%. Since higher UA indicates worse unlearning (model still correctly classifies forget samples), how is OFMU's higher UA a positive result? Please clarify the direction of this metric and the interpretation.
- The overall performance score normalizes each metric by its maximum across methods. This can be manipulated by methods achieving extreme values on a single metric (e.g., GA achieving near-zero utility). How does this affect the comparison? Have you considered alternative aggregation methods?
- Why does the Retrain baseline achieve 100% Retain Accuracy on CIFAR-10 random forgetting? This seems implausible given that the retain set is 90% of the training data. Please explain.
- Can you provide more details on the hyperparameter sensitivity, particularly for β (similarity penalty weight) and the penalty schedule ρ_{k+1} = γρ_k? How were these set across benchmarks, and how sensitive are the results to their values?
- Have you compared against recent unlearning methods such as RULE (Zhang et al., 2025) or UNDIAL (Dong et al., 2024)? If not, why were they excluded from the experiments?
- How does OFMU perform when given the same computational budget (e.g., equal total FLOPs or wall-clock time) as the baselines? The current comparison may favor OFMU if it uses more compute.

### Limitations

- The theoretical guarantees are for stationary points of the penalty objective, not directly for the original bi-level problem or the actual unlearning objectives, limiting their practical relevance.
- The computational overhead (2.85x-4.22x runtime compared to gradient ascent) is significant and may limit practical adoption, especially for very large models (e.g., 70B+ parameters).
- The method requires careful tuning of multiple hyperparameters (β, ρ schedule, T, learning rates), and the paper does not provide comprehensive sensitivity analysis or practical guidance.
- The evaluation is limited to English-language benchmarks and does not consider multilingual or multimodal scenarios.
- The paper does not address potential negative societal impacts of machine unlearning, such as the possibility of using unlearning to evade content moderation, accountability, or safety regulations.
- The method's behavior in continual unlearning scenarios (sequential unlearning requests) is not addressed, though it is mentioned as future work.
- The theoretical analysis assumes smoothness and bounded gradients, which may not hold in practice for large language models.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 145,854
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 136,894
- Completion tokens: 11,654
- Reasoning tokens reported: 0
- Total tokens: 157,508
- Estimated total: $0.02245337

Full individual reviews and raw JSON responses are in `review_bundle.json`.
