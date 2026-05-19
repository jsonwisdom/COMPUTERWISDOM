# Grok Batch Receipts · Compute Wisdom Shortcut Layer

Status: Candidate infrastructure.
Operator: jaywisdom.eth / jaywisdom.base.eth
Purpose: Give Grok a compact, machine-readable batch receipt packet so it stops hand-waving and stops re-discovering branch/path/commit state one file at a time.

## Problem

Grok repeatedly fails when it reviews isolated claims without a complete trace packet.

Observed failure modes:

- wrong branch assumption, usually `main` instead of `master`
- file path checked without commit or blob SHA
- verdict issued before field-level trace
- placeholder treated as repo failure instead of normal HELD state
- public pointer confused with proof
- candidate entry confused with badge or live claim

## Shortcut Rule

Before Grok reviews a claim, provide a batch packet containing:

1. branch
2. file path
3. commit SHA
4. blob SHA when available
5. field map
6. boundary flags
7. parent receipts
8. allowed verdicts
9. replacement rule
10. next artifact

## Batch Packet Types

| Packet | Purpose |
|---|---|
| `TRACE_PACKET` | Prove file/branch/commit/blob exists |
| `FIELD_PACKET` | Map fields to claims |
| `BOUNDARY_PACKET` | Confirm false flags: badge/onchain/legal/etc. |
| `PLACEHOLDER_PACKET` | State whether placeholder is HELD or replaceable |
| `COUNTER_REVIEW_PACKET` | Archive reviewer verdict and next action |
| `PARENT_UPDATE_PACKET` | Authorize parent file update after review |
| `COURT_LOCK_PACKET` | Seal verified candidate entry |

## Grok Review Order

```text
Batch Packet -> Evidence Table -> Boundary Check -> Missing Proof -> Verdict -> JSON Receipt
```

Grok must not output a verdict before the Evidence Table.

## 05-20 Current Workflow

1. Parent daily candidate created.
2. Grok found placeholder and requested evidence.
3. Evidence intake candidate created.
4. Evidence item filled as process move.
5. Grok reviewed item as `READY_TO_REPLACE_PLACEHOLDER`.
6. Parent daily candidate updated with reviewed process item.
7. Final Grok review now required.
8. If passed, court-lock 05-20.

## Canon

No conclusion before trace.
No batch review without branch, path, commit, and field map.
Grok gets shortcuts only when the shortcuts are receipts.
Compute Wisdom validates by receipts.
