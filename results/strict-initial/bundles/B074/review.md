# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B074.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.018137**

## Final Meta-review

The paper proposes an out-of-core training and rendering framework for large-scale 3D Gaussian Splatting on a single consumer GPU without spatial partitioning. Gaussian data is stored in CPU memory, and a hierarchical Level-of-Detail (LoD) representation combined with Sequential Point Trees (HSPT) streams only view-relevant Gaussians to the GPU. The method introduces hierarchy densification during training, GPU caching with view scheduling, and is evaluated on synthetic MatrixCity and real street-level H-3DGS datasets, showing improved quality over chunk-based baselines on multi-scale scenes and reduced GPU memory usage.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.800 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 2.600 | 0.490 | 2-3 |
| Significance | 4 | 3.800 | 0.400 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 2.600 | 0.490 | 2-3 |
| Contribution | 4 | 3.600 | 0.490 | 3-4 |
| Overall | 7 | 6.600 | 1.020 | 5-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The HSPT data structure is an original and effective combination of Gaussian hierarchies and Sequential Point Trees, enabling fast parallel LoD cuts with modest GPU memory overhead.
- The out-of-core streaming design with caching and view scheduling is a practical approach to training and rendering very large 3DGS scenes on a single consumer GPU without chunking artifacts.
- The proposed hierarchy densification strategy allows the LoD tree to evolve during training, which prior methods avoided by building hierarchies post hoc.
- The method achieves strong quantitative results on the large-scale MC-small-city+ dataset, outperforming chunk-based baselines that require substantially more GPU memory or run out of memory.
- The paper includes detailed ablations, memory analyses, and implementation descriptions, which support reproducibility despite some missing details.

### Weaknesses

- The theoretical soundness of the conservative distance bound in HSPT is questioned: the triangle inequality argument as presented does not necessarily guarantee the claimed bound, which could affect LoD cut validity.
- The main evaluation relies on synthetic MatrixCity; real-world validation is limited to smaller street-level datasets, and on Mill19 (uniform-scale aerial views) the method underperforms simpler baselines, weakening the claim of general superiority.
- The consumer-GPU claim is only partially substantiated: training is done on a 24GB RTX 3090, but rendering uses up to 25GB VRAM on an H200; it is unclear how the full model is rendered on 24GB VRAM.
- Baseline comparisons are not fully apples-to-apples: some baselines require modified configurations or are disadvantaged by initializations (e.g., H-3DGS with COLMAP-generated points), and several baselines OOM on the largest dataset.
- The paper is incomplete in places: missing figures, pseudocode, and references, along with typos, make the technical description harder to follow and verify.
- Several components (cache size, distance ratio tolerance, view scheduling, stochastic noise) rely on heuristics whose impact on final quality is not rigorously analyzed, and wall-clock training times are not reported.

### Questions

- Can the authors provide a formal proof or a counterexample for the M_d conservative bound? The current triangle inequality argument does not appear to guarantee m_d(i) <= ||mu_i - p_cam|| under the stated assumptions.
- How is rendering performed within 24GB VRAM if the reported rendering VRAM for MC-small-city+ is 25.0GB? Is the consumer-GPU claim only for training, or can the full model be interactively rendered on a 24GB GPU at an appropriate LoD?
- What are the total wall-clock training times for the main experiments compared to baselines? Per-iteration times alone do not establish end-to-end efficiency.
- What happens when the CPU RAM is insufficient or the hierarchy must be partially swapped to disk? How does this affect training time and final quality?
- Why do H-3DGS and OctreeGS OOM on a 141GB H200 even though they use chunking or LoD? Could tuning their configurations allow them to run, and how would the comparison change?
- How sensitive are the results to the cache size, distance ratio tolerance, and view scheduling hyperparameters? Is there a risk of overfitting to the guided view schedule?
- The hierarchy densification can create unreachable Gaussians where a child becomes larger than its parent. How does this affect LoD cut quality and training stability, and is there a rebalancing strategy?

### Limitations

- The method requires approximately 1GB of CPU RAM per million Gaussians, so scalability is still limited by available RAM; disk loading is about 10x slower.
- Initialization relies on accurate camera poses and sparse point clouds, which are difficult to obtain for real-world city-scale scenes; noisy or incomplete SfM reconstructions can degrade quality.
- The guided view scheduling introduces training bias; random-view injection is a heuristic without formal convergence guarantees.
- The LoD hierarchy provides little benefit for scenes with a single viewing scale (e.g., same-height aerial imagery) and can even cause overhead compared to chunk-based methods.
- Frustum culling becomes ineffective when the entire scene is inside the frustum, and occlusion culling is not implemented.
- The paper does not address dynamic scenes, appearance changes, or significant exposure variation, limiting applicability.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 80,867
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 76,771
- Completion tokens: 26,348
- Reasoning tokens reported: 19,497
- Total tokens: 107,215
- Estimated total: $0.01813685

Full individual reviews and raw JSON responses are in `review_bundle.json`.
