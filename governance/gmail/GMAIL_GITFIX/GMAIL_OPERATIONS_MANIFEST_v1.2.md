# GMAIL_OPERATIONS_MANIFEST v1.2

## Scope

This manifest governs Gmail GitFix cleanup work tracked under COMPUTERWISDOM issue 409.

The mailbox is treated as a perimeter and telemetry surface. Cleanup must be replay-safe, reversible where possible, and auditable.

## Current checkpoint

- Confirmed archived/labeled: 23,655
- Active inbox surface reduction: 24,986
- Render build-failed messages surfaced: 2,317
- Work label: `!Work_Item/Render`
- Deletions: 0
- Mark-read actions: 0

## Rule 0: protected mail

Protected mail must not be moved by broad cleanup lanes.

Protected terms and senders include:

- bank
- payment
- billing
- security
- login
- VA
- HRA
- housing
- rent
- court
- legal
- GitHub
- Google
- Render
- OpenAI
- Stripe

## Execution rule

Use sender-lane sampling before action.

Flow:

1. Preview query.
2. Inspect 20 to 50 messages.
3. Confirm no protected leakage.
4. Record clean or contaminated status.
5. Only then apply a label or archive.

## Authorized Operation 001

Preview Substack lane, read-only.

```text
from:substack.com older_than:1y -bank -payment -billing -security -login -VA -HRA -housing -rent -court -legal -github -google -render -openai -stripe
```

Inspection criteria:

- Sample size: first 20 to 50 messages.
- Goal: confirm newsletter or digest noise only.
- Zero protected senders.
- Zero legal or financial leakage.
- No high-value research-critical author newsletters in the sample.

## Status

GMAIL_GITFIX remains active.

v1.2 is freeze-ready for Operation 001 preview only.
