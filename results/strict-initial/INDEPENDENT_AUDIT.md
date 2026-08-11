# Independent audit record

Audit date: 2026-08-11

## Verdict

PASS. The approved blind corpus and the canonical 200-paper result chain have no
hard blocker. The audit was performed independently and the result-package audit
did not read the private mapping, ground-truth labels, `.env`, `evaluation.json`,
or `real_ratio_report.json`.

## Blind-corpus audit

- 200 papers: 78 Accept and 122 Reject in the private mapping; the 160-paper
  extension adds 58 Accept and 102 Reject.
- The additions are the uninterrupted class-specific hash ranks required by the
  frozen seed. No manual replacements were made.
- All source IDs, blind-text hashes, manifest hashes, uniqueness checks, and
  `0700`/`0600` permissions passed.
- Exact-title, high-coverage title n-gram, author and author-alias, self paper ID,
  arXiv ID, URL, email, domain, DOI, ORCID, OpenReview, GitHub, ICLR, lifecycle,
  and decision-label scans produced zero hard findings.
- Targeted rechecks of all previously blocked papers passed. Controlled domain
  redaction removed 240 sensitive occurrences while preserving 21,815 ordinary
  `et al.` occurrences; the largest text reduction was 4.76% and was attributable
  to sensitive sections rather than scientific content.

## Canonical result-chain audit

- `B001` through `B200` are complete; each directory has one canonical
  `review_bundle.json` and one readable `review.md`, with no symlinks or extras.
- Blind manifest SHA-256:
  `db65de8b2cf3d6c164d7f40496d7c96effe9b8da4f97b01dfc5548fd2fa5d774`.
- Frozen predictions SHA-256:
  `892b4a407badc29cbd065fc5eefcf1784948edb0e26156e28620e9720bc6cbb1`.
- All 200 blind-text hashes and bundle hashes match the manifests and on-disk
  bytes. All 1,200 response IDs are unique; every raw response parses to the
  stored structured review; the Area Chair output is the final review.
- Configuration is uniform: `deepseek-v4-flash`, reasoning effort `max`, five
  reviewers plus one Area Chair, maximum three attempts, and no reviewer tools.
- Frozen predictions contain exactly 200 IDs and match the canonical final
  decisions and five-reviewer Overall score vectors. The frozen distribution is
  55 Accept and 145 Reject.

## Usage and cost

- Successful calls: 1,200; attempts: 1,212.
- Successful-response tokens: 29,178,389.
- Recomputed successful-response cost: `$4.61247628`.
- Historical reuse: 29 papers, 174 successful calls, 176 attempts, 4,890,581
  tokens, `$0.76860367`.
- Fresh work: 171 papers, 1,026 successful calls, 1,036 attempts, 24,287,808
  tokens, `$3.84387261`.
- Failed retries did not persist usage, so the cost above is a verifiable lower
  bound and not the exact provider invoice.

## Non-blocking provenance limitation

`review.md` is a human-readable derivative. Its semantic content was checked and
all 200 Markdown files are unique, but its SHA-256 is not recorded in the run
manifest or frozen predictions. Therefore only `review_bundle.json` belongs to
the cryptographically committed authoritative chain.
