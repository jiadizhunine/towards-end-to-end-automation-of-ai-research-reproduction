# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B049.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.014558**

## Final Meta-review

The paper addresses the problem of post-training generative models in extremely sparse reward settings, where the base model receives near-zero reward signal and reward oracle evaluations are expensive. The authors propose BaNEL (Bayesian Negative Evidence Learning), which trains a separate generative model on failed (zero-reward) samples and uses it to define a rejection region via likelihood ratios, filtering out samples similar to previously seen failures before querying the reward oracle. The method allows multiple parameter updates per reward evaluation and uses distillation to make sequential filtering practical. The paper provides conceptual analysis of why existing methods (policy gradient, GFlowNets, intrinsic reward methods) fail in this regime, and evaluates BaNEL on MNIST digit transformation, adversarial attacks on a toy language model, and GSM8K reasoning tasks, showing improvements over count-based and RND baselines in terms of success rate per number of reward evaluations.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 4.000 | 0.000 | 4-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.400 | 0.490 | 3-4 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.400 | 0.490 | 3-4 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.400 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The problem setting is important, well-motivated, and underexplored: learning from purely negative samples with expensive reward oracles is highly relevant to applications like theorem proving, drug discovery, and algorithmic reasoning.
- The core idea of training a generative model on failures and using it for Bayesian-style rejection filtering is novel and conceptually elegant.
- The paper provides clear reasoning for why existing sparse-RL methods (policy gradient, negative RL, intrinsic rewards, GFlowNets) fail in this extreme sparsity regime.
- Experimental evaluation spans diverse domains (images, adversarial attacks, reasoning), with consistent improvements over baselines and useful ablations.
- The method demonstrates a compute-scaling property, improving with additional training epochs for the failure model, which is a valuable insight.
- The authors are honest about limitations, including non-monotonic success rates and computational costs.

### Weaknesses

- Theoretical analysis is informal; no strong guarantees on convergence, sample complexity, or robustness to misclassification of the rejection region are provided.
- Absolute success rates remain extremely low (e.g., 1e-21 on MNIST), raising questions about practical significance despite large relative gains.
- GSM8K-Hard results are mixed, with BaNEL underperforming RND on one of six problems without deep analysis.
- Maintaining a separate generative model p_phi at each round is computationally expensive; scalability to very large language models is not demonstrated.
- The filter factor f requires task-specific tuning (ranging from 2 to 16), and no principled selection method is provided.
- The success rate peaks and then declines, with no clear stopping criterion, which undermines the NRE efficiency claim in practice.
- The claimed equivalence between the sequential filtering algorithm and the distillation-based algorithm is not rigorously proven.

### Questions

- Can you provide theoretical guarantees on the convergence or sample complexity of BaNEL? Under what conditions on the failure model p_phi is improvement in success rate guaranteed?
- What is a principled way to select the filter factor f, given its high variance across tasks (f=2 for MNIST, f=16 for GSM8K)?
- How does the method perform when failures do not exhibit learnable regularities (e.g., essentially random failures)?
- Given the non-monotonic success rate, what practical stopping criterion would you recommend for deployment?
- How does the computational cost of training p_phi compare to the savings in reward evaluations, especially for large models? Could LoRA or other parameter-efficient methods make this practical?
- Why does BaNEL underperform RND on GSM8K problem 510, and what does this reveal about the method's limitations?
- How would the results differ if using the final model's success rate instead of the cumulative best?
- Could BaNEL be combined with other exploration methods (e.g., RND) for further gains, or are they fundamentally incompatible?

### Limitations

- The method requires likelihood-based generative models, limiting applicability to architectures where exact likelihood computation is tractable.
- Training an additional generative model at each round is computationally expensive and may be prohibitive for large-scale models.
- Success rate is not monotonically increasing, making stopping criteria unclear without additional reward evaluations.
- The absolute success rates achieved in some experiments (especially MNIST) are extremely small, limiting immediate practical impact.
- The method assumes failures have learnable regularities; for tasks where failures are essentially random, the method may not provide benefits.
- The adversarial attack experiment, while in a toy setting, demonstrates potential misuse of the method for discovering model vulnerabilities, which should be considered in broader deployment contexts.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 92,350
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 83,390
- Completion tokens: 10,208
- Reasoning tokens reported: 0
- Total tokens: 102,558
- Estimated total: $0.01455793

Full individual reviews and raw JSON responses are in `review_bundle.json`.
