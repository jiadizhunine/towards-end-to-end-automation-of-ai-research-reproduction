# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B037.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.016959**

## Final Meta-review

The paper introduces LEAP (Local ECT-based Learnable Positional Encodings), a novel end-to-end trainable local structural positional encoding for graphs based on the local Euler Characteristic Transform (ℓ-ECT). LEAP computes differentiable ECTs on local neighborhoods of nodes, followed by learnable projection strategies to generate node-level embeddings. The authors propose five projection strategies (linear, 1D convolutions, DeepSets, attention, attention with PE) and evaluate LEAP on multiple real-world datasets (TU benchmark, Alchemy, HIV) and a synthetic task, comparing against established baselines (RWPE, LaPE) across multiple architectures (GCN, GAT, GIN, NoMP). Results show consistent improvements over baselines, with learnable directions providing additional benefits. The paper also includes extensive ablation studies on hyperparameters, embedding dimensions, and locality parameters.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 4 | 3.800 | 0.400 | 3-4 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.200 | 0.400 | 3-4 |
| Presentation | 4 | 3.800 | 0.400 | 3-4 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 7 | 6.600 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel combination of topological methods (ℓ-ECT) with deep learning in an end-to-end trainable framework, representing a unique contribution to graph positional encodings
- Comprehensive empirical evaluation across multiple datasets, architectures (GCN, GAT, GIN, NoMP), and five different projection strategies
- Clear theoretical grounding in prior work on ECT injectivity and ℓ-ECT expressivity, providing a solid foundation
- Thoughtful analysis of permutation invariance properties of the different projection strategies
- Well-designed ablation studies examining locality, embedding dimension, and DECT hyperparameters
- Code is provided for reproducibility, with fixed seeds and detailed experimental configurations
- The NoMP architecture provides a clean way to isolate the contribution of the positional encoding itself

### Weaknesses

- Limited theoretical novelty - the paper relies heavily on prior work (von Rohrscheidt & Rieck, 2025) for expressivity guarantees without providing new theory specific to LEAP
- The synthetic experiment (Section 4.1) is relatively trivial (3-node graphs with 0-3 edges), and the authors note that LaPE and RWPE also achieve perfect accuracy, limiting the demonstration of LEAP's unique capabilities
- Performance gains on smaller datasets (COX2, BZR, DHFR) are modest (3-11% relative improvement), raising questions about practical significance and statistical significance is not thoroughly tested
- Comparison with baselines is limited to RWPE and LaPE; more recent PE methods (e.g., SignNet, PEG) are not considered
- The comparison with DECT (Table S.2) is somewhat unfair since DECT is designed for graph-level descriptors, not node-level PEs
- Computational overhead is non-trivial (preprocessing time 11.57s for Roman Empire vs 0.18s for RWPE, ~2x training time per epoch), and scalability to very large graphs is not demonstrated
- The paper does not provide a thorough analysis of when LEAP fails or where it is most beneficial compared to other PEs

### Questions

- The paper states LEAP is 'specifically geared to work with geometric graphs,' but most experiments use non-geometric datasets. Could you elaborate on how LEAP performs on datasets with explicit geometric node features (e.g., 3D coordinates in molecular datasets like QM9 or MD17)?
- In the synthetic experiment, you note that LaPE and RWPE also achieve perfect accuracy. Can you design a more challenging synthetic task where LEAP's unique properties (e.g., handling of geometric features, combination of topology and geometry) would be more clearly demonstrated?
- For the HIV dataset, LaPE outperforms both LEAP variants. You suggest combining LaPE and LEAP helps. Can you provide more details on how the combination was performed (concatenation, weighted sum, etc.) and whether this combination approach generalizes to other datasets?
- The learnable directions in LEAP-L provide improvements in most cases. Can you provide intuition or analysis for why learning the directions helps? Is it learning to focus on discriminative directions or something else?
- The paper mentions that LEAP can be applied to learned features. In the HIV experiments, you use a learnable embedding layer. How sensitive is LEAP to the quality of these learned features, and does it require careful initialization?
- The improvements on COX2 and BZR datasets are marginal (3-8%). Have you performed statistical significance tests (e.g., paired t-tests or Wilcoxon signed-rank tests) to confirm these differences are meaningful?
- How does LEAP scale to very large graphs (millions of nodes)? The preprocessing time for the Roman Empire dataset (11.57 seconds) is substantial compared to RWPE (0.18 seconds).
- Have you considered comparing LEAP with other recent learnable PEs beyond RWPE and LaPE, such as SignNet or other topological approaches like persistent homology-based encodings?
- The 'NoMP' architecture seems to be a transformer without message passing. How does this compare to standard graph transformers like GPS? Would LEAP provide similar benefits when integrated into more sophisticated architectures?

### Limitations

- LEAP requires node features to compute ECTs, making it not a purely structural positional encoding (though the authors suggest learned features could address this)
- The theoretical guarantees of the exact ECT (injectivity) may not fully carry over to the differentiable approximation used in LEAP, especially for non-geometric graphs
- LEAP introduces multiple hyperparameters (number of directions, thresholds, smoothing parameter, locality m, projection strategy) that may require tuning for optimal performance on new datasets
- The method's performance on the HIV dataset shows that global positional information (LaPE) can sometimes be more valuable than local structural encodings, suggesting LEAP may be most effective when combined with complementary PEs
- The computational overhead of LEAP, particularly for large graphs, may limit its scalability compared to simpler PEs
- The paper does not address potential negative societal impacts, though this is common for methodological papers in graph representation learning with no direct societal applications

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 109,500
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 100,540
- Completion tokens: 10,208
- Reasoning tokens reported: 0
- Total tokens: 119,708
- Estimated total: $0.01695893

Full individual reviews and raw JSON responses are in `review_bundle.json`.
