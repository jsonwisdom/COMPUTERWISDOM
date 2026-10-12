# PMEM-IMPL-002 — Receipt + Event Ledger Schema

Depends on: `PMEM-IMPL-001`

Every attempted state-changing operation produces exactly one immutable receipt, including SUCCESS, FAILURE, and REJECTION. Absence of a receipt means no recognized ledger effect.

Canonical receipt binds: `receipt_id`, `event_id`, `operation`, `target_ids`, `attempted_at`, `actor`, `authority_basis`, `dependencies`, `pre_state_ref`, `request_ref`, `result`, `reason_codes`, `post_state_ref`, `receipt_hash`.

The event ledger is append-only. Events cannot be edited, reordered, or deleted; corrections create new events.

Admission requires: `I1 AND I2 AND I3 AND POLICY_001 AND AUTHORIZED`. Failure means `EXECUTION=FALSE`, `RESULT=REJECTED`, and receipt required. A rejected request cannot be reinterpreted into another successful operation.

Admitted state changes bind canonical pre/post state hashes. FORGET receipts preserve the revocation fact but must not retain forgotten content or sufficient material to reconstruct it.

Cascade descendants receive their own linked receipts via `caused_by`.

Replay must explain WHAT happened, WHEN, TO WHICH object, BY WHOM, UNDER WHAT authority, WHICH rule admitted/rejected it, and WHAT state resulted.

Core invariant: **NO STATE CHANGE WITHOUT RECEIPT**.

`AUTHORITY_CREATED = FALSE`
