# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B029.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.029255**

## Final Meta-review

The paper proposes Astraea, a training-free acceleration framework for video diffusion transformers (vDiTs) that operates at the token level. It introduces a lightweight token selection metric combining LSE scores, token value changes, and a penalty for repeated non-selection, and a sparse attention method that computes selected queries while keeping full keys/values. An evolutionary search allocates per-timestep token budgets. Experiments on HunyuanVideo, Wan, and OpenSora report up to 2.4x single-GPU speedup and 13.2x on 8 GPUs, with VBench loss claimed under 0.5% and better PSNR/SSIM than baselines.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 2.800 | 0.400 | 2-3 |
| Quality | 2 | 1.800 | 0.400 | 1-2 |
| Clarity | 2 | 2.000 | 0.632 | 1-3 |
| Significance | 2 | 2.400 | 0.490 | 2-3 |
| Soundness | 2 | 1.800 | 0.400 | 1-2 |
| Presentation | 2 | 2.000 | 0.632 | 1-3 |
| Contribution | 2 | 2.000 | 0.000 | 2-2 |
| Overall | 4 | 4.000 | 0.000 | 4-4 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Addresses an important practical problem: reducing inference cost of video diffusion transformers.
- The token selection metric is lightweight and avoids storing full attention maps, unlike some prior methods.
- The sparse attention design that computes selected queries but full keys/values preserves softmax correctness and is GPU-friendly with FlashAttention.
- The evolutionary search for per-timestep token budgets automates compute allocation and is evaluated on multiple vDiT models.
- Comprehensive evaluation across three vDiT families, multiple resolutions/durations, and GPU platforms demonstrates meaningful speedups over baselines.

### Weaknesses

- Memory consumption under Astraea is consistently higher than the original model (e.g., HunyuanVideo 69.01 GB vs 45.81 GB, OpenSora 4s 27.98 GB vs 16.96 GB), contradicting the claim of negligible memory overhead.
- The offline evolutionary search is very expensive (82 GPU hours on 8 A100s per configuration) and must be rerun for different models/budgets, limiting practical deployment.
- The claimed '<0.5% VBench loss' is contradicted by the paper's own tables (e.g., OpenSora 4s Astraea 40% drops from 79.00 to 76.62, a 2.38% loss).
- PSNR/SSIM are computed against the original model's output, which favors methods that reuse previous timesteps; these metrics do not directly measure perceptual quality or fairness against baselines.
- Several technical details are missing or inconsistent: FLOPs tables show linear scaling with token budget despite full K/V computation, the treatment of MLP layers is unclear (Hunyuan MLP FLOPs unchanged), and the handling of cross-attention and cached key/values is not fully specified.
- The selection metric is heuristic, with no ablation or sensitivity analysis of its components (S_sig and S_penalty) or hyperparameters (w_alpha, w_beta).
- The writing and presentation contain typos, malformed tables, missing algorithm content, and misaligned numbers, making reproduction difficult.
- Baseline coverage is incomplete (e.g., ToCa omitted on HunyuanVideo due to OOM; some recent token-caching methods not compared).

### Questions

- How is the LSE score computed for unselected tokens at subsequent timesteps? Is it from the previous full attention or only from selected tokens?
- Why does Astraea increase peak memory on HunyuanVideo from 45.81 to 69.01 GB despite claiming cached tokens are negligible? What exactly is cached and for how long?
- How is the 0.5% VBench loss claim reconciled with OpenSora 4s Astraea 40% showing a 2.38% drop? Are the numbers correct?
- The FLOPs tables show self-attention FLOPs scaling linearly with token budget, but the method computes full K and V. Please provide a detailed FLOPs derivation for the actual implementation.
- How are cross-attention and MLP handled? Are selected tokens reused across all sub-layers, and are cached outputs for unselected tokens combined with computed ones?
- What is the end-to-end overhead of the token selection step itself (computing S_sig, S_penalty, top-k)? Is it included in reported latencies?
- How sensitive is the EA-searched token schedule to the 4 prompts used? Could it transfer across resolutions, durations, or prompt distributions without rerunning?
- What is the total computational cost of the search relative to the inference savings? Could the search be reused across models or batch sizes?
- In Table 1, why do original Wan (4s) and HunyuanVideo both have VBench 80.28? Are there other duplicated or misreported numbers?

### Limitations

- The expensive offline evolutionary search (82 GPU hours per configuration on 8 A100s) is not amortized and may make the method impractical for quick deployment on new models.
- Memory usage is higher than the original model, which can be prohibitive on memory-constrained GPUs and contradicts the paper's claims.
- The method is only evaluated on short videos (2-5 seconds) at 480p; scalability to longer or higher-resolution videos is untested.
- The search uses only 4 prompts, and the paper provides limited evidence that the selected token schedules generalize across diverse content.
- The sparse attention performs full K/V projections and attention score computations for all keys/values, bounding the achievable speedup below linear scaling with token count.
- The method has not been combined with step-reduction or distillation techniques, so its benefits in a multi-technique acceleration pipeline remain unclear.
- The paper does not discuss potential negative societal impacts, such as misuse of faster video generation for misinformation.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 153,818
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 149,722
- Completion tokens: 29,581
- Reasoning tokens reported: 22,713
- Total tokens: 183,399
- Estimated total: $0.02925523

Full individual reviews and raw JSON responses are in `review_bundle.json`.
