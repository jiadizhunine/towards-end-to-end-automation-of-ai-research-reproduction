# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B119.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **3/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.017662**

## Final Meta-review

The paper proposes Vision-EKIPL, a reinforcement learning (RL) framework for multimodal large language models (MLLMs) on visual reasoning tasks. It augments GRPO by sampling additional candidate actions from external auxiliary models (GPT-4o, Gemini-1.5-Pro), pooling them with policy-model samples, selecting the top-G actions by reward, and using these to compute advantages and update the policy. Experiments on visual counting, structure perception, and spatial transformation with Qwen2-VL 2B/7B show moderate improvements over Reason-RFT and other baselines, faster convergence, and improved Pass@K. The authors argue this expands the reasoning boundary.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 2.600 | 0.490 | 2-3 |
| Quality | 2 | 1.800 | 0.400 | 1-2 |
| Clarity | 2 | 2.000 | 0.000 | 2-2 |
| Significance | 2 | 2.400 | 0.490 | 2-3 |
| Soundness | 2 | 1.800 | 0.400 | 1-2 |
| Presentation | 2 | 2.000 | 0.000 | 2-2 |
| Contribution | 2 | 2.000 | 0.000 | 2-2 |
| Overall | 3 | 3.600 | 0.490 | 3-4 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- The idea of mixing actions from external expert models into RL training is novel and could broaden exploration beyond the policy's own sampling distribution.
- Empirical results show consistent, albeit modest, gains over Reason-RFT across multiple visual reasoning tasks and two model scales, including out-of-domain generalization.
- The paper reports faster convergence and useful diagnostics (action-source ratio, Pass@K) that shed light on training dynamics.
- The authors acknowledge API cost and propose future work on open-source alternatives, showing practical awareness.

### Weaknesses

- The central theoretical justification is flawed: the actual algorithm uses the standard GRPO ratio π_new/π_old even when actions are sampled from external models and top-G filtered, while the appendix derives that the correct importance ratio is π_new/q (with q the full proposal distribution). No importance weights are applied, so the policy update is biased and the claimed unbiasedness is unsupported.
- The top-G reward filtering further changes the proposal distribution in a way that is not accounted for, and no effective sample size or bias diagnostics are reported.
- No ablation compares Vision-EKIPL to simple supervised fine-tuning on the top-G external actions (without the GRPO advantage term), so the contribution of the RL objective over distillation is not isolated.
- The use of proprietary models (GPT-4o, Gemini-1.5-Pro) introduces potential test-set contamination, high API costs, and reproducibility issues; no contamination analysis or comparison with open-source auxiliary models is provided.
- Missing ablations for key design choices (number of auxiliary models M, group size G, choice of external models, KL penalty), and no standard deviations or statistical significance tests despite three repeats.
- The reported improvements are often 1–4 absolute percentage points, which may be within noise; textual claims sometimes overstate the gains.
- Several implementation details are ambiguous or missing, including exact prompts, reward definitions, whether a CoT-SFT stage is used before RL, and how π_new/π_old is computed for low-probability external actions.

### Questions

- Why does the algorithm use the uncorrected ratio π_new/π_old in Eq. (3) despite Appendix A proving that the correct importance ratio for a general proposal q is π_new/q? Is the estimator intentionally biased, or is the appendix meant to justify a different implementation that is not reported?
- How is the proposal distribution q(o|s) after top-G reward filtering defined, and how would importance weights be computed in practice? What are the effective sample sizes during training?
- Would simple SFT on the top-G external actions (selected by reward) achieve similar or better performance than the proposed GRPO-based method? Has this ablation been run?
- How are the actions sampled from external models prompted to fit the required <think> and <answer> format? Is the reward function identical to Reason-RFT for all tasks?
- What are the standard deviations and confidence intervals for the reported accuracies? Are the gains statistically significant?
- Have the authors checked for test-set contamination in GPT-4o/Gemini generations for the Reason-RFT-CoT benchmark, and would that affect the OOD generalization claims?
- What is the total API cost and wall-clock time compared to Reason-RFT, and how do the choices of M and G affect performance and cost?
- Does Vision-EKIPL include a CoT-SFT warm-up stage? If not, how is the comparison to Reason-RFT (which uses CoT-SFT) fair?
- Have the authors experimented with open-source auxiliary models (e.g., larger Qwen variants) and would the gains persist without proprietary APIs?

### Limitations

- Reliance on proprietary external models introduces monetary, latency, and reproducibility barriers, and may not be feasible for many researchers.
- The theoretical soundness is compromised by the absence of the importance-sampling correction developed in the appendix, making the policy update biased and the claimed unbiasedness unsubstantiated.
- External-model outputs may contain biases or hallucinations; the paper does not analyze failure modes or the risk of learning from flawed expert actions beyond reward thresholds.
- Evaluation is limited to three visual reasoning tasks with Qwen2-VL 2B/7B; generalizability to other MLLMs, tasks, or domains is unknown.
- The method assumes a verifiable reward function, which may not hold for open-ended reasoning tasks.
- No code or data release details are provided, hindering reproducibility.
- The observed performance gains are modest and may be partly attributable to distillation from stronger models rather than the RL mechanism itself.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 87,404
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 83,308
- Completion tokens: 21,382
- Reasoning tokens reported: 14,299
- Total tokens: 108,786
- Estimated total: $0.01766155

Full individual reviews and raw JSON responses are in `review_bundle.json`.
