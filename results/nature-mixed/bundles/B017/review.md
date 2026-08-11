# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B017.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.043158**

## Final Meta-review

This paper introduces MF-MAPPO, a mean-field extension of Proximal Policy Optimization (PPO) for zero-sum team games (ZS-MFTGs) that combine intra-team cooperation with inter-team competition. The algorithm uses a shared actor network per team and a minimally-informed critic that depends only on team population distributions (mean-fields), enabling scalability to thousands of agents. The paper provides theoretical guarantees connecting finite-population training to infinite-population optimality, policy gradient convergence, and generalization across population sizes. For partially observable settings, it proposes a gradient-regularized training scheme and a Dynamic-Projected Consensus (D-PC) estimator for decentralized opponent mean-field estimation with exponential convergence guarantees. The authors introduce MFEnv, a benchmarking platform with constrained Rock-Paper-Scissors (cRPS) and a grid-based Battlefield game, and demonstrate that MF-MAPPO outperforms the DDPG-MFTG baseline.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 2.800 | 0.400 | 2-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 2.800 | 0.400 | 2-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.000 | 0.632 | 5-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important and underexplored gap in mean-field MARL: mixed cooperative-competitive zero-sum team games (ZS-MFTGs).
- The algorithm design is practical and scalable, with a shared actor and minimally-informed critic that reduce computational complexity.
- Provides solid theoretical grounding, including finite-population optimality bounds (O(1/sqrt(N))), policy gradient convergence, and policy transfer guarantees.
- The D-PC estimator for partially observable settings is a novel contribution with exponential convergence guarantees.
- Introduces useful benchmark environments (MFEnv) that could benefit the community.
- Empirical results demonstrate scalability to thousands of agents and emergent heterogeneous behaviors from identical policies.
- The paper is generally well-written and organized, with comprehensive appendices.

### Weaknesses

- Limited baseline comparisons: only DDPG-MFTG is used; other mean-field methods (MF-Q, MF-AC) or large-scale MARL algorithms (e.g., MAPPO with parameter sharing) are not considered.
- Theoretical proofs, particularly Theorem 2, are presented as sketches with high-level arguments (e.g., LLN convergence without explicit rates) and rely on several assumptions that may be hard to verify.
- Experimental evaluation lacks statistical rigor: no error bars, confidence intervals, or significance tests are reported in some cases; limited number of seeds.
- The partially observable extension relies on restrictive assumptions (connected communication graphs, specific visibility models) that may not generalize to real-world scenarios.
- Benchmark environments are relatively simple grid-worlds; practical impact for real-world large-scale applications is not fully demonstrated.
- The claim of being 'first PPO-based algorithm for mixed cooperative-competitive mean-field settings' is somewhat overstated given prior work in related areas.
- The gradient regularization method is somewhat ad hoc, with no principled guidance for selecting the penalty coefficient lambda.
- Computational complexity and memory requirements are not adequately discussed; training times are significant (up to 3 days on a single GPU).

### Questions

- How does MF-MAPPO compare to other mean-field baselines like MF-Q or MF-AC on the cRPS environment? Would these be tractable at this scale?
- Can you provide a comparison with simpler baselines such as independent PPO (without mean-field inputs) to isolate the benefit of the mean-field approximation?
- In Theorem 2, can you provide explicit convergence rates or a more rigorous proof? What are the exact conditions under which the policy gradient converges?
- How sensitive is MF-MAPPO to hyperparameters (entropy coefficient, clip value, learning rates, gradient penalty lambda)? Have you performed ablation studies?
- What happens when the two teams have different population sizes? Does the ratio N1/N2 affect the theoretical guarantees or empirical performance?
- How does performance degrade when the communication graph is disconnected (violating Assumption 2)?
- Can you provide more quantitative results for the battlefield experiments (e.g., fraction of Blue agents reaching the target, number of deactivations) rather than just qualitative trajectory analysis?
- The paper claims scalability to thousands of agents, but battlefield training uses only 100 agents per team. Why not train with larger populations?
- What are the hardware specifications for the training time comparisons (DDPG-MFTG 60h vs MF-MAPPO 2h)? Are these fair comparisons with the same number of environment steps?
- Could you clarify the privacy guarantees of D-PC? What exactly is preserved and under what threat model?

### Limitations

- The paper acknowledges scaling limitations with state dimensionality but could discuss this more thoroughly and propose specific future directions.
- The theoretical framework assumes finite discrete state and action spaces, limiting applicability to continuous control problems.
- The D-PC estimator requires connected communication graphs and specific regularity conditions that may not hold in all practical scenarios.
- The potential negative societal impact of large-scale competitive team RL (e.g., military applications of battlefield scenarios) is not discussed.
- No code or benchmark platform is publicly released, limiting reproducibility and the practical value of MFEnv.
- The evaluation is limited to simulated grid-world environments; no real-world or more complex robotic applications are demonstrated.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 293,813
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 284,853
- Completion tokens: 11,619
- Reasoning tokens reported: 0
- Total tokens: 305,432
- Estimated total: $0.04315783

Full individual reviews and raw JSON responses are in `review_bundle.json`.
