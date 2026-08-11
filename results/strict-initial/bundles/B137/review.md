# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B137.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 1, 'Reject': 4}
- Estimated API cost: **$0.027378**

## Final Meta-review

The paper proposes SurgiFlowVid, a diffusion-based video generation framework that aims to mitigate class imbalance in surgical video datasets. It extends SurV-Gen with a dual-prediction diffusion U-Net that jointly denoises RGB frames and optical flow during training, and a sparse visual encoder (adapted from SparseCtrl) that conditions generation on lightweight signals such as sparse segmentation masks or RGB frames. The framework is evaluated on three surgical datasets (SAR-RARP50, GraSP, AutoLaparo) across three downstream tasks (action recognition, tool presence detection, laparoscope motion prediction), reporting performance improvements from synthetic augmentation. The method also includes ablations on synthetic data attributes and an additional GynSurg dataset in the appendix.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 2 | 2.200 | 0.400 | 2-3 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 2 | 2.200 | 0.400 | 2-3 |
| Significance | 3 | 2.600 | 0.490 | 2-3 |
| Soundness | 2 | 2.200 | 0.400 | 2-3 |
| Presentation | 2 | 2.200 | 0.400 | 2-3 |
| Contribution | 2 | 2.200 | 0.400 | 2-3 |
| Overall | 4 | 4.400 | 0.800 | 4-6 |
| Confidence | 4 | 3.600 | 0.490 | 3-4 |

### Strengths

- Addresses an important practical problem: class imbalance in surgical video datasets, which limits the robustness of downstream models.
- The dual-prediction (RGB + optical flow) approach is a sensible inductive bias for improving temporal consistency in low-data regimes.
- The sparse conditioning mechanism reduces the need for dense annotations, increasing practical applicability to surgical datasets where dense labels are scarce.
- Extensive experimental evaluation spans three datasets and three downstream tasks, with useful ablations of synthetic data attributes (duplication, frame shuffle, noise, sparse frames).
- The additional GynSurg dataset in the appendix demonstrates some generalizability to different surgical settings.

### Weaknesses

- The novelty is incremental: the framework builds directly on SurV-Gen and adapts SparseCtrl, and the dual-prediction module is a straightforward extension of existing ideas from FlowVid/VideoJam without an isolated ablation.
- Comparisons with baselines are confounded: SurgiFlowVid is pre-trained on a large internal dataset (~7000 clips), while baselines (SurV-Gen, SparseCtrl) are not given the same pre-training; also, SurgiFlowVid is trained at 512x512 resolution while baselines may use lower resolutions.
- No ablation isolates the contribution of the dual-prediction (optical flow) module or the internal pre-training; the source of reported gains is unclear.
- Most reported improvements are within one standard deviation, and no statistical significance tests are provided, making the robustness of gains questionable.
- The abstract and introduction claim '10–20%' gains, but many tables show absolute improvements of only ~3–6 percentage points with overlapping error bars; this overstates the evidence.
- The paper's claim of being 'the first' conditional video diffusion for surgical data imbalance contradicts the existence of SurV-Gen (by the same authors).
- Video quality is not assessed with standard video-specific metrics (e.g., FVD, temporal consistency), and CLIP/LPIPS scores do not correlate with downstream performance.
- Reproducibility is limited: the internal pre-training dataset is not released and code is not provided, despite the reproducibility statement.
- The paper contains typos and inconsistencies (e.g., SurgFlowVid vs SurgiFlowVid) and some tables appear malformed in the provided text.

### Questions

- How do you ensure that the performance gains come from the proposed method and not from the larger internal pre-training dataset or higher training resolution? Could you compare SurgiFlowVid against SurV-Gen and SparseCtrl when they are pre-trained and trained at the same resolution?
- What is the isolated contribution of the dual-prediction (optical flow) module? Have you ablated by removing the flow prediction loss while keeping all else fixed, including pre-training?
- Are the reported improvements statistically significant? Please provide confidence intervals or hypothesis tests across seeds (e.g., paired t-tests or Wilcoxon).
- Since the generated videos condition on real frames from the training set and reuse those frames verbatim, how do you rule out that downstream gains come from the direct inclusion of those real frames rather than from the newly synthesized content?
- Why does the abstract claim 10–20% gains when most tables show smaller and/or overlapping improvements? Please provide the specific evidence supporting this claim.
- Can you provide standard video generation quality metrics (e.g., FVD, optical flow warp error) to complement downstream task performance, given that CLIP/LPIPS do not correlate with downstream gains?
- Will the code and the internal pre-training dataset be released to enable independent verification and fair comparison?
- What is the total training time and compute cost, including the pre-training stage on the internal dataset, compared with baselines?

### Limitations

- The method generates only short clips (16 frames, ~4 seconds), limiting applicability to tasks like surgical phase recognition that require longer temporal context.
- Sparse segmentation conditioning can lead to incorrect tool positions, as acknowledged in the paper.
- The method relies on real training frames as conditioning, which may compromise the novelty and diversity of the generated videos.
- The internal pre-training dataset is not released, harming reproducibility.
- No human evaluation or clinical validation of the generated videos is performed; practical utility beyond downstream metrics is unclear.
- The paper does not discuss potential ethical and privacy implications of using an in-house dataset of surgical recordings, nor does it mention IRB approval or data de-identification.

### Ethics

Ethical concerns flagged: **True**

## Usage and Cost

- Requests: 6
- Prompt tokens: 157,773
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 153,677
- Completion tokens: 20,898
- Reasoning tokens reported: 14,744
- Total tokens: 178,671
- Estimated total: $0.02737769

Full individual reviews and raw JSON responses are in `review_bundle.json`.
