# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B128.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 1, 'Reject': 4}
- Estimated API cost: **$0.032092**

## Final Meta-review

The paper introduces HydraFake-100K, a large-scale deepfake detection dataset with a hierarchical OOD evaluation protocol covering in-domain, cross-model, cross-forgery, and cross-domain splits. It also proposes Veritas, an MLLM-based detector trained with pattern-aware reasoning (fast judgment, reasoning, conclusion, planning, self-reflection) via a two-stage pipeline: cold-start SFT plus Mixed Preference Optimization (MiPO), followed by pattern-aware GRPO (P-GRPO). Experiments show that prior detectors generalize well on cross-model data but poorly on unseen forgeries/domains, while Veritas achieves substantial accuracy gains on several OOD splits and provides transparent reasoning traces.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 2 | 2.400 | 0.490 | 2-3 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 2 | 2.200 | 0.400 | 2-3 |
| Presentation | 2 | 2.400 | 0.490 | 2-3 |
| Contribution | 2 | 3.000 | 0.632 | 2-4 |
| Overall | 4 | 4.600 | 1.200 | 4-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- HydraFake-100K addresses a real gap in benchmark design by including diverse generators, resolutions, and in-the-wild data, and the hierarchical OOD splits enable finer-grained diagnosis of detector generalization.
- The pattern-aware reasoning framework is a novel adaptation of LLM reasoning techniques to deepfake detection, and the two-stage training pipeline (SFT+MiPO then P-GRPO) shows clear empirical gains over vanilla CoT and prior MLLM detectors.
- Extensive experiments compare 10 specialized detectors and several MLLMs, with ablations showing contributions of each training stage, robustness checks under JPEG compression/blur, and reasoning-quality analyses.
- Veritas outperforms strong baselines by large margins on cross-forgery and cross-domain splits, and the human-readable reasoning outputs are valuable for forensic interpretation.
- The paper provides detailed appendix material, including per-subset precision/recall and qualitative examples, which support the main claims.

### Weaknesses

- A critical implementation inconsistency: the paper states β and β′ are set to 0, but β=0 makes the MiPO objective in Eq. (2) constant and unlearnable, and β′=0 removes KL regularization in P-GRPO; this directly contradicts the described method and undermines reproducibility.
- Several key technical details are under-specified: exact MiPO preference data construction, how planning/self-reflection flags are automatically detected for P-GRPO rewards, the values of λ1/λ2, and the validation of the reflection-quality reward model.
- Potential data leakage/overlap is not ruled out: training fake data are claimed to include classic data sampled from FFIW, which is also used as a cross-domain test subset, and no exact source-to-split mapping or identity-level separation is provided.
- Reasoning faithfulness is not rigorously validated: only MLLM-as-a-judge is used, with no human evaluation, inter-annotator agreement, or hallucination metrics; the claim that reasoning is 'transparent and faithful' is therefore not well supported.
- The claimed superiority is uneven: Veritas underperforms several baselines on IC-Light (75.7 vs 94.8) and DeepFaceLab (58.6 vs 69.7), which are only mentioned in the appendix and not discussed as limitations in the main text.
- The presentation quality is poor: Table 1 is severely malformed, table ordering is inconsistent, and several key hyperparameters and evaluation details are missing, hampering reproducibility.
- The dataset release plan is unclear, and ethical/legal concerns about scraping social media images and removing watermarks without explicit consent are not adequately addressed.

### Questions

- What are the actual values of β and β′? If β=0 is intended, how does MiPO learn any preference signal?
- How are planning (P) and self-reflection (R) automatically detected in P-GRPO rollouts? What parser or LLM judge is used, and what are the accuracy and calibration of this detection?
- Please provide a complete mapping of every HydraFake subset to training/validation/test and clarify whether any FFIW, WILD, or TalkingHeadBench data appear in both training and evaluation splits.
- How were the MiPO preference pairs curated? Were human annotators involved, and what was the inter-annotator agreement?
- Why is Veritas much weaker on IC-Light and DeepFaceLab than some specialized detectors? What does this reveal about the method's actual OOD robustness?
- Were all reported accuracies averaged over multiple seeds/checkpoints? Can confidence intervals or standard deviations be provided?
- Will the dataset and code be publicly released, and under what license? How were privacy and consent for social media images handled, and is watermark removal compliant with platform policies?
- What is the inference cost of Veritas compared to lightweight detectors, and is reasoning-based detection practical for large-scale deployment?

### Limitations

- The method relies on expensive MLLM inference and RL training; no analysis of computational cost or deployment feasibility is provided.
- The dataset is image-only and face-centric, covering no video/audio temporal artifacts or full-scene AIGC content.
- Performance remains weak on low-resolution and classic deepfake data (e.g., DeepFaceLab, FFIW), indicating unresolved generalization gaps.
- Reasoning traces and preference annotations are largely MLLM-generated with limited human verification, so annotation noise and hallucinated rationales may propagate.
- The use of social media images and realistic deepfakes of real identities raises dual-use and privacy concerns that are not fully mitigated beyond a generic ethics statement.
- No analysis of adversarial robustness, demographic bias, or false positives on natural images is provided.

### Ethics

Ethical concerns flagged: **True**

## Usage and Cost

- Requests: 6
- Prompt tokens: 169,578
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 165,482
- Completion tokens: 31,834
- Reasoning tokens reported: 25,206
- Total tokens: 201,412
- Estimated total: $0.03209247

Full individual reviews and raw JSON responses are in `review_bundle.json`.
