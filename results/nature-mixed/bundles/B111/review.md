# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B111.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **5/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 2, 'Reject': 3}
- Estimated API cost: **$0.020258**

## Final Meta-review

This paper presents the first systematic investigation of adversarial attacks on graph-aware Large Language Models (LLMs), focusing on two representative projector-based models: LLaGA (node sequence template + linear projector) and GraphPrompter (GNN encoder + linear projector). The authors propose a taxonomy of graph encoding methods (textual description vs. learned projector), adapt existing GNN attacks (Nettack, MetaAttack) for poisoning and evasion scenarios, discover a new attack surface in LLaGA's node sequence template via malicious node injection, demonstrate that imperceptible feature perturbations (homoglyphs, reorderings) are highly effective, and propose a unified attack combining structural and feature perturbations. They also introduce GaLGuard, an end-to-end defense combining an LLM-based feature corrector with adapted GNN structural defenses (graph purification and GNNGuard). Experiments on Cora, Citeseer, PubMed, and ArXiv reveal that graph-aware LLMs are more vulnerable to evasion than poisoning attacks, and that LLaGA is more susceptible than GraphPrompter due to its node sequence template.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 2 | 2.400 | 0.490 | 2-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 3 | 2.800 | 0.400 | 2-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 2.800 | 0.400 | 2-3 |
| Overall | 5 | 5.200 | 0.748 | 4-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Timely and important research question: adversarial robustness of graph-aware LLMs is largely unexplored.
- Useful taxonomy of graph encoding methods (textual vs. learned projector) provides a clear framework for analysis.
- Discovery of a novel attack surface in LLaGA's node sequence template (malicious node/placeholder injection) is a genuine and interesting contribution.
- Finding that feature perturbation attacks (homoglyphs, reorderings) are more effective than structural attacks on graph-aware LLMs is a counter-intuitive and significant insight compared to traditional GNNs.
- Comprehensive evaluation across multiple datasets (Cora, Citeseer, PubMed, ArXiv) and attack types (poisoning, evasion, structural, feature, unified).
- Proposed defense (GaLGuard) is a thoughtful first attempt at addressing both structural and feature-level vulnerabilities in an integrated manner.
- Ablation studies (perturbation levels, base LLM choice) add depth to the analysis.

### Weaknesses

- Critical gap: GaLGuard is only evaluated against MetaAttack, not against the paper's own more effective attacks (feature perturbations, unified attack, node injection). This leaves the defense's effectiveness against the most severe threats unvalidated, undermining the paper's central claim of providing a robust defense.
- Limited model coverage: only two graph-aware LLM architectures (LLaGA and GraphPrompter) are evaluated, limiting generalizability of findings to the broader landscape of graph-aware LLMs.
- No comparison with existing defense baselines (e.g., text sanitization, adversarial training, or standard GNN defenses applied directly), making it difficult to assess GaLGuard's relative merit.
- Threat model details are unclear: for black-box attacks using Nettack and MetaAttack, the surrogate model selection and transferability validation are not adequately described.
- The defense relies on GPT-4 Turbo, which is proprietary, expensive, and computationally intensive; its practical feasibility for large graphs is not discussed.
- Some analysis is superficial (e.g., why LLaGA is more vulnerable than GraphPrompter), lacking formal or empirical verification of proposed mechanisms.
- The node sequence template injection attack may be an artifact of LLaGA's specific implementation (placeholder mechanism) and could potentially be mitigated by simple design changes, raising questions about its fundamental significance.
- The unified attack is mentioned but not detailed in the main text (no dedicated results table), making it hard to verify claims about its effectiveness.
- Feature perturbation attacks are borrowed from NLP without deep adaptation to the graph context; their task-specificity and robustness to preprocessing (e.g., OCR) are not explored.
- The paper's writing has occasional grammatical errors and typos, and some experimental details (hyperparameters, computational costs) are missing.

### Questions

- Why is GaLGuard only evaluated against MetaAttack? How does it perform against the feature perturbation attacks (homoglyph, reordering), the node injection attack, and the unified attack? This is crucial for validating the defense's core purpose.
- How is the surrogate model for Nettack and MetaAttack chosen, and how is the transferability of these black-box attacks validated? Please provide details on the surrogate architecture and any validation experiments.
- How does GaLGuard compare to simpler baselines, such as using only the LLM feature corrector (without GNN structural defenses) or only the structural defenses (without the LLM corrector)? This would help isolate each component's contribution.
- What is the computational overhead of GaLGuard, particularly the GPT-4 Turbo-based feature corrector? Is this feasible for large graphs like ArXiv in real-world deployment?
- Could the node sequence template injection attack be mitigated by simple design changes (e.g., randomizing placeholder positions, using special tokens, or downweighting placeholder contributions via attention)? If so, how significant is this attack surface?
- How sensitive are the feature perturbation attacks to the choice of translation objective and language? Would task-specific perturbations (targeting classification labels) be more effective?
- How would the findings generalize to other graph-aware LLM architectures (e.g., textual description methods, graph transformers, or different projector designs)? Would textual description methods be more robust overall?
- What are the specific reasons that poisoning attacks are less effective than evasion attacks? Is this due to projector retraining dynamics adapting to perturbations? Would a more sophisticated poisoning attack that anticipates retraining be more effective?
- How does the performance of GaLGuard compare to simply using a robust GNN (e.g., GNNGuard) without the LLM component? This would isolate the contribution of the LLM-based feature corrector.
- In the unified attack, how are budgets split between structural and feature perturbations? Is there an optimal trade-off?
- Would fine-tuning the LLM (rather than using a frozen model) change the vulnerability profile significantly?

### Limitations

- The defense evaluation is incomplete, as it does not cover the most effective attack types (feature perturbations and unified attacks), which are the paper's own proposed threats.
- The study is limited to two model architectures and citation network datasets, limiting generalizability to other graph domains (e.g., social networks, knowledge graphs) and graph-aware LLM designs.
- The computational cost and practical feasibility of the defense (particularly GPT-4 Turbo calls) are not addressed, raising concerns about reproducibility and accessibility.
- The threat model assumes complete access to training/inference data, which may be unrealistic in some black-box LLM API deployment scenarios.
- The paper does not thoroughly discuss potential negative societal impacts, such as the dual-use nature of the demonstrated attacks in sensitive applications (e.g., healthcare, finance) or responsible disclosure considerations.
- The potential detectability of the proposed node injection attacks via simple graph statistics is not discussed.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 133,944
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 124,984
- Completion tokens: 9,767
- Reasoning tokens reported: 0
- Total tokens: 143,711
- Estimated total: $0.02025761

Full individual reviews and raw JSON responses are in `review_bundle.json`.
