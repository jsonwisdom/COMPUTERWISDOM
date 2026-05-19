# Byte Verification Epochs · Compute Wisdom

Status: Candidate infrastructure.
Operator: jaywisdom.eth / jaywisdom.base.eth
Scope: daily, weekly, and monthly byte-by-byte verification for Computer Wisdom public surfaces and receipt chains.

## Purpose

Use Compute Wisdom to verify public civic memory byte by byte.

Daily checks protect the moving ledger.
Weekly checks update the public page.
Monthly checks summarize drift, proof, and unresolved HELD items.

## Verification Levels

| Level | Cadence | Target | Output |
|---|---|---|---|
| Daily | every ledger day | daily receipts and changed artifacts | daily byte receipt |
| Weekly | every week | portal.html + active public pointers | weekly portal byte receipt + public page update |
| Monthly | every month | receipt chain, batch packets, snapshots, court locks | monthly verification summary |

## Byte Rule

A file is verified only when these are recorded:

1. path
2. branch or commit ref
3. blob SHA or SHA-256
4. byte count when available
5. expected status
6. boundary flags
7. next action

## Weekly Public Page Rule

`portal.html` may be updated weekly only after a portal mutation receipt exists.

The weekly page update must show:

- current weekly verification receipt
- portal file blob SHA
- active daily epoch status
- unresolved HELD items, if any
- boundary statement: no public badge, no live onchain claim, no authority claim unless separately receipted

## Standard Path

```text
Daily receipt -> weekly byte manifest -> portal mutation receipt -> portal update -> commit-pinned snapshot -> Grok/AI counter-review -> weekly court-lock
```

## Canon

Byte by byte.
Day by day.
Week by week.
Month by month.
Floating pages drift. Commit-pinned bytes settle.
