# GOBLIN_VERIFIER_V0_1

Status: SPEC_FIRST  
Issue: #82  
Parent: #67  
Authority: false  
Membrane: HOLDS

## Purpose

`GOBLIN_VERIFIER_V0_1` defines a bounded transition checker for the Constitutional Game Stack v0.2.

The verifier gates transitions. It does not adjudicate truth.

## Allowed Outputs

- `PASS_TO_EXISTENCE_CHECK`
- `NEEDS_RECEIPT`
- `GHOST_PROMOTION_BLOCKED`
- `DUPLICATE_FOUND`
- `DISPUTE_REQUIRED`
- `INVALID_TRANSITION`

## Core Invariant

`NO_SILENT_CATEGORY_PROMOTION`

The verifier must never upgrade observation, witness output, score, anchor, or agent action into verified truth or authority.

## Boundary Rules

- Observations may be surfaced.
- Claims may be routed.
- Missing receipts require `NEEDS_RECEIPT`.
- Ghost promotion attempts require `GHOST_PROMOTION_BLOCKED`.
- Invalid transitions require `INVALID_TRANSITION`.
- Contradictions or unresolved conflicts require `DISPUTE_REQUIRED`.
- Duplicate surfaces require `DUPLICATE_FOUND`.

## Non-Goals

- No runtime automation yet
- No external witness calls
- No scoring implementation
- No wallet signing
- No Base anchoring
- No ENS changes
- No social-credit surface
- No truth-finality claim
- No autonomous merge authority

## Closing Rule

Goblin Verifier gates transitions only. Humans merge. Authority remains false.

## Goblin Precedent Index Integration (V0.1)

The canonical source for goblin classification, receipts, and checklists is now:

**`docs/GOBLIN_PRECEDENT_INDEX_V0_1.md`**

This index defines:

- 10 goblin precedents (GC-001 through GC-010)
- Corresponding receipts (FR-001 through FR-010)
- Executable checklists (CL-001 through CL-010)
- Symptom lookup table
- Intercept priority order
- Circuit breaker protocol (GC-010)

### Machine Verification

The index is machine-verifiable via:

| Artifact | Path | Purpose |
|---|---|---|
| JSON Schema | `schemas/goblin_precedent_index.v0_1.schema.json` | Validates structure, authority, Trinity, goblin count, cascade rule |
| Test suite | `tests/test_goblin_precedent_index_v0_1.py` | Asserts all IDs present, authority false, trigger semantics |
| Hash manifest | `receipts/goblin_precedent_index_hash_manifest_v0_1.json` | Maps receipts to content hashes for on-chain anchoring |

All changes to goblin precedents must pass:

1. Schema validation
2. Test suite
3. CI workflow (`.github/workflows/verify.yml`)

### Observer-Only Doctrine

The verifier enforces `authority: false` — it can witness and report, but never block or modify state. The Court advises; the operator decides.

For details, see PR #172 and the merged commit `c7f7c4d`.
