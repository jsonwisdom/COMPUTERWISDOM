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
