# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B029.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.023411**

## Final Meta-review

This paper introduces ASTRAEA, a training-free framework for accelerating video diffusion transformers (vDiTs) through token-level selection and sparse attention. The framework consists of three main components: (1) a lightweight token selection mechanism that uses LSE scores from previous timesteps and input token differences to identify important tokens, with a penalty term to avoid repeatedly skipping the same tokens; (2) a GPU-friendly sparse attention strategy that computes only selected queries while keeping all keys and values, ensuring correctness and efficient parallelization with FlashAttention; and (3) an evolutionary algorithm-based search framework that automatically determines optimal token budget allocation across denoising timesteps. The method is evaluated on three vDiT models (HunyuanVideo, Wan, OpenSora) across multiple hardware platforms, achieving up to 2.4× inference speedup on a single GPU and 13.2× on 8 GPUs with minimal quality degradation (<0.5% VBench loss) compared to five state-of-the-art baselines.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.600 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 3.400 | 0.490 | 3-4 |
| Soundness | 3 | 3.200 | 0.400 | 3-4 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.400 | 0.490 | 3-4 |
| Overall | 6 | 6.400 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important and timely problem: the high computational cost of video diffusion transformer inference, which is a major barrier to practical deployment
- The token selection mechanism is lightweight and memory-efficient compared to prior work (e.g., ToCa), with negligible overhead (2.3% of execution time)
- The sparse attention design (computing only selected queries while keeping all keys/values) is elegant, ensuring correctness and GPU-parallelizability while integrating well with FlashAttention
- The evolutionary algorithm-based search framework is well-motivated, with appropriate crossover, mutation, and repair operations, and provides good justification for choosing EA over alternatives like NAS
- Comprehensive evaluation across three vDiT models (HunyuanVideo, Wan, OpenSora), multiple video lengths, two hardware platforms (A100, A6000), and extensive metrics (VBench, PSNR, SSIM, LPIPS, FLOPs, latency, memory)
- Well-designed ablation studies (SELECTQ&K, TIMSTEP-LEVEL, FIXED-TOKEN) and sensitivity analyses that clearly demonstrate the contribution of each component
- The paper is honest about limitations, including the computational cost of the EA search (82 GPU hours) and adaptations from prior work

### Weaknesses

- The claim of '>10 dB video quality compared to the state-of-the-art methods' is misleading, as it refers to PSNR improvements in specific settings and may not be representative across all models and configurations
- The EA search framework requires significant computational resources (average 82 GPU hours), which may limit practical deployment despite the paper's brief discussion of parallelization and dynamic programming acceleration
- The sparse attention approach still computes attention over all keys/values for selected queries, limiting computational savings compared to truly sparse approaches; more analysis of this trade-off is needed
- The token selection metric relies on LSE scores from previous timesteps, and while the 99.1% cosine similarity analysis provides some evidence, the robustness for highly dynamic scenes or rapid motion is not thoroughly explored
- The scalability results (13.2× on 8 GPUs) combine multi-GPU parallelism with token reduction benefits, making it unclear how much speedup is attributed to each factor
- The search framework is evaluated on only 4 prompts, and while the paper argues similarity in robustness trends, a more rigorous analysis of prompt diversity and its impact on search quality would strengthen the claims
- No discussion of potential negative societal impacts of faster video generation (e.g., deepfakes, misinformation)

### Questions

- Can you clarify the '>10 dB video quality' claim? Does this refer to PSNR against the original model's output rather than ground truth, and is this representative across all models and configurations?
- Can you provide a more detailed analysis of the computational savings of the sparse attention strategy compared to naive sparse attention, including theoretical and actual FLOPs reduction?
- How much of the 13.2× speedup on 8 GPUs is due to token reduction versus multi-GPU parallelism?
- What is the variance in optimal schedules found by the EA across different prompts? Could different prompt selections lead to significantly different token allocation schedules?
- How does the token selection metric behave for highly dynamic scenes or rapid motion? Does the reliance on LSE scores from previous timesteps break down in such cases?
- Why does ASTRAEA consume more memory than the original model for HunyuanVideo (69.01 GB vs 45.81 GB)? What is the source of this additional memory overhead?
- Could you elaborate on how the EA search cost scales with model size and video resolution, and is there a way to amortize this cost across different prompts or video configurations?
- Have you considered combining ASTRAEA with other acceleration methods (e.g., step reduction techniques like distillation) for even greater speedups?
- How does ASTRAEA perform on longer videos (e.g., 10+ seconds) or higher resolutions? Are there known limitations?
- Could you provide more details on how the baseline hyperparameters were tuned? This would help assess the fairness of the comparisons.

### Limitations

- The EA search framework requires substantial GPU resources (82 GPU hours per model), which could be a barrier for practitioners with limited compute; the paper mentions parallelization and dynamic programming acceleration but doesn't provide a comprehensive cost analysis
- The framework has been evaluated on three open-source vDiT models; applicability to proprietary or very large-scale models (e.g., Sora-class systems) is not directly demonstrated
- The token selection metric relies on LSE scores from previous timesteps, which may not generalize to all vDiT architectures or video content with rapid motion or scene changes
- The sparse attention approach still requires computing attention over all keys/values for selected queries, which limits the maximum achievable speedup
- The paper uses VBench as the primary quality metric, which has known limitations; additional human evaluation or other quality metrics could provide a more complete picture
- The search framework uses only 4 prompts for evaluation; a larger and more diverse prompt set could reveal cases where the search results are suboptimal
- Potential negative societal impacts of video generation acceleration (e.g., deepfakes, misinformation) are not discussed

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 154,093
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 145,133
- Completion tokens: 10,954
- Reasoning tokens reported: 0
- Total tokens: 165,047
- Estimated total: $0.02341083

Full individual reviews and raw JSON responses are in `review_bundle.json`.
