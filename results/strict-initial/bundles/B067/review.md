# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B067.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.019470**

## Final Meta-review

The paper introduces EgoExo-Con, a benchmark for evaluating cross-view temporal understanding in Video-LLMs using synchronized egocentric/exocentric video pairs. It contains 491 video pairs and 3,178 human-refined temporal queries for temporal verification and temporal grounding, measuring both per-view performance and cross-view consistency. The authors evaluate 10 Video-LLMs and human performance, finding that cross-view consistency is much lower than single-view accuracy, and that naive multi-view supervised fine-tuning does not reliably improve consistency. They propose View-GRPO, a reinforcement learning framework with viewpoint-specific reasoning chains and an LLM-judge-based reasoning reward, demonstrating improvements over SFT and vanilla GRPO on Qwen2.5-VL (3B/7B).

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 2.800 | 0.400 | 2-3 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 2.800 | 0.400 | 2-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.000 | 0.000 | 6-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The paper addresses a novel and underexplored problem: cross-view temporal consistency in Video-LLMs, and constructs a benchmark with human-validated queries from synchronized ego-exo video pairs.
- The evaluation is broad, covering open-source, closed-source, time-aware, and general-purpose Video-LLMs, with human performance as a reference, and reveals a clear gap between single-view and cross-view consistency.
- The negative result that naive multi-view SFT does not improve and can even hurt consistency is a useful insight for the community.
- View-GRPO is a reasonable RL-based method that integrates viewpoint-specific reasoning and a reasoning-aware reward; it shows consistent gains over SFT and basic GRPO on the tested models.
- The analysis of LLM-judge scale effects on RL training and the calibration discussion are useful contributions.

### Weaknesses

- The benchmark is relatively small (491 video pairs, 3,178 queries) and built from only three source datasets, which may limit generalizability and statistical power; no confidence intervals or significance tests are provided.
- The consistency metric definition appears to contain a typo ('IoU < 0.5' instead of 'IoU >= 0.5' for grounding correctness), and the metric name 'V-ExoEgo' is inconsistent with the 'EgoExo' terminology.
- Table 2 omits the TimeSuite and TimeChat results that are referenced in the text, undermining the credibility of the fine-tuning analysis.
- View-GRPO is evaluated only on Qwen2.5-VL (3B/7B), so its generalization to other base models remains unclear; no comparison against existing cross-view alignment or representation learning methods is provided.
- The method relies on GPT-5-generated reasoning chains and a fixed LLM judge (Qwen2.5-3B), introducing potential bias, reproducibility concerns, and a risk of reward hacking that is not thoroughly analyzed.
- Closed-source models and human performance are evaluated on only a ~30% random subset, while open-source models are evaluated on the full set, making absolute comparisons less rigorous.
- Temporal grounding results are extremely low for many models (often below 20% R@1), raising questions about the evaluation protocol and whether consistency scores are informative at such low accuracy.

### Questions

- What is the exact definition of the consistency metric? In Section 4.1, is the grounding correctness criterion a typo, and should it be IoU >= 0.5 rather than IoU < 0.5?
- How were the train/test splits constructed, and is there any video-level overlap between View30K training data and EgoExo-Con evaluation pairs?
- Why are TimeSuite and TimeChat results referenced in Table 2 but not shown? Can the full results be provided?
- What is the inter-annotator agreement (e.g., Cohen's kappa) among the human evaluators for query validation and human performance measurement?
- For View-GRPO, can the contribution of the reasoning reward be isolated by ablating the reward while keeping the reasoning-chain data in GRPO?
- How sensitive are the results to the choice of LLM judge and the reasoning reward weight? Is there evidence against reward hacking or style overfitting?
- Why was Qwen2.5-VL selected as the only base model for View-GRPO, and would the method transfer to other Video-LLMs?
- For temporal grounding, how exactly are model outputs parsed into timestamps, and how are unparseable or unanswerable outputs handled?
- How is the synchronization of ego and exo videos validated in each source dataset, and what alignment error is considered acceptable?
- The random baseline for temporal verification is reported as V-ExoEgo=50.0, yet some open-source models score below 50; does this indicate models are worse than a constant predictor due to answer bias, and how should this be interpreted?

### Limitations

- The benchmark is limited to daily activities and skilled tasks from CharadesEgo, LEMMA, and Ego-Exo4D; it may not cover the diversity of real-world ego-exo domains.
- The benchmark construction uses GPT-4o for query generation and GPT-5 for reasoning chains, which may introduce selection bias and reproducibility issues if APIs are updated or become unavailable.
- Human validation and evaluation involve only four annotators, and inter-annotator agreement is not reported.
- The proposed View-GRPO is tested only on Qwen2.5-VL and requires substantial compute (8 A100 GPUs for 1-2 days) and access to GPT-5-generated reasoning data, which may limit adoption.
- The paper does not explore other temporal tasks (e.g., action segmentation, anticipation) or long-video settings, and does not compare against non-RL cross-view consistency methods.
- No negative societal impacts are discussed; although the benchmark uses public datasets, it could potentially be applied to surveillance scenarios.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 95,477
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 91,381
- Completion tokens: 23,804
- Reasoning tokens reported: 17,381
- Total tokens: 119,281
- Estimated total: $0.01946993

Full individual reviews and raw JSON responses are in `review_bundle.json`.
