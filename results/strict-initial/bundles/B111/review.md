# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B111.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.023287**

## Final Meta-review

The paper investigates adversarial robustness of graph-aware LLMs, focusing on two projector-based models with frozen LLM backbones: LLaGA and GraphPrompter. It adapts GNN poisoning and evasion attacks (Nettack, MetaAttack), identifies a novel attack surface in LLaGA's node-sequence template through malicious node injection (NI, SI, MSI), evaluates imperceptible feature perturbation attacks (homoglyph and reordering), and introduces a unified structural+feature attack. The authors also propose an end-to-end defense, GaLGuard, which combines an LLM-based feature corrector with adapted GNN structural defenses, and evaluate it on several citation datasets.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.632 | 2-4 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 2 | 2.000 | 0.000 | 2-2 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 2 | 2.200 | 0.400 | 2-3 |
| Presentation | 2 | 2.000 | 0.000 | 2-2 |
| Contribution | 2 | 2.600 | 0.490 | 2-3 |
| Overall | 4 | 4.200 | 0.400 | 4-5 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- The paper addresses a timely and underexplored problem: adversarial robustness of graph-aware LLMs, and provides one of the first systematic evaluations.
- The proposed taxonomy of graph encoding methods (textual descriptions vs. learned projectors) helps structure the investigation.
- The discovery of a new attack surface in LLaGA's node-sequence template via malicious node injection is a concrete and original contribution.
- The paper demonstrates that feature-level perturbations can be highly effective against graph-aware LLMs, contrasting with typical GNN behavior.
- The proposed GaLGuard defense integrates feature correction and structural purification, showing some robustness gains under MetaAttack.
- The evaluation includes multiple datasets and ablations such as perturbation budget and LLM backbone choice.

### Weaknesses

- The defense GaLGuard is evaluated only against MetaAttack; there are no results for the node-injection attacks, feature perturbation attacks, or the unified attack, which the paper itself identifies as the most damaging threats.
- The unified attack results referenced in Section 8 as Table 5 are missing; no accuracy numbers for the combined structural+feature attack are actually reported, leaving a central claim unsubstantiated.
- The adaptation of Nettack and MetaAttack to graph-aware LLMs is underspecified: details about surrogate models, projector retraining, and the exact black-box assumption are unclear.
- The feature perturbation attack is optimized using an English-to-French translation objective rather than directly degrading node classification; no evidence shows that translation errors transfer to classification errors.
- The scope is narrow: only two projector-based architectures and mostly small citation datasets are studied, limiting generality to other graph-aware LLMs such as textual-description methods.
- Presentation issues recur: inconsistent table numbering, duplicated tables, typos, and missing experimental details hinder reproducibility.
- The defense relies on GPT-4 Turbo, a proprietary LLM, raising concerns about cost, reproducibility, determinism, and vulnerability to adaptive adversaries, none of which are adequately discussed.

### Questions

- What are the exact accuracy results for the unified attack? Why is the referenced Table 5 not included?
- How do the NI/SI/MSI injection attacks preserve unnoticeability constraints, and how does an attacker guarantee injected nodes appear as placeholders?
- How exactly are Nettack and MetaAttack adapted to LLaGA and GraphPrompter? Is a surrogate GCN used, and is the attacker aware of the projector architecture?
- Why is the feature attack optimized with a translation objective rather than a node classification loss? Was any human study performed to validate imperceptibility at a 10% budget?
- What are GaLGuard's performance results against homoglyph, reordering, the unified attack, and the node-injection attacks?
- What is the computational and monetary cost of the GPT-4 Turbo feature corrector? Could a smaller open-source model achieve similar robustness?
- Do the conclusions generalize to other graph-aware LLMs, especially those using textual graph descriptions instead of learned projectors?

### Limitations

- The study is limited to two learned-projector graph-aware LLMs with frozen backbones; findings may not extend to fine-tuned LLMs or textual-description-based methods.
- Only standard citation networks are used; real-world graphs with different properties may show different vulnerability patterns.
- The imperceptibility of homoglyph and reordering attacks is asserted but not validated through human evaluation or perceptual metrics.
- No adaptive attacks are considered against GaLGuard, so the robustness of the defense against a knowledgeable adversary is unknown.
- The defense uses a proprietary LLM, which may be unavailable, costly, non-deterministic, or susceptible to adversarial prompts.
- The paper does not discuss potential dual-use risks or negative societal impacts of releasing attack methods for graph-aware LLMs.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 123,622
- Cache-hit prompt tokens: 3,840
- Cache-miss prompt tokens: 119,782
- Completion tokens: 23,239
- Reasoning tokens reported: 16,798
- Total tokens: 146,861
- Estimated total: $0.02328715

Full individual reviews and raw JSON responses are in `review_bundle.json`.
