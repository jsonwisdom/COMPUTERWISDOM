# Presidential Dice v0.2 — Adversarial Replay + Merkle Hardening

**Class:** public-education game / epistemic stress harness  
**Authority created:** false  
**Operational command claimed:** false

## Decision

Freeze the weighted-receipt hierarchy for later review and harden serialization + append-only receipt anchoring first.

A single scalar such as `EO=1.0`, `SCOTUS=0.98`, or `Statute=0.95` is not yet safe as a general conflict resolver because legal force depends on jurisdiction, issue, posture, date, supersession, and the proposition for which a source is cited.

## Critical separation

`EXACT_REPLAY` proves reproducibility of a run. It does **not** by itself prove the underlying real-world claim.

```text
REPLAY_INTEGRITY = MATCH | MISMATCH | HOLD
EVIDENCE_STATE   = PROVEN | BOUND | HOLD | CONFLICT | REJECT
```

Therefore:

```text
BYTE_MATCH != CLAIM_PROVEN
MERKLE_ROOT != TRUTH
HASH != AUTHORITY
D8_GATE != AUTHORITY_STRENGTH
```

The D8 roll routes the authority question; it is never a legal-authority score.

## Hash correction

A receipt hash MUST NOT be calculated over an object containing its own `receipt_hash` field. The canonical digest is computed over the receipt body with `receipt_hash` excluded.

Likewise:

```text
receipt_hash != sealed_parent_hash
```

`sealed_parent_hash` binds the immutable parent run. `receipt_hash` binds the child replay receipt.

## Source anchors

Public sources often do not provide cryptographic signatures. Do not invent one.

Minimum source anchor:

```text
source_uri
retrieved_at
content_digest
```

Optional:

```text
signature
signature_scheme
signature_verified
```

`signature_verified=true` is allowed only when an actual signature was independently verified.

## Branch namespaces

Evidence ledger:

```text
EXACT_REPLAY
PARAMETER_CHALLENGE
AUTHORITY_CHALLENGE
COUNTER_RECEIPT
```

Quarantine ledger:

```text
COUNTERFACTUAL_X
STOCHASTIC_STRESS
```

Quarantined receipts may be integrity-verified and Merkle-anchored, but they remain invisible to evidence-state promotion.

## Canonical serialization

Use deterministic UTF-8 JSON:

```text
sort_keys=true
separators=(",", ":")
allow_nan=false
Enums -> string values
```

Receipt leaf:

```text
leaf_hash = SHA256(canonical_receipt_bytes)
```

Merkle parent:

```text
parent = SHA256(left_digest_bytes || right_digest_bytes)
```

For an odd number of leaves, duplicate the final leaf at that tree level.

## Four proof predicates

For a real-world claim to be promoted to `PROVEN`:

```text
PROVEN iff
  RECEIPT_INTEGRITY
  and AUTHORITY_CHAIN
  and LOGICAL_CONSISTENCY
  and NO_ACTIVE_CONFLICT
```

But these predicates are claim predicates, not replay-integrity predicates.

An `EXACT_REPLAY` may establish `REPLAY_INTEGRITY=MATCH` while `EVIDENCE_STATE` remains `HOLD`, `BOUND`, `CONFLICT`, or `REJECT`.

## Sticky states

`CONFLICT` and `REJECT` remain sticky on the same run lineage. A later superseding run is a new immutable object and must reference the prior run explicitly; it never rewrites history.

Conflict-resolution precedence remains **HOLD for v0.2** until a proposition-aware authority model replaces the proposed scalar weight table.

## Final kernel

```text
FREEZE ORIGINAL
-> CANONICAL SERIALIZE
-> HASH CHILD RECEIPT
-> VERIFY PARENT LINK
-> APPEND TO NAMESPACE
-> MERKLE ROOT
-> ADVERSARIAL REPLAY
-> REPLAY_INTEGRITY + EVIDENCE_STATE
```

Gray Baby standing order:

> **SHOW ME THE EDGE.**
