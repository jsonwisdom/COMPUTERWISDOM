# GBS-BOXDEE-BURDEN-V001

**Class:** Gray Baby / BoxDee transition-proof standard  
**Version:** V001  
**Design namespace:** `jaywisdom.base.eth`  
**Authority created:** `FALSE`

## Purpose

Define who carries the burden when a claim asserts that an object changed state.

This standard does not decide external truth by narrative. It controls whether a claimed transition may be promoted inside a BoxDee environment.

## Governing law

```text
CLAIMANT_BEARING_CLAIM
→ BEARS_BURDEN_FOR_TRANSITION
→ SOURCE → OBJECT → TIME → ACTION → READBACK
→ PASS | DELTA | HOLD
```

**Whoever asserts the transition bears the burden of proving the transition.**

A missing witness proves only that the witness is missing.

## Kernel invariants

```text
UNOBSERVED != NONEXISTENT
SEARCH_MISS != ABSENCE
SCREENSHOT != BACKEND_CAUSE
CURRENT_STATE != PROOF_OF_TRANSITION
SUPPORT_REFUSAL != RESOLUTION
PUBLIC_STATUS_NOW != EARLIER_STATE_NEVER_EXISTED
CI_PASS != AUTHORITY
ENS_LABEL != AUTHORITY
AUTHORITY_CREATED = FALSE
```

## Transition receipt

Every asserted transition MUST preserve these fields independently:

1. `claimant` — who or what asserts the transition.
2. `claim` — the exact bounded transition claim.
3. `source` — origin of the evidence.
4. `object` — exact object identifier or bounded description.
5. `time` — observed or source-provided timestamp with timezone when available.
6. `action` — transition being asserted.
7. `readback` — independent or same-surface state readback.
8. `provenance` — URLs, hashes, transaction IDs, commit IDs, screenshot hashes, or equivalent receipts.
9. `burdenSatisfied` — boolean.
10. `result` — `PASS`, `DELTA`, or `HOLD`.
11. `authorityCreated` — MUST remain `false` under this standard.

## Receipt interpretation

### Screenshot

A screenshot proves what was displayed on the captured surface at capture time, subject to the integrity of the supplied image.

It does not by itself prove backend cause, deletion, resolution, or global absence.

### Public status now

A current public status readback proves the current public representation observed at that time.

It does not by itself prove an earlier incident never existed or prove the missing transition path.

### Support refusal

A support response such as inability or refusal to answer is a receipt for that support response.

It is not evidence that the underlying incident is false, absent, or resolved.

### Search miss

A failed search establishes only that the requested lookup did not return a matching artifact within the searched scope.

It does not establish global absence or deletion.

## Disposition rules

```text
REQUIRED EDGE MISSING      → HOLD
BOUND RECEIPTS DISAGREE    → DELTA
REQUIRED EDGES RECONCILE   → PASS
```

`PASS` is scoped only to the bounded transition. It does not create institutional, governmental, legal, identity, or protocol authority.

## Replay corridor

```text
FREEZE CLAIM
→ IDENTIFY CLAIMANT
→ BIND SOURCE
→ NAME EXACT OBJECT
→ BIND TIME
→ IDENTIFY ASSERTED ACTION
→ READ BACK RESULTING STATE
→ COMPARE SOURCE ↔ OBJECT ↔ ACTION ↔ READBACK
→ EMIT PASS | DELTA | HOLD
→ APPEND RECEIPT
→ PRESERVE HISTORY
```

ReverseReplay may walk the corridor backward to expose a missing transition and ForwardReplay may test whether the surviving path can be reconstructed without invented edges.

## Coinbase PayPal example

For `RRR-COINBASE-PAYPAL-V001`, an observed app incident, a current public-status representation, and a support-assistant response remain distinct receipts.

A resolution claim requires the missing transition edge, for example:

```text
incident ID
→ incident history
→ status transition
→ resolved timestamp
→ component readback
```

Until the asserted transition is supported:

```text
BURDEN_SATISFIED = FALSE
TRANSITION_PROVEN = FALSE
BOXDEE = HOLD
```

This example does not assert that the incident was deleted, concealed, resolved, or nonexistent.

## Namespace boundary

`jaywisdom.base.eth` is recorded here as the design/provenance namespace for this standard.

```text
DESIGN_NAMESPACE = jaywisdom.base.eth
ENS_LABEL != IDENTITY_PROOF
ENS_LABEL != AUTHORITY
AUTHORITY_CREATED = FALSE
```

## Machine contract

The companion schema is:

`docs/gray-baby/GBS_BOXDEE_BURDEN_V001.schema.json`

Conforming domain receipts may extend the schema, but MUST NOT weaken the invariants above or promote `authorityCreated` to `true` through this standard.
