# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B090.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.018150**

## Final Meta-review

The paper introduces TheMCPCompany, a benchmark for evaluating LLM agents that interact with real-world services through task-specific MCP tools rather than general-purpose browsers. It extends TheAgentCompany by creating MCP servers for Azure, GitLab, Plane, RocketChat, and ownCloud, yielding over 18,000 tools. The benchmark includes 10 primitive and 7 composite Azure tasks, manually annotated oracle tool sets for each task, and a baseline agent called MCPAgent that retrieves tools on the fly via a find_tools gateway. Experiments across six LLMs show that oracle tool access improves performance and reduces cost relative to a browser-based agent; retrieval-based MCPAgent also often outperforms the browser baseline, although smaller models suffer from imperfect retrieval and all models largely fail on complex Azure composite tasks.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 3 | 2.600 | 0.490 | 2-3 |
| Clarity | 2 | 2.400 | 0.490 | 2-3 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 3 | 2.600 | 0.490 | 2-3 |
| Presentation | 2 | 2.400 | 0.490 | 2-3 |
| Contribution | 3 | 3.000 | 0.632 | 2-4 |
| Overall | 6 | 6.000 | 1.265 | 4-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The benchmark is large-scale and realistic, with over 18,000 tools derived from real REST APIs, far exceeding prior MCP/tool benchmarks and addressing a timely gap in evaluating agents that use heterogeneous tool collections.
- The oracle tool-set annotation is a useful experimental design that separates tool selection from tool execution, providing an upper bound on tool-based agent performance and enabling diagnosis of retrieval failures.
- MCPAgent's find_tools retrieval-gateway architecture is a practical and scalable baseline for accessing tens of thousands of tools without overflowing context, and the finding that it can outperform browser-based agents on TheAgentCompany tasks is valuable.
- The evaluation covers six diverse LLMs and multiple operating modes (browser, oracle, retrieval), providing insights into reasoning models, retrieval recall, cost savings, and failure modes.
- The paper includes strong reproducibility infrastructure: Terraform scripts for Azure tasks, evaluation scripts, free-tier Azure resources, and detailed appendix prompts.

### Weaknesses

- The central performance table (Table 1) and some other numeric results referenced in the main text are missing from the submitted manuscript, making it impossible to fully verify the main performance and cost claims.
- The Azure task suite is very small (10 primitive + 7 composite tasks) and composite tasks are nearly unsolved by all models, limiting statistical power and discriminative ability at the top end.
- Only a single embedding-based retrieval method is evaluated; there are no ablations of top-k, embedding model, query rewriting, re-ranking, or comparisons with stronger or learned tool-retrieval methods, so the paper's conclusions about retrieval bottlenecks are not well supported.
- No multiple runs, confidence intervals, or significance tests are reported despite stochastic LLM agents, so differences between models and conditions may be within noise.
- Oracle tool sets were manually annotated without inter-annotator agreement, validation of minimality/sufficiency, or sensitivity analysis, so the reported upper-bound may be subjective.
- The comparison is only against a text-based browser agent; there is no direct comparison to REST API-calling agents or prior MCP/tool-retrieval baselines, making it difficult to isolate the contribution of MCP versus task-specific tools.
- Some experimental choices are questionable or understated, such as disabling thinking for Opus-4.1, rewriting RocketChat descriptions with GPT-4.1, and not reporting cumulative token counts or the exact number of retrieved tools.

### Questions

- Can the authors provide the full numeric results for Table 1 and all other missing tables, including performance, cost, and variance across runs?
- What was the retrieval top-k value, and how sensitive are the results to this choice and to the embedding model?
- How were the oracle tool sets validated, and was there any inter-annotator agreement or verification of sufficiency/minimality?
- Are the reported differences statistically significant given only single-run results? Were multiple seeds or runs used?
- For Azure composite tasks, why was there no oracle-tool or browser baseline condition to isolate whether failures stem from retrieval, tool use, or task complexity?
- How does MCPAgent compare to directly providing all tool descriptions via long-context models or to stronger retrieval methods such as BM25, fine-tuned retrievers, or iterative retrieval?
- Why was Opus-4.1's thinking disabled, and could this have materially disadvantaged that model?
- Does the paper report the cumulative token usage and context lengths when many tools are retrieved over long trajectories?

### Limitations

- The Azure task set is small and mostly unsolved, limiting the ability to rank models on the most challenging enterprise scenarios.
- The benchmark uses only a single retrieval method and a single agent framework (OpenHands CodeAct) with a text-only browser baseline, so findings may not generalize to other architectures, retrievers, or multimodal agents.
- The tool set is dominated by Azure (about 17,000 of 18,505 tools), so conclusions may not generalize to other large tool ecosystems.
- Manual annotation and automatic generation of tool descriptions may introduce biases, including potential bias toward OpenAI models from GPT-4.1-rewritten RocketChat descriptions.
- Deploying agents against production services can cause irreversible actions and incur costs; the paper acknowledges but does not mitigate these safety risks.
- The paper omits key reproducibility details such as exact top-k values, cumulative token counts, and the full content of Table 1.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 89,852
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 85,756
- Completion tokens: 21,901
- Reasoning tokens reported: 15,517
- Total tokens: 111,753
- Estimated total: $0.01814959

Full individual reviews and raw JSON responses are in `review_bundle.json`.
