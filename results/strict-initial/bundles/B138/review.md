# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B138.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 1, 'Reject': 4}
- Estimated API cost: **$0.019675**

## Final Meta-review

The paper proposes R-Horizon, a query composition method that converts existing single-horizon reasoning tasks (math, code, agentic) into sequences of dependent multi-step problems. It uses R-Horizon to construct a long-horizon benchmark, evaluates 25 large reasoning models (LRMs), and observes substantial performance degradation as the reasoning horizon grows. The authors also use R-Horizon to create RLVR training data with GRPO/RLVR on R1-Qwen-7B, reporting improved performance on composed benchmarks and some transfer to original tasks such as AIME24. The paper further analyzes failure modes, including effective reasoning length, reflection locality, and thinking-budget allocation.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 2 | 2.400 | 0.490 | 2-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 2 | 2.200 | 0.400 | 2-3 |
| Presentation | 2 | 2.400 | 0.490 | 2-3 |
| Contribution | 2 | 2.400 | 0.490 | 2-3 |
| Overall | 4 | 4.400 | 0.800 | 4-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses an important and underexplored gap: evaluating and training for long-horizon or multi-step reasoning in LRMs.
- Proposes a simple, low-cost, and scalable composition mechanism that reuses existing benchmarks and creates explicit dependencies for math tasks.
- Provides a broad evaluation across 25 LRMs and multiple task families (math, code, agentic), with consistent degradation trends as horizon grows.
- Offers useful analyses of error types, effective reasoning length, reflection locality, and token-budget allocation, going beyond simple accuracy comparisons.
- Demonstrates practical value through RLVR: training on composed data improves composed performance and also transfers to some standard benchmarks, with more efficient token allocation.

### Weaknesses

- True interdependent composition is only implemented for integer-answer math problems; code tasks are simply concatenated without dependencies and WebShaper has only 50 composed questions, weakening the paper's central 'long-horizon dependent reasoning' claim across domains.
- The benchmark and synthetic compositions may not reflect realistic long-horizon tasks, and small subset sizes (e.g., AIME24/25 30 problems, WebShaper 50) reduce statistical reliability.
- The theoretical expected-accuracy metric assumes independence and unchanged difficulty across composed sub-problems, which is violated by explicit dependencies and changed prompts; this undermines the comparison between expected and actual accuracy.
- RL experiments are limited to one 7B model (R1-Qwen-7B) and one base dataset, with no multiple seeds or confidence intervals; the abstract's +7.5 AIME2024 claim is inconsistent with Table 1 (which shows +17.1 for n=2), and gains on original benchmarks are mixed.
- Evaluation depends on LLM-based answer extraction (GPT-4.1) and LLM-based key-variable verification without human validation; the reported inconsistency of extraction (~9% at n=16) could affect benchmark conclusions.
- The paper acknowledges an anomalous 'correct final answer despite earlier wrong answers' pattern and speculates data contamination, but does not quantify or mitigate it, threatening benchmark validity.
- Several figures and algorithm details are redacted or inaccessible in the submitted version, making the analysis and methods difficult to verify or reproduce.
- Key concepts (effective reasoning length, reflection scope, budget allocation) lack precise definitions or reproducible methodology, raising concerns about their interpretation.

### Questions

- How exactly is effective reasoning length defined and computed? Is it the token range where errors are most likely, and how is it distinguished from context-length or model-specific artifacts?
- For code and WebShaper tasks, since dependencies are not explicitly enforced, how does R-Horizon measure interdependent long-horizon reasoning rather than merely long-context multi-task performance?
- How valid is the product-of-pass-rates expected accuracy when the composition changes prompts and adds dependencies? Did the authors compare against a REST-style independent concatenation baseline on the same benchmark to isolate dependency effects?
- Which model M is used for key-variable extraction and verification, and what is its accuracy? How many extracted key variables are accepted versus rejected?
- Are the RL results stable across random seeds and model sizes? Does training on n=2/n=4 transfer to n=16/higher, and is the +7.5 AIME24 improvement statistically significant?
- What steps were taken to detect or prevent data contamination in both the benchmark and the RL training data? The paper itself attributes anomalous final-answer success to contamination; how does this affect all-or-nothing scoring and the R_all reward?
- How are responses truncated at the 64k token limit handled in scoring, and does truncation interact with the reported effective reasoning length analysis?

### Limitations

- The composition method is restricted to problems with integer answers and extractable key variables, limiting applicability to many real-world reasoning tasks with unstructured or non-integer outputs.
- Code and agentic compositions lack true dependencies, so the benchmark does not uniformly evaluate dependent long-horizon reasoning across all task families.
- LLM-based answer extraction and key-variable verification introduce unquantified errors; the benchmark relies heavily on synthetic construction rather than naturally occurring long-horizon problems.
- RL training experiments are confined to a single 7B model and one base dataset, so generalization to larger models or other domains is unverified.
- Data contamination remains a confound; the paper's own anomaly suggests that some final correct answers could result from memorization rather than dependent reasoning.
- The paper does not release code or data, limiting reproducibility, and does not discuss the increased computational/energy costs of long-horizon evaluation and training.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 98,139
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 94,043
- Completion tokens: 23,206
- Reasoning tokens reported: 16,639
- Total tokens: 121,345
- Estimated total: $0.01967517

Full individual reviews and raw JSON responses are in `review_bundle.json`.
