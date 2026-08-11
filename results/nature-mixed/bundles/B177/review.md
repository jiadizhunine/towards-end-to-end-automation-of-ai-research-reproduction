# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B177.txt
- Model: deepseek-v4-flash
- Final decision: **Accept**
- Overall: **7/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 5, 'Reject': 0}
- Estimated API cost: **$0.036555**

## Final Meta-review

The paper introduces ZeroSiam, an asymmetric Siamese architecture for test-time entropy minimization (TTA). The key innovation is embedding asymmetry within a single forward pass: a lightweight learnable predictor and stop-gradient branch are inserted before the classifier, creating online and target branches from the same feature. The objective combines entropy minimization on the online branch with a symmetric KL alignment regularizer to the stop-gradient target branch. This design prevents collapse to constant one-hot outputs, a common failure of pure entropy minimization, while maintaining efficiency (no augmentations, no extra backbone passes). The paper provides empirical and theoretical evidence that the asymmetry not only prevents collapse but also absorbs and regularizes biased shortcut signals, improving performance even when collapse does not occur. Extensive experiments across vision (ImageNet-C with ResNet50-GN, ViT-Base/Small, ConvNeXt-Tiny, Swin-Tiny) and language (Llama3.1-8B on math reasoning benchmarks) demonstrate consistent gains over prior TTA methods, with negligible computational overhead. The method is also shown to be plug-and-play with existing TTA methods (EATA, DeYO).

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 4 | 4.000 | 0.000 | 4-4 |
| Quality | 3 | 3.200 | 0.400 | 3-4 |
| Clarity | 4 | 3.800 | 0.400 | 3-4 |
| Significance | 4 | 4.000 | 0.000 | 4-4 |
| Soundness | 3 | 3.200 | 0.400 | 3-4 |
| Presentation | 4 | 3.800 | 0.400 | 3-4 |
| Contribution | 4 | 4.000 | 0.000 | 4-4 |
| Overall | 7 | 7.200 | 0.400 | 7-8 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- Novel and well-motivated: First to apply asymmetric SSL design (SimSiam/BYOL) to test-time entropy minimization, directly addressing the collapse problem in a principled manner.
- Comprehensive empirical evaluation: Tested across 5 vision architectures and 4 LLM reasoning benchmarks, covering diverse scenarios (label shifts, batch size 1, mixed corruptions, blind-spot adaptation, noise resistance).
- Strong results, especially on collapse-prone tiny models where prior methods fail (e.g., ViT-Small under noise).
- Efficient: Negligible overhead compared to Tent; faster than sample-selection methods like SAR and DeYO.
- Thorough ablations: Predictor design, stop-gradient necessity, learning rate sensitivity, α sensitivity, divergence choices, integration with prior methods.
- Plug-and-play nature: Improves existing TTA methods (EATA, DeYO).
- Theoretical analysis (Theorem 1) provides some formal grounding for the anti-collapse mechanism.
- Demonstrates broader applicability beyond vision to LLM reasoning incentivization.

### Weaknesses

- Theoretical analysis is somewhat informal: relies on standard assumptions (Lipschitz, smoothness) that may not hold in practice; the specific contribution of asymmetry to collapse prevention is not deeply analyzed; the 'absorber of biased signals' mechanism is supported mainly by correlation, not rigorous causation.
- Some experimental details are unclear: learning rate selection per model appears ad-hoc; LLM entropy computation and adaptation details are incomplete; 'center dominance' metric is not defined in the main text.
- Presentation issues: Table 4 appears to have swapped rows (ConvNeXt-Tiny vs ViT-Small); multi-branch baselines (SPA, REM, TTE) are only in the appendix, which weakens the claim of superiority over architectural alternatives.
- Collapse recovery is only partially successful (4/7 domains), and the conditions for success are not explained.
- LLM experiments use only one model (Llama3.1-8B), limiting generalizability claims.
- The paper lacks a deep failure case analysis—when might the alignment regularizer hurt or the asymmetry be insufficient?
- The data-free hyperparameter selection method (Appendix E.6) does not work for all architectures, leaving ηh selection partially unresolved.

### Questions

- How were the learning rates for each model determined? Were these tuned per model, and is the method sensitive to these choices in practice?
- In Table 4, the ConvNeXt-Tiny results appear to be swapped with ViT-Small. Could you clarify/correct this?
- The paper claims the predictor 'absorbs' biased shortcut signals. Can you provide more direct evidence (e.g., analysis of predictor parameters or gradient contributions) that demonstrates this absorption mechanism, rather than just correlation with imbalance ratio?
- In Theorem 1, what happens theoretically if the target branch itself starts to collapse? Does the alignment term still bound the entropy from below?
- What is the practical meaning of the hmin bound? Can you provide a numerical estimate for the ImageNet-C experiments?
- In the LLM experiments, how exactly is the entropy computed over token predictions (e.g., first 8 tokens, average over sequence)? How sensitive are the results to this choice?
- How does ZeroSiam behave when the test distribution shifts back to the source distribution (non-stationary streams)? The paper focuses on continuous shifts but does not address recovery.
- The fixed random predictor (Exp1 in Table 8) already improves over Tent. Could a fixed random predictor be sufficient in some scenarios? What is the specific role of making it learnable?
- In the blind-spot adaptation experiment, how does the alignment term prevent learning from misclassified samples? Is it purely due to the stop-gradient, or does the predictor also filter noisy gradients?
- For the noise resistance experiment, does the predictor learn a mapping from Gaussian noise features to high-entropy distributions, and does this generalize to real corrupted images?
- Why does integrating ZeroSiam with EATA/DeYO not beat plain ZeroSiam? Does sample selection become unnecessary when the alignment term is present?

### Limitations

- The theoretical analysis relies on simplifying assumptions (Lipschitz continuity, smoothness) that may not hold for deep networks; the practical implications of the bounds are unclear.
- Collapse recovery is only successful in 4 out of 7 domains, limiting the method's applicability for rescuing already-collapsed models.
- The method introduces an additional hyperparameter (α) and predictor learning rate (ηh); while shown to be robust, they still require tuning, and the data-free selection method is not universally applicable.
- LLM experiments are limited to a single model (Llama3.1-8B) and math reasoning tasks; broader claims about general reasoning improvements require more diverse evaluation.
- The method is evaluated on classification and reasoning tasks only; applicability to other tasks (e.g., segmentation, detection) is not explored.
- The paper does not deeply explore potential negative societal impacts, though the work is aimed at improving model robustness and appears benign. TTA methods could potentially amplify biases in test data, but this is not a major concern given the scope.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 247,103
- Cache-hit prompt tokens: 8,960
- Cache-miss prompt tokens: 238,143
- Completion tokens: 11,392
- Reasoning tokens reported: 0
- Total tokens: 258,495
- Estimated total: $0.03655487

Full individual reviews and raw JSON responses are in `review_bundle.json`.
