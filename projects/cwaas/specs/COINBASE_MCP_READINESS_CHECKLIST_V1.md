# COINBASE_MCP_READINESS_CHECKLIST_V1

Status: REVIEW_ONLY
Lane: CWaaS / Agent Pay
Repository: jsonwisdom/COMPUTERWISDOM
Branch: boss-bre-coinbase-mcp-review-v1

## Purpose

This checklist records the Boss Bre review gate for the Coinbase MCP adapter lane.

The checklist is evidence, not narrative. Any unchecked item keeps the adapter in preview-only dry-run mode.

## Checklist

```text
[ ] Preview receipt + replay PASS present
[ ] Human approval receipt present (/approve-agent-pay)
[ ] Identity binding (JAYWISDOM.eth) verified
[ ] Payment payload schema compliant
[ ] Adapter in DRY_RUN mode only
[ ] External adapter activity blocked until human gate is satisfied
[ ] Receipt + hash written back on every step
[ ] No funds moved, no chain action in preview
[ ] Full replay trace for every adapter run
```

## Boss Bre Lock

```text
No premature execution.
No funds moved in preview.
No chain action in preview.
No adapter green without receipts.
No fake green.
```
