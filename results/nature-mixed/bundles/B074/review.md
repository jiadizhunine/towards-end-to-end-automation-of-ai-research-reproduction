# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B074.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **8/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.014162**

## Final Meta-review

The paper introduces 'A LoD of Gaussians', a framework for training and rendering ultra-large-scale 3D Gaussian Splatting scenes on a single consumer-grade GPU without scene partitioning. The method stores all Gaussian data in CPU RAM and streams only visible Gaussians to GPU memory using a hierarchical Level-of-Detail representation. Key contributions include: (1) a novel hierarchy densification strategy enabling dynamic expansion of Gaussian LoD hierarchies during training, (2) adaptation of Sequential Point Trees (SPTs) into a hierarchical SPT (HSPT) data structure for efficient parallel LoD cut computation, (3) an out-of-core training pipeline with caching and view scheduling exploiting temporal coherence, and (4) extensive evaluation on multi-scale datasets (MatrixCity, H-3DGS, Mill19) showing superior quality over chunk-based baselines while using significantly less VRAM.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 4.000 | 0.000 | 4-4 |
| Quality | 3 | 3.400 | 0.490 | 3-4 |
| Clarity | 3 | 3.400 | 0.490 | 3-4 |
| Significance | 4 | 4.000 | 0.000 | 4-4 |
| Soundness | 4 | 3.600 | 0.490 | 3-4 |
| Presentation | 3 | 3.400 | 0.490 | 3-4 |
| Contribution | 4 | 4.000 | 0.000 | 4-4 |
| Overall | 8 | 7.800 | 0.400 | 7-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses a significant and timely problem: scaling 3DGS to ultra-large scenes without the artifacts and complexity of chunk-based partitioning.
- Novel HSPT data structure effectively combines the correctness of BFS hierarchy traversal with the parallel efficiency of SPTs, enabling practical LoD selection at scale.
- The out-of-core training approach with caching and view scheduling is well-engineered and demonstrates training on consumer GPUs (RTX 3090) for scenes that cause baselines to OOM even on H200.
- Comprehensive evaluation on challenging multi-scale datasets with strong ablations showing the contribution of each system component.
- Honest discussion of limitations, including scenarios where the LoD approach is not beneficial (e.g., single-height aerial datasets).
- Reproducibility is well supported with code and configuration files provided.

### Weaknesses

- The primary benchmark (MatrixCity) is synthetic; real-world results on H-3DGS and Mill19 show mixed performance, with Mill19 worse than baselines.
- No quantitative comparison of total wall-clock training time against baselines; per-iteration overhead is acknowledged but not fully analyzed.
- Requires ~1GB RAM per million Gaussians, which still limits scalability on typical workstations; disk-based storage incurs 10x slowdown.
- The method's advantage is mainly for multi-scale scenes; for uniform view distances, simpler divide-and-conquer approaches are preferable.
- Baseline comparisons are not entirely fair in some cases (e.g., suboptimal COLMAP initialization for H-3DGS, modifications to load images from disk).
- The cache-induced LoD variation is claimed to improve robustness but lacks strong ablation evidence.
- The paper is dense and technically complex, with some sections (e.g., HSPT construction) that could benefit from clearer exposition.

### Questions

- Can you provide a quantitative comparison of total wall-clock training time (not just iterations) against baselines, accounting for the reduced iteration count but longer per-iteration time?
- What is the breakdown of training time between loading, hierarchy cutting, and optimization?
- How sensitive is the method to the HSPT volume threshold parameter 'size'? Is there a principled way to choose it for different scene scales?
- Can you quantify the trade-off between guided view selection bias and random view injection? What evidence supports the claim that cache-induced LoD variation improves robustness?
- What is the impact of 'unreachable Gaussians' (children larger than parents, <10%) on rendering quality and memory efficiency? Could they be pruned more aggressively?
- How does the method scale with system RAM availability? What is the minimum RAM requirement for MC-small-city+?
- How does the method perform with higher SH degrees (e.g., 2 or 3)?
- For the real-world H-3DDS Small City, the improvement over H-3DGS is marginal and SSIM/LPIPS are worse. How do you explain this?
- Have you tested on larger scenes (e.g., full MatrixCity small city) or other real-world multi-scale datasets?
- Could the caching system be extended for asynchronous prefetching in interactive rendering?

### Limitations

- Initialization requires accurate camera poses and sparse point clouds, which remains challenging for real-world large-scale scenes.
- RAM usage of ~1GB per million Gaussians constrains scalability on typical workstations; disk loading incurs 10x slowdown.
- The LoD system is a burden for scenes with uniform view distances (e.g., single-height aerial datasets), where simpler chunk-based methods perform better.
- Individual training iterations are slower due to CPU-GPU transfer and hierarchy cuts, though fewer iterations are needed.
- Frustum culling is ineffective when the entire scene is in view; occlusion culling is suggested as future work.
- The paper does not discuss potential negative societal impacts, such as privacy concerns in urban scene reconstruction or surveillance applications.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 90,046
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 81,086
- Completion tokens: 9,945
- Reasoning tokens reported: 0
- Total tokens: 99,991
- Estimated total: $0.01416173

Full individual reviews and raw JSON responses are in `review_bundle.json`.
