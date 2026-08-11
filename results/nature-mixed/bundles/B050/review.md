# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B050.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.012943**

## Final Meta-review

This paper identifies and addresses a training-inference mismatch in discrete diffusion language models. Classical SFT randomly masks tokens across the entire response, while inference uses blockwise semi-autoregressive decoding with clean prefixes and hidden future tokens. The authors propose Blockwise SFT, which partitions responses into fixed-size blocks, selects one active block per training step for stochastic masking, freezes preceding tokens, and hides future ones, computing loss only on the active block. This directly mirrors the blockwise decoding procedure. The paper provides theoretical grounding (gradient bias bound, variational bound, unbiased gradient estimation) and empirical evaluation on GSM8K and MATH using LLaDA-8B-Instruct with LoRA fine-tuning. Experiments show consistent gains over classical SFT and other baselines under matched compute and token budgets. Ablations confirm that improvements stem from training-inference alignment rather than incidental masking effects.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 3 | 3.000 | 0.000 | 3-3 |
| Clarity | 4 | 3.800 | 0.400 | 3-4 |
| Significance | 3 | 3.000 | 0.000 | 3-3 |
| Soundness | 3 | 3.000 | 0.000 | 3-3 |
| Presentation | 4 | 3.800 | 0.400 | 3-4 |
| Contribution | 3 | 3.000 | 0.000 | 3-3 |
| Overall | 6 | 6.400 | 0.490 | 6-7 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Clearly identifies a genuine and important training-inference mismatch in diffusion LMs
- Proposes a simple, elegant, and architecture-agnostic solution that is a drop-in replacement for classical SFT
- Provides solid theoretical grounding including variational bounds, unbiased gradient estimation, and gradient bias analysis
- Careful experimental design with matched-compute and matched-token protocols
- Well-designed ablations and block-size consistency studies that convincingly attribute gains to alignment
- Consistent and substantial empirical gains on GSM8K and MATH
- Clear and well-organized writing

### Weaknesses

- Limited evaluation scope: only mathematical reasoning tasks, a single base model (LLaDA-8B-Instruct), and LoRA fine-tuning; generalizability to other domains and model scales is untested
- Theoretical contributions are somewhat standard (variational bounds and unbiased gradient estimation are well-known in diffusion literature)
- Gradient bias bound relies on Lipschitz assumptions that are not empirically verified
- Baseline comparisons may not be fully tuned to the same extent, and some baselines are primarily pretraining objectives rather than SFT methods
- No inference efficiency/speed comparisons, despite the motivation of aligning with blockwise decoding
- The paper does not explore adaptive block sizing or non-uniform block sampling, which could further improve results

### Questions

- How does Blockwise SFT perform on non-math domains such as general instruction following, summarization, or code generation?
- Would the gains persist with larger models (e.g., LLaDA-33B) or with full fine-tuning instead of LoRA?
- How sensitive is the method to the block sampling distribution? Has difficulty-aware or length-aware reweighting been explored?
- In the Equal-Tokens protocol, does Blockwise SFT require more wall-clock time due to more epochs, and how does this affect overfitting risk?
- What is the effect of the diffusion step schedule T on performance, and does the optimal schedule differ from classical SFT?
- How does Blockwise SFT compare to simply using a higher masking probability in classical SFT?
- How are partial blocks handled when response length is not a multiple of the block size?
- Can you provide estimates of the Lipschitz constants in Theorem 3.1 for the model used?
- Have you measured inference speed or throughput gains from blockwise decoding, and how does Blockwise SFT affect these?

### Limitations

- Empirical evaluation is confined to mathematical reasoning tasks and a single model family; broader validation across domains and model sizes is needed
- Theoretical analysis provides bounds but does not quantify their practical tightness for realistic models
- The method assumes fixed block sizes; interaction with adaptive block sizing (e.g., APD) is unexplored
- Training with Blockwise SFT may require more epochs to cover all blocks, potentially increasing wall-clock time
- Potential negative societal impact is not discussed in detail, though the method itself is unlikely to introduce novel harms beyond general LLM fine-tuning concerns

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 80,932
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 71,972
- Completion tokens: 10,151
- Reasoning tokens reported: 0
- Total tokens: 91,083
- Estimated total: $0.01294345

Full individual reviews and raw JSON responses are in `review_bundle.json`.
