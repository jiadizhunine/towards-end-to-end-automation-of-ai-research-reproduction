# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B044.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 1, 'Reject': 4}
- Estimated API cost: **$0.015050**

## Final Meta-review

The paper proposes ARSS, a decoder-only autoregressive transformer for novel view synthesis from a single image conditioned on predefined camera trajectories. It uses a video tokenizer to discretize multi-view sequences, a camera autoencoder to map Plücker raymaps into 3D positional tokens, and a hybrid permutation strategy that shuffles spatial token order while preserving temporal order. Evaluations on RealEstate10K, ACID, and zero-shot DL3DV show competitive LPIPS/PSNR but mixed SSIM/FID relative to diffusion baselines.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 2 | 2.400 | 0.490 | 2-3 |
| Clarity | 2 | 2.200 | 0.400 | 2-3 |
| Significance | 2 | 2.400 | 0.490 | 2-3 |
| Soundness | 2 | 2.400 | 0.490 | 2-3 |
| Presentation | 2 | 2.200 | 0.400 | 2-3 |
| Contribution | 2 | 2.400 | 0.490 | 2-3 |
| Overall | 4 | 4.600 | 0.800 | 4-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel application of decoder-only autoregressive models to multi-view novel view synthesis with explicit camera control, opening a direction distinct from diffusion-based approaches.
- The camera autoencoder design, using Plücker raymaps as token-level 3D positional guidance, is an elegant mechanism for integrating geometric information into next-token prediction.
- The hybrid token ordering (random spatial permutation with fixed temporal order) is well motivated and supported by ablations showing gains over raster and full-permutation strategies.
- The paper includes evaluations on multiple datasets including a zero-shot benchmark, with qualitative and quantitative comparisons against several baseline methods.
- Ablations on token ordering and tokenization provide useful insights into the design choices.

### Weaknesses

- Quantitative results do not consistently support the claim of outperforming state-of-the-art: SEVA shows higher SSIM on both RealEstate10K and ACID and substantially lower FID on ACID (47.76 vs 33.16), with no confidence intervals or significance tests.
- Important implementation details are missing, including the camera autoencoder architecture, training data, loss weights, codebook size, and whether it is jointly trained or frozen; the inference token ordering is also underspecified.
- An ablation table referenced as Table 3 for tokenization is missing from the manuscript, and the claimed FVD improvement cannot be verified.
- There are notation errors and ambiguities in equations (e.g., Eq. 5 defines d twice, Eq. 7/8 are incomplete/confusing), reducing clarity and reproducibility.
- The adaptation of baselines (e.g., per-frame generation for Genwarp and LVSM) may bias comparisons unfavorably, and metric aggregation across frames is not described.
- The method is only evaluated at 256x256 resolution and on 13 generated frames, with no evidence for scalability to higher resolutions or longer trajectories, which is central to the world-model motivation.
- No code or model weights are released, limiting reproducibility.

### Questions

- How is the camera autoencoder trained exactly? Is it pretrained separately and frozen, or fine-tuned with the AR transformer? What are the loss weights λ1-λ4 and codebook size/quantization for camera tokens?
- At inference, what is the spatial token order? Is it fixed raster, random, or a predetermined schedule? Does random training with fixed inference cause train-test mismatch?
- How were LVSM and Genwarp adapted? Were previous generated frames fed as source views during sequence generation? If not, is the comparison unfair?
- Why is Table 3, referenced for the tokenizer ablation, missing? Can you provide the FVD and other metrics for the VQ image tokenizer versus the video tokenizer?
- Can you explain the discrepancy between 17 input frames and 5 latent temporal codes? How many target frames are generated during evaluation?
- What is the effect of classifier-free guidance? What guidance scale was used, and how sensitive are results to it?
- Does ARSS support arbitrary-length video generation beyond 13 frames? Does performance degrade as sequence length grows and is there a mechanism to prevent error accumulation?

### Limitations

- Generation quality is bounded by the frozen video tokenizer, which is not specialized for multi-view images and struggles with large viewpoint changes.
- Training from scratch on limited public datasets at 256x256 resolution restricts fidelity and generalization compared to large-scale pretrained diffusion baselines.
- Quantitative results are mixed against SEVA, so the claimed advantage over state-of-the-art diffusion methods is not conclusive.
- No explicit evaluation of temporal consistency (e.g., FVD) is provided in the main comparison, despite the claimed advantage of video tokenization.
- No discussion of computational cost, model size, or inference speed despite claims of practical advantages over diffusion models.
- The generative model could potentially be misused to create deceptive visual content, but the broader impact section focuses only on future research directions.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 73,644
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 69,548
- Completion tokens: 18,934
- Reasoning tokens reported: 12,891
- Total tokens: 92,578
- Estimated total: $0.01504971

Full individual reviews and raw JSON responses are in `review_bundle.json`.
