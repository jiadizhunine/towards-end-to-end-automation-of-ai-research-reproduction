<div align="center">

**English** | [简体中文](./SECURITY.md)

</div>

# Security and responsible use

## API credentials

Never commit a DeepSeek API key or any other credential. The client reads
`DEEPSEEK_API_KEY` from the process environment. Use the ignored local `.env`
file only on a trusted machine:

```bash
cp .env.example .env
chmod 600 .env
```

The repository intentionally ignores `.env`, `.env.*`, credential files, raw
datasets, manuscript PDFs, extracted manuscript text, and local run directories.
The example file contains only a placeholder.

Before publishing a fork, inspect all tracked content and history:

```bash
git grep -nEi '(api[_-]?key|authorization|bearer|secret|token)'
git log -p --all -- . ':!*.png'
```

If a real key is ever committed, revoke it immediately at the provider, remove it
from history, and issue a replacement. Deleting only the latest file is not
sufficient.

## Manuscripts and labels

Manuscript PDFs and dataset snapshots may be subject to third-party terms. This
repository records hashes and retrieval code but does not redistribute those
files. Private mappings connect blind IDs to source identities and final labels;
they should remain outside the formal review process and outside public forks
unless their redistribution rights and disclosure purpose have been reviewed.

## Network boundary

The AutoReviewer does not expose browser, search, retrieval, RAG, shell, or URL
fetching to the model. The runtime still uses network transport to call the
configured DeepSeek `/chat/completions` endpoint. Application-level URL checks are
not an operating-system firewall.

## High-stakes use

This software is an evaluation artifact and research prototype. Do not use its
Accept/Reject output as an autonomous publication decision, scientific-quality
certificate, misconduct finding, hiring decision, or substitute for qualified
human review.

## Reporting security issues

Open a GitHub security advisory for repository vulnerabilities. Do not paste API
keys, unpublished manuscripts, or private mappings into a public issue.
