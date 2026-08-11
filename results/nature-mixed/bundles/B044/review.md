# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B044.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.012650**

## Final Meta-review

The paper introduces ARSS, a novel framework for single-image novel view synthesis using a GPT-style decoder-only autoregressive transformer. The method has three key components: (1) a video tokenizer that converts multi-view image sequences into discrete tokens while preserving temporal consistency, (2) a camera autoencoder that maps Plücker raymaps into 3D positional tokens for precise camera control, and (3) a hybrid token permutation strategy that shuffles spatial order while preserving temporal order, enabling causal modeling of bi-directional visual data. The model is trained on RealEstate-10K and ACID and evaluated for zero-shot generalization on DL3DV, showing competitive or superior performance compared to diffusion-based baselines. Ablation studies validate the design choices.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 4.000 | 0.000 | 4-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 4 | 3.600 | 0.490 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.200 | 0.400 | 3-4 |
| Overall | 6 | 6.400 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel application of autoregressive models to novel view synthesis with explicit camera control, opening a new direction in the field
- Well-designed camera autoencoder that provides effective 3D geometric guidance through Plücker raymap encoding
- Thoughtful hybrid token permutation strategy that addresses the mismatch between causal modeling and bi-directional visual data
- Comprehensive evaluation across multiple datasets including zero-shot generalization
- Ablation studies clearly validate the key design choices
- Clear potential for scalability and integration with LLM-style unified generative frameworks

### Weaknesses

- Quantitative results are mixed: while PSNR and LPIPS improve over SEVA, SSIM and FID are notably worse, suggesting geometric inconsistencies that are not deeply analyzed
- Evaluation limited to 256x256 resolution, which is lower than many current SOTA methods
- Missing comparison with several strong recent baselines (e.g., ViewCrafter, CAT3D, MVSplat360)
- Technical clarity issues in equations (e.g., Eq. 5 uses 'd' for both ray direction and momentum)
- The claim of being 'first' may need qualification given concurrent AR video generation work
- No user study or preference evaluation was conducted
- The camera autoencoder's ablation is limited; no analysis of loss component weights or comparison with simpler conditioning approaches

### Questions

- Can you provide a more detailed analysis of why SSIM and FID are worse than SEVA? Is this a fundamental limitation of the AR approach or can it be addressed?
- Have you considered comparing with recent diffusion-based methods like ViewCrafter, CAT3D, or ReconFusion?
- What is the computational cost (training time, inference time, GPU memory) compared to SEVA and other diffusion baselines?
- How does the model handle large camera displacements? Can you show results or discuss failure cases for extreme viewpoint changes?
- Can you quantify the speedup achieved with parallel decoding compared to sequential decoding?
- How does performance scale with longer sequences (e.g., 30, 50 frames)? This is important for the world modeling application claim.
- How does the camera autoencoder compare to simpler alternatives like direct camera parameter embedding or cross-attention conditioning?
- In Table 2, why do the ablation results (PSNR 19.22) not match the main results in Table 1 (PSNR 19.02)?
- What is the effect of the camera autoencoder loss weights (lambda_1 to lambda_4)? Are there ablations for these?

### Limitations

- Generation quality is limited by the frozen video tokenizer, which is not specifically designed for multi-view data and struggles with large viewpoint changes
- Training is done from scratch on limited public datasets at relatively low resolution (256x256), which may not generalize as well as large-scale pre-trained models
- The autoregressive sampling process may be slower than parallel diffusion generation for short sequences, though parallel decoding partially mitigates this
- The method generates sequences of fixed length (13 target frames in experiments) and may not easily extend to arbitrarily long sequences without further analysis
- Potential negative societal impact: the technology could be misused for creating realistic fake imagery or misleading visual content, though this is common to all generative view synthesis methods and not unique to this work

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 83,141
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 74,181
- Completion tokens: 7,999
- Reasoning tokens reported: 0
- Total tokens: 91,140
- Estimated total: $0.01265015

Full individual reviews and raw JSON responses are in `review_bundle.json`.
