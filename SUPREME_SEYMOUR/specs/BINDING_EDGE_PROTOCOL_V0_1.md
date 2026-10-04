# BINDING EDGE PROTOCOL V0.1

**Module:** SUPREME_SEYMOUR_V0_1  
**Lane:** HOLD  
**Canon:** false  
**Authority created:** false  
**Formal alias:** HOLD  
**Dependency:** RECEIPT_CLAIM_CLASS_SPEC_V0_1  
**Relationship to prior records:** adjacent; does not overwrite the receipt claim-class specification, PUBLIC_REPLAY_RUN_BINDING_V0_1, or PUBLIC_REPLAY_RUN_BINDING_V0_2.

## Purpose

This protocol decides whether a specific evidence edge may be bound.

A receipt is necessary but not sufficient.

```text
RECEIPT_EXISTS != EDGE_BOUND
RC_LEVEL_SUFFICIENT != EDGE_BOUND
```

Binding requires both:

1. sufficient receipt claim class; and
2. exact applicability of that receipt to the edge under test.

## Core pipeline

```text
NAME_EDGE
-> FREEZE_EDGE_REQUIREMENTS
-> ADMIT_RECEIPTS
-> CLASSIFY_RECEIPT_CLAIM_SCOPE
-> CHECK_OBJECT_IDENTITY
-> CHECK_PROPOSITION_IDENTITY
-> CHECK_SCOPE
-> CHECK_CLOCK_AND_VERSION
-> CHECK_FRESHNESS
-> CHECK_CONFLICTS
-> CHECK_REQUIRED_RC_LEVEL
-> PASS | HOLD | CONFLICT | REJECT
```

No step may be skipped by narrative inference.

## Edge object

```yaml
binding_edge:
  edge_id: string
  from_object:
    object_id: string
    version: string | NOT_APPLICABLE | UNKNOWN
    hash: string | NOT_AVAILABLE
  relationship: string
  to_object:
    object_id: string
    version: string | NOT_APPLICABLE | UNKNOWN
    hash: string | NOT_AVAILABLE

  proposition: string
  jurisdiction_or_scope: string | NOT_APPLICABLE
  valid_clock_window:
    start: string | NOT_APPLICABLE | UNKNOWN
    end: string | NOT_APPLICABLE | UNKNOWN

  required_receipt_claim_class: RC0 | RC1 | RC2 | RC3 | RC4 | RC5 | RC6

  lifecycle: UNRUN | HOLD | PASS | CONFLICT | REJECT | NOT_APPLICABLE
  binding_decision: NOT_EVALUATED | BIND_ALLOWED | BIND_BLOCKED
  canon: false
  authority_created: false
```

The lifecycle vocabulary is evidence closure only. This protocol does not add new tokens to the sealed edge lifecycle enum.

## Receipt admission

Every candidate receipt must carry or resolve to:

```yaml
admitted_receipt:
  receipt_id: string
  receipt_transport_class: string
  receipt_claim_class: RC0 | RC1 | RC2 | RC3 | RC4 | RC5 | RC6

  source_rail: string
  source_pointer: string

  proposition_bound: string
  subject_object_ids: []
  versions_bound: []
  hashes_bound: []
  clock_window_bound:
    start: string | NOT_APPLICABLE | UNKNOWN
    end: string | NOT_APPLICABLE | UNKNOWN

  inspection_status: PERFORMED | NOT_PERFORMED
  replay_status: PASS | HOLD | REJECT | NOT_PERFORMED
  independent_reproduction: ESTABLISHED | NOT_ESTABLISHED
  consensus_status: ESTABLISHED | NOT_ESTABLISHED

  stale: TRUE | FALSE | UNKNOWN
  authority_created: false
```

A missing required field does not become false. It becomes an unresolved applicability edge.

## Gate 1 — Object identity

The receipt must bind the same object or objects required by the edge.

```text
SAME_LABEL != SAME_OBJECT
SAME_PATH != SAME_BYTES
SAME_NAME != SAME_VERSION
RELATED_OBJECT != TARGET_OBJECT
```

If object identity is required and cannot be established:

```yaml
lifecycle: HOLD
binding_decision: BIND_BLOCKED
missing_receipt: OBJECT_IDENTITY
```

## Gate 2 — Proposition identity

The receipt must support the exact proposition being bound.

