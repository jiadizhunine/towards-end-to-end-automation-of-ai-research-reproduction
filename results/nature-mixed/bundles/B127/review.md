# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B127.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.031570**

## Final Meta-review

This paper develops a tractable mean-field (MF) theory for the Bayesian posterior of two-layer non-linear neural networks trained with stochastic gradient Langevin dynamics (SGLD). The authors show that the basic MF theory captures the onset of feature learning (FL) as a symmetry-breaking phase transition but underestimates post-transition generalization gains. They identify input feature selection (IFS) as the missing mechanism and propose MF-ARD, which extends the MF theory with Automatic Relevance Determination (coordinate-wise learnable variances). MF-ARD quantitatively matches SGLD-trained network performance on k-sparse parity and single-index tasks, and a theorem shows it eliminates the O(d) curse of dimensionality inherent in plain MF. The paper provides a hierarchy of theories (SGLD → MF → NNGP) with increasing simplification, offering mechanistic insight into feature learning as a two-stage process: phase transition onset followed by self-reinforcing feature selection.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.800 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.632 | 2-4 |
| Significance | 3 | 3.400 | 0.490 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.632 | 2-4 |
| Contribution | 3 | 3.400 | 0.490 | 3-4 |
| Overall | 7 | 6.800 | 0.748 | 6-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Clear hierarchical theoretical framework (SGLD → MF → NNGP) that provides conceptual clarity and tractability
- Novel identification of input feature selection (IFS) as a key mechanism missing from standard MF theory, with an elegant ARD-based fix
- Theorem 4.1 provides a concrete theoretical result showing MF-ARD eliminates the O(d) penalty in input dimension, offering a mechanistic explanation for how FL overcomes the curse of dimensionality
- Quantitative empirical validation on k-sparse parity and single-index models, showing MF-ARD closely tracks SGLD learning curves and phase boundaries
- The two-stage picture of FL (onset via phase transition + specialization via self-reinforcing IFS) provides a useful conceptual framework
- Comprehensive related work discussion and well-contextualized contribution

### Weaknesses

- Theorem 4.1 relies on an ε-symmetry-breaking assumption that is stated but not proven or empirically verified, weakening the theoretical contribution
- The theory is restricted to two-layer networks and target functions with sparse structure, limiting generalizability
- The 'helpful noise' regime (kink around κ=0.05 in Figure 5) is observed but not mechanistically explained
- Sensitivity to the ARD hyperparameter α₀ is claimed to be minimal but not systematically tested
- The static posterior view does not fully capture training dynamics; the connection to dynamics is only briefly discussed
- Comparison with dynamical mean-field theory (DMFT) approaches is cursory; a direct quantitative comparison would strengthen the claims
- The main text is dense and some derivations are hard to follow; more intuitive explanations would improve accessibility

### Questions

- Can the ε-symmetry breaking assumption in Theorem 4.1 be justified more rigorously or verified empirically? Under what conditions does it hold in practice?
- How sensitive are the quantitative predictions to the ARD hyperparameter α₀? Can you provide a systematic study over a wider range of values?
- Can you provide a mechanistic explanation for the 'helpful noise' regime (the kink around κ=0.05 in Figure 5)? Why does moderate noise lower the critical sample size P_c?
- How does MF-ARD compare quantitatively with dynamical mean-field theory (DMFT) approaches (e.g., Bordelon & Pehlevan) on the same tasks?
- How would MF-ARD perform on targets requiring distributed representations (e.g., smooth functions of many variables)? Does the ARD mechanism fail or underperform in such cases?
- How well does the fixed-point iteration in Algorithm 1 correspond to actual SGLD training dynamics, especially in terms of convergence time and potential divergence?
- How do the results change with different activation functions (e.g., tanh, sigmoid) or with γ ≠ 0.5?

### Limitations

- The theory is limited to two-layer networks; extension to deeper architectures (convolutional, attention) remains an open challenge
- The ARD mechanism is best suited for sparse target functions; its effectiveness for distributed or smooth representations is unclear
- Theorem 4.1 relies on an unproven ε-symmetry breaking assumption, limiting the rigor of the curse-of-dimensionality result
- The static posterior view does not capture the full training dynamics, and the connection between the two is not fully explored
- Empirical validation is limited to synthetic tasks (parity, single-index); applicability to real-world datasets is not demonstrated
- The paper does not discuss potential negative societal impacts, though this is a theoretical work with limited direct societal implications

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 215,712
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 206,752
- Completion tokens: 9,285
- Reasoning tokens reported: 0
- Total tokens: 224,997
- Estimated total: $0.03157017

Full individual reviews and raw JSON responses are in `review_bundle.json`.
