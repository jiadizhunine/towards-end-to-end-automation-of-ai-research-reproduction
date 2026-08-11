# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B157.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.018586**

## Final Meta-review

The paper proposes Sparsity Evolution Fine-Tuning (SEFT), a method for fine-tuning already-pruned sparse LLMs while dynamically evolving the sparse topology. SEFT builds on Dynamic Sparse Training (DST) principles and sparse fine-tuning, introducing a drop-and-grow mechanism to update the sparse connectivity pattern during fine-tuning, followed by a sensitivity-based sparsity adaptation step to restore the target sparsity level. This allows previously pruned weights to be reactivated, enabling task-specific adaptation. Experiments on LLaMA, DeepSeek, and Mistral models pruned with SparseGPT and Wanda at various sparsity levels show consistent improvements over sparsity-preserving baselines (LoRA*, SPP, SQFT) on commonsense reasoning, MMLU, and GSM8K benchmarks, with lower memory and time costs.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.400 | 0.490 | 3-4 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.400 | 0.490 | 3-4 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.000 | 0.000 | 6-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important and practical problem: fine-tuning sparse LLMs while maintaining sparsity for deployment efficiency
- Technically sound method combining DST principles with sparse fine-tuning, with clear algorithmic details and a well-motivated approach
- Comprehensive experimental evaluation across multiple model families (LLaMA, DeepSeek, Mistral), pruning methods (SparseGPT, Wanda), and benchmarks (commonsense reasoning, MMLU, GSM8K)
- Clear efficiency gains in memory usage and training time compared to baselines
- Thorough ablation studies and sensitivity analyses covering mask constraints, sparsity adaptation, drop rates, update frequency, and learning rate
- Public code is provided for reproducibility

### Weaknesses

- Novelty is limited; the method is essentially a combination of existing DST and sparse fine-tuning techniques applied to sparse LLMs, with modest new adaptations
- Performance improvements over baselines are modest (typically 1-2% absolute accuracy gains), and no statistical significance testing or error bars are reported
- The method requires computing full dense gradients during the topology evolution phase, which limits the practical efficiency gains on GPUs; the paper acknowledges this but does not propose a solution
- The LoRA* baseline (with post-hoc pruning) may be somewhat unfair, as post-hoc pruning naturally degrades performance; a more careful baseline analysis is needed
- Limited analysis of when and why topology evolution helps; the paper could provide deeper insights into the conditions under which dynamic topology adaptation is most beneficial
- Evaluation on MMLU and GSM8K is limited (only 2 models, only Wanda pruning), weakening the claim of generality
- N:M sparsity experiments are limited and restrict topology evolution to active weights, which somewhat undermines the core contribution of reactivating pruned weights

### Questions

- How does SEFT compare to simply fine-tuning the sparse model with a larger number of trainable parameters (e.g., using a higher-rank LoRA) without topology evolution? The current comparison with LoRA* may not isolate the benefit of topology evolution.
- Could the authors clarify how the 'matched parameter count' is exactly configured for the baselines? Is it matched to the number of non-zero deltas in SEFT or to the LoRA rank?
- The method computes full dense gradients during topology evolution. Could the authors quantify the actual wall-clock time overhead of this gradient computation versus the overall training time, and how does this compare to the efficiency gains shown in Figure 3?
- How does SEFT compare to simply fine-tuning with a randomly re-sampled sparse mask (without gradient-based growth)? This would isolate the benefit of the dynamic topology evolution.
- For the N:M sparsity experiments, why is the topology evolution restricted to only active weights? Would it be possible to evolve the N:M pattern itself to better adapt to tasks?
- How sensitive is SEFT to the choice of the initial sparse topology (e.g., from Wanda vs SparseGPT)? Are there systematic differences in which starting points benefit most from dynamic evolution?
- In Appendix D, SEFT underperforms original LoRA on some benchmarks. How should practitioners weigh this performance gap against the sparsity preservation benefit?
- Could the authors provide error bars or statistical significance tests for the reported results, especially where the gains over baselines are small (1-2%)?
- Have the authors experimented with using the sensitivity metric (rather than gradient magnitude) for the grow step in the drop-and-grow mechanism?
- What is the practical overhead of storing the indices and deltas compared to LoRA's low-rank matrices, especially for very high sparsity levels?

### Limitations

- The method requires computing full dense gradients during the topology evolution phase, which limits the computational efficiency gains on GPUs; the paper acknowledges this but does not provide a solution
- The performance improvements over baselines are modest, suggesting the practical impact may be limited
- The paper focuses on unstructured sparsity, which has limited hardware support on GPUs; the N:M sparsity experiments are limited to a few configurations and restrict topology evolution to active weights
- The paper does not explore the interaction between SEFT and other compression techniques (e.g., quantization)
- The method requires careful hyperparameter tuning (drop rate, update frequency) which varies by task, potentially limiting ease of use
- The evaluation is primarily on English-language benchmarks; the method's effectiveness on multilingual or domain-specific tasks is not explored
- The paper does not discuss potential negative societal impacts in detail, though it includes a brief impact statement

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 122,193
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 113,233
- Completion tokens: 9,672
- Reasoning tokens reported: 0
- Total tokens: 131,865
- Estimated total: $0.01858587

Full individual reviews and raw JSON responses are in `review_bundle.json`.
