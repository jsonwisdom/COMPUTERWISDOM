# AL Memory

**Status:** active memory surface  
**Authority:** false  
**Role:** doctrine, replay, verification, court procedure, and protocol memory

AL is the procedural memory layer for COMPUTERWISDOM.

It preserves the rules that keep expression from becoming false authority.

## Purpose

AL stores:

- ALMS doctrine
- replay rules
- court procedures
- verification gates
- receipt promotion logic
- authority:false constraints
- agent delegation boundaries

## Operating Doctrine

```text
Expression may move.
Receipts must replay.
Identity must anchor.
Authority remains false.
```

## Memory Boundary

AL does not store vibes as truth.
AL stores procedures that decide whether a claim can be replayed.

A claim enters AL only when it can be described as:

```yaml
claim: string
status: UNOBSERVED | OBSERVED | REPLAYED | REJECTED
evidence: required
authority: false
```

## Relationship to COMPUTERWISDOM

COMPUTERWISDOM creates artifacts.
AL decides whether the artifact has a replay path.

```text
Artifact
→ Receipt
→ Source
→ Timeline
→ Replay
→ Memory
```

## Current Memory Nodes

- `ALMS` — replay doctrine
- `COURTS` — Meme Court, Goblin Court, Clown Court
- `RECEIPTS` — evidence and promotion logic
- `AGENTS` — delegation, traceability, reproducibility

## Constitutional Line

No Crown.  
No Decree.  
Only Receipts.
