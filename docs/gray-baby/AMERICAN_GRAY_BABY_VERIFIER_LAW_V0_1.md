# AMERICAN GRAY BABY — VERIFIER LAW v0.1

**Class:** bounded verifier specification  
**Status:** `PROPOSED / PENDING_REPLAY_TEST`  
**FULL_VERIFIER_LAW:** `PROPOSED / PENDING_REPLAY_TEST`  
**AUTHORITY_CREATED:** `false`

## Keeper Law

> Indexer failure changes availability, not historical truth.

## Principle

> Observation systems may delay knowledge; they may not rewrite the underlying evidence.

## Existing Receipt Standard Pointer

This specification is additive to, and does not replace, the existing Drive artifact:

- **Title:** `American Gray Baby — Receipt Standard v0.1 — 2026-08-19`
- **Drive file ID:** `1eN_DhvnVD5Cb-f51brSzUCK_0vzEmw-RaNx6SvNmr1c`
- **Authority created:** `FALSE`
- **Pointer:** `https://docs.google.com/document/d/1eN_DhvnVD5Cb-f51brSzUCK_0vzEmw-RaNx6SvNmr1c/edit`

The Receipt Standard remains a separate historical artifact. This verifier law does not silently amend or supersede it.

## Four-State Model

`CANONICALITY_STATE` describes observed security position only. It does not certify semantic correctness.

### CONTENT_STATE

What the source actually published or what the pinned chain evidence establishes.

```text
UNKNOWN | OBSERVED | PASS | DELTA
```

Examples of evidence include immutable source bytes, hashes, transaction receipts, and pinned event/state reconstruction.

### INGESTION_STATE

Whether an indexer has observed the object.

```text
PENDING | OBSERVED | STALLED
```

Indexer lag does not mutate `CONTENT_STATE`.

### RENDER_STATE

What the user interface may display.

```text
HOLD_ON_RENDER | RENDER_WITH_GATE | RENDER_PASS
```

A retrieval miss must not be rendered as historical absence when ingestion is unresolved.

### CANONICALITY_STATE

Observed security position only.

```text
PRECONFIRMED
SEALED_L2
L1_BATCHED
L1_FINALIZED
REORG_HOLD
```

`CANONICALITY_STATE != semantic truth`.

## Promotion Law

```text
SOURCE_BYTES_OBSERVED
        ↓
CONTENT_STATE = PASS

Indexer missing?
        ↓
INGESTION_STATE = PENDING
RENDER_STATE    = HOLD_ON_RENDER
CONTENT_STATE   = PASS

RPC receipt binds:
transactionHash + blockNumber + blockHash + status
        ↓
CANONICALITY_STATE = SEALED_L2

Indexer catches same object
        ↓
INGESTION_STATE = OBSERVED
RENDER_STATE    = RENDER_PASS

Same blockNumber, different blockHash
        ↓
CANONICALITY_STATE = REORG_HOLD
RENDER_STATE       = HOLD_ON_RENDER
PROMOTION          = RESET
```

## Base Binding — Future-Proofed

No wall-clock duration is a verifier gate.

Observed Base performance bands may include approximately:

```text
Flashblock preconfirmation ~200 ms
sealed L2 inclusion       ~2 s
L1 batch inclusion        ~2 m
L1 finality               ~20 m
```

These are operational observations, not promotion constants.

The verifier gate binds to observed chain evidence:

```text
blockNumber + blockHash + status
```

The verifier must remain valid if Base changes block production cadence, including migration toward native canonical 200 ms blocks.

## RPC Reconstruction Requirements

### 1. INDEXER_HEAD_COMPARE

Store and compare:

```text
indexer_head.blockNumber
indexer_head.blockHash
chain_head.blockNumber
chain_head.blockHash
```

Compare indexer position with RPC evidence and, where relevant, the known transaction block.

### 2. INGESTION_PENDING

The archival layer must preserve source bytes unchanged and record ingestion state separately.

```text
CONTENT_STATE     = PASS
INGESTION_STATE   = PENDING
INGESTION_PENDING = true
RENDER_STATE      = HOLD_ON_RENDER
```

No byte is dropped or rewritten because an indexer is behind.

### 3. PINNED_ETH_CALL

Historical reads must use an explicit block boundary rather than `latest` when reconstructing historical evidence.

Use the appropriate primitive for the claim:

```text
eth_getTransactionReceipt -> transaction inclusion + status + block binding
eth_getLogs               -> event reconstruction
eth_call                  -> contract-state read at an explicit block
```

`eth_call` alone does not prove that a historical transaction occurred.

### 4. REORG_PROMOTION_GATE

Before promotion, verify that the stored receipt's `blockHash` still corresponds to the canonical block at the stored `blockNumber`.

If the hash changes under the same block number:

```text
CANONICALITY_STATE = REORG_HOLD
RENDER_STATE       = HOLD_ON_RENDER
PROMOTION          = RESET
```

Re-run receipt, log, and pinned-state verification before any new promotion.

## Evaluation State Machine

```text
INDEXER_MATCH
  -> INGESTION_STATE = OBSERVED
  -> INGESTION_PENDING = false
  -> RENDER_STATE = RENDER_PASS

INDEXER_BEHIND
  -> INGESTION_STATE = PENDING | STALLED
  -> RENDER_STATE = HOLD_ON_RENDER

INDEXER_TIMEOUT_POLICY + RPC_MATCH
  -> CONTENT_STATE = PASS
  -> SOURCE_STATE = PASS
  -> INDEXER_STATE = DEGRADED
  -> RENDER_STATE = RENDER_WITH_GATE

RPC_CONTRADICTION
  -> CONTENT_STATE = DELTA

RPC_UNAVAILABLE
  -> HOLD
```

Any timeout is an operational retry policy only. It must not imply chain finality.

## Closure Gate — Required for BOUND

All four implementation elements must be repository-bound and replay-tested:

```text
INDEXER_HEAD_COMPARE = REQUIRED
INGESTION_PENDING    = REQUIRED
PINNED_ETH_CALL      = REQUIRED
REORG_PROMOTION_GATE = REQUIRED
```

Until all four are committed and replay-tested:

```text
FULL_VERIFIER_LAW = PROPOSED / PENDING_REPLAY_TEST
AUTHORITY_CREATED = false
```

After successful repository binding and replay tests:

```text
FULL_VERIFIER_LAW = BOUND
AUTHORITY_CREATED = false
```

`BOUND` means the verifier behavior is repository-defined and replay-tested. It does not create legal, governmental, semantic, or interpretive authority.

## Boundary

```text
INDEXER_MISS        != HISTORICAL_ABSENCE
RPC_SUCCESS         != SEMANTIC_TRUTH
SEALED_L2           != L1_FINALITY
L1_FINALITY         != SEMANTIC_CORRECTNESS
RECEIPT             != AUTHORITY
RENDER_PASS         != AUTHORITY
BOUND_VERIFIER      != AUTHORITY
AUTHORITY_CREATED    = false
```
