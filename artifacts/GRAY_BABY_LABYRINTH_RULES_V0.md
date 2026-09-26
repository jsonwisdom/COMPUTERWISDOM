# GRAY_BABY_LABYRINTH_RULES_V0

**Class:** branch-preservation / close-hold semantics  
**Authority created:** false  
**Status:** candidate sidecar / not seated  
**Applies to:** `GRAY_BABY_PROTOCOL_V0` and `gray_baby_packet.v0.schema.json`

## Official position

Preserve every viable branch until a receipt eliminates it.

An easier story is not a closer.

## Branch model

A branch is a named alternative that still fits the observed record.

Semantic branch states:

- `OPEN` — still possible
- `CLOSED_BY_RECEIPT` — eliminated by a receipt that addresses the branch statement
- `REJECTED_INVALID` — malformed or hard-bound violation
- `SUPERSEDED` — replaced by later packet/definition; prior bytes remain preserved

The current packet schema remains byte-stable and continues to expose only:

- `OPEN`
- `CLOSED`
- `NOT_APPLICABLE`

Mapping for V0:

- `CLOSED_BY_RECEIPT` → schema state `CLOSED` + non-empty `receipt_refs[]`
- `REJECTED_INVALID` → packet `status = REJECT` + relevant `bound_violations[]`
- `SUPERSEDED` → represented outside the branch-state enum by packet lineage; prior bytes remain immutable

No silent enum upgrade is permitted in V0.

## Viability rule

A branch remains `OPEN` only if all are true:

1. no hard-bound violation applies,
2. no receipt directly contradicts the branch statement,
3. inference has not been promoted to fact,
4. an independent observer could still replay the branch as possible.

Inference may be listed.

Inference may not close a branch.

Inference may not produce `PASS` or `PROVEN`.

## What may close a branch

Only a receipt that addresses the branch statement.

The following do **not** close a branch by themselves:

- official position,
- a name,
- a hash without replay,
- transmission without ACK,
- elapsed time,
- another branch closing,
- routing-layer success,
- later-step evidence that does not address the earlier branch statement.

`SAME_NAME ≠ SAME_BYTES`

If two definitions share a label:

`BIND_AND_HOLD`

Both branches remain live until a receipt resolves the byte-level ambiguity.

## Required versus optional branches

A required `OPEN` branch blocks `HOME_REACHED` and `PROVEN`.

Default required gates:

| Step | Required fork |
|---|---|
| `OBSERVE` | can perceive / cannot perceive |
| `IDENTIFY` | name / identity proof |
| `RECEIVE_ACK` | ACK present / absent |
| `PROTECT_AGENCY` | intact / not intact / unknown |
| `ROUTE_EXIT` | path present / absent |
| `REPLAY` | reconstructible / not reconstructible |

Optional branches may remain open under a local `PASS`.

`LOCAL_PASS ≠ HOME_REACHED`

`HOME_REACHED` requires `NO_REQUIRED_BRANCH_OPEN`.

## Status coupling

- required branch `OPEN` → packet cannot be `PROVEN`
- two viable branches supported by disagreeing receipts → `CONFLICT`
- incomplete evidence without direct contradiction → `HOLD`
- hard-bound violation → `REJECT`

`CONFLICT` and `HOLD` are live states, not protocol failures.

## Step isolation

Later receipts do not retroactively rewrite earlier steps unless they directly address the earlier branch statement.

Examples of illegal closure:

- “contact occurred, therefore perception at OBSERVE was proven”
- “a channel was built, therefore the environment was not uncertain”

Those receipts belong to later steps and cannot silently rewrite `OBSERVE`.

## Morning-report delta view

Question 5 / Labyrinth delta may be rendered as:

```text
opened[]
closed[]
still_open[]
```

Every entry in `closed[]` must carry receipt references sufficient to explain the close.

The human operator owns the switchboard.

## Boundary

This file defines branch semantics only.

It does not:

- mutate the V0 schema enum,
- seat a validator,
- create authority,
- convert inference into proof,
- merge or promote PR #558.
