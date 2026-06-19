# GOBLIN_COURT_V0_2_REPLAY_MANIFEST.md

## Overview

This manifest defines the operational parameters for the Replay Goblin Court V0.2. Its purpose is to use the relationship graph to generate candidate replay paths based on the sealed V0.1 foundation.

## Foundational Constraints

- **V0.1 Integrity:** The V0.1 sealed and anchored foundation remains immutable. No modifications to V0.1 logic, packet hash, or EAS attestation are permitted.
- **Witness Protocol:** GC-010 is designated as `cascade_witness` for clustered assumption-chain observations.
- **Liability Boundary:** This document makes no truth claims, no liability claims, and no warranties regarding output accuracy.
- **Authority Boundary:** Authority remains false.

## Relationship Graph Integration

The replay layer may parse the V0.2 relationship graph to identify structural nodes and edges.

- **Candidate Path Generation:** The graph may map possible trajectory sequences based on graph connectivity.
- **Scope:** Outputs are restricted exclusively to candidate paths.
- **Verification:** No runtime verification is performed by this manifest.
- **Causation Boundary:** Candidate paths do not prove causation.

## Acceptance Tests Design

Successful path candidacy is bounded by the merged V0.2 acceptance test design:

1. **Connectivity Check:** Candidate paths must follow valid graph edges.
2. **Node Preservation:** Candidate paths must use the preserved GC-001 through GC-010 node set.
3. **Edge Boundary:** Candidate paths must use allowed edge types only.
4. **GC-010 Witness Constraint:** GC-010 may witness cascades but must not judge, block, or assign blame.
5. **Candidate-Only Rule:** Traversal output must remain candidate-only.
6. **V0.1 Immutability:** V0.2 replay must not mutate sealed V0.1 receipts.

## Operational Status

```json
{
  "runtime_verified": false,
  "anchored": false,
  "authority": false
}
```

## Output Shape

```json
{
  "observed": ["GC-009"],
  "candidate_paths": [
    ["GC-001", "GC-002", "GC-009"],
    ["GC-006", "GC-009"]
  ],
  "candidate_only": true,
  "truth_claim": false,
  "liability_claim": false,
  "runtime_verified": false,
  "anchored": false,
  "authority": false
}
```

## Closure

Replay Goblin Court V0.2 is a candidate-path manifest only.

It does not execute runtime verification. It does not anchor V0.2. It does not mutate V0.1.

Authority remains false.
