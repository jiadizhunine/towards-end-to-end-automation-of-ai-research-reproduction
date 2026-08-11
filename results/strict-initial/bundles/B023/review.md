# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B023.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **3/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.059551**

## Final Meta-review

The paper proposes a theoretical framework for analyzing convergence of adaptive optimizers (Adam and Muon) under floating-point quantization of weights, gradients, and optimizer states. It introduces a relative-error quantization model and derives convergence rates on smooth non-convex objectives, claiming O(T^{-1/4}) rates for both quantized Adam and Muon when mantissa lengths grow logarithmically with T. The paper also argues that Muon is more robust than Adam to low-precision training. Experiments on Rosenbrock and CIFAR-10 with a small MLP are provided to corroborate the theory.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 2.800 | 0.400 | 2-3 |
| Quality | 2 | 1.800 | 0.400 | 1-2 |
| Clarity | 1 | 1.600 | 0.490 | 1-2 |
| Significance | 2 | 2.400 | 0.490 | 2-3 |
| Soundness | 2 | 1.800 | 0.400 | 1-2 |
| Presentation | 1 | 1.600 | 0.490 | 1-2 |
| Contribution | 2 | 2.400 | 0.490 | 2-3 |
| Overall | 3 | 3.400 | 0.800 | 2-4 |
| Confidence | 4 | 3.600 | 0.490 | 3-4 |

### Strengths

- Addresses an important and timely gap: prior theoretical work on quantized adaptive optimizers largely ignores quantization of optimizer states, whereas this paper explicitly models weights, gradients, first moments, and second moments.
- Uses a relative-error quantization model that is well aligned with floating-point formats (e.g., BF16/FP8), avoiding unrealistic unbiased-quantization or error-feedback assumptions.
- Provides a component-wise characterization of quantization errors, yielding the qualitative insight that Adam requires stricter precision for second moments and weights, while Muon has a different error profile.
- Includes experiments demonstrating that higher mantissa precision improves convergence, consistent with the general direction of the theory.
- Provides a detailed proof structure with lemmas and a proof dependency graph, even though the presentation has issues.

### Weaknesses

- Theorem 4.6 for quantized Muon contains a serious asymptotic error: with q_M = O(T^{-1/2}) and 1 - beta = Theta(T^{-1/2}), the factor q_M beta / (1 - beta(1+q_M)) is Theta(1), not O(T^{-1/2}) as claimed; the final bound does not vanish and the claimed O(T^{-1/4}) rate is not established.
- The theorems require quantization errors to decay polynomially with T (e.g., q = O(T^{-1}) or O(T^{-2})). For fixed-precision hardware, q is constant; the conditions only hold if mantissa length grows with T, which is far beyond BF16/FP8 capacities and undermines practical applicability.
- Adam's analysis requires stochastic gradients to be uniformly bounded in l_infinity almost surely, which is unrealistic in deep learning; Muon only needs bounded variance, making the comparison unbalanced.
- The analyzed Adam algorithm differs from standard Adam (no first-moment bias correction, weighted-sum moments instead of weighted-average), so the theorems do not directly cover the practical algorithm.
- The main algorithms (1, 2, 3) are missing from the manuscript, leaving the exact quantized update rules and quantization points ambiguous.
- Muon's analysis assumes exact SVD and does not model quantization of auxiliary Adam states used in practical Muon implementations, while the experiments quantize these states, causing a theory-practice mismatch.
- The q_W = O(T^{-2}) requirement for Adam is admitted to be a possible proof artifact, weakening the claim that Adam is inherently sensitive to weight quantization.
- Experiments are limited to a synthetic function and a small MLP, do not directly compare Adam vs Muon under identical precision, lack error bars and test accuracy, and do not implement the precision schedules required by the theory.
- Presentation is poor with typos, undefined constants (e.g., \tilde Q, C), duplicated terms, and hand-wavy asymptotic analysis, making the proofs difficult to verify.
- The framework does not account for other low-precision training effects such as activation quantization, FP8 matmul errors, or communication compression.

### Questions

- In Theorem 4.6, how is q_M beta / (1 - beta(1+q_M)) = O(T^{-1/2}) when both q_M and 1 - beta are Theta(T^{-1/2})? Does the Muon bound actually vanish to achieve the claimed O(T^{-1/4}) rate?
- Can the theoretical results be extended to constant quantization errors (fixed mantissa length), or is a horizon-dependent precision schedule fundamental? How would this apply to fixed-precision hardware at LLM scale?
- Can Adam's convergence be analyzed under the relaxed bounded-variance assumption instead of l_infinity bounded gradients, and can the q_W = O(T^{-2}) condition be proven or relaxed under bounded weight norms?
- What are the exact quantization steps in Algorithms 1-3? In particular, are weights and optimizer states quantized before or after the optimizer update, and how does this affect the recurrence?
- How does the Muon analysis account for the auxiliary Adam states and the Newton-Schulz approximation used in practical implementations? Does the theorem cover the full practical algorithm?
- Do the experiments directly compare Adam and Muon under identical precision and stochastic noise, and do they use practical formats such as BF16/FP8 instead of synthetic mantissa truncation?

### Limitations

- The relative-error quantization model assumes no underflow/overflow and is inaccurate for values near zero or subnormals.
- The analysis relies on strong assumptions (L-smoothness, bounded initialization, l_infinity bounded gradients for Adam) that may not hold for practical LLM objectives.
- The theoretical precision requirements require quantization error to be annealed to zero with T, which is not how fixed-precision training is performed and may not be implementable without knowing T in advance.
- The framework does not model activation quantization, FP8 matrix multiplication errors, or communication compression, all critical in low-precision pipelines.
- Muon is analyzed with exact SVD, not the Newton-Schulz approximation used in practice; the approximation error is not modeled.
- Experiments are small-scale and do not validate the logarithmic mantissa scaling prediction or the claimed robustness differences on realistic large-scale tasks.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 331,993
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 327,897
- Completion tokens: 48,692
- Reasoning tokens reported: 41,913
- Total tokens: 380,685
- Estimated total: $0.05955081

Full individual reviews and raw JSON responses are in `review_bundle.json`.
