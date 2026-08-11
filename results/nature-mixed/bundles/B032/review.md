# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B032.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.028307**

## Final Meta-review

This paper introduces REPIT (Representing Isolated Targets), a framework for isolating concept-specific refusal vectors in LLM activations. REPIT applies a three-step procedure (reweighting, whitening, orthogonalization) to disentangle difference-in-means vectors, enabling selective suppression of refusal on targeted harmful concepts (e.g., weapons of mass destruction) while preserving refusal on other categories. The authors demonstrate the method across five frontier LMs, achieving target-category jailbreak rates of 0.4-0.7 while keeping non-target ASR increases near baseline, using as few as 12 examples on a single GPU. They also show the edit localizes to 100-200 residual dimensions, exposing vulnerabilities in current safety evaluation practices that rely on aggregate benchmark scores. The paper includes a formal threat model, geometric analysis, ablations, and a comprehensive ethics discussion.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 3.200 | 0.400 | 3-4 |
| Clarity | 3 | 3.200 | 0.400 | 3-4 |
| Significance | 4 | 3.600 | 0.490 | 3-4 |
| Soundness | 3 | 3.200 | 0.400 | 3-4 |
| Presentation | 3 | 3.200 | 0.400 | 3-4 |
| Contribution | 3 | 3.200 | 0.400 | 3-4 |
| Overall | 6 | 6.400 | 1.020 | 5-8 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Addresses an important and timely problem: the vulnerability of benchmark-based safety evaluations to targeted, representation-level attacks.
- Technically sound methodology with clear motivation for each disentanglement step (reweighting, whitening, partial orthogonalization), addressing the collinearity issue in DIM vectors.
- Comprehensive evaluation across five diverse models, multiple target concepts, multiple non-target datasets, and generalization tests to other benchmarks.
- Impressive data efficiency demonstration (12 examples suffice), highlighting a practical and low-resource threat model.
- Valuable interpretability analysis showing the edit localizes to 100-200 dimensions and the non-target basis is low-rank.
- Thorough threat model formalization and ethical considerations with concrete defensive recommendations.
- Ablations and geometric analysis (projection diagnostics, tailweight analysis) strengthen the methodological claims.

### Weaknesses

- Lack of comparison to existing disentanglement methods (e.g., LEACE, INLP, iterative nullspace projection), making it difficult to assess relative effectiveness and novelty.
- Evaluation is narrowly focused on WMD-related concepts; generalizability to other harmful domains is only demonstrated in a limited toxicity experiment.
- Reliance on a single judge (LlamaGuard 3) for ASR measurement; no human evaluation or alternative judges to validate results.
- The ρ hyperparameter selection (non-target ASR < 0.1) is arbitrary and not well-justified; sensitivity to this threshold is underexplored.
- The 'evaluation evasion' claim is somewhat overstated since the target concepts are known and could be probed directly.
- Reproducibility is limited by the gated release of WMD prompts, despite code availability.
- The paper provides a concrete recipe for creating stealthy jailbreaks with minimal resources, raising dual-use concerns that are acknowledged but not fully mitigated.

### Questions

- How does REPIT compare quantitatively to existing concept erasure/disentanglement methods such as LEACE, INLP, or simple null-space projection in terms of target ASR and non-target preservation? Have the authors considered including these as baselines?
- How sensitive are the main results to the choice of ρ threshold? Is there a systematic way to select ρ without grid search on validation data?
- How well does REPIT generalize to non-WMD concepts (e.g., hate speech, fraud, privacy violations)? The toxicity experiment is promising but limited in scope.
- Could REPIT-style vectors be detected by existing representation-level auditing methods (e.g., sparse autoencoders, probing, anomaly detection)? Any preliminary analysis would strengthen the threat model discussion.
- The tailweight analysis shows bidirectional flips approaching 10% in some cases—does this suggest the localization claim (100-200 dimensions) is more about noise removal than true signal concentration?
- How do the results change with different ASR judges (e.g., GPT-4, human evaluation)? Are there cases where LlamaGuard's judgments disagree with human assessments?
- How does REPIT relate to prior findings that narrow misalignment is difficult via fine-tuning (Betley et al., 2025; Turner et al., 2025)? Does this suggest activation-space interventions are fundamentally more precise?
- How sensitive is the method to the choice of non-target concepts? Would using a different set of non-target categories substantially change disentanglement quality?

### Limitations

- The paper primarily evaluates on WMD-related concepts, which may have unique representational properties; generalizability to other harmful domains is not thoroughly demonstrated.
- The threat model assumes white-box access to model activations, which limits applicability to many real-world deployment scenarios.
- The method relies on COSMIC for direction selection, which is acknowledged as suboptimal for the three-way target/non-target/harmless objective, potentially limiting performance.
- Detection methods and defensive countermeasures are only suggested, not implemented or evaluated, limiting practical guidance.
- The evaluation relies solely on LlamaGuard as the judge, which may introduce systematic biases.
- The WMD prompts are not publicly available, limiting immediate reproducibility despite planned gated release.
- The paper's detailed technical descriptions of harmful procedures (e.g., explosives synthesis) could enable misuse despite redaction attempts.
- The finding that benchmarks can be evaded may undermine trust in safety evaluation practices without providing immediate alternatives.

### Ethics

Ethical concerns flagged: **True**

## Usage and Cost

- Requests: 6
- Prompt tokens: 191,730
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 182,770
- Completion tokens: 9,621
- Reasoning tokens reported: 0
- Total tokens: 201,351
- Estimated total: $0.02830677

Full individual reviews and raw JSON responses are in `review_bundle.json`.
