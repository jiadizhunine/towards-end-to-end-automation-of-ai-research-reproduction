# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B171.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **3/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 0, 'Reject': 5}
- Estimated API cost: **$0.032410**

## Final Meta-review

The paper analyzes the Muon optimizer with two momentum-based variance-reduced variants, Muon-MVR1 (one-gradient) and Muon-MVR2 (two-gradient). It claims ergodic convergence rates of O~(T^{-1/4}) for MVR1 and O~(T^{-1/3}) for MVR2 with fixed batch size, the latter claimed optimal, and last-iterate rates under the Polyak-Łojasiewicz condition. Experiments on CIFAR-10 and C4 compare with SGD, Adam/AdamW.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 2 | 2.200 | 0.400 | 2-3 |
| Quality | 1 | 1.400 | 0.490 | 1-2 |
| Clarity | 1 | 1.600 | 0.490 | 1-2 |
| Significance | 2 | 2.000 | 0.000 | 2-2 |
| Soundness | 1 | 1.400 | 0.490 | 1-2 |
| Presentation | 1 | 1.600 | 0.490 | 1-2 |
| Contribution | 2 | 1.800 | 0.400 | 1-2 |
| Overall | 3 | 3.200 | 0.748 | 2-4 |
| Confidence | 4 | 3.400 | 0.490 | 3-4 |

### Strengths

- Addresses a relevant gap between Muon's empirical success and theoretical guarantees.
- Provides a unified analysis framework for variance-reduced Muon variants, with MVR2 achieving a fixed-batch O~(T^{-1/3}) rate that improves on prior growing-batch analyses.
- Includes last-iterate convergence results under PL for Muon variants, a novel contribution.
- Experiments on both vision and language benchmarks show practical promise of the proposed variants.

### Weaknesses

- Lemma E.2, central to PL results, is not rigorous: the contradiction argument does not rule out isolated spikes or handle noise when G_t is small, so last-iterate bounds are unsubstantiated.
- The proof of Lemma C.3 / Theorem 3.2 contains incorrect constant derivations; e.g., squaring inequality issues with eta_t.
- Algorithm 1 pseudocode is missing, preventing reproduction and verification of exact update rules.
- Theorem statements oscillate between average squared gradient norm and average gradient norm; iteration complexity interpretation is unclear.
- The optimality claim is overstated: no formal lower-bound match is shown under the same oracle model (two gradients per iteration), and prior work already achieves O(T^{-1/3}) with growing batch.
- Experiments use gamma=0.1/0.05 for MVR2 whereas theory requires gamma=1; thus the experiments do not validate the theoretical setting.
- MVR2 uses two gradients per iteration but only iteration complexity is reported; total gradient complexity is not addressed.
- Presentation is poor: repeated assumptions/theorems, broken citations, typos, and missing algorithm box.

### Questions

- Can the authors provide a rigorous proof of Lemma E.2 that handles oscillating sequences and small values of G_t, or is the current contradiction argument irreparable?
- Could the authors clarify the exact convergence metric in Theorems 3.1 and 3.2: is it the average squared gradient norm or the average gradient norm?
- What is the precise lower-bound problem class from arjevani2023lower, and how does it account for MVR2's two-gradient oracle and orthogonalization?
- What is the full Algorithm 1 pseudocode, including initialization and orthogonalization, and how is it exactly implemented?
- Why do experiments use gamma values different from the theoretical gamma=1 for MVR2, and would the theory hold for those values?
- If complexity is measured in total stochastic gradient evaluations, does MVR2 still retain optimality? Provide the adjusted complexity.

### Limitations

- Theoretical results depend on exact orthogonalization and standard smoothness/variance assumptions that may not hold in large-scale deep learning.
- MVR2 doubles the gradient computation per iteration, but no wall-clock or memory overhead comparison is provided.
- The PL analysis is not reliable due to invalid proof steps, and even if repaired, rates may differ.
- No code is provided, and missing algorithm details hinder reproducibility.
- Experiments are small-scale and do not quantitatively validate the claimed convergence rates.
- No discussion of broader societal impacts, though none are apparent.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 170,830
- Cache-hit prompt tokens: 67,840
- Cache-miss prompt tokens: 102,990
- Completion tokens: 63,575
- Reasoning tokens reported: 56,521
- Total tokens: 234,405
- Estimated total: $0.03240955

Full individual reviews and raw JSON responses are in `review_bundle.json`.
