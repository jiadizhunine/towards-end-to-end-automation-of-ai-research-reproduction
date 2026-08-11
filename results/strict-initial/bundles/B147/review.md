# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B147.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 2, 'Reject': 3}
- Estimated API cost: **$0.023451**

## Final Meta-review

The paper proposes SPA, a two-stage framework for training LLM agents in out-of-distribution (OOD) environments. Stage 1 performs a supervised fine-tuning (SFT) stage on self-play rollouts, augmenting raw observations with hand-crafted coordinate descriptions and training the model to predict current and next states before actions (transition modeling). Stage 2 initializes PPO from this SFT checkpoint. Experiments on Sokoban, FrozenLake, and Sudoku across several Qwen and LLaMA models report consistent improvements in Pass@1 and Pass@8 over vanilla RL, state-estimation-only RL, and the VAGEN baseline, with small models sometimes outperforming a 20B model evaluated zero-shot. The paper also presents ablations and a study of Pass@k dynamics during RL.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 2 | 2.400 | 0.490 | 2-3 |
| Quality | 2 | 2.600 | 0.490 | 2-3 |
| Clarity | 2 | 2.000 | 0.632 | 1-3 |
| Significance | 3 | 2.600 | 0.490 | 2-3 |
| Soundness | 2 | 2.600 | 0.490 | 2-3 |
| Presentation | 2 | 2.000 | 0.632 | 1-3 |
| Contribution | 2 | 2.600 | 0.490 | 2-3 |
| Overall | 4 | 5.000 | 0.894 | 4-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Identifies an important and underappreciated failure mode: vanilla agentic RL can improve Pass@1 while degrading Pass@k in OOD environments, and proposes Pass@k as a diagnostic for world-model or coverage learning.
- The SPA recipe is simple, compute-efficient, and yields large and consistent gains across multiple base models (Qwen2.5-0.5B/1.5B/3B, LLaMA3.2-1B) and three environments, with some small models outperforming a much larger zero-shot reference.
- Ablations are extensive and informative, covering transition-mask supervision, ground-truth versus self-belief states, random-action data generation, incorrect coordinates, number of SFT epochs, and easy-to-hard transfer.
- The comparison to VAGEN is conducted under the same state-estimation setting, strengthening the claim that offline/SFT transition modeling is preferable to online reward-based world modeling in this context.
- The method is reproducible from the provided algorithmic description and is built on an open codebase, with useful practical details such as batch sizes and training steps.

### Weaknesses

- Despite the 'world model' terminology, the learned transition model is never used for planning, rollouts, or simulation at inference or during RL; it serves only as an SFT initialization, making claims about simulating future states overstated.
- State estimation relies on hand-crafted, environment-specific coordinate abstractions (player/box/goal coordinates), which require domain engineering and limit applicability to new or real-world environments; no automatic state representation is proposed.
- Evaluation is restricted to small, deterministic, fully observable text-grid tasks (Sokoban, FrozenLake, 4x4 Sudoku); stochastic transitions, partial observability, and high-dimensional or multi-modal observations are not tested despite being cited as motivating scenarios.
- The OOD claim is not convincingly established: the evidence is mainly based on perplexity of state strings, and the tasks are small synthetic grids; no genuinely unseen environment distributions are evaluated.
- No statistical significance or variance analysis is provided. Results appear to be single-run point estimates without seeds or error bars, so the magnitude of improvements may be partly due to noise.
- The definition and computation of Pass@1 and Pass@k are inconsistent across the paper (e.g., greedy vs sampling, number of samples, temperature), which hampers reproduction.
- The term 'self-play' is misleading: there is no opponent or iterative self-improvement; the data is simply collected from the base policy interacting with the environment.
- The paper lacks key baselines such as standard SFT on successful trajectories, behavior cloning, or a compute-equalized comparison where vanilla RL is given the same total training budget as SPA.
- Presentation quality is poor: duplicated paragraphs (Section 2.2, Appendices B/C), mismatched table captions and figure references, and an empty Appendix A in the submission make reproduction difficult.
- In the later phase of RL, Pass@k still declines; the paper does not establish that SPA prevents the exploitation collapse, only that it delays it.

### Questions

- How exactly are Pass@1 and Pass@k computed? Is Pass@1 greedy decoding or the mode of sampled trajectories, and are results averaged over multiple seeds with confidence intervals?
- Is the predicted next state ever used at inference or during RL to condition subsequent actions or for imagined rollouts, or is it purely a training signal? If the latter, what evidence indicates the model has internalized a world model rather than just a better policy initialization?
- How does SPA compare with an SFT baseline trained on the same self-play rollouts but only on action tokens (without next-state prediction), followed by PPO? Does next-state prediction add benefit beyond learning action priors?
- How are the 1,280 SFT samples selected and filtered? What is the success rate and instruction-following rate of the base model during data collection, and how does filtering change the data distribution?
- Could the state coordinate descriptions be generated automatically or learned? How would SPA work in a partially observable or rich-modality environment where such ground-truth coordinates are unavailable?
- What is the exact reward formulation for each environment, and were VAGEN hyperparameters tuned under the same compute budget and SFT initialization as SPA?
- In the later RL phase, Pass@k declines—does this reflect policy entropy collapse, and does SPA only postpone this decline? Would longer training erase the improvements?

### Limitations

- Hand-crafted state abstractions require domain expertise and cannot be easily transferred to new tasks or real-world domains.
- The method is evaluated only on small, deterministic grid/text environments; stochastic dynamics, partial observability, and large-scale or multi-modal tasks remain untested.
- The learned transition model is not used for planning or simulation, so the full model-based RL promise is not realized.
- No multi-seed or statistical significance testing is reported; empirical claims may be sensitive to random seeds.
- The success of SFT depends on base-model instruction compliance, and extra filtering steps are needed without a clear quantitative analysis.
- SFT adds extra compute and hyperparameters that are not accounted for in a compute-equalized comparison against vanilla RL.
- Cross-game generalization is shown to fail, raising questions about the generality of the learned world model.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 126,260
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 122,164
- Completion tokens: 22,630
- Reasoning tokens reported: 15,090
- Total tokens: 148,890
- Estimated total: $0.02345083

Full individual reviews and raw JSON responses are in `review_bundle.json`.
