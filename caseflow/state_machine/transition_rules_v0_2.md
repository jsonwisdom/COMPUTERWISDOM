# CASEFLOW_TRANSITION_RULES_V0_2

## Status

```json
{
  "artifact": "CASEFLOW_TRANSITION_RULES_V0_2",
  "implements": "Issue #68",
  "phase": "RULES_v0.2",
  "authority": false,
  "membrane": "HOLDS"
}
```

## Purpose

Define the allowed state transitions, actors, required checks, and membrane behavior for the Constitutional Game Stack v0.2 Caseflow State Machine.

This artifact complements `caseflow/state_machine/schema_v0_2.json`.

## Canonical States

- `DRAFT`
- `UNDER_REVIEW`
- `GOVERNANCE_CHECK`
- `APPROVED`
- `IN_PROGRESS`
- `MERGED`
- `REJECTED`
- `REPLAY`
- `DISPUTED`

## Allowed Transition Table

| From | To | Allowed Actors | Required Checks | Membrane Hold |
|---|---|---|---|---|
| `DRAFT` | `UNDER_REVIEW` | HUMAN, AGENT | source_declared, authority_false | false |
| `DRAFT` | `REJECTED` | HUMAN, MEMBRANE | rejection_reason_present | true |
| `UNDER_REVIEW` | `GOVERNANCE_CHECK` | HUMAN, AGENT, GROK_WITNESS, OBSERVER | review_context_present, receipt_or_pointer_present | true |
| `UNDER_REVIEW` | `DISPUTED` | HUMAN, AGENT, GROK_WITNESS, OBSERVER | contradiction_or_missing_receipt_present | true |
| `UNDER_REVIEW` | `REJECTED` | HUMAN, MEMBRANE | rejection_reason_present | true |
| `GOVERNANCE_CHECK` | `APPROVED` | HUMAN, MEMBRANE | authority_false, boundary_honest, required_receipts_present | true |
| `GOVERNANCE_CHECK` | `DISPUTED` | HUMAN, MEMBRANE | ghost_promotion_or_invalid_transition_detected | true |
| `GOVERNANCE_CHECK` | `REJECTED` | HUMAN, MEMBRANE | failed_required_check, rejection_reason_present | true |
| `APPROVED` | `IN_PROGRESS` | HUMAN, AGENT | implementation_scope_declared, authority_false | false |
| `IN_PROGRESS` | `MERGED` | HUMAN | human_merge_confirmed, verify_gate_passed, receipt_generated | true |
| `IN_PROGRESS` | `DISPUTED` | HUMAN, AGENT, MEMBRANE | contradiction_or_runtime_mismatch_present | true |
| `IN_PROGRESS` | `REJECTED` | HUMAN, MEMBRANE | failed_runtime_or_governance_check | true |
| `MERGED` | `REPLAY` | HUMAN, AGENT, OBSERVER | merged_receipt_present, replay_request_present | false |
| `DISPUTED` | `UNDER_REVIEW` | HUMAN, AGENT, OBSERVER | dispute_context_preserved, counter_receipt_or_source_present | true |
| `DISPUTED` | `REJECTED` | HUMAN, MEMBRANE | dispute_resolved_as_invalid, rejection_reason_present | true |
| `REPLAY` | `DISPUTED` | HUMAN, AGENT, OBSERVER, MEMBRANE | replay_mismatch_or_drift_detected | true |

## Forbidden Transitions

These are always invalid:

- `DRAFT` → `MERGED`
- `DRAFT` → `REPLAY`
- `DRAFT` → `APPROVED`
- `UNDER_REVIEW` → `MERGED`
- `GOVERNANCE_CHECK` → `MERGED`
- `APPROVED` → `MERGED`
- `REJECTED` → `MERGED`
- `DISPUTED` → `MERGED`
- `REPLAY` → `MERGED`
- `WITNESS_OUTPUT` → `VERIFIED_TRUTH`
- `SCORE` → `AUTHORITY`
- `ANCHOR_POINTER` → `LEGAL_EFFECT`

## Required Global Checks

Every transition must preserve:

```json
{
  "authority": false,
  "legal_effect": false,
  "boundary_honest": true,
  "no_ghost_anchor": true
}
```

## Membrane Rules

A transition enters membrane hold when:

- required receipts are missing
- source is absent
- witness output attempts truth promotion
- score attempts authority promotion
- Base / ENS anchor is claimed without tx, UID, or receipt
- runtime parity mismatch is observed
- transition is not explicitly listed as allowed

## Receipt Hooks

Major transitions should emit or reference a receipt:

- `UNDER_REVIEW` → `GOVERNANCE_CHECK`
- `GOVERNANCE_CHECK` → `APPROVED`
- `GOVERNANCE_CHECK` → `DISPUTED`
- `IN_PROGRESS` → `MERGED`
- `MERGED` → `REPLAY`
- `REPLAY` → `DISPUTED`

## Canonical Rule

Observers surface. Witnesses report. Agents play. Verifiers gate. Courts translate. Receipts replay. Humans merge. Authority remains false.

## Court Alignment

- 🧌 Goblin Court: TRANSITION RULES ADMISSIBLE
- 🎮 Meme Court: RULES ENGINE ADVANCING
- 🎪 Clown Court: NO AUTHORITY UPGRADE
