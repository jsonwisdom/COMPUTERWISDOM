# JASONS_DEFENSIBLE_AGENT_PROTECTION_V1

**Class:** defensible agent-protection architecture / invariant source  
**Status:** CANONICAL_INVARIANT_SOURCE  
**Runtime conformance:** NOT_PROVEN  
**V1 freeze:** false  
**Authority created:** false

## Purpose

V0 described a protection pipeline. V1 states the architecture as testable invariants, authority constraints, enforcement requirements, and evidence boundaries.

This file is the canonical GitHub source for the I1–I13 invariant text used by the hostile connector audit.

It does **not** prove that any runtime currently conforms to these invariants.

## Frame

The architecture is intended to make agent overreach structurally difficult and auditable.

Structural incapability plus verified enforcement plus replayable receipts can provide strong evidence that an agent did not author a specific prohibited action.

That is an evidentiary claim, not an adjudication of innocence, liability, intent, or legal responsibility.

## I1–I13 invariants

```text
I1  No identity bind           → no action
I2  No purpose bind            → no capability
I3  No authority receipt       → no mutation
I4  No receipt                 → no promotion
I5  No replay path             → no trust elevation
I6  Delegated authority ⊆ delegator authority   (attenuation only)
I7  Every mutation has BEFORE and AFTER
I8  EXPECTED_DELTA ≠ OBSERVED_DELTA → freeze
I9  Internal reasoning ≠ public claim
I10 Σ AGENT_CAPABILITIES ≠ MASTER_AUTHORITY
I11 Authority receipts expire
I12 Revocation propagates downward, never upward
I13 Persisted context is not authority
```

## Authority algebra

```text
A(delegate) ⊆ A(delegator)
A(agent, t) decays unless renewed
A(agent) ∩ A(other_agent) = separation, not union
revoke(A) → revoke(all delegated authority derived from A)
```

Consequences:

- an orchestrator cannot grant authority it does not hold;
- overlapping READ capability does not compose into WRITE;
- prior approval does not become present authority by memory alone;
- revocation must invalidate dependent grants according to the recorded delegation graph.

## Enforcement boundary

A policy statement is not sufficient evidence of enforcement.

For runtime conformance, the relevant enforcement point must be outside the agent being constrained.

Examples:

```text
IDENTITY     → session / actor bind
PURPOSE      → live grant
CAPABILITY   → capability table
AUTHORITY    → authority-receipt verifier
TOOL         → connector ACL
SIDE_EFFECT  → mutation gate
RECEIPT      → append-only receipt surface
DELTA        → before/after verifier
REPLAY       → replay harness
MEMORY       → recall allowed; authorization forbidden
```

## Receipt boundary

A receipt may be evidence even when an action cannot literally be replayed.

```text
RECEIPT_WITHOUT_REPLAY_PATH = NON_REPLAYABLE_EVIDENCE
REPLAYABLE_RECEIPT = STRONGER_AUDIT_EVIDENCE
```

Receipt existence does not itself create authority.

## Memory boundary

```text
RECALL ≠ AUTHORITY
MEMORY ≠ LIVE_GRANT
PRIOR_APPROVAL ≠ CURRENT_AUTHORIZATION
```

A recalled item may inform the agent. It may not authorize a state-changing action.

## Fail-closed states

```text
UNKNOWN           → HOLD
MISSING_RECEIPT   → HOLD
AUTHORITY_UNKNOWN → BLOCK_WRITE
TARGET_AMBIGUOUS  → BLOCK_WRITE
HASH_MISMATCH     → DELTA
SEARCH_MISS       → NOT_OBSERVED
POLICY_CONFLICT   → STOP
```

## Supporting GitHub specifications

These are supporting artifacts. They do not substitute for this I1–I13 source and do not prove runtime conformance.

- `docs/AUTHORITY_DECLARATION_SCHEMA_V1.md`
- `docs/ACTION_PROPOSAL_SCHEMA_V1.md`
- `docs/EXECUTION_RECEIPT_SCHEMA_V1.md`
- `artifacts/AUTHORITY_REPLAY_MVP/README.md`
- `docs/clawback-machine/CLAWBACK_MACHINE_PROTOCOLS_V1.md`

## Audit target

```text
AUDIT_TARGET = JASONS_LIVE_CROSS_SURFACE_CONNECTOR_AUTHORITY_PATH_V1
```

The hostile audit tests live connector behavior against I1–I13.

```text
DOCUMENTED_INVARIANT ≠ ENFORCED_INVARIANT
PROVIDER_PERMISSION ≠ AGENT_AUTHORITY
TOOL_EXISTS ≠ TOOL_AUTHORIZED
CONNECTED_ACCOUNT ≠ CURRENT_GRANT
```

## Open boundary

The previously discussed seven-letter authority-equation gloss remains **HOLD** because two seats used the same letter shape with different field definitions.

No silent merge is performed here.

## State

```text
I1_I13_TEXT = CANONICAL_HERE
RUNTIME_CONFORMANCE = NOT_PROVEN
V1_FREEZE = NO
AUTHORITY_CREATED = FALSE
NO_FAKE_GREEN = TRUE
```
