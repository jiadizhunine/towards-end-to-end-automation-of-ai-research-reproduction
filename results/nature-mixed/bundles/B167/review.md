# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B167.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.012945**

## Final Meta-review

This paper presents Lego-Edit, an agent-based framework for instruction-based image editing that uses a fine-tuned Multi-modal Large Language Model (MLLM) as a Builder agent to orchestrate a suite of model-level editing tools (Bricks). The framework introduces two main contributions: (1) a model-level toolkit of task-specialized editing models that enable fine-grained composition of editing actions, and (2) a three-stage progressive reinforcement learning strategy (SFT, GT-based RL, and GT-free RL with critic feedback) that enhances the Builder's reasoning and tool composition abilities using unlabeled open-domain data. Experiments on GEdit-Bench and ImgEdit-Bench demonstrate state-of-the-art performance, with additional demonstrations of zero-shot adaptation to new tools and user feedback without retraining.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.600 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.200 | 0.400 | 3-4 |
| Significance | 4 | 3.600 | 0.490 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.200 | 0.400 | 3-4 |
| Contribution | 3 | 3.400 | 0.490 | 3-4 |
| Overall | 7 | 6.800 | 0.400 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel and well-motivated approach: Decomposing image editing into model-level atomic tools orchestrated by an RL-trained MLLM agent is a fresh perspective that directly addresses the generalization limitations of end-to-end instruction-based editing methods.
- Well-designed three-stage progressive RL training strategy that gradually reduces reliance on ground-truth data, culminating in a GT-free critic-based reward stage that enables generalization to open-domain instructions.
- Strong empirical results: Achieves state-of-the-art performance on two widely-used benchmarks (GEdit-Bench and ImgEdit-Bench), with particularly strong results on complex/hybrid editing tasks.
- Comprehensive ablation studies validating key design choices: task-specialized tools outperform multi-task LoRA approaches, and each RL training stage contributes to performance gains.
- Demonstrated practical advantages including lower latency than end-to-end methods and the ability to integrate new tools without retraining.
- Compelling qualitative results illustrating zero-shot adaptation to flexible instructions, new tools, and user feedback.
- The paper is well-written and clearly organized, with helpful figures illustrating the framework and qualitative comparisons.

### Weaknesses

- Evaluation relies almost exclusively on VIEScore (an MLLM-based metric using GPT-4o), without human evaluation or complementary metrics (e.g., LPIPS, CLIP score), which is a significant gap for an image editing paper.
- The 'zero-shot' claims are somewhat overstated; the Builder is trained on related tasks, so its ability to handle novel instructions is arguably compositional generalization rather than true zero-shot capability.
- The Stage 3 critic model (Qwen2.5-VL-72B) is also used for generating ground-truth workflows, which could introduce systematic bias. The reliability and failure modes of this critic are not thoroughly analyzed.
- Limited analysis of failure cases, error propagation in multi-step workflows, and robustness when individual tools fail.
- The comparison with GPT-4o as an agent may be unfair, as GPT-4o is used zero-shot without fine-tuning while the Builder is specifically trained on the tool interfaces.
- Training data scale choices (500 SFT pairs, 20K/50K RL pairs) appear arbitrary and lack sensitivity analysis.
- The paper does not disclose the total training computational cost, including the Stage 3 critic model inference over 50K samples.
- Some tool descriptions are vague in the main text (e.g., 'three additional tools' and 'one additional tool' are not clearly specified until the appendix).

### Questions

- Since Qwen2.5-VL-72B was used for both generating ground-truth workflows and as the Stage 3 critic, could there be systematic bias? How would results differ with an independent critic model? Was the critic's judgment validated against human annotations?
- How was the 50K unlabeled instruction dataset for Stage 3 constructed? Were instructions filtered for diversity or difficulty? How representative are they of real-world user instructions?
- Can you clarify the distinction between compositional generalization (combining known atomic skills) and true zero-shot capability? What percentage of GEdit-Bench instructions require genuinely novel tool combinations not seen in training?
- Have you considered human evaluation? Given that VIEScore is an MLLM-based metric, how confident are you that the reported improvements reflect actual perceptual quality improvements for human users?
- What happens when the Builder generates an executable but semantically incorrect workflow (e.g., wrong tool parameters that still run)? How does the reward structure in Stage 3 address this?
- How does the framework handle cases where individual tools fail or produce poor intermediate results? Is there any error recovery mechanism in the Executor?
- What is the distribution of workflow lengths (number of tools invoked) for typical instructions? How does the framework handle very complex instructions that might require many steps?
- Could you provide a more detailed comparison with ComfyAgent, specifically in terms of tool invocation flexibility and performance on open-domain instructions?
- The paper reports results from a single run. What is the variance across multiple runs with different random seeds? Is the improvement from Stage 2 to Stage 3 statistically significant?
- What is the total training time and computational cost (GPU hours) for the full three-stage pipeline, including the critic model inference in Stage 3?

### Limitations

- The system's generalization is bounded by the available tool set; instructions requiring capabilities outside the tool library cannot be executed.
- The framework's performance is bounded by the quality of the individual editing tools. Error propagation in multi-step workflows and tool failure recovery are not analyzed.
- The Stage 3 RL training relies on a large critic model (Qwen2.5-VL-72B) for reward computation, which adds significant computational overhead and may be a reproducibility bottleneck.
- The evaluation is limited to two benchmarks, and the paper does not provide a thorough failure case analysis or broader testing on diverse real-world user instructions.
- All training data is sourced from OmniEdit, which may limit instruction diversity despite the Stage 3 unlabeled data.
- The framework requires training multiple specialized models (Builder, RES, SOS, ADD-PRED, 5 LoRA adapters), which is computationally expensive and may hinder reproducibility.
- Potential negative societal impact: The framework could be misused for creating misleading or harmful edited images (e.g., deepfakes, misinformation). The paper does not discuss safeguards or mitigation strategies.
- The paper does not address the environmental impact of training multiple specialized models and running a large critic model for RL training.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 77,583
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 68,623
- Completion tokens: 11,832
- Reasoning tokens reported: 0
- Total tokens: 89,415
- Estimated total: $0.01294527

Full individual reviews and raw JSON responses are in `review_bundle.json`.
