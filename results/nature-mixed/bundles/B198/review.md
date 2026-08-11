# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B198.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.017742**

## Final Meta-review

This paper investigates the role of the L0 hyperparameter (average number of active features per token) in Sparse Autoencoders (SAEs) for LLM interpretability. Using toy models with known ground-truth features, the authors demonstrate that both too-low and too-high L0 values cause SAEs to mix correlated features, producing polysemantic latents. They show that MSE loss actively incentivizes this incorrect behavior at low L0, and that sparsity-reconstruction tradeoff plots are misleading because a ground-truth SAE can score worse on reconstruction than an incorrect SAE that mixes features. The paper proposes a proxy metric, the nth decoder projection score (s_n^dec), which is minimized at the correct L0 in toy models and correlates with peak sparse probing performance in LLM SAEs (Gemma-2-2b, Llama-3.2-1b) for both BatchTopK and JumpReLU architectures. The authors conclude that most commonly used SAEs have L0 set too low and that L0 must be carefully tuned for SAEs to learn correct features.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.600 | 0.490 | 3-4 |
| Quality | 3 | 3.200 | 0.400 | 3-4 |
| Clarity | 3 | 3.200 | 0.400 | 3-4 |
| Significance | 4 | 3.600 | 0.490 | 3-4 |
| Soundness | 3 | 3.200 | 0.400 | 3-4 |
| Presentation | 3 | 3.200 | 0.400 | 3-4 |
| Contribution | 3 | 3.400 | 0.490 | 3-4 |
| Overall | 7 | 6.800 | 0.748 | 6-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important and under-explored question: the correct setting of L0 in SAEs, challenging the common assumption that L0 is a free parameter tuned via sparsity-reconstruction tradeoff plots.
- Clear and compelling toy model experiments with ground-truth features provide strong causal evidence for the feature-mixing phenomenon at incorrect L0 values.
- The demonstration that sparsity-reconstruction tradeoff plots can actively mislead SAE evaluation is a significant methodological insight.
- The proposed s_n^dec metric is simple, intuitive, and validated across toy models, multiple LLMs (Gemma-2-2b, Llama-3.2-1b), and two SAE architectures (BatchTopK, JumpReLU), showing correlation with sparse probing performance.
- Honest and thorough discussion of limitations, including the metric's behavior at high L0, the computational cost of L0 sweeps, and the difficulty of automating L0 selection.
- The finding that most open-source SAEs have L0 too low has direct practical implications for the interpretability community.
- Code is provided for reproducibility, and the paper includes useful appendices with extended analyses.

### Weaknesses

- The claim that 'most commonly used SAEs have an L0 that is too low' is based on a limited survey (primarily one layer of Gemma-2-2b on Neuronpedia) and may not generalize broadly.
- The proposed metric requires training a full sweep of SAEs at different L0 values, which is computationally expensive and limits its practical utility; the automated optimization approach in the appendix is noted as needing heavy tuning and being impractical for LLMs.
- LLM experiments are limited to two models (Gemma-2-2b, Llama-3.2-1b) and a few layers, raising questions about generalizability across architectures, layers, and model sizes.
- The interpretation of the s_n^dec curve in LLM settings is somewhat subjective: sometimes the global minimum is at high L0, and the paper advises using an 'elbow' instead, without providing a rigorous algorithm for automatic identification.
- The paper lacks a theoretical justification for why s_n^dec should be minimized at the true L0; the connection is purely empirical.
- The toy model assumes linear, orthogonal features, and the paper does not explore how non-orthogonal or non-linear feature structures (e.g., as in Engels et al. 2025) would affect the conclusions.
- The validation of 'correct' L0 in LLMs relies on sparse probing performance, which is itself a proxy and may be subject to the same feature-mixing issues; potential circularity is not fully discussed.
- The paper does not explore downstream interpretability tasks beyond sparse probing (e.g., causal interventions, feature visualization).

### Questions

- How sensitive is the s_n^dec metric to the choice of n? The paper recommends n near h/2, but the optimal n seems to vary; is there a principled way to choose n, and how robust is the 'elbow' detection across different n values in LLM settings?
- The paper notes the metric sometimes has a shallow region or global minimum at high L0. How should practitioners decide between using the global minimum versus the 'elbow'? Is there a principled, automated way to identify the elbow?
- Have you tested the metric on SAEs trained on other layers (e.g., early or late layers) or other models? Do you expect the same patterns to hold?
- Could you provide a more systematic analysis of open-source SAEs (e.g., across model sizes, layers, and training details) to support the claim that most SAEs have too-low L0?
- How does the feature-mixing phenomenon interact with SAE width (number of latents h)? Would a wider SAE be more or less prone to this issue at fixed L0?
- Does the proposed metric work for SAEs with different architectures (e.g., Gated SAEs, Matryoshka SAEs, TopK, L1) beyond BatchTopK and JumpReLU?
- Can you provide a more formal theoretical argument for why s_n^dec should be minimized at the true L0, rather than just empirical observations?
- How was the 'true' optimal L0 determined in LLM experiments beyond sparse probing? Is there additional validation (e.g., human interpretability studies or downstream task performance) that supports the chosen optimal L0?
- What is the variance in sparse probing performance across seeds at the optimal L0? Are the differences between L0 values statistically significant?
- Could the s_n^dec metric be adapted to work during training without full sweeps, perhaps by monitoring it dynamically and adjusting L0 on the fly? The appendix discusses this but notes significant challenges.

### Limitations

- The paper focuses on linear features satisfying the Linear Representation Hypothesis and does not investigate non-linear feature structures, which may be present in real LLMs.
- LLM validation is limited to two models (Gemma-2-2b, Llama-3.2-1b) and a few layers, which may not capture the full diversity of SAE behavior across architectures.
- The proposed metric requires training sweeps over L0, which is computationally expensive and may be prohibitive for many practitioners.
- The paper does not provide a fully automated method for L0 selection, only a diagnostic tool that requires manual interpretation of plots.
- The analysis of open-source SAEs is based on a brief scan of Neuronpedia and may not be representative of all SAEs in the field.
- Potential negative societal impact is minimal, but the paper could briefly discuss how improved SAE interpretability might be misused (e.g., for surveillance or manipulation), and also caution against misinterpretation of findings as a reason to distrust all SAE-based interpretability results.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 111,045
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 102,085
- Completion tokens: 12,232
- Reasoning tokens reported: 0
- Total tokens: 123,277
- Estimated total: $0.01774195

Full individual reviews and raw JSON responses are in `review_bundle.json`.
