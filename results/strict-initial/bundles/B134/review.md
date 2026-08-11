# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B134.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.022297**

## Final Meta-review

The paper introduces ProteinZero, an online reinforcement learning (RL) framework for protein inverse folding that enables continuous self-improvement of sequence design models. It proposes efficient proxy rewards: ESMFold-based TM-score for designability and a novel rapid ddG predictor based on backbone-conditioned sequence likelihoods normalized by an unconditional prior. To prevent mode collapse, it uses an embedding-level diversity regularization. ProteinZero is instantiated with GRPO and RAFT and evaluated on CATH-4.3, showing improvements over ProteinMPNN, ESM-IF, InstructPLM, and a DPO baseline across recovery, stability, structural accuracy, diversity, and success rate, with success rates above 90%.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.000 | 0.000 | 2-2 |
| Clarity | 2 | 2.000 | 0.000 | 2-2 |
| Significance | 2 | 2.400 | 0.490 | 2-3 |
| Soundness | 2 | 2.000 | 0.000 | 2-2 |
| Presentation | 2 | 2.000 | 0.000 | 2-2 |
| Contribution | 2 | 2.000 | 0.000 | 2-2 |
| Overall | 4 | 3.800 | 0.400 | 3-4 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important problem: making online RL for inverse folding computationally tractable through efficient proxy rewards (ESMFold TM-score and fast likelihood-based ddG surrogate).
- The embedding-level diversity regularization is a novel approach that helps maintain sequence diversity without sacrificing structural quality, as supported by ablations.
- Comprehensive ablation studies across reward formulations, loss components, and diversity strategies provide useful insights for designing RL fine-tuning for protein models.
- Reported computational speedups (25-760x) over traditional structure prediction and FoldX make online RL potentially accessible to more researchers.
- Evaluation spans multiple complementary metrics (recovery, stability, TM-score, pLDDT, scRMSD, diversity, success rate) and includes FoldX-based success rates rather than only predicted ddG.

### Weaknesses

- The ddG reward surrogate uses p_theta (the policy under training) without a frozen reference, making the reward non-stationary and potentially exploitable by the model inflating its own likelihood rather than improving true stability.
- Structural evaluation metrics in the main results are computed with ESMFold, which is also part of the reward, creating circularity; independent AlphaFold2/3 validation is only qualitative and on few examples.
- The abstract claims the entire CATH-4.3 run completes in under 3 days on an 8-GPU node, but Appendix B.2 reports 274.33 hours (~11.4 days) for the 150-300 residue category alone, a clear contradiction.
- The likelihood-based ddG predictor is not validated against experimental stability data; the reported FoldX ddG values (e.g., -30 to -40 kcal/mol) are implausibly large and not discussed, leaving stability claims uncertain.
- Table 3 shows that removing the diversity term slightly improves overall success rate in both length categories, undermining the claim that diversity regularization is essential; its only clear benefit is sequence diversity.
- The only RL baseline is DPO, which is offline and not a strong representative of recent online RL methods for protein design (e.g., ReFT, AbDPO); no comparison to other online RL methods is provided.
- The paper is poorly written with numerous LaTeX artifacts, redacted citations, broken equation macros, and unclear notation, hindering reproducibility.

### Questions

- In Eq. 4, is p_theta the current online policy or a frozen pretrained model? If it is the current policy, how do you prevent the model from increasing its own likelihood and artificially improving the ddG reward?
- Can the authors reconcile the abstract's 'under 3 days' claim with the reported 274.33 hours for the 150-300 residue category in Appendix B.2? What was the actual total runtime?
- Has the proposed ddG surrogate been validated against experimental ΔΔG values (e.g., S669 or ProTherm) or independently against Rosetta on a held-out set? What is its correlation with FoldX on a large dataset?
- In the diversity regularization, is the cosine similarity computed among sequences generated for the same backbone or across the whole batch? If the batch contains multiple backbones, what is the justification?
- Are the TM-score, PLDDT, and scRMSD evaluation metrics in the main results computed using ESMFold predictions? If so, how do the results change when evaluated with AlphaFold2 on the full test set?
- How many test proteins and random seeds are used in Table 2? How are the means and standard deviations computed?
- How was the DPO baseline compute-matched to ProteinZero? DPO uses 20 epochs of offline training while ProteinZero uses 20 online iterations with generation and reward evaluation; were the total GPU-hours comparable?
- What are the exact values of λ_TM and λ_ddG in the reward function, and was a sensitivity analysis performed over these weights?

### Limitations

- No wet-lab or experimental validation; all designability and stability claims rely on computational proxies (ESMFold, FoldX) that are known to be imperfect.
- The non-stationary ddG reward (depending on the policy being trained) is a potential source of reward hacking and is not discussed.
- The framework is only tested on monomeric CATH-4.3 domains up to 300 residues; multi-chain complexes, antibodies, and larger proteins are not addressed.
- The runtime claim of 'under 3 days' is contradicted by the appendix, raising concerns about the feasibility and reproducibility of the scaling claims.
- The diversity regularization based on hidden activations may be sensitive to architectural changes, and its benefit is not consistent across ablations.
- Potential dual-use risks of AI-generated stable proteins are not discussed in the broader impact section.
- The base model InstructPLM is not widely accessible and its architecture details are not provided, hindering reproduction.

### Ethics

Ethical concerns flagged: **True**

## Usage and Cost

- Requests: 6
- Prompt tokens: 110,513
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 106,417
- Completion tokens: 26,381
- Reasoning tokens reported: 19,431
- Total tokens: 136,894
- Estimated total: $0.02229653

Full individual reviews and raw JSON responses are in `review_bundle.json`.
