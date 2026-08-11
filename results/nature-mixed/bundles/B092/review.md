# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B092.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **8/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.023839**

## Final Meta-review

This paper establishes fundamental computational impossibility results for AI alignment achieved through input-prompt, output, and mitigation filtering mechanisms. Under cryptographic assumptions (existence of time-lock puzzles and one-way functions), the authors prove that: (1) input-prompt filters running significantly faster than the LLM cannot distinguish adversarial prompts from benign ones, even when those prompts elicit harmful behavior; (2) output filters, even those more computationally powerful than the LLM, cannot reliably distinguish harmful from benign outputs when harmfulness is judged by a more powerful downstream oracle; and (3) mitigation filters that can modify prompts face similar fundamental limits, with connections to watermarking security. The key technical innovation is a novel method using pseudo-random time-lock puzzles and recoverable-randomness sampling to construct adversarial prompts that are provably indistinguishable from benign prompts for computationally bounded filters while still leading the LLM to produce harmful outputs. The paper validates its theoretical findings with experiments showing that time-lock-inspired attacks bypass real-world safety filters (Llama Guard, ShieldGemma) and can elicit harmful behavior from production models (e.g., Gemini 2.5 Flash). The central conclusion is that external black-box filtering alone cannot guarantee safety; achieving alignment requires filters with computational resources comparable to the LLM and access to model internals.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 4.000 | 0.000 | 4-4 |
| Quality | 3 | 3.400 | 0.490 | 3-4 |
| Clarity | 4 | 3.600 | 0.490 | 3-4 |
| Significance | 4 | 3.800 | 0.400 | 3-4 |
| Soundness | 4 | 3.800 | 0.400 | 3-4 |
| Presentation | 4 | 3.600 | 0.490 | 3-4 |
| Contribution | 4 | 3.800 | 0.400 | 3-4 |
| Overall | 8 | 7.600 | 0.490 | 7-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel and significant theoretical contribution: provides the first formal impossibility results for filtering-based alignment, connecting cryptography (time-lock puzzles) to AI safety in an elegant and rigorous manner
- Comprehensive treatment of multiple filtering approaches (input, output, and mitigation filters), demonstrating the breadth of computational barriers
- The recoverable-randomness sampling (RRS) construction is technically sophisticated and well-motivated, with clear connections to watermarking literature
- Rigorous proofs with clearly stated assumptions, including careful handling of edge cases in the RSW construction
- Empirical validation with real-world filters and production LLMs demonstrates practical relevance and feasibility of the theoretical attacks
- Strong implications for AI safety policy, regulation, and the design of future alignment mechanisms
- Clear positioning relative to related work, distinguishing from prior empirical jailbreak studies and other theoretical impossibility results

### Weaknesses

- Theoretical constructions rely on highly stylized LLMs (e.g., M' that can solve time-lock puzzles) that may not accurately reflect real-world model architectures or training procedures; the gap between theory and practice is acknowledged but not fully bridged
- Reliance on specific cryptographic assumptions (e.g., RSW time-lock puzzles with pseudo-randomness property) that may not hold for all proposed constructions and could be vulnerable to quantum attacks (though LWE-based alternatives are mentioned)
- The assumption of computational asymmetry between filters and LLMs may not always hold in practice, especially as guard models become more sophisticated
- Empirical evaluation is limited in scope: only a small number of filters and models tested, and the attacks used in experiments (e.g., Caesar cipher) are simpler than the full time-lock construction
- The connection between the theoretical impossibility results and the practical experiments could be more clearly articulated
- The paper does not deeply explore potential defenses or alternative alignment approaches (e.g., training-time interventions, white-box auditing) that might circumvent these filtering barriers

### Questions

- How sensitive are the theoretical results to the specific choice of time-lock puzzle? Would the results hold with other puzzle constructions (e.g., LWE-based), and what are the specific challenges in generalizing the pseudo-randomness property?
- The paper assumes a computational asymmetry between filters and LLMs. How robust are the results if the filter has comparable or greater computational resources than the LLM? For instance, could a filter running in time O(t) or O(t log t) still be fooled?
- How does the RRS construction handle the case where the innocent prompt generator G has very low entropy? The paper assumes high entropy, but real-world prompt distributions may be more concentrated.
- Could the impossibility results be extended to settings where the filter has access to the LLM's internals (white-box access) but is still computationally bounded? Does the conclusion about needing access to internals follow directly from the impossibility results, or is it an additional assumption?
- In the output filtering result, the harmfulness measure H' is constructed to be as powerful as the environment. Does this make the result somewhat trivial, since the filter is compared against an oracle that can execute outputs? Could you clarify the practical interpretation?
- The experiments use fine-tuned 'uncensored' models. Would the same bypass rates hold for production-aligned models like GPT-4 or Claude? How do the results change with models that have been explicitly safety-trained?
- Are there any practical defenses suggested by the theoretical analysis? For example, does the analysis imply that filters should be as computationally powerful as the models, or that model internals should be made available to auditors?
- What are the concrete parameter choices (e.g., time parameter t, security parameter λ) needed to make the full time-lock-based attacks practical against current-generation models, and how do the bypass rates compare to the simpler encodings used in experiments?

### Limitations

- The theoretical results are worst-case and show existence of problematic LLMs, not that all or most LLMs are vulnerable; practical relevance depends on whether such adversarial LLMs could realistically emerge
- The constructions rely on stylized LLMs that may not directly apply to real-world systems; the gap between the constructed M' and actual LLMs is not fully bridged
- The experiments are limited in scale and do not cover the full range of production models and filters; the attacks tested are simpler than the full theoretical construction
- The paper does not explore potential defenses or alternative alignment approaches in depth, which could provide a more balanced perspective
- The assumption of computational asymmetry between filters and LLMs may not hold in all real-world deployment scenarios
- Potential negative societal impact: the paper's techniques could be misused to develop more effective jailbreaks against current and future LLMs, though the authors note follow-up work already demonstrates this

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 161,411
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 152,451
- Completion tokens: 8,825
- Reasoning tokens reported: 0
- Total tokens: 170,236
- Estimated total: $0.02383923

Full individual reviews and raw JSON responses are in `review_bundle.json`.
