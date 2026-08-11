# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B115.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.016103**

## Final Meta-review

The paper proposes Training-Free GRPO, a non-parametric alternative to GRPO that keeps the LLM frozen and iteratively refines an external experience library injected into the context. Instead of gradient updates, it computes a semantic group-relative advantage by asking the LLM to summarize and compare rollouts, then updates the experience library with add/delete/modify/keep operations. The method is evaluated on AIME24/AIME25 math reasoning and WebWalkerQA web searching, showing improvements over ReAct baselines with substantially lower training cost, and it includes ablations on ground-truth availability, group size, and cross-domain transfer.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 2.800 | 0.400 | 2-3 |
| Quality | 2 | 2.000 | 0.000 | 2-2 |
| Clarity | 2 | 2.200 | 0.400 | 2-3 |
| Significance | 2 | 2.000 | 0.000 | 2-2 |
| Soundness | 2 | 2.000 | 0.000 | 2-2 |
| Presentation | 2 | 2.200 | 0.400 | 2-3 |
| Contribution | 2 | 2.000 | 0.000 | 2-2 |
| Overall | 4 | 4.000 | 0.000 | 4-4 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- The core idea of shifting GRPO-style optimization from parameter space to context space via an evolving experience library is original and timely, directly addressing the prohibitive cost of fine-tuning large models.
- The method is cost-effective, requiring no gradient updates and using only API calls, making it appealing for large frozen models.
- The paper includes useful ablations (directly generated experiences, without ground truths, without group computation) that help attribute the gains to the proposed components.
- The cross-domain transfer analysis highlights a potential advantage over parameter-tuned specialists, which often degrade in out-of-domain settings.

### Weaknesses

- The main comparisons are not apples-to-apples: Training-Free GRPO on DeepSeek-V3.1-Terminus is compared against RL-trained 32B models, so the gains could reflect the base model's superiority rather than the proposed method; a same-backbone fine-tuned baseline is missing.
- Reported results lack variance, confidence intervals, or significance tests; for differences like +1.1% on AIME25, it is unclear whether the improvement is statistically meaningful, and the web ablation uses only 51 instances.
- The method is underspecified: exact prompts for summarization, semantic advantage extraction, and experience updates are only shown in redacted appendices, and key design choices (group size, reward formulation, number of epochs) are not thoroughly justified.
- No comparisons with strong training-free baselines such as Reflexion, Self-Refine, or in-context RL; the 'Directly Generated Experiences' control is insufficient because it does not match the iterative process or the group-comparison mechanism.
- The method relies heavily on the base LLM's ability to introspect and extract reliable semantic advantages, which may not hold for weaker models (as demonstrated by QwQ-32B); the approach is not theoretically grounded as RL and offers no convergence guarantees.
- Potential data contamination is not addressed: DAPO-100 may contain problems similar to or overlapping with AIME benchmarks, which could inflate out-of-domain improvements.

### Questions

- How exactly is the scalar reward computed in each domain? Is the ground-truth answer used directly to assign 0/1 rewards, or is a separate reward model involved? Please provide the exact scoring prompt.
- Have the authors checked for overlap or semantic similarity between DAPO-100 and AIME24/25 test problems? If so, what was the contamination rate?
- What are the confidence intervals or p-values for the main results (e.g., AIME25 +1.1%, WebWalkerQA +4.6%) given the limited number of test items and 32/51 samples?
- How does Training-Free GRPO compare empirically to other training-free methods like Reflexion, Self-Refine, or in-context RL on AIME and WebWalkerQA, under the same base model and compute budget?
- How are the add/delete/modify/keep operations on the experience library implemented, and what prevents the library from growing beyond context limits or accumulating contradictory experiences?
- Why does QwQ-32B degrade with Training-Free GRPO? Is there a minimum base-model capability threshold for the method to be effective?
- Could you provide results with Training-Free GRPO applied to Qwen2.5-32B-Instruct under the same setup as ReTool to enable a fair comparison with parameter-tuning methods?

### Limitations

- The method still requires a reward signal (often ground truth) to achieve its best performance; without ground truths the gains are notably smaller, so the 'training-free' label is somewhat misleading.
- The effectiveness appears highly dependent on the underlying model's capability; it fails to improve QwQ-32B on web searching, suggesting it is not universally applicable.
- The learned experience library may be model-specific and task-specific, and may need manual curation or filtering as it grows; there is no formal convergence or correctness guarantee.
- Evaluation is limited to two domains (math and web searching); no results on long-horizon agentic tasks, code generation, or safety-critical applications are provided.
- The cost analysis focuses on API pricing and may not account for full context overhead in repeated rollouts; a local open-source deployment could have different cost characteristics.
- No public code, data, or detailed prompts are provided, making the work difficult to reproduce or build upon.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 75,453
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 71,357
- Completion tokens: 21,793
- Reasoning tokens reported: 15,157
- Total tokens: 97,246
- Estimated total: $0.01610349

Full individual reviews and raw JSON responses are in `review_bundle.json`.
