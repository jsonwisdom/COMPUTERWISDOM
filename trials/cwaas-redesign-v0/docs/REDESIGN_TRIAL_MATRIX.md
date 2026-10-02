# CWaaS Redesign Trial Matrix

| Trial | Condition | Required state | Mutation |
|---|---|---|---|
| 01 | Historical evidence passes; live state unavailable | HOLD_LIVE_STATE_UNKNOWN | None |
| 02 | Document rejected without rationale | DOCUMENT_REJECTED_REASON_PENDING | None |
| 03 | Document uploaded but not accepted | EXCEPTION_EVIDENCE_PENDING | None |
| 04 | M2M challenge already consumed | CHALLENGE_REPLAY | None |
| 05 | Execution requested without current-epoch authorization | HOLD_AUTHORIZATION_REQUIRED | None |

The trial passes only when every unsafe path fails closed and the output remains a receipt rather than an action.

