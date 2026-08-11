# AutoReviewer Report

> Calibration warning: this run reproduces the Nature pipeline structure, but substitutes
> DeepSeek V4 Flash for the paper's validated o4-mini model. Its scores are not human-calibrated.

- Paper: B089.txt
- Model: deepseek-v4-flash
- Final decision: **Reject**
- Overall: **4/10**
- Confidence: **4/5**
- Independent decisions: {'Accept': 1, 'Reject': 4}
- Estimated API cost: **$0.018263**

## Final Meta-review

The paper introduces a two-stage, prompt-based framework for retrosynthesis using general-purpose LLMs without task-specific fine-tuning. Stage one is a zero-shot 'position model' that analyzes atom-mapped SMILES to identify and rank disconnection sites, assign reaction names/classes, importance scores, and chemical rationales. Stage two is an optional few-shot 'transition model' that converts a selected site into reactant sets using up to five exemplars of the named reaction. The authors evaluate on a balanced subsample of USPTO50k (USPTO-LLM) across many open and closed LLMs, and on five expert-validated drug discovery molecules. They report high accuracy on custom positional/template/reactant metrics, and ablations showing the importance of reaction-name anchoring, prompt detail, and in-context examples.

### Scores

| Dimension | Final | Five-review mean | SD | Range |
|---|---:|---:|---:|---:|
| Originality | 3 | 3.000 | 0.000 | 3-3 |
| Quality | 2 | 2.200 | 0.400 | 2-3 |
| Clarity | 3 | 2.600 | 0.490 | 2-3 |
| Significance | 3 | 2.600 | 0.490 | 2-3 |
| Soundness | 2 | 2.200 | 0.400 | 2-3 |
| Presentation | 3 | 2.600 | 0.490 | 2-3 |
| Contribution | 3 | 2.600 | 0.490 | 2-3 |
| Overall | 4 | 4.600 | 0.800 | 4-6 |
| Confidence | 4 | 4.000 | 0.000 | 4-4 |

### Strengths

- The atom-map-anchored reasoning framework is a novel and intuitive way to let LLMs reason about molecular structure without task-specific training, providing explainable predictions.
- The paper evaluates a broad range of LLMs (open/closed, reasoning/non-reasoning, chemistry-specialized) and shows clear scaling trends, which is useful for practitioners.
- Expert validation on real drug discovery molecules adds practical relevance and yields valuable failure-mode analyses that go beyond standard benchmark accuracy.
- Ablation studies isolate the contributions of reaction names, prompt detail, examples, and chain-of-thought reasoning to the overall performance.
- The writing is generally clear, with formal definitions of the framework, metrics, and dataset preprocessing steps.
- The authors release their labeled data and reaction ontology, which could facilitate reproducibility and future work.

### Weaknesses

- The custom evaluation metrics are unusually lenient and do not align with standard retrosynthesis benchmarks: partial match only requires a non-empty overlap with the ground-truth site, template accuracy uses a 75% atom-overlap threshold, and reaction accuracy is computed conditional on a partial position match, which inflates apparent performance.
- No comparison is made against supervised retrosynthesis baselines (e.g., transformer, graph neural network, or fine-tuned LLM) using the same data, nor against prior LLM retrosynthesis results with standard top-k exact-match accuracy; the claim of 'high success rates' is therefore not contextualized.
- The transition model is evaluated using ground-truth disconnection positions and reaction names rather than the predicted ones, so the reported reactant accuracy does not reflect end-to-end performance; the position model's reaction-name accuracy is only 40-47%.
- The expert validation is limited to five molecules, uses subjective questions without inter-annotator reliability, and reveals low recovery of the actually performed reactions (25.4% on P5), so the practical utility is less clear than the aggregated high percentages suggest.
- Critical prompts are redacted in the submitted version, and the description of post-processing, output parsing, and failure handling is incomplete, making exact reproduction difficult.
- The claim of operating 'without labeled training data' is overstated: the transition model requires up to five labeled reaction examples per reaction class, and the reaction ontology is constructed from labeled training data.
- The method depends on atom-mapped SMILES, but many real-world molecules lack such annotations; the sequential atom counting used in the case study may not be chemically valid for arbitrary molecules.
- No ranking or calibration of the multiple predictions is provided; a model that returns many candidates (e.g., an average of 15.3 for Gemini Flash) is not directly useful without a reliable ranking mechanism.

### Questions

- How do the proposed models compare to standard single-step retrosynthesis baselines (e.g., Chemformer, GraphRetro, Retroformer) on the same USPTO50k test split using top-1 and top-10 exact-match accuracy?
- What is the end-to-end accuracy on USPTO-LLM when the transition model is fed the top-predicted position and reaction from the position model, rather than the ground truth?
- What is the unconditional reaction accuracy (without conditioning on partial position match), and how would random or trivial baselines score on the partial-match and Jaccard metrics?
- How is the ground-truth disconnection site S_gt defined for USPTO50k, and could a model trivially guess the reaction center by identifying atoms with altered bonding without chemical reasoning?
- For molecules without pre-existing atom maps, how does sequential atom numbering in canonical SMILES preserve chemical semantics, and how does it affect the model's ability to reason about equivalent atoms?
- How are the up-to-five in-context examples selected from the training set? Randomly, by similarity, or by reaction class? Does example selection affect accuracy?
- In the expert study, were all 63 position predictions used to create the 19 transition evaluations? What was the selection criterion, and could this curation bias the reported accuracies?
- Will the full prompts (Position Model and Transition Model) be released without redaction, including all formatting instructions and few-shot example selection criteria?
- The abstract describes stage one as 'one-shot' but the methods call it zero-shot; what exactly does 'one-shot' mean in this context?
- How often do the atom-map indices provided to the model actually correspond to the ground-truth reaction center in the corrected USPTO50k data, and what is the impact of atom-mapping errors on downstream performance?

### Limitations

- The evaluation is primarily based on custom, often lenient metrics; standard exact-match and ranking metrics are missing, limiting comparability with prior work.
- The expert validation sample is small (5 molecules, 63 position predictions, 19 selected positions) and subjective, which limits statistical generalizability.
- Best performance requires large proprietary models (e.g., Gemini 2.5 Pro), while smaller open models are substantially weaker, limiting practical accessibility and reproducibility.
- The method relies on a known reaction ontology and named reaction classes; for reactions outside this ontology or novel chemistry, performance drops significantly (reactant accuracy from ~75% to ~30%).
- The framework is demonstrated only for single-step retrosynthesis; extension to multistep synthesis is not shown.
- No analysis of stereochemical correctness or atom-mapping consistency in predicted reactants is provided.
- The paper acknowledges academic benchmark contamination risk but does not fully mitigate it; the expert set is small and may still be biased by the authors' selection of molecules.
- Inference uses large proprietary LLMs, which may be costly and not readily accessible to all researchers.

### Ethics

Ethical concerns flagged: **False**

## Usage and Cost

- Requests: 6
- Prompt tokens: 96,715
- Cache-hit prompt tokens: 4,096
- Cache-miss prompt tokens: 92,619
- Completion tokens: 18,876
- Reasoning tokens reported: 11,757
- Total tokens: 115,591
- Estimated total: $0.01826341

Full individual reviews and raw JSON responses are in `review_bundle.json`.
