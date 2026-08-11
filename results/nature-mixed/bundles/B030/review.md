# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B030.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.029189**

## Final Meta-review

This paper proposes a framework for recycling fully converged Mixture-of-Experts (MoE) checkpoints by growing them into larger models, thereby leveraging 'sunk' computational costs. Two orthogonal growth strategies are introduced: (1) depth growth via interpositional layer copying (duplicating each layer in place) rather than the traditional stacking approach, which the authors argue better preserves learned layer-wise weight norm trends, and (2) width growth via expert duplication with small Gaussian noise injection to promote expert specialization. The paper demonstrates that growing from checkpoints with higher sunk cost leads to better final performance, that model growth is comparable or superior to training from scratch under fixed total FLOPs, and that the method scales to 70B parameters with a 10.66% accuracy improvement over a scratch-trained baseline under the same additional compute budget. Experiments span 3B to 70B parameters and include extensive ablations on growth timing, noise injection scale, and interposition vs. stacking.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 4 | 3.600 | 0.490 | 3-4 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 4 | 3.600 | 0.490 | 3-4 |
| Contribution | 3 | 3.200 | 0.400 | 3-4 |
| Overall | 7 | 6.800 | 0.400 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses a timely and practically important problem: efficient LLM pretraining through checkpoint recycling, which is highly relevant given the computational costs of training large models.
- The interposition vs. stacking comparison for converged models is a novel and well-motivated contribution, supported by analysis of layer-wise weight norm distributions across multiple open-source models.
- The noise injection strategy for expert duplication during width growth is a simple but effective technique, backed by ablation studies showing its benefit over direct copying.
- The growth timing analysis with sunk cost correlation is a valuable practical contribution, providing heuristics for when to apply growth.
- Large-scale validation (17B→70B, 1T tokens) demonstrates real-world applicability and robustness of the proposed methods.
- The paper is well-written and organized, with extensive experimental details in the appendix, supporting reproducibility.

### Weaknesses

- The theoretical justification for interposition over stacking is heuristic, relying primarily on empirical weight norm observations rather than a formal analysis or mechanistic explanation.
- The comparison to scratch training may be potentially unfair due to FLOPs accounting; the 'same extra FLOPs' budget includes sunk cost in the growth trajectory but not in the scratch baseline, which could inflate the apparent benefit of growth.
- Limited evaluation benchmarks (MMLU + 6 QA tasks); no code, math, multilingual, or long-context evaluations, limiting the generalizability of the claims.
- No head-to-head comparison with other model growth methods (e.g., LiGO, LEMON, MSG, or MoE-specific approaches like GroveMoE), making it difficult to position the contribution relative to the state of the art.
- The growth factor k is fixed at 2; no exploration of other growth ratios or their interaction with the proposed methods.
- The width growth timing and noise injection effectiveness are not systematically studied at larger scales or with different MoE configurations.
- The 70B experiment uses a different training procedure (no annealing) compared to the 3B experiments, limiting direct comparability across scales.

### Questions

- Could you clarify the exact FLOPs accounting in Fig. 1? Does the 'same extra FLOPs' comparison include the sunk FLOPs of the base model in the growth trajectory? If not, how does this affect the claimed 10.66% advantage?
- Have you considered applying the timing analysis to width growth as well? Would the positive correlation with sunk cost also hold, or does width growth have different optimal timing characteristics?
- How sensitive are the results to the choice of growth factor k beyond k=2? Does the benefit of interposition over stacking change with larger growth factors?
- Did you evaluate the grown models on benchmarks beyond MMLU and the six QA tasks (e.g., code, math, or multilingual)? If not, how might the conclusions change?
- Can you provide a more mechanistic explanation for why interposition preserves learned structure better than stacking, beyond the weight norm visualization?
- How does the choice of checkpoint from the annealing phase interact with the learning rate schedule for continued training? Would a different LR schedule mitigate the diminishing returns observed in Section 4.1?
- For the width growth, did you explore different noise distributions (e.g., uniform) or noise applied only to certain weight matrices? What is the sensitivity of the results to the noise injection scheme?
- Have you considered comparing your interposition method with other growth techniques beyond stacking, such as LEMON or LiGO, to strengthen the claim that interposition is the best approach for converged models?
- What is the computational and memory overhead of the growth process itself (excluding continued training)? This is important for practical adoption.

### Limitations

- The experiments are limited to MoE architectures; applicability to dense models is not demonstrated.
- The evaluation is limited to a small set of English-language benchmarks; generalizability to code, math, multilingual, and long-context domains is not shown.
- The paper does not provide a detailed analysis of why interposition works better than stacking beyond the weight norm observation; a more mechanistic understanding is needed.
- The comparison to scratch training may be confounded by different training schedules and data ordering.
- The paper does not discuss the computational overhead of the growth process itself (e.g., memory overhead during expansion), which could be a practical limitation.
- The paper does not release the actual pretrained checkpoints, only code fragments, which may limit reproducibility for the broader community.
- The broader societal impact of more efficient LLM training (e.g., lowering barriers to developing powerful models) is mentioned but not deeply analyzed.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 198,042
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 189,082
- Completion tokens: 9,616
- Reasoning tokens reported: 0
- Total tokens: 207,658
- Estimated total: $0.02918905

Full individual reviews and raw JSON responses are in `review_bundle.json`.
