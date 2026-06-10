---
artifact_id: ERS_V0_1
artifact_type: protocol
schema_version: ERS_V0_1
status: PROPOSED
lineage_root: f5c98f688296d1cece1cb8ac6635421384756f00
constitutional_root: 808f2b1c6c339eb46e68a2161da3cca22f7b0eeb
authority: false
authority_boundary: NONE
authority_proof_context: ERS defines structure only and grants no authority, truth, adjudication, execution rights, or institutional privilege.
admission_manifest: 238
---

# Evidence Rendering Schema V0.1

**Status:** PROPOSED  
**Authority:** false  
**Authority Boundary:** NONE  
**Lineage Root:** `f5c98f688296d1cece1cb8ac6635421384756f00`  
**Constitutional Root:** `808f2b1c6c339eb46e68a2161da3cca22f7b0eeb`  
**Admission Manifest:** Issue #238

---

## Purpose

ERS V0.1 defines the canonical evidence representation used by Computer Wisdom replay, observation, and rendering systems.

ERS defines structure.

ERS does not determine truth.

ERS does not perform adjudication.

ERS does not grant authority.

---

## Core Invariant

> Every rendered conclusion must carry replayable lineage.

---

## Required Structural Block

Every ERS object must include:

```json
{
  "artifact_type": "string",
  "artifact_id": "string",
  "timestamp": "ISO8601",
  "lineage_root": "parent_admitted_artifact",
  "constitutional_root": "808f2b1c6c339eb46e68a2161da3cca22f7b0eeb",
  "schema_version": "ERS_V0_1",
  "authority": false,
  "authority_boundary": "NONE",
  "hash": "sha256_checksum"
}
```

---

## Object Types

ERS V0.1 defines five object types:

1. `event`
2. `observation`
3. `dispute`
4. `adjudication`
5. `protocol`

---

## Field Semantics

### artifact_type

The category of ERS object.

Allowed values:

- event
- observation
- dispute
- adjudication
- protocol

### artifact_id

A stable identifier for the artifact.

### timestamp

The ISO8601 timestamp associated with artifact creation or recording.

### lineage_root

The immediate admitted parent artifact, commit, or merge reference.

### constitutional_root

The Constitutional Baseline V1 merge commit:

```text
808f2b1c6c339eb46e68a2161da3cca22f7b0eeb
```

### schema_version

Must equal:

```text
ERS_V0_1
```

### authority

Must equal:

```json
false
```

### authority_boundary

Must equal:

```text
NONE
```

### hash

A SHA-256 checksum of the canonical artifact payload.

---

## Non-Claims

ERS does not claim that evidence is true.

ERS does not adjudicate disputes.

ERS does not create execution rights.

ERS does not grant institutional authority.

ERS only defines structure for replayable evidence representation.

---

## Revision Rule

ERS changes must version forward.

Prior schema versions must remain preserved.

No expiry gate is used.

Authority: false.
