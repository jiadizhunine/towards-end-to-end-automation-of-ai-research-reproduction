# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B031.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 3, 'Reject': 2}
- Estimated API cost: **$0.060578**

## Final Meta-review

The paper presents a unified robustness evaluation framework for text-attributed graph (TAG) learning, benchmarking classical GNNs, robust GNNs, and GraphLLMs across 10 datasets from 4 domains under text-based, structure-based, and hybrid perturbations in both poisoning and evasion settings. It reports several empirical findings, including a text-structure robustness trade-off, the importance of advanced text encoders for simple RGNNs, and GraphLLM vulnerability to text poisoning. To address the trade-off, it proposes SFT-auto, an LLM-based detection-and-recovery framework that aims for balanced robustness, and provides extensive appendix results including adaptive attacks, ablations, and WTGIA analysis.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.600 | 0.490 | 2-3 |
| Clarity | 3 | 2.800 | 0.400 | 2-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 2 | 2.600 | 0.490 | 2-3 |
| Presentation | 3 | 2.800 | 0.400 | 2-3 |
| Contribution | 2 | 2.800 | 0.400 | 2-3 |
| Overall | 4 | 5.200 | 0.980 | 4-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Comprehensive and unified benchmark spanning 10 datasets, 4 domains, GNNs/RGNNs/GraphLLMs, multiple attack types, and both poisoning/evasion settings, filling a gap left by fragmented prior evaluations.
- Non-obvious empirical insights: the text-structure robustness trade-off, the strong performance of GNNGuard with advanced text encoders, and GraphLLM vulnerability to training-data corruption are clearly demonstrated with extensive tables.
- Sound evaluation protocol choices, including aligning poisoning with transductive and evasion with inductive settings, using transfer attacks, and filtering baselines with non-comparable clean accuracy.
- SFT-auto is a novel approach that combines attack detection and recovery inside an LLM, showing substantial gains in textual robustness (e.g., WikiCS) while preserving structural robustness in some settings.
- Extensive appendices with full numerical results, ablations, hyperparameters, and some adaptive attack analysis support reproducibility.

### Weaknesses

- SFT-auto is not evaluated under transductive poisoning attacks, despite the paper's key finding that GraphLLMs are particularly vulnerable to training-data corruption; hence the claim of 'balanced robustness' is not established in the poisoning setting.
- No adaptive attacks are considered against SFT-auto; detection relies on a fixed cosine-similarity threshold (0.5) without sensitivity analysis, and the method is likely bypassable by an adversary aware of the detection heuristic.
- The LLM-based text attack replaces a very large fraction of nodes (40% evasion, 80% poisoning) with different-class text, which is unrealistic and easily detectable; imperceptibility or semantic preservation is not validated, and word-level attacks are excluded on weak transferability grounds.
- The main results are reported as average ranks without statistical significance tests; many standard deviations overlap, and the exact combination of absolute accuracy and relative drop in the rank metric is not fully specified.
- The complexity analysis contains a mathematically incorrect statement: 'p_attack is bounded above by 2' is meaningless for a fraction; also, no measured inference overhead is provided, and SFT-auto likely requires multiple LLM forward passes per node, making it much more expensive than baselines.
- There is an inconsistency in the reported perturbation ratio for transductive structural attacks: the main text states 0.30 while appendix tables are labeled ptb_rate=0.2, harming reproducibility.
- Missing comparisons with existing GraphLLM defenses (e.g., GraphEdit, RLLMGNN) and missing evaluations on large datasets (ArXiv, Computer for several methods) limit the generality of conclusions.

### Questions

- How does SFT-auto perform under adaptive attacks that are aware of its detection mechanism (e.g., text modifications with high similarity to original nodes, or structural attacks that preserve embedding similarity)?
- Why is SFT-auto not evaluated in transductive poisoning settings, where the paper itself shows GraphLLMs are most vulnerable? What are the results for SFT-auto under those settings?
- How sensitive are the findings to the cosine-similarity threshold (0.5) and to the perturbation ratios? Would the text-structure trade-off persist at lower, more realistic attack budgets (e.g., 10% text perturbation)?
- Are the head-to-head differences between SFT-auto and baselines statistically significant given the reported standard deviations? What is the exact ranking metric used in Figures 2 and 3?
- Can the LLM-based text attack preserve semantics and unnoticeability? Would results change with more constrained attacks like TextFooler or WTGIA?
- What is the actual end-to-end training and inference overhead of SFT-auto compared to SFT-neighbor? Does the detection stage require an additional LLM forward pass for every node?
- How does SFT-auto compare with other GraphLLM defense methods such as GraphEdit and RLLMGNN in terms of robustness and computational cost?

### Limitations

- The proposed SFT-auto framework is only validated in inductive/evasion scenarios; no evidence supports its effectiveness in transductive/poisoning scenarios, which are critical given the paper's own findings.
- The evaluation is restricted to node classification; other TAG tasks like link prediction or graph classification are not covered.
- The threat model is primarily transfer-based; fully adaptive attacks are only explored for GNNGuard (PGD-Guard), not for SFT-auto.
- High perturbation ratios (40% text, 20-30% structure) may be unrealistic in practice and could favor defenses relying on simple outlier removal.
- SFT-auto requires supervised attack labels and a fixed similarity threshold, limiting its applicability to unseen attack types without retraining or tuning.
- Scalability concerns prevent evaluation of GraphLLMs and SFT-auto on the largest datasets (e.g., ArXiv is missing for SFT-auto), and several RGNN variants are not evaluated on large datasets.
- The text-structure trade-off is descriptive but lacks theoretical justification or a mechanistic explanation beyond architecture choice.
- Potential negative societal impact is not discussed, though the dual text/structure attack scenarios are socially relevant; the paper is defense-focused and does not warrant additional ethical review.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 386,818
- Cache-hit prompt tokens: 3,840
- Cache-miss prompt tokens: 382,978
- Completion tokens: 24,823
- Reasoning tokens reported: 17,984
- Total tokens: 411,641
- Estimated total: $0.06057811

Full individual reviews and raw JSON responses are in `review_bundle.json`.
