# PURPOSEFUL WALLET SHELF — V0.1

STATUS = CANDIDATE
CANON = false
AUTHORITY_CREATED = false
FACTS_PROMOTED = 0
MERKLE_ROOT = NOT_BUILT
BRIDGE = HOLD
PNL_LICENSED = false
MAKEJAYMONEY_COINBASE_BASELINE = EXCLUDED

## Wallet shelf

### Slot 001 — Zora public
ADDRESS = 0x829AdfEdBe565F9885a7eA6Bc78912acAef055E2
CONTROL_PROOF_STATUS = PENDING
CONTROL_PROVEN = false
OWNERSHIP_DECLARED_BY_JASON = HUMAN_DECLARATION_ONLY

### Slot 002 — Base public anchor
ADDRESS = 0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8
CONTROL_PROOF_STATUS = ONE_MESSAGE_ERC1271

JOIN = NONE
MULTIPLE_WALLETS != COLLISION

## Leaf schema

LEAF_REQUIRED_FIELDS:
- chain_id
- tx_hash
- log_index
- block_number
- event_class
- quarter

QUARTER_TIMEZONE = UTC

EVENT_CLASSES:
- CREATOR_REWARD
- CONTENT_PAYOUT
- TRANSFER
- SWAP
- OTHER_INFLOW

A leaf is not replay-complete unless chain_id, tx_hash, log_index, block_number, event_class, and quarter are present.

## Fields

Merkle Story: the flat flywheel loop is the story so far. A forest needs one tree per wallet, quarter, and event class. No root until the leaf set is frozen.

Reason: keep creator rewards, content payouts, and other inflows from being told as one balance.

Function: admit a wallet, split fields, bind a receipt, replay the receipt. Function does not spend.

FullMath: count leaves and name gaps. Missing basis is not zero. No quarter dollar total.

Defensible: each claim points at a transaction plus chain id, tx hash, log index, and block number, or it stays on hold. A sender name is not an event decode.

Replayable: same transaction coordinates, same event class, same amount. Later decode does not erase an earlier hold.

Shareable: public summary only. No keys, no private connector payload, no human identity join.

## Transfer / sale boundary

TRANSFER != SALE
SALE_STATUS = UNBOUND_UNTIL_SWAP_EVENT_DECODED
"SOLD ~27.5M" = INTERPRETATION_ONLY
796.46_ZORA = OBSERVED_ONLY
796.46_ZORA_SUBJECT_BINDING = NONE

A transfer may be observed without proving a sale. Sale language requires the relevant swap event to be decoded and bound to the leaf.

## Super Secret Sister sidecar

CANONICAL_OBJECT = SUPER_SECRET_SISTER_SIDECAR
ALIAS = SuoerSecret
SIDECAR_ADDRESS = NONE
SIDECAR != WALLET
SIDECAR != ROOT
SIDECAR != AUTHORITY
SECRET_LABEL != PRIVACY
SISTER != FAMILY_SEAT
SISTER != CONSENT

Family and translation rail. It may carry a question. It may not move funds or mint a Merkle root.

## Holds preserved

0x829a_CONTROL = HOLD
MERKLE_ROOT = HOLD
BRIDGE = HOLD
PNL = HOLD

A later decode does not erase an earlier hold.
