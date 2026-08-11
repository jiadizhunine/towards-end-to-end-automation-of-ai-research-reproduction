# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B069.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.016463**

## Final Meta-review

The paper proposes CHROMA, a feed-forward transformer for multi-view appearance harmonization in 3D reconstruction. It predicts per-frame 3D bilateral grids of affine color transforms conditioned on a selected reference frame, along with uncertainty-aware confidence grids. A reference-frame selection heuristic combines DINOv2 semantic similarity with photometric exposure statistics. Training uses synthetic paired data from simulated camera ISP pipelines and a self-supervised loss based on a pretrained feed-forward 3D reconstruction model (AnySplat) to leverage unpaired real-world data. The method is designed to plug into existing 3DGS/2DGS/DashGS pipelines without per-scene appearance optimization, with experiments claimed across DL3DV, LOM, and BilaRF datasets.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.000 | 0.000 | 2-2 |
| Clarity | 2 | 2.000 | 0.000 | 2-2 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 2 | 2.000 | 0.000 | 2-2 |
| Presentation | 2 | 2.000 | 0.000 | 2-2 |
| Contribution | 2 | 2.400 | 0.490 | 2-3 |
| Overall | 4 | 4.000 | 0.000 | 4-4 |
| Confidence | 4 | 3.400 | 0.490 | 3-4 |

### Strengths

- Novel decoupling of appearance harmonization from per-scene optimization, yielding a generalizable feed-forward model that can be dropped into multiple 3DGS variants without retraining.
- Bilateral grids predicted by a multi-view transformer provide a compact and expressive representation for spatially-varying color transforms while enforcing cross-view consistency.
- Hybrid training combining synthetic paired ISP data with a self-supervised rendering loss from a 3D foundation model is a creative and practical solution to the lack of paired real-world appearance data.
- Automatic reference frame selection using DINOv2 semantics and photometric quality is a sensible heuristic that improves over arbitrary reference selection.
- Evaluation spans synthetic ISP, exposure variation, and real captured scenes, and integrates with several downstream reconstruction baselines.

### Weaknesses

- The manuscript contains no actual numerical results: Tables 1, 2, and 3 are referenced but their entries are placeholders, making all quantitative claims unverifiable.
- Several technical details are underspecified or erroneous: Eq. 3 uses LAB luminance thresholds incompatible with the 0-100 range, Eq. 6 describes a VGG loss on a difference image rather than a standard perceptual loss, and the confidence loss weight beta is not given.
- The self-supervised loss relies on a pretrained feed-forward 3D model whose pose and geometry predictions may be unreliable under severe appearance changes; no failure analysis or ablation of this dependence is provided.
- The model processes hundreds of frames via global attention, but no memory/complexity analysis or inference-time scaling is given to support the claim of fixed per-frame cost.
- Training is performed at 224x224 resolution, but evaluation is at full resolution; how bilateral grids are applied or upsampled to full resolution is not discussed, nor the impact on quality.
- The reference selection score uses hand-tuned weights and thresholds without sensitivity analysis, and the paper does not address what happens when all frames are poor references.
- Evaluation protocols may include global color correction that can mask appearance inaccuracies, and no comparison with the closely related BilaRF method is provided.

### Questions

- What are the actual PSNR/SSIM/LPIPS values in Tables 1-3, including standard deviations and number of runs?
- How are the predicted bilateral grids at 224x224 upsampled or applied to full-resolution images during inference, and what is the resulting per-frame overhead?
- In Eq. 3, what is the valid range of L? If CIE-LAB lightness (0-100), why are thresholds 250 and 5 used?
- How is the confidence grid parameterized to ensure positive values for the logarithmic loss term?
- What is the value of beta in Eq. 4, and what happens if confidence predictions collapse to low weights for hard pixels?
- How exactly does the self-supervised loss ensure multi-view consistency if rendering is only performed at the reference viewpoint, and how sensitive is training to AnySplat's failures on poorly exposed frames?
- How sensitive is the reference frame selection to the hyperparameters alpha and the 5%/95% thresholds, and is there any validation against human-selected references?
- What is the memory usage and runtime when processing 300+ frames in a single forward pass on the 80GB GPU, and how does the architecture scale beyond 24 frames?

### Limitations

- The most significant limitation is the absence of all quantitative results in the submitted manuscript, preventing any validation of the claimed improvements.
- The method only handles static scenes; transient objects, occlusions, and moving elements are not addressed.
- The reference-based harmonization ties the output appearance to a chosen frame; if no good reference exists, quality may degrade.
- The low resolution of the bilateral grids (28x28x8 at 224x224) may not capture high-frequency spatially-varying appearance changes at full resolution.
- Self-supervised training relies on a large pretrained 3D reconstruction model, which may introduce domain bias and computational overhead, and failed pose/geometry predictions are not analyzed.
- No code or data are provided, limiting reproducibility and independent verification.
- No discussion of negative societal impacts, though the technology appears benign.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 69,848
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 65,752
- Completion tokens: 25,881
- Reasoning tokens reported: 19,093
- Total tokens: 95,729
- Estimated total: $0.01646343

Full individual reviews and raw JSON responses are in `review_bundle.json`.
