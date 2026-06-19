---
artifact_id: DISPUTE_PROTOCOL_V0_1
artifact_type: protocol
status: PROPOSED
lineage_root: 57bea5c3d116bc5fa267d3e2da98626fb6ed50c6
constitutional_root: 808f2b1c6c339eb46e68a2161da3cca22f7b0eeb
authority: false
authority_boundary: NONE
authority_proof_context: Dispute Protocol defines structural dispute attachment only and grants no authority, truth, adjudication, semantic correctness, execution rights, or institutional privilege.
admission_manifest: 242
---

# Dispute Protocol V0.1

**Status:** PROPOSED  
**Authority:** false  
**Authority Boundary:** NONE  
**Lineage Root:** `57bea5c3d116bc5fa267d3e2da98626fb6ed50c6`  
**Constitutional Root:** `808f2b1c6c339eb46e68a2161da3cca22f7b0eeb`  
**Admission Manifest:** Issue #242

---

## Purpose

Dispute Protocol V0.1 defines how disputes attach to `ERS_V0_1` artifacts and `REPLAY_TRACE_V0_1` traces.

Disputes are first-class records.

Disputes reference contested content.

Disputes do not mutate prior records.

Disputes do not assert truth.

Disputes do not adjudicate.

Disputes do not grant authority.

---

## Core Invariant

> Disputes reference structure and lineage only.

No truth adjudication.

No authority escalation.

No semantic resolution.

---

## Required Fields

A `DISPUTE_V0_1` record must include:

- dispute_id
- target_artifact_id or target_trace_id
- dispute_type
- dispute_reason
- timestamp
- lineage_root
- constitutional_root
- schema_version
- authority
- authority_boundary
- hash

---

## Structural Rules

A dispute attaches to a target by reference only.

A dispute does not modify its target.

A dispute is additive.

A dispute may be replayed alongside its target.

A dispute may be superseded by future versioned artifacts, but prior dispute records remain preserved.

---

## Non-Goals

Dispute Protocol V0.1 does not:

- validate real-world truth
- score credibility
- resolve disputes
- perform adjudication
- mutate ERS artifacts
- mutate replay traces
- erase contested content
- grant authority
- infer semantic correctness

---

## Authority Boundary

```yaml
authority: false
authority_boundary: NONE
```

The protocol records contestation only.

**Authority:** false
