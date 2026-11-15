# CI-FIRST — 50-State Emergency Worker Public Reachability Receipt

**Recorded:** 2026-11-14 America/New_York (external HTTP response at 2026-11-15T01:20:22Z)
**Object:** `cw-ooda-emergency-50state-v01`
**Domain:** https://emergency.jsonwisdom.com
**Health URL:** https://emergency.jsonwisdom.com/api/v1/health
**Classification:** Public read-only research scaffold; not emergency dispatch and not government-affiliated.

## Independent external observations — Wolfram Language URLRead

| Method | Path | HTTP | Evidence |
| --- | --- | --- | --- |
| GET | `/` | 200 | HTML homepage, 6,310-character body |
| GET | `/api/v1/health` | 200 | JSON schema `cw-ooda-emergency-estate/0.1`; `state_count=50`, `authority_created=false`, `live_alerts=false`, `source_bundles_verified=0` |
| GET | `/api/v1/states` | 200 | JSON list of jurisdiction records |
| GET | `/api/v1/state/AL` | 200 | Alabama record |
| GET | `/api/v1/state/DC` | 200 | DC record (district separate) |
| GET | `/api/v1/next` | 200 | Open evidence-task queue |
| POST | `/api/v1/health` | 405 | `{"error":"READ_ONLY","authority_created":false}` |

**HTTP response headers for health GET:** `server: cloudflare`, `content-type: application/json;charset=utf-8`, `cf-ray: a5aa6ed9a92f111c-ORD`, `date: Sun, 15 Nov 2026 01:20:22 GMT`.

### Cloudflare control-plane readback

- Script: `cw-ooda-emergency-50state-v01`
- Deployment: `43f03540-d808-4378-bba0-8d9fe7c35f84`
- Version: `bb458f55-f4f4-43a7-b534-f2a3bfa2d911` at 100% weight
- `emergency.jsonwisdom.com` Worker Domain: enabled, production, routes to exact script.

## CI-FIRST disposition

- **PASS (observed at stated time):** target custom domain answered direct HTTPS GET 200 with expected Worker-specific JSON schema; separate paths answered 200; POST answered 405.
- **PASS (Cloudflare metadata):** named script, 100% deployment, custom-domain assignment.
- **UNKNOWN:** long-term uptime, availability from arbitrary networks, page rendering in every browser, real-time official agency feed ingestion, external-source provenance for state emergency records, jurisdiction-specific readiness, congressional agency integration.
- **NOT CONFIGURED / disclosed in health response:** live alerts; source bundles verified = 0. Do not promote those claims.
- **NO FINANCIAL AUTHORITY:** Stripe/Coinbase/x402 are outside public-read-only emergency evidence checks.

## Earlier access errors — explanation

A different Cloudflare-tool sandbox `fetch()` returned HTTP 403 `Forbidden: requests to [hostname] are not allowed` for four unrelated domains, including `example.com` and existing `matrix.jsonwisdom.com`. This is a client-tool egress restriction, not sufficient proof of target Worker failure. A separate restricted container could not resolve DNS; public search had no indexed match. `SEARCH_MISS != ABSENCE`. These limitations coexist with the later genuine independent direct-HTTP 200 receipt.

## Scope / next evidence gate

Treat this as a **single successful public HTTP observation**, not an uptime guarantee. Next gate is authenticated per-state public-source ingestion (FEMA/state EMA/FCC/etc.), provenance, freshness, time-window labeling, and human-governed congressional oversight, all fail-closed on missing records. No operational commands, dispatch actions, payments, wallet actions, or government authority established.

## November 15 UTC — secondary route and mathematical replay

A second independent script in the **same Cloudflare account** was deployed as `cw-ooda-emergency-50state-replica-v01` and bound to `https://emergency.jsonwisdom.io/api/v1/health`.

Wolfram URLRead tested BOTH exact endpoints from its external runtime: **HTTP 200** each, matched `cw-ooda-emergency-estate/0.1`, confirmed state count 50, and produced matching SHA-256 of the returned JSON bodies:

`8257726cd3865a73be64c09a6c1c749bd09517463d6e5f4fe385a532cf459fdc`

The replay returned **5/5 verification tests succeeded**. Cloudflare Rays recorded: primary `a5aa879f4b596164-ORD`, replica `a5aa87a0c9a4c6f1-ORD`. A separate synthetic Wolfram JSON/base64 replay verified the digest and schema comparison logic, but did not authenticate third-party agency records.

A five-minute GitHub Action and portable Windows/Google Drive desktop mirror are **proposed in this draft PR; NOT ACTIVATED**. GitHub ledger branch `ledger/ooda-emergency-observations` has been created. An action run and a successful Google Drive cloud sync are not yet evidenced.

Cross-provider redundancy, 24–72-hour uptime, independent-geography coverage, actual emergency feed ingestion, and 50-state source coverage remain **UNKNOWN/NOT ESTABLISHED**. The recorded second route is a separate Worker and domain, **not** independent infrastructure.
