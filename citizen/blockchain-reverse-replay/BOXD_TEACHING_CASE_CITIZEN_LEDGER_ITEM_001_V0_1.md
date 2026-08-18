# BoxD Teaching Case — CITIZEN_LEDGER_ITEM_001 v0.1

**Lane:** `AMERICAN_CITIZEN_PUBLIC_RECORD`  
**Primary audit home:** `jsonwisdom/COMPUTERWISDOM`  
**Parent PR:** `#493`  
**Parent stack PR:** `#481`  
**Family lane imported:** `FALSE`  
**Authority created:** `FALSE`

## Teaching objective

Demonstrate that a repository record, hash, UID, or apparently plausible blockchain claim does not become chain truth until an independent replay binds the corresponding chain object.

```text
REPOSITORY_RECORD != CHAIN_TRUTH
TX_HASH != FACT
UID_STRING != ATTESTATION
HASH != SEMANTIC_TRUTH
NEGATIVE_CHAIN_REPLAY != MOTIVE_PROOF
REJECTED_BASE_SEPOLIA_EDGE != GLOBAL_ABSENCE
```

## Original repository declaration

The COMPUTERWISDOM anchor topology declared the following Base Sepolia objects:

- transaction hash: `0x4cef493d67d8744d2458fd82c169aa872b14cfe2ecaf13f03329b57bd93acc35`
- EAS attestation UID: `0x23b3b97514fa232cfdbcdee7a5031ff11a5fcd36aa874a5f4067805cd0ad6c84`
- EAS schema UID: `0x244c84adef25091c97090e6e3f0b1bb932fc7022b913b7546406f4213a202cab`
- attester address: `0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5`

Initial normalization did not promote those values into independent chain truth.

## State-transition replay

```text
REPOSITORY CLAIM
        ↓
HOLD
        ↓
USER-SUPPLIED NEGATIVE RPC REPLAY
        ↓
CONFLICT
        ↓
OPTION B — DIRECT EAS UID RECOVERY
        ↓
EASSCAN / RPC / CONTRACT REPLAY
        ↓
DECODER ERROR DETECTED
        ↓
DECODER CORRECTED
        ↓
DIRECT REPLAY REPEATED
        ↓
CHILD REJECT
```

The earlier states remain part of the audit history. The final child disposition does not rewrite the parent entry.

```text
PARENT_HISTORICAL_STATE = CONFLICT_PRESERVED
CHILD_RECOVERY_STATE = REJECT_DECLARED_BASE_SEPOLIA_ANCHOR_OBJECTS
```

## Phase 1 — HOLD

The repository declared the values, but no independently bound transaction receipt, block, event decode, contract invocation, natural-person identity, invoice, payment source, government-money bridge, or legal-authority edge existed.

Disposition:

`HOLD_INDEPENDENT_CHAIN_REPLAY`

## Phase 2 — user-supplied negative replay → CONFLICT

On 2026-08-18, user-supplied RPC output reported `null` for both the transaction and transaction receipt on Base Sepolia, and also reported no matching transaction on Base mainnet.

The source was deliberately typed:

`USER_SUPPLIED_RPC_OUTPUT`

It was not mislabeled as assistant-independent verification.

Receipt:

`receipts/CITIZEN_LEDGER_ITEM_001_NEGATIVE_RPC_REPLAY_2026_08_18.json`

Disposition:

```text
REPOSITORY_ANCHOR_CLAIM = CONFLICT
TRANSACTION_EDGE = CONFLICT
INDEPENDENT_CHAIN_REPLAY = CONFLICT
REJECT_THRESHOLD = NOT_YET_MET
```

## Phase 3 — direct UID recovery

The recovery path intentionally did **not** replace the failed transaction hash.

```text
OPTION_A_HASH_CORRECTION = BLOCKED_NO_CORRECTED_HASH
OPTION_B_DIRECT_EAS_UID_REPLAY = ACTIVE
```

The declared attestation UID and schema UID became the lookup anchors.

Recovery record:

`EAS_UID_RECOVERY_REPLAY_V0_1.json`

## Phase 4 — first direct replay and decoder fault

The public-network recovery workflow queried Base Sepolia and the EAS surfaces. During direct contract replay, the first Solidity ABI decoder incorrectly interpreted the outer tuple offset as the returned UID.

