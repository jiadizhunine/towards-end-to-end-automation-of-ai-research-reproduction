# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B094.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 1, 'Reject': 4}
- Estimated API cost: **$0.018210**

## Final Meta-review

The paper proposes Code2Video, a code-centric multi-agent framework for generating educational videos by producing executable Manim code. It introduces three agents: Planner (structures lecture content and retrieves visual assets), Coder (converts storyboards into executable code with scope-guided repair), and Critic (refines spatial layout using visual anchor prompts and VLM feedback). The authors also present MMMC, a benchmark of 456 educational units derived from 3Blue1Brown videos across 13 disciplines, and TeachQuiz, a metric that attempts to measure knowledge transfer via prompt-based unlearning in a VLM. Experiments compare against pixel-based diffusion models, direct code-generation LLMs, and human-made videos on aesthetics, efficiency, and TeachQuiz, reporting consistent gains and a small human study. The paper is well-motivated and contains novel ideas, but the reviewers express serious concerns about the validity of the TeachQuiz metric, unfair baselines, evaluation bias, reproducibility, and scalability.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.200 | 0.400 | 3-4 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 2 | 2.400 | 0.490 | 2-3 |
| Significance | 2 | 2.400 | 0.490 | 2-3 |
| Soundness | 2 | 2.200 | 0.400 | 2-3 |
| Presentation | 2 | 2.400 | 0.490 | 2-3 |
| Contribution | 2 | 2.200 | 0.400 | 2-3 |
| Overall | 4 | 4.600 | 1.200 | 4-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Code-centric agentic framework is a novel and well-motivated approach for educational video generation, offering controllability, interpretability, and reproducibility through executable Manim code.
- The tri-agent design (Planner-Coder-Critic) includes practical engineering contributions such as scope-guided debugging and visual anchor prompts for spatial layout.
- MMMC is a substantial benchmark with 456 curated units across 13 scientific disciplines, filling a gap in code-based educational video evaluation.
- TeachQuiz is a creative attempt to measure educational efficacy beyond visual fidelity, using an unlearning-relearning protocol to isolate the video's contribution to knowledge acquisition.
- Comprehensive experiments covering multiple LLM backbones, pixel-based baselines, ablations, and a human study demonstrate the framework's broad applicability.
- The paper is generally well-organized and clearly motivated, with qualitative examples illustrating the advantages of code-driven synthesis.

### Weaknesses

- TeachQuiz relies on prompt-based 'unlearning' in a closed-source VLM (Gemini-2.5 Pro), which does not guarantee true removal of parametric knowledge; the reported unlearned baseline accuracy of 5% (below 25% random chance) suggests the prompt forces refusal rather than measuring actual knowledge absence, undermining the metric's validity.
- Pixel-based baselines generate only ~8-second clips without lecture lines, while Code2Video produces minutes-long videos with detailed explanations, making aesthetic and TeachQuiz comparisons unfair and confounded by the amount of information rather than teaching quality.
- Potential self-preference bias exists because the same VLM (Gemini-2.5 Pro) is used as the Critic, the aesthetics judge, and the student in TeachQuiz; no independent judge or human validation is provided.
- The human study is small (8-10 participants per group depending on reading, 40 total), not clearly randomized or screened for prior knowledge, and confounds video duration (8 s to 16.9 min) with engagement; IRB/consent details are missing.
- Reproducibility is severely limited: Appendix A.2 lists prompt names but contains no actual prompt content, and code/datasets are redacted.
- Scalability claims are contradicted by efficiency numbers: Code2Video uses 19-49K tokens and 8-17 minutes per video, whereas direct code generation uses 1.1-2.3K tokens and 1.8-2.8 minutes, making the agent pipeline 10-20x more expensive.
- Main results report only point estimates with no variance, confidence intervals, or significance tests, making it difficult to assess the reliability of the improvements.
- Claims of being 'comparable to human-crafted tutorials' are overstated: the best Code2Video achieves 87.9 AES and 86.0 TeachQuiz versus 99.7 and 97.1 for human-made 3B1B videos, a clear gap in absolute terms.

### Questions

- How is the prompt-based unlearning validated to genuinely block prior knowledge? Have the authors compared with parameter-level unlearning on an open-source model to confirm that the unlearned baseline is meaningful and not merely instruction-following refusal?
- How would results change if pixel-based baselines generated same-length videos or if Code2Video were evaluated on short clips? Could the TeachQuiz gap be attributed to information volume rather than teaching methodology?
- Since Gemini-2.5 Pro serves as both the Critic and the VLM-as-judge, how do the authors rule out self-preference bias? Have they evaluated with other VLMs or blinded human raters?
- Can the authors provide the exact prompts, scoring rubrics, and implementation details (e.g., visual anchor coordinate mapping) needed for reproduction? The appendix currently only lists section headings.
- What are the exact participant counts, recruitment criteria, prior-knowledge checks, and IRB approval for the human study? How were the 20 learning topics selected, and why were there so few participants per group?
- Are the reported improvements (e.g., '40% improvement') absolute percentage-point gains or relative improvements? What is the variance across topics and runs, and are differences statistically significant?
- Why was TheoremExplainAgent, a closely related code-based educational video system, not evaluated on MMMC as a main baseline? How does Code2Video compare to it on MMMC in terms of quality and efficiency?

### Limitations

- The benchmark and method are limited to Manim-style math/physics tutorials from a single source (3Blue1Brown), limiting generalizability to other educational formats, languages, or pedagogical approaches.
- The system depends on large proprietary LLMs and a commercial VLM, making it expensive, non-transparent, and difficult to reproduce or audit.
- External assets are scraped from Google Images and Iconfinder without clear licensing or content-safety filtering, raising copyright and potential bias concerns.
- The framework does not address potential hallucination or factual errors in generated content; the 'Accuracy & Depth' metric is VLM-judged and may not catch subtle scientific inaccuracies.
- The TeachQuiz metric is only as reliable as the unlearning protocol, which is not a true intervention and may not isolate the video's contribution to knowledge acquisition.
- The human study is small, non-diverse, and confounded by video duration, limiting confidence in claims of superiority over human tutorials.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 92,691
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 88,595
- Completion tokens: 20,698
- Reasoning tokens reported: 13,363
- Total tokens: 113,389
- Estimated total: $0.01821021

Full individual reviews and raw JSON responses are in `review_bundle.json`.
