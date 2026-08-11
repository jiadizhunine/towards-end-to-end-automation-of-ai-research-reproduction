# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B113.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.017787**

## Final Meta-review

The paper proposes ANSE (Active Noise Selection for Generation), a model-aware framework for selecting high-quality initial noise seeds in text-to-video diffusion models. The core contribution is BANSA (Bayesian Active Noise Selection via Attention), an acquisition function that adapts the BALD uncertainty criterion from active learning to measure entropy disagreement across stochastic attention samples. Lower BANSA scores indicate more confident and consistent attention, which empirically correlates with higher-quality video generation. To make the approach efficient, the authors introduce a Bernoulli-masked approximation that estimates BANSA from a single forward pass and a correlation-based layer selection method to use only a subset of informative attention layers. Experiments across multiple backbones (AnimateDiff, CogVideoX-2B/5B, Wan2.1, HunyuanVideo) show consistent improvements in VBench metrics, FVMD motion quality, and human preference, with only ~10-15% inference overhead. The paper also provides analyses of cross-prompt behavior, attention consistency, and latent trajectory properties, along with comprehensive ablations.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.200 | 0.400 | 3-4 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.200 | 0.400 | 3-4 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.200 | 0.400 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel and well-motivated idea: applying BALD-style uncertainty to attention maps for noise seed selection in video diffusion, addressing a practically relevant problem.
- Model-agnostic approach tested on diverse backbones (U-Net and MMDiT architectures, various scales), demonstrating generalizability.
- Efficient inference via Bernoulli-masked attention and layer truncation, with thorough analysis of the trade-offs.
- Comprehensive ablation studies covering acquisition functions, ensemble size, pool size, masking probability, reversed scoring, temporal scope, attention type, CFG interaction, and equivalent compute budget.
- Statistical validation with confidence intervals on VBench scores strengthens the reliability of reported improvements.
- Honest discussion of limitations (failure cases, attention-level uncertainty not capturing semantics) and clear future directions.
- Qualitative results and user study provide complementary evidence of practical benefits.
- Method is orthogonal to existing noise-prior approaches and can be combined with them (demonstrated with FreqPrior).

### Weaknesses

- The theoretical contribution is limited: Proposition 1 (BANSA = 0 iff all attention maps identical) follows directly from Jensen's inequality and entropy concavity, providing no deep insight into why lower BANSA correlates with quality.
- The 'Bayesian' interpretation is loose; Bernoulli-masked attention is a heuristic for generating stochastic samples rather than a principled Bayesian posterior approximation.
- Quantitative gains are modest in several cases (e.g., VBench total score improvements of ~0.5-1.5 points), and some improvements fall within confidence intervals (e.g., Aesthetic Quality on HunyuanVideo).
- The layer selection procedure uses an arbitrary correlation threshold (0.7) without clear justification or sensitivity analysis.
- Comparison with prior noise-based methods is limited: FreqPrior is only evaluated on AnimateDiff, and FreeInit, InitNO, or other seed selection approaches are not directly compared.
- For HunyuanVideo and Wan2.1, only quality metrics are reported (not semantic), limiting comparability with other backbones.
- The user study is relatively small (12 evaluators, 30 prompts) and lacks statistical significance testing or inter-rater agreement measures.
- The claim of being the 'first active noise selection framework' may be slightly overstated given related work on noise optimization.

### Questions

- How is the noise pool Z constructed? Are the M seeds sampled randomly for each prompt, or is there a fixed pool? Does the optimal seed vary significantly across prompts, and how does this affect practical utility?
- What is the theoretical justification for Bernoulli masking with p=0.2? How does the choice of p relate to the model's architecture or the noise level at the first denoising step?
- How sensitive is the layer selection procedure to the correlation threshold τ=0.7? Would different thresholds (e.g., 0.5, 0.9) significantly change the selected layers and final performance?
- In Table 5, the vanilla baseline values for HunyuanVideo and Wan2.1 appear identical for several metrics. Is this a typo or are these values genuinely the same?
- What is the total compute overhead when accounting for the fact that you need to run partial denoising for all M=10 candidates before selecting one? How does this compare to simply generating more samples from the same budget?
- Does the method extend to image diffusion models? If so, what would be the expected gains compared to video models?
- How does BANSA compare against simpler model-agnostic selection criteria, such as CLIP score or LPIPS-based metrics?
- Could you provide a more rigorous theoretical analysis of why lower BANSA scores should correlate with better generation quality? The current justification is primarily empirical.
- What happens when the noise pool size M is increased beyond 10 (e.g., M=50)? Does performance continue to improve, and at what computational cost?
- In the user study, what was the inter-rater agreement (e.g., Fleiss' kappa)? Were the preferences statistically significant across the 12 evaluators?

### Limitations

- The method selects seeds but does not modify the generation process, so even low-BANSA seeds can produce unnatural results in some cases (acknowledged by the authors).
- BANSA captures attention-level uncertainty, which may not fully account for semantic or aesthetic quality dimensions.
- The method requires evaluating multiple candidate seeds (M=10) with multiple stochastic passes (K=10), adding computational overhead that may be prohibitive for real-time or resource-constrained applications.
- The evaluation on HunyuanVideo and Wan2.1 is restricted to quality dimensions only (not semantic), limiting the assessment of prompt alignment for these larger models.
- The correlation analysis for layer selection is based on a specific set of 100 prompts from VBench categories; generalization to other prompt distributions is not verified.
- The paper does not discuss potential negative societal impacts of improved video generation, such as increased potential for deepfakes or misinformation.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 110,900
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 101,940
- Completion tokens: 12,465
- Reasoning tokens reported: 0
- Total tokens: 123,365
- Estimated total: $0.01778689

Full individual reviews and raw JSON responses are in `review_bundle.json`.
