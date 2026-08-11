# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B114.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.014900**

## Final Meta-review

Omni-View is a unified multimodal model for 3D scenes that jointly performs scene understanding, novel view synthesis, and geometry estimation. Built on BAGEL-7B, it splits generation into a texture module (RGB novel view synthesis via flow matching and autoregressive generation) and a geometry module (depth and camera pose estimation), and trains the full system in two stages: a joint understanding-and-generation stage with a dense-to-sparse reference-view curriculum, followed by a generation-focused fine-tuning stage. The model achieves state-of-the-art results on VSI-Bench (55.4) and strong performance on 3D QA/localization benchmarks, while also demonstrating competitive novel view synthesis and scene generation, all from RGB-only input.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 2 | 2.000 | 0.000 | 2-2 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 2 | 2.200 | 0.400 | 2-3 |
| Presentation | 2 | 2.000 | 0.000 | 2-2 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 4 | 4.200 | 0.400 | 4-5 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- The core idea of leveraging generation (novel view synthesis and geometry estimation) to improve 3D scene understanding is novel and well-motivated, connecting to neurocognitive evidence.
- The split into separate texture and geometry modules is a thoughtful architectural design that enables explicit geometric supervision and autoregressive spatiotemporal modeling.
- The dense-to-sparse (D2S) reference-view curriculum is a simple yet effective training strategy, with ablations showing clear benefits over dense-only, sparse-only, and random masking.
- Strong empirical results: Omni-View substantially outperforms the BAGEL-FT baseline on VSI-Bench (55.4 vs. 46.3) and achieves competitive or state-of-the-art results on 3D understanding benchmarks without explicit 3D input.
- Comprehensive ablation studies (Tables 4-7) decompose the contributions of texture/geometry modules, autoregressive generation, D2S schedule, and stage 2, providing useful insights.
- The model operates on RGB-only input, making it more practical than methods that require point clouds, voxels, or BEV representations.

### Weaknesses

- A major confound exists in the main comparison: BAGEL-7B-FT is trained on understanding data only, while Omni-View also uses 61k additional video clips from Re10k for generation. The reported gains could stem from extra data/compute rather than the 'generation facilitates understanding' mechanism; no control experiment trains on the same added data with only an understanding objective.
- Model-size mismatch in comparisons: several strong baselines (e.g., VG-LLM-4B, Spatial-MLLM-4B) have 4B parameters, while Omni-View is 7B, weakening the claim of state-of-the-art status.
- The geometry module's actual depth and camera-pose prediction accuracy is never directly evaluated on standard benchmarks. Since training uses synthetic depth maps from Voyager, the contribution of 'explicit geometric constraints' is not validated, and the limited ablation shows only modest improvements in absolute distance tasks.
- The paper is poorly written with numerous typos, grammatical errors, and LaTeX artifacts (e.g., 'forzen', 'randon mask', 'donate', 'Archtitectures', broken equations, garbled table formatting), which significantly hampers clarity and reproducibility.
- Missing technical details: exact architectures of texture/geometry modules, cross-attention mechanism, flow-matching formulation, diffusion-forcing specifics, camera pose query, dataset filtering criteria, and hyperparameters are not fully specified.
- The VSI-Bench subset used in ablations is not clearly defined; if it overlaps with the test set, repeated ablations could lead to overfitting.
- The paper claims state-of-the-art in scene generation, but Table 3 shows only marginal improvements over specialized models (e.g., PSNR 23.22 vs. 23.12 for Voyager), with no statistical significance tests; text is even contradictory about the extent of improvement.
- The generation evaluation uses a non-standard protocol (Dust3R reconstruction) that may not be fully comparable with prior work, and the paper admits camera-pose control is challenging.

### Questions

- Did BAGEL-7B-FT receive the exact same total data and training compute as Omni-View (including the 61k re10k clips) but with only the understanding objective? If not, how do you disentangle the performance gain from additional generation data versus the proposed architecture/objectives?
- What exactly is the 'VSI-Bench (subset)' used in ablations? Is it the full test set, a separate validation set, or a random sample? If it overlaps with the test set, how do you avoid overfitting through repeated ablations?
- How are the understanding model's features integrated into the texture and geometry modules? Provide precise architecture details (dimensions, cross-attention layers, conditioning mechanisms).
- What is the flow-matching formulation: number of sampling steps, noise parameterization, how autoregressive conditioning is applied across frames, and what 'diffusion forcing' concretely involves?
- How are the camera poses used in the texture module obtained during training and inference? Are they ground-truth, predicted by the geometry module, or specified externally? What is the relationship between the pose used for NVS and the pose estimated by the geometry module?
- Can you provide quantitative evaluation of the geometry module's depth and camera-pose prediction accuracy on standard benchmarks (e.g., Re10k or ScanNet depth/pose metrics)? Without this, it is hard to assess the role of 'explicit geometric constraints.'
- What are the exact hyperparameters (learning rate, batch size, training steps, loss weights) and computational cost (GPU hours) for Omni-View and BAGEL-FT?
- Why does the geometry module, trained on synthetic depth, still improve understanding on relative distance? Does this improvement transfer to real-world depth estimation?
- How was the 780k understanding data composed and filtered? What is the distribution across datasets? Are any validation or test scenes from SQA3D/ScanQA/ScanRefer included in training?
- In Table 4, the unified texture+geometry architecture performs worse than separate modules. What is the suspected reason and what architectural changes would recover performance?
- Why is λ_geo set to 0.1? What is the sensitivity of results to this weight?
- Does stage 2 fine-tuning affect understanding performance? If so, is there degradation or improvement?

### Limitations

- The geometry module relies on synthetic depth maps from the Voyager pipeline, which lack absolute metric scale and may not generalize to real-world scenes, limiting absolute distance estimation and real-world geometric accuracy.
- The model is limited to short-range generation (25 frames) and cannot produce long, consistent 3D world sequences.
- 3D visual grounding (e.g., referring object localization) is not evaluated, and the paper notes this as future work.
- The paper does not analyze failure modes in complex real-world scenes beyond a single qualitative bad case.
- The method requires multiview images as input, which may not be available in many practical scenarios.
- Evaluation is largely confined to indoor scenes (Re10k, ScanNet, SQA3D); generalization to outdoor or dynamic scenes is unclear.
- The main claim that generation facilitates understanding is confounded by the addition of extra video data in Omni-View compared to BAGEL-FT, so the true effect of generative objectives is not isolated.
- No analysis of computational resource requirements (GPU-hours, memory, inference speed) is provided, hindering practical reproducibility.
- Potential negative societal impacts are acknowledged only generically, with no concrete discussion of safeguards against synthetic scene misuse or biases.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 61,993
- Cache-hit prompt tokens: 3,840
- Cache-miss prompt tokens: 58,153
- Completion tokens: 24,099
- Reasoning tokens reported: 16,535
- Total tokens: 86,092
- Estimated total: $0.01489989

Full individual reviews and raw JSON responses are in `review_bundle.json`.
