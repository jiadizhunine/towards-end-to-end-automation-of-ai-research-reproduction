# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B118.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **5/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 1, 'Reject': 4}
- Estimated API cost: **$0.023702**

## Final Meta-review

This paper introduces Chain-of-Agents (CoA), a paradigm for training LLMs to perform multi-agent-style problem solving within a single end-to-end trainable model, as opposed to using external multi-agent frameworks. The approach involves: (1) distilling trajectories from a state-of-the-art multi-agent system (OAgents) into CoA-format training data via a multi-agent distillation framework with progressive quality filtering, (2) supervised fine-tuning on these trajectories, and (3) agentic reinforcement learning on verifiable tasks using DAPO. The resulting 'Agent Foundation Models' (AFMs) are evaluated across web agent benchmarks (GAIA, BrowseComp, HLE, WebWalker, MHQA) and code/math benchmarks (LiveCodeBench, CodeContests, AIME), claiming state-of-the-art results and significant inference cost reductions. All code, data, and model weights are promised to be open-sourced.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.894 | 2-4 |
| Quality | 3 | 2.600 | 0.490 | 2-3 |
| Clarity | 2 | 1.800 | 0.400 | 1-2 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 3 | 2.800 | 0.400 | 2-3 |
| Presentation | 2 | 1.800 | 0.400 | 1-2 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 5 | 4.800 | 0.748 | 4-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The core idea of unifying multi-agent collaboration within a single trainable model is timely and addresses a real limitation of current multi-agent frameworks, namely the lack of data-centric learning.
- The multi-agent distillation framework is a practical and scalable approach to generating high-quality training data from existing multi-agent systems, with a thoughtful progressive quality filtering pipeline.
- The empirical evaluation is extensive, covering a broad range of benchmarks across web, code, and math domains, with strong results demonstrating improvements over existing TIR methods.
- The commitment to open-sourcing all resources (models, code, data) is highly valuable for reproducibility and future research.
- The efficiency analysis demonstrating reduced token consumption compared to traditional multi-agent systems is a useful practical contribution.
- The agentic RL stage using DAPO with a simplified reward function is a sensible and clean design choice.

### Weaknesses

- Limited novelty: The CoA paradigm is essentially an extension of Tool-Integrated Reasoning (TIR) with multiple role-playing agents. The distinction between CoA and existing TIR methods is not crisply defined, and the formalization resembles a general state-action loop rather than a fundamentally new mechanism.
- Critical lack of ablations: The paper does not isolate the contribution of multi-agent distillation versus standard SFT on the same tasks in a ReAct/TIR format. The claim that multi-agent distillation is key to performance is not directly supported.
- Significant presentation issues: Malformed tables (e.g., Table 4, Table 6, Table 7), broken references, garbled math notation, empty appendix sections, and typos undermine the credibility and readability of the paper.
- Weak efficiency analysis: The 84.6% token reduction claim is based on only 10 randomly sampled GAIA instances, which is too small a sample size for a robust conclusion.
- LLM-as-judge reliability concerns: The reward function for web agent RL relies on Qwen-2.5-72B as a judge, with no validation against human annotations or discussion of reward hacking risks.
- Data inconsistencies: Dataset sizes in tables do not match totals stated in the text (e.g., Table 4 lists TQ as 11,313 but text says single-hop benchmark is 11,015), raising concerns about experimental rigor.
- Overclaiming with the term 'Agent Foundation Models': The models are fine-tuned Qwen variants rather than foundation models in the traditional sense.
- Generalization analysis is superficial: The 'Generalization on Unseen Agents' experiments are qualitative, with no quantitative success rates or rigorous analysis of failure modes.
- Technical details are sparse: The trajectory conversion process from OAgents to CoA format, the definition of 'hops', and the mechanism of 'dynamic agent orchestration' are not clearly explained.

### Questions

- How exactly does CoA differ mechanistically from standard TIR beyond having more diverse agent roles? What specific mechanisms enable 'dynamic agent orchestration' vs. the static think-action-observation pattern in TIR?
- Can you provide an ablation where you train with SFT on standard ReAct trajectories (without the multi-agent role-playing structure) using the same underlying agent and data, and compare against AFM-SFT? This would isolate the contribution of the multi-agent distillation component.
- Could you clarify the data inconsistencies in Table 4 and Table 6? For example, why is TQ listed as 11,313 in Table 4 but the text says the single-hop benchmark is 11,015 examples?
- The efficiency claim of 84.6% token reduction is based on only 10 GAIA samples. Can you provide results on a larger evaluation set (e.g., 100+ samples) with confidence intervals and a breakdown of token consumption components?
- How was the LLM-as-Judge validated? Did you compare its judgments against human annotations? What is the agreement rate, and how do you address potential reward hacking?
- In the 'Generalization on Unseen Agents' analysis, why does the web agent fail to generalize while the code agent succeeds? Could you provide quantitative results for this analysis?
- What is the marginal contribution of each stage of the progressive quality filtering (complexity, quality, reflection enrichment, error-correction upsampling)? An ablation study would be valuable.
- The paper claims the framework can distill 'any multi-agent system.' Have you tested with a teacher other than OAgents (e.g., OWL or AutoGen)? How sensitive are the results to the choice of teacher?
- AFM underperforms on single-hop QA benchmarks (e.g., NQ, TriviaQA) compared to some baselines. Is this due to overfitting to multi-hop patterns? Have you analyzed this trade-off?
- What is the computational cost of the multi-agent distillation process itself? How many trajectories were generated and what was the filtering rate?

### Limitations

- The paper does not adequately discuss limitations of the CoA paradigm, such as the upper bound imposed by the teacher multi-agent system's capabilities, and the potential loss of modularity compared to true multi-agent systems with specialized models.
- The generalization analysis reveals that the model's ability to use unseen tools is highly dependent on the format of the training data, which may limit the general applicability of the CoA paradigm.
- The computational cost of the multi-agent distillation pipeline is not reported, which may limit reproducibility for smaller labs.
- The evaluation focuses on English-language benchmarks; generalization to other languages or cultural contexts is not explored.
- Potential negative societal impacts of autonomous web agents (e.g., automated misinformation gathering, privacy violations, bias amplification in LLM-as-Judge evaluations) are not discussed.
- The models are specialized for the tasks and tools seen during training, and the term 'Agent Foundation Models' may overstate the scope of the contribution.
- The maximum context length (32k tokens) may limit the complexity of tasks that can be solved, and the reliance on a single model for all agent roles may constrain the diversity of expertise.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 151,379
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 142,419
- Completion tokens: 13,350
- Reasoning tokens reported: 0
- Total tokens: 164,729
- Estimated total: $0.02370175

Full individual reviews and raw JSON responses are in `review_bundle.json`.
