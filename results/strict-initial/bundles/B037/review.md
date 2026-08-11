# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B037.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **5/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 3, 'Reject': 2}
- Estimated API cost: **$0.018973**

## Final Meta-review

The paper introduces LEAP, a learnable local structural positional encoding for graphs based on the local Euler Characteristic Transform (ℓ-ECT). LEAP computes differentiable ECTs on normalized m-hop neighborhoods across multiple directions and thresholds, then applies one of five learnable projection strategies (linear, 1D convolution, DeepSets, transformer, or transformer with direction conditioning) to produce node embeddings. The method is end-to-end trainable and can be integrated with GNNs or transformer-style architectures. Experiments on a synthetic edge-counting task, multiple TUDatasets, and Alchemy/HIV evaluate LEAP against RWPE and LaPE using GCN, GAT, and a transformer without message passing (NoMP). The paper reports consistent improvements over baselines in most settings, along with ablations on projection strategy, neighborhood size, embedding dimension, and DECT hyperparameters.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 3 | 2.800 | 0.400 | 2-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 2.800 | 0.400 | 2-3 |
| Overall | 5 | 5.600 | 0.490 | 5-6 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Novel synthesis of the local Euler Characteristic Transform and modern deep learning, making the ℓ-ECT learnable for graph positional encodings.
- Comprehensive empirical evaluation across multiple datasets, architectures, and baselines, including ablations on key components.
- The synthetic experiment demonstrates that LEAP can capture structural information (e.g., edge counts) even when node features are uninformative, while standard MPNNs fail.
- Flexible design: supports end-to-end training, learnable directions, multiple permutation-invariant projection strategies, and integration with various backbones.
- Clear exposition of the methodology and related background on ECTs, PEs, and MPNN limitations.

### Weaknesses

- Baselines are limited to RWPE and LaPE; more recent and potentially stronger PEs (e.g., SignNet, PEG, subgraph-based PEs) are not compared, weakening the claim of consistent superiority.
- No statistical significance tests (e.g., paired t-tests, confidence intervals) are reported; many improvements are small with overlapping variance.
- Computational and memory complexity of per-node local ECT computation is not analyzed; scalability to large or dense graphs is unknown.
- Theoretical guarantees of the exact ECT (e.g., injectivity) do not directly apply to the differentiable approximation and normalization used in LEAP, and the paper does not empirically probe this.
- The synthetic task (3-node graphs by edge count) is trivially simple and does not convincingly demonstrate complex topological expressivity.
- On HIV, LaPE outperforms LEAP, indicating that global information can be more important; LEAP's local-only nature is a limitation.
- Five projection strategies are proposed, but no clear guidance is given on selection; results show dataset-dependent performance, leaving a practical gap.
- The paper does not specify how node features are defined for datasets lacking natural attributes, which hinders reproducibility.

### Questions

- How does LEAP compare to stronger recent PEs like SignNet, PEG, or persistent-homology-based methods on standard benchmarks (e.g., ZINC, OGB)?
- What is the time and memory complexity of LEAP per node? How does it scale to graphs with high degree or millions of nodes?
- Are the reported improvements statistically significant? Were multiple seeds and paired significance tests performed?
- What is the exact formulation of the differentiable approximation (e.g., sigmoid temperature, threshold grid) and how are directions learned?
- How does LEAP behave when node features are noisy or categorical? Is the method still robust?
- Why does the 1-hop neighborhood consistently perform best? Could this indicate that larger hops oversmooth or dilute structural information?
- Could LEAP be combined with global PEs (e.g., LaPE) to capture both local and global structure, and would this improve results on HIV?

### Limitations

- LEAP is not purely structural; it depends on node features (though these can be learned), which may be unavailable or noisy in some applications.
- The differentiable approximation of the ECT and the normalization of features break the theoretical guarantees of the exact ECT, so injectivity is not guaranteed.
- The method introduces several hyperparameters (directions, thresholds, smoothing, locality radius, projection choice) that require tuning; ablation suggests robustness, but no systematic guideline is provided.
- Scalability is unaddressed: computing ECTs for m-hop subgraphs with a 16×16 grid for every node may be prohibitive for large or dense graphs.
- The empirical evaluation is confined to small/mid-sized TUDatasets and a synthetic toy; performance on large-scale graph-level or node-level tasks is not demonstrated.
- The choice of projection strategy is left as a hyperparameter with no principled way to select, and some projections are not permutation-invariant to direction order.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 98,726
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 94,630
- Completion tokens: 20,403
- Reasoning tokens reported: 14,421
- Total tokens: 119,129
- Estimated total: $0.01897251

Full individual reviews and raw JSON responses are in `review_bundle.json`.
