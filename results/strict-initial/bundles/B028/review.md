# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B028.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.042047**

## Final Meta-review

The paper proposes an iterative self-supervised fine-tuning method for diffusion models to sample from tilted distributions, defined as the base data distribution reweighted by a reward/likelihood. The method alternates between sampling from the current h-transform-guided reverse SDE, rejecting samples via path-based importance weights (approximate Radon-Nikodym derivative times reward), and updating the h-transform using a supervised score-matching loss on accepted endpoints. The authors prove a descent property for an idealized version of the algorithm and demonstrate it on a 2D toy, MNIST class-conditional sampling, Flowers super-resolution, and Stable Diffusion reward fine-tuning, highlighting memory savings by avoiding backpropagation through the sampling process.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 2 | 2.200 | 0.400 | 2-3 |
| Quality | 2 | 2.000 | 0.000 | 2-2 |
| Clarity | 1 | 1.600 | 0.490 | 1-2 |
| Significance | 2 | 2.000 | 0.000 | 2-2 |
| Soundness | 2 | 2.000 | 0.000 | 2-2 |
| Presentation | 1 | 1.600 | 0.490 | 1-2 |
| Contribution | 2 | 2.000 | 0.000 | 2-2 |
| Overall | 4 | 4.000 | 0.000 | 4-4 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Self-supervised framework: estimates the h-transform without requiring samples from the tilted distribution, overcoming a key limitation of supervised h-transform learning.
- Memory efficiency: avoids backpropagating through the full SDE trajectory, enabling fine-tuning of large text-to-image models on a single 16-24 GB GPU.
- Path-based importance weighting: integrates both reward and path probability, and the toy experiment suggests it mitigates mode collapse compared to reward-only selection.
- Theoretical attempt: provides a theorem that the iterative procedure decreases a free-energy objective, offering a formal framing.
- Broad applicability: evaluated on class-conditional generation, super-resolution, and text-to-image reward fine-tuning.

### Weaknesses

- The proof of the central descent theorem (Theorem 5(iii)) is flawed: the path measure equality is not rigorously justified, especially the mismatch between the terminal distribution of the guided SDE (base Gaussian) and the tilted forward distribution; the assertion that the score-matching minimizer yields the desired path measure is underdeveloped and likely incorrect.
- The path-wise Radon-Nikodym derivative is used to approximate the marginal density ratio, introducing a systematic bias that is not analyzed or bounded; this approximation may be inaccurate for discrete DDPM samplers used in practice.
- Descent guarantee only holds for exact minimization and fixed acceptance constant c; the practical algorithm uses approximate gradient updates, replay buffers, and adaptive c, so the theory does not apply to the implemented method.
- Experimental results are weak: on MNIST, Importance FT achieves lower expected reward than online fine-tuning, and on text-to-image, it underperforms both DPOK and Adjoint Matching on most prompts with also lower diversity; no error bars or multiple seeds are reported.
- Super-resolution experiment lacks quantitative evaluation (e.g., PSNR, LPIPS) and comparisons to existing posterior sampling baselines like DPS or DDRM, making it hard to assess usefulness.
- The paper has severe presentation issues: garbled equations, undefined notation (e.g., RND), duplicated theorem statements, incomplete sentences, and inconsistencies (e.g., DPOK memory reported as 34GB while text claims it runs on 24GB), harming reproducibility.
- Hyperparameters such as the acceptance threshold c and KL regularization coefficient are chosen heuristically with no sensitivity analysis, leaving robustness unclear.

### Questions

- Can the authors provide a rigorous proof of Theorem 5(iii) accounting for the terminal distribution mismatch and the discrete-time approximation?
- What is the exact bias introduced by using the path-wise Radon-Nikodym derivative instead of the marginal density ratio, and can it be bounded or corrected?
- How does the adaptive choice of acceptance threshold c affect the stationary distribution and the descent property? Is there a principled way to set it?
- Why does Importance FT achieve lower expected reward than online fine-tuning on MNIST? Does this indicate the descent property fails in practice or that the objective is different?
- For super-resolution, how does the method compare to standard baselines like DPS or DDRM quantitatively (PSNR, LPIPS)?
- How sensitive are results to hyperparameters (acceptance rate, KL weight, buffer size) and the number of gradient steps per iteration?
- What is the effect of the KL regularizer? Does it break the theoretical descent property?
- Can the authors provide training time and memory comparisons under the same hardware and batch size for all baselines?

### Limitations

- The method can only sample within the support of the pre-trained model; high-reward regions outside this support cannot be discovered, and no off-policy extension is demonstrated.
- Path-based importance weights may have high variance, and the approximation of the marginal ratio by the path RND is not quantified, potentially biasing the final distribution.
- The theoretical descent guarantee assumes exact optimization and continuous-time processes; the practical algorithm is discrete and uses stochastic updates, so convergence is not guaranteed.
- The acceptance threshold c is a heuristic hyperparameter, and the method may not converge to the tilted distribution if c is not sufficiently large.
- Experimental validation is limited: no quantitative super-resolution results, limited text-to-image prompts without statistical significance, and no iterative-retraining degradation analysis.
- The paper does not discuss societal impacts of reward fine-tuning generative models, such as enabling harmful content creation.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 246,163
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 242,067
- Completion tokens: 29,095
- Reasoning tokens reported: 22,306
- Total tokens: 275,258
- Estimated total: $0.04204745

Full individual reviews and raw JSON responses are in `review_bundle.json`.
