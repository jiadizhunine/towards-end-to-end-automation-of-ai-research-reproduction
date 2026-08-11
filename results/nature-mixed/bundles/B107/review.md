# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B107.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.023363**

## Final Meta-review

The paper proposes FORMED, a framework for repurposing pre-trained time series foundation models (specifically TimesFM) for medical time series (MedTS) classification. FORMED freezes the backbone and introduces a novel attention-based classifier comprising task-specific channel embeddings (CEs), label queries (LQs), and a shared decoding attention (SDA) layer. The framework operates in three stages: pre-training (already done), repurposing (jointly training the classifier on a cohort of 5 MedTS datasets to capture domain knowledge), and adapting (training only lightweight task-specific parameters for new datasets). The paper evaluates FORMED against 15 baselines (11 task-specific models and 4 task-specific adaptation methods) on 5 MedTS datasets (EEG and ECG), reporting improvements in F1-score, with up to 35% absolute improvement on ADFTD. It also demonstrates adaptation to 2 out-of-domain datasets (ECG200, StandWalkJump) with limited training data. The paper includes ablation studies and extended baseline comparisons.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.600 | 0.490 | 3-4 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 3 | 3.200 | 0.400 | 3-4 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 2.800 | 0.400 | 2-3 |
| Presentation | 3 | 3.200 | 0.400 | 3-4 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 5.800 | 0.980 | 4-7 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- The problem is well-motivated: medical time series classification faces significant heterogeneity challenges across datasets, and the paper clearly articulates these challenges.
- The architectural design is novel and principled: separating task-agnostic (shared decoding attention) from task-specific (channel embeddings, label queries) knowledge enables efficient adaptation to new datasets with variable channel/class configurations.
- Comprehensive evaluation: 5 datasets, 15 baselines, multiple metrics, and ablation studies provide a thorough assessment.
- Significant performance improvements are reported on several datasets (e.g., ADFTD, PTB-XL), suggesting the approach has practical potential.
- The three-stage framework (pre-training, repurposing, adapting) is clearly conceptualized and well explained.
- Code is publicly available, supporting reproducibility.

### Weaknesses

- Extremely high variance in FORMED's results (e.g., ADFTD F1 = 63.66±21.67, APAVA F1 = 82.45±12.6) raises serious concerns about the reliability and statistical significance of the claimed improvements. No significance testing (e.g., paired t-tests, confidence intervals) is provided.
- Only one backbone (TimesFM) is evaluated. The claim of a generalizable 'repurposing foundation models' framework is not validated across other foundation models (e.g., MOMENT, UniTS, PatchTST).
- The comparison with TSA baselines may be unfair: FORMED uses a sophisticated attention-based classifier while TSA baselines use simple CNN/MLP heads. The performance gain could be partly attributed to the classifier architecture rather than the repurposing strategy.
- Adaptation experiments are limited to only 2 small out-of-domain datasets (ECG200 with ~100 samples, StandWalkJump with ~27 samples), which may not represent diverse real-world MedTS scenarios. FORMED underperforms baselines at small k values and only shows clear improvements at large k.
- The 'power law' scaling claim with k is not rigorously demonstrated (no formal fitting or hypothesis testing).
- Computational cost of the repurposing stage (training a 500M-parameter backbone on 340K samples for 100 epochs) is not reported, which is important for practical feasibility.
- No comparison with recent specialized cross-data MedTS models (e.g., BIOT) that are designed for similar settings.
- The paper does not discuss potential negative societal impacts, such as risks of misdiagnosis in clinical deployment or bias in medical datasets.

### Questions

- Given the very high variance in FORMED's results (e.g., ±21.67 F1 on ADFTD), can the authors provide statistical significance tests (e.g., paired t-tests or confidence intervals) to confirm that FORMED's improvements over baselines are statistically significant?
- How many random seeds and data splits were used? Is the high variance primarily due to data splits, initialization, or training instability? Could variance reduction techniques (e.g., ensembling) mitigate this?
- Why was TimesFM-TSA (with CNN head) chosen as the primary TSA baseline? Would a fairer comparison use the same attention-based classifier head for both FORMED and TSA, isolating the contribution of the joint repurposing training?
- How does FORMED perform with other backbone foundation models (e.g., MOMENT, UniTS, PatchTST)? The paper only evaluates TimesFM, so it is unclear if the framework benefits are specific to TimesFM or generalizable.
- What is the computational cost (GPU hours, memory) of the repurposing stage? This is important for practical adoption.
- How does FORMED compare with BIOT (Biosignal Transformer for Cross-data Learning), which is specifically designed for cross-dataset medical time series learning?
- In the adaptation experiments, FORMED underperforms TimesFM-TSA at small k values. What is the practical recommendation for choosing k for a new dataset? Is there a way to determine the optimal k without extensive grid search?
- The paper claims a 'power law' improvement with k but does not provide theoretical justification or thorough analysis. Can the authors elaborate on this?
- How sensitive is FORMED to the composition of the repurposing cohort (e.g., adding/removing datasets, balancing EEG vs ECG)? Is there a minimum cohort size needed for the SDA to learn useful domain knowledge?
- How does FORMED handle class imbalance in the datasets? Are the reported F1 scores macro-averaged?

### Limitations

- Only one backbone foundation model (TimesFM) is evaluated, limiting the generalizability of the 'repurposing foundation models' claim.
- The repurposing cohort is limited to 5 datasets (2 ECG, 3 EEG), which may not capture the full diversity of MedTS data. The impact of cohort composition/scale is not thoroughly investigated.
- Extremely high variance in FORMED's results (sometimes exceeding ±20% on key metrics) raises concerns about reliability for clinical deployment.
- Adaptation experiments are limited to 2 small out-of-domain datasets, which may not represent the full range of inter-dataset heterogeneity in real clinical settings.
- No analysis of failure cases or error patterns; no discussion of model interpretability or explainability, which is important for clinical acceptance.
- No discussion of potential negative societal impacts, such as risks of misdiagnosis or bias in medical datasets.
- Computational cost of the repurposing stage is not reported, which is important for practical adoption.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 151,032
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 142,072
- Completion tokens: 12,312
- Reasoning tokens reported: 0
- Total tokens: 163,344
- Estimated total: $0.02336253

Full individual reviews and raw JSON responses are in `review_bundle.json`.