```text
RECEIPT_ABOUT_OBJECT != RECEIPT_FOR_PROPOSITION
BROADER_CLAIM != BOUNDED_CLAIM
ADJACENT_FACT != REQUIRED_FACT
```

Example:

```text
receipt proves: "CI run completed successfully"
edge asks: "artifact bytes equal declared receipt bytes"

RESULT = HOLD
```

The receipt exists, but it does not answer the proposition.

## Gate 3 — Scope identity

Required dimensions must be compatible:

```text
same_subject
same_relationship
same_jurisdiction_or_declared_scope
same_metric_or_field_definition_when_applicable
same_unit_when_applicable
compatible_method_when_applicable
```

A scope mismatch is not automatically false evidence.

```text
SCOPE_MISMATCH -> HOLD or CONFLICT
SCOPE_MISMATCH != REJECT by default
```

Use CONFLICT when two admitted receipts establish incompatible scope claims that cannot both satisfy the edge as written.

## Gate 4 — Clock and version

A receipt binds only the version and time range it actually observed.

```text
OLD_RECEIPT != CURRENT_STATE
NEW_RUN != OLD_RUN
SAME_FILENAME != SAME_VERSION
CURRENT_POINTER != HISTORICAL_BYTES
```

If the edge is timeless by definition, mark the clock field NOT_APPLICABLE rather than inventing a time dependency.

## Gate 5 — Freshness

Apply invalidation rules from RECEIPT_CLAIM_CLASS_SPEC_V0_1.

Relevant changes may stale prior receipts:

```text
CODE_CHANGED -> REPLAY_RECEIPT_STALE
TEST_CHANGED -> TEST_OR_CI_RECEIPT_STALE
FIXTURE_CHANGED -> REPLAY_BINDING_STALE
ARTIFACT_CHANGED -> ARTIFACT_HASH_STALE
RUN_CHANGED -> EXECUTION_POINTER_CHANGED
CONSENSUS_RULE_CHANGED -> CONSENSUS_REEVALUATION_REQUIRED
```

Historical receipts remain valid as historical records even when stale for a current-state edge.

```text
STALE_FOR_CURRENT_EDGE != INVALID_HISTORICAL_RECEIPT
```

## Gate 6 — Conflict preservation

Contradictory receipts are not silently averaged, merged, or discarded.

```text
CONFLICT -> PRESERVE_BOTH
CONFLICT -> IDENTIFY_CONFLICT_DIMENSION
CONFLICT -> BLOCK_BINDING_IF_REQUIRED_EDGE_DEPENDS_ON_IT
```

A conflict that does not touch a required dimension does not automatically block unrelated binding.

```text
IRRELEVANT_CONFLICT != REQUIRED_EDGE_CONFLICT
```

## Gate 7 — Required receipt claim class

Only after Gates 1–6 pass may the RC threshold be evaluated.

```text
AVAILABLE_RC >= REQUIRED_RC
```

is necessary but not sufficient.

The effective class is the highest class established for the same proposition, same object set, compatible scope, valid clock/version, and non-stale evidence chain.

Do not compute an effective class by taking the maximum RC number across unrelated receipts.

```text
MAX(RC_UNRELATED_RECEIPTS) != EFFECTIVE_RC
```

### Threshold result

If all applicability gates pass and effective RC meets the required class:

```yaml
lifecycle: PASS
binding_decision: BIND_ALLOWED
```

If applicability is unresolved or effective RC is below the required class:

```yaml
lifecycle: HOLD
binding_decision: BIND_BLOCKED
```

If admitted receipts conflict on a required dimension:

```yaml
lifecycle: CONFLICT
binding_decision: BIND_BLOCKED
```

If a receipt directly disproves or disqualifies the exact tested edge under the declared rule:

```yaml
lifecycle: REJECT
binding_decision: BIND_BLOCKED
```

Insufficient evidence alone is HOLD, not REJECT.

## RC comparison rule

For this protocol, RC0–RC6 are ordered only within one compatible evidence chain:

```text
RC0 < RC1 < RC2 < RC3 < RC4 < RC5 < RC6
```

But:

```text
RC5_DIFFERENT_PROPOSITION !>= RC2_REQUIRED_PROPOSITION
RC6_WRONG_OBJECT !>= RC1_TARGET_OBJECT
```

Class ordering never overrides identity or scope.

