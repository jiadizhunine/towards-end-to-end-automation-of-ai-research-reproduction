# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B004.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.022700**

## Final Meta-review

This paper introduces InfoDet, a large-scale dataset for infographic element detection containing 101,264 infographics (11,264 real and 90,000 synthetic) with over 14 million bounding box annotations covering texts, charts, human-recognizable objects (HROs), and 26 finer-grained chart sub-element categories. The dataset is constructed using a combination of programmatic annotation for synthetic infographics and a model-in-the-loop approach with expert refinement for real infographics, achieving annotation quality comparable to established datasets (93.9% precision, 96.7% recall). The paper demonstrates the dataset's utility through three applications: (1) a Thinking-with-Boxes scheme that improves VLM chart understanding via grounded chain-of-thought reasoning on ChartQAPro, (2) comprehensive evaluation of 11 object detection models showing that fine-tuning on InfoDet substantially outperforms zero/few-shot prompting of foundation models, and (3) transfer learning to graphic layout detection tasks (Rico, DocGenome, PosterLayout) showing consistent improvements from InfoDet pre-training. The dataset and code are publicly released.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.400 | 0.490 | 3-4 |
| Significance | 3 | 3.400 | 0.490 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.400 | 0.490 | 3-4 |
| Contribution | 3 | 3.200 | 0.400 | 3-4 |
| Overall | 7 | 6.800 | 0.400 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The dataset fills a clear gap in the literature—existing infographic datasets are either very small (e.g., Borkin et al. with 393 samples) or focus only on plain charts without HROs. InfoDet's scale (101,264 infographics, 14M+ annotations) is impressive and addresses a real need.
- The construction methodology is thoughtful and well-documented, combining programmatic annotation for synthetic data with a model-in-the-loop refinement process for real data, achieving annotation quality metrics (93.9% precision, 96.7% recall) comparable to established datasets like COCO.
- The dataset includes rich annotations beyond basic boxes: 75 chart types, 26 mark-level sub-element categories, text annotations via OCR, and segmentation masks via SAM, enabling multiple downstream tasks.
- The three applications are well-designed and demonstrate broad utility: improved VLM chart understanding, comprehensive object detection model benchmarking, and successful transfer to graphic layout detection tasks.
- The evaluation is comprehensive, covering 11 object detection models across multiple adaptation strategies (zero-shot, few-shot, fine-tuning) with detailed analysis of failure patterns.
- The paper is honest about limitations, including remaining annotation errors, dataset scope constraints, and post-fine-tuning regression on natural images, and provides extensive supplementary materials.
- Good reproducibility practices: code, data, and a dataset card are publicly released, and ethical considerations (copyright, content filtering) are addressed.

### Weaknesses

- The improvements from the Thinking-with-Boxes scheme are relatively modest (e.g., +1.7 overall accuracy for o4-mini on ChartQAPro), and gains are primarily on infographic charts rather than plain charts, limiting the perceived impact of the proposed approach.
- The object detection evaluation, while comprehensive, largely confirms expected findings that fine-tuning on domain-specific data outperforms zero/few-shot prompting for specialized tasks. The paper could provide deeper analysis of why foundation models fail and what specific aspects of infographics cause the domain gap.
- The model-in-the-loop annotation process for real infographics may introduce systematic biases despite expert review; the inter-annotator agreement study is relatively small (1,000 images, 2 experts).
- The synthetic infographics, while covering 92.64% of real infographics in feature space, may not fully capture the diversity of real-world infographic design, particularly composite charts which are noted as unique to real data.
- The real infographic collection is limited to 10 platforms, which may introduce platform-specific and cultural/regional biases in infographic style and content.
- The paper lacks detailed analysis of failure cases for the Thinking-with-Boxes approach (e.g., which question types fail and why) and does not rigorously establish statistical significance for all comparisons.
- The cross-dataset evaluation for mark-level detection is limited to only 4 common categories between InfoDet and VG-DCU, which may not fully demonstrate generalization capability.
- The reliance on GPT-4o mini for content filtering and synthetic text generation raises potential concerns about systematic biases in the dataset, though the authors report bias analysis with no harmful bias found.

### Questions

- Could the authors provide a breakdown of Thinking-with-Boxes improvements by question type (e.g., numeric extraction, comparison, trend analysis, multi-hop reasoning)? Which question types still fail and why?
- What are the characteristics of the 7.36% of real infographics not covered by synthetic data in the UMAP analysis? Does this gap affect model performance on those cases?
- How sensitive is the model-in-the-loop annotation process to the initial model choice (InternImage-L with DINO)? Would a different initial model lead to different annotation biases?
- Could the authors provide error bars or confidence intervals for the ChartQAPro results in Table 1? The improvements seem modest and might not be statistically significant.
- How was the balance between the 75 chart types ensured in both real and synthetic data? Are any types significantly underrepresented?
- What is the specific contribution of the two-layer visual prompt separation versus the textual descriptions in the Thinking-with-Boxes scheme? Is one more critical than the other?
- Have the authors considered evaluating the dataset's utility for training VLMs directly (e.g., through fine-tuning or as part of a larger training mixture), rather than only as a prompting aid?
- How were the 1,072 synthetic templates selected from real infographics? Was there a diversity-based selection process to ensure broad coverage of design styles?
- Regarding the transfer learning results, the improvements on Rico are notably larger than on DocGenome. What specific aspects of InfoDet's annotations contribute most to this transferability?
- The paper mentions that in-context examples hurt performance. Is this consistent across all model versions (o1, o3, o4-mini), or model-specific?

### Limitations

- The dataset focuses exclusively on infographics containing charts and HROs, excluding other graphic design types without these elements, limiting its applicability as a sole training source for broader graphic design tasks.
- The model-in-the-loop annotation approach may introduce consistent errors in ambiguous cases, which could propagate through models trained on the dataset.
- Remaining annotation errors include imprecise bounding-box localization (36.5%), marks/annotations detected as HROs (32.9%), and missed tiny elements (20.4%).
- The synthetic infographics, while covering 92.64% of real infographics in feature space, may not capture the full diversity of real-world infographic design, particularly composite charts and hand-drawn styles.
- The real infographics are collected from only 10 online platforms, potentially introducing platform-specific and cultural/regional biases.
- The model after fine-tuning on InfoDet no longer predicts natural-image classes, limiting its applicability to unified detection scenarios.
- The paper does not deeply explore potential negative societal impacts beyond copyright and content filtering, such as potential misuse of improved infographic understanding for misinformation campaigns or automated content generation that could bypass human oversight.
- The computational cost of fine-tuning on InfoDet (up to 70 GPU hours per model) may be prohibitive for some researchers, though this is comparable to COCO.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 147,666
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 138,706
- Completion tokens: 11,628
- Reasoning tokens reported: 0
- Total tokens: 159,294
- Estimated total: $0.02269977

Full individual reviews and raw JSON responses are in `review_bundle.json`.
