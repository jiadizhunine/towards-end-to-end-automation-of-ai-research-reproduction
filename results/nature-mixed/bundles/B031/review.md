# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B031.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.053455**

## Final Meta-review

This paper presents a comprehensive robustness evaluation framework for Text-Attributed Graph (TAG) learning, systematically benchmarking classical GNNs, Robust GNNs (RGNNs), and GraphLLMs across 10 datasets from 4 domains under diverse text-based, structure-based, and hybrid perturbations in both poisoning and evasion settings. The study reveals three key insights: (1) models exhibit an inherent text-structure robustness trade-off, (2) simple RGNNs like GNNGuard can be surprisingly effective when paired with advanced text encoders, and (3) GraphLLMs are particularly vulnerable to training data corruption. To address the identified trade-off, the authors propose SFT-auto, a novel framework that uses LLM reasoning for adversarial attack detection and recovery within a single model, achieving superior and balanced robustness against both textual and structural attacks. The paper includes extensive appendices with detailed results, ablations, and adaptive attack analyses.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.400 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.000 | 0.632 | 2-4 |
| Significance | 3 | 3.200 | 0.400 | 3-4 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.000 | 0.632 | 2-4 |
| Contribution | 3 | 3.200 | 0.400 | 3-4 |
| Overall | 6 | 6.200 | 0.400 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Comprehensive evaluation framework that unifies GNNs, RGNNs, and GraphLLMs across diverse datasets (10 across 4 domains), attack types (text, structure, hybrid), and settings (poisoning, evasion, transductive, inductive)
- Novel empirical insights, particularly the text-structure robustness trade-off, which provides valuable guidance for model design
- The proposed SFT-auto framework is creative, leveraging LLM reasoning capabilities for attack detection and recovery in a unified pipeline
- Thorough experimental methodology with careful attention to hyperparameter tuning, fair baseline comparison, and alignment of attack settings
- Detailed appendices providing full numerical results, ablation studies, adaptive attack analyses, and embedding quality metrics supporting key claims
- The analysis of why GNNGuard performs well with advanced text encoders is insightful and well-supported with quantitative evidence
- Code release for reproducibility
- Honest discussion of limitations and excluded attacks with justifications

### Weaknesses

- Heavy reliance on rank-based evaluation in the main paper can obscure absolute performance differences and make it difficult to assess practical impact
- The proposed LLM-based text attack (full text replacement with different-class content) may not represent sophisticated real-world attack scenarios compared to word-level or character-level perturbations
- SFT-auto's detection mechanism relies on a fixed cosine similarity threshold (0.5) that may not generalize well across diverse datasets or attack patterns; no principled adaptive threshold selection is provided
- The paper's contributions are primarily empirical; the proposed defense method's novelty is limited relative to existing approaches, and the text-structure trade-off lacks theoretical analysis or deeper mechanistic explanation
- Limited GraphLLM baseline coverage (only GraphGPT, LLaGA, and SFT-neighbor) given the rapid growth of this field
- SFT-auto does not consistently outperform baselines across all datasets (e.g., SFT-neighbor achieves higher accuracy on PubMed under structural attacks), and claims of 'balanced robustness' are not always clearly demonstrated
- The paper is extremely dense and tries to cover too much ground, making it difficult to follow the main narrative; some key results (hybrid attacks, SFT-auto adaptive attack performance) are relegated to the appendix
- Exclusion of certain attack types (Mettack, TextAttack) and datasets from some experiments may limit the generalizability of findings
- Computational cost of SFT-auto (requiring fine-tuning a 7B parameter LLM) is not thoroughly analyzed and may limit practical applicability

### Questions

- How does SFT-auto perform against adaptive attacks specifically designed to bypass its detection mechanism? The paper mentions adaptive attacks in the appendix but does not appear to provide comprehensive results for SFT-auto against such attacks.
- The paper uses a fixed cosine similarity threshold of 0.5 for structure attack detection. How sensitive is SFT-auto's performance to this threshold? Have you considered learning or adaptively selecting this threshold per dataset?
- What is the actual computational overhead of SFT-auto compared to SFT-neighbor in terms of wall-clock training and inference time? The paper claims 'comparable' but does not provide concrete numbers.
- How does SFT-auto handle the case where both text and structure are attacked simultaneously? The paper mentions hybrid attacks in the appendix but does not detail SFT-auto's performance under such scenarios in the main text.
- The text attack replaces entire node texts with LLM-generated content. How would SFT-auto perform against more realistic attacks such as word-level perturbations or character-level modifications that preserve the original text structure?
- The paper excludes some datasets for certain attacks (e.g., Computer and ArXiv for text attacks). How does this affect the generalizability of the conclusions?
- How does SFT-auto's performance vary with different LLM backbones? The paper only evaluates with Mistral-7B. Would smaller or larger models affect the detection and recovery capabilities?
- Can you provide statistical significance tests to support the claim that SFT-auto achieves 'superior and balanced robustness'? Rank-based evaluation may obscure important differences between methods.
- What are the failure modes of SFT-auto? Under what conditions does it fail to detect attacks or produce incorrect recoveries?

### Limitations

- The evaluation is limited to node classification tasks; other important graph learning tasks such as link prediction and graph classification are not considered
- The proposed SFT-auto method requires a large LLM backbone (Mistral-7B), which may be computationally prohibitive for some applications and has significant energy/environmental implications that are not addressed
- The text-structure trade-off finding is based on empirical observations; a theoretical framework explaining this phenomenon would strengthen the contribution
- The paper focuses primarily on transfer attacks; adaptive attacks are only explored in limited settings in the appendix, and the robustness of SFT-auto against adaptive attackers is not thoroughly evaluated
- The evaluation excludes some large-scale datasets (e.g., ArXiv for GraphLLMs) due to scalability, which may limit the generalizability of findings to very large graphs
- The paper does not thoroughly explore the potential negative societal impacts of the proposed attack and defense methods, particularly the dual-use nature of the attacks in high-stakes domains like social networks and financial systems
- The evaluation framework, while comprehensive, may not generalize to other types of text-attributed graphs, such as those with heterogeneous node types or dynamic graph structures
- The SFT-auto method's detection mechanism may produce false positives/negatives that could affect performance in real-world settings, and this is not deeply analyzed

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 370,464
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 361,504
- Completion tokens: 10,068
- Reasoning tokens reported: 0
- Total tokens: 380,532
- Estimated total: $0.05345469

Full individual reviews and raw JSON responses are in `review_bundle.json`.
