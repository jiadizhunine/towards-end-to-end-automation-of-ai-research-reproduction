# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B200.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.022933**

## Final Meta-review

The paper introduces a decision-focused learning (DFL) framework that employs conditional diffusion models to represent the distribution of uncertain optimization parameters, replacing point predictions. It proposes two gradient estimators: a reparameterization estimator that backpropagates through the diffusion sampling process and a score-function estimator that approximates the gradient of the log-likelihood using the ELBO gradient and importance sampling across diffusion timesteps. Experiments on synthetic allocation, power scheduling, and stock portfolio optimization demonstrate that the diffusion-based DFL methods outperform deterministic and Gaussian DFL baselines, with the score-function estimator drastically reducing GPU memory usage while maintaining decision quality.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 2 | 2.000 | 0.000 | 2-2 |
| Clarity | 2 | 2.000 | 0.000 | 2-2 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 2 | 2.000 | 0.000 | 2-2 |
| Presentation | 2 | 2.000 | 0.000 | 2-2 |
| Contribution | 3 | 2.600 | 0.490 | 2-3 |
| Overall | 4 | 3.600 | 0.490 | 3-4 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Novel integration of diffusion models into decision-focused learning, enabling multi-modal uncertainty modeling in stochastic optimization.
- The score-function estimator avoids backpropagating through the diffusion sampler, yielding a large memory reduction (60.75 GB to 0.13 GB) while retaining competitive decision quality.
- Empirical evaluation across three distinct tasks consistently shows improvements over deterministic and Gaussian DFL baselines.
- Detailed derivations connecting diffusion sampling, ELBO, and KKT-based implicit differentiation are provided, along with a code release.

### Weaknesses

- The central approximation ∇_θ log P_θ(y|x) ≈ ∇_θ ELBO(y|x;θ) is heuristic and lacks theoretical justification, with no bias or consistency analysis beyond a simple linear toy example.
- The derivation of the weighted-ELBO estimator in Eq. (13) is mathematically questionable: it detaches the θ-dependent importance weight w_θ(y) and moves a θ-dependent matrix inside the expectation, introducing an unquantified and potentially large bias.
- No comparison is made with existing expressive generative DFL baselines such as gen-DFL (normalizing flows) or score-function DFL methods, weakening the claim of being the first or best generative DFL approach.
- Experimental details are incomplete, including missing diffusion hyperparameters (number of steps T, noise schedule), exact training loops, and clarification of the importance sampling update rule for p_t; several results lack error bars or statistical significance tests, and some formatting issues (e.g., zero standard errors) reduce clarity.
- The method is restricted to convex, differentiable optimization problems with affine constraints, relying on KKT conditions; it does not address combinatorial or non-convex decision tasks.
- The paper omits training time and total compute as practical overhead indicators, focusing only on GPU memory.

### Questions

- Under what conditions does ∇_θ ELBO(y|x;θ) approximate ∇_θ log P_θ(y|x)? Can the authors provide a bias bound or formal consistency analysis, especially for deep conditional diffusion models?
- In Eq. (13), why is it valid to detach w_θ(y) and move u(θ) inside the expectation? What is the induced bias, and how does it affect gradient estimation and convergence?
- Why is the gen-DFL (normalizing flow) baseline, which is cited in related work, not included in the comparisons? Would the diffusion model still retain an advantage against a strong generative DFL baseline?
- What are the exact values of diffusion steps T, sampled timesteps k, and the reverse sampling procedure used in training and inference? How are the importance sampling probabilities p_t estimated and updated?
- In the stock portfolio experiment, why do baselines achieve near-zero returns while diffusion DFL achieves about 4%? Is there any data leakage or evaluation metric inconsistency, and what is the risk parameter α?
- Can the authors provide confidence intervals or pairwise significance tests for the results in Table 1 to support the claimed superiority of diffusion DFL?
- How does the proposed score-function estimator compare empirically to an unbiased REINFORCE estimator using denoising score matching? Does the ELBO surrogate suffer from higher variance or bias?

### Limitations

- The score-function gradient is biased due to the ELBO approximation; no theoretical guarantees are provided for its bias, variance, or convergence.
- The detachment of the importance weight in Eq. (13) is a heuristic that may lead to incorrect gradients, with no analysis of its impact.
- Diffusion models require iterative sampling at inference time, which can be computationally expensive and limit real-time decision-making applicability.
- The method is limited to convex optimization problems with differentiable (affine) constraints, excluding many decision problems in practice.
- The experiments cover only small- to medium-scale problems (dimensions up to 50); scalability to larger decision spaces is not demonstrated.
- The synthetic task lacks contextual features x, so it does not adequately test the conditional modeling capabilities of the proposed framework.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 125,414
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 121,318
- Completion tokens: 21,202
- Reasoning tokens reported: 15,046
- Total tokens: 146,616
- Estimated total: $0.02293255

Full individual reviews and raw JSON responses are in `review_bundle.json`.
