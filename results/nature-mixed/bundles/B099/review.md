# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B099.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.037669**

## Final Meta-review

The paper introduces ChartGalaxy, a million-scale dataset for infographic chart understanding and generation. The dataset comprises 1,701,356 synthetic and 61,833 real infographic charts, each paired with source data tables. The construction pipeline follows an inductive structuring process: real charts are collected from 18 chart-rich websites and search engines with license filtering; synthetic charts are programmatically generated using 75 chart types, 440 chart variations, and 68 layout templates extracted from real designs. The paper demonstrates three applications: (1) fine-tuning LVLMs (InternVL3-8B, Qwen2.5-VL-7B) on a constructed instruction dataset improves performance on public benchmarks (InfographicVQA, ChartQAPro) and a synthetic evaluation set; (2) a code generation benchmark evaluates 17 LVLMs on Direct Mimic (chart-to-D3.js code) with both high-level (GPT-4o judged) and low-level (SVG element matching) metrics; (3) an example-based infographic chart generation method outperforms GPT-Image-1 in a user study on fidelity, aesthetics, and creativity. The paper includes extensive ethical considerations including IP attorney review, URL-only release format, and IRB approval for the user study.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.800 | 0.400 | 3-4 |
| Quality | 3 | 3.200 | 0.400 | 3-4 |
| Clarity | 4 | 3.600 | 0.490 | 3-4 |
| Significance | 4 | 3.800 | 0.400 | 3-4 |
| Soundness | 3 | 3.200 | 0.400 | 3-4 |
| Presentation | 4 | 3.600 | 0.490 | 3-4 |
| Contribution | 4 | 3.800 | 0.400 | 3-4 |
| Overall | 7 | 7.000 | 0.632 | 6-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The dataset fills a clear gap in the field: existing chart datasets focus on plain charts, while infographic charts with rich visual-textual interplay are underrepresented. ChartGalaxy provides the first million-scale resource specifically for this domain (1.7M+ synthetic and 61K+ real charts).
- The construction pipeline is novel and well-documented: the inductive structuring process (75 chart types, 440 variations, 68 layout templates) grounded in real designs provides a systematic approach to synthetic generation. The human-in-the-loop verification for real chart table extraction is careful, with clear success rates reported.
- The paper demonstrates broad utility through three diverse applications: VQA fine-tuning shows consistent gains on public benchmarks and a custom evaluation set; a comprehensive code generation benchmark covers 17 models with multi-faceted metrics; and example-based generation shows superior results over GPT-Image-1 in a user study.
- The evaluation methodology is thorough, including ablations (real vs. synthetic data, pipeline components), comparisons against strong baselines, and human studies with proper IRB approval. The code generation benchmark includes a rigorous low-level SVG-based metric with human validation (92.33% agreement).
- The ethics statement is exemplary: IP attorney consultation, licensing review of all 18 sources, URL-only release format to avoid copyright issues, sensitive content filtering, and IRB approval for the user study.
- Extensive supplementary material (16+ pages of appendices) provides sufficient detail for reproduction, including chart type illustrations, layout templates, prompts, ablation studies, and extended analyses.

### Weaknesses

- The dataset is 96.5% synthetic (1.7M synthetic vs. 61K real). While DreamSim coverage analysis shows 97.62% feature-space overlap, this does not guarantee semantic equivalence. The large fine-tuning gains on the synthetic evaluation set (+24-27%) compared to public benchmarks (+3-6%) raise concerns about potential overfitting to the synthetic distribution.
- The independent evaluation set for understanding (2,176 charts, 4,975 QA pairs) is entirely synthetic, which limits the strength of claims about real-world understanding improvements. The authors acknowledge this choice but it weakens the evaluation.
- The code generation benchmark uses only 500 synthetic charts, which may not represent the difficulty distribution of real infographic charts with more complex layouts and imagery.
- The user study for example-based generation uses only 16 participants and 30 pairs, which is a relatively small sample. The comparison is limited to GPT-Image-1, a general-purpose generation model, rather than chart-specific baselines.
- The real infographic charts are released as URLs only, which may limit reproducibility if sources change or become unavailable.
- The synthetic data is English-only, and the real data sources skew toward North America and Europe, potentially introducing geographic/cultural biases.
- The paper does not deeply analyze potential systematic biases in the synthetic generation pipeline (e.g., template usage frequency, chart type distribution skew) or the remaining failure modes of models on the generated benchmarks.

### Questions

- The fine-tuning gains on the synthetic evaluation set are much larger than on public benchmarks. To what extent is this gap due to distribution matching (i.e., the evaluation set being from the same distribution as training data) versus genuinely improved reasoning capabilities? Have you evaluated on a held-out set of real infographic charts not from public benchmarks?
- What is the distribution of template usage across the 68 layouts? Are some templates over-represented, and could this bias models towards certain layouts? How does this compare to real infographic charts?
- For the code generation benchmark, how were the 500 synthetic charts sampled to ensure coverage of all chart types, variations, and layout templates? What is the distribution of chart types compared to the full dataset?
- In the user study, the comparison is with GPT-Image-1 only. Would a chart-specific baseline (e.g., ChartMimic-style approaches) narrow the fidelity gap? Were the 16 experts blinded to the method, and what was the inter-rater reliability?
- The real infographic charts are released as URLs only. How do you handle link rot or changes in source content? Is there a mechanism for users to access the charts reliably?
- For the VQA fine-tuning, did you compare against fine-tuning on existing chart datasets (e.g., ChartQA, ChartGemma) using the same models and hyperparameters? If not, this would be a valuable comparison to demonstrate the unique value of ChartGalaxy.
- What is the estimated error rate for the automatically extracted data tables from real charts (from the 86.6% that were auto-processed)? How does this error rate affect downstream tasks?
- The synthetic data generation relies heavily on Gemini-2.0-Flash for title generation and chart type selection. How sensitive are the results to this choice? Would a different LLM produce significantly different synthetic charts?
- For the example-based generation method, how does it handle cases where the reference chart's layout is incompatible with the new data? Are there fallback strategies?
- Could you provide more analysis on which chart types or layout templates are most/least effectively handled by the fine-tuned models, and which remain challenging?

### Limitations

- The dataset focuses on single-chart infographics, limiting coverage of multi-chart narratives common in real-world infographics.
- The synthetic data, despite its scale and diversity, may not fully capture the semantic complexity and nuance of real-world infographics (e.g., cultural references, domain-specific visual metaphors). The DreamSim coverage analysis does not measure semantic equivalence.
- The real infographic charts are released as URLs only, meaning the dataset is not self-contained. Users must access external sources, which may have availability or licensing issues, potentially hindering reproducibility.
- The instruction dataset (443K QA pairs) is generated using LLMs and template-based methods. While table extraction is human-verified, the QA pairs themselves may contain errors or biases; no human evaluation of QA quality is reported.
- The user study for generation has a small sample (16 participants, 30 pairs), limiting generalizability despite statistical significance.
- The synthetic data is English-only, and the real data sources are geographically skewed toward North America and Europe, potentially limiting cross-cultural generalization.
- Potential negative societal impact: The dataset could be used to generate misleading infographics (e.g., for disinformation campaigns). The paper filters sensitive content but does not discuss this dual-use risk explicitly. The fidelity improvements could make AI-generated infographics more convincing.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 248,408
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 239,448
- Completion tokens: 14,719
- Reasoning tokens reported: 0
- Total tokens: 263,127
- Estimated total: $0.03766913

Full individual reviews and raw JSON responses are in `review_bundle.json`.
