# ADR-009 — Runtime Enforcement Boundary Specification

**Status:** Draft  
**Category:** Governance / Enforcement  
**Applies to:** JOY, ALMS, COMPUTERWISDOM, Wisdom Index, Replay Engine  
**PR:** #426  
**Commit:** `cbe0dfb7d9a10a9dc969e2e062d6b904122a8cb0`

## Context

The architecture now includes four layers:

- **ALMS** — Can we prove it?
- **JOY** — Why does it matter?
- **COMPUTERWISDOM** — How do we teach and share it?
- **WISDOM** — Should we do it at all?

The Wisdom Operator introduces human-only review steps (`CARE`, `DECIDE`, `AUTHORIZE`) that must never be automated or inferred. Before integrating Wisdom into the replay engine, the system requires a formal boundary defining:

- what runtime enforcement may do;
- what runtime enforcement may not do;
- what AI may assist with;
- what AI may never authorize;
- what humans must approve;
- what evidence must be produced;
- what transitions may be blocked;
- what transitions may never be manufactured.

This ADR prevents implementation details from silently becoming governance law.

## Decision

The system adopts a strict separation between:

- **POLICY** — declared rules;
- **ENFORCEMENT** — runtime validation of declared rules;
- **AUTHORIZATION** — explicit human permission;
- **EXECUTION** — state-changing operations;
- **EVIDENCE** — receipts proving what occurred.

These layers must never collapse into one another.

## Core invariant

> Runtime enforcement may block an unauthorized transition. It may not manufacture authorization.

This invariant is non-negotiable and applies across all namespaces.

## Boundary definitions

### POLICY

Rules declared in ADRs, manifests, or governance files. Policy remains unchanged until updated through a human-authorized governance transition.

### ENFORCEMENT

Software checks whether a proposed transition complies with declared policy. Enforcement may validate or block. Enforcement may not infer consent, create authority, or silently alter policy.

### AUTHORIZATION

A human decision granting permission for a specific transition. Authorization must be explicit, scope-bound, receipt-bound, and independently distinguishable from recommendation or verification.

A cryptographic signature is required only when the applicable policy requires one and key custody has been operationally established. Until then, the authorization remains a draft or operator-recorded decision and must not be represented as cryptographically proven.

### EXECUTION

The actual state-changing operation. Execution requires a valid, unexpired, scope-matching authorization grant and successful enforcement validation.

### EVIDENCE

Receipts record what was proposed, checked, authorized, attempted, and observed. Corrections append new receipts. Historical evidence is not silently rewritten.

## Capability boundary table

| Capability | AI | Runtime | Human |
|---|---:|---:|---:|
| Search and organize | Yes | Yes | Yes |
| Verify deterministic rules | Assist | Yes | Review |
| Recommend a decision | Yes | No | Yes |
| Supply consent | No | No | Yes |
| Authorize publication | No | No | Yes |
| Execute an approved action | No direct authority | Only with a valid grant | Authorizes |
| Rewrite historical receipts | No | No | No |
| Draft a correction receipt | Yes | No | Yes |
| Validate a correction receipt | Assist | Yes | Review |
| Approve a correction receipt | No | No | Yes |

This table is binding for the draft architecture.

## Runtime enforcement schema

```json
{
  "runtime_enforcement": {
    "may_validate": true,
    "may_block": true,
    "may_recommend": false,
    "may_create_authority": false,
    "may_infer_consent": false,
    "may_execute_without_grant": false,
    "human_authorization_required": true
  }
}
```

Future enforcement modules must either conform to this boundary or cite a later accepted ADR that explicitly supersedes it.

## Authorization-grant minimum fields

Any executable authorization envelope must bind at least:

```text
grant_id
human_authorizer
policy_version
intent_hash
scope
allowed_side_effects
prohibited_side_effects
issued_at
expires_at_or_single_use
execution_nonce
```

The runtime must reject missing, expired, reused, scope-mismatched, policy-mismatched, or intent-mismatched grants.

## Required receipts

Each authorization attempt must produce one terminal receipt recording:

```text
proposal_reference
policy_version
validation_result
authorization_reference
nonce_state
execution_attempted
terminal_outcome
observed_side_effects
correction_reference_if_any
```

A blocked transition also receives a receipt. A failure is evidence, not an excuse to omit the record.

## Promotion sequence

```text
ADR-009 ACCEPTED
→ enforcement schema
→ authorization envelope
→ replay-engine hooks
→ negative test vectors
→ human approval tests
→ independent replay
→ runtime status review
```

The first implementation target is fail-closed transition validation, not autonomous decision-making.

## Minimum negative tests

Before runtime status may advance, tests must demonstrate rejection of:

1. missing authorization;
2. AI-generated pseudo-consent;
3. expired authorization;
4. reused execution nonce;
5. mismatched intent hash;
6. scope expansion;
7. undeclared side effects;
8. policy-version mismatch;
9. missing terminal receipt;
10. attempted historical receipt rewrite.

Passing these tests establishes only the tested boundary. It does not establish general production safety or publication authority.

## Consequences

- Implementation cannot silently redefine governance.
- AI cannot escalate privileges through recommendation or inference.
- Verification cannot be treated as permission.
- Human authorization remains the only source of consent.
- Runtime checks can prevent transitions but cannot morally or legally validate them.
- Receipts preserve the evidence chain for both successful and blocked attempts.
- The Wisdom Operator gains enforceable boundaries without gaining autonomous execution authority.
- The architecture remains vendor-independent and operator-controlled.

## Non-claims

This ADR does not establish that:

- runtime enforcement is implemented;
- authorization signatures are operational;
- key custody is secure;
- receipt storage is immutable;
- independent replay has passed;
- any action is legally authorized;
- any publication is approved;
- any symbolic identity has governance authority.

## Status

This ADR remains **DRAFT** until reviewed and explicitly accepted by human authority.

No enforcement module may claim conformance, activation, production readiness, or authorization solely because this file exists.