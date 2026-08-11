# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B149.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.013163**

## Final Meta-review

The paper introduces CodeAlignBench, a benchmark for evaluating instruction-following (IF) capabilities in code generation models. The benchmark is grounded in a user study with 30 developers across Python, Java, and JavaScript, collecting 228 verified real-world developer instructions categorized into cosmetic, structural, and semantic (algorithm, performance, correctness) types. The framework provides an automated pipeline with modular is_applicable/verify functions for each instruction type, supporting two evaluation settings: predefined instructions (embedded in the initial prompt) and follow-up instructions (provided after initial code generation). The authors evaluate 10 LLMs across three proprietary model families (OpenAI, Claude, Gemini), finding that models perform better on follow-up tasks than predefined tasks, structural instructions are easier to follow than semantic or cosmetic ones, and the benchmark reveals significant performance gaps not captured by functional correctness benchmarks.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 5.800 | 0.400 | 5-6 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- The user study grounding instructions in real developer preferences is a genuine contribution, distinguishing this work from synthetic instruction benchmarks.
- Multi-language support (Python, Java, JavaScript) adds practical breadth and enables cross-language analysis.
- The two evaluation settings (predefined vs. follow-up instructions) provide complementary views of instruction-following ability.
- The modular framework design (is_applicable/verify functions) is clean, extensible, and allows for rule-based or LLM-based implementations.
- The paper includes LLM judge reliability analysis (87% agreement with humans) and a bias ablation study, demonstrating methodological rigor.
- The benchmark reveals meaningful findings, such as model rankings differing from functional correctness benchmarks and large performance gaps among frontier models.
- Statistical analyses (Wilcoxon, Friedman tests) are included, and the authors are upfront about potential judge bias.

### Weaknesses

- The user study sample size is small (30 developers, 10 per language) and lacks demographic analysis, potentially limiting the generalizability of the instruction catalog.
- The benchmark is built solely on LiveBench competitive programming problems (LeetCode/AtCoder style), which may not represent real-world software engineering tasks.
- The instruction catalog is relatively small (228 total) and when divided across three languages and multiple categories, sample sizes per cell appear limited, leading to wide confidence intervals and reduced statistical power.
- No direct comparison with existing code IF benchmarks (e.g., CodeIF, BigCodeBench-Instruct, CodeIF-Bench) is provided, making it difficult to assess the incremental contribution.
- The reliance on LLM-as-a-judge with ~87% agreement introduces measurement noise that could affect ranking conclusions, especially for small performance gaps.
- The Python-to-Java/JavaScript translation pipeline may introduce errors or unnatural code patterns that could confound cross-language results; validation details are insufficient.
- The claim of being 'the first IF benchmark' for code generation is somewhat overstated given existing related work.
- The evaluation is limited to 10 proprietary models from 3 families, with no open-source or smaller models, limiting the breadth of the comparison.
- The paper does not deeply analyze why models fail on specific instruction types, which would strengthen the insights.

### Questions

- How does CodeAlignBench compare directly with existing code instruction-following benchmarks (e.g., CodeIF, BigCodeBench-Instruct) on the same models? Would the rankings differ?
- What is the total number of LiveBench problems used in the benchmark, and how many tasks are generated per problem? What is the exact number of tasks per instruction category and per language in the final evaluation?
- What is the per-language distribution of the 228 verified instructions? Is there sufficient representation of each category for reliable statistical analysis?
- How was the Python-to-Java/JavaScript translation validated? Were there cases where translation introduced errors that affected instruction applicability or verification?
- What is the inter-annotator agreement among human annotators during the instruction coding process and the LLM judge reliability study? Were inconsistent raters excluded?
- How was the is_applicable function validated? What is its false positive/negative rate?
- For the follow-up setting, how is the initial code selected? Is it always the model's own generation or a fixed baseline?
- How sensitive are the results to the choice of LLM judge and prompt variations? Could the authors provide examples of judge disagreements and analyze the failure modes?
- How was the sample size of 30 developers determined? What is the confidence interval for the instruction distribution across the broader developer population?
- Have the authors considered evaluating on more diverse coding problems beyond algorithmic tasks, or combining multiple instructions in a single task?

### Limitations

- The benchmark is limited to algorithmic/competitive programming problems from LiveBench, which may not represent the full spectrum of real-world coding scenarios.
- The user study involved a relatively small number of developers with specific backgrounds, which may limit the generalizability of the instruction catalog.
- The reliance on LLM-as-a-judge for verification introduces potential biases and measurement error that are only partially mitigated by the reported ablation study.
- The translation of problems across languages may introduce artifacts that affect instruction-following performance differently across languages.
- The evaluation is limited to proprietary models, and reproducibility over time is uncertain given API changes and LiveBench's constant updates.
- The paper does not address potential negative societal impacts, such as environmental costs of large-scale LLM evaluation or potential misuse of the benchmark for misleading model comparisons.
- The benchmark inherits LiveBench's constant updates, which reduces contamination but creates reproducibility challenges for future comparisons.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 83,481
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 74,521
- Completion tokens: 9,662
- Reasoning tokens reported: 0
- Total tokens: 93,143
- Estimated total: $0.01316339

Full individual reviews and raw JSON responses are in `review_bundle.json`.
