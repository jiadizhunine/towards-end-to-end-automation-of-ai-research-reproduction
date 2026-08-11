# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B099.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.026597**

## Final Meta-review

The paper introduces ChartGalaxy, a large-scale dataset of infographic charts consisting of 61,833 real charts and 1,701,356 programmatically generated synthetic charts, each paired with tabular data. The construction pipeline extracts 75 chart types, 440 chart variations, and 68 layout templates from real infographic designs via a human-in-the-loop approach, and uses them to synthesize diverse charts with D3.js. The dataset is evaluated in three applications: fine-tuning LVLMs for infographic chart VQA, benchmarking D3.js code generation across 17 LVLMs, and example-based infographic chart generation compared against GPT-Image-1 in a user study.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.200 | 0.400 | 3-4 |
| Contribution | 3 | 3.200 | 0.400 | 3-4 |
| Overall | 7 | 6.600 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Fills a clear gap in chart datasets by targeting infographic charts with rich text-image-layout structure, providing a large-scale resource of 61,833 real and 1,701,356 synthetic charts with aligned tabular data.
- The inductive pipeline that extracts chart types, variations, and layout templates from real infographics and synthesizes at scale is well-motivated and grounded in real designs, with detailed appendices supporting reproducibility.
- Demonstrates utility across three applications: fine-tuning on ChartGalaxy improves InternVL3 and Qwen2.5-VL on InfographicVQA and ChartQAPro; the code generation benchmark provides a broad comparison of 17 LVLMs with fine-grained metrics; and the example-based generation method outperforms GPT-Image-1 in an expert user study.
- The paper addresses ethics and reproducibility through careful source licensing, sensitive-content filtering, IRB approval for the user study, and release of chart URLs rather than images.
- The authors provide extensive documentation of chart types, variations, layout templates, prompts, ablations, and user study details.

### Weaknesses

- The independent VQA evaluation set is sampled from the same synthetic distribution as the training data, so the reported gains (e.g., +60.49 on style detection) may be inflated by distribution overlap; public benchmark gains are more modest, and no comparison is made with existing chart instruction datasets.
- Real chart table extraction relies on LVLM agreement with only a small manual verification subset (200 exact-match samples), leaving the error rate of the 61,833 real chart-table pairs uncertain.
- The code generation benchmark is limited to 500 synthetic charts generated from the same pipeline, so it may not represent arbitrary real-world infographics; the high-level score from GPT-4o is not validated against human raters, and the low-level SVG metric may miss semantic quality.
- The example-based generation method is essentially a template-filling approach, and the user study uses only 16 experts and 30 pairs with a single baseline (GPT-Image-1), which may not be optimized for data-accurate chart generation; this limits the strength of the comparative claim.
- Synthetic charts are limited to 68 layout templates and 440 variations, which may not capture the full long-tail diversity of real infographics; the paper does not provide human perceptual validation of realism beyond an automatic DreamSim coverage metric.
- Reproducibility is partly hindered in the manuscript by redacted prompts, algorithm pseudocode, and dataset URLs, and the closed-loop training of the detection model on synthetic charts may bias template discovery.
- The dataset is English-only, with geographic/domain skew toward North America and Europe, and it does not cover multi-chart infographic narratives.

### Questions

- How does fine-tuning on ChartGalaxy compare with fine-tuning on existing chart instruction datasets (e.g., ChartAssistant, ChartInstruct) of similar size when evaluated on InfographicVQA and ChartQAPro?
- What is the estimated error rate of the LVLM-based table extraction on real infographic charts, and how were the 13.4% manually corrected tables quality-checked?
- Why is the code generation benchmark limited to synthetic charts, and how would the 17 models perform on a real-chart subset with reconstructed code?
- How were the 30 reference charts and 16 experts selected in the user study, and would different prompts or additional baselines change the relative ranking?
- Were the 120,000 synthetic charts used to train the detection model also included in the final dataset or evaluation sets, and are there near-duplicates between training and evaluation data that could inflate results?
- How are the 68 layout templates distributed across the 1.7M synthetic charts, and does the popularity skew of certain templates reduce diversity?

### Limitations

- The dataset covers only single-chart infographics; multi-chart narratives and complex storytelling infographics are not addressed.
- Synthetic charts are generated from a finite set of templates and predefined variations, which may not capture the full creative diversity of human-designed infographics.
- Automatic table extraction from real charts may introduce undetected errors, affecting both the real and synthetic portions of the dataset.
- The dataset is predominantly English and geographically/domain-skewed toward North America/Europe, limiting global representativeness.
- The code generation benchmark targets D3.js and synthetic charts only, so findings may not generalize to other libraries or real-world chart images.
- Real charts are released as URLs that may become inaccessible over time.
- Potential negative societal impacts of generating infographics, such as misleading data presentation, are not discussed.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 150,540
- Cache-hit prompt tokens: 3,840
- Cache-miss prompt tokens: 146,700
- Completion tokens: 21,601
- Reasoning tokens reported: 15,037
- Total tokens: 172,141
- Estimated total: $0.02659703

Full individual reviews and raw JSON responses are in `review_bundle.json`.
