# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B045.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.022542**

## Final Meta-review

The paper introduces the Adversarial Déjà Vu hypothesis, which posits that novel jailbreaks are largely recombinations of a finite set of adversarial skill primitives from past attacks. To test this, the authors build a pipeline that extracts skills from 32 jailbreak papers using GPT-4.1, compresses them via sparse dictionary learning into a 397-atom Jailbreak Dictionary, and shows that unseen attacks can be explained as sparse compositions of these primitives with high LLM-judged explainability. Based on this, they propose Adversarial Skill Compositional Training (ASCoT), which generates training data by composing dictionary primitives. Experiments on LLaMA-3.1-8B and Zephyr-7B show improved robustness to unseen single- and multi-turn attacks compared to several adversarial training baselines while maintaining low over-refusal. The paper also analyzes the effects of skill coverage and composition depth, and includes an open-source replication with Qwen3.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 2.400 | 0.490 | 2-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 2.400 | 0.490 | 2-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 5.200 | 0.748 | 4-6 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- The Adversarial Déjà Vu hypothesis is a novel and compelling framing that shifts jailbreak robustness from attack-specific patching to compositional generalization over skills.
- The temporal cutoff study across 32 attack papers is a large-scale and principled way to test generalization to unseen attacks; the monotonic improvement in explainability supports the core hypothesis.
- The dictionary learning pipeline is technically interesting and provides interpretable, human-readable primitive descriptions.
- ASCoT demonstrates strong empirical gains over several baselines (PAP, WildJailbreak, CAT, LAT) on two different base models, with low over-refusal and a favorable robustness/utility trade-off.
- The ablations on skill coverage ('Coverage Dividend') and composition depth offer actionable insights for designing training data, and the open-source replication with Qwen3 suggests the approach is not tied to a single proprietary model.

### Weaknesses

- The core evidence for the Adversarial Déjà Vu hypothesis relies heavily on LLM-based skill extraction, naming, and explainability scoring, with no human validation; using GPT-4.1 for both extraction and evaluation creates a risk of circularity that a second LLM judge only partially mitigates.
- The 'unseen' attack set is small (only six post-cutoff attacks), and temporal novelty is not guaranteed because pretrained LLMs may have encountered these publications during pretraining; contamination is not ruled out.
- Baseline comparisons may be unfair: reimplementations (CAT*, LAT*) are underspecified and show extremely high over-refusal rates (e.g., 0.98 on XSTest), suggesting they are not operating in a comparable utility regime.
- ASCoT's training data includes vanilla harmful queries, benign data, and refusal calibration alongside composed queries, but there is no ablation isolating the contribution of skill composition; the gains may partly stem from data diversity or generic refusal training.
- The sparse linear composition model in embedding space is asserted rather than validated; no comparison to non-compressed or random/skill-set baselines is provided, and 'sparse' activation of 5–7 atoms is only moderately sparse.
- Evaluation lacks error bars, multiple seeds, and statistical significance tests; on some attacks (e.g., Zephyr Implicit Reference and DarkCite) ASCoT is worse than CAT* or LAT*.
- The composition-depth analysis shows an apparent inconsistency: PAIR is said to contain ~9.7 skills, yet shallow training (k=1–2) works best against it, and the relation between training depth and attack complexity is unclear.

### Questions

- How do the authors rule out data contamination between GPT-4.1's pretraining and the post-cutoff attacks, and would the temporal results change if skill extraction were redone with an LLM whose training data stops before the earliest unseen attack?
- Were any human annotators used to validate the extracted skills, primitive names, or explainability scores? What is the inter-annotator agreement?
- What is the performance of a control model trained on the same total data size but with random/non-compositional prompt mutations (or only vanilla harmful queries) plus the same benign and refusal-calibration data?
- How does dictionary explainability compare to a non-compressed baseline using all raw seen skills or a nearest-neighbor search, and to a random dictionary of the same size?
- What are the exact variances and statistical significance of the improvements over baselines across attack families and random seeds?
- How was the coverage-dividend experiment designed to keep data size fixed while increasing dictionary size, and are the numbers of unique primitive combinations and composition structures identical across settings?
- For the multi-turn GALA improvement, which skill primitives are active, and why does single-turn compositional training transfer successfully to a dialogue-based attack?
- How sensitive are ASCoT results to the choice of dictionary size (397) and the composition model (DeepSeek-V3)? Were other LLMs tried?
- Can the full pipeline be reproduced using only open-weight models, and how much do the proprietary components (GPT-4.1, DeepSeek-V3) affect the conclusions?

### Limitations

- No human validation of extracted skills or explainability scores; all judgments come from LLMs, introducing potential bias and circularity.
- The study is scoped to single-turn, language-based jailbreaks; the multi-turn claim is supported by only one attack (GALA) and is therefore preliminary.
- The sparse linear composition assumption in embedding space is a pragmatic heuristic without formal or empirical validation of its fidelity.
- Potential temporal contamination from using GPT-4.1, which may have memorized future attacks, and the 'unseen' attack set is small and may not be truly novel.
- ASCoT may be conflating compositional training with generic refusal training on diverse harmful data; the specific advantage of composition over data diversity is not isolated.
- The evaluation does not include adaptive attacks specifically designed to evade ASCoT, limiting claims about worst-case robustness.
- Experiments are limited to 7B/8B models; transferability to larger or closed-weight models is not demonstrated.
- The paper does not release the extracted dataset, dictionary, or full training code, which limits reproducibility and verification.
- Publishing a 'Jailbreak Dictionary' and composition methodology has potential dual-use risks, although the authors state responsible disclosure and local experimentation.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 104,470
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 100,374
- Completion tokens: 30,279
- Reasoning tokens reported: 22,698
- Total tokens: 134,749
- Estimated total: $0.02254195

Full individual reviews and raw JSON responses are in `review_bundle.json`.
