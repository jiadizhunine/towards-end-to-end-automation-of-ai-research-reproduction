# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B003.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.017939**

## Final Meta-review

The paper proposes STaMP (Sequence Transformation and Mixed Precision), a novel post-training quantization method that applies invertible linear transformations (e.g., DCT, DWT, WHT) along the sequence dimension of activations to exploit local correlations between tokens in language and visual models. By concentrating activation energy into a small number of tokens, STaMP allocates higher bit-widths (8-bit) to these energy-dense tokens and lower precision (4-bit) to the rest, achieving improved quantization accuracy under a fixed average bit-width budget. The method is designed to complement existing feature-dimension transforms (e.g., QuaRot, SmoothQuant) and weight quantization techniques. The paper provides theoretical analysis (an upper bound on quantization error and optimal bit allocation), demonstrates that autocorrelation matrices of intermediate activations exhibit Toeplitz-like structure (justifying DCT/DWT as approximations to the optimal KLT), and validates the method through extensive experiments on LLMs (Llama 3, Llama 3.2, Qwen 2.5) and LVMs (PixArt-Σ, SANA) across multiple baselines and metrics. The method adds minimal computational overhead and is training-free, with code released.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 4.000 | 0.000 | 4-4 |
| Quality | 3 | 3.200 | 0.400 | 3-4 |
| Clarity | 3 | 3.400 | 0.490 | 3-4 |
| Significance | 4 | 3.600 | 0.490 | 3-4 |
| Soundness | 4 | 3.600 | 0.490 | 3-4 |
| Presentation | 3 | 3.400 | 0.490 | 3-4 |
| Contribution | 4 | 3.600 | 0.490 | 3-4 |
| Overall | 7 | 7.200 | 0.748 | 6-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel and well-motivated approach: applying sequence-dimension transforms for activation quantization is a fresh perspective that complements existing feature-transform methods.
- Solid theoretical foundation: provides an upper bound on quantization error and derives optimal bit allocation strategies, with a reasoned connection between autocorrelation structure and DCT/DWT.
- Comprehensive experimental evaluation: consistent improvements across multiple LLM and LVM architectures and several strong baselines (RTN, SmoothQuant, QuaRot, FlatQuant, ViDiT-Q, SVDQuant), demonstrating orthogonality with existing methods.
- Practical considerations addressed: overhead estimates, mixed-precision kernel implementation, and honest discussion of limitations such as applicability to prompt processing only.
- Clear writing and helpful visualizations: autocorrelation matrices and energy distribution plots effectively illustrate the key insights.
- Code availability for reproducibility.

### Weaknesses

- Limited applicability to LLM generation: STaMP is only applicable during prompt processing, not token-by-token generation, which limits its impact for decode-heavy workloads.
- The choice of 64 high-precision tokens appears heuristic and not rigorously justified across different models or sequence lengths; sensitivity analysis is limited.
- The practical bit allocation (64 tokens at 8-bit, rest at 4-bit) is a simplification of the theoretical optimal allocation, and the connection between theory and practice is not fully explored.
- Improvements on some strong baselines (e.g., FlatQuant) are modest, though more significant for harder cases.
- No empirical comparison with the theoretically optimal KLT transform or learned sequence transforms is provided, making it difficult to assess how much performance is lost by using fixed transforms.
- The overhead analysis is limited to a single GPU (A100) and may not generalize to edge devices where quantization benefits are most critical.

### Questions

- How sensitive is the performance of STaMP to the number of high-precision tokens (currently fixed at 64)? Is there a principled way to determine this hyperparameter based on energy distribution or sequence length?
- For LLMs, since STaMP only applies to prompt processing, what fraction of real-world inference workloads benefit? Could the method be extended to generation via a sliding window or chunked approach?
- How does the performance of DWT compare to DCT/WHT specifically in the LLM setting? Are there scenarios where DCT would be preferable despite higher computational cost?
- Could STaMP be extended to the KV cache as well as activations, and if so, what results would be expected?
- How does the method perform on longer sequences (e.g., 8192 or 16384 tokens) where local correlation patterns might differ?
- Could the sequence transformation be learned (rather than fixed) to better adapt to specific model activations, and what would be the computational cost?
- How does STaMP interact with attention sinks (e.g., the first token often containing outliers)? Is it necessary to exclude such tokens from the transform?
- What is the end-to-end speedup on real hardware when accounting for mixed-precision matrix multiplication overhead, especially on edge devices?

### Limitations

- The method is only applicable to prompt processing in LLMs, not autoregressive token generation, limiting its utility for decode-phase optimization.
- The mixed-precision scheme (4-bit and 8-bit) requires hardware support for multiple bit-widths, which may not be available on all deployment platforms.
- The bit allocation and number of high-precision tokens are chosen heuristically; a more principled selection criterion would strengthen the work.
- The theoretical analysis provides an upper bound but does not fully characterize how tight it is for practical activation distributions.
- The paper does not explore interaction with other quantization granularities (e.g., per-block, per-group) or more advanced weight-quantization methods.
- The approach relies on the assumption of local correlation in the sequence dimension, which may not hold for all data types or architectures (e.g., pooled embeddings).
- Potential negative societal impact: more efficient quantization could enable deployment of powerful generative models on resource-constrained devices, potentially increasing misuse; however, this is not specific to this work and applies to quantization in general.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 106,810
- Cache-hit prompt tokens: 0
- Cache-miss prompt tokens: 106,810
- Completion tokens: 10,664
- Reasoning tokens reported: 0
- Total tokens: 117,474
- Estimated total: $0.01793932

Full individual reviews and raw JSON responses are in `review_bundle.json`.
