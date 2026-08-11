# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B134.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.018567**

## Final Meta-review

The paper introduces ProteinZero, an online reinforcement learning framework for protein inverse folding that enables continuous self-improvement without curated preference datasets. Key contributions include: (1) efficient proxy reward models using ESMFold for structural designability and a novel rapid ddG predictor based on inverse folding likelihood ratios, achieving 25-760x speedups in reward computation; (2) an embedding-level diversity regularization that prevents mode collapse while promoting sequence diversity; and (3) systematic exploration of the RL design space comparing GRPO, RAFT, and DPO algorithms. Experiments on CATH-4.3 demonstrate consistent improvements over ProteinMPNN, ESM-IF, and InstructPLM across structural accuracy, stability, diversity, and success rate metrics, with failure rate reductions of 36-48%. The framework completes RL training in under 3 days on a single 8-GPU node.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 3.400 | 0.490 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.200 | 0.400 | 3-4 |
| Overall | 6 | 6.200 | 0.400 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important and timely problem: data scarcity in protein inverse folding and misalignment between supervised training objectives and real-world design goals
- Makes online RL tractable for protein design through efficient proxy rewards (25-760x speedup), a significant practical contribution
- Novel embedding-level diversity regularization that prevents mode collapse and outperforms sequence-level alternatives
- Comprehensive experimental evaluation with multiple metrics, multiple baselines, and thorough ablation studies across reward formulations, objective components, and diversity strategies
- Demonstrates stable multi-round self-improvement over 20 iterations, addressing a key limitation of prior single-round RL approaches
- Clear and well-organized presentation with useful ablation tables and qualitative case studies
- Reproducibility details provided including hyperparameters, hardware, and training time

### Weaknesses

- The proposed ddG predictor is a heuristic based on likelihood ratios and lacks rigorous validation against experimental stability measurements or established computational predictors; its reliability as a reward signal is uncertain
- Evaluation relies entirely on computational proxies (ESMFold, FoldX, AlphaFold3) without any wet-lab experimental validation, limiting the biological significance of the claims
- The evaluation is partially self-referential: ESMFold is used both for the TM-score reward and for evaluation metrics, potentially biasing results favorably
- The improvements over the base model are relatively modest in absolute terms (e.g., recovery 0.574→0.590, success rate 84.45%→90.13%), and the '36-48% failure rate reduction' is a relative metric that may exaggerate practical significance
- The DPO baseline comparison may be unfair since DPO is offline and run for only 20 epochs, while online methods run for 20 iterations with continuous data generation
- The diversity regularization operates on the current policy's decoder activations, which change during training, creating a moving target; its long-term stability and correlation with functional diversity are not demonstrated
- In some cases (150-300 residues), removing the diversity term slightly improves success rate, creating tension with the paper's emphasis on diversity as essential
- Limited discussion of potential reward hacking or exploitation of ESMFold and the ddG proxy during online RL
- No comparison with more recent inverse folding baselines (e.g., ESM3 or 2024-2025 methods)

### Questions

- Can you provide validation of the proposed ddG predictor against experimental ΔΔG values (e.g., ProTherm) or established computational methods (e.g., FoldX, Rosetta, DDGun, DeepDDG)? A correlation analysis would strengthen confidence in this reward.
- How sensitive are the results to the specific success rate thresholds (scRMSD < 2Å, FoldX ddG < 0)? Would relative improvements hold with stricter criteria?
- Have you investigated whether the improvements generalize to proteins outside the CATH-4.3 distribution, such as membrane proteins, designed proteins from RFdiffusion, or larger benchmarks?
- How does the performance degrade or improve with more RL iterations (e.g., 50 or 100)? Is there evidence of overfitting to reward models or reward hacking?
- The KL weight of 0.1 is higher than typical GRPO settings. What is the actual KL divergence between the final and reference policies? Could improvements be attributed primarily to the KL weight and LoRA fine-tuning rather than the RL framework itself?
- How does the DPO baseline compare if given a comparable training budget (e.g., 20 iterations of data generation and preference collection)?
- Does the embedding-level diversity regularization actually promote functional diversity, or just sequence diversity? Have you analyzed conserved functional sites or other functional properties of diverse sequences?
- What is the wall-clock time breakdown for the 150-300 residue category (274 hours)? How much is reward computation vs. training?
- How does the framework perform when fine-tuning from a different base model (e.g., ProteinMPNN or ESM-IF) instead of InstructPLM? Is it architecture-agnostic?

### Limitations

- The ddG surrogate's physical validity is questionable; it is a likelihood-based heuristic that has not been validated against experimental stability data
- Evaluation relies entirely on computational structure prediction and energy functions which have known limitations; no wet-lab experiments validate the designed proteins
- The framework is demonstrated only on monomeric proteins up to 300 residues; extension to multimers, protein-protein interactions, or larger proteins is not addressed
- The diversity regularization operates on the decoder's embedding space which is model-specific and may not transfer to other architectures
- Potential reward hacking and proxy reward exploitation are not fully characterized
- The paper does not adequately address potential negative societal impacts, including dual-use concerns for designing toxins or bioweapons
- The computational cost, while reduced, is still substantial (up to 274 hours for 150-300 residue proteins), which may limit accessibility for smaller research groups

### Ethics

Ethical concerns flagged: **True**

## Usage and Cost

- Requests: 6
- Prompt tokens: 118,813
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 109,853
- Completion tokens: 11,295
- Reasoning tokens reported: 0
- Total tokens: 130,108
- Estimated total: $0.01856711

Full individual reviews and raw JSON responses are in `review_bundle.json`.
