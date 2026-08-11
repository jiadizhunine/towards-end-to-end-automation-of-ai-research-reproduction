# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B046.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.018121**

## Final Meta-review

This paper introduces InSTA, an automated pipeline for generating internet-scale training data for web navigation agents without human annotations. The pipeline consists of three stages: (1) an LLM task proposer that annotates 150k websites (filtered from 1M based on safety) with agentic tasks via a feedback loop, (2) LLM agents that complete these tasks, producing 2.2M screenshots and reasoning traces, and (3) an LLM judge that filters trajectories by predicting success scores. The authors train small Qwen 3 1.7B models on this data and demonstrate they achieve 56.9% success rate on held-out websites, outperforming the Qwen 3 235B data collection policy and Llama 4 Maverick (400B), and reaching 94.7% of Gemini 2.5 Flash performance. The agents also zero-shot transfer to WebVoyager and improve performance on WebLINX and Mind2Web when mixed with human data. The paper releases code, models, and data, and reports a total data collection cost of $521.55.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.800 | 0.400 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.000 | 3-3 |
| Significance | 4 | 3.800 | 0.400 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.000 | 3-3 |
| Contribution | 4 | 3.600 | 0.490 | 3-4 |
| Overall | 7 | 6.800 | 0.400 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Impressive scale: 150k websites annotated, 2.2M trajectories and screenshots collected, representing a significant advance over prior datasets limited to ~200 sites.
- Novel three-stage pipeline (task proposer, agent, judge) with a feedback loop for task generation, providing a complete automated solution for web agent data generation.
- Strong empirical results showing a 1.7B parameter model can match or exceed much larger models (235B, 400B), demonstrating the quality of the generated data.
- Clean train-test separation: models are evaluated on held-out sites and zero-shot transfer to WebVoyager without overlap with training data, supporting genuine generalization claims.
- Comprehensive evaluation including zero-shot transfer, static benchmark integration, reasoning budget analysis, and multiple judges.
- Thorough safety considerations with 97% accuracy in harmful content detection and PII removal, along with transparent cost analysis making the pipeline accessible to academic labs.
- Full release of code, models, and data, enabling reproducibility and further research.

### Weaknesses

- The LLM judge accuracy of 82.6% is a critical bottleneck; with 150k trajectories, this could mislabel ~26k trajectories, potentially propagating errors into training data.
- Potential circularity: the same model family (Qwen 3 235B) is used for data collection, filtering, and evaluation, which could introduce systematic bias favoring the Qwen family.
- Human validation sets are small (100 trajectories for judge accuracy, 300 tasks for reliability), limiting statistical robustness given the scale of the pipeline.
- Limited analysis of judge failure modes (false positives/negatives) and how judge errors correlate with downstream agent performance across task categories.
- The paper does not deeply analyze task diversity beyond word clouds and category frequencies; it is unclear how many tasks are trivial vs. requiring multi-step reasoning, and some categories (e.g., product comparison) have very low success rates.
- The 'internet-scale' claim is somewhat overstated: 150k sites from the top 1M by PageRank is still a small fraction of the internet, and coverage biases are not addressed.
- Comparison to frontier LLMs may be confounded by different judges used across evaluations; the 'matching' claim varies across judges (only 3 of 4 for WebVoyager).
- The reasoning budget ablation is only performed on Gemini 2.5 Flash, not on the trained Qwen 3 1.7B model, leaving unclear whether the trained model benefits from test-time compute scaling.

### Questions

- How does the judge's accuracy vary across different task categories? Are there systematic biases, and how do judge errors correlate with downstream agent performance?
- Given that the same model family (Qwen 3) is used for data collection, filtering, and evaluation, could there be a systematic bias? Have you tested with a judge from a completely different model family (e.g., only GPT-4o or only Gemini) for final evaluation of trained agents?
- What is the distribution of judge scores? Is there a clear separation between successful and unsuccessful trajectories, and how sensitive are the results to the filtering threshold (e.g., Judge(Success) > 0.8 instead of =1)?
- What is the inter-annotator agreement on the 100 human-labeled trajectories used to evaluate the judge? Were evaluators given specific criteria, and what was the reliability?
- For the WebVoyager zero-shot transfer, what is the breakdown of success rates per website? Are there particular website types where the trained model performs well or poorly?
- How was the 3,000-site held-out test set selected? Was there any human verification of task quality or feasibility, and how does performance vary by site popularity?
- Does the trained Qwen 3 1.7B model show monotonic improvement with increased reasoning budget, similar to the Gemini 2.5 Flash ablation shown in Figure 10?
- How much of the 150k sites' data was actually used for training the small models? Was the full 20k trajectory dataset used for the main results?

### Limitations

- The judge's 82.6% accuracy means significant noise in training labels, which could propagate errors to trained agents; a more detailed error analysis is needed.
- The safety filter is evaluated on only 100 websites (50 safe, 50 unsafe), which may not adequately represent the diversity of content on the internet; approximately 4,500 unsafe sites could pass through in the 150k dataset.
- The task proposer filters out social media and forum sites, and does not handle tasks requiring user accounts or personal data, limiting the diversity of skills agents can learn.
- The pipeline's reliance on LLM judgment for both data generation and evaluation could introduce systematic biases that are not fully explored.
- The paper focuses on text-based observations despite collecting multimodal data (2.2M screenshots), leaving multimodal training unexplored.
- Only one loop of task generation was used; the full potential of the iterative feedback process is not demonstrated.
- Ethical concerns about autonomous agents interacting with live websites (e.g., analytics pollution, scraping, potential misuse for fraud or misinformation) are acknowledged but mitigation strategies may not fully address these risks.
- The paper does not deeply explore the effectiveness of PII removal (scrubadub) or potential privacy concerns from screenshots of live websites.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 115,169
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 106,209
- Completion tokens: 11,522
- Reasoning tokens reported: 0
- Total tokens: 126,691
- Estimated total: $0.01812051

Full individual reviews and raw JSON responses are in `review_bundle.json`.
