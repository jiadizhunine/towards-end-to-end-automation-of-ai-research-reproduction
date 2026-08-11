# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B054.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.016887**

## Final Meta-review

The paper presents VSSFlow, a unified flow-matching framework for video-conditioned sound generation (V2S) and visual text-to-speech (VisualTTS). The key contributions are: (1) a condition aggregation mechanism that uses cross-attention for video features and self-attention/concatenation for phoneme embeddings, based on the observation that these conditions have different determinism levels and attention layers have different inductive biases; (2) empirical evidence showing that end-to-end joint training of sound and speech generation is mutually beneficial, contrary to prior beliefs that required curriculum learning; (3) competitive results on V2S (VGGSound) and VisualTTS (Chem, GRID) benchmarks, with a demonstrated capability for joint sound+speech generation via fine-tuning on synthetic mixed data.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.000 | 0.000 | 6-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses a timely and important problem: unifying V2S and VisualTTS tasks in a single framework, which are typically treated separately in research.
- The condition aggregation mechanism is novel and well-motivated, with systematic ablation of four conditioning variants (CrossV, CrossVS, ConcatV, ConcatVS) providing interpretable evidence for design choices.
- The finding that joint training of sound and speech generation is mutually beneficial (rather than suppressive) challenges prior assumptions and is supported by convergence curves, CFG-scale analysis, and quality metrics.
- Thorough experimental evaluation covering sound quality, synchronization, semantic alignment, speech quality, speaker similarity, and lip-sync metrics.
- Well-written and organized paper with detailed appendices for reproducibility, including implementation specifics, datasets, and metrics.
- Relatively lightweight model (443M params) achieving competitive results compared to larger or more complex baselines.
- Promises to release code and checkpoints, aiding future research.

### Weaknesses

- The claim of 'surpassing SOTA' is somewhat overstated. VSSFlow achieves best FAD(vgg) on V2S but not on several other metrics (IS, KL, Onset Acc, DeSync). For VisualTTS, VSSFlow's WER on GRID (18.2) is notably worse than StyleDubber (10.9), and UTMOS is lower than several baselines on both Chem and GRID.
- Baseline comparisons are not entirely fair: VSSFlow is trained on additional TTS data (LJSpeech, LibriTTS, Chem, GRID, LRS2) while some baselines (e.g., Frieren) use only VGGSound. This makes it difficult to attribute performance gains solely to the architecture.
- The joint sound-speech generation capability (Section 4.5) is only demonstrated qualitatively on a few examples with synthetic mixed data, lacking quantitative evaluation or comparison with other unified models.
- No direct comparison is made with recent unified models (AudioGen-Omni, DualDub, DeepAudio) on the same benchmarks, which would strengthen the claims of superiority for the unified approach.
- The mechanistic explanation for why joint training helps (e.g., 'general audio prior', 'more stable CFG') is somewhat speculative and lacks rigorous analysis or controlled experiments to isolate the mechanism.
- The attention inductive bias analysis is based on visualizations but lacks quantitative metrics (e.g., attention entropy, distance from diagonal) to rigorously support the claims.
- The paper uses a VAE-vocoder pipeline (AudioLDM 2 VAE + HiFiGAN) which introduces reconstruction artifacts, as evidenced by the GT-vocoder baseline gap in UTMOS (3.19 vs. 4.19).

### Questions

- The abstract claims 'surpasses the state-of-the-art domain-specific baselines' but Tables 1 and 2 show VSSFlow is not best on all metrics (e.g., IS, KL, WER on GRID). Could you clarify which specific claims of superiority are being made and why certain metrics are prioritized?
- How does VSSFlow compare directly to AudioGen-Omni, DualDub, and DeepAudio on the same V2S and VisualTTS benchmarks? These are the most directly comparable unified methods, and a direct comparison would strengthen the claims.
- On GRID, VSSFlow's WER (18.2) is significantly worse than StyleDubber (10.9). What explains this gap? Is it due to the multi-speaker setting, the VAE-vocoder pipeline, the condition mechanism, or training data differences?
- Could you provide a matched-data comparison where VSSFlow is trained only on VGGSound for V2S evaluation, to enable a fair comparison with Frieren and other baselines that use only VGGSound?
- For the joint sound-speech generation case study, can you provide any quantitative evaluation (e.g., WER for speech, FAD for sound, alignment accuracy, intelligibility)? How does performance compare to separate models?
- The paper attributes joint training benefits to a 'general audio prior' and 'more stable CFG'. Could you provide more direct evidence, such as analyzing learned representations, measuring gradient conflicts, or ablating the CFG mechanism?
- The conditioning mechanism ablation is done at 100 epochs, but the final model is trained for 150 epochs. Do the relative rankings of the four variants hold at 150 epochs?
- How does the model handle videos longer than 10 seconds? Is there a truncation strategy or a sliding window approach?
- What is the computational cost (GPU hours, inference latency) of VSSFlow compared to baselines? The paper reports parameter counts but not FLOPs or latency.
- How sensitive are the VisualTTS results to the choice of speaker embedding extractor (RawNet3)?

### Limitations

- The joint sound-speech generation relies on synthetic mixed data, which may not fully capture the complexity of real-world co-occurring audio; native joint data would likely improve performance.
- The VAE-vocoder pipeline (AudioLDM 2 VAE + HiFiGAN) introduces reconstruction artifacts that limit upper-bound quality, as evidenced by the GT-vocoder baseline.
- The model is evaluated on English-only datasets (VGGSound, Chem, GRID, LRS2, LJSpeech, LibriTTS); generalization to other languages or low-resource settings is not explored.
- Potential bias in training data (e.g., demographics in LRS2, speaker diversity, accents) is acknowledged but not analyzed in detail.
- The paper does not provide a thorough analysis of failure cases or limitations of the proposed condition aggregation mechanism for edge cases (e.g., videos with no clear semantic audio, very long sequences).
- The joint training finding may be specific to flow-matching/DiT architectures and may not generalize to other paradigms (e.g., autoregressive models).
- The paper does not extensively discuss potential negative societal impacts beyond generic deepfake concerns; no specific mitigation strategies are proposed.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 104,590
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 95,630
- Completion tokens: 12,406
- Reasoning tokens reported: 0
- Total tokens: 116,996
- Estimated total: $0.01688697

Full individual reviews and raw JSON responses are in `review_bundle.json`.
