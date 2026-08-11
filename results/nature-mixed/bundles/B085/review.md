# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B085.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.024396**

## Final Meta-review

This paper introduces Vlaser, a vision-language-action (VLA) model that integrates embodied reasoning with end-to-end robot control. The authors construct Vlaser-6M, a large-scale dataset (6M samples) spanning embodied QA, grounding, spatial reasoning, planning, and in-domain simulation data. They fine-tune InternVL3 models (2B and 8B) on this dataset, achieving state-of-the-art results on 12 embodied reasoning benchmarks. The central contribution is a systematic analysis of how different VLM pre-training data streams (out-of-domain reasoning vs. in-domain robot data) affect downstream VLA fine-tuning, revealing that in-domain data significantly improves closed-loop manipulation performance while OOD embodied reasoning data does not. The model achieves competitive results on SimplerEnv (WidowX and Google Robot) and RoboTwin benchmarks. Code, model weights, and the dataset are released publicly.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 3.200 | 0.400 | 3-4 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.200 | 0.400 | 3-4 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.000 | 0.000 | 6-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Comprehensive and well-documented construction of Vlaser-6M, covering multiple embodied reasoning modalities with detailed data generation pipelines
- Valuable systematic ablation study isolating the contribution of different data types (OOD, QA, Spatial, Grounding) to downstream VLA performance, providing actionable insights about domain shift between internet-scale data and robot embodiment
- Broad evaluation across 12 embodied reasoning benchmarks and multiple robot simulation platforms (WidowX, Google Robot, RoboTwin) with strong self-comparable results
- Open-source release of code, model weights, and dataset supporting reproducibility and future research
- Clear improvements over base models (e.g., InternVL3-2B: 15.2→45.3 avg on embodied reasoning benchmarks)
- Well-designed hyperparameter ablations (action chunk length, execution length, sampling steps)

### Weaknesses

- No real-robot experiments - all evaluation is in simulation, which limits claims about real-world applicability and is a significant gap for a robotics-focused paper
- The 'synergistic embodied reasoning' framing is somewhat overstated; the paper's own finding that OOD reasoning data does not transfer to control performance undermines the synergy claim
- Limited mechanistic analysis of why in-domain data helps - the attribution to 'domain shift' is plausible but not experimentally verified (e.g., isolating visual alignment vs. task understanding)
- Potential benchmark overlap: some evaluation benchmarks (e.g., RefSpatial) may overlap with training data sources, potentially inflating results
- Comparison with general-purpose closed-source models (GPT-4o, Gemini) may be considered unfair since Vlaser is specifically trained on embodied data
- In-domain data generation relies on Qwen2.5VL-7B and LLM-as-a-judge filtering, which may introduce model-specific biases not thoroughly analyzed
- Vlaser-8B results are not shown on robot manipulation tasks, limiting insights into scaling behavior for control
- The technical contribution is somewhat incremental, combining InternVL3 with a flow-matching action expert similar to existing approaches

### Questions

- Could you provide deeper analysis on what specific aspects of in-domain data (e.g., visual appearance, camera perspective, task-specific knowledge) drive the improvements in VLA performance? Would fine-tuning on raw robot images without QA annotations provide similar benefits?
- Why was Vlaser-8B not evaluated on the robot manipulation tasks? Would scaling model size help or hurt VLA fine-tuning performance?
- How do you ensure the quality of the 2M in-domain generated samples beyond the Qwen2.5VL-32B LLM-as-a-judge filtering? What were the disagreement cases with human raters and how were they handled?
- Have you considered evaluating on real-robot setups or other sim-to-real transfer benchmarks to validate the generalizability of your findings?
- The 2B model outperforms the 8B model on several benchmarks (e.g., Where2place, Pixmo-Points, grounding tasks). Is this due to overfitting, architectural reasons, or data quality issues? What does this suggest about optimal model size for embodied applications?
- How much of the in-domain data improvement is due to the specific data generation/filtering pipeline versus the raw data itself? Would synthetic data generated from the same simulation platforms without LLM annotation provide similar gains?
- For the planning data generated in Habitat, what was the success rate of the GPT-4o rollouts? How many trajectories were discarded, and does this filtering introduce any bias?
- What is the computational cost of the full training pipeline for the 2B and 8B models? This information would help practitioners assess feasibility of reproduction.
- Have you examined whether OOD data actively degrades VLA performance or simply does not help? What are the potential negative interactions?
- The flow-matching action expert uses non-causal attention for the VLA stream. How does this compare to causal attention in terms of training stability and performance?

### Limitations

- All experiments are conducted in simulation without real-robot validation, which may not fully capture real-world challenges such as sensor noise, calibration errors, and physical dynamics
- The Vlaser-6M dataset relies heavily on existing public datasets and LLM-based annotation, which may introduce systematic biases from the generating models
- The analysis of data effectiveness is limited to specific robot embodiments (WidowX, Google Robot, Aloha-AgileX) and may not generalize to other robot platforms or task distributions
- Potential benchmark overlap between training data sources and evaluation benchmarks may inflate reported results
- The paper does not deeply explore potential negative societal impacts of embodied AI systems, such as safety concerns in real-world deployment, job displacement, or dual-use risks
- The computational cost and environmental impact of training 8B models and generating 6M data samples are not discussed, which may limit accessibility for smaller research groups
- The paper does not investigate whether smaller amounts of in-domain data would suffice or whether the data generation pipeline could be made more efficient

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 163,273
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 154,313
- Completion tokens: 9,881
- Reasoning tokens reported: 0
- Total tokens: 173,154
- Estimated total: $0.02439559

Full individual reviews and raw JSON responses are in `review_bundle.json`.
