# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B159.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.022376**

## Final Meta-review

The paper introduces Dynadiff, a single-stage diffusion-based model for reconstructing natural images from time-resolved fMRI BOLD signals. Unlike multi-stage pipelines that rely on time-collapsed beta values, Dynadiff directly conditions a pretrained latent diffusion model on fMRI time-series via a brain module with subject-specific and timestep-specific linear layers, temporal aggregation, and LoRA adapters on cross-attention layers. It is trained end-to-end with a standard diffusion loss. On the Natural Scenes Dataset, Dynadiff reports improved single-trial reconstruction over baselines on high-level semantic metrics, demonstrates time-resolved decoding with shifted windows, and provides ablations on window duration, module design, finetuning strategy, and cross-subject transfer.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 2 | 2.800 | 0.400 | 2-3 |
| Clarity | 2 | 2.800 | 0.400 | 2-3 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 2 | 2.800 | 0.400 | 2-3 |
| Presentation | 2 | 2.800 | 0.400 | 2-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 4 | 6.000 | 1.095 | 4-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Proposes a genuinely simpler single-stage training pipeline compared to multi-stage baselines (MindEye2, WAVE, Brain-Diffuser), reducing hand-engineered components.
- Reports state-of-the-art or competitive results on single-trial BOLD time series from NSD, with consistent improvements on high-level semantic metrics (CLIP, AlexNet, DreamSim, mIoU).
- Demonstrates time-resolved decoding with general and specialized models, offering a novel tool to study temporal evolution of image representations in fMRI.
- Includes comprehensive ablations and additional experiments (beta values, cross-subject pretraining), strengthening technical soundness.
- Authors include an ethics/impact statement and commit to blurring reconstructed faces.

### Weaknesses

- The main single-trial results use the standard NSD split with interleaved train/test presentations and an 8s fMRI window starting 3s after onset, which overlaps subsequent stimuli (4s ISI). This may allow the decoder to exploit train-image information from adjacent trials, confounding the reported performance. The authors only use a time-resolved split for auxiliary analyses, not for the main results.
- Baseline comparisons may be unfair: MindEye1/2 are adapted to time series by simply flattening the temporal dimension, likely failing to exploit temporal structure; WAVE uses a different atlas/preprocessing and window, so the comparison is not fully controlled.
- No inferential statistics are provided beyond SEM across four subjects; it is unclear whether improvements over MindEye2 are statistically significant given the small sample.
- There are inconsistencies in reported metrics across tables (e.g., CLIP/AlexNet values for the same Dynadiff configuration differ between Table 1 and Tables 2/3), undermining reproducibility and clarity.
- The 'single-stage' claim is partially overstated: the method relies on a heavy pretrained latent diffusion model and CLIP encoders, and still requires training LoRA adapters plus a 400M-parameter brain module.
- The temporal generalization 'dynamic coding' interpretation is confounded by the hemodynamic response function and overlapping stimulus responses; the paper does not disentangle these effects.
- The computational cost is high (8 A100 GPUs for 2.5 days per model, plus many specialized models), limiting accessibility and practical adoption.

### Questions

- How do you ensure that the standard NSD split does not lead to temporal contamination between train and test trials? Could the decoder be reconstructing adjacent train images rather than the intended test stimulus, given the 8s window and 4s ISI? Why not use the time-resolved split for the main results?
- For MindEye1/2 baselines, were hyperparameters re-tuned after adapting to time series by flattening? Would a temporally aware adaptation (e.g., a temporal Transformer) substantially improve their performance?
- What statistical tests were used to establish significance of improvements over MindEye2 given only four subjects? Could permutation tests or per-trial paired analyses change the conclusions?
- Can the authors reconcile the discrepancies in reported metrics across tables (Table 1 vs Tables 2/3)? Are these due to different splits, repetition averaging, or other protocol differences?
- How do you separate dynamic coding from hemodynamic delays? Would a simple convolution model of the HRF reproduce the time-shift generalization curves?
- What is the exact breakdown of the 400M brain module parameters, and how many are subject-specific? Does the model overfit on 27,000 training trials per subject?
- Why is null text conditioning used instead of image captions or CLIP text embeddings? What was the empirical comparison?
- Could the time-resolved results be driven by low-level visual features rather than semantic representations? What evidence supports high-level dynamic coding?

### Limitations

- Evaluation is limited to four subjects from the NSD dataset, which has a stereotyped image distribution, and generalization to other datasets or more diverse images is untested.
- The method requires large per-subject training data (27,000 trials) and does not achieve zero-shot decoding for unseen participants without fine-tuning.
- The main results may be confounded by temporal overlap between training and test trials due to the standard NSD split and the long 8s window.
- Computational cost is substantial: 8 A100 GPUs for 2.5 days per model, and the time-resolved analysis requires many specialized models, limiting practical utility.
- The model reconstructs static images only; extension to continuous video decoding is not demonstrated.
- Preprocessing still involves manual detrending, ROI selection, and z-scoring, so the approach is not fully end-to-end from raw brain signals.
- The face-blurring safeguard is described but not evaluated; mental privacy risks are acknowledged but not fully mitigated.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 111,822
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 107,726
- Completion tokens: 26,010
- Reasoning tokens reported: 17,924
- Total tokens: 137,832
- Estimated total: $0.02237591

Full individual reviews and raw JSON responses are in `review_bundle.json`.
