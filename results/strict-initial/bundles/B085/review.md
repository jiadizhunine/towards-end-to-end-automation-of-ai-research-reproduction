# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B085.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.022348**

## Final Meta-review

The paper introduces Vlaser, a vision-language-action model built on InternVL3 with an added flow-matching action expert, and Vlaser-6M, a large multi-task dataset for embodied reasoning. The model is pretrained on this dataset and then fine-tuned for closed-loop robot control. The authors report strong performance on 12 embodied reasoning benchmarks and analyze how different VLM pretraining data streams (e.g., embodied QA, grounding, spatial, in-domain simulation data) affect downstream VLA policy learning on SimplerEnv, concluding that in-domain robot-viewpoint data transfers better than generic embodied reasoning data.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 2 | 2.600 | 0.490 | 2-3 |
| Quality | 2 | 2.000 | 0.000 | 2-2 |
| Clarity | 2 | 2.400 | 0.490 | 2-3 |
| Significance | 2 | 2.600 | 0.490 | 2-3 |
| Soundness | 2 | 2.000 | 0.000 | 2-2 |
| Presentation | 2 | 2.400 | 0.490 | 2-3 |
| Contribution | 2 | 2.200 | 0.400 | 2-3 |
| Overall | 4 | 4.000 | 0.000 | 4-4 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- The construction and release plan for the large Vlaser-6M dataset is a valuable community contribution.
- The paper investigates an important and under-explored question: which VLM pretraining data streams are most effective for downstream VLA fine-tuning.
- Evaluation spans many embodied reasoning benchmarks and two model scales, demonstrating consistent improvements over the base InternVL3 models on these benchmarks.
- The observation that in-domain robot data is more effective than out-of-domain internet data for VLA control is practically useful and can guide future dataset collection.

### Weaknesses

- There is a serious risk of training/evaluation contamination: Vlaser-6M is built from datasets that overlap with or closely mirror many of the evaluation benchmarks (e.g., RefSpatial, Pixmo-Points, Paco-Lavis, VSI-Bench, EgoPlan-IT, SPAR), and the in-domain data are generated from SimplerEnv and then evaluated on the same SimplerEnv tasks, with no explicit leakage analysis.
- All robot-control results are from simulation only (SimplerEnv); no real-robot experiments are provided, limiting claims about real-world embodied agents.
- The main empirical conclusion is not robust: the full Vlaser-2B model underperforms or matches the InternVL3 baseline on several tasks, while only the Vlaser-QA variant (trained solely on in-domain data) shows clear improvements, and the ablation is confounded by dataset size and composition.
- The paper provides no statistical significance testing, no confidence intervals or multiple seeds, making it unclear whether reported differences are meaningful.
- The naming and composition of model variants (e.g., Vlaser-QA) are confusing, and technical details (e.g., action head integration step size, training epochs) are inconsistent or underwritten.
- The conclusions are based on a single VLM architecture (InternVL3), two embodiments, and only up to 8B parameters; no comparison with other VLM backbones or larger scales is made to isolate the effect of VLM initialization.

### Questions

- How do the authors prevent training/evaluation leakage given that Vlaser-6M includes data from benchmarks that are then used in Table 1? What explicit overlap analysis was performed, and how were test splits excluded?
- What exactly constitutes Vlaser-QA? Is it trained solely on the 2M in-domain QA pairs from SimplerEnv, or does it include other robot QA data? Please clarify the data composition of each model variant.
- Why does the full Vlaser model (trained on all 6M data) underperform Vlaser-QA on closed-loop tasks? Is this due to negative transfer, data imbalance, or training instability?
- Can the authors provide a controlled ablation that matches data volume and composition (e.g., 2M in-domain vs 2M out-of-domain vs mixed) to isolate the effect of domain mismatch?
- Are the reported SimplerEnv success rates averaged over multiple seeds with standard deviations? Were the baselines and Vlaser models evaluated under identical conditions with the same number of episodes?
- Have the authors validated the VLA policies on real physical robots? If not, what evidence is there that the in-domain data finding transfers beyond the simulator?

### Limitations

- All VLA evaluations are conducted in simulation (SimplerEnv); no real-robot deployment is reported, and sim-to-real gaps are not addressed.
- Potential train/test contamination between Vlaser-6M and the embodied reasoning benchmarks limits the credibility of the claimed state-of-the-art results.
- In-domain QA data are automatically generated using proprietary models (e.g., Qwen2.5-VL-7B) without human validation, which may introduce label noise and bias.
- The study is limited to two robot embodiments (WidowX and Google Robot) and two model sizes (2B and 8B); findings may not generalize to other embodiments or larger models.
- No analysis of failure cases, robustness, or safety of the closed-loop policies is provided.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 120,989
- Cache-hit prompt tokens: 10,496
- Cache-miss prompt tokens: 110,493
- Completion tokens: 24,462
- Reasoning tokens reported: 17,476
- Total tokens: 145,451
- Estimated total: $0.02234777

Full individual reviews and raw JSON responses are in `review_bundle.json`.
