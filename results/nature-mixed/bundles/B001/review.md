# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B001.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.017436**

## Final Meta-review

This paper presents Durian, a diffusion-based framework for portrait animation with cross-identity attribute transfer from one or more reference images. The key innovation is a self-reconstruction training strategy that uses two frames from the same video as pseudo attribute/identity pairs, avoiding the need for expensive paired attribute data. The Dual ReferenceNet architecture processes attribute and identity references separately, fusing features via spatial attention in a diffusion model. Complementary masking ensures role separation, while mask expansion and augmentation strategies bridge the self-reconstruction to cross-identity gap. The method supports multiple facial attributes (hair, glasses, beard, hat) and exhibits emergent capabilities for multi-attribute composition and attribute interpolation. Extensive experiments show state-of-the-art performance compared to 12 two-stage baseline combinations.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.800 | 0.400 | 3-4 |
| Quality | 3 | 3.200 | 0.400 | 3-4 |
| Clarity | 3 | 3.400 | 0.490 | 3-4 |
| Significance | 4 | 3.600 | 0.490 | 3-4 |
| Soundness | 3 | 3.200 | 0.400 | 3-4 |
| Presentation | 3 | 3.400 | 0.490 | 3-4 |
| Contribution | 4 | 3.600 | 0.490 | 3-4 |
| Overall | 7 | 7.000 | 0.894 | 6-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel task formulation: first to jointly perform portrait animation with cross-identity attribute transfer, addressing a practical need for virtual styling applications.
- Clever self-reconstruction training strategy that avoids the need for paired attribute data, making the approach scalable to in-the-wild videos.
- Dual ReferenceNet architecture with complementary masking effectively disentangles identity and attribute information.
- Comprehensive evaluation: 12 baseline combinations, self- and cross-attribute transfer settings, ablations, user study, and qualitative comparisons.
- Emergent capabilities for multi-attribute composition and attribute interpolation without additional training are impressive and practically valuable.
- Honest analysis of failure cases and limitations, demonstrating a balanced assessment of the method's capabilities.
- Clear writing with well-organized structure and sufficient implementation details for reproducibility.

### Weaknesses

- The 'full ref. image input' ablation performs better on quantitative self-attribute transfer metrics, which could be confusing and weakens the ablation story despite the authors' explanation of content copying shortcuts.
- Cross-attribute transfer evaluation lacks ground truth and relies on proxy metrics (CLIP-I, DINO, ID-Sim) that may not fully capture perceptual quality; the user study is limited in scope.
- Heavy reliance on multiple external components (Sapiens, SDXL, FLUX, LivePortrait, FaceAligner) adds complexity and potential error accumulation, with limited analysis of failure modes for these components.
- Only four attribute categories are supported (hair, beard, glasses, hat), and generalization to other attributes (e.g., makeup, earrings) is not demonstrated.
- Training data is relatively small (2,747 videos) and dominated by CelebV-Text; generalization to other domains or low-quality videos is unclear.
- The mask expansion strategy depends on SDXL-generated images, which could introduce distribution bias or artifacts into training.

### Questions

- How sensitive is the method to the quality of the SDXL-generated mask expansion images? What happens if SDXL produces poor or unrealistic attribute variations?
- How robust is the Face Aligner for extreme poses, occlusions, or non-frontal faces? Are there failure cases where alignment degrades performance?
- For multi-attribute transfer, how does the model handle conflicting attributes (e.g., a hat overlapping with hair)? Does the model learn to prioritize one attribute over another?
- What is the minimum video length or quality threshold for effective self-reconstruction training?
- How does the model perform on attributes not in the training set (e.g., earrings, facial piercings)? Does the self-reconstruction framework generalize to unseen attribute types?
- How is the interpolation ratio alpha related to the perceptual attribute change? Is the mapping linear?
- What is the computational cost of the full inference pipeline (including Face Aligner and mask estimation) compared to the baselines?
- How does the method handle cases where the attribute reference has a very different pose or viewpoint from the portrait, beyond what the face aligner can correct?

### Limitations

- The method is limited to four attribute categories (hair, beard, glasses, hat); generalization to other facial attributes is not demonstrated.
- Cross-identity transfer with significant lighting or appearance mismatch between attribute and portrait images can lead to suboptimal results (acknowledged in failure cases).
- The self-reconstruction training may not fully capture the diversity of cross-identity scenarios, despite augmentation strategies.
- The method requires segmentation masks at inference, which may limit practical applicability in some scenarios.
- Potential negative societal impact: the technology could be misused for creating misleading or deceptive videos (deepfakes) with manipulated facial attributes. The paper does not discuss this risk or potential safeguards.
- The Face Aligner and mask expansion components add complexity that may limit practical deployment in resource-constrained settings.
- No discussion of computational cost or memory requirements for training or inference.

### Ethics

Ethical concerns flagged: **True**

## Usage and Cost

- Requests: 6
- Prompt tokens: 105,764
- Cache-hit prompt tokens: 0
- Cache-miss prompt tokens: 105,764
- Completion tokens: 9,389
- Reasoning tokens reported: 0
- Total tokens: 115,153
- Estimated total: $0.01743588

Full individual reviews and raw JSON responses are in `review_bundle.json`.
