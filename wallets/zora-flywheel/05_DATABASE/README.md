# ZORA FLYWHEEL — APPEND-ONLY DATABASE

Perspective: Jason's daily operating history.

The database is an event ledger, not a mutable biography. New facts and experiences append. Corrections append a later corrective record that points to the earlier record; prior rows are never silently erased.

```text
STATE[t+1] = REPLAY(STATE[t], DELTA[t+1])
```

A useful "quantum" is the smallest auditable progress packet:

```text
Q = FACT + RECEIPT + AUDIT + (FIX if needed) + RECOMMENDATION
```

"Quantum" is an engineering metaphor here, not a physics claim.

Public state may contain classifications, counts, statuses, receipts, and recommendations. Public state must not contain private keys, credentials, bank account numbers, or raw private financial connector payloads.
