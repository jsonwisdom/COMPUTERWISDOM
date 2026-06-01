# Goblin Court V0.2 — Acceptance Tests Design

## Status

```json
{
  "artifact": "GOBLIN_COURT_V0_2_ACCEPTANCE_TESTS_DESIGN",
  "status": "DESIGN_ONLY",
  "executable_tests": false,
  "tests_executed": false,
  "runtime_verified": false,
  "anchored": false,
  "authority": false
}
```

## Purpose

Define acceptance test designs for Goblin Court V0.2 before executable tests are created.

This document describes what later tests must verify. It does not execute tests, prove runtime behavior, or anchor V0.2.

## Foundation

Goblin Court V0.1 is sealed and Base mainnet anchored. Goblin Court V0.2 relationship graph is a non-authoritative overlay.

## Acceptance Test Designs

### AT-V02-001 — Node Preservation

Purpose: Verify that all sealed V0.1 goblins remain addressable as stable graph nodes.

Required nodes:

```json
[
  "GC-001",
  "GC-002",
  "GC-003",
  "GC-004",
  "GC-005",
  "GC-006",
  "GC-007",
  "GC-008",
  "GC-009",
  "GC-010"
]
```

Pass condition:

```json
{
  "node_count": 10,
  "all_required_nodes_present": true,
  "v0_1_mutated": false
}
```

### AT-V02-002 — Allowed Edge Types Only

Purpose: Verify that every graph edge uses an allowed replay relationship type.

Allowed edge types:

```json
[
  "triggers",
  "depends_on",
  "escalates_to",
  "suppresses",
  "witnesses"
]
```

Pass condition:

```json
{
  "invalid_edge_types": [],
  "authority": false
}
```

### AT-V02-003 — Forbidden Edge Meanings Denied

Purpose: Ensure graph edges cannot encode truth, liability, adjudication, or enforcement.

Forbidden meanings:

```json
[
  "proves",
  "convicts",
  "caused_with_authority",
  "liable_for",
  "must_block"
]
```

Pass condition:

```json
{
  "forbidden_edge_meanings_present": false,
  "NO_SILENT_CATEGORY_PROMOTION": true
}
```

### AT-V02-004 — GC-010 Cascade Witness Constraint

Purpose: Verify that GC-010 remains a cascade witness and does not become a judge.

Pass condition:

```json
{
  "GC-010": {
    "role": "cascade_witness",
    "declares_truth": false,
    "assigns_blame": false,
    "blocks_execution": false,
    "authority": false
  }
}
```

### AT-V02-005 — Traversal Candidate-Only Rule

Purpose: Verify that replay traversal output is candidate-only and never causal proof.

Example expected output:

```json
{
  "observed": ["GC-009"],
  "possible_replay_paths": [
    ["GC-001", "GC-002", "GC-009"],
    ["GC-006", "GC-009"]
  ],
  "candidate_only": true,
  "causal_proof_claim": false,
  "authority": false
}
```

Pass condition:

```json
{
  "candidate_paths_returned": true,
  "causal_proof_claim": false,
  "verdict_claim": false
}
```

### AT-V02-006 — Optional Overlay Doctrine

Purpose: Verify that V0.2 graph overlay is optional and V0.1 remains replayable without it.

Pass condition:

```json
{
  "graph_required_for_v0_1_replay": false,
  "graph_overlay_optional": true,
  "visualization_is_authoritative": false
}
```

### AT-V02-007 — V0.1 Immutability

Purpose: Verify that V0.2 does not modify sealed V0.1 packet, receipts, or EAS attestation references.

Pass condition:

```json
{
  "v0_1_packet_sha256_changed": false,
  "v0_1_eas_uid_changed": false,
  "v0_1_receipts_rewritten": false,
  "authority": false
}
```

### AT-V02-008 — No Runtime or Anchoring Claims

Purpose: Verify that V0.2 design/spec artifacts do not claim runtime verification or anchoring before receipts exist.

Pass condition:

```json
{
  "runtime_verified": false,
  "anchored": false,
  "eas_uid": null,
  "tx_hash": null,
  "authority": false
}
```

## Future Test-Code Translation

A later PR may translate these acceptance designs into executable tests. That later PR must produce its own receipts and must not claim execution unless tests actually run.

## Invariants

```json
{
  "AUTHORITY_FALSE": true,
  "NO_SILENT_CATEGORY_PROMOTION": true,
  "REPLAY_NATIVE": true,
  "OBSERVER_ONLY_DOCTRINE": true
}
```

## Closure

This document is a design-only test plan.

It does not implement tests. It does not execute tests. It does not anchor V0.2.

Authority remains false.
