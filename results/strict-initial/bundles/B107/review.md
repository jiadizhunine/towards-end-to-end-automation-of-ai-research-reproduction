# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B107.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.027002**

## Final Meta-review

The paper proposes FORMED, a framework that repurposes a frozen pre-trained time-series foundation model (TimesFM) for medical time-series classification. It introduces a trainable attention-based classifier with task-specific channel embeddings and label queries, and a shared decoding attention layer jointly trained across five MedTS datasets in a repurposing stage. New datasets are adapted by learning only task-specific channel embeddings and label queries. Experiments on five in-domain datasets and two out-of-domain datasets report substantial gains over task-specific and task-specific-adaptation baselines.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 2 | 2.800 | 0.400 | 2-3 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 2 | 2.600 | 0.490 | 2-3 |
| Significance | 2 | 2.200 | 0.400 | 2-3 |
| Soundness | 2 | 2.200 | 0.400 | 2-3 |
| Presentation | 2 | 2.600 | 0.490 | 2-3 |
| Contribution | 2 | 2.200 | 0.400 | 2-3 |
| Overall | 4 | 4.000 | 0.000 | 4-4 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The repurposing paradigm is a timely and conceptually clean approach to enable a single foundation model to handle heterogeneous medical time-series tasks with varying channels, classes, and lengths.
- The architecture with channel embeddings, label queries, and shared decoding attention naturally accommodates variable input/output configurations and is a reasonable design for cross-dataset generalization.
- Empirical evaluation is broad in terms of datasets and baselines, with patient-independent splits and multiple metrics.
- The adaptation-stage analysis with varying k demonstrates a useful scaling behavior and suggests data-efficient adaptation to new tasks.
- The paper reports strong improvements on several datasets, notably ADFTD, PTB, and PTB-XL.

### Weaknesses

- Only a single foundation model (TimesFM) is tested, so the claim that FORMED is a general repurposing framework is not well supported.
- No ablation studies isolate the contributions of the shared decoding attention, channel embeddings, label queries, the frozen backbone, or the multi-task repurposing stage, leaving the source of gains unclear.
- The comparison to task-specific adaptation (TSA) baselines appears weak; no strong parameter-efficient methods such as LoRA, adapters, or prompt tuning are included, and no medical time-series foundation model such as BIOT is compared.
- Statistical significance is not assessed; several results show very large standard deviations (e.g., APAVA, TDBrain), making it unclear whether improvements are reliable.
- The in-domain comparison is confounded because FORMED is jointly repurposed on all five datasets, including the evaluation dataset, while TSM/TSA baselines are trained per dataset; no multi-task baseline with per-task heads is included.
- The out-of-domain adaptation is limited to two small datasets (one non-medical), and performance is highly sensitive to hyperparameter k, with underperformance at small k and non-monotonic scaling on StandWalkJump.
- The claimed adaptation with only 0.1% of parameters is not substantiated; for large k (e.g., 512 or 1024), the number of trainable parameters is likely much higher, and no exact counts or calculation method are provided.
- Potential contamination of the pre-training corpus with ECG200 or StandWalkJump is not discussed, which would weaken the out-of-domain generalization claim.

### Questions

- What is the exact number of trainable parameters in the repurposing and adapting stages, and how is the 0.1% figure computed for the k values used in practice?
- How would FORMED compare to linear probing, LoRA, adapters, or prompt tuning on the same frozen TimesFM backbone, and to stronger baselines like BIOT?
- Can the authors provide ablation results that remove each component (SDA, CEs, LQs) and that replace the shared decoder with a task-specific decoder, or that use a randomly initialized SDA without repurposing?
- Were ECG200 and StandWalkJump or similar signals part of TimesFM's pre-training data? If not, what evidence supports that they are truly unseen?
- Are the reported improvements statistically significant given the large standard deviations, and were any paired significance tests performed?
- How was k=16 chosen for repurposing, and how do repurposed model quality and adaptation performance vary as a function of k during repurposing?
- Why does FORMED underperform iTransformer-TSA on APAVA in AUROC and AUPRC, and why does it underperform Medformer on TDBrain in F1?
- Is the comparison fair given that FORMED sees all five datasets during repurposing while baselines are per-dataset? What happens if baselines are jointly trained on the five-dataset cohort?

### Limitations

- The framework is validated with only TimesFM as the backbone; generality to other time-series foundation models is not demonstrated.
- No ablation or systematic study isolates the contribution of each proposed component, so the method's design is not fully justified.
- Out-of-domain evaluation is limited to two small, non-representative datasets, and StandWalkJump is not a medical task, limiting the strength of generalization claims.
- The hyperparameter k is chosen arbitrarily during repurposing and strongly influences adaptation performance; no sensitivity analysis is provided.
- The paper does not provide code, training time, compute cost, or total parameter counts, hindering reproducibility and assessment of efficiency.
- Potential contamination of the pretraining corpus is not addressed, especially for ECG200 and StandWalkJump.
- No analysis of calibration, fairness, subgroup performance, failure cases, or clinical risks is included, which is important for medical applications.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 145,698
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 141,602
- Completion tokens: 25,595
- Reasoning tokens reported: 19,139
- Total tokens: 171,293
- Estimated total: $0.02700235

Full individual reviews and raw JSON responses are in `review_bundle.json`.
