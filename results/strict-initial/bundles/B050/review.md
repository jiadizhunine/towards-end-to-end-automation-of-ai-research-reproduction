# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B050.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **6/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 3, 'Reject': 2}
- Estimated API cost: **$0.019165**

## Final Meta-review

The paper addresses the mismatch between standard full-response random-mask supervised fine-tuning (SFT) and blockwise semi-autoregressive decoding in discrete diffusion language models. It proposes Blockwise SFT, which at each training step keeps a clean prefix frozen, hides the future suffix, and computes the denoising loss only on one active block, thereby aligning training with blockwise inference. The authors provide theoretical analyses including a gradient-bias bound, a variational upper bound, and an unbiased estimator, and empirically evaluate on GSM8K and MATH using LLaDA-8B-Instruct with LoRA, showing consistent gains over classical SFT and several recent diffusion-SFT baselines under matched FLOPs and token budgets. Block-size consistency and prefix/suffix ablation studies support the training-inference alignment hypothesis.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 2.800 | 0.400 | 2-3 |
| Quality | 3 | 2.400 | 0.490 | 2-3 |
| Clarity | 2 | 2.400 | 0.490 | 2-3 |
| Significance | 3 | 2.800 | 0.400 | 2-3 |
| Soundness | 3 | 2.600 | 0.490 | 2-3 |
| Presentation | 2 | 2.400 | 0.490 | 2-3 |
| Contribution | 3 | 2.800 | 0.400 | 2-3 |
| Overall | 6 | 5.400 | 0.800 | 4-6 |
| Confidence | 4 | 3.600 | 0.490 | 3-4 |

### Strengths

- The paper identifies a practical and important training-inference mismatch in discrete diffusion LMs and proposes a simple, architecture-agnostic, drop-in objective that directly mirrors blockwise semi-autoregressive decoding.
- Empirical results on GSM8K and MATH show consistent improvements over classical SFT and several recent diffusion-specific objectives under both Equal-FLOPS and Equal-Tokens protocols.
- Block-size consistency and prefix/suffix ablation studies provide direct evidence that the gains stem from clean prefixes and hidden suffixes rather than incidental masking effects.
- The method requires no architectural or inference changes, making it easy to adopt in existing diffusion LM pipelines.

### Weaknesses

- The theoretical analysis is incomplete and at times informal: Theorem 3.2 relies on 'standard manipulations' without a full derivation, Theorem 3.3's unbiasedness claim is qualified by an 'overall positive scalar' that is not reconciled, and duplicated theorem headings and abbreviated proofs hurt clarity.
- The evaluation is narrow: only one base model (LLaDA-8B-Instruct), only LoRA fine-tuning, and only two mathematical reasoning benchmarks (GSM8K and MATH), leaving generalizability to other domains, model families, and scales unverified.
- Implementation details for the baseline methods (MDLM, Soft-Masked, RDM, Two-Step Loss) are not provided, so it is unclear whether each baseline was tuned fairly under the same compute/token budgets.
- Equal-FLOPS and Equal-Tokens comparisons may confound supervision alignment with optimization dynamics, since Blockwise SFT supervises many fewer tokens per optimizer step than classical SFT; the paper does not report actual loss-bearing token counts or wall-clock time.
- MATH evaluation uses exact string match without answer extraction or normalization, which may be brittle and could distort relative performance; no significance testing or multiple-seed analysis is reported.
- The paper has several presentation issues (Algorithm 1 only as a figure, duplicate theorem headings, repeated proofs) and no code or trained checkpoints are released, hindering reproducibility.

### Questions

- How exactly were the baseline objectives (MDLM, Soft-Masked, RDM, Two-Step Loss) implemented on LLaDA-8B-Instruct? Were they tuned with the same hyperparameters, compute budget, and data as Blockwise SFT?
- In the Equal-Tokens protocol, how is a supervised token counted? Since the masking rate is sampled from Uniform(1e-3,1), the number of loss-bearing tokens per step is random and not equal to the response length; could the authors report actual loss-token counts and optimizer steps for each method?
- Can the authors provide a complete derivation of Theorem 3.2, including the ELBO-to-weighted-cross-entropy conversion and the explicit form of the constant C? Does the bound rely on positional masking inside the active block?
- How is the diffusion timestep t sampled in Blockwise SFT, and how does the single Bernoulli masking event per update correspond to the 128-step denoising process used at inference?
- How sensitive are the results to the training and inference block size, especially for responses whose length is not a multiple of B? Is there a principled way to choose B for new tasks or models?
- Does Blockwise SFT's advantage persist on non-mathematical tasks such as instruction following, summarization, or code generation, or with other discrete diffusion LMs such as SSD-LM?
- In the block-size consistency study, were statistical significances computed for the diagonal dominance, and were classical SFT results evaluated at each inference block size as a control?

### Limitations

- Only evaluated on mathematical reasoning benchmarks (GSM8K, MATH) with a single base model (LLaDA-8B-Instruct) and LoRA; no full fine-tuning or other diffusion LMs are tested.
- The theoretical guarantees are not fully rigorous: the variational bound and unbiasedness results rely on sketches and unverified assumptions, and the gradient-bias bound uses Lipschitz constants that are not estimated.
- The equal-compute comparisons may not isolate supervision alignment because Blockwise SFT changes the number of supervised tokens per step and potentially the number of epochs per sample, creating a regularization or optimization-speed confound.
- MATH evaluation uses exact string matching on raw outputs, which is brittle and may not reflect true mathematical reasoning ability.
- No code, checkpoints, or detailed reproduction scripts are provided, limiting reproducibility.
- Potential negative societal impacts are not discussed; while math reasoning seems benign, the method could be applied to other domains to improve generation of harmful content.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 71,470
- Cache-hit prompt tokens: 3,840
- Cache-miss prompt tokens: 67,630
- Completion tokens: 34,594
- Reasoning tokens reported: 26,627
- Total tokens: 106,064
- Estimated total: $0.01916527

Full individual reviews and raw JSON responses are in `review_bundle.json`.
