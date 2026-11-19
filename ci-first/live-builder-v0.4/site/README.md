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
- `last_seen_utc` is when the API inventory was queried. It is **not** the repository's latest commit timestamp. `last_commit_utc` is null until it is actually queried. Never infer it from index order.
- `forest.json` derives its five candidate trees and three groves from [MERKLE_FOREST_SCHEMA_V1](https://github.com/jsonwisdom/COMPUTERWISDOM/blob/master/workflows/deepseek-zora-ingestion-v1/merkle_forest_schema_v1.json). The schema's `CANDIDATE` state is retained; `PENDING_HASH` is not a cryptographic root and is represented as unresolved work, not a fabricated leaf.
- Historical EIP-191 proof is linked from GitHub and has no connection to current signer privilege.
- Connected Google Drive documents remain private and are neither copied nor linked from the public index.

## Inclusion and safety

Wallet-free, no-cost access for anyone, with intentional opportunities for women and girls to learn and contribute. Public repository names are GitHub project slugs, not identities or endorsements. Do not publish personal details about minors; review any future contribution/publication before sharing personal information.

## Deployment boundary

**No live domain, DNS, hosting, repository promotion, signing, spending, or protected-branch merge has been performed.** This is a working static prototype on a review branch. Promotion must be authorized by the human owner.

## Follow-on work

1. Pagination and periodic authenticated GitHub listing refresh with public-only filter, observed timestamps, and audit receipt for snapshot creation.
2. Last-commit timestamp collection per public repository, distinct from observed timestamp.
3. Forest leaf inventory only from actual receipts; SHA-256 canonicalization with independently replayed roots and bridge receipts.
4. Accessibility and user testing on the preview, then human-approved site integration.
