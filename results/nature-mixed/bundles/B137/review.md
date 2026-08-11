# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B137.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **5/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 1, 'Reject': 4}
- Estimated API cost: **$0.026280**

## Final Meta-review

The paper proposes SurgiFlowVid, a sparse and controllable video diffusion framework for generating synthetic surgical videos of under-represented classes to mitigate data imbalance. The key contributions are: (1) a dual-prediction diffusion U-Net that jointly denoises RGB frames and optical flow maps to provide temporal inductive biases for motion modeling from limited samples; (2) a sparse visual encoder that conditions generation on lightweight signals such as sparse segmentation masks or RGB frames, avoiding the need for dense annotations; and (3) extensive evaluation on three surgical datasets (SAR-RARP50, GraSP, AutoLaparo) across downstream tasks including surgical action recognition, tool presence detection, and laparoscope motion prediction, showing performance gains over competitive baselines. The method builds directly on the recent SurV-Gen framework with these extensions.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 2.800 | 0.400 | 2-3 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 2.800 | 0.400 | 2-3 |
| Overall | 5 | 5.400 | 0.800 | 5-7 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- The paper addresses a practically important problem: data imbalance in surgical video datasets, which is a critical bottleneck for downstream model robustness.
- The dual-prediction approach (joint RGB + optical flow denoising) is a reasonable and well-motivated technique for improving temporal modeling from limited data.
- The sparse conditioning mechanism is practical and well-motivated, enabling controllability without requiring dense expert annotations that are rarely available in surgical settings.
- The experimental evaluation is extensive, covering three diverse surgical datasets and multiple downstream tasks, with useful ablations on synthetic data attributes and conditioning strategies.
- The paper is generally well-written and organized, with detailed appendices supporting reproducibility.

### Weaknesses

- The novelty is incremental over the closely related SurV-Gen framework; the core architecture builds directly on SurV-Gen with modifications (optical flow prediction, sparse encoder) that are relatively straightforward extensions.
- The claimed '10-20% improvements' are not consistently achieved across all settings; gains vary significantly by class and conditioning type, and some improvements are within standard deviation ranges, with no statistical significance testing.
- The use of an internal curated dataset (~7000 clips) for pre-training is a significant confound; it is unclear whether baselines also benefited from this pre-training, raising concerns about fairness and reproducibility.
- The evaluation lacks comparison with simpler data augmentation strategies (e.g., Mixup, CutMix, temporal cropping) that could serve as strong baselines for the data imbalance problem.
- No quantitative evaluation of generated video quality using standard metrics (e.g., FVD, IS) is provided; CLIP/LPIPS scores show no clear correlation with downstream performance.
- The individual class modeling results are inconsistent (e.g., SurgiFlowVid with Seg conditioning performs worse than without individual modeling in some settings), and the paper opts out of segmentation conditioning on GraSP due to sparsity, limiting generalizability claims.
- The paper does not discuss potential negative societal impacts or clinical safety concerns of synthetic surgical data.

### Questions

- Did the baseline methods (SurV-Gen, SparseCtrl) also use the internally pre-trained temporal layers? If not, could this pre-training advantage explain the observed performance differences?
- Can you provide statistical significance tests (e.g., paired t-tests or confidence intervals) for the key comparisons in Tables 2-5 to better assess the reliability of the reported gains?
- How does your method compare to simpler video augmentation techniques like temporal cropping, frame interpolation, or speed perturbation? These would be stronger baselines than simple data duplication.
- What is the specific contribution of the optical flow dual-prediction? Please provide an ablation where the model is trained without the flow loss (i.e., standard SurV-Gen with the same pre-training) to isolate its effect.
- Can you provide more details about the internal dataset of 7000 clips used for pre-training? What surgical procedures are included, and how does it differ from the downstream evaluation datasets?
- Have you considered evaluating generated videos with surgical-specific metrics (e.g., tool presence accuracy in generated frames, action consistency) or standard video generation metrics like FVD?
- How sensitive are the results to the number of synthetic samples added? Is there an optimal ratio of synthetic to real data?
- What is the total computational cost of the full pipeline (pre-training, fine-tuning, inference), and how scalable is this to larger datasets or longer videos?

### Limitations

- The paper acknowledges the limitation of generating only short video clips (~4 seconds), which may limit applicability to tasks requiring longer temporal context such as phase recognition.
- The paper notes that sparse segmentation frames can lead to incorrect tool position generation, but this limitation is not deeply analyzed or mitigated.
- The reliance on an internal, not publicly described dataset for pre-training is a significant limitation for reproducibility and generalizability.
- The paper does not discuss potential negative societal impacts of synthetic surgical data, such as the risk of generated videos being used for training models without proper validation, potentially leading to unsafe deployment in clinical settings.
- The computational resources required (H200-140GB GPUs) are substantial and may limit practical adoption in resource-constrained healthcare settings.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 172,464
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 163,504
- Completion tokens: 12,014
- Reasoning tokens reported: 0
- Total tokens: 184,478
- Estimated total: $0.02627957

Full individual reviews and raw JSON responses are in `review_bundle.json`.
