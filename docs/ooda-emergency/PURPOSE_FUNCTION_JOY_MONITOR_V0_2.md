# Computer Wisdom / OODA Emergency — Provenance, Persistence, Purpose → Function → JOY

**Status:** PROPOSED ACTION WORKFLOW (draft PR; not active until reviewed and merged).
**Authority:** false. No live emergency-feed integration or operational emergency authority.

## Naming and redundancy

- PRIMARY: `cw-ooda-emergency-50state-v01` at `https://emergency.jsonwisdom.com/api/v1/health`
- REPLICA: `cw-ooda-emergency-50state-replica-v01` at `https://emergency.jsonwisdom.io/api/v1/health`
- Both live within the **same Cloudflare account**: separate route/Worker, NOT cross-provider failover.

## Recurring GitHub Actions evidence

The proposed workflow `.github/workflows/cw-ooda-emergency-probe.yml` runs on the default branch's best-effort five-minute schedule. GitHub may delay or omit cron runs. `scripts/ooda_emergency_probe.py` sends GET-only HTTP health probes to both exact targets, stores status, timestamp, Cloudflare Ray, raw base64 response (public health only), SHA-256 of original response bytes, schema and coverage claims. No tokens, wallet signatures or payment calls.

Storage: per-run GitHub Actions artifacts with 90-day retention AND durable Git commit copies on the dedicated branch `ledger/ooda-emergency-observations`. The branch was created separately, so data writes never change `master`. GitHub token must be allowed to push to that branch; failure stays explicit. At 5-minute cadence, expect up to 288 Git commits/day: review volume and replace with periodic Merkle rollups before long-term scaling.

## Google Drive

Source documentation: existing Google Drive CI-FIRST reachability receipt.
**Automatic GitHub→Drive upload: NOT CONFIGURED**. A scheduled GitHub Action cannot use the ChatGPT connector authorization. A least-privilege service account or OAuth workflow and approved Drive destination are necessary.

For the Windows PC route, use `CW_PC_TwoRoutes_5min_Drive.ps1 -DriveMirrorPath <EXISTING-GOOGLE-DRIVE-DESKTOP-FOLDER>`. It copies each new local JSON receipt to the exact folder provided. That copy is **not proof of Google cloud sync** until the Drive client or connector readback confirms it. The PC must remain powered on and syncing.

## Mathematics / Wolfram

`scripts/ooda_verify.wl` independently recalculates SHA-256 from the saved response bytes and validates route parity, the 50-state health schema, and `authority_created=false`. Wolfram runtime is **not installed or configured in GitHub Actions** by this PR. A successful receipt hash proves byte consistency relative to supplied bytes; it does not authenticate a state EMA feed or establish any duty/command authority.

## Chats, memory, and JOY

ChatGPT conversations are NOT automatically accessible to the scheduled GitHub runner. Raw chats, family data, and secrets must never be published into the public evidence branch. For explicitly consented research decisions, save a **short, redacted decision receipt** with purpose/function/JOY fields and claims separately labeled `OBSERVED`, `INFERRED`, `UNKNOWN`. An AI transcript is not an authenticated government primary source.

Architecture source: [School of Wisdom Grand OODA Loop](https://github.com/jsonwisdom/JOY/blob/main/SCHOOL_OF_WISDOM_GRAND_OODA_LOOP_2026-11-07.md): COMPUTERWISDOM provenance and human oversight, AL boundary/protection, JOY student-owned and family-safe education. Students remain agents, not data objects.

## Open gates

- Repeated probes from two independent network regions over 24–72 hours: UNKNOWN (one GitHub runner location and one separately operated PC may provide distinct vantage points; verify actual region).
- Drive cloud sync of recurring receipts: NOT CONFIGURED.
- Per-state authentic FEMA / FCC / state EMA source bundles: 0 VERIFIED, per current health response.
- Congressional authority / emergency response command: NEVER CREATED.
- Stripe and wallet signing: OUT OF SCOPE.