That intermediate decode was **not promoted**.

```text
DECODER_OUTPUT != CHAIN_FACT
PARSER_BUG_DETECTED = TRUE
PROMOTION_BLOCKED = TRUE
```

The decoder was corrected and the exact direct calls were repeated.

This failed decode remains a teaching step because deterministic replay includes auditing the verifier itself.

## Phase 5 — corrected independent replay

Bound GitHub Actions replay:

- workflow: `EAS UID Recovery Replay v0.1`
- run: `32106944392`
- job: `95618197380`
- replay head: `141d4af42578d28586ddcadbf661efcc33c7c0c2`
- artifact: `9313480754`
- artifact SHA-256: `fdb0e6d5d28221ed21b2452b85803234b2e5507e8e39df30d879f4e75b96a8ff`
- Base Sepolia chain ID: `84532`

Observed after corrected decoding:

```text
eth_getTransactionByHash = null
eth_getTransactionReceipt = null
EASSCAN GraphQL attestation = null
EAS.getAttestation(uid) = ZERO ATTESTATION STRUCT
SchemaRegistry.getSchema(schemaUID) = ZERO SCHEMA RECORD
```

Bound receipt:

`receipts/CITIZEN_LEDGER_ITEM_001_EAS_UID_DIRECT_REPLAY_2026_08_18.json`

## Scoped disposition

```text
DECLARED_TRANSACTION_EDGE = REJECT
DECLARED_TRANSACTION_RECEIPT_EDGE = REJECT
DECLARED_ONCHAIN_ATTESTATION_EDGE = REJECT
DECLARED_SCHEMA_REGISTRATION_EDGE = REJECT
RECOVERY_TERMINAL = REJECT_DECLARED_BASE_SEPOLIA_ANCHOR_OBJECTS
CORRECTED_TRANSACTION_HASH = NOT_FOUND
```

The rejection is deliberately narrow.

It does **not** establish:

- motive;
- wrongdoing;
- who introduced the incorrect repository values;
- natural-person identity behind an address;
- absence on unrelated networks;
- absence from off-chain systems;
- governmental authority or governmental involvement.

## Parent / child rule

```text
FAILED_PARENT_CLAIM
!= DELETE_AND_REPLACE

FAILED_PARENT_CLAIM
→ PRESERVE_HISTORY
→ OPEN_CHILD_RECOVERY
→ REPLAY
→ APPEND_CHILD_DISPOSITION
```

Therefore:

```text
PARENT = CONFLICT_PRESERVED
CHILD = REJECT
```

This is not inconsistency. It is append-only evidence history.

## CI and stack boundary

At documentation freeze:

```text
COMPUTERWISDOM #493 = OPEN / DRAFT / UNMERGED
BASE = agent/jaytree-evidence-mechanics-v0-1
PARENT #481 = OPEN / DRAFT / UNMERGED / base master
ROUND_06_EXECUTIVE = READY_NOT_ROLLED
```

Green checks on `#493` validate the proposed stacked branch. They do not make the result canonical on `master` while `#481` remains unmerged.

```text
CI_GREEN != MERGED
STACK_GREEN != DEFAULT_BRANCH_CANONICAL
```

## Classroom replay questions

1. What did the repository claim?
2. What did the first independent source actually prove?
3. Why did HOLD become CONFLICT instead of immediately becoming REJECT?
4. Why was a replacement transaction hash not guessed?
5. Why did the UID become the next replay anchor?
6. What happened when the verifier itself decoded the contract response incorrectly?
7. What evidence justified the final child REJECT?
8. Why does the parent remain CONFLICT?
9. What claims remain outside the scope of the rejection?
10. What would be required to reopen the chain claim on another network or with a different bound object?

## Canonical teaching rule

```text
REPOSITORY CLAIM
    ↓
HOLD
    ↓
CONTRADICTORY REPLAY
    ↓
CONFLICT
    ↓
INDEPENDENT RECOVERY
    ↓
DECODER ERROR DETECTED
    ↓
CORRECTED REPLAY
    ↓
CHILD REJECT

PARENT HISTORY = PRESERVED
REJECT SCOPE = DECLARED BASE SEPOLIA OBJECTS ONLY
AUTHORITY_CREATED = FALSE
```
