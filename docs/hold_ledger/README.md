# JSONWisdom — one shared hold ledger (pilot V0.1)

**Policy ID:** `NO_UNRECEIPTED_PROMOTION_V0_1`  
**Canonical ledger:** [HOLD_LEDGER_V0_1.json](./HOLD_LEDGER_V0_1.json) — this file is the **only authoritative data table** for the pilot. This README states the rules, not a second ledger.  
**Scope:** five inspected evidence-bound instances from **five distinct public repositories**; **NOT** the complete 87-repository inventory and **NOT** five independently assigned HOLDs.  
**Publication:** GitHub draft PR review branch; no merge, deployment, deletion, archive, or cross-repository sync executed. `authority_created=false`.

## Why the statuses differ

The original source records remain untouched, including their exact HOLD, pending, or not-admitted expressions. An operational ledger applies a separate **coordination status**:

- `HOLD`: a concrete missing evidence artifact, objective release criterion, and specifically accepted accountable owner exist, but the evidence has not cleared.
- `STOP_TRIAGE`: an owner OR release criterion is not established. Requires a human keep/hold/archive/abandon/scope decision, but **is not an automatic terminal action**.
- `RELEASE_REVIEW`: evidence has been independently checked, and a human approval is still required; this is **not** automatic promotion.
- `ARCHIVED`, `ABANDONED`, `CLOSED_VERIFIED`, `MERGED_IMPORTED`: terminal operational outcomes only with a human decision receipt and linkable audit event. Never infer from staleness or inactivity.

`ORIGINAL_SOURCE_STATUS != COORDINATION_STATUS`; `POLICY_ONCE != FACTS_COLLAPSED`.

## One row, one scoped missing-evidence instance

Each JSON entry records a stable hold ID; repository; case/object; source status; exact source URL and blob; primary bucket; missing-evidence reason and **specific release artifact**; release-path ID; **accepted owner with assignment receipt**; genuine opened_at or null; **USD cost/day with cost basis** or null; discovery/review date; current coordination state; and authorization receipt for terminal decisions.

The account or repository owner is **not** silently substituted for the accountable hold owner. The source document's date is not assumed to be its original opened date. `cost_per_day_usd:null` does not mean $0/day. Any individual can decline an assignment.

## Five classified source examples

Use the canonical JSON rather than copying rows into another independent spreadsheet:
- `HOLD-001` — COMPUTERWISDOM original-72 historical manifest integrity; release path HISTORICAL_SOURCE_PRESERVATION.
- `HOLD-002` — JOY live-site evidence and distinct consent gate; LIVE_DEPLOYMENT_WITNESS.
- `HOLD-003` — CITIZEN_ROOT undefined RAIL_3 definition; DEFINITION_OR_AUTHORIZED_GENERATION.
- `HOLD-004` — provenance-audit-kit documented SSA 403 not-admitted capture; LAWFUL_PUBLIC_SOURCE_ACQUISITION.
- `HOLD-005` — receipts-engine-v1 telemetry envelope awaiting qualified observations; TELEMETRY_SEAL_REPLAY.

All five are `STOP_TRIAGE` **in this new operational ledger only** because no individualized owner-assignment receipt was found in the inspected source. Their original source postures stay untouched. These rows are *pilot findings*, not a claim that all related work is stalled or all evidence missing across other branches/surfaces.

## Group by release path, not repository

Batch `HISTORICAL_SOURCE_PRESERVATION`, `LIVE_DEPLOYMENT_WITNESS`, `DEFINITION_OR_AUTHORIZED_GENERATION`, `LAWFUL_PUBLIC_SOURCE_ACQUISITION`, and `TELEMETRY_SEAL_REPLAY` only when their **evidence classes and authorizations actually match**. A shared procedure cannot overwrite a per-case proof requirement. Privacy/licensing/integrity must be checked for each source object.

## Weekly discipline

- Week 0: triage the five rows; solicit owner acceptance and concrete evidence. No guessed owners.
- Every seven days: flag `last_reviewed_at` older than 14 days and record movement or no movement with timestamps.
- After two completed weekly cycles with no individually assigned owner, escalate to human `KEEP_HOLD / RE-SCOPE / ARCHIVE / ABANDON` review. No auto-kill.
- Batch release procedures after primary evidence is captured; independent verifier examines each receipt. Human authorization is necessary for consequential changes.
- Expand 5 → 20 → current inventory only through **observed individual cases**, never by assuming 87 automatically have holds. Leave unrelated repositories unclassified until inspected.
- A scheduled scan **cannot silently change status or approve release**. Do not count automated reminders as validated evidence.

## Constitutional and privacy guardrails

`RECEIPT_EXISTS != CLAIM_PROVEN`  
`MISSING_OWNER != PERMISSION_TO_DELETE`  
`STOP_TRIAGE != ORIGINAL_RECORD_REWRITE`  
`UNKNOWN_COST != ZERO_COST`  
`NO_EVIDENCE != RELEASE`  
`GITHUB_ACCOUNT_OWNER != ASSIGNED_CASE_OWNER`  
`GITHUB_CURRENT_ENUMERATION != ORIGINAL_72_MANIFEST`

Public ledger includes only public source references and no private repo names, PII, wallet secret, family biographies, or access credentials. Private holds require a private ledger or redacted reference, not a leak into this public file.

## Validation and reproducibility

Run `python scripts/validate_hold_ledger.py --self-test`. This proves local schema, state, counting, and policy invariants; it **does not** establish that the evidence artifacts are complete or current, and it does not assign owners. The existing protected GitHub `verify` check is extended to run the validator on draft PR updates.
