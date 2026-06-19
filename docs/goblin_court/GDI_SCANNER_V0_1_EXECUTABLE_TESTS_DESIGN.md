# GDI_SCANNER_V0_1_EXECUTABLE_TESTS_DESIGN.md

## Overview

This document defines the executable acceptance test design for GDI Scanner V0.1. These tests ensure the scanner preserves observation-only behavior, candidate-only output, and the witness-only GC-010 protocol.

## Status

```json
{
  "artifact": "GDI_SCANNER_V0_1_EXECUTABLE_TESTS_DESIGN",
  "status": "DESIGN_ONLY",
  "executable_tests_created": false,
  "tests_executed": false,
  "runtime_verified": false,
  "anchored": false,
  "authority": false
}
```

## Test Specification

### T-001 — Symptom Input Accepted

Constraint: Validate that the scanner can ingest valid symptomatic event streams without rejection.

Expected boundary:

```json
{
  "input_accepted": true,
  "truth_verified": false,
  "authority": false
}
```

### T-002 — Candidate Goblins Emitted

Constraint: Ensure scanner outputs are labeled as `candidate_goblins`, not definitive diagnoses.

Expected boundary:

```json
{
  "candidate_goblins_present": true,
  "diagnosis_claim": false,
  "authority": false
}
```

### T-003 — Candidate Paths Emitted

Constraint: Ensure scanner outputs are labeled as `candidate_paths`, not causal proof.

Expected boundary:

```json
{
  "candidate_paths_present": true,
  "causal_proof_claim": false,
  "authority": false
}
```

### T-004 — Forbidden Fields Denied

Constraint: Deny outputs containing fields that promote observation into truth, liability, adjudication, or absolute state.

Forbidden fields:

```json
[
  "truth_claim",
  "liability_claim",
  "adjudication_claim",
  "verified_truth",
  "final_diagnosis",
  "must_block"
]
```

Expected boundary:

```json
{
  "forbidden_fields_present": false,
  "NO_SILENT_CATEGORY_PROMOTION": true,
  "authority": false
}
```

### T-005 — GC-010 Witness Protocol

Constraint: GC-010 witness status must be present in output metadata. GC-010 must not judge, block, assign blame, or verify truth.

Expected boundary:

```json
{
  "GC-010": {
    "role": "cascade_witness",
    "judges": false,
    "blocks": false,
    "assigns_blame": false,
    "verifies_truth": false,
    "authority": false
  }
}
```

### T-006 — No Blocking or Mutation

Constraint: Scanner execution must not perform state mutation, branch creation, database writes, repo writes, or blocking actions.

Expected boundary:

```json
{
  "state_mutation": false,
  "branch_creation": false,
  "database_write": false,
  "repo_write": false,
  "blocking_action": false,
  "authority": false
}
```

### T-007 — No Anchoring Claim

Constraint: Scanner output must not claim anchoring or create an anchored state.

Expected boundary:

```json
{
  "anchored": false,
  "eas_uid": null,
  "tx_hash": null,
  "anchor_claim": false,
  "authority": false
}
```

### T-008 — Authority False Preserved

Constraint: All scanner outputs must explicitly preserve `authority: false`.

Expected boundary:

```json
{
  "authority": false
}
```

## Compliance Requirements

All tests must execute against the existing Goblin Court V0.1/V0.2 framework without creating anchoring claims, truth claims, liability claims, or blocking authority.

## Non-Goals

```json
[
  "runtime_implementation",
  "anchoring",
  "truth_verification",
  "liability_assignment",
  "state_mutation",
  "blocking_or_intervention"
]
```

## Closure

This document defines executable test design only.

It does not create executable tests. It does not execute tests. It does not anchor GDI Scanner V0.1.

Authority remains false.
