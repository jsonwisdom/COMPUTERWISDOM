# CI-FIRST front-door prototype

This is the live **development preview source** in PR #774, not the existing production front door. GitHub tree browsing will show HTML source; serve this directory over HTTP to interact with search/filter controls.

```bash
cd ci-first/live-builder-v0.4/site
python3 -m http.server 8000
# Open http://localhost:8000/
```

Zero dependencies; the browser reads local `projects.json` and `forest.json`. Tests:

```bash
python3 -m unittest discover -s ci-first/live-builder-v0.4/tests -p 'test_*.py' -v
node --check ci-first/live-builder-v0.4/site/app.js
```

## Sources and freshness

- `projects.json` was built from an authenticated GitHub repository listing for `jsonwisdom`. It contains **81 public** repository records and **no names or URLs from the 7 private repositories** seen in the same listing.
- `last_seen_utc` is when the API inventory was queried. It is **not** the repository's latest commit timestamp. `last_commit_utc` and `last_commit_sha` are now sourced for **all 65 nonempty public repositories** from the GitHub REST default-branch commit endpoint; all 16 empty repositories retain null. Commit dates may postdate the preserved inventory observation at `2026-11-19T04:45:29.213Z` because this is a later metadata enrichment, not a historical snapshot rewrite. Never infer commit dates from search-index order.
- `forest.json` derives its five candidate trees and three groves from [MERKLE_FOREST_SCHEMA_V1](https://github.com/jsonwisdom/COMPUTERWISDOM/blob/master/workflows/deepseek-zora-ingestion-v1/merkle_forest_schema_v1.json). The schema's `CANDIDATE` state is retained; `PENDING_HASH` is not a cryptographic root and is represented as unresolved work, not a fabricated leaf.
- Historical EIP-191 proof is linked from GitHub and has no connection to current signer privilege.
- Connected Google Drive documents remain private and are neither copied nor linked from the public index.

## Inclusion and safety

Wallet-free, no-cost access for anyone, with intentional opportunities for women and girls to learn and contribute. Public repository names are GitHub project slugs, not identities or endorsements. Do not publish personal details about minors; review any future contribution/publication before sharing personal information.

## Deployment boundary

An isolated **public Cloudflare Workers preview** is hosted at https://cw-ci-first-frontdoor-pr774-preview.jaywisdom44.workers.dev/ and currently serves the source-linked 65/65 metadata index. No production domain, DNS change, existing Pages replacement, signing, spending, protected-branch merge or on-chain transaction was performed. The preview is public and tagged noindex; noindex is not an access-control restriction. Production promotion must be authorized by the human owner.

## Follow-on work

1. Pagination and periodic authenticated GitHub listing refresh with public-only filter, observed timestamps, and audit receipt for snapshot creation.
2. Re-run the manual/branch metadata refresh workflow to generate a source-verified 65-repository artifact and commit it after passing CI; do not update the original snapshot timestamp.
3. Forest leaf inventory only from actual receipts; SHA-256 canonicalization with independently replayed roots and bridge receipts.
4. Accessibility and user testing on the preview, then human-approved site integration.