## Minimum bind receipt

Every PASS must emit a binding receipt:

```yaml
binding_receipt:
  binding_receipt_id: string
  edge_id: string

  from_object_id: string
  relationship: string
  to_object_id: string
  proposition: string

  required_receipt_claim_class: RC0 | RC1 | RC2 | RC3 | RC4 | RC5 | RC6
  effective_receipt_claim_class: RC0 | RC1 | RC2 | RC3 | RC4 | RC5 | RC6

  supporting_receipt_ids: []
  supporting_source_pointers: []

  object_identity_gate: PASS
  proposition_identity_gate: PASS
  scope_gate: PASS | NOT_APPLICABLE
  clock_version_gate: PASS | NOT_APPLICABLE
  freshness_gate: PASS
  conflict_gate: PASS
  rc_threshold_gate: PASS

  lifecycle: PASS
  binding_decision: BIND_ALLOWED

  canon: false
  authority_created: false
```

No PASS receipt may omit the gates that justified PASS.

## HOLD receipt

A HOLD must identify the exact missing edge rather than merely repeat HOLD.

```yaml
binding_hold_receipt:
  edge_id: string
  lifecycle: HOLD
  binding_decision: BIND_BLOCKED

  passed_gates: []
  unresolved_gates: []
  missing_receipts: []
  next_receipt_required: string

  canon: false
  authority_created: false
```

```text
HOLD = ROUTING_STATE
HOLD != TERMINAL_FAILURE
```

## CONFLICT receipt

```yaml
binding_conflict_receipt:
  edge_id: string
  lifecycle: CONFLICT
  binding_decision: BIND_BLOCKED

  conflict_dimension: string
  receipt_a: string
  receipt_b: string
  preserved_receipts: true
  next_resolution_receipt_required: string

  canon: false
  authority_created: false
```

## REJECT receipt

REJECT requires positive disqualifying evidence for the exact edge.

```yaml
binding_reject_receipt:
  edge_id: string
  lifecycle: REJECT
  binding_decision: BIND_BLOCKED

  disqualifying_receipt_id: string
  disqualifying_rule: string
  proposition_rejected: string

  canon: false
  authority_created: false
```

```text
SEARCH_MISS != REJECT
LOW_RC != REJECT
MISSING_RECEIPT != REJECT
UNINSPECTED != REJECT
```

## Application — PUBLIC_REPLAY_RUN_BINDING_V0_2

The current classification is:

```yaml
available_receipt:
  receipt_claim_class: RC1
  basis: EXECUTION_SUCCESS_ONLY
  artifact_inspection: NOT_PERFORMED
```

Therefore an edge requiring only:

```text
"the named execution completed successfully"
```

may be eligible for PASS after identity, scope, clock/version, freshness, and conflict gates pass.

An edge requiring:

```text
"the produced receipt artifact bytes were inspected and locally hashed"
```

requires RC3.

With only RC1 available:

```yaml
lifecycle: HOLD
binding_decision: BIND_BLOCKED
missing_receipt: ARTIFACT_INSPECTION_AND_LOCAL_HASH
```

No amount of pointer repetition upgrades RC1 to RC3.

## Non-actions

This protocol does not:

- inspect Run #7 artifacts by declaring the protocol;
- promote PUBLIC_REPLAY_RUN_BINDING_V0_2;
- alter FORMAL_ALIAS;
- merge PR #607 or PR #608;
- create public consensus;
- create authority;
- replace the global constitutional dependency registry.

```text
PROTOCOL_DEFINED != EDGE_EXECUTED
EDGE_EXECUTED != EDGE_PASS
EDGE_PASS != CANON
CANON != AUTHORITY
```

## State

```yaml
BINDING_EDGE_PROTOCOL_V0_1:
  module: SUPREME_SEYMOUR_V0_1
  lane: HOLD
  canon: FALSE
  authority_created: FALSE

  receipt_claim_spec_dependency: RECEIPT_CLAIM_CLASS_SPEC_V0_1
  dependency_state: DRAFT_UNMERGED

  protocol_defined: TRUE
  protocol_executed: FALSE
  edges_bound_by_this_protocol: 0

  next_receipt_required:
    - "execute this protocol against one bounded candidate edge"
    - "emit PASS/HOLD/CONFLICT/REJECT receipt without promotion"
```
