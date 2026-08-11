# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B004.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.021777**

## Final Meta-review

The paper introduces InfoDet, a large-scale dataset for detecting charts and human-recognizable objects (HROs) in infographics, containing 11,264 real and 90,000 synthetic infographics with over 14 million bounding-box annotations. Annotations are generated via programmatic parsing for synthetic data and a model-in-the-loop with expert refinement for real data. The paper demonstrates three applications: a Thinking-with-Boxes grounded chain-of-thought prompting scheme that improves VLM performance on ChartQAPro, an evaluation of 11 object detection models on InfoDet, and transfer learning to document layout and UI detection (Rico, DocGenome).

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 3 | 2.600 | 0.490 | 2-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 2.600 | 0.490 | 2-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 5.800 | 1.166 | 4-7 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- InfoDet fills a clear gap in infographic element detection, providing a large-scale resource (101,264 infographics, 14M+ boxes) that combines real and synthetic data for diversity and scale.
- The model-in-the-loop annotation pipeline is practical and reduces human effort while achieving reported precision/recall (93.9%/96.7%) comparable to established detection datasets.
- The Thinking-with-Boxes scheme consistently improves ChartQAPro performance over strong baselines across several state-of-the-art VLMs, demonstrating a useful application for chart understanding.
- The benchmark of 11 object detection models reveals that zero-/few-shot prompting is insufficient for infographics and that fine-tuning on InfoDet yields strong gains, providing a valuable reference.
- Transfer learning to document layout and UI detection (Rico, DocGenome) suggests InfoDet is a useful pretraining resource beyond infographics.
- The paper includes analyses of diversity, bias, synthetic fidelity, and ethical considerations, increasing the credibility of the resource.

### Weaknesses

- The annotation quality of real infographics is only evaluated on a small sample (1,250 images) without inter-annotator agreement, detailed protocol, or per-category breakdown, leaving uncertainty about annotation consistency and quality.
- Fine-grained chart-type (75 types) and mark-level (26 categories) annotations are only available for synthetic infographics; real infographics lack these due to model limitations, reducing the dataset's utility for fine-grained real-world detection.
- The Thinking-with-Boxes gains are modest (e.g., o4-mini overall from 63.2 to 64.9) and only evaluated on ChartQAPro; no comparison with other visual grounding methods (e.g., Set-of-Marks) or other chart QA benchmarks is provided, and the impact of detection/OCR errors is not isolated.
- VLM experiments rely solely on proprietary models (o1, o3, o4-mini); no open-source VLM is tested, and no statistical significance tests are reported.
- The object detection benchmark is not fully systematic: foundation models are often tested zero-shot with only two class names, few-shot prompting is only tested on a subset, and fine-tuning is limited by GPU memory, making comparisons less comprehensive than claimed.
- Text annotations are obtained via PP-OCRv4 without reported accuracy on infographic text, which could affect both dataset quality and the grounded CoT prompts.
- Presentation issues include incomplete tables, broken internal references, and inconsistencies (e.g., 67 vs. 75 chart types, unclear definitions of metrics and class names).
- Dataset release links are redacted in the anonymized version, and real images are only available via source URLs, which may affect reproducibility if links change or content is removed.

### Questions

- How were the 1,250 evaluation samples selected, what IoU threshold was used for precision/recall, and what was the inter-annotator agreement among experts?
- Are fine-grained chart-type and mark-level annotations available for real infographics, or only for synthetic? If only synthetic, how does this affect the claimed comprehensiveness of the dataset?
- What is the accuracy of PP-OCRv4 text annotations on infographics, and how does OCR noise affect the grounded CoT prompt results?
- What is the performance of Thinking-with-Boxes when using ground-truth boxes instead of predicted boxes, and what is the individual contribution of text vs. boxes?
- How does Thinking-with-Boxes compare with other visual prompting methods (e.g., Set-of-Marks) and on other chart QA benchmarks (ChartQA, PlotQA, InfographicVQA)?
- Why does the diversity analysis report 67 chart types while the annotation taxonomy lists 75, and are all 75 present?
- Were the modifications to the relaxed accuracy metric consistently applied to all baselines, and could they affect comparability with official ChartQAPro results?
- How many expert annotators were involved in the model-in-the-loop refinement, how many rounds were performed, and was the final detector retrained on corrected real labels?
- Would more descriptive prompts (e.g., listing specific chart types) improve zero-shot detection performance of foundation models?
- Are the dataset and code publicly available, and what are the exact licenses for both real and synthetic infographics?

### Limitations

- Real infographics are collected from only 10 online platforms, which may introduce domain bias and limit diversity of styles and topics.
- Synthetic infographics are derived from 1,072 templates, potentially limiting coverage of novel or composite chart designs; 92.64% CLIP coverage leaves a non-trivial fraction of real infographics unrepresented.
- The model-in-the-loop annotation pipeline may propagate errors from the initial synthetic-trained model into real annotations, and systematic bias is not thoroughly measured.
- Fine-grained annotations are absent for real infographics, restricting the scope of fine-grained detection evaluation.
- Text annotations from OCR may contain errors, especially on stylized or overlapping text.
- The chart understanding experiments are limited to ChartQAPro and proprietary VLMs, so generalization to open-source models and other benchmarks is unclear.
- Releasing only source URLs rather than images may lead to broken links or non-reproducible downloads.
- The paper does not provide a standardized benchmark protocol for InfoDet, making comparisons across future methods less consistent.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 109,533
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 105,437
- Completion tokens: 25,015
- Reasoning tokens reported: 18,219
- Total tokens: 134,548
- Estimated total: $0.02177685

Full individual reviews and raw JSON responses are in `review_bundle.json`.
