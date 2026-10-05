# CLASSIFICATION_RECEIPT_CHAIN_V0_1

Status: SCHEMA_ONLY  
Classification run: NOT_RUN  
Replay run: NOT_RUN  
Audit run: NOT_RUN  
Authority created: FALSE  
Canon: FALSE  
Join: FALSE  
Mutation: FALSE

## Purpose

Define an append-only receipt chain for classification work without creating or changing a classification.

The chain records computation history. It does not prove the world-state claim is true.

`HASH_VALID != EVENT_TRUE`  
`CHAIN_COMPLETE != CLASSIFICATION_TRUE`  
`REPLAY_MATCH != WORLD_STATE_TRUE`  
`AUDIT_VERIFIED != OBJECT_CLASS_TRUE`

## Ordering

1. `CLASSIFICATION_CORE_RECEIPT`
2. `REPLAY_RECEIPT`
3. `AUDIT_RECEIPT`
4. `CLASSIFICATION_RECEIPT_BUNDLE`

Later receipts bind earlier receipt hashes. Earlier receipts are never rewritten to add later pointers.

## CLASSIFICATION_CORE_RECEIPT

Minimum typed fields:

- `receipt_id`
- `object_address`
- `interval_id`
- `source_receipts[]`
- `burden_ladder_result`
- `collision_state`
- `classification_disposition`
- `ontology_version`
- `burden_rule_version`
- `class_rule_version`
- `collision_rule_version`
- `validator_version`
- `issued_at`
- `issuer_lane`
- `receipt_hash`

The hash is computed over the canonical receipt with `receipt_hash` omitted.

## REPLAY_RECEIPT

Binds:

- `classification_core_receipt_hash`
- same object and interval
- exact source receipt bytes or hashes
- ontology/rule/validator versions used for replay
- replay disposition
- replay result
- `receipt_hash`

Replay is recomputation, not reclassification.

## AUDIT_RECEIPT

Binds:

- `classification_core_receipt_hash`
- `replay_receipt_hash`
- audit rule version
- validator version
- audit checks and disposition
- `receipt_hash`

Audit is oversight, not a classification decision engine.

## CLASSIFICATION_RECEIPT_BUNDLE

Binds:

- `classification_core_receipt_hash`
- `replay_receipt_hash`
- `audit_receipt_hash`
- object address
- interval id
- bundle version
- `receipt_hash`

The bundle does not mutate any prior receipt.

## Hash Rule

Canonicalization: RFC 8785 JCS  
Encoding: UTF-8  
Digest: SHA-256  
Display: `sha256:` + lowercase hexadecimal digest

For each receipt:

1. Remove only its own `receipt_hash` field.
2. Canonicalize the remaining object with RFC 8785 JCS.
3. Encode as UTF-8.
4. SHA-256 the bytes.
5. Lowercase-hex encode the digest.
6. Prefix with `sha256:`.
7. Store as `receipt_hash`.

## Status Separation

Receipt validity and classification disposition are separate types.

Receipt status:
- `VALID`
- `INVALID`
- `INCOMPLETE`

Classification disposition may include:
- `CREATOR_COIN`
- `CONTENT_COIN`
- `UNASSIGNED`
- `COLLISION_CANDIDATE`
- `HOLD`

Missing required receipt input does not become a negative finding.

`MISSING_RECEIPT -> UNASSIGNED` applies on the classification rail.  
`MISSING_REPLAY_INPUT -> REPLAY = UNRUN`.  
`MISSING_AUDIT_INPUT -> AUDIT = UNRUN`.

## Collision Rule

A collision requires valid receipts for mutually exclusive class claims on the same object in the same interval.

If both valid:
`COLLISION_CANDIDATE -> HOLD -> NO MERGE -> NO CLASS LABEL`

If one claim is invalid, collision is cleared and the remaining claim returns to the classification burden gate. Invalidating one side does not validate the other.

## Persistence Rule

GitHub and Google Drive are recording rails, not authority rails.

A GitHub commit, Drive file, ENS name, wallet, signature, repository state, chat declaration, adapter output, price, liquidity, popularity, or market behavior cannot by itself establish the classification.

Persistence observations may point to repository commits or Drive file IDs after writing. They do not rewrite the canonical receipt that they record.

## Existing Repository Schema

This schema coexists with and does not replace:

`schemas/classification_receipt.v0_1.schema.json`

## State

`RECEIPT_INSTANCE = ABSENT` for an object classification.  
A separate schema-definition recording receipt may exist to prove that this schema was persisted.

`AUTHORITY_CREATED = FALSE`  
`CANON = FALSE`  
`JOIN = FALSE`
