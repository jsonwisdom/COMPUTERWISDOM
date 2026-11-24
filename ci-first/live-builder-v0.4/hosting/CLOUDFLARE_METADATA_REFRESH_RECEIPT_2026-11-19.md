# CI-FIRST Front Door — Metadata Refresh + Isolated Cloudflare Deployment Receipt

## Chain of evidence
- Google Drive private engineering contract: `DATA PARKOUR CI/OPS — METADATA V0.1` (source readback; not copied to public assets).
- Contract flow: QUESTION → METADATA → DRIVE_READBACK → GITHUB_MIRROR → RECEIPT.
- Immutable inventory observation: `2026-11-19T04:45:29.213Z` in `snapshot_utc` and every `last_seen_utc`.
- GitHub Actions refresh: [run 44463766598](https://github.com/jsonwisdom/COMPUTERWISDOM/actions/runs/44463766598) — SUCCESS, 65 default-branch REST API commits retrieved, validators passed and refreshed JSON committed on draft PR branch.
- Development metadata commit: `bfe5604fc2357c81e44f2e66ba77271fc8391a71` (branch `ci-first/live-builder-inclusive-v0.4`).
- Preview source commit: `5cfc9ee6797af01c09b1a3613f9dd236b299bafc`, including updated rendering of per-repository commit dates and source links.
- CI-FIRST Front Door [run 44463951331](https://github.com/jsonwisdom/COMPUTERWISDOM/actions/runs/44463951331) PASS; [verify run 44463951238](https://github.com/jsonwisdom/COMPUTERWISDOM/actions/runs/44463951238) PASS.

## Invariants
- Public repository count: 81; excluded private count: 7. Private names and URLs absent from `projects.json`.
- Nonempty public repositories: 65 of 65 have `last_commit_utc`, `last_commit_sha`, `last_commit_url` from source-backed default-branch commit endpoint.
- Empty public repositories: 16 of 16 retain null commit metadata.
- `last_commit_utc` is the committer date for the latest commit at the default branch at metadata read time. It can legitimately be later than the original observation timestamp.
- Forest remains five `CANDIDATE` trees, three groves, roots `PENDING_HASH`, never represented as cryptographically verified.
- No wallet signature repetition, keys, contract permissions or mutable storage included.

## Cloudflare deployment
- **Worker:** `cw-ci-first-frontdoor-pr774-preview`.
- **Preview URL:** https://cw-ci-first-frontdoor-pr774-preview.jaywisdom44.workers.dev/
- **Deployment ID:** `f87e922a-5933-4fbd-8793-da6af9a148cd`.
- **Version ID:** `224818d9-9d4f-4abb-a6c1-a487e212e7bd`.
- **Cloudflare API confirmation:** this version receives 100% of isolated Worker traffic; existing earlier deployment `f3f9c4b7-b6ad-44c3-9a84-f669295557e7` remains in deployment history.
- **Provider updated UTC:** `2026-11-19T05:17:02.776416Z`.
- **Runtime scope:** static GET/HEAD with no bindings, database, cookies, signup or payment requirements; noindex response headers and robots disallow; publicly addressable preview, not access-restricted.

### Five source asset blob SHAs from GitHub, fetched at source commit
- `ci-first/live-builder-v0.4/site/index.html` — `4ae551c93e5baf5574c096fe5f2e37bf58b46020`
- `ci-first/live-builder-v0.4/site/styles.css` — `74bcb8593886077c2e47b6377fdd324107f98849`
- `ci-first/live-builder-v0.4/site/app.js` — `6a2e0bfe6a1845e873fd829f957f4383c1bdd720`
- `ci-first/live-builder-v0.4/site/projects.json` — `9b9570bf7279b27563818181704b880a2cfb8df3`
- `ci-first/live-builder-v0.4/site/forest.json` — `714831a985066da9c4eb91d58f1ac8521ad32c77`

## Verification and limits
- GitHub Actions completed the default-branch source fetch and unit tests. GitHub API readback confirmed the updated metadata on the development branch.
- Cloudflare API confirmed the new deployment and version at 100%. Separate independent HTTP fetch attempts from the assistant runtime failed due network/DNS restrictions; **the current version's end-to-end external browser rendering remains unverified in that runtime**.
- No production DNS, existing Pages resources, protected branch merge, wallet signing, spending or on-chain write was performed.
- Keep draft PR #774 unmerged pending human promotion authorization. Historical original hosting receipt stays intact.
