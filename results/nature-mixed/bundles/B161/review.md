# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B161.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.017041**

## Final Meta-review

This paper introduces HSCodeComp, a benchmark for evaluating deep search agents on hierarchical rule application through the task of predicting 10-digit Harmonized System (HS) Codes for e-commerce products. The benchmark contains 632 real-world product entries with expert-annotated HSCodes spanning 27 HS chapters and 32 product categories. The authors evaluate 14 foundation models, 6 open-source agent systems, and 3 closed-source agent systems, finding that the best agent (SmolAgent with GPT-5) achieves only 46.8% accuracy compared to 95.0% for human experts. The paper includes detailed analyses of failure modes, ablations on decision rules, image inputs, and backbone models, as well as a study showing that test-time scaling fails to improve performance. The benchmark and code are released publicly.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 2.800 | 0.400 | 2-3 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 2.800 | 0.400 | 2-3 |
| Contribution | 3 | 3.200 | 0.400 | 3-4 |
| Overall | 6 | 6.200 | 0.400 | 6-7 |
| Confidence | 4 | 3.800 | 0.400 | 3-4 |

### Strengths

- Addresses a genuinely under-explored capability—rule application in deep search agents—which is distinct from existing open-domain and structured data benchmarks.
- The task is realistic and practically important, as HSCode classification is critical for global trade and customs operations.
- Rigorous benchmark construction pipeline with expert annotation, multi-expert validation, and quality review showing only 2% disagreement rate.
- Comprehensive evaluation across a wide range of models (14 foundation models, 6 open-source agents, 3 closed-source agents).
- Detailed analysis of failure modes provides useful qualitative insights into agent limitations in rule application.
- Ablation studies on decision rules, image inputs, and backbone models are thoughtfully designed.
- The finding that test-time scaling (majority voting and self-reflection) fails to improve performance is an important negative result for the community.
- Transparent ethical considerations with fair annotator compensation (34.6 USD/hour).

### Weaknesses

- The dataset is relatively small (632 entries), which raises concerns about statistical significance of performance differences, particularly for the closed-source agent evaluation on only 49 examples.
- The ablation on human-written decision rules shows mixed results (decreasing performance for some agents), but the paper does not provide a thorough explanation for this counterintuitive finding.
- The test-time scaling analysis is limited to majority voting and self-reflection; more sophisticated scaling approaches (e.g., best-of-N with verifiers) are not explored.
- The proposed three-level knowledge categorization (open-domain, structured, rule data) is somewhat artificial, as rule application is embedded in many existing benchmarks.
- The claim of being the 'first' benchmark for rule application could be better contextualized against prior work on rule-based reasoning in LLMs (e.g., LegalBench).
- The 95% human expert accuracy is not thoroughly discussed; the paper does not explain the 5% disagreement or how consensus was reached in those cases, and it is unclear if this was measured on the same instances used for annotation, which could introduce circularity.
- The paper does not deeply analyze the impact of the noisy product descriptions on agent performance, which is mentioned as a key challenge.
- The improvement from 46.8% to 95.0% is used as the primary evidence of difficulty, but no analysis is provided on what specific capabilities human experts possess that agents lack.
- The removal of product images and URLs from the released dataset may limit reproducibility of multimodal experiments.
- The paper has some clarity issues, including repeated text in the abstract, broken figure references, and inconsistent terminology (e.g., HScodBench vs HSCodeComp).

### Questions

- The dataset contains only 632 entries. How was this sample size determined, and what are the confidence intervals for the reported performance differences between baselines?
- The decision rule ablation shows mixed results (decrease for SmolAgent and WebSailor, slight increase for Aworld). Could you provide more analysis on why these rules hurt performance? Is it due to prompt length, ambiguity in the rules, or the agents' inability to correctly apply them?
- For the closed-source agent evaluation on 49 examples, how were these examples selected? Is this subset representative of the full benchmark distribution?
- How was the 95% human expert accuracy measured? Was it computed on the same 632 examples used for ground truth annotation? If so, how do you avoid circularity in this comparison? Were the experts given the same tools (web search, CROSS database) as the agents?
- The test-time scaling study shows negligible improvement with majority voting. Did you consider using a verifier or reward model to select the best answer rather than simple majority voting?
- How do you handle the temporal validity of HSCodes? Tariff rules change over time—are the ground truth codes verified against the current version of the tariff schedule? What is the expected shelf life of the ground truth annotations?
- What is the inter-annotator agreement rate (e.g., Cohen's kappa) between the two initial annotators before the senior expert resolves disagreements?
- The paper mentions that product images and URLs are removed from the released dataset for security reasons. How will researchers be able to reproduce the multi-modal experiments without access to images?
- Have you compared HSCodeComp with existing HSCode prediction benchmarks (e.g., the one by Judy 2024)? What are the quantitative differences in difficulty and characteristics?
- Could you provide more details on the specific tools available to agents? For example, what search APIs were used, and how were results presented to the agent?
- The paper mentions that 27 unique HS chapters are covered. What is the distribution of codes across these chapters, and are some chapters over-represented?
- For the 'Medium-Think' variant of WebSailor, how was this reasoning depth controlled? This seems crucial for reproducibility.
- The paper states that webpage visits decrease agent performance. Could you provide more analysis on what specific types of webpage content cause the degradation? Is this a limitation of the agent's long-context handling or the search tool's snippet extraction?
- The benchmark is described as the 'first' for hierarchical rule application. How does HSCodeComp differ from or relate to other rule-based benchmarks like LegalBench or ARC-AGI-2? What specific aspects of hierarchical rule application are unique to this benchmark?
- The dataset uses eWTP tariff rules and US CROSS rulings. How transferable are these rules to other countries' customs systems? Would an agent trained on this benchmark generalize to other jurisdictions?
- Could you provide more details on the annotation process - how long did it take per product, what was the total cost, and how many annotators were involved?
- The paper mentions that semantic redundancy filtering was applied. What was the original data size before filtering, and how much was discarded?
- Have you considered evaluating retrieval-augmented approaches that specifically retrieve relevant tariff rules before classification, rather than relying on general web search?
- The paper uses eWTP tariff rules - how do these differ from the WCO's official HS nomenclature or the US HTSUS? Could this introduce a bias for agents more familiar with certain tariff systems?

### Limitations

- The dataset is limited to 632 entries, which may not capture the full diversity of products and HSCodes in real-world e-commerce and may limit statistical power for per-category analysis.
- The evaluation focuses on English-language product descriptions and U.S. customs rulings (CROSS), potentially limiting generalizability to other languages and customs jurisdictions.
- The paper does not address potential biases in the data collection process, such as platform-specific product distributions.
- The removal of product images and URLs from the released dataset limits reproducibility of the multi-modal experiments.
- The benchmark focuses exclusively on HSCode prediction, which may limit its generalizability to other rule-application domains (e.g., law, medicine), though the paper argues these share structural similarities.
- The evaluation of closed-source agents was conducted on only 49 examples, which may not be representative.
- The benchmark may become outdated as HSCode rules change over time, requiring periodic updates.
- Potential negative societal impact: improved HSCode prediction could be used to circumvent customs regulations or facilitate trade fraud, though this risk is minimal. The paper does not discuss the potential for automation to displace human customs classifiers.
- The paper does not thoroughly explore potential negative societal impacts, such as how improved HSCode classification could affect customs enforcement or trade compliance.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 106,131
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 97,171
- Completion tokens: 12,186
- Reasoning tokens reported: 0
- Total tokens: 118,317
- Estimated total: $0.01704111

Full individual reviews and raw JSON responses are in `review_bundle.json`.
