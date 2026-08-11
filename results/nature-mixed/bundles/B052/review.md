# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B052.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.027459**

## Final Meta-review

The paper introduces OmniPlay, an interactive benchmark for evaluating omni-modal fusion and reasoning capabilities of agentic foundation models. The benchmark comprises five game environments designed around principles of modality complementarity, controlled modality conflict, and variable modality complexity. The authors evaluate six leading omni-modal models (Gemini 2.5 Pro/Flash, Qwen-2.5-Omni, MiniCPM-o-2.6, Baichuan-Omni-1.5, VITA-1.5) against human expert and random baselines. Key findings include: (1) a dichotomy between superhuman memory performance and sub-par reasoning/strategic planning, (2) catastrophic performance degradation under modality conflict, and (3) a counter-intuitive 'less is more' phenomenon where removing sensory information can improve performance for models with weaker fusion mechanisms. The paper also conducts diagnostic experiments including modality ablation, conflict, substitution, noise robustness, and aided reasoning.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.600 | 0.490 | 3-4 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 4 | 3.600 | 0.490 | 3-4 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 3 | 2.800 | 0.400 | 2-3 |
| Presentation | 4 | 3.600 | 0.490 | 3-4 |
| Contribution | 3 | 3.200 | 0.400 | 3-4 |
| Overall | 6 | 5.800 | 0.980 | 4-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel benchmark concept addressing a genuine gap: interactive omni-modal evaluation with diagnostic focus on modality fusion
- Well-designed game suite with systematic manipulation of modality complementarity and conflict
- Comprehensive evaluation across six diverse models (proprietary and open-source) with human and random baselines
- Interesting and potentially impactful findings, especially the 'less is more' paradox and modality conflict fragility
- Detailed diagnostic experiments (ablation, conflict, substitution, noise) provide deeper insights beyond simple performance metrics
- Thorough appendices with full experimental details, prompts, and raw data supporting reproducibility
- Clear writing and well-organized structure

### Weaknesses

- Statistical rigor concerns: no formal significance testing (e.g., t-tests, confidence intervals) to support claims of 'statistically significant' differences
- The 'less is more' finding is based on a single model (MiniCPM-o-2.6) in a single task (Whispered Pathfinding), limiting generalizability
- Potential inconsistency in NPS calculations between main text and appendix raw data (as noted by one reviewer), needs clarification
- Human baseline is small (N=12) and the NPS metric can be unstable when human scores are near the performance floor
- Lack of mechanistic analysis explaining why models fail, beyond descriptive statistics
- Only zero-shot evaluation; no fine-tuning or few-shot analysis
- Limited comparison to existing interactive benchmarks to demonstrate unique diagnostic value
- Some games show floor effects for open-source models, limiting discriminative power

### Questions

- Can you clarify the NPS calculation? The reported NPS values in Table 2 (e.g., 399.2 for Gemini 2.5 Pro on Myriad Echoes Hard) seem inconsistent with raw data in Appendix I. Please provide a worked example.
- How is the audio modality presented to the models? Is it passed as raw audio, transcribed to text, or some other representation? How is video processed in Phantom Soldiers (video stream vs. frames)?
- What statistical tests were used to support claims of 'statistically significant' performance differences? Please provide p-values or confidence intervals for key comparisons.
- The 'less is more' paradox is observed for MiniCPM-o-2.6 in Whispered Pathfinding. Have you tested this across other models and tasks to confirm it's a general pattern?
- How robust is the NPS metric when human baselines are near random performance (e.g., The Alchemist's Melody)? Could the results change with a larger human sample?
- How does OmniPlay compare to existing interactive benchmarks (e.g., ALFWorld, WebArena, BALROG)? Would the same findings be observed in those environments?
- Why does Gemini 2.5 Pro perform poorly on The Alchemist's Melody (20% completion rate)? Is there a task design or prompting issue?
- In modality conflict experiments, how were conflicts instantiated? Were conflicting cues semantically contradictory in a controlled way? Did models show awareness of the conflict?
- For Blasting Showdown, win rates do not sum to 100%. How are draws/ties handled, and what is the tournament structure?
- Have you analyzed attention patterns or internal representations to explain the 'less is more' paradox beyond the 'immature fusion' hypothesis?

### Limitations

- The human baseline is limited to 12 participants with specific demographics; broader cultural and cognitive diversity is not captured.
- The evaluation is zero-shot only; fine-tuning or few-shot performance is not explored, limiting generalizability.
- The benchmark is entirely simulated; real-world omni-modal interaction may involve different challenges.
- The paper does not deeply analyze root causes of failure modes (e.g., why removing image helps MiniCPM-o-2.6); the 'immature fusion' explanation is plausible but not directly evidenced.
- Potential negative societal impact is not discussed, though the risk appears low. The findings about model fragility under conflict could have implications for safety-critical deployments.
- The benchmark may require continuous updates as models improve, and the computational cost of evaluation may limit adoption.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 180,743
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 171,783
- Completion tokens: 12,086
- Reasoning tokens reported: 0
- Total tokens: 192,829
- Estimated total: $0.02745879

Full individual reviews and raw JSON responses are in `review_bundle.json`.
