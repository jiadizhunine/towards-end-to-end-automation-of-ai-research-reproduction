# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B162.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **3/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 1, 'Reject': 4}
- Estimated API cost: **$0.020521**

## Final Meta-review

The paper introduces DriveAction, a benchmark for evaluating Vision-Language-Action (VLA) models in autonomous driving. It comprises 16,185 QA pairs from 2,610 real-world driving scenarios collected by drivers of autonomous vehicles across 148 cities. Action labels are derived from real-time driver operations and manually verified. The benchmark proposes an action-rooted, tree-structured evaluation framework linking action decisions to prerequisite vision and language tasks, supporting both comprehensive and task-specific evaluation. Experiments with 12 state-of-the-art VLMs and two proprietary driving-domain models show that performance drops when vision/language QA guidance is removed, and the benchmark is claimed to be more discriminative than existing benchmarks.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 2 | 2.600 | 0.490 | 2-3 |
| Significance | 2 | 2.600 | 0.490 | 2-3 |
| Soundness | 2 | 2.200 | 0.400 | 2-3 |
| Presentation | 2 | 2.600 | 0.490 | 2-3 |
| Contribution | 2 | 2.200 | 0.400 | 2-3 |
| Overall | 3 | 4.400 | 0.800 | 4-6 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- The action-rooted, tree-structured evaluation is a novel concept that explicitly connects action outputs to required vision and language sub-tasks, enabling goal-driven analysis.
- Using real-time driver operations for action labels provides a more realistic and human-aligned ground truth than post-hoc manual annotation.
- The dataset spans 148 cities with diverse scenarios including ramps, construction, and VRU interactions, offering broad coverage.
- The benchmark includes extensive experiments across 12 VLMs and two domain-specific models, with four evaluation modes and stability analysis.
- DriveAction appears to differentiate model performance more sensitively than several existing benchmarks, which is valuable for model comparison.

### Weaknesses

- The core modality-ablation experiment is confounded: the model always receives raw visual frames and navigation information; only the ground-truth QA textual hints are removed in the V-A, L-A, and A modes. Thus claims about 'without vision input' or 'without language input' are misleading, and the evaluation is oracle-based rather than end-to-end.
- The dataset and evaluation code are not publicly released (the benchmark link is redacted with no release information), severely limiting reproducibility and community adoption.
- Critical dataset construction details are missing, including scenario sampling strategy, distribution statistics, annotation protocol, inter-annotator agreement, QA generation prompts, and the discretization process from continuous driving operations to high-level actions.
- The action-rooted tree structure is only informally described; no formal specification or validation is provided, and the redacted figures prevent full understanding.
- The proprietary driving-domain models are not described in sufficient detail (architecture, training data, hyperparameters), and there is a potential risk of data leakage since both the models and benchmark originate from the same company's fleet.
- No comparisons are made with existing open-source driving VLA models (e.g., DriveGPT4, OpenDriveVLA) or with action-related benchmarks such as DriveLM and DriveBench, making the claim of being the 'first action-driven benchmark' overstated.
- Evaluation is limited to QA accuracy; there are no metrics for safety, trajectory quality, temporal consistency, or uncertainty, and no chance-level or majority-class baseline is reported.
- Statistical significance and confidence intervals are absent, and the task-specific bottleneck conclusions are based on informal comparisons.
- Ethical and privacy concerns regarding the use of real-world driver-contributed data (faces, license plates, bystander privacy, consent) are not addressed.

### Questions

- In the comprehensive evaluation modes, are the ground-truth answers from vision and language QA tasks injected verbatim into the action prompt? If so, what exactly do the V-L-A versus A comparisons measure, and how does this support claims about 'without vision input' or 'without language input'?
- How were the 2,610 driving scenarios sampled from the driver-contributed data, and what are the distributions across cities, scenario categories, and action types?
- How are continuous driving operations (e.g., steering angle, throttle) discretized into high-level action labels? What thresholds or rules are used?
- What is the inter-annotator agreement for the manual verification and QA screening stages? Were multiple annotators used?
- What is the random-chance or majority-class accuracy for each task, and are answer choices balanced across options?
- How is the action-rooted tree formally defined? Can you provide pseudocode or an explicit mapping from actions to language/vision tasks, and was the tree validated with human or automatic methods?
- What are the training details and data sources for the two proprietary driving models? Were they trained on DriveAction or on data that overlaps with the benchmark evaluating them?
- Why were no open-source driving-specific VLA models (e.g., DriveGPT4, OpenDriveVLA) evaluated, and how should models that output continuous trajectories be assessed with the discrete QA format?
- What privacy and consent measures were taken for the driver-collected data, including anonymization of faces, license plates, and third-party individuals?

### Limitations

- The main experimental protocol uses oracle-based intermediate QA answers, so it does not reflect true end-to-end VLA perception and reasoning.
- The benchmark is not publicly available, limiting verification, reuse, and community impact.
- The proprietary nature of the driving data and models prevents independent reproducibility and may introduce geographic or company-specific bias.
- The discrete high-level action space oversimplifies continuous driving decisions, and the manually defined tree may miss important action-reasoning dependencies.
- The evaluation focuses on QA accuracy and does not capture safety, comfort, or temporal consistency of driving behavior.
- The paper does not discuss potential negative societal impacts, including privacy and surveillance risks from real-world driving imagery.
- The absence of chance-level baselines, confidence intervals, and statistical significance tests weakens the interpretability of results.

### Ethics

Ethical concerns flagged: **True**

## Usage and Cost

- Requests: 6
- Prompt tokens: 105,870
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 101,774
- Completion tokens: 22,360
- Reasoning tokens reported: 15,309
- Total tokens: 128,230
- Estimated total: $0.02052063

Full individual reviews and raw JSON responses are in `review_bundle.json`.
