# Forest Replay Validator Spec V1

## Purpose

Deterministic replay of the Receipt Vault and Merkle Forest to detect integrity violations, dangling references, and invalid state transitions.

The validator does not create truth. It only verifies that receipts produce a consistent forest or halt.

## Scope

Processes only receipted artifacts:

- `TREE_ROOT` receipts
- `BRIDGE_CONTRADICTION` receipts
- `BRIDGE_RESOLUTION_RECEIPT` receipts
- `BRIDGE_SUPERSEDES_RECEIPT` receipts
- `PUBLIC_INDEX` mirror entries

## Core Rules Enforced

- Replay detects conflict.
- Resolution is a receipt.
- Dangling references halt the forest.
- PUBLIC_INDEX is append-only mirror only.
- No receipt → no state entry.
- No canon without full replay.
- Linear sequential processing is mandatory.

## Validation Guarantees

- Every receipt must link through `previous_vault_merkle_root`.
- Status attaches only to specific receipt/root versions.
- Contradictions remain visible until explicitly receipted.
- Silent pruning is forbidden.
- Publication surfaces are mirrors, not judges.

## Canonical States

- `CANDIDATE`
- `HELD`
- `REJECTED`
- `VERIFIED_RECEIPT`
- `CANON`

## Boundary

This validator is repo-governance infrastructure only. It does not imply external authority, surveillance, classified access, or publication truth.

## Final Line

A validator does not decide truth by authority. It replays receipts until the forest either converges or halts.
