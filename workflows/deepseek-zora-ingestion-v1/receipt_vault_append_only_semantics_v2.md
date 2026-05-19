# Receipt Vault Append-Only Semantics V2

## Core Rule

The Receipt Vault is strictly append-only. Once a receipt is written, it is immutable. No edits, deletions, or retroactive changes are permitted.

## Receipt Entry Fields

- `receipt_id`: UUID or sequential index.
- `timestamp_utc`: ISO 8601 UTC timestamp.
- `previous_merkle_root`: SHA-256 hash of prior vault state. Genesis = `GENESIS_ROOT`.
- `receipt_digest`: SHA-256 of the verified source artifact.
- `source_reference`: canonical source identifier, hash, or signed pointer.
- `state_transition`: one canonical state transition.
- `metadata`: minimal key-value metadata. No executable code.
- `new_merkle_root`: computed root after append.

## Allowed State Transitions

- `CANDIDATE → HELD`
- `HELD → REJECTED`
- `HELD → VERIFIED_RECEIPT`
- `VERIFIED_RECEIPT → CANON`

No other transition is valid unless this protocol is superseded by a later version.

## Correction Mechanism

Corrections occur only by appending a superseding receipt. The new receipt must reference the `receipt_id` being superseded and include a justification digest. The original receipt remains in the vault.

## Prior Merkle Root Requirement

Every new receipt must include the exact current `merkle_root` of the vault at time of append. A mismatch causes rejection.

## New Merkle Root Computation

```text
new_merkle_root = SHA256(previous_merkle_root || receipt_digest || receipt_id)
```

## Idempotent Duplicate Handling

An identical `receipt_digest` for the same source is ignored as a duplicate and logged as idempotent duplicate handling.

## Invalid Receipt Handling

Invalid receipts are rejected with a `REJECTED` log entry that remains in the vault for replay.

Invalid conditions include:

- bad signature
- mismatched digest
- missing `previous_merkle_root`
- invalid state transition
- empty claim
- source reference that violates protocol placeholder rules

## Replay-From-Genesis Rule

Any verifier can reconstruct the entire vault state by starting from `GENESIS_ROOT` and sequentially applying every receipt in order, verifying each `merkle_root` link.

Replayability is the constitution. Receipts are the atoms.
