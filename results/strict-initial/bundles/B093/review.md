# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B093.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 3, 'Reject': 2}
- Estimated API cost: **$0.019457**

## Final Meta-review

The paper introduces LangNav, a synthetic HSSD-based dataset for language-guided multi-object navigation with manually validated natural-language goal descriptions and fine-grained linguistic tags (attributes and spatial relations). It defines the LaMoN task, an extension of MultiON with three language-specified goals at varying specificity. The authors propose MLFM, a zero-shot multi-layer semantic feature map with three query variants (vanilla, VLM, RGraph) and a two-phase explore-and-exploit navigation strategy. On LangNav and GOAT-Bench, MLFM variants outperform several zero-shot mapping baselines, with MLFM+RGraph achieving the highest success rate.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 2.800 | 0.400 | 2-3 |
| Quality | 2 | 2.600 | 0.490 | 2-3 |
| Clarity | 2 | 2.600 | 0.490 | 2-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 2 | 2.800 | 0.400 | 2-3 |
| Presentation | 2 | 2.600 | 0.490 | 2-3 |
| Contribution | 3 | 2.800 | 0.400 | 2-3 |
| Overall | 4 | 5.200 | 0.980 | 4-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- LangNav addresses a real gap by providing manually validated, open-vocabulary language descriptions with fine-grained attribute and spatial-relation annotations, enabling systematic evaluation of language understanding in navigation.
- LaMoN is a natural extension of MultiON to sequential, language-specified goals with varying specificity and multiple correct matches.
- The multi-layer feature map is a practical middle ground between 2D and 3D representations, and ablations show it improves attribute and relation grounding over 2D baselines.
- The paper includes extensive ablations (feature types, detectors, map resolution, EAE split) and failure analyses, giving insight into component contributions.
- MLFM is zero-shot and modular; it generalizes to GOAT-Bench, suggesting some cross-dataset utility.

### Weaknesses

- Dataset statistics are inconsistent: the main text reports 855 test episodes and 2565 goal descriptions, while Table 5 reports 875 and 2625; the paper also inconsistently cites GPT-4 vs GPT-5, harming reproducibility.
- Reported gains are often within the stated ±2.5 standard deviation (e.g., MLFM+RGraph 39.5 vs EgoImageMap+VLM 35.1 SR) and no statistical significance tests or confidence intervals are provided, so the main superiority claim is unsupported.
- The evaluation conflates language grounding with navigation and detection; success is defined by reaching a target, and per-attribute SR does not isolate language errors from exploration or perception errors.
- LangNav is entirely synthetic, with only 35 HSSD scenes and 31 object categories; descriptions are generated from ground-truth attributes rather than human speakers, limiting ecological validity and open-vocabulary scope.
- MLFM is an integration of existing components (CLIP/SED, YOLO-World, GPT-4/5, A*) with incremental novelty; the multi-layer map is essentially a coarse 3D grid, and no trained end-to-end or recent 3D scene-graph baselines are compared.
- Certain attribute categories (e.g., texture) achieve 0% success across all MLFM variants, and per-category metrics lack sample sizes/confidence intervals, making some comparisons statistically fragile.

### Questions

- How do the authors reconcile the discrepancies in test split size and LLM version (GPT-4 vs GPT-5) across the paper and appendix?
- Are the differences between MLFM+RGraph and EgoImageMap+VLM statistically significant given the reported standard deviation? Please provide per-metric confidence intervals or paired tests.
- How does the evaluation separate language understanding from exploration and detection? Could the authors report grounding metrics or a diagnostic where targets are explicitly observed?
- What are the sample sizes per attribute/relation category, and why are some categories (e.g., texture) reported at 0% across methods?
- Why are no trained end-to-end navigation agents evaluated on LangNav? Such comparisons would test whether the benchmark is useful beyond zero-shot mapping baselines.
- How were the fine-grained linguistic tags validated beyond manual review? Is there inter-annotator agreement or a correction rate?

### Limitations

- The dataset is limited to synthetic HSSD scenes with 35 scenes and 31 object categories; language descriptions are auto-generated from ground-truth attributes and lack coreference, negation, and action directives.
- Spatial relation extraction uses bounding-box geometry and fixed proximity thresholds, which can mislabel relations for irregular objects or scene-dependent semantics.
- The method's success depends on CLIP and an open-vocabulary detector, which fail on texture and state attributes; the multi-layer map does not solve perception limitations.
- The absence of significance tests and the small per-category samples weaken the reliability of the reported comparisons.
- No analysis of computational efficiency or memory footprint of the multi-layer map is provided.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 103,257
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 99,161
- Completion tokens: 19,868
- Reasoning tokens reported: 12,823
- Total tokens: 123,125
- Estimated total: $0.01945705

Full individual reviews and raw JSON responses are in `review_bundle.json`.
