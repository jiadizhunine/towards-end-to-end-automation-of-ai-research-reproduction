# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B162.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 3, 'Reject': 2}
- Estimated API cost: **$0.017910**

## Final Meta-review

The paper introduces DriveAction, a benchmark for evaluating Vision-Language-Action (VLA) models in autonomous driving. It comprises 16,185 QA pairs from 2,610 real-world driving scenarios collected by drivers of autonomous vehicles across 148 cities. Key contributions are: (1) driver-contributed broad-coverage scenarios, (2) action labels derived from real-time driver operations rather than post-hoc annotation, and (3) an action-rooted tree-structured evaluation framework linking actions to vision and language tasks. The authors evaluate 12 state-of-the-art VLMs across four evaluation modes (full pipeline, vision-only, language-only, uninformed) and two proprietary driving models, showing that both vision and language guidance are needed for optimal action prediction. The benchmark also demonstrates better discriminative power between models compared to existing benchmarks.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 2.800 | 0.400 | 2-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 5.600 | 0.490 | 5-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel data collection approach using real-time driver operations, which better captures human driving intent than post-hoc annotations.
- Broad scenario coverage across 148 cities and 7 scenario categories, addressing diversity limitations of existing benchmarks.
- Well-designed action-rooted tree-structured evaluation framework that supports both comprehensive and task-specific assessment.
- Comprehensive evaluation across 12 state-of-the-art VLMs with four ablation modes, providing useful insights into modality dependencies.
- Good stability analysis showing consistent results across repeated runs, supporting benchmark reliability.
- The benchmark demonstrates better sensitivity in distinguishing between domain-specific driving models compared to existing benchmarks.

### Weaknesses

- Insufficient documentation of the QA generation process, including prompting strategy, human annotation workflow, inter-annotator agreement, and quality control metrics.
- The claim of being 'the first action-driven benchmark' is overstated, as DriveLM and DriveBench also address the full V-L-A pipeline, though with different structures.
- The V-L-A evaluation mode injects ground-truth answers to upstream vision and language tasks, which may not reflect real-world conditions where models must generate these answers, potentially inflating performance.
- No statistical significance testing is provided for performance differences between models or evaluation modes.
- The comparison with existing benchmarks uses different evaluation protocols and metrics, making the claimed superiority in sensitivity questionable.
- The proprietary driving models used for comparison are not open-sourced, limiting reproducibility.
- The paper does not address potential biases in driver-contributed data, such as geographic or demographic distribution, or privacy concerns regarding real-world images.
- The dataset is based on a single company's autonomous vehicle fleet, which may introduce selection bias.

### Questions

- What is the exact process for generating QA pairs? Please provide details on the two-stage LLM prompting framework, validation criteria, human annotation workflow, number of annotators, inter-annotator agreement, and rejection rates.
- How were the 2,610 scenarios selected from the broader pool of driving data? What criteria were used, and what is the distribution across the 7 scenario categories and 148 cities?
- In the V-L-A mode, the model receives ground-truth answers to upstream vision and language tasks. How does this compare to providing raw scenario information directly? Does this artificially inflate performance compared to a realistic setting where models must generate these answers?
- How were the 14 tasks selected, and how were the dependencies between vision, language, and action tasks determined in the tree-structured framework? Is there any validation of this structure?
- Could you provide statistical significance tests (e.g., confidence intervals) for the performance differences between evaluation modes and between models?
- How do the proprietary driving models (Non-MOE and MOE) compare in terms of architecture, training data, and fine-tuning process? This is crucial for understanding their performance differences.
- In Table 6, the comparison with existing benchmarks uses different question formats and metrics. How was the unified average score computed, and is this comparison truly fair?
- How are ambiguous driving scenarios handled where multiple actions could be equally valid? Is there a mechanism to acknowledge valid alternative actions?
- What measures have been taken to address privacy concerns with real-world driving data (e.g., faces, license plates)? Are there plans for data anonymization and clear licensing?
- Have you considered evaluating open-source VLA models (e.g., OpenDriveVLA, AutoVLA) on DriveAction to improve reproducibility?

### Limitations

- The benchmark relies on proprietary data from a single company's autonomous vehicle fleet, which may introduce bias in scenario distribution and driving styles.
- Action labels are discretized into high-level categories, which may not capture the full nuance of continuous driving decisions.
- The evaluation focuses on closed-set QA tasks with accuracy as the primary metric, which may not capture safety-critical aspects or open-ended driving scenarios.
- The evaluation uses API-based models, which may have changing performance over time, affecting long-term reproducibility.
- The paper does not discuss potential negative societal impacts, such as over-reliance on benchmark results for safety-critical deployment decisions, or privacy concerns related to real-world driving data.
- The dataset size (16,185 QA pairs) may be limited for training purposes, though it appears sufficient for evaluation.
- The evaluation does not consider temporal consistency of decisions across consecutive frames, which is important for real-world driving.

### Ethics

Ethical concerns flagged: **True**

## Usage and Cost

- Requests: 6
- Prompt tokens: 115,051
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 106,091
- Completion tokens: 10,828
- Reasoning tokens reported: 0
- Total tokens: 125,879
- Estimated total: $0.01790967

Full individual reviews and raw JSON responses are in `review_bundle.json`.
