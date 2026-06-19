---
artifact_id: REPLAY_KERNEL_V0_1
artifact_type: protocol
status: PROPOSED
lineage_root: a42678a5484ffb238dd1ffe66ced595ccd392d33
constitutional_root: 808f2b1c6c339eb46e68a2161da3cca22f7b0eeb
authority: false
authority_boundary: NONE
authority_proof_context: Replay Kernel defines deterministic execution over ERS_V0_1 artifacts only and grants no authority, truth, adjudication, semantic correctness, execution rights, or institutional privilege.
admission_manifest: 240
---

# Replay Kernel V0.1

**Status:** PROPOSED  
**Authority:** false  
**Authority Boundary:** NONE  
**Lineage Root:** `a42678a5484ffb238dd1ffe66ced595ccd392d33`  
**Constitutional Root:** `808f2b1c6c339eb46e68a2161da3cca22f7b0eeb`  
**Admission Manifest:** Issue #240

---

## Purpose

Replay Kernel V0.1 defines deterministic replay execution over `ERS_V0_1` artifacts.

The kernel computes structure and lineage only.

It does not assert truth.

It does not resolve disputes.

It does not grant authority.

---

## Inputs

The kernel accepts a list of `ERS_V0_1` artifacts.

Each artifact must validate against:

```text
schemas/ers.v0_1.schema.json
```

---

## Replay-Critical Fields

The kernel reads only:

- artifact_id
- artifact_type
- timestamp
- lineage_root
- constitutional_root
- schema_version
- hash
- authority
- authority_boundary

Optional fields may be preserved but must not affect deterministic validity.

---

## Execution Contract

Given identical input artifacts, the kernel must emit identical replay traces.

The deterministic ordering rule is:

1. timestamp ascending
2. artifact_id ascending
3. hash ascending

The kernel emits:

- trace_id
- schema_version
- constitutional_root
- artifact_count
- ordered_artifact_ids
- lineage_edges
- replay_hash
- authority
- authority_boundary

---

## Rejection Rules

The kernel rejects artifacts where:

- schema_version is not ERS_V0_1
- authority is not false
- authority_boundary is not NONE
- constitutional_root is not the Constitutional Baseline V1 root
- required replay-critical fields are missing

---

## Non-Goals

Replay Kernel V0.1 does not:

- validate real-world truth
- score credibility
- resolve disputes
- perform adjudication
- mutate external systems
- grant authority
- infer semantic correctness
- privilege one observation over another

---

## Core Invariant

> Every rendered conclusion must carry replayable lineage.

Replay output is provenance, not judgment.

**Authority:** false
