# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B193.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 4, 'Reject': 1}
- Estimated API cost: **$0.016770**

## Final Meta-review

This paper addresses the limitation of single-query-vector dense retrievers in multi-target retrieval tasks where a query has multiple valid answers. The authors first empirically demonstrate that existing retrievers (Contriever, Stella, Inf-Retriever, NV-Embed) perform worse as the distance between target document embeddings increases. To address this, they propose AMER (Autoregressive Multi-Embedding Retriever), which generates multiple query embeddings autoregressively using an LLM backbone. During training, the model uses InfoNCE loss with Hungarian matching to handle unordered target sets and scheduled sampling to bridge the train-inference gap. During inference, multiple query embeddings are used for retrieval and results are aggregated via round-robin merging. Experiments on synthetic vectorized data show AMER achieves 100% recall while single-query models achieve at most 21%. On real-world datasets (AmbigQA and QAMPARI), AMER shows 4% and 21% relative gains over single-embedding baselines respectively, with larger gains (5% and 144%) on subsets where target documents are less similar. The paper also provides analysis showing that real-world datasets have relatively homogeneous targets, explaining the modest gains, and releases code for reproducibility.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 3.600 | 0.490 | 3-4 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 3 | 3.200 | 0.400 | 3-4 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 3 | 3.200 | 0.400 | 3-4 |
| Contribution | 3 | 2.800 | 0.400 | 2-3 |
| Overall | 6 | 6.000 | 0.632 | 5-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Clear problem identification with quantitative evidence: The paper convincingly demonstrates the limitation of single-vector retrievers on diverse targets through experiments with four different retrievers on two datasets.
- Novel architecture: AMER's autoregressive multi-embedding generation is a creative approach that directly addresses the identified limitation, differing from existing multi-vector methods like ColBERT.
- Comprehensive synthetic evaluation: The synthetic experiments are well-designed, testing multiple input distributions and transformations, and clearly show the advantage of AMER over single-query models.
- Thorough real-world evaluation: The paper tests multiple backbone LMs (Llama-1B/3B/8B, Qwen3-4B), uses statistical significance testing, and includes ablation studies (scheduled sampling, output diversity analysis).
- Honest analysis: The authors acknowledge the modest real-world gains and provide insightful analysis (target similarity analysis) explaining why gains are smaller than in synthetic settings.
- Reproducibility: Code is released, and training details are well-documented in appendices.

### Weaknesses

- Modest real-world improvements: The 4-21% relative gains on whole datasets are relatively small, and absolute MRecall@100 values remain low, especially on QAMPARI (e.g., 8-12%).
- Fixed number of output embeddings: The model requires manually specifying the number of query embeddings per dataset (2 for AmbigQA, 5 for QAMPARI), which may not generalize well to varying numbers of targets.
- Frozen document encoder: The document encoder is fixed, which limits joint optimization potential and may not fully leverage the multi-vector approach's benefits.
- Missing comparison with multi-vector baselines: No comparison to ColBERT-style multi-vector retrievers, which also generate multiple query vectors, is provided.
- Limited practical evaluation: The use of MRecall@100 is lenient; results at smaller k (e.g., @10, @20) would be more informative for real-world retrieval systems.
- Computational overhead not quantified: The autoregressive generation of multiple embeddings and separate retrieval passes adds latency and cost, but this is not analyzed.

### Questions

- How is the number of output embeddings (m_pred) determined for each dataset? Is it always set to the average number of targets, and how sensitive are results to this choice?
- What is the computational overhead of AMER compared to single-query retrievers, both in training and inference? The autoregressive generation of multiple embeddings likely adds latency.
- How does AMER compare to ColBERT-style multi-vector retrievers on these datasets? The paper only compares to single-vector methods.
- Could the model be extended to dynamically predict the number of query embeddings based on the query, rather than using a fixed number?
- Why is the document encoder frozen? Would joint training of both encoders improve results, and what are the computational trade-offs?
- Could you report MRecall at smaller k values (e.g., @10, @20) to better understand practical retrieval performance?
- Would hard negative mining improve the single-query baseline and reduce the observed gap with AMER? This would strengthen the claim that multi-embedding is inherently beneficial.

### Limitations

- The paper acknowledges that real-world datasets have highly similar target documents (cosine similarity 0.86-0.9), which limits the demonstration of the method's diversity benefits. Better benchmarks with more diverse targets are needed.
- The method requires knowing the number of answers in advance, which is often unknown in practice. The paper does not provide a clear solution for this.
- The evaluation is limited to two datasets (AmbigQA, QAMPARI) with relatively small test sets (827 and 531 examples). Broader evaluation across more diverse retrieval tasks would strengthen conclusions.
- The frozen document encoder and LoRA fine-tuning may limit the approach's generalizability to different document encoders or training regimes.
- Potential negative societal impacts are not discussed, though retrieval methods could amplify biases if the underlying corpus or training data is biased.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 109,393
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 100,433
- Completion tokens: 9,586
- Reasoning tokens reported: 0
- Total tokens: 118,979
- Estimated total: $0.01676979

Full individual reviews and raw JSON responses are in `review_bundle.json`.
