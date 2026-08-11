# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B054.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 1, 'Reject': 4}
- Estimated API cost: **$0.019678**

## Final Meta-review

VSSFlow is a unified flow-matching framework for video-to-sound (V2S) and visual text-to-speech (VisualTTS) generation. It uses a DiT-based architecture with two condition aggregation mechanisms: video features are injected via cross-attention, while phoneme transcript embeddings are concatenated with the audio latent and processed via self-attention. The paper claims that this design exploits the inductive biases of the attention mechanisms, and that joint training on sound and speech is mutually beneficial, unlike prior curriculum-based approaches. It also demonstrates a fine-tuning recipe on synthetic sound-speech mixtures to enable simultaneous sound-speech generation. Experiments are conducted on VGGSound, Chem, and GRID benchmarks, with competitive results on some metrics.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 2.800 | 0.400 | 2-3 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 2 | 2.600 | 0.490 | 2-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 2 | 2.400 | 0.490 | 2-3 |
| Presentation | 2 | 2.600 | 0.490 | 2-3 |
| Contribution | 2 | 2.400 | 0.490 | 2-3 |
| Overall | 4 | 4.600 | 0.800 | 4-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses a timely and relevant problem of unifying V2S and VisualTTS in a single framework without complex multi-stage training.
- Provides a systematic ablation of condition aggregation mechanisms (cross-attention vs concatenation), with attention visualizations supporting the design choices.
- Reports that joint training of sound and speech tasks can improve V2S performance while maintaining VisualTTS quality, with convergence and CFG analyses providing some insight.
- The model is parameter-efficient (443M) and achieves strong FAD on VGGSound, demonstrating comparable sound quality to larger domain-specific baselines.
- The case study on joint sound-speech generation from out-of-domain videos is a compelling qualitative demonstration of the model's potential.

### Weaknesses

- The claimed mutual benefit from joint training is confounded by data volume: joint-training settings use more training data than single-task settings, and no control experiments (e.g., adding sound-only data) isolate the effect of task synergy.
- The SOTA claim is not consistently supported by the results: on V2S, VSSFlow trails MMAudio on several metrics (FAD-pann, IS, Onset AP, DeSync), and on VisualTTS, it has higher WER on GRID and lower UTMOS on Chem than StyleDubber and EmoDubber.
- The unified model is not compared with the most relevant unified baselines (AudioGen-Omni, DualDub), making it unclear whether the proposed condition aggregation mechanism is superior to existing in-context or fusion approaches.
- The joint sound-speech generation capability is only demonstrated via a qualitative case study using synthetic mixed data; no quantitative metrics (e.g., WER for speech, FAD for sound) are provided.
- Several implementation details are missing, including the initialization of the DiT backbone (whether pretrained weights are used), the training of the phoneme duration predictor, and the exact use of speaker embeddings, which hinders reproducibility.
- The condition mechanism ablation lacks statistical significance testing and error bars, and the attention-map analysis is qualitative, making the claimed inductive biases not fully supported.
- VisualTTS performance is inconsistent across datasets, and the model seems to sacrifice speech intelligibility on GRID in favor of joint generation; LRS2 results are not reported despite LRS2 being in the training set.

### Questions

- Did you control for data volume in the joint training experiments? For example, did you train a V2S-only model on the same number of total samples by adding sound-only data (e.g., AudioSet) or by increasing training steps? Could the observed improvements come solely from seeing more data?
- Why are AudioGen-Omni and DualDub not included in the comparisons? Can you provide any quantitative or qualitative evidence that your condition aggregation mechanism outperforms their in-context conditioning or fusion modules?
- What is the exact initialization of the DiT backbone? If it is pretrained (e.g., from Stable Audio Open), how does that affect the joint-training conclusions and the fairness of comparisons with baselines?
- Are the reported metrics from a single run? What is the variance across seeds, and are the differences between condition variants statistically significant?
- How are phoneme durations predicted at inference for VisualTTS? Is the duration predictor trained separately, and what inputs does it use? How does its accuracy affect the final WER?
- Since VSSFlow's WER on GRID is notably higher than StyleDubber, what specific design choices contribute to this gap? Would a larger model or a different text-conditioning strategy close it?
- Can you provide quantitative metrics (e.g., WER for speech, FAD for sound) for the joint sound-speech generation fine-tuning on the Veo3 videos or on a held-out mixed dataset?
- Why are LRS2 VisualTTS results not reported, given that LRS2 is used for training? What are the model's performance and potential failure cases on LRS2?

### Limitations

- The joint-learning benefit is not isolated from increased training data, so the main qualitative conclusion of mutual benefit is not well-supported.
- The joint sound-speech generation capability relies on fine-tuning on synthetic sound-speech mixtures, which likely underperforms native co-occurring data and is not quantitatively evaluated.
- The model is evaluated only on English audio-visual datasets (VGGSound, Chem, GRID, LRS2, LJSpeech, LibriTTS); generalization to other languages, accents, and in-the-wild video domains is untested.
- The audio quality is bounded by the fixed VAE/vocoder pipeline; GT-vocoder baselines show a reconstruction ceiling below ground truth, limiting speech naturalness and sound fidelity.
- No human perceptual evaluation (e.g., MOS listening tests) is conducted; all results rely on automatic metrics that may not fully capture perceived quality and synchronization.
- The paper does not report inference time, memory usage, or computational cost beyond parameter count, limiting practical applicability assessment.
- Potential negative societal impacts from deepfake audio creation are acknowledged but not thoroughly discussed with concrete mitigation measures.
- The code and checkpoints are promised for release but not provided in the submission, hindering reproduction and verification.

### Ethics

Ethical concerns flagged: **True**

## Usage and Cost

- Requests: 6
- Prompt tokens: 94,420
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 90,324
- Completion tokens: 25,077
- Reasoning tokens reported: 17,863
- Total tokens: 119,497
- Estimated total: $0.01967839

Full individual reviews and raw JSON responses are in `review_bundle.json`.
