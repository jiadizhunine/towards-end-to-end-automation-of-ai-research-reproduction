# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B093.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.017510**

## Final Meta-review

This paper introduces LangNav, a new dataset for language-guided multi-object navigation with fine-grained linguistic annotations (attributes like color/size/material and spatial relations like support/proximity/containment), built on synthetic HSSD scenes with ground-truth attributes and manual validation to avoid VLM hallucination errors found in prior datasets like GOAT-Bench. The paper also proposes LaMoN, a task extension where agents navigate to three sequential goals described at varying specificity levels, and MLFM (Multi-Layered Feature Map), a zero-shot navigation method that builds a layered top-down semantic map storing CLIP features, with three querying variants (vanilla, VLM-based, and relation-graph-based RGraph) and a two-phase exploration strategy (EAE-E). Experiments on LangNav show MLFM variants outperform 2D mapping baselines, with MLFM+RGraph achieving the best overall success rate (39.5%), and additional results on GOAT-Bench demonstrate generalization to real-world scans.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.200 | 0.400 | 3-4 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.200 | 0.400 | 3-4 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.000 | 0.632 | 5-7 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- LangNav addresses a real gap by providing fine-grained linguistic annotations for systematic evaluation of language understanding in navigation, with manual validation to mitigate VLM hallucination errors.
- The multi-layer map representation (MLFM) is a novel and practical middle-ground between 2D and 3D maps, preserving height information with linear memory cost and showing clear improvements over 2D baselines.
- The two-phase navigation strategy (EAE-E) is well-motivated and shows consistent improvements when adapted to existing baselines (VLFM-v2, OneMap-v2), demonstrating general applicability.
- Comprehensive experimental evaluation including ablations on feature types, detectors, map resolution, number of layers, and EAE percentage, plus detailed failure analysis.
- The dataset construction process is carefully documented, including analysis of GOAT-Bench errors and spatial relation extraction procedures.
- Validation on GOAT-Bench provides some evidence of generalizability to real-world scans.
- The writing is clear and well-organized, with honest discussion of limitations.

### Weaknesses

- Absolute success rates are low (best overall SR ~39.5%), raising questions about practical applicability of the approach.
- The EgoImageMap+VLM baseline achieves comparable performance to the best MLFM variant (35.1% vs 39.5% SR), suggesting the multi-layer map's advantage over a simpler egocentric image storage approach is limited.
- The dataset is limited to synthetic HSSD scenes with 35 scenes and 31 distinct object categories, which may limit generalizability and statistical power of per-attribute analyses.
- No comparison with learned (non-zero-shot) navigation methods, limiting the assessment of where the approach stands in the broader landscape.
- Statistical significance of performance differences is not established beyond reporting standard deviations; no significance tests are provided.
- The paper claims 'open-vocabulary' but the evaluation relies on a closed set of object categories and attributes from HSSD.
- The manual validation process is not described in sufficient detail (e.g., number of annotators, inter-annotator agreement).
- MLFM completely fails on the texture attribute (0% SR), indicating a fundamental limitation of the feature extractor that is acknowledged but not fully addressed.

### Questions

- Could you provide more details on the manual validation process? How many annotators were involved, and what was the inter-annotator agreement rate? Were all descriptions manually checked?
- Given that EgoImageMap+VLM achieves comparable performance to MLFM+RGraph, what specific advantages does the multi-layer map provide over storing raw egocentric images? What are the failure modes of MLFM that EgoImageMap+VLM handles better?
- Have you considered comparing with learning-based navigation methods or more recent zero-shot approaches beyond the cited baselines?
- Could you provide statistical significance tests (e.g., paired t-tests) for the key comparisons in Table 2 to confirm the improvements are meaningful?
- How sensitive is MLFM to the threshold for accepting a candidate cell in MLFM-vanilla and to the graph construction thresholds in RGraph? Are there ablations on these hyperparameters?
- Can you provide a breakdown of performance by goal specificity level (e.g., category-only vs. full attribute descriptions)?
- How does the EAE-E adaptation work for VLFM and OneMap? Could you provide more implementation details to ensure fair comparison?
- How is the 'found' action verified during the exploitation phase to avoid false positives from the detector?
- How does the dataset's limited object vocabulary (31 categories) affect the open-vocabulary claims? Would more diverse categories change the results?
- What is the computational cost of MLFM compared to baselines, particularly the VLM variants that rely on GPT-4 API calls?

### Limitations

- The dataset is restricted to synthetic HSSD scenes, which may not fully capture real-world complexity and visual diversity; the GOAT-Bench experiment only partially addresses this.
- Language descriptions lack complex linguistic structures such as coreference, negation, and action directives, as acknowledged by the authors.
- The method relies on multiple pretrained models (CLIP, YOLO-World, GPT-4), making deployment computationally expensive and potentially fragile to model failures.
- Fixed thresholds for spatial relations (e.g., 'near' defined as 0.2-1.0m) may not generalize across object scales or scene types.
- The paper does not discuss potential negative societal impacts, though the use of synthetic scenes and indoor navigation raises minimal direct concerns; however, reliance on large pretrained models could have environmental costs.
- The evaluation focuses on success rate and SPL but does not separately measure language understanding from navigation challenges, which could conflate perceptual and navigational failures.
- The texture attribute is completely unhandled by the method, indicating a limitation of the feature extractors used.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 114,861
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 105,901
- Completion tokens: 9,494
- Reasoning tokens reported: 0
- Total tokens: 124,355
- Estimated total: $0.01750955

Full individual reviews and raw JSON responses are in `review_bundle.json`.
