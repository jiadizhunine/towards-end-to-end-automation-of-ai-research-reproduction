# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B040.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.015328**

## Final Meta-review

The paper proposes Surf3R, a feedforward multi-view surface reconstruction method that operates without camera poses or calibration. It uses a multi-branch cross-reference fusion transformer to aggregate features across views and predicts per-pixel 3D Gaussians. A D-Normal regularizer is introduced to improve geometric fidelity. Experiments on ScanNet++ and Replica claim state-of-the-art reconstruction accuracy and zero-shot generalization with reconstruction under 10 seconds.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 2 | 2.600 | 0.490 | 2-3 |
| Quality | 2 | 2.000 | 0.000 | 2-2 |
| Clarity | 2 | 1.800 | 0.400 | 1-2 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 2 | 2.000 | 0.000 | 2-2 |
| Presentation | 2 | 1.800 | 0.400 | 1-2 |
| Contribution | 2 | 2.200 | 0.400 | 2-3 |
| Overall | 4 | 3.800 | 0.400 | 3-4 |
| Confidence | 4 | 3.400 | 0.490 | 3-4 |

### Strengths

- Addresses the practically important problem of removing costly SfM preprocessing for multi-view surface reconstruction.
- The multi-branch cross-reference fusion architecture is a reasonable extension to handle wide-baseline sparse views, supported by ablation studies.
- Reports strong quantitative results on ScanNet++ and competitive zero-shot generalization on Replica.
- The method is significantly faster than per-scene optimization baselines, with reconstruction under 10 seconds.
- Ablations confirm the contributions of the multi-branch design and the D-Normal regularizer.

### Weaknesses

- The evaluation protocol is unfair: per-scene optimization methods are evaluated on only 8 ScanNet++ scenes while feedforward methods are evaluated on 50 scenes, making the claimed state-of-the-art statistically questionable.
- The method is not compared to recent feedforward pose-free reconstruction approaches such as MASt3R, VGGT, and FLARE, which also produce geometry; the claim of 'first feedforward pose-free surface reconstruction' is overstated.
- The 'pose-free' claim is ambiguous: mesh extraction via TSDF fusion and novel-view synthesis likely require camera poses, but the paper does not clarify how poses are avoided at inference or evaluation.
- The technical novelty is incremental: the D-Normal regularizer is directly adapted from VCR-GauS, the flattening loss from NeuSG, and the multi-branch design is an extension of DUSt3R.
- The paper contains numerous typos, malformed equations, and missing implementation details (architecture dimensions, loss weights, runtime measurement setup), hindering reproducibility.
- The zero-shot Replica result (F1=41.92) is much lower than ScanNet++ (F1=78.71), indicating limited cross-domain generalization; also, performance drops sharply with fewer views (F1=12.29 at 10 views on Replica).

### Questions

- How are camera poses used at inference when fusing predicted depth maps into a mesh and when rendering novel views? If ground-truth poses are required, in what sense is the method pose-free?
- Why are per-scene baselines evaluated on only 8 ScanNet++ scenes while feedforward methods are evaluated on 50 scenes? Could the results change if evaluated on the same subset?
- How are ground-truth pointmaps generated for training? Do they require known camera poses, contradicting the pose-free claim?
- Can you provide a quantitative comparison against MASt3R, VGGT, and FLARE using the same evaluation protocol?
- What is the exact runtime breakdown and hardware used for the '<10 seconds' claim?
- Why does the final per-view Gaussian prediction come only from the first branch? How do the other M-1 branches influence it during inference?
- What thresholds are used to compute precision, recall, and F1-score for surface reconstruction?

### Limitations

- Training requires ground-truth depth or pointmaps, which typically come from SLAM/SfM with known poses, limiting applicability to datasets with dense 3D supervision.
- The evaluation likely still depends on camera poses for mesh fusion and novel-view synthesis, so the 'pose-free' claim is not fully substantiated.
- The method is only evaluated on indoor scenes (ScanNet++, Replica); generalization to outdoor or large-scale scenes is untested.
- The input resolution of 224x224 may limit fine geometric detail.
- No failure cases or robustness analysis is provided for challenging conditions such as textureless regions, strong occlusions, or dynamic scenes.
- The computational and memory overhead of the multi-branch architecture is not quantified beyond the total runtime.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 70,603
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 66,507
- Completion tokens: 21,449
- Reasoning tokens reported: 15,637
- Total tokens: 92,052
- Estimated total: $0.01532817

Full individual reviews and raw JSON responses are in `review_bundle.json`.
