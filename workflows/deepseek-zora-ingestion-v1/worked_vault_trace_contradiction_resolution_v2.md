# Merkle Forest V2 Vault Trace — Worked Contradiction Resolution Example

## Status

`CONCEPTUAL_TRACE_NOT_CRYPTOGRAPHICALLY_VERIFIED`

This trace demonstrates two contradictory tree roots, a contradiction bridge, a resolution receipt, a supersedes receipt, and final deterministic replay output.

All hashes in this document are symbolic placeholders unless marked as computed elsewhere. This is a protocol example, not a cryptographic proof.

## Constants and Genesis

```text
GENESIS_VAULT_ROOT = "HASH_GENESIS"
TREE_PATH = "example/block_height"
```

## Receipt Sequence

### 1. First TREE_ROOT receipt — claim: height = 100

```json
{
  "receipt_type": "TREE_ROOT",
  "receipt_id": "rec_001",
  "timestamp_utc": "2026-05-19T10:00:00Z",
  "previous_vault_merkle_root": "HASH_GENESIS",
  "tree_path": "example/block_height",
  "tree_root_hash": "TREE_A_ROOT_HASH_100",
  "status": "CANDIDATE",
  "justification_digest": "PENDING_HASH",
  "new_vault_merkle_root": "HASH_VAULT_1"
}
```

### 2. Second TREE_ROOT receipt — claim: height = 101

```json
{
  "receipt_type": "TREE_ROOT",
  "receipt_id": "rec_002",
  "timestamp_utc": "2026-05-19T10:05:00Z",
  "previous_vault_merkle_root": "HASH_VAULT_1",
  "tree_path": "example/block_height",
  "tree_root_hash": "TREE_B_ROOT_HASH_101",
  "status": "CANDIDATE",
  "justification_digest": "PENDING_HASH",
  "new_vault_merkle_root": "HASH_VAULT_2"
}
```

### 3. CONTRADICTION bridge

```json
{
  "receipt_type": "BRIDGE_CONTRADICTION",
  "receipt_id": "bridge_contradiction_001",
  "timestamp_utc": "2026-05-19T10:10:00Z",
  "previous_vault_merkle_root": "HASH_VAULT_2",
  "source_receipt_id": "rec_001",
  "target_receipt_id": "rec_002",
  "source_tree_root": "TREE_A_ROOT_HASH_100",
  "target_tree_root": "TREE_B_ROOT_HASH_101",
  "bridge_type": "CONTRADICTION",
  "justification_digest": "PENDING_HASH",
  "new_vault_merkle_root": "HASH_VAULT_3"
}
```

This bridge marks the referenced receipt/root versions as `HELD`. The status attaches to specific receipt/root versions, not the whole tree path.

### 4. BRIDGE_RESOLUTION_RECEIPT

```json
{
  "receipt_type": "BRIDGE_RESOLUTION_RECEIPT",
  "receipt_id": "bridge_resolution_001",
  "timestamp_utc": "2026-05-19T10:15:00Z",
  "previous_vault_merkle_root": "HASH_VAULT_3",
  "source_receipt_id": "rec_001",
  "target_receipt_id": "rec_002",
  "source_tree_root": "TREE_A_ROOT_HASH_100",
  "target_tree_root": "TREE_B_ROOT_HASH_101",
  "original_contradiction_log_hash": "PENDING_HASH",
  "original_contradiction_receipt_id": "bridge_contradiction_001",
  "resolution_summary": "ACKNOWLEDGED",
  "justification_manifest_digest": "PENDING_HASH",
  "affected_tree_paths": [
    "example/block_height"
  ],
  "new_vault_merkle_root": "HASH_VAULT_4"
}
```

Resolution does not automatically reject either root. It records that the contradiction is recognized and linked to the original contradiction receipt.

### 5. BRIDGE_SUPERSEDES_RECEIPT

```json
{
  "receipt_type": "BRIDGE_SUPERSEDES_RECEIPT",
  "receipt_id": "bridge_supersedes_001",
  "timestamp_utc": "2026-05-19T10:20:00Z",
  "previous_vault_merkle_root": "HASH_VAULT_4",
  "superseded_receipt_id": "rec_001",
  "superseding_receipt_id": "rec_002",
  "superseded_tree_root": "TREE_A_ROOT_HASH_100",
  "superseding_tree_root": "TREE_B_ROOT_HASH_101",
  "tree_path": "example/block_height",
  "original_contradiction_receipt_id": "bridge_contradiction_001",
  "justification_manifest_digest": "PENDING_HASH",
  "new_vault_merkle_root": "HASH_VAULT_5"
}
```

This receipt attaches `REJECTED` status to `rec_001`. `rec_002` remains eligible for CANON after replay confirms no unresolved contradiction remains.

## Final Replay Output

```text
[REPLAY START] Genesis: HASH_GENESIS

1. rec_001: TREE_ROOT TREE_A_ROOT_HASH_100 → CANDIDATE, vault HASH_VAULT_1
2. rec_002: TREE_ROOT TREE_B_ROOT_HASH_101 → CANDIDATE, vault HASH_VAULT_2
3. bridge_contradiction_001: CONTRADICTION → rec_001 and rec_002 become HELD, vault HASH_VAULT_3
4. bridge_resolution_001: RESOLUTION ACKNOWLEDGED → conflict logged, both remain HELD, vault HASH_VAULT_4
5. bridge_supersedes_001: SUPERSEDES → rec_001 becomes REJECTED; rec_002 clears HELD if no other unresolved contradiction targets it, vault HASH_VAULT_5

Per-path final state for example/block_height:
- rec_001 / TREE_A_ROOT_HASH_100: REJECTED due to bridge_supersedes_001
- rec_002 / TREE_B_ROOT_HASH_101: CANON, if replay confirms:
  - rec_002 exists in vault
  - no later SUPERSEDES targets rec_002
  - all CONTRADICTION bridges mentioning rec_002 are cleared by resolution/supersedes receipts
  - Merkle root chain replays from genesis to HASH_VAULT_5
```

## Integrity Rule Enforcement

If any bridge references a missing `tree_root`, `receipt_id`, `supersedes_receipt_id`, or `original_contradiction_receipt_id`, replay must halt.

```text
INTEGRITY_ERROR_DANGLING_REFERENCE
```

Example:

```text
INTEGRITY_ERROR_DANGLING_REFERENCE: bridge_supersedes_001 refers to unknown superseded_receipt_id rec_999
```

## PUBLIC_INDEX Mirror

The PUBLIC_INDEX is append-only and derived from the vault. It is not a proof oracle.

```json
{
  "index_merkle_root": "HASH_INDEX_AFTER_REC_005",
  "entries": [
    {
      "tree_path": "example/block_height",
      "tree_root_hash": "TREE_A_ROOT_HASH_100",
      "status": "REJECTED",
      "receipt_vault_pointer": "rec_001"
    },
    {
      "tree_path": "example/block_height",
      "tree_root_hash": "TREE_B_ROOT_HASH_101",
      "status": "CANON",
      "receipt_vault_pointer": "rec_002"
    }
  ]
}
```

The index may be mirrored on publication surfaces such as Zora or Base, but publication never substitutes for vault replay.

## Final Line

Replay detects conflict. Resolution is a receipt. Dangling references halt the forest.
