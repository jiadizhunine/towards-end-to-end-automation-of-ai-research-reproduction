# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B101.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.011884**

## Final Meta-review

StyleAR is the first framework to enable style-aligned text-to-image generation in multimodal autoregressive (AR) models. To overcome the scarcity of text-image-to-image triplet training data, the authors propose a data curation strategy that generates stylized images with a diffusion model (InstantStyle) and uses only the prompt and stylized image as binary training data. A frozen CLIP image encoder with a trainable perceiver resampler converts input reference images into style tokens, and a style-enhanced token technique (SAM-based feature subtraction plus Gaussian noise injection) is introduced to prevent content leakage. The method also employs a 1:3 stylized-to-raw data mixing ratio and DPO post-training. Experiments against five diffusion-based baselines (InstantStyle, IP-Adapter, StyleAligned, StyleCrafter, StyleShot) show competitive performance on CLIP-T, CLIP-I, and DINO metrics, with qualitative results, ablations, and a user study.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 3 | 2.800 | 0.400 | 2-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 2.800 | 0.400 | 2-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 5.800 | 0.400 | 5-6 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Addresses an important and underexplored problem: style-aligned generation with AR models, which has been dominated by diffusion-based approaches.
- Novel and practical data curation strategy: converting triplet data into binary data avoids the upper-bound limitation of using diffusion-generated triplets as ground truth and simplifies data collection.
- Well-designed style-enhanced token technique using SAM and Gaussian noise injection to mitigate content leakage, supported by ablation studies.
- Comprehensive evaluation including quantitative metrics, qualitative comparisons, ablations, and a user study.
- Demonstrates additional capabilities of the base AR model, such as integrating depth-map-based structural control while preserving style and quality.
- Clear motivation and reasoning for design choices, with well-organized presentation.

### Weaknesses

- Limited evaluation scope: only 10 reference styles, 20 prompts, and 800 generated images, which is insufficient to demonstrate robust generalization across diverse styles and prompts.
- Quantitative results are not top-ranked on any single metric (second on CLIP-T, CLIP-I, and DINO); the claim of state-of-the-art performance is not fully supported and lacks statistical significance tests.
- The explanation that IP-Adapter's high style metrics are due to content leakage is plausible but not rigorously quantified or validated with controlled experiments.
- The method still depends on a diffusion model (InstantStyle) for generating stylized training data, partially contradicting the motivation of avoiding diffusion model limitations.
- Insufficient details on DPO post-training: the choice of VLM for preference scoring, number of preference pairs, and training hyperparameters are not reported.
- No comparison with other AR-based personalization methods or a direct ablation against triplet-data training for AR models.
- No computational cost analysis (training time, inference speed, GPU memory) compared to diffusion baselines.
- Limited discussion of societal impacts, especially the potential for style mimicry of copyrighted artwork or misleading content creation.
- Some technical details are sparse (e.g., perceiver resampler architecture and initialization, hyperparameter sensitivity for alpha and gamma).

### Questions

- How do you justify the claim of state-of-the-art performance when the method ranks second on all three quantitative metrics? Could you provide confidence intervals or statistical significance tests?
- How does StyleAR compare against training an AR model with triplet data (e.g., using InstantStyle to generate triplet data)? This would directly validate the benefit of binary data over triplet data.
- What VLM was used for DPO preference scoring, how many preference pairs were collected, and what were the DPO training hyperparameters (steps, learning rate)?
- How sensitive is the method to the number of style tokens (M=16), the residual ratio alpha, and the Gaussian noise strength gamma? Have you conducted a sensitivity analysis?
- What is the rationale for the 1:3 stylized-to-raw data ratio? Is it optimal across datasets of different sizes?
- How does the method generalize to styles not present in the 80 training styles (e.g., 3D render, pixel art, watercolor)? Have you tested on a broader style set or standard benchmarks?
- Could you provide a quantitative measure of content leakage (e.g., semantic similarity between generated and reference image content) to support the claim about IP-Adapter?
- What is the computational cost (training time, inference speed, GPU memory) of StyleAR compared to the diffusion baselines?
- Can the style-enhanced token technique be applied to other AR models (e.g., Chameleon, Emu3), or is it specific to Lumina-mGPT?
- How was the diversity of the 200 prompts per style ensured in the data curation process?

### Limitations

- The evaluation is limited to 10 styles and 20 prompts, which may not capture the full diversity of real-world style-aligned generation scenarios.
- The method relies on a diffusion model for generating stylized training data, which introduces a ceiling on data quality and potential biases from the diffusion model.
- The current implementation requires depth map extraction for content control rather than directly accepting a content image, limiting flexibility for pure style transfer tasks.
- The paper does not discuss computational cost, which is relevant for practical deployment.
- Potential negative societal impact: the method could be misused to generate images in the style of living artists without consent, raising copyright and ethical concerns. This is not adequately discussed.
- The evaluation is limited to English prompts and Western-centric styles, potentially limiting generalizability to other cultural contexts.

### Ethics

Ethical concerns flagged: **True**

## Usage and Cost

- Requests: 6
- Prompt tokens: 70,114
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 61,154
- Completion tokens: 11,776
- Reasoning tokens reported: 0
- Total tokens: 81,890
- Estimated total: $0.01188393

Full individual reviews and raw JSON responses are in `review_bundle.json`.
