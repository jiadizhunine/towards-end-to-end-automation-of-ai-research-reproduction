# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B115.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **5/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 3, 'Reject': 2}
- Estimated API cost: **$0.014558**

## Final Meta-review

The paper proposes Training-Free GRPO, a method that adapts frozen LLM agents to specialized tasks by iteratively distilling 'semantic advantages' (natural language experiences) from group rollouts and maintaining an external experience library injected into prompts at inference time. The method is evaluated on mathematical reasoning (AIME24/25) and web searching (WebWalkerQA), showing improvements over ReAct baselines with only 100 training samples and ~$18 cost, and is compared against fine-tuned 32B models that require $10K+ training costs. The paper includes ablations on group computation, ground-truth dependence, and cross-domain transfer.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.800 | 0.400 | 3-4 |
| Quality | 3 | 2.600 | 0.490 | 2-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 3 | 2.600 | 0.490 | 2-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 2.600 | 0.490 | 2-3 |
| Overall | 5 | 5.200 | 0.980 | 4-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel and well-motivated idea: shifting RL policy optimization from parameter space to context space via an evolving token prior (experience library).
- Extremely cost-effective: achieving competitive results with ~$18 learning cost versus $10,000+ for parameter-tuning baselines is compelling for practical deployment.
- Preserves generalization: since the base model is frozen, cross-domain performance is maintained, avoiding the specialization trade-off seen in fine-tuned models.
- Comprehensive ablations: directly generated experiences, removing group computation, removing ground truths, and cross-domain transfer analysis.
- Detailed cost analysis comparing training and inference costs with fine-tuning approaches, highlighting the economic advantages.
- Case studies in the appendix provide concrete illustrations of how learned experiences improve reasoning trajectories.

### Weaknesses

- The primary comparison against fine-tuned baselines (ReTool, AFM) is confounded: these baselines use Qwen2.5-32B, a much weaker base model than DeepSeek-V3.1-Terminus used by the proposed method. The performance differences are likely dominated by base model capability rather than the method itself.
- The connection to GRPO is somewhat loose; the method is essentially iterative prompt refinement with group-based feedback, not RL in a strict sense.
- Evaluation is limited to two domains (math and web) with a small number of benchmarks, and the web searching ablation uses only 51 instances.
- No statistical significance testing or confidence intervals are reported, making it difficult to assess whether the observed improvements are robust.
- The method's effectiveness appears highly model-dependent: it fails on QwQ-32B for web searching (25.5% vs 27.5% baseline), suggesting limited generality across model families.
- The experience library update mechanism (Add/Delete/Modify/Keep) is described at a high level; no analysis of the quality, stability, or size evolution of the learned experiences is provided.
- No comparison against simpler training-free baselines (e.g., Reflexion, Self-Refine, ICRL) on the same benchmarks and base models.
- Inference cost per query is higher than for fine-tuned small models, which may be a drawback for high-volume or latency-sensitive applications.

### Questions

- How does Training-Free GRPO perform when applied to the same base model (e.g., Qwen2.5-32B-Instruct) that the fine-tuned baselines (ReTool, AFM, SimpleTIR) use? This would provide a fairer comparison isolating the method's contribution from base model capability.
- What is the variance across different random seeds for the 100-sample training set? Are the reported improvements statistically significant (e.g., with bootstrap confidence intervals or paired tests)?
- How does performance scale with the number of training samples (e.g., 50, 200, 500) and epochs (e.g., 1, 5, 10)? Is there a plateau or overfitting risk?
- Why does Training-Free GRPO fail on QwQ-32B for web searching? Is this due to the model's weaker tool-use capabilities, the reward signal quality, or the experience extraction quality?
- How sensitive is the method to the specific prompt templates used for summarization, advantage extraction, and experience update? Have alternative prompt formulations been tested?
- What is the distribution of Add/Delete/Modify/Keep operations across training steps? How does the experience library size evolve, and is there a risk of context overflow?
- How does Training-Free GRPO compare against other training-free methods like Reflexion, Self-Refine, or in-context RL (ICRL) on the same benchmarks and base models?
- In the ablation without ground truths, what reward signal is used to identify winners and losers within a group? Could this lead to reward hacking or circular self-reinforcement?

### Limitations

- The method's effectiveness is strongly dependent on the base LLM's inherent capabilities. For models below a certain capability threshold (e.g., QwQ-32B on web tasks), the method can actually degrade performance, limiting its applicability to weaker or smaller models.
- The evaluation is limited to two domains (mathematical reasoning and web searching) and specific benchmarks. Broader validation across more diverse agentic tasks (e.g., coding, tool use, multi-step planning) is needed.
- The comparison against parameter-tuning methods is confounded by model scale differences. The paper does not isolate the effect of the method from the effect of using a much larger base model.
- The experience library maintenance relies on LLM judgment, which may be unstable, non-reproducible, or sensitive to prompt variations. No analysis of this stability is provided.
- No statistical significance testing or confidence intervals are reported, making it difficult to assess whether the observed improvements are robust.
- The paper does not discuss potential negative societal impacts, such as the risk of amplifying biases present in the training data or the potential for misuse of the learned experiences in harmful applications.
- The cost comparison focuses on API pricing for DeepSeek; results may vary significantly with other API providers or self-hosted inference.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 87,052
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 78,092
- Completion tokens: 12,857
- Reasoning tokens reported: 0
- Total tokens: 99,909
- Estimated total: $0.01455793

Full individual reviews and raw JSON responses are in `review_bundle.json`.
