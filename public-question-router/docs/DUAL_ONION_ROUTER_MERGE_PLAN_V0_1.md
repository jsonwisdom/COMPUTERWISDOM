# Dual Onion + Public Question Router Merge Plan v0.1

Status: DRAFT / HUMAN-MERGE-ONLY

```text
AUTHORITY_CREATED = FALSE
MERGE_AUTHORITY = HUMAN
DRAFT != RELEASE
CI_PASS != LEGAL_VALIDATION
```

## Current stack

```text
master
  ↑
agent/reversereplay-azure-nsa-rendition-v0-1
  ↑
agent/public-question-authority-router-v0-1
     PR #505
```

PR #505 is intentionally stacked on the ReverseReplayAzureNSA/rendition integration branch rather than directly on `master`.

## Promotion objective

Promote the smallest coherent architecture while preserving replayable history and preventing the router from silently importing unreviewed assumptions.

## Gate A — Parent integration review

Before PR #505 can become a clean master-bound change, review the parent branch for:

- Dual Onion compatibility;
- CIA/DOJ/OIG jurisdiction boundaries;
- infrastructure-vs-authority distinctions;
- no unsupported current-person allegation;
- `AIRCRAFT_USE != AUTHORITY`;
- `FLIGHT_LOG != LEGAL_JUSTIFICATION`;
- `AUTHORITY_CREATED = FALSE`.

Disposition: `PASS | HOLD | CONFLICT | REJECT`.

## Gate B — Router mechanical review

Require exact-head verification of:

- question-ID validation;
- deterministic directory materialization;
- 24-hour clock arithmetic;
- separation of portal SLA from legal clocks;
- immutable/append-only historical status behavior;
- Q-object schema validation;
- authority candidate status cannot self-promote from AI proposal;
- `NO_RESPONSE_OBSERVED != GUILT`.

## Gate C — Source-law review

Bind primary/official sources for every legal-clock example admitted into documentation.

At minimum:

- DOJ/OIP FOIA response-time guidance;
- PACER public-record availability guidance.

Source examples do not become universal legal advice; jurisdiction-specific clocks remain separate.

## Gate D — OpenAI optional layer

The deterministic router must continue to run with:

```text
MODEL_REQUIRED = FALSE
API_KEY_REQUIRED = FALSE
```

If an OpenAI routing sidecar is later added, it must emit candidate nodes/questions only and may not write PASS/HOLD/CONFLICT/REJECT or create authority.

## Recommended merge sequence

### Step 1 — Freeze parent head

Record the exact parent branch SHA and its review disposition.

### Step 2 — Give parent a reviewable PR surface

If not already present, open a draft PR from `agent/reversereplay-azure-nsa-rendition-v0-1` to `master` so the base of PR #505 is independently inspectable.

### Step 3 — Verify parent

Do not merge parent until its bounded architecture and source references survive review.

### Step 4 — Rebase/retarget router after parent promotion

After the parent is merged, retarget or rebase PR #505 onto the resulting `master` state without rewriting the historical evidence of the original stack.

### Step 5 — Exact-head router CI

Run CI on the new PR #505 exact head. Prior green runs do not pay for a changed head.

### Step 6 — Human review

Review:

- changed files;
- test coverage;
- schema/version compatibility;
- public wording;
- legal-clock boundaries;
- authority membranes.

### Step 7 — Merge router

Merge only after the exact head is green and the human reviewer accepts the scope.

### Step 8 — Post-merge replay receipt

Record:

```text
MERGE_COMMIT
SOURCE PR
EXACT REVIEWED HEAD
CI RUN / JOB
DRIVE MIRROR
SCHEMA VERSION
AUTHORITY_CREATED = FALSE
```

## Rollback / conflict rule

If parent review fails, PR #505 remains intact as a stacked historical artifact. It may be restacked onto a corrected parent only through an explicit new comparison; do not pretend the original base never existed.

## Public-release gate

A merged router is not automatically a public government-facing service.

```text
MERGED_CODE != DEPLOYED_PORTAL
DEPLOYED_PORTAL != GOVERNMENT ENDORSEMENT
PUBLIC QUESTION != OFFICIAL FILING
ROUTED QUESTION != FOIA REQUEST
ROUTED QUESTION != OIG COMPLAINT
ROUTED QUESTION != COURT FILING
```

Each external submission mechanism must have its own explicit connector, terms, jurisdiction, and receipt.

## Core rule

**Promote architecture in dependency order. Re-run receipts after every changed head. Never let a green child hide an unreviewed parent.**
