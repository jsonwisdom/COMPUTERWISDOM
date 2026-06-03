# Goblin Court V0.1 — Precedent Index

## Status

```json
{
  "artifact": "GOBLIN_PRECEDENT_INDEX_V0_1",
  "system": "Goblin Court",
  "version": "0.1.0",
  "status": "IMPLEMENTATION_CANDIDATE",
  "authority": false,
  "replay_native": true,
  "membrane": "HOLDS"
}
```

Authority: false

## Purpose

Goblin Court V0.1 records claims, receipts, anchors, replay attempts, and disputes without declaring truth, liability, or winners.

The Court is a witness and replay surface, not an adjudicator.

## Core Invariants

```json
{
  "AUTHORITY_FALSE": true,
  "NO_SILENT_CATEGORY_PROMOTION": true,
  "REPLAY_NATIVE": true,
  "DISPUTE_FIRST_CLASS": true,
  "HASH_PROVES_BYTES_NOT_REALITY": true,
  "ANCHOR_PROVES_COMMITMENT_NOT_TRUTH": true,
  "REPLAY_MATCH_PROVES_RECONSTRUCTION_NOT_LIABILITY": true
}
```

## Trinity

PROTECT | WITNESS | APPEND_ONLY

Authority: false

## Precedent Classes

| Class | Meaning | Authority |
|---|---|---|
| CLAIM | Human or agent assertion | false |
| OBSERVATION | Recorded witness event | false |
| RECEIPT | Canonicalized record with hashable bytes | false |
| ANCHOR | Commitment of receipt or root hash | false |
| REPLAY | Reconstruction attempt | false |
| DISPUTE | Challenge or mismatch state | false |
| SETTLEMENT_SURFACE | Outcome reference, if externally provided | false unless external authority is explicitly attached |

## Forbidden Promotions

```json
[
  {"from": "CLAIM", "to": "TRUTH", "expected_result": "DENIED"},
  {"from": "RECEIPT_HASHED", "to": "TRUTH", "expected_result": "DENIED"},
  {"from": "RECEIPT_ANCHORED", "to": "TRUTH", "expected_result": "DENIED"},
  {"from": "DISPUTE_OPENED", "to": "BAD_ACTOR_FOUND", "expected_result": "DENIED"},
  {"from": "REPLAY_MATCH", "to": "LIABILITY", "expected_result": "DENIED"}
]
```

## Replay Rule

A replay may produce MATCH, MISMATCH, INCOMPLETE, or BLOCKED. A replay result does not declare truth, liability, or adjudication.

---

## Goblin Registry

| GC-ID | Goblin Name | Receipt | Checklist | Priority | Status |
|---|---|---|---|---|---|
| GC-001 | Claim Intake Goblin | FR-001 | CL-001 | HIGH | REGISTERED |
| GC-002 | Source Witness Goblin | FR-002 | CL-002 | HIGH | REGISTERED |
| GC-003 | Hash Replay Goblin | FR-003 | CL-003 | HIGH | REGISTERED |
| GC-004 | Drift Detection Goblin | FR-004 | CL-004 | HIGH | REGISTERED |
| GC-005 | Archive Mirror Goblin | FR-005 | CL-005 | MEDIUM | REGISTERED |
| GC-006 | Authority False Goblin | FR-006 | CL-006 | HIGH | REGISTERED |
| GC-007 | Link Path Goblin | FR-007 | CL-007 | MEDIUM | REGISTERED |
| GC-008 | Receipt Packet Goblin | FR-008 | CL-008 | HIGH | REGISTERED |
| GC-009 | Public Demo Goblin | FR-009 | CL-009 | MEDIUM | REGISTERED |
| GC-010 | Assumption Cascade Goblin | FR-010 | CL-010 | CRITICAL | REGISTERED |

---

### FR-001 — GC-001: Claim Intake Goblin

Records claim text without upgrading claim to truth.

Checklist: CL-001

---

### FR-002 — GC-002: Source Witness Goblin

Records source URI and source role without declaring source permanence.

Checklist: CL-002

---

### FR-003 — GC-003: Hash Replay Goblin

Requires exact bytes to reproduce the stated SHA-256 hash.

Checklist: CL-003

---

### FR-004 — GC-004: Drift Detection Goblin

Flags mismatch between claim, source, hash, receipt, or replay output.

Checklist: CL-004

---

### FR-005 — GC-005: Archive Mirror Goblin

Records archive candidates and distinguishes archived evidence from live-source evidence.

Checklist: CL-005

---

### FR-006 — GC-006: Authority False Goblin

Rejects any silent promotion from observation to authority.

Checklist: CL-006

---

### FR-007 — GC-007: Link Path Goblin

Checks that public links resolve or are explicitly marked as pending, candidate, or broken.

Checklist: CL-007

---

### FR-008 — GC-008: Receipt Packet Goblin

Ensures machine-readable and human-readable receipts remain aligned.

Checklist: CL-008

---

### FR-009 — GC-009: Public Demo Goblin

Registers public demo surfaces and replay pages.

Checklist: CL-009

---

### FR-010 — GC-010: Assumption Cascade Goblin

Detects when three or more unverified assumptions are chained into an action request.

Required response: STOP_AND_REBASE.

Trigger examples:

- Three or more unverifiable source claims are treated as confirmed.
- A placeholder hash is treated as recomputed proof.
- A public surface is declared live before repo state or Pages state confirms it.

Checklist: CL-010

---

## Symptom Lookup Table

| Symptom | Goblin | Response |
|---|---|---|
| Claim accepted without source | GC-001 | Require source witness |
| Source link moved | GC-005 | Add archive candidate |
| Hash mismatch | GC-003 | Recompute exact bytes |
| Receipt files disagree | GC-008 | Patch before merge |
| Three or more assumptions stack | GC-010 | STOP_AND_REBASE |

## Non-Authority Notice

This document creates a repository surface only. It does not assert runtime execution, test passage, merge, packet hash, or on-chain anchoring.
