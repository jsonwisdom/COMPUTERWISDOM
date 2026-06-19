# GDI_SCANNER_V0_1_DESIGN.md

## Overview

This document defines the architecture for the GDI Scanner V0.1. The scanner is an observation engine that maps system symptoms to candidate goblin paths derived from the Goblin Court V0.2 relationship graph and replay manifest.

## Status

```json
{
  "artifact": "GDI_SCANNER_V0_1_DESIGN",
  "status": "DESIGN_ONLY",
  "runtime_verified": false,
  "anchored": false,
  "authority": false
}
```

## Operational Parameters

- **Purpose:** Symptom observation and candidate path mapping.
- **GC-010 Cascade Witness:** GC-010 witnesses cascades; GC-010 does not verify, judge, block, or assign blame.
- **Non-Interference:** The scanner operates strictly in an observation-only capacity. It has no blocking, mutation, or intervention authority.

## Architecture Components

### 1. Symptom Input Stream

The scanner may consume event streams from the system environment.

Potential data sources:

```json
[
  "system_event_logs",
  "repository_metadata",
  "pull_request_lifecycle_states",
  "artifact_versioning_markers",
  "branch_and_commit_receipts",
  "workflow_status_events"
]
```

Constraint: Inputs are processed as symptomatic evidence. The scanner does not verify input truth.

### 2. Mapping Logic

The scanner may use the V0.2 relationship graph to cross-reference symptoms against known Goblin trajectories.

- **Candidate Path Generation:** Outputs represent possibilities, not definitive diagnoses.
- **Anchoring:** Forbidden by this design.
- **Mutation:** Forbidden by this design.
- **V0.1 Protection:** The scanner cannot modify V0.1 foundations, packet hashes, or EAS attestations.

### 3. Candidate Output Shape

```json
{
  "observed_inputs": [
    "repository_metadata",
    "pull_request_lifecycle_state"
  ],
  "candidate_goblins": [
    "GC-009",
    "GC-010"
  ],
  "candidate_paths": [
    ["GC-009", "GC-010"]
  ],
  "candidate_only": true,
  "truth_claim": false,
  "liability_claim": false,
  "runtime_verified": false,
  "anchored": false,
  "authority": false
}
```

## Non-Goals

```json
[
  "runtime_verification",
  "truth_claims",
  "liability_claims",
  "system_state_mutation",
  "blocking_or_intervention",
  "anchoring",
  "rewriting_v0_1",
  "assigning_blame"
]
```

## Compliance

```json
{
  "constitutional_drift": "NONE",
  "v0_1_alignment": true,
  "v0_2_relationship_graph_alignment": true,
  "v0_2_replay_manifest_alignment": true,
  "GC-010": "cascade_witness_only",
  "authority": false
}
```

## Closure

GDI Scanner V0.1 is design-only.

It observes symptoms and produces candidate goblin paths. It does not verify, judge, block, anchor, or mutate.

Authority remains false.
