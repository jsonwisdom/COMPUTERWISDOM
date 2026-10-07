# Coinbase Full-History Membrane v0.1

Status: REVIEW_ONLY  
Mode: READ_ONLY  
Authority created: false

## Purpose

Coordinate a private Google Drive archive, a public GitHub control plane, and Wolfram verification without placing private Coinbase history in this public repository.

## Surface contract

- Google Drive = private raw archive, manifests, hashes, timestamp windows, completion receipts.
- GitHub = public schemas, validators, workflow logic, fixtures, audit doctrine.
- Wolfram = deterministic math over sanitized metadata or locally materialized private files.
- Human = final decision gate for any trade or execution.

## Hard membrane

```text
PRIVATE_FINANCIAL_DATA != PUBLIC_GITHUB_DATA
OBSERVATION != AUTHORITY
SIGNAL != ORDER
ORDER_CANDIDATE != EXECUTION
TIMESTAMP_DIFF != CAUSE
TRIGGER != TRADE
```

No raw account IDs, order IDs, trade IDs, balances, wallet addresses, transaction rows, or pagination cursors are committed to this repository.

## Loop

```text
COINBASE READ
  -> DRIVE RAW CHUNK
  -> DRIVE MANIFEST/HASH
  -> METADATA DIFF
  -> WOLFRAM CHECK
  -> TRIGGER CLASSIFICATION
  -> HUMAN REVIEW
  -> OPTIONAL HUMAN-AUTHORIZED EXECUTION
  -> RECEIPT
  -> REPLAY
  -> LOOP
```

The loop is circular for observation and verification. Execution is not circular and is never automatic in v0.1.

## Trigger classes

- NEW_CHUNK
- CURSOR_ADVANCED
- CURSOR_ENDED
- HASH_CHANGED
- SCHEMA_DRIFT
- TIMESTAMP_GAP
- TIMESTAMP_OVERLAP
- DUPLICATE_STABLE_ID
- HISTORY_COMPLETE
- HISTORY_INCOMPLETE
- FIELD_SEMANTICS_HOLD
- WOLFRAM_DIVERGENCE
- REVIEW_REQUIRED

Triggers create review work, not trades.

## Completion gate

Full-history status is PASS only when every requested surface has an explicit pagination terminus and all archived chunks pass hash, schema, stable-ID, and timestamp-continuity checks.

## Execution gate

```text
AUTO_EXECUTION = false
HUMAN_APPROVAL_REQUIRED = true
EXECUTION_RECEIPT_REQUIRED = true
```
