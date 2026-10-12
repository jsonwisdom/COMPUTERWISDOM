# PMEM-IMPL-004 — Authorization + Scope Contract

Depends on: `001..003`

Authority is explicit, scoped, revocable, and purpose-bound. `AUTHORITY != IDENTITY`.

Canonical grants bind subject, object scope, independent permissions (`READ`, `REASON`, `EXPORT`, `ACT`, `DELEGATE`), purpose, validity interval, delegation flag, issuer, and status.

`AUTHORIZED(o) = GRANT_EXISTS AND SCOPE_MATCH AND PURPOSE_MATCH AND TIME_VALID AND NOT_REVOKED`. Unknown terms evaluate FALSE.

Permissions are independent: `READ != REASON != EXPORT != ACT != DELEGATE`.

For derived object `x`: `A_x subseteq A_creator intersection intersection(A_dependencies)`.

Purpose expansion requires a new authorization event. Delegation is prohibited unless explicitly granted and can only narrow authority.

Revocation immediately blocks future operations while preserving historical receipts.

EXPORT and ACT require explicit gates beyond REASON; destination, purpose, dependent scopes, and revocation state are checked fail-closed.

All GRANT/NARROW/DELEGATE/REVOKE/EXPORT_ATTEMPT/ACTION_ATTEMPT events produce receipts.

Core invariant: **NO AUTHORITY BY IMPLICATION**.

`AUTHORITY_CREATED = FALSE`
