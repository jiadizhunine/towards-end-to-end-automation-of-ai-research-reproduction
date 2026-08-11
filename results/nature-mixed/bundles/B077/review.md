# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B077.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.027670**

## Final Meta-review

This paper proposes SISL (Self-Improving Skill Learning), a framework for robust skill-based meta-reinforcement learning that addresses the challenge of noisy offline demonstrations in long-horizon tasks. The key contributions are: (1) a decoupled skill self-improvement mechanism with an improvement policy that perturbs trajectories near the offline data distribution to discover higher-quality behaviors, and (2) a skill prioritization approach via maximum return relabeling that assigns hypothetical returns to offline trajectories and reweights samples to focus on task-relevant data. SISL dynamically balances offline and online data contributions through a mixing coefficient, progressively denoising the skill library. The paper evaluates SISL on four long-horizon multi-task environments (Kitchen, Office, Maze2D, AntMaze) with varying noise levels, demonstrating consistent improvements over baselines including SPiRL, SiMPL, PEARL, and SAC variants. The authors also provide extensive ablation studies and analysis of the skill refinement process.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 3.400 | 0.490 | 3-4 |
| Clarity | 4 | 3.800 | 0.400 | 3-4 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 3 | 3.400 | 0.490 | 3-4 |
| Presentation | 4 | 3.800 | 0.400 | 3-4 |
| Contribution | 3 | 3.200 | 0.400 | 3-4 |
| Overall | 7 | 7.000 | 0.632 | 6-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important and under-explored problem: robustness of skill-based meta-RL to noisy offline demonstrations
- Well-motivated framework with clear problem analysis and intuitive figures illustrating the failure mode
- Comprehensive experimental evaluation across four environments with multiple noise levels, including two newly introduced environments (Office, AntMaze)
- Thorough ablation studies examining each component's contribution and key hyperparameters
- Good analysis of the skill refinement process, including visualization of skill evolution and task representations
- Honest discussion of limitations, including computational overhead and meta-test fine-tuning requirements
- Code is provided for reproducibility
- Additional robustness experiments (limited data, random noise injection, diverse sub-optimal datasets) strengthen the claims

### Weaknesses

- Incremental novelty: combines existing techniques (SPiRL, SiMPL, RND, relabeling) in a new way, but individual components are well-known; the contribution is primarily in the specific combination for the noisy demonstration setting
- The improvement policy design is similar to existing exploration techniques (e.g., RND-based), and its novelty over simply using RND in the skill-based setting is not fully clarified
- The maximum return relabeling mechanism is a straightforward application of reward-model-based relabeling, and its interaction with the skill learning objective could be better analyzed theoretically
- Some design choices (e.g., reinitializing the high-level policy every Kiter iterations) seem ad hoc and could use more principled justification
- The paper does not provide theoretical analysis of why the proposed method should be robust to noise, relying solely on empirical evidence
- The comparison with SiMPL baseline may not be fully fair given that SISL has access to additional components (improvement policy, reward model) that SiMPL lacks
- Hyperparameter sensitivity, particularly temperature T and KLD coefficient, requires careful tuning that may limit practical applicability
- Performance gains over baselines are modest in low-noise regimes for some environments
- The method assumes noise primarily affects actions; other types of data corruption (state noise, missing transitions) are not extensively explored

### Questions

- How does the method perform when the number of training tasks is small (e.g., 5-10)? The current experiments use 20-25 training tasks.
- Could the improvement policy πimp discover behaviors that are not realizable by the low-level skill policy, and if so, how does the framework handle this mismatch?
- Is there a risk of catastrophic forgetting of useful offline skills when β becomes very high (close to 1)? How is this mitigated?
- The reward model is trained only on online trajectories - how does this affect relabeling of offline trajectories that may be far from the online data distribution?
- The paper reinitializes the high-level policy πh every Kiter iterations. Could you provide more intuition for why this is necessary? Have you considered more smooth ways to handle this, such as KL regularization during re-training?
- How sensitive is the maximum return relabeling to reward model errors, especially in early training when online data is limited? Could noisy offline trajectories be incorrectly labeled as high-return if the reward model is not yet accurate?
- The mixing coefficient β is computed based on average returns of offline and online buffers. In environments with very different return scales across tasks, how does this affect the balance? Have you considered per-task normalization?
- How does SISL compare to methods that use offline RL techniques (e.g., conservative Q-learning) to handle noisy demonstrations, rather than the proposed exploration-based approach?
- How does the method scale to environments with more complex reward structures than the simple sparse rewards used in the experiments?
- What happens if the noise in offline demonstrations affects not just actions but also state observations?

### Limitations

- The paper acknowledges computational overhead (~16%) and the need for meta-test fine-tuning, which are reasonable limitations.
- The approach assumes that noisy demonstrations are the primary source of data corruption; it may not handle other types of data quality issues (e.g., missing transitions, misaligned observations) as effectively.
- The method requires training an additional improvement policy and reward model, which adds complexity to the overall framework.
- The paper does not analyze potential negative societal impacts beyond a brief statement. While the work is foundational, it could be used in applications where robustness to noisy data might have unintended consequences (e.g., in safety-critical systems).
- The experimental evaluation is limited to simulated environments; real-world validation with physical robots would strengthen the claims.
- Hyperparameter sensitivity requires careful tuning, which may limit applicability in new domains.
- The method requires fine-tuning during meta-test, which adds computational cost; zero-shot adaptation would be more practical.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 185,202
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 176,242
- Completion tokens: 10,611
- Reasoning tokens reported: 0
- Total tokens: 195,813
- Estimated total: $0.02767005

Full individual reviews and raw JSON responses are in `review_bundle.json`.
