# AutoReviewer Reproduction v0.1.0

This is the first public release of the AutoReviewer reproduction accompanying
*Towards End-to-End Automation of AI Research*.

## Included

- A 200-paper ICLR 2026 strict all-initial evaluation.
- A 200-paper Nature-mixed evaluation using camera-ready text for accepted
  papers and initial-submission text for rejected papers.
- Five DeepSeek V4 Flash reviews and one Area Chair meta-review per paper.
- Frozen predictions, per-paper review bundles, evaluation JSON, independent
  audit reports, and Nature-style comparison tables.
- An English AutoReviewer report and a documented, reproducible protocol.
- A DeepSeek dashboard screenshot showing aggregate 30-day usage. The image
  contains an API-key alias only and does not expose the credential value.

## Important interpretation boundary

The two runs differ in manuscript version, extraction format, prompt/output
protocol, sampling configuration, and visible version-related cues. Their
difference is descriptive and is not a causal estimate of the camera-ready
effect.

## Security and data boundary

This release does not include API credentials, `.env` files, private
identifier-to-label mappings, source PDFs, the pinned parquet dataset, or
redistributable manuscript text. See `SECURITY.md` and `docs/PROTOCOL.md` before
running the API client.

## Verification

The release test suite contains 68 tests and passed before publication.
