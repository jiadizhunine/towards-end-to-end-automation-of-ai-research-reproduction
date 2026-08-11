# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B159.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.019200**

## Final Meta-review

The paper introduces Dynadiff, a single-stage diffusion model for reconstructing images from time-resolved fMRI BOLD signals. Unlike prior multi-stage pipelines that collapse the temporal dimension of fMRI data (e.g., MindEye2, Brain-Diffuser), Dynadiff directly conditions a pretrained latent diffusion model on fMRI time-series via a brain module with subject-specific and timestep-specific layers, followed by temporal aggregation. The model is trained end-to-end with a single diffusion loss using LoRA adapters on cross-attention layers. Experiments on the Natural Scenes Dataset (NSD) demonstrate state-of-the-art performance on time-resolved fMRI signals, particularly on high-level semantic metrics (CLIP, DreamSim, AlexNet(2/5), mIoU), while remaining competitive on beta-value benchmarks. The paper also presents a novel time-resolved decoding analysis showing that specialized models trained at different time offsets can decode images at various points in the hemodynamic response, suggesting dynamic coding of visual representations in fMRI. Extensive ablations on window duration, brain module design, and fine-tuning strategies provide insights into the contribution of each component. The authors release code and discuss ethical considerations including mental privacy and face blurring.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.600 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.200 | 0.400 | 3-4 |
| Significance | 4 | 3.600 | 0.490 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.200 | 0.400 | 3-4 |
| Contribution | 4 | 3.600 | 0.490 | 3-4 |
| Overall | 7 | 6.800 | 0.400 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important limitation of existing fMRI-to-image decoding methods: the collapse of temporal information through beta-value preprocessing. The time-resolved approach is a novel and timely contribution.
- Significantly simplifies the decoding pipeline to a single-stage training process with a single diffusion loss, contrasting with the complex 2-4 stage architectures of prior work (Brain-Diffuser, MindEye2, WAVE).
- Achieves strong results on time-resolved fMRI data from NSD, outperforming adapted baselines on key high-level semantic metrics (AlexNet(2/5), CLIP, DreamSim, mIoU).
- The temporal analysis (Figures 4-5) is a unique contribution, characterizing how image representations evolve over time in brain activity and demonstrating that specialized decoders can decode images at different time offsets.
- Comprehensive ablation studies on brain module design, diffusion model fine-tuning strategies, time window duration, and preprocessing choices provide valuable insights for the community.
- The paper is well-written, clearly organized, and transparent about limitations and ethical considerations. Public code release enhances reproducibility.
- Cross-subject experiments showing transfer learning benefits and reduced data requirements with pretraining add practical value.

### Weaknesses

- The claim of state-of-the-art performance is primarily supported on time-resolved data; on the standard beta-value benchmark (Table 4), Dynadiff underperforms MindEye2 on low-level metrics (SSIM 0.37 vs 0.43, PixCorr 0.21 vs 0.32). This trade-off is not transparently highlighted in the main text.
- The adaptation of baselines (MindEye1/2) to time-series data by simply flattening the time dimension may be suboptimal and potentially unfair, as these methods were designed for beta values. A more sophisticated temporal adaptation could yield different comparison results.
- The interpretation of temporal dynamics as 'dynamic coding' is speculative given the low temporal resolution of fMRI (TR=1.3s) and the slow hemodynamic response. Observed temporal patterns could largely reflect the HRF shape rather than true neural dynamics.
- The gains over MindEye2 on low-level metrics (SSIM, PixCorr) are negligible or slightly negative, suggesting the advantage is mainly on high-level semantic metrics. The paper does not deeply analyze this trade-off.
- The 'specialized' models in the temporal analysis require training a separate model for each time offset, which is computationally expensive and partially contradicts the simplicity claim of the approach.
- The comparison with the most recent methods (e.g., Psychometry, NeuroPictor) is only present in the beta-value appendix, not in the main time-series evaluation, limiting the completeness of the state-of-the-art comparison.
- Computational cost (2.5 days on 8 A100 GPUs per subject) is substantial and may limit reproducibility for smaller research groups; this limitation is not explicitly discussed.

### Questions

- How were MindEye1/2 adapted to time-series fMRI input? The paper mentions flattening the time dimension, but could this have disadvantaged these models? Would a more sophisticated adaptation (e.g., a temporal encoder before the existing architecture) change the comparison results?
- In the temporal analysis, the 'General' model decodes previous/next images at extreme time shifts. Is this due to information leakage from neighboring trials (e.g., overlapping hemodynamic responses), or does it indicate the model is decoding the wrong stimulus? How does this affect interpretation of the time-resolved results?
- Given the slow HRF, how do you disentangle neural dynamics from hemodynamic response properties? Have you considered deconvolution or explicit HRF modeling to support the 'dynamic coding' claim?
- The paper reports lower performance on low-level metrics (SSIM, PixCorr) compared to MindEye2 while high-level metrics improve. Is this an inherent trade-off of the approach, or could it be addressed through architectural or training modifications?
- What is the total computational cost of training all 'specialized' models for the temporal analysis? How many models were trained in total?
- How sensitive are the results to the choice of LoRA rank and alpha? Was any hyperparameter search conducted for these?
- For the cross-subject experiments, how does the multi-subject model perform without fine-tuning on the new subject? This would clarify the true generalization capability.
- The paper mentions that null text embeddings didn't boost performance. What was the rationale for this experiment, and were there any differences in training stability?
- The evaluation uses a fixed random seed for selecting one of three test repetitions. How sensitive are results to this choice? Would averaging across all three repetitions change conclusions?

### Limitations

- The approach is validated only on the NSD dataset, which has a stereotypical image distribution (MS-COCO images) and only 4 subjects. Generalization to other datasets or more naturalistic stimuli remains unclear.
- The method requires substantial per-subject training data (27,000 trials), limiting applicability to studies with limited data availability.
- Preprocessing still requires manual steps (detrending, z-scoring, ROI selection) that could be automated with learned or foundational models of brain activity.
- The time-resolved analysis is limited to static images; extending to video decoding would require additional architectural considerations.
- The model does not address cross-subject generalization without fine-tuning, which remains an open challenge.
- The computational cost (2.5 days on 8 A100 GPUs per subject) may hinder adoption by researchers with limited resources.
- The paper acknowledges potential ethical concerns about mental privacy and face generation, but the face-blurring solution is only briefly mentioned and may not fully address the issue. The paper could also discuss the risk of overclaiming 'mind reading' capabilities and the need for responsible communication of brain decoding results.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 123,146
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 114,186
- Completion tokens: 11,389
- Reasoning tokens reported: 0
- Total tokens: 134,535
- Estimated total: $0.01920005

Full individual reviews and raw JSON responses are in `review_bundle.json`.
