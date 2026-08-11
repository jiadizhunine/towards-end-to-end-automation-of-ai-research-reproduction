# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B125.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.026816**

## Final Meta-review

The paper proposes LLaVA-Critic-R1, a multimodal critic trained by reformulating preference-labeled critic data into a verifiable pairwise-judgment task and applying GRPO to a base VLM, without using GPT-generated rationales. The authors report that critic-only RL training improves both critic and policy performance across 26 visual benchmarks, and that the same model can be used for test-time self-critic scaling, outperforming majority vote and base-model critics. They introduce LLaVA-Critic-R1+ by applying the procedure to a stronger reasoning VLM, and ablate training strategies, SFT-vs-RFT, and the sources of policy improvement.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 2 | 2.400 | 0.490 | 2-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 2 | 2.400 | 0.490 | 2-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.200 | 0.400 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Simple, clean idea: converting preference labels into a verifiable RL objective avoids distillation from GPT rationales and yields a unified policy/critic model.
- Broad evaluation across 26 benchmarks and multiple base models (Qwen-2.5-VL, ThinkLite-VL, MiMo-VL, LLaMA-3.2-Vision) supports the generality of the approach.
- Thoughtful ablations separate the effect of format reward, data mixing/training order, and SFT-vs-RFT, helping attribute the policy improvement to structured thinking and enhanced perception.
- Test-time self-critic scaling is practical and shows consistent gains over majority voting and base-model critics on five reasoning benchmarks.
- Demonstration that critic training can preserve or even improve policy ability while policy training may degrade critic ability is an interesting empirical finding.
- The paper includes additional base-model experiments in the appendix, strengthening the claims of generalizability.

### Weaknesses

- Missing key control: no GRPO run on 40k non-critic instruction-QA data with the same format reward, so policy gains cannot be clearly attributed to preference-judgment data versus RL on any diverse instruction data; the Format-RFT ablation only controls format, not data content.
- Reproducibility is limited: GRPO hyperparameters (learning rate, batch size, group size, steps, KL coefficient), compute budget, and code are not provided; all results appear single-run with no error bars or statistical significance tests.
- Potential data contamination is not addressed: the 40K critic data from VLFeedback, RLHF, and RLHF-V may overlap with evaluation benchmarks such as VLRewardBench, MM-RLHF, and general VQA benchmarks.
- Test-time scaling baselines are weak: self-critic is compared only with majority vote and base-model critics, not with a dedicated SFT-trained critic or a strong external reward model; the effect of forcing the thinking template on baselines is not analyzed.
- Several claims are overstated or inconsistent: e.g., the abstract claims LLaVA-Critic-R1+ advances policy 'without sacrificing critic quality,' but Table 7 shows its reward average (64.9) is lower than the critic-only model (68.1); the '+13.8%' self-critic gain is not clearly specified.
- Critic evaluation is narrow (only VLRewardBench and MM-RLHF), and no analysis of tie handling, positional bias, or label noise in the 40K data is provided.

### Questions

- Can you provide a control experiment running the same GRPO pipeline on 40k policy or generic instruction-following data with exact-answer rewards and format reward, to prove the policy gains are specific to critic data rather than RL+thinking in general?
- What are the exact training hyperparameters (learning rate, batch size, GRPO group size, number of steps, KL coefficient) and compute budget? Were multiple seeds or runs averaged, and what is the variance?
- How were the 40K critic instances selected from VLFeedback, RLHF, and RLHF-V? What is the tie distribution, and how are ties handled in reward computation? Were the two response orders randomized?
- Was any contamination or overlap analysis performed between the 40K training data and the 26 evaluation benchmarks (especially VLRewardBench and MM-RLHF)?
- How does self-critic Best-of-N compare against a dedicated SFT-trained critic (e.g., LLaVA-Critic) or a strong external reward model under the same protocol? What is the compute cost of 128 generations per question?
- Can you clarify the '+13.8%' self-critic improvement formula and the discrepancy between the abstract and Table 7 regarding 'without sacrificing critic quality'?

### Limitations

- No statistical significance testing or multiple-seed results are reported; many benchmark gains are small and may be within evaluation noise.
- Training details and code are missing, limiting reproducibility.
- Experiments are limited to 7B/11B scale; transfer to larger VLMs is untested.
- Potential contamination between training data and evaluation benchmarks is not analyzed.
- Test-time self-critic scaling requires 128 generations per question and remains far below the ground-truth oracle, indicating limited critic ability.
- Critic training data is only 40K and inherited from prior work; label noise and biases are not characterized.
- Possible negative societal impacts of a dual actor-critic model for automated evaluation are not discussed.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 135,570
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 131,474
- Completion tokens: 29,994
- Reasoning tokens reported: 22,167
- Total tokens: 165,564
- Estimated total: $0.02681615

Full individual reviews and raw JSON responses are in `review_bundle.json`.
