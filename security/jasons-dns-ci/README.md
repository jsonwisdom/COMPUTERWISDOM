# Jason's DNS · CI-FIRST security proof harness

**Status:** build/test lane only, no automatic deployment or legal authority. Existing `FULLMATH Public 200 Audit` unchanged. Source: Supreme Seymour top-level invariant (`HUMAN_CONTROLLED=true`, `NO_FAKE_GREEN`).

## Checks

- **Math / fixtures**: Node built-in `node:test` verifies Wolfram SHA-256 (`empty`, `abc`), hypothetical 6-billion 64/128-bit birthday model, deterministic business-day timeline (Veterans Day), RFC3339 time gaps, duplicate-vs-collision classification, status precedence, human gate, and negative test fixtures for tampered bytes, payment exposure, and unsigned DNSSEC.
- **Public live**: GET-only checks across four domains pin exact response **bytes and SHA-256** of HTML/JS/CSS/engine (not HTTP multipart wrappers), CSP, `nosniff`, `/__health` response. Health claims are **self-reported** until binding inspection independently corroborates them.
- **RDAP**: GET registrar public records; reports transfer prohibition and unsigned/signed delegation independently; hashes complete returned RDAP bytes, but does not assert registrar MFA or account ownership.
- **Cloudflare private**: GET-only token with separate zone/account identifiers verifies DNSSEC, HTTPS policy, TLS minimum, Full Strict state, Worker count, expected Worker core names, routing and empty Worker bindings.
- **Human approval**: registrar MFA/recovery, external origin certificate validation, independent evidence archival and change authorization remain UNKNOWN until separately evidenced and approved. This harness never permits automatic deployment.

## Run

```bash
node --test security/jasons-dns-ci/JASONS_DNS_CI_TESTS.mjs
node security/jasons-dns-ci/JASONS_DNS_CI_RUNNER.mjs public ./jasons-dns-public-receipt.json
node security/jasons-dns-ci/JASONS_DNS_CI_RUNNER.mjs rdap ./jasons-dns-rdap-receipt.json
node security/jasons-dns-ci/JASONS_DNS_CI_RUNNER.mjs private ./jasons-dns-private-receipt.json
```

Only local test output/receipt files are written. Upstream methods are GET-only. A failed security state returns exit 1; missing evidence returns exit 2. Never interpret exit 0 from the public-only lane as full-security certification.

## Private GitHub Secrets (not in repo)

Read-only Cloudflare API credentials are optional for running public CI, required to complete private diagnostics:
`JASONS_DNS_CF_READ_ONLY`, `JASONS_DNS_CF_ACCOUNT_ID`, `JASONS_DNS_CF_ZONE_COM`, `JASONS_DNS_CF_ZONE_IO`. Give tokens the narrowest applicable read access. The workflow never prints tokens or account IDs. **Do not put account credentials, keys, signed wallet messages, personal DNS exhibits or payment artifacts in the repo.**

## Promotion gates

`PASS` may only describe tests actually performed. `FAIL` signals a demonstrable mismatch. `UNKNOWN` signals missing or untrusted evidence; no fourth status. A claim about stolen websites or Bitcoin is a separate, human-reviewed investigation. Payment authorization and x402 settle are explicitly **out of scope**. The workflow is designed to stay red/unknown while DNSSEC is off, TLS 1.0 is permitted, HTTPS enforcement is off, independent origin certificate checks are missing, or registrar/MFA/recovery evidence is absent. Human approval cannot be inferred from CI tests.

## Risk notes

- `Full (strict)` on zones with external origin servers must be separately staged and tested for certificates. Cloudflare Worker custom domains are not evidence that other origins are ready.
- `client transfer prohibited` RDAP is not proof of a registry lock, hardened registrar MFA, or safe recovery.
- A SHA-256 digest is a byte-integrity comparison, **not** proof of authorship, fraud, immutable retention or trustworthy timestamp.
- Calendar/date fixtures are examples, not legal deadline determinations; observed events need receipt IDs and jurisdiction-specific notice laws.
- GitHub Actions may lack network access or secrets. Such outcomes are UNKNOWN, never silent PASS.
