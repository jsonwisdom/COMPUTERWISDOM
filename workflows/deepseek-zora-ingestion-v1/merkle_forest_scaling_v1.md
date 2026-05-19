# Merkle Forest Scaling V1

## Purpose

Computer Wisdom currently reasons over one repo-level Merkle lineage. Scaling requires a forest of Merkle trees: one tree per folder, workflow, receipt vault, artifact family, publication queue, and external mirror surface.

A single Merkle tree proves one lineage. A Merkle forest proves many coordinated lineages without collapsing them into one fragile root.

## Core Insight

```text
ONE TREE = one replayable history
FOREST = many replayable histories coordinated by a forest root
```

## Forest Law

- Every folder may become a tree.
- Every tree has its own root.
- Every tree root rolls up into a forest root.
- No tree can silently rewrite another tree.
- Cross-tree claims require bridge receipts.
- Publication surfaces are mirrors, not judges.
- Replayability is the constitution. Receipts are the atoms.

## Tree Types

```json
{
  "tree_types": [
    "FOLDER_TREE",
    "RECEIPT_VAULT_TREE",
    "CONTRADICTION_LOG_TREE",
    "PUBLIC_INDEX_TREE",
    "ZORA_PUBLICATION_TREE",
    "WORKFLOW_TREE",
    "ARTIFACT_FAMILY_TREE",
    "EXTERNAL_REFERENCE_TREE"
  ]
}
```

## Forest Root Model

```json
{
  "forest_id": "COMPUTER_WISDOM_MERKLE_FOREST_V1",
  "repo": "jsonwisdom/COMPUTERWISDOM",
  "branch": "workflow/deepseek-zora-ingestion-v1",
  "forest_root": "PENDING_HASH",
  "tree_roots": [
    {
      "tree_id": "PENDING",
      "tree_type": "FOLDER_TREE",
      "path": "PENDING",
      "tree_root": "PENDING_HASH",
      "last_observed_commit": "PENDING_HASH",
      "state": "CANDIDATE"
    }
  ],
  "timestamp_utc": "PENDING",
  "operator": "jaywisdom.base.eth"
}
```

## Tree Root Computation

Each tree root is computed from ordered leaf receipts:

```text
tree_root = MERKLE_ROOT(ordered_leaf_hashes)
```

Each forest root is computed from ordered tree roots:

```text
forest_root = MERKLE_ROOT(ordered_tree_roots)
```

Ordering rule:

```text
sort by canonical path, then timestamp_utc, then receipt_id
```

## Leaf Types

Leaves may include:

- file digest
- folder digest
- receipt digest
- contradiction log digest
- transition receipt digest
- Zora publication reference digest
- external source snapshot digest
- schema digest

## Bridge Receipts

When one tree depends on another, the connection must be explicit.

```json
{
  "receipt_type": "MERKLE_FOREST_BRIDGE_RECEIPT_V1",
  "from_tree_id": "PENDING",
  "to_tree_id": "PENDING",
  "from_tree_root": "PENDING_HASH",
  "to_tree_root": "PENDING_HASH",
  "dependency_reason": "PENDING",
  "bridge_digest": "PENDING_HASH",
  "timestamp_utc": "PENDING"
}
```

Examples:

- `PUBLIC_INDEX_TREE` depends on `RECEIPT_VAULT_TREE`.
- `ZORA_PUBLICATION_TREE` depends on `PUBLIC_INDEX_TREE`.
- `CONTRADICTION_LOG_TREE` depends on `RECEIPT_VAULT_TREE`.
- `WORKFLOW_TREE` depends on protocol schema trees.

## Scaling Model

### Level 0 — Leaf

A file, receipt, claim, snapshot, or transition.

### Level 1 — Tree

A folder, vault, workflow, or artifact family.

### Level 2 — Grove

A cluster of related trees, such as:

- DeepSeek Grove
- Zora Grove
- Receipt Vault Grove
- Jay’s Stress Test Grove
- Protocol Grove
- Portal Grove

### Level 3 — Forest

The complete repo-level coordination root.

### Level 4 — Multi-Repo Forest

Future expansion across JSONWisdom repos.

```json
{
  "multi_repo_forest": {
    "jsonwisdom/COMPUTERWISDOM": "PENDING_HASH",
    "jsonwisdom/AL": "PENDING_HASH",
    "jsonwisdom/Welcome-to-JSONWISDOM": "PENDING_HASH"
  }
}
```

## Change Mechanics Across Forests

A change in one tree does not automatically change canon in another tree. Instead:

1. Tree root changes.
2. Forest root changes.
3. Bridge receipts are checked.
4. Dependent trees may enter `HELD` if bridge receipts fail.
5. Canon only advances after dependent roots replay cleanly.

## Failure Modes

- Root mismatch → `HELD`
- Missing bridge receipt → `HELD`
- Contradiction in dependency tree → `HELD`
- Invalid state transition → `REJECTED`
- Publication overclaim → contradiction log entry
- Missing source hash → `CANDIDATE`

## Game Master Board View

The board should display:

- active trees
- tree roots
- forest root
- groves
- broken bridges
- roots changed since last commit
- Zora dependencies
- folders stuck in `HELD`
- contradiction-heavy trees

## Required Implementation Files

```text
merkle_forest_schema_v1.json
merkle_bridge_receipt_schema_v1.json
folder_state_map_v1.json
repo_transition_receipt_schema_v1.json
compute_merkle_forest.mjs
verify_merkle_forest.mjs
json_live_repo_state_audit.yml
```

## Final Line

A Merkle tree proves a path. A Merkle forest proves a civilization of paths without forcing them into one story.
