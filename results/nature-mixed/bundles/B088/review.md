# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B088.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **5/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 1, 'Reject': 4}
- Estimated API cost: **$0.013076**

## Final Meta-review

The paper introduces MCCE (Multi-LLM Collaborative Co-evolution), a hybrid optimization framework that combines a frozen closed-source LLM (e.g., GPT-4o) with a lightweight trainable local model (Qwen2.5-7B) for multi-objective discrete optimization, demonstrated on molecular drug design with five objectives (QED, SAscore, DRD2, GSK3β, JNK3). The framework operates in an evolutionary loop where the two models alternate as genetic operators, with the local model periodically fine-tuned via Direct Preference Optimization (DPO) using similarity-filtered preference pairs constructed from successful search trajectories. The authors argue this co-evolution enables mutual inspiration: the large model provides global exploration while the small model internalizes experience through parameter updates. Experiments show that MCCE with DPO achieves the highest Hypervolume and Top-k fitness scores compared to single-model baselines and alternative training paradigms (SFT, RL), with evidence that both models benefit from collaboration.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.400 | 0.490 | 2-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 2.600 | 0.490 | 2-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 2.800 | 0.400 | 2-3 |
| Overall | 5 | 5.400 | 0.490 | 5-6 |
| Confidence | 4 | 3.600 | 0.490 | 3-4 |

### Strengths

- Novel and well-motivated framework combining frozen closed-source LLMs with trainable open-source models in a co-evolutionary loop, addressing a real limitation of purely prompt-based or purely trainable approaches.
- Clear demonstration that DPO outperforms SFT and RL for this setting, with thoughtful analysis of why (catastrophic forgetting for SFT, reward instability for RL).
- The similarity-based data synthesis for DPO is a clever contribution that addresses distribution shift and training instability, with reasonable algorithmic detail and fallback rules.
- Comprehensive evaluation on a challenging 5-objective drug design problem with multiple metrics (Top-k fitness, AUC, uniqueness, diversity, HV, validity), with results reported over 10 runs.
- The framework is presented as general-purpose and extensible to other discrete optimization domains, broadening its potential impact.
- Well-written and organized paper with clear figures and a reproducible methodology description.
- Ablation studies comparing DPO, SFT, and RL co-evolution variants help isolate the contribution of the training paradigm.

### Weaknesses

- Critical lack of comparison with the most relevant state-of-the-art baselines, specifically ExLLM (Ran et al., 2025) and MoLLEO (Wang et al., 2024), which are cited as prior work. Without these comparisons, the claim of 'state-of-the-art' is not well-supported.
- No statistical significance testing (e.g., t-tests, Wilcoxon) despite reporting overlapping standard deviations across many metrics; some improvements may not be significant.
- No comparison with strong non-LLM baselines such as traditional multi-objective evolutionary algorithms (NSGA-II, MOEA/D), GFlowNets, or Bayesian optimization, which are standard in molecular optimization.
- The claim of 'mutual inspiration' is overstated since the API model is frozen and only benefits indirectly through improved population quality; the co-evolution is asymmetric.
- Evaluation is limited to a single domain (molecular design), despite claims of generality to other discrete optimization problems.
- The similarity-based data synthesis introduces several hyperparameters (α, I1-I3, μ±σ filter) but lacks sensitivity analysis to show robustness.
- Computational cost (API calls, training time, GPU requirements) is not discussed, which is important for practical adoption.
- The validity of generated molecules decreases for dpo_coevolve (0.820) compared to the frozen LLM (0.902) and even the untrained Qwen (0.838), suggesting a potential trade-off from training that is not adequately discussed.
- The 'co-evolutionary curve' is presented qualitatively without clear quantitative metrics of how the two models complement each other over time.

### Questions

- Why were ExLLM and MoLLEO, which are cited as the most relevant prior work, not included as baselines in the experiments? Can you provide a comparison using the same evaluation setup?
- How does MCCE compare to standard multi-objective evolutionary algorithms (e.g., NSGA-II, MOEA/D) or GFlowNets on the same 5-objective task?
- Have you conducted statistical significance tests (e.g., paired t-tests or Wilcoxon signed-rank tests) to confirm that improvements over baselines are significant given the reported standard deviations?
- What is the total computational cost of the framework, including the number of API calls to the frozen LLM, the training time for the local model, and the hardware requirements?
- Can you provide a sensitivity analysis for the key hyperparameters in the similarity-based data synthesis (α, similarity intervals I1-I3, update frequency f, dataset size D)?
- How is the 'breakthrough' trajectory defined exactly? Is it based on Pareto dominance or scalarized score improvement?
- The paper claims 'mutual inspiration'—can you provide evidence that the frozen API model's exploration improves over time due to the local model's learning, beyond population-level metrics?
- What is the balance between the frozen LLM and local model in terms of how many candidates each generates per generation? Is this ratio fixed or adaptive?
- Why does the validity of dpo_coevolve decrease compared to the untrained model? Is this a concern for practical drug design applications?
- How sensitive is the method to the choice of the local model size (e.g., 7B vs smaller/larger)? What happens if the API model is unavailable or changes?

### Limitations

- The evaluation is restricted to a single domain (molecular design); the claimed generality to other discrete optimization problems is not empirically demonstrated.
- The paper does not compare against the most relevant prior work (ExLLM, MoLLEO), which weakens the claim of state-of-the-art performance.
- The improvement over baselines is modest and may not be statistically significant given the reported variances.
- The computational and financial costs of relying on closed-source APIs (GPT-4o) are not discussed, limiting practical accessibility.
- The 'mutual inspiration' claim is not fully substantiated since only the local model is trained; the frozen LLM's improvement is indirect at best.
- No analysis of failure cases or scenarios where the similarity-based filtering might discard useful training data.
- Potential negative societal impact: the framework could be misused for designing molecules with harmful properties (e.g., toxins, chemical weapons), a general concern for drug design tools that is only briefly addressed.
- No discussion of potential biases in the ZINC dataset or the objectives used.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 77,155
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 68,195
- Completion tokens: 12,513
- Reasoning tokens reported: 0
- Total tokens: 89,668
- Estimated total: $0.01307603

Full individual reviews and raw JSON responses are in `review_bundle.json`.
