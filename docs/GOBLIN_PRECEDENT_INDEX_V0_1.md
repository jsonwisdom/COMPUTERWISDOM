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

## Non-Authority Notice

This document creates a repository surface only. It does not assert runtime execution, test passage, merge, packet hash, or on-chain anchoring.
