# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B188.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **5/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 1, 'Reject': 4}
- Estimated API cost: **$0.016852**

## Final Meta-review

This paper introduces 'vericoding' — the task of generating formally verified code (implementation + proof) from formal specifications — and presents the largest benchmark to date for this task. The benchmark contains 12,504 formal specification tasks across three verification languages: Dafny (3,029 tasks), Verus/Rust (2,334 tasks), and Lean (7,141 tasks), with 6,174 being new unseen problems. The benchmark is constructed by curating existing sources (DafnyBench, VerifiedCogen, Verina, CLEVER, APPS, HumanEval, FVAPPS, NumPy docs, BigNum) and translating specifications across languages using LLMs with a conversational repair loop. The authors evaluate 9 off-the-shelf LLMs (GPT-5, Claude, Gemini, etc.) with a repair loop of up to 5 attempts, reporting success rates of 82% for Dafny, 44% for Verus, and 27% for Lean (model union). They also report that adding natural language descriptions does not significantly improve performance, and document rapid progress in formal verification (DafnyBench improved from 68% to 96% over the past year). The paper includes quality assessment, cheating detection mechanisms, and analysis of difficulty factors. The benchmark and results are publicly released.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 2 | 2.400 | 0.490 | 2-3 |
| Clarity | 3 | 2.600 | 0.490 | 2-3 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 2 | 2.400 | 0.490 | 2-3 |
| Presentation | 3 | 2.600 | 0.490 | 2-3 |
| Contribution | 3 | 3.200 | 0.400 | 3-4 |
| Overall | 5 | 5.200 | 0.980 | 4-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The benchmark is by far the largest vericoding benchmark to date, with 12,504 tasks across three verification languages (Dafny, Verus, Lean), filling a significant gap in the field.
- Multi-language coverage enables cross-language comparison and research across different verification paradigms (ATP vs. ITP).
- Comprehensive evaluation with 9 different LLMs provides valuable baseline results for the community.
- The authors are transparent about benchmark limitations, including weak specs and translation issues discovered through manual inspection.
- The paper includes thoughtful quality control measures: LLM-as-judge validation, manual inspection, quality scoring, and systematic cheating detection.
- The temporal comparison showing verification progress (68% to 96% on DafnyBench) is valuable for tracking LLM improvement.
- Reproducibility is addressed with detailed prompts, hyperparameters, and scripts in the supplementary material.

### Weaknesses

- Benchmark quality is a major concern: the authors admit ~9% of successful specs are 'too weak' and ~15% have 'poor translations,' which undermines the reliability of reported success rates as measures of true vericoding capability.
- The LLM-based translation pipeline and 'LLM-as-judge' validation are not rigorously validated (no inter-annotator agreement, no comparison with human judges), so systematic biases may be introduced.
- The claim that adding natural language descriptions does not improve performance is based on only one small dataset (Verina, 157 tasks) and lacks statistical significance testing.
- The 'model union' results are prominently presented but represent an oracle-like ensemble that is not practically deployable, potentially overstating achievable performance.
- Some benchmark sources have very high near-duplicate rates (e.g., BigNum Dafny at 98.4%), and the quality metrics table reveals concerning issues (e.g., BigNum Lean quality score 18.3 with 49 sorry definitions).
- The paper does not systematically compare against existing benchmarks (e.g., CLEVER, VERINA, DafnyBench) on their original tasks, making it hard to calibrate the difficulty of new tasks.
- The experimental analysis is relatively shallow — mostly success rates without deep failure analysis or investigation of why models fail on specific tasks.
- Presentation issues: Table 3 is nearly unreadable due to formatting, some appendix prompts are referenced but not shown, and there are grammatical errors throughout.
- The inclusion of tasks with incomplete, inconsistent, or non-compilable specs conflates spec repair with vericoding ability and complicates cross-source comparisons.

### Questions

- How do the reported success rates change when excluding tasks with 'weak specs' or 'poor translations'? Would the 82% Dafny success rate drop significantly if only high-quality specs were considered?
- What was the inter-annotator agreement for the manual inspection? How reliable is the 9%/15% estimate of weak/poorly-translated specs?
- How was the 'LLM-as-judge' validation approach itself validated? What is the agreement rate between LLM judges and human judges? Could the LLM judge be biased toward accepting its own translations?
- For the 'no improvement from natural language descriptions' claim, why was the experiment only conducted on Verina (157 tasks)? What statistical test was used, and would the conclusion hold on more complex tasks?
- How exactly is the 'model union' metric computed? Is it the fraction of tasks solved by at least one model, and does this represent an oracle that requires perfect model selection in practice?
- What is the distribution of task difficulty across the benchmark? Are most tasks simple single-function problems, and how does the benchmark scale to more complex, multi-function verification?
- Why is the FVAPPS benchmark (4,006 tasks) treated separately from the main Lean results? What would the Lean success rate be excluding FVAPPS?
- How do the success rates on this benchmark compare to existing benchmarks (e.g., DafnyBench, CLEVER, VERINA) for the same tasks? This would help calibrate the difficulty of new tasks.
- The paper mentions using ghost functions in Dafny/Verus to mitigate implementation leakage. Can you elaborate on how this works and its limitations?
- Could you clarify the exact token/compute costs for running the full benchmark evaluation? The paper mentions $25,000 on OpenRouter — is this reproducible for other researchers?
- The prompts in Appendix 1.3 appear to be missing. Could you provide the actual prompts used for code generation and repair in each language?

### Limitations

- The benchmark has significant quality issues: ~9% of specs are 'too weak' and ~15% have 'poor translations,' which limits the reliability of the reported results and the benchmark's usefulness for tracking LLM progress in vericoding.
- The vericoding task formulation excludes spec generation, which is acknowledged as an important part of the verification workflow.
- The benchmark focuses on relatively small, single-function programs (typically under 100 lines), limiting its applicability to real-world software verification.
- The evaluation is limited to a simple repair loop without advanced techniques (tree search, RL, fine-tuning), so results may underestimate potential LLM capabilities.
- The paper does not deeply analyze failure modes — why LLMs fail on specific tasks — which would be valuable for improving vericoding approaches.
- The computational cost of running the full benchmark is significant (reported $25,000 on OpenRouter), which may limit reproducibility for many researchers.
- The benchmark includes tasks from sources with different licenses, which may complicate redistribution and use by others.
- The paper does not address potential negative societal impacts beyond carbon emissions, such as over-reliance on AI-generated verified code or the potential for malicious use of verification tools.
- The dependence on LLM-based translation and validation may introduce systematic biases that are not fully characterized, potentially affecting the validity of cross-language comparisons.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 106,381
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 97,421
- Completion tokens: 11,385
- Reasoning tokens reported: 0
- Total tokens: 117,766
- Estimated total: $0.01685183

Full individual reviews and raw JSON responses are in `review_bundle.json`.
