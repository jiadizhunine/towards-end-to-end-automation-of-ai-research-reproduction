# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B167.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.015762**

## Final Meta-review

The paper introduces Lego-Edit, an instruction-based image editing framework in which a multimodal large language model (Builder) is trained to orchestrate a library of specialized model-level editing tools (Bricks). The Builder is trained via a three-stage progressive reinforcement learning pipeline: supervised fine-tuning on expert workflow traces, GRPO with ground-truth workflow rewards, and GRPO with a critic-based reward on unannotated instructions. The toolkit includes predictive tools (segmentation, captioning, position prediction) and edit-specific diffusion adapters (inpainting, style, color, pose, environment). The method reports state-of-the-art VIEScore results on GEdit-Bench and ImgBench, with ablations supporting the design choices and qualitative demonstrations of zero-shot tool composition, user feedback adaptation, and new-tool insertion.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 2.800 | 0.400 | 2-3 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 2 | 2.200 | 0.400 | 2-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 3 | 2.800 | 0.400 | 2-3 |
| Presentation | 2 | 2.200 | 0.400 | 2-3 |
| Contribution | 3 | 2.800 | 0.400 | 2-3 |
| Overall | 6 | 5.600 | 0.800 | 4-6 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- The modular agent-tool decomposition is a flexible and clean design, allowing the Builder to compose specialized editing models without task confusion and enabling zero-shot generalization to new workflows.
- The three-stage progressive RL curriculum (SFT -> GT-based GRPO -> GT-free critic-based GRPO) is well motivated, and ablations show consistent gains in execution success and editing quality, especially on complex paraphrased instructions.
- Strong quantitative results are reported on two benchmarks, with the highest overall scores on GEdit-Bench and ImgBench, and particularly large improvements on the Hybrid Editing subtask.
- Ablations isolate contributions of task-specialized LoRA adapters, tool composition, and each RL stage, supporting the core design choices.
- Qualitative examples demonstrate useful capabilities beyond fixed pipelines, including zero-shot tool composition and adaptation to new tools or user feedback without retraining.
- The reported latency (~7.2s) is substantially lower than an end-to-end baseline (>25s), suggesting practical viability.

### Weaknesses

- The Stage-3 critic reward is based on a single 72B MLLM without validation against human judgments, no inter-annotator agreement, and no analysis of potential reward hacking; the effectiveness reward is a coarse heuristic (N_add/N_remove) that may not correlate with actual visual quality.
- Training data (OmniEdit, MagicBrush) may overlap with evaluation benchmarks (GEdit-Bench, ImgBench), but no contamination analysis is provided, which could inflate reported state-of-the-art numbers.
- Evaluation relies exclusively on GPT-4o-based VIEScore with a single seed and no human study or statistical significance testing; the margin over the next-best baseline on ImgBench is small (3.50 vs 3.44) and may be within noise.
- Key implementation details are missing: several tools are unnamed, the complete GEdit-Bench table is absent/redacted, and ground-truth workflow generation, Executor behavior, and GRPO hyperparameters are not fully specified, limiting reproducibility.
- Open-domain generalization is not convincingly demonstrated because Stage-3 instructions are still derived from OmniEdit; the benchmark instructions may follow similar distributions, and the 'complex' set uses only GPT-4o paraphrases.
- The work has limited novelty: MLLM-as-agent tool invocation and RL for tool selection have been explored in prior systems (e.g., ComfyAgent, VisualToolAgent), and the contribution is mostly an application of these ideas to image editing with a curated tool library.
- The framework has no built-in verification, retry, or fallback for tool failures; robustness depends on explicit user feedback, and only a single qualitative example is given for new-tool integration.

### Questions

- How was the Qwen2.5-VL-72B critic validated, and what measures were taken to prevent the Builder from exploiting the critic's limitations or reward hacking?
- What is the exact overlap between training data (OmniEdit/MagicBrush) and evaluation benchmarks (GEdit-Bench/ImgBench), and were near-duplicates filtered?
- Can the authors provide the full GEdit-Bench results table, including per-category scores and statistical significance tests for the marginal improvements?
- What exactly defines a 'pass' for execution success (99% complex), and how are workflow parameters verified semantically?
- What are the identities and interfaces of the unspecified 'additional tools', and how is the Executor's parsing and DAG execution implemented?
- How were the 50K Stage-3 unannotated instructions selected, and are they truly open-domain relative to the training distribution?
- What are the exact GRPO hyperparameters (group size, clipping epsilon, KL coefficient), and how sensitive are the results to the graph-matching threshold (0.6) and reward weights?
- Why is there no quantitative comparison with other MLLM-based agent frameworks such as ComfyAgent, and is the claimed state-of-the-art benefit robust to that comparison?
- Has any human evaluation or side-by-side perceptual study been conducted to confirm that VIEScore differences translate to meaningful quality gains?

### Limitations

- The framework's capabilities are bounded by the predefined tool library; any instruction requiring an operation outside the toolkit cannot be executed unless a new tool is provided.
- The reliance on a 72B MLLM for both expert workflow generation and critic scoring introduces bias and significant computational overhead, with no sensitivity analysis provided.
- The Stage-3 reward is computed from workflow text rather than the final edited image, so it may miss visual artifacts, color inaccuracies, or other perceptual quality issues.
- No human evaluation is conducted; automated metrics may not fully capture instruction-following quality or user satisfaction.
- The paper does not discuss failure cases, cascading tool-execution errors, or performance across multiple random seeds; reproducibility is hampered by missing/redacted experimental details.
- Potential negative societal impacts of flexible image editing (e.g., creating misleading or harmful imagery) are not discussed, and no safeguards or mitigation strategies are proposed.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 69,233
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 65,137
- Completion tokens: 23,682
- Reasoning tokens reported: 16,453
- Total tokens: 92,915
- Estimated total: $0.01576161

Full individual reviews and raw JSON responses are in `review_bundle.json`.
