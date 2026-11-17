# CI-FIRST · Quad Onion Resilience — Recovery Rehearsal V1

**State:** DRAFT, branch-scoped, read-only production verification and ephemeral staging-fixture destruction only.

## Evidence anchor
- Baseline: `workers/jsonwisdom-io/CI_FIRST_IO_PRODUCTION_BASELINE_20261108.json`.
- Production proof source: GitHub Actions [42530790545](https://github.com/jsonwisdom/COMPUTERWISDOM/actions/runs/42530790545), 2026-11-08T22:33:34Z.
- Three production sites: `proof.jsonwisdom.io`, `seymour.jsonwisdom.io`, `supreme.jsonwisdom.io`.
- GitHub copy of the original Cloudflare source: `workers/jsonwisdom-io/proof-origin.mjs` and `supreme-origin.mjs`, with source SHA-256 declared by `backend-contract.json`.
- These are two Worker applications, **not independent Cloudflare fault domains**.

## Pipeline (no authority)
1. **CI-FIRST:** `.github/workflows/ci-first-io-recovery-rehearsal.yml` runs on push, PR, or dispatch. Its actions are pinned to published immutable commit IDs and GitHub token permission is `contents:read`.
2. **VERIFY:** `scripts/audit/ci-first-io-production-regression.mjs` independently fetches the three public .io identity endpoints and homepage bytes plus each .com control. It rejects non-200, wrong service, wrong SHA-256, wrong byte length, redirects, oversized bodies, and unknown hostnames. The immutable expected digests were captured by an earlier, independent GitHub Actions run, rather than learned from current traffic.
3. **RECEIPT:** Creates `.ci-first/receipts/CI_FIRST_IO_REGRESSION_<commit>_<run>.json`. The workflow uploads these to an Actions artifact retained for 30 days; **Actions artifacts are not immutable forever nor copies across a different provider**. The fixed baseline is preserved within the Git commit. Promotion of a new expected digest requires explicit review.
4. **REPLAY / RECOVER (local rehearsal):** `scripts/audit/ci-first-io-staging-restore.mjs --simulate` validates preserved source bytes, copies them into an isolated OS temporary backup, intentionally deletes only a dummy staging response file, reconstructs the original response *from the temporary backup*, and compares response bytes and SHA-256 to the pinned production receipt. The test refuses mismatched bytes.
5. **FAIL CLOSED:** Negative unit tests mutate the response and demand FAIL. A staging Cloudflare upload has a separate `--stage-upload --role=proof|supreme` mode, *not called by the workflow*. It requires `CI_FIRST_STAGING_ONLY=1`, `CI_FIRST_DRILL_APPROVED=YES`, and a scoped Cloudflare token; it refuses any Worker already used by a custom domain or an existing same-name Worker. Its target is strictly `jw-io-recovery-drill-20261108-<role>`. It does not add a hostname or alter production.
6. **PROVE:** A full cross-substrate recovery certificate is **NOT** earned by the local rehearsal. Only a genuinely independent storage copy, isolated staging restore, independent Wolfram byte hash, and chain-anchored hash (if separately authorized) can earn that stronger claim.

## R2 and independence blocker
As of 2026-11-08, Cloudflare R2 bucket API returned **403 / 10042 (enable R2)**. Load-balancer monitors: **zero**. Do not delete R2/KV objects or claim that R2 is an independent provider. R2 is under Cloudflare; a second provider or offline archive is necessary for Cloudflare-wide recovery. Google Drive is an evidence-note location but is not yet proven to contain independently restorable *raw source and response bytes*.

## Base and settlement boundary
`jaywisdom.base.eth` and x402 are separate gates. An onchain hash is an existence attestation, **not** proof of a particular USDC settlement or that the holder currently controls a wallet. A final settlement-to-delivery certificate additionally needs a verified Base transaction receipt, USDC Transfer event and resource-byte binding. **No attestor deployment, signature, wallet transfer, or payment is in this draft.**

## Earnable verdicts
- Production HTTP comparison: PASS only after GitHub's independent network read and strict pinned SHA.
- Temporary staging-fixture restoration: PASS only if corrupt/destroy -> restore -> hash match succeeds from isolated temp backup.
- Real Cloudflare staging deployment and destructive restoration: UNKNOWN until separately authorized, executed, and independently probed.
- R2 backup/recovery: UNKNOWN (unavailable).
- Wolfram independent bytes: UNKNOWN until it fetches the raw bytes itself and computes their digest.
- Base attestation/payment: UNKNOWN (not attempted).
- Cross-provider disaster recovery and automatic failover: UNKNOWN (not yet implemented).

**CANON=false · AUTHORITY_CREATED=false.** No DNS, production Worker, R2, GitHub main, or wallet mutation.
