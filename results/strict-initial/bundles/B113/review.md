# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B113.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **3/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.015705**

## Final Meta-review

The paper proposes ANSE (Active Noise Selection for Generation), an inference-time framework for selecting initial noise seeds in text-to-video diffusion models. The central component is BANSA, an acquisition function inspired by Bayesian active learning that measures disagreement across stochastic attention maps (generated via Bernoulli-masked attention) to estimate model confidence. To reduce overhead, BANSA is computed on a single early denoising step and on a subset of attention layers selected by correlation analysis. Experiments on CogVideoX-2B and CogVideoX-5B report small VBench quality/semantic improvements with an 8-13% inference-time overhead. All five reviewers recommend rejection due to fundamental theoretical inconsistency, questionable empirical significance, and incomplete comparisons and presentation.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 2.800 | 0.400 | 2-3 |
| Quality | 2 | 1.800 | 0.400 | 1-2 |
| Clarity | 2 | 1.800 | 0.400 | 1-2 |
| Significance | 2 | 2.000 | 0.000 | 2-2 |
| Soundness | 2 | 1.800 | 0.400 | 1-2 |
| Presentation | 2 | 1.800 | 0.400 | 1-2 |
| Contribution | 2 | 2.000 | 0.000 | 2-2 |
| Overall | 3 | 3.400 | 0.490 | 3-4 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- The idea of leveraging internal attention uncertainty for noise seed selection is novel and interesting, extending active learning principles to inference-time generation.
- The method is training-free and can be integrated into existing text-to-video diffusion pipelines without modifying the generation model.
- The Bernoulli-masked approximation and layer/timestep truncation are practical approaches that keep the computational overhead relatively low (8-13%).
- The paper includes multiple ablations (acquisition functions, ensemble size, pool size, reversed criterion, full vs. truncated layers) that provide useful insights.
- The approach is orthogonal to prior noise-prior methods and could potentially be combined with them.

### Weaknesses

- There is a serious sign inconsistency in the definition of BANSA: Eq. (4) defines it as (1/K)Σ H(A_k) − H(mean A), which is non-positive by Jensen's inequality, contradicting the stated goal of minimizing BANSA to prefer confident, consistent attention. The appendix uses the opposite sign but claims the relative ordering is unchanged, which is mathematically incorrect since the two are negatives.
- The theoretical justification is weak: Proposition 1 only shows that identical attention maps give zero score, but does not establish that lower BANSA correlates with better generation quality; the connection is purely empirical.
- The reported improvements on VBench are very small (e.g., total score +0.63 on 2B and +0.25 on 5B) and no error bars, confidence intervals, or significance tests are provided, despite generating 4,730 videos per configuration; the gains may be within run-to-run variability.
- No direct comparison is made with prior noise-prior methods such as FreeInit or FreqPrior, despite claims of comparable or superior quality and lower inference cost; the relative effectiveness is unsubstantiated.
- The evaluation is limited to CogVideoX-2B and CogVideoX-5B; the claimed generalizability to 'various text-to-video architectures' is not supported.
- The use of the term 'Bayesian' is misleading: Bernoulli-masked attention is a heuristic perturbation, not a posterior over model parameters, and the paper acknowledges this but still uses the terminology.
- Several technical details are inconsistent or unclear: the layer-selection procedure in Section 3.3 correlates with the full-layer average BANSA while Appendix E says 'official quality scores'; the Bernoulli masking in Eq. (7) sets masked logits to 0 instead of −∞ before softmax, which is not a proper masked-dropout operation and lacks justification.
- Presentation is poor: duplicated Definition 1 and Proposition 1, references to a missing Table 3 in the ablation section, inconsistent notation, and incomplete method details that hinder reproducibility.

### Questions

- What is the exact objective minimized in the experiments? The main text and appendix give opposite signs for BANSA; which one was used, and why is the relative ordering claimed to be unchanged when the two definitions are negatives?
- Are the VBench score differences statistically significant across multiple runs or seeds? Can the authors report standard deviations, confidence intervals, or paired significance tests?
- Why were no comparisons with FreeInit or FreqPrior performed on CogVideoX even on a subset? What evidence supports the claim of 'comparable or superior generation quality' and 'reduces inference cost by approximately 64%' relative to those methods?
- How exactly are the Bernoulli masks applied to attention logits in Eq. (7)? Does setting masked entries to 0 rather than −∞ produce valid stochastic perturbations, and how does this differ from standard dropout on attention scores?
- What is the exact set of attention layers and heads used to compute BANSA? How are cross-attention, self-attention, and temporal attention aggregated?
- How sensitive are the results to the masking probability p, the correlation threshold τ=0.7, and the choice of the early denoising step?
- Could a simple best-of-M baseline (e.g., generating M videos and selecting by CLIP or VBench on a small subset) outperform ANSE?
- How does attention consistency at the first denoising step correlate with final video quality? Is there a theoretical or empirical justification for using t=1 only?

### Limitations

- The sign inconsistency in the BANSA definition undermines the theoretical correctness and reproducibility of the core acquisition function.
- The method only selects seeds; it cannot correct failures in the generation process, and low-BANSA seeds can still produce unnatural videos (as acknowledged).
- The improvements are small and may not be perceptible in practice; no statistical significance is established.
- The evaluation is restricted to a single model family (CogVideoX), limiting claims of generalizability.
- The 'Bayesian' framing is heuristic and not based on a rigorous posterior distribution, limiting the theoretical contribution.
- The Bernoulli-masked approximation and layer-truncation heuristic lack bias/variance analysis and could affect selection quality in unknown ways.
- The layer selection was tuned on a limited set of 100 prompts and may require re-calibration for other models or domains.
- No discussion of potential negative societal impacts of improved video generation (e.g., deepfakes) is provided.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 76,064
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 71,968
- Completion tokens: 20,066
- Reasoning tokens reported: 13,616
- Total tokens: 96,130
- Estimated total: $0.01570547

Full individual reviews and raw JSON responses are in `review_bundle.json`.
