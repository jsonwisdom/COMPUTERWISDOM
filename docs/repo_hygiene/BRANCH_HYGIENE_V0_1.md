# Branch Hygiene V0.1

Status: ACTIVE  
Authority: false

## Rule

All new protocol, packet, anchor, archive, verifier, and replay branches must be created from current `master`.

Do not create new protocol branches from stale feature branches.

## Reason

Stale feature branches can resurrect placeholder evidence fields, including:

- `PENDING_MERGE`
- `PENDING_PR`
- empty `base_transaction`
- empty `eas_uid`
- empty `archive_uri`
- outdated `MAINTAIN` classifications

## Required Practice

Before creating a new branch:

1. Fetch current `master`.
2. Confirm the packet state on `master`.
3. Create the new branch from `master` only.
4. Apply one focused change.
5. Open a PR.
6. Delete stale branches after merge or closure.

## Leaf 002 Incident

The Leaf 002 archive-CID update conflicted because an old feature branch contained an obsolete packet state.

The stale packet had placeholder fields and `MAINTAIN` classification.

Corrective rule:

Never branch from `feature/proof-president-002-*`.

Always branch from current `master`.

Authority remains false.
