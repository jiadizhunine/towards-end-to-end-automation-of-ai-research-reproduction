# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B076.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.016497**

## Final Meta-review

The paper presents ABxLab, a man-in-the-middle intervention framework that intercepts and modifies real web pages to run controlled behavioral experiments on LLM-based shopping agents. Using a binary forced-choice task in a OneStopMarket environment, the authors manipulate prices, ratings, product order, and ten psychological nudges across 17 LLMs and over 80,000 trials, with a small human baseline. They find that agents exhibit strong systematic biases toward higher ratings, lower prices, order position, and persuasive cues, often exceeding human sensitivity. They also show that explicit user preferences act as categorical switches. The framework and benchmark are released as an open-source contribution.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 2.800 | 0.400 | 2-3 |
| Clarity | 3 | 2.800 | 0.400 | 2-3 |
| Significance | 4 | 3.400 | 0.490 | 3-4 |
| Soundness | 3 | 2.800 | 0.400 | 2-3 |
| Presentation | 3 | 2.800 | 0.400 | 2-3 |
| Contribution | 4 | 3.200 | 0.400 | 3-4 |
| Overall | 6 | 6.000 | 1.095 | 4-7 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Novel and timely framework (ABxLab) that turns arbitrary websites into controllable behavioral testbeds for LLM agents, enabling causal manipulation in realistic web environments.
- Large-scale empirical evaluation with 17 models, over 80,000 trials, multiple intervention types (price, rating, order, nudges), and matched conditions, providing a rich dataset.
- Inclusion of a human baseline, though limited, allows direct comparison and highlights the striking finding that agent biases often exceed human susceptibility by 3-10x.
- Statistical analysis uses fixed-effects models with cluster-robust standard errors and multiple-testing corrections, which is more rigorous than typical WebAgent benchmark reporting.
- The open release of the framework and data (claimed) could enable reproducible, cumulative behavioral science of AI agents, addressing an important gap in trust and safety.
- The study reveals that agents implement simplistic decision rules (threshold switches for preferences), shedding light on their decision-making mechanisms.

### Weaknesses

- The human baseline is small (30 participants, 50 choices each) and collected only for the original (unmatched) condition, making human-agent comparisons across matched conditions unsupported and potentially underpowered.
- Ecological validity is limited: the binary forced-choice task, 10-step action cap, text-only pruned HTML observation space, and artificially injected textual nudges may not generalize to real-world multimodal, multi-option decision-making.
- The coding of negative-framing nudges (e.g., 'newer version available', 'final sale') is ambiguous; the 'Nudged' indicator appears to be sign-inverted for these items, which could inflate average nudge effects and conflate distinct mechanisms.
- Product pair selection relies on heuristic filters (e.g., LLM title filter, k-neighborhood) that may introduce selection bias; no validation of these filters or of the naturalness of injected nudge text is provided.
- The paper largely documents biases without offering a mechanistic explanation or testing mitigation strategies, limiting actionable implications.
- Statistical concerns include potential unreliability from clustering on only 10 nudge-text clusters, the use of linear probability models with near-deterministic choices, and unclear specification of interaction order in the regression models.
- The framework is built on WebArena/AgentLab; extensibility to other domains is not demonstrated, and the study focuses only on consumer shopping.
- Several figures and appendices are redacted in the provided manuscript, hindering full reproducibility and verification.

### Questions

- How exactly are negative-framing nudges coded in the regression? Is the 'Nudged' indicator sign-inverted for 'newer version' and 'final sale' items, and if so, does this assume a directional effect that may not hold universally?
- Why was the human baseline collected only for the original condition and not for matched rating/price conditions? How would human-agent comparisons change if humans faced the same matched conditions?
- What is the value of N in the interaction terms for the M1/M2 specifications, and how was it chosen?
- How are price and rating matched in the MRaP condition? Do agents ever notice inconsistencies between the modified text and other page elements?
- What fraction of agent episodes hit the 10-action cap? Could the results be driven by agents forced to decide prematurely, and is there an analysis excluding such episodes?
- What validation was performed to ensure the LLM title filter does not introduce selection bias in product pairs? What are its false positive/negative rates?
- Were the 30 human participants given identical text-based interfaces as the agents, or a simplified presentation? What instructions and incentives were provided?
- The user-profile experiments are reported qualitatively; what are the effect sizes and significance levels for these conditions?

### Limitations

- The study is confined to binary forced-choice, text-only observations in a single shopping environment, limiting generalizability to real-world multi-option, multimodal, and longer-horizon decisions.
- The human baseline is underpowered and unmatched, making the headline human-vs-agent bias comparison fragile for several conditions.
- The injected nudges may be more salient than naturally occurring web content, potentially inflating measured effects.
- The paper does not identify underlying causes of the biases (e.g., pretraining data, instruction following, architecture), limiting mitigation insights.
- The study uses current LLMs; findings may not generalize to future models or specialized agents.
- No ethics statement regarding human participants or IRB approval is included, and the open-source framework could be misused for adversarial manipulation of agents; responsible disclosure is not discussed.

### Ethics

Ethical concerns flagged: **True**

## Usage and Cost

- Requests: 6
- Prompt tokens: 77,650
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 73,554
- Completion tokens: 22,101
- Reasoning tokens reported: 15,688
- Total tokens: 99,751
- Estimated total: $0.01649731

Full individual reviews and raw JSON responses are in `review_bundle.json`.
