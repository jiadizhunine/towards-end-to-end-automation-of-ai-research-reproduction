# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B127.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.035397**

## Final Meta-review

The paper develops a mean-field (MF) theory for the Bayesian posterior of two-layer ReLU networks trained with stochastic gradient Langevin dynamics (SGLD), positioned between the fully interacting posterior and the NNGP limit. It interprets the onset of feature learning as a symmetry-breaking phase transition, identifies input feature selection (IFS) as a missing mechanism in plain MF, and extends MF with an Automatic Relevance Determination (ARD) prior (MF-ARD) to capture IFS. The paper proves a conditional scaling theorem claiming that ARD removes an O(d) penalty in the critical noise, and presents numerical experiments on sparse parity and single-index tasks where MF-ARD matches SGLD better than plain MF.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.000 | 0.000 | 2-2 |
| Clarity | 2 | 2.200 | 0.400 | 2-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 2 | 2.000 | 0.000 | 2-2 |
| Presentation | 2 | 2.200 | 0.400 | 2-3 |
| Contribution | 2 | 2.400 | 0.490 | 2-3 |
| Overall | 4 | 4.000 | 0.000 | 4-4 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Provides a clear conceptual hierarchy (SGLD posterior, MF, NNGP) that makes feature-learning onset interpretable as a phase transition followed by specialization.
- The ARD extension is minimal and principled, preserving tractability while capturing heavy-tailed coordinate marginals and sparsification observed in SGLD-trained networks.
- The scaling theorem (Theorem 4.1) offers an elegant message: ARD changes critical noise scaling from ~1/sqrt(dk) to ~1/sqrt(k), potentially explaining how feature learning overcomes the curse of dimensionality for sparse targets.
- Empirical phase diagrams for k-sparse parity and single-index tasks show that MF-ARD substantially improves on plain MF in matching the location and sharpness of the SGLD transition, including the 'helpful noise' regime.
- The appendix provides detailed algorithms and hyperparameter tables, aiding reproducibility.

### Weaknesses

- The central Theorem 4.1 relies on an unproven epsilon-symmetry-breaking assumption; the proof only shows amplification of a pre-existing gap, not its emergence, making the headline curse-of-dimensionality result conditional and partially circular.
- The MF and MF-ARD derivations are heuristic (saddle-point/free-energy stationarity) without rigorous error bounds or a controlled limit showing the factorized posterior approximates the true SGLD posterior.
- Empirical validation is limited to two synthetic sparse tasks with small input dimensions (d=35, 18) and few seeds; no error bars, statistical tests, or comparisons to alternative theories (e.g., DMFT, kernel renormalization) are provided.
- The particle-based Algorithm 1 is used for MF and MF-ARD rather than directly solving the fixed-point equations; its equivalence to the derived equations and convergence to stationarity are not established.
- The quantitative claim is overstated: phase diagrams show qualitative agreement with visible discrepancies, and sensitivity to ARD hyperparameters (alpha0, beta0, EMA rate) is not systematically explored.
- The main text omits several key equations, and the appendix contains duplicated theorem/proof blocks and empty placeholders, impairing readability and verifiability.

### Questions

- Can the epsilon-symmetry-breaking assumption in Theorem 4.1 be derived from the isotropic prior or from the MF phase transition, or is it an additional unproven condition? If not, what evidence shows it holds for SGLD-trained networks?
- How sensitive are the results to the ARD hyperparameters alpha0, beta0, and the EMA rate? The paper uses specific values (alpha0=4.0 for parity, 0.1 for single-index) without justification or a wide sensitivity study.
- How does MF-ARD compare quantitatively to existing state-of-the-art predictive theories (e.g., DMFT, kernel renormalization) on the same tasks? Are its predictions more accurate than those baselines?
- Does the particle-based SGLD algorithm with ARD updates converge to the same stationary solution as the derived MF-ARD fixed point? Were the 7.5M steps sufficient to reach stationarity?
- Can MF-ARD be extended to tasks with non-sparse or distributed features, such as random features, smooth target functions, or real-world datasets?
- How is the infinite-data scaling of Theorem 4.1 connected to the finite-P phase boundaries shown in the experiments?

### Limitations

- The theory is restricted to two-layer fully connected ReLU networks; deeper architectures, convolutions, and attention are not addressed.
- The framework is tailored to tasks with sparse or low-dimensional structure; its applicability to distributed or smooth representations is uncertain.
- The main scaling result is conditional on an externally assumed symmetry-breaking seed, limiting its generality.
- The static posterior framework does not model the actual training dynamics or convergence time of SGLD; finite-time and non-equilibrium effects are not discussed.
- The ARD mechanism relies on coordinate-wise precision variables, which may not capture distributed or entangled feature representations.
- No real-world datasets, high-dimensional scaling studies, or systematic sweeps over N, d, k, and hyperparameters are included.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 204,865
- Cache-hit prompt tokens: 3,840
- Cache-miss prompt tokens: 201,025
- Completion tokens: 25,867
- Reasoning tokens reported: 19,150
- Total tokens: 230,732
- Estimated total: $0.03539701

Full individual reviews and raw JSON responses are in `review_bundle.json`.
