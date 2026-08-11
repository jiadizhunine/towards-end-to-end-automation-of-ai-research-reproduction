# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B067.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.016189**

## Final Meta-review

This paper introduces EgoExo-Con, a benchmark for evaluating cross-view temporal understanding in Video-LLMs using synchronized egocentric-exocentric video pairs. The benchmark contains 491 video pairs and 3,178 human-validated queries for two tasks: temporal verification (binary QA) and temporal grounding (moment localization). The authors evaluate 10 models (8 open-source, 2 closed-source) plus human baselines, revealing that models achieve cross-view consistency scores barely over half their single-view performance, indicating reliance on view-specific biases. They also show that naive multi-view supervised fine-tuning (SFT) can underperform single-view training. To address this, they propose View-GRPO, a reinforcement learning framework combining GRPO with viewpoint-specific reasoning chains and a three-part reward (format, accuracy, reasoning similarity) using an LLM judge. Experiments on Qwen2.5-VL (3B and 7B) show consistent improvements over SFT and standard GRPO, particularly on cross-view consistency metrics. The benchmark and View30K training data will be released publicly.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.600 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.400 | 0.490 | 3-4 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.400 | 0.490 | 3-4 |
| Contribution | 3 | 3.200 | 0.400 | 3-4 |
| Overall | 6 | 6.400 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important and underexplored problem: cross-view temporal consistency in Video-LLMs.
- Careful benchmark construction with multi-stage query refinement, human validation, and filtering of ambiguous samples.
- Comprehensive evaluation across a diverse set of models (general-purpose, time-aware, closed-source) with human performance as reference.
- Counterintuitive and valuable finding that naive multi-view training can be detrimental to consistency.
- View-GRPO is a well-motivated method showing consistent improvements over SFT and standard GRPO, especially on consistency metrics.
- Good analysis of LLM-judge reliability and its impact on training stability.
- Well-organized paper with clear figures, tables, and a detailed appendix.

### Weaknesses

- Benchmark scale is relatively small (491 pairs, 3,178 queries), which may limit statistical power and generalizability.
- Heavy reliance on GPT-4o/GPT-5 for query refinement and reasoning chain generation could introduce model-specific biases and reproducibility concerns.
- View-GRPO improvements are modest in absolute terms (e.g., 5-11 percentage points on consistency) and lack statistical significance testing.
- The method is only evaluated on Qwen2.5-VL (3B/7B); generalizability to other architectures is unknown.
- The reasoning reward relies on an LLM judge (Qwen2.5-3B), which may introduce bias; sensitivity to judge choice is only partially explored.
- Human and closed-source model evaluation is only on a 30% subset, potentially limiting comparability with open-source models on the full set.
- Limited analysis of failure cases and why the reasoning reward helps beyond conjectures about reducing view-specific biases.
- No comparison with alternative cross-view alignment methods (e.g., contrastive learning, distillation).

### Questions

- How robust are the results to different random seeds or data splits? Were statistical significance tests (e.g., bootstrap) performed for the consistency improvements?
- What is the inter-annotator agreement for the human validation of queries and the human performance evaluation?
- How was the 30% subset for human/closed-source evaluation selected? Was it random and stratified? Could this affect comparability of results across model categories?
- How sensitive is View-GRPO to the choice of LLM judge? The paper shows Qwen2.5-0.5B vs 3B, but what about larger or different judge models (e.g., GPT-4o)?
- Could the improvements from View-GRPO be attributed to the additional training data (View30K) rather than the RL formulation? Have you compared against SFT on the same View30K data?
- Does View-GRPO generalize to other base models beyond Qwen2.5-VL (e.g., Video-LLaMA3, TimeChat)?
- Have you considered using a continuous consistency metric for grounding (e.g., average temporal IoU between viewpoint predictions) instead of the binary metric?
- Could the reasoning reward be replaced with a more objective metric (e.g., rule-based verification) to reduce LLM judge bias?
- What is the impact of the reasoning reward weight in the total reward function? Is there a sensitivity analysis?
- How does the performance of View-GRPO compare with simpler alternatives like contrastive representation learning or explicit alignment losses?

### Limitations

- The benchmark is limited to three source datasets (CharadesEgo, LEMMA, Ego-Exo4D) and may not cover all ego-exo video scenarios or domains.
- Video segmentation for videos longer than 5 minutes may introduce artificial boundaries that don't reflect real-world long-video understanding.
- The reliance on GPT-5 for generating reasoning chains and GPT-4o for query refinement may introduce proprietary model biases and limit reproducibility for researchers without access to these APIs.
- The LLM judge for reasoning rewards adds complexity and potential calibration issues; performance may be sensitive to judge choice.
- The modest improvements from View-GRPO may not justify the computational cost (1-2 days on 8 A100s) for all practical deployments.
- The evaluation focuses only on temporal tasks; cross-view consistency in other dimensions (spatial, semantic) is not explored.
- The paper does not discuss potential negative societal impacts, such as privacy concerns in egocentric video data or potential misuse of temporal grounding in surveillance.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 105,356
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 96,396
- Completion tokens: 9,530
- Reasoning tokens reported: 0
- Total tokens: 114,886
- Estimated total: $0.01618893

Full individual reviews and raw JSON responses are in `review_bundle.json`.
