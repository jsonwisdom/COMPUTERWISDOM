# PMEM-IMPL-008 — Custody + Retention + Replication Contract

Depends on: `001..007`

`POSSESSION != AUTHORITY` and `MEMORY != COPY`.

Each materialized copy is attributable by `copy_id`, `memory_id`, `content_ref`, storage class (`PRIMARY|REPLICA|CACHE|BACKUP|EXPORT`), custodian, retention policy, encryption state, and status.

Persistent reproduction creates a ledger event: `CREATE_COPY|REPLICATE|CACHE|BACKUP|EXPORT|RESTORE|DESTROY_COPY`. Unregistered persistent copies are violations.

Retention requires explicit scope, purpose, deadline, and disposition. Conflicts surface as `DISPUTED_POLICY`; they are not silently resolved.

FORGET must locate known primary copies, replicas, caches, indexes, backups, and controllable exports; revoke access; destroy where controllable; invalidate descendants/indexes; and issue per-copy receipts.

Uncontrolled external copies remain `DESTRUCTION_CONFIRMED=FALSE`: `LOCAL FORGET != GLOBAL ERASURE`.

Backup restore must replay revocation ledger/tombstones before admission. Caches inherit source authority/retention. Searchable derived index material cannot preserve forgotten protected content.

`ENCRYPTED != FORGOTTEN`; key deletion is not proven byte destruction unless explicit cryptographic-erasure semantics are verified.

Core: **BACKUP RESTORE != REVOCATION ROLLBACK**.

`AUTHORITY_CREATED = FALSE`
