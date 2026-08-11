# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B170.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.021589**

## Final Meta-review

MotionStream presents a streaming motion-conditioned video generation framework that enables real-time interactive generation. The method trains a bidirectional motion-conditioned teacher model using lightweight sinusoidal track embeddings and joint text-motion guidance, then distills it into a causal student via Self Forcing-style Distribution Matching Distillation. Key innovations include attention sinks with rolling KV caches for stable long-video extrapolation, extrapolation-aware training, and a Tiny VAE decoder. The system achieves up to 29.5 FPS on a single H100 GPU with sub-second latency, enabling drag-based control, camera control, and motion transfer. The paper demonstrates state-of-the-art results on motion transfer and camera control benchmarks while being orders of magnitude faster than prior methods.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.800 | 0.400 | 3-4 |
| Quality | 3 | 3.400 | 0.490 | 3-4 |
| Clarity | 3 | 3.400 | 0.490 | 3-4 |
| Significance | 4 | 3.800 | 0.400 | 3-4 |
| Soundness | 4 | 3.600 | 0.490 | 3-4 |
| Presentation | 3 | 3.400 | 0.490 | 3-4 |
| Contribution | 4 | 3.800 | 0.400 | 3-4 |
| Overall | 7 | 7.400 | 0.490 | 7-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses a significant and timely gap: real-time interactive motion-controlled video generation, which prior methods cannot achieve due to slow, non-causal, and short-duration generation.
- The technical approach is well-motivated, with careful analysis of attention patterns leading to the attention sink mechanism adapted from LLMs.
- Comprehensive evaluation across multiple tasks (motion transfer, camera control) with thorough ablations on key design choices (chunk size, sink size, window size, guidance scales).
- Novel combination of techniques: Self Forcing, DMD, attention sinks, and rolling KV caches integrated into a unified framework for video generation.
- Impressive practical speedup: two orders of magnitude faster than prior methods while maintaining competitive quality.
- The joint text-motion guidance approach elegantly balances trajectory adherence with natural motion generation.
- Multiple downstream applications demonstrated: motion transfer, drag-based control, and camera control.
- Honest and thorough discussion of limitations, including failure cases and scenarios where the approach struggles.
- Clear writing and good contextualization with related work.

### Weaknesses

- Evaluation of 'infinite-length' generation is limited to 241 frames (~15 seconds), which does not fully substantiate the claim of truly infinite generation.
- Comparisons with baselines use different backbone models (e.g., ATI uses Wan 2.1-14B vs. the authors' 1.3B), making direct quality comparisons unfair and not prominently addressed in main results.
- The camera control evaluation on LLFF is somewhat indirect, as it adapts 2D tracks to 3D camera control rather than directly supporting camera parameters.
- Limited direct comparison with other real-time video generation methods (e.g., CausVid, TalkingMachines) in terms of quality-speed trade-offs.
- The user study only evaluates video quality, not trajectory adherence, which is a key claim of the paper.
- The paper does not provide a detailed analysis of memory footprint during long generation, which is important for practical deployment.
- Evaluation datasets are small (30 DAVIS videos, 20 Sora videos), and the evaluation metrics are largely reconstruction-based, which may not fully capture generative quality.

### Questions

- How does the model handle user interactions that change trajectories mid-generation? What is the exact mechanism for updating tracks during streaming, and how quickly do changes take effect?
- What is the memory footprint during long generation? Does the KV cache rolling maintain constant memory usage regardless of generated video length?
- Is there evidence of quality degradation for videos longer than 241 frames? Have you tested generation beyond this horizon, and what were the results?
- How does the method perform when user inputs are imperfect or noisy (e.g., jittery mouse movements)? The paper mentions stochastic masking during training, but could you provide more analysis of robustness to imperfect inputs?
- Given that ATI with 14B backbone produces more visually favorable videos according to the user study, what specific advantages does MotionStream offer beyond speed for practitioners who prioritize quality over interactivity?
- Could you provide more details on the Tiny VAE training—specifically, how does the quality degradation from the Tiny VAE compare to other components in the pipeline, and are there scenarios where the Full VAE is preferable despite lower throughput?
- Could you provide a more direct comparison with CausVid or TalkingMachines on the same tasks and backbone to better isolate the contribution of your attention sink and training strategy?

### Limitations

- The fixed attention sink mechanism limits handling of complete scene changes, as the model tends to preserve the initial scene rather than adapting to new contexts.
- Artifacts occur with extremely rapid or physically implausible motion trajectories, manifesting as temporal inconsistencies or distortions.
- The model sometimes struggles to preserve source details for highly complex scenes, prompts, or motions, partly due to backbone capacity limitations.
- The evaluation of 'infinite-length' generation is limited to 241 frames, and longer-term stability is not fully demonstrated.
- The method currently supports 2D track-based control but not other control modalities (e.g., audio, 3D geometry), which may limit its applicability to certain downstream tasks.
- Potential negative societal impact includes the creation of deceptive media, which the authors acknowledge in the ethics statement.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 142,648
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 133,688
- Completion tokens: 10,170
- Reasoning tokens reported: 0
- Total tokens: 152,818
- Estimated total: $0.02158901

Full individual reviews and raw JSON responses are in `review_bundle.json`.
