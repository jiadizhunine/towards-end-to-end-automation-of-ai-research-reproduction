# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B179.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.021214**

## Final Meta-review

The paper introduces GUI-Shift, a self-supervised reinforcement learning framework for training VLM-based GUI agents. The core contribution is a K-step GUI Transition task, an inverse dynamics objective where the model predicts the first action that transitions between two GUI states (current state St and future state St+k), using the future state as a visual goal instead of human-annotated instructions. The framework applies GRPO with rule-based rewards (format + action correctness) and a data filtering pipeline to select informative training samples. Experiments across four VLM backbones (Qwen2.5-VL-7B, InternVL3-8B, MimoVL-7B-SFT, MimoVL-7B-RL) and five benchmarks (AndroidControl, GUI Odyssey, AndroidWorld, ScreenSpot-v2, ScreenSpot-Pro) show improvements of up to 11.2% on GUI task automation and moderate gains on grounding tasks, using only 2K training samples. Ablations demonstrate the benefits of data filtering, the superiority of visual targets over textual instructions, the efficiency of omitting reasoning traces, and the advantages of GRPO over SFT.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.800 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.400 | 0.490 | 3-4 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.400 | 0.490 | 3-4 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.400 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel and well-motivated task formulation: K-step GUI Transition with visual goals is an elegant way to address the annotation bottleneck in GUI agent training.
- Comprehensive evaluation across multiple VLM backbones and diverse benchmarks, including both static and end-to-end evaluations.
- Strong experimental results showing consistent improvements over base models in most settings, with notable gains on AndroidControl-High.
- Thorough ablation studies covering data filtering, task formulation, reasoning configurations, and training algorithm comparisons.
- The finding that visual goals (St+k) can outperform textual instructions is interesting and well-supported.
- The comparison showing GRPO's advantage over SFT for this task is valuable, highlighting the issue of action multiplicity.
- Clear writing, good organization, and open-source release enhance reproducibility.
- Training efficiency improvements (no reasoning traces, ~50% time reduction) without performance compromise are practically significant.

### Weaknesses

- The 'self-supervised' and 'annotation-free' claims are somewhat overstated: training data is sourced from AndroidControl which has human-annotated trajectories, and ground-truth actions are still used as supervision in the reward function.
- Results are inconsistent across benchmarks: GUI Odyssey shows declines for Mimo models (up to -3.6% EM), and InternVL3-8B shows drops on AndroidControl-Low. These are briefly attributed to domain differences but lack deep analysis.
- The optimal K value varies inconsistently across models and benchmarks (e.g., K=1 best for Qwen, K=4 best for InternVL), with no clear guidance for practitioners.
- The data filtering process uses the same reward function as training, which could introduce a selection bias or circularity issue.
- Only 2K training samples are used; the scaling study is limited to InternVL3-8B and shows only modest gains from increasing data size.
- Comparison with annotation-trained baselines is confounded by different training data sources, volumes, and settings, making direct comparison difficult.
- Limited analysis of failure cases, qualitative behavior, or cross-domain generalization (e.g., tablet layouts, web/desktop GUIs).

### Questions

- 1. Since the training data is derived from AndroidControl's annotated trajectories, how would the approach perform with truly unlabeled data from automated exploration or raw user logs? Have you tested this scenario?
- 2. What determines the optimal K for a given model? Is there a relationship between model capacity, prior GUI experience, and the ideal transition step size?
- 3. The data filtering uses the same reward function as training. Could this create a selection bias where the model only learns from samples it can partially solve? Have you considered using a different criterion for filtering?
- 4. For GUI Odyssey declines, have you analyzed performance separately for phone vs. tablet episodes to validate the tablet-layout hypothesis?
- 5. The SFT results show dramatic performance drops. Is this due to training/evaluation format mismatch, or does SFT fundamentally fail on this task? Would SFT on a mixed dataset (transition + instruction) help?
- 6. How does the reward function handle action ambiguity (e.g., different first actions leading to the same St+k, or functionally equivalent clicks)?
- 7. What is the computational cost of the data filtering process (8 generations per sample), and how does it scale to larger datasets?
- 8. Have you considered using multiple K values simultaneously during training, and what would be the expected effect?
- 9. For the grounding benchmarks, the gains are modest (0.0-2.5%). What explains the limited transfer, and could specific training configurations improve it further?

### Limitations

- The approach still requires ground-truth action annotations for reward computation, so the 'annotation-free' claim should be clarified to specify that it removes instruction annotations but not action labels.
- Training data is from a single dataset (AndroidControl), limiting diversity of GUI environments; generalization to web, desktop, or other platforms is not tested for training.
- Evaluation is primarily on Android-style interfaces; tablet layouts cause performance drops on GUI Odyssey, suggesting limited cross-form-factor generalization.
- The computational cost of data filtering (8 rollouts per sample) may limit accessibility for smaller research groups and scalability to very large datasets.
- Potential negative societal impact of GUI agents (e.g., malicious automation, unauthorized actions, data scraping) is not discussed.
- The paper does not address potential bias in GUI trajectories (e.g., underrepresentation of certain apps, user demographics, or accessibility features).

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 138,685
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 129,725
- Completion tokens: 10,811
- Reasoning tokens reported: 0
- Total tokens: 149,496
- Estimated total: $0.02121367

Full individual reviews and raw JSON responses are in `review_bundle.json`.
