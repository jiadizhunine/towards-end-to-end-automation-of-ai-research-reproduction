# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B110.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.012612**

## Final Meta-review

This paper introduces ProtoMM, a self-supervised learning framework for multimodal time-series biosignals (PPG and accelerometry). The method extends SwAV's swapped prediction mechanism to multiple modalities by using a shared prototype dictionary, enabling alignment without explicit negative sampling. The framework captures both within-modality (unique) and between-modality (shared) information through a balanced Multimodal Prototype Prediction loss. The authors evaluate ProtoMM on three datasets across six tasks (stress detection, activity recognition, heart rate prediction), demonstrating superior performance over CLIP-style, contrastive, and other multimodal SSL baselines. The paper also provides qualitative analysis showing that learned prototypes capture semantically meaningful physiological patterns.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.200 | 0.400 | 3-4 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.200 | 0.400 | 3-4 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 5.800 | 0.400 | 5-6 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Clear motivation addressing a real limitation of contrastive multimodal methods (false negatives, over-alignment) for complementary modalities
- Technically sound extension of SwAV to multimodal settings with a clean mathematical formulation
- Comprehensive experimental evaluation across 3 datasets and 6 downstream tasks with consistent experimental setup and multiple strong baselines
- Well-designed ablation studies (α parameter, unimodal vs multimodal) that validate the design choices
- Interpretability analysis via prototype visualization adds value beyond standard SSL methods
- Detailed reproducibility information with hyperparameters provided
- Between-modal knowledge transfer analysis provides interesting insights

### Weaknesses

- Methodological novelty is limited - essentially a straightforward multi-view extension of SwAV to multimodal settings
- No statistical significance testing or confidence intervals reported; unclear if performance gains are consistent across seeds
- Performance improvements over strongest baselines are modest in several tasks
- Limited evaluation depth: only linear probing is used, no fine-tuning experiments
- Pretraining data is relatively small (122 participants, 10 days) for a claimed 'foundation model'
- No sensitivity analysis for number of prototypes P, temperature τ, or Sinkhorn iterations
- The result that unimodal SimCLR outperforms ProtoMM Within-Mod is not deeply analyzed or explained
- Interpretability analysis is qualitative only - no quantitative metrics for prototype quality
- No comparison with more recent prototype-based SSL methods (e.g., DINO, MSN)
- No discussion of computational cost or training time compared to baselines
- Limited investigation of scaling to more than 2 modalities

### Questions

- How sensitive is ProtoMM's performance to the number of prototype vectors P? Was any hyperparameter search performed for P?
- Why does unimodal SimCLR consistently outperform ProtoMM Within-Mod? This seems to contradict the method's motivation. Could you provide more analysis or theoretical justification?
- Can you disentangle the contribution of the prototype mechanism from the swapped prediction loss itself? Would a version of SLIP with swapped prediction (without prototypes) perform similarly?
- Are the performance differences between ProtoMM and the best baselines statistically significant? Please provide confidence intervals or significance tests across multiple seeds.
- How does the method scale to more than two modalities (e.g., adding ECG or EDA)? Would the between-modality loss scale combinatorially?
- What is the effect of α values other than 0, 0.5, and 1? Is there a sweet spot or does performance vary smoothly?
- How does the choice of Sinkhorn-Knopp iterations and temperature affect training stability and final performance?
- Have you compared against more recent prototype-based methods like DINO or MSN?
- What is the computational overhead of ProtoMM compared to baselines in terms of training time and memory?
- Could you provide quantitative metrics for the interpretability analysis (e.g., prototype purity, clustering quality)?
- Why does ProtoMM show particularly large improvements on WESAD (24.6% F1 improvement for 4-class stress) compared to other datasets?
- The conclusion mentions 'twelve state-of-the-art baselines' but the experiments evaluate 7 baselines. Can this discrepancy be clarified?

### Limitations

- The method is only evaluated on PPG and accelerometry - generalization to other modality combinations (ECG, EDA, EEG) is untested
- The pretraining dataset is limited to 122 participants from a single study (MOODS), potentially limiting generalization claims
- All downstream evaluations use linear probing only, not fine-tuning, which may not reflect full representation quality
- No statistical significance testing or confidence intervals reported, making it difficult to assess reliability of improvements
- The interpretability analysis is qualitative and somewhat superficial; quantitative metrics would strengthen claims
- The paper doesn't deeply investigate why prototypes work better for multimodal alignment specifically, given that unimodal results show prototypes are worse than SimCLR
- Potential privacy concerns with physiological data collection and modeling, though the authors acknowledge this in the ethics section
- The paper doesn't address potential biases in the pretraining data (e.g., demographic distribution) that could affect downstream performance on underrepresented groups

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 79,732
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 70,772
- Completion tokens: 9,568
- Reasoning tokens reported: 0
- Total tokens: 89,300
- Estimated total: $0.01261221

Full individual reviews and raw JSON responses are in `review_bundle.json`.
