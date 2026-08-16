# PMEM-IMPL-005 — Integrity + Trust Anchor Contract

Depends on: `001..004`

`HASH(x) != TRUTH(x)` and `HASH(x) != AUTHORITY(x)`.

Anything hashed must first be transformed into deterministic canonical bytes with declared serialization format/version, encoding, normalization rules, and hash algorithm.

`CID(x)=SHA256(CANONICAL(x))` from actual bytes. Receipt hashes exclude the `receipt_hash` field itself.

Ledger events chain `previous_receipt_hash`; edits, reorder, insertion, and deletion become detectable as hash/sequence/chain failures.

Checkpoints commit to ledger prefixes but are not external trust anchors by default. External anchor states are distinct: `REQUESTED`, `SUBMITTED`, `CONFIRMED`; CONFIRMED requires independently retrievable proof.

`SIGNATURE != IDENTITY` without a separately established binding, and `IDENTITY != AUTHORITY`.

Verification states: `UNVERIFIED | VERIFIED_LOCAL | VERIFIED_EXTERNAL | FAILED`. Missing canonical bytes means `HASH_RECOMPUTED=FALSE` and `INTEGRITY_VERIFIED=FALSE`.

After FORGET, a surviving digest is not retained content: `DIGEST != CONTENT`.

No aggregate PASS may hide failed subchecks. Cryptographic inconsistency sets `INTEGRITY=FAILED` and forbids silent repair.

Core: **NO CRYPTOGRAPHIC CLAIM WITHOUT BYTE-LEVEL VERIFICATION**.

`AUTHORITY_CREATED = FALSE`
