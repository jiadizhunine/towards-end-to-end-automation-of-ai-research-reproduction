# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B138.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.022756**

## Final Meta-review

The paper introduces R-HORIZON, a method to construct multi-horizon reasoning tasks by composing existing single-horizon problems with explicit dependencies. The authors build a benchmark spanning math (MATH500, AIME, AMC), code (LiveCodeBench), and agentic (WebShaper) tasks, and evaluate 25+ large reasoning models (LRMs). They find significant performance degradation as reasoning horizon increases and identify three key failure modes: limited effective reasoning length, constrained reflection scope, and poor thinking budget allocation. They further use R-HORIZON composed data for reinforcement learning with verifiable rewards (RLVR), demonstrating improvements on both multi-horizon tasks and standard single-horizon benchmarks (e.g., +7.5 on AIME24), along with improved token efficiency and reflection quality.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 3.400 | 0.490 | 3-4 |
| Clarity | 4 | 3.600 | 0.490 | 3-4 |
| Significance | 3 | 3.400 | 0.490 | 3-4 |
| Soundness | 3 | 3.400 | 0.490 | 3-4 |
| Presentation | 4 | 3.600 | 0.490 | 3-4 |
| Contribution | 3 | 3.400 | 0.490 | 3-4 |
| Overall | 7 | 7.000 | 0.632 | 6-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Addresses a timely and important gap: current benchmarks focus on isolated single-horizon tasks, while real-world reasoning often requires long sequential chains
- Simple, scalable, and low-cost composition method that leverages existing datasets, making it practical and easy to adopt
- Comprehensive evaluation across 26 models spanning multiple families and sizes, and three task categories (math, code, agentic)
- Insightful analysis of failure modes (effective reasoning length, reflection scope, thinking budget allocation) with quantitative evidence and actionable insights
- RLVR training with composed data demonstrates clear practical utility, including generalization to standard single-horizon benchmarks
- Good ablation studies on dependencies, evaluation metrics, and difficulty ordering
- Well-organized paper with clear figures and detailed appendices

### Weaknesses

- The composition method relies on simple arithmetic dependencies (e.g., answer + offset) that may not capture the full complexity of real-world long-horizon reasoning
- The 'expected accuracy' metric assumes independence of sub-problem pass rates, which is questionable given the introduced dependencies
- RL training experiments are limited to a single model size (R1-Qwen-7B) and a single base dataset, limiting generalizability claims
- Code task composition uses simple concatenation without dependencies, and agentic task composition is only briefly described, creating methodological inconsistency across task types
- The impact of different dependency functions (e.g., non-linear transformations) is not explored
- Data contamination is acknowledged as a possible explanation for anomalous behavior but not thoroughly investigated
- The paper does not provide a detailed cost analysis of the RL training process, despite claiming the method is low-cost

### Questions

- How does R-HORIZON compare directly to existing long-horizon composition methods like GSM-Infinite or NEST on the same benchmark? Could a head-to-head comparison clarify the distinct contributions?
- How sensitive are the main conclusions to the 'expected accuracy' assumption of independent sub-problems? Would a different baseline (e.g., sequential solving without dependencies) be more appropriate?
- Why is dependency-based composition not used for code tasks? Would adding true dependencies (e.g., one program's output feeding into another's input) lead to different findings?
- How do the RL-trained models perform on other standard benchmarks beyond math (e.g., code, general reasoning) to assess potential negative transfer?
- Do the benefits of composed training data hold for larger models (e.g., 32B or 70B) or different base models?
- Could the improvements from composed data be partly due to increased data diversity or longer context exposure, rather than the dependency structure specifically? An ablation with independent concatenated problems trained via RL would be informative.
- How is the quality of the model-based key variable verification (Eq. 2) validated? What is the error rate, and how does it affect the composed problems?
- How do you ensure that models don't exploit shortcuts in the composed problems (e.g., solving later problems without actually using dependency information)?
- What is the computational cost overhead of RL training with composed data compared to single-horizon data?

### Limitations

- The synthetic composition paradigm may not fully capture the complexity of real-world long-horizon tasks, where dependencies may be more implicit or varied
- The benchmark and training data are constructed from existing datasets, which may inherit biases or contamination issues
- RL experiments are limited in scale (one model size, one base dataset) and may not generalize to other training regimes or architectures
- The composition method is primarily designed for problems with verifiable integer answers and may not directly extend to open-ended or subjective reasoning tasks
- The paper does not deeply explore potential negative societal impacts of improving long-horizon reasoning, though these are likely minimal for this type of work

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 149,370
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 140,410
- Completion tokens: 10,978
- Reasoning tokens reported: 0
- Total tokens: 160,348
- Estimated total: $0.02275633

Full individual reviews and raw JSON responses are in `review_bundle.json`.
