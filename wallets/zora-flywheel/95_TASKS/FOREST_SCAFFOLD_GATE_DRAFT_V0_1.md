# GATE AFTER LEAF REPLAY — FOREST SCAFFOLD — DRAFT

STATUS = DRAFT
PARENT_GATE = LEAF_REPLAY_COMPLETION_GATE_DRAFT_V0_1
PARENT_RUN = false
THIS_RUN = false
PROMOTION = false

## Opens only if

The leaf gate has been run, and each in-scope receipt is either LEAF_COMPLETE or LEAF_INCOMPLETE. Incomplete leaves are listed. They are not dropped.

## Purpose

Freeze the completed leaf set and scaffold one tree per wallet slot, UTC quarter, and event class. Do not compute a Merkle root in this gate.

## Pass rule

A tree scaffold exists only when:

- slot is named
- quarter is UTC
- event_class is one of CREATOR_REWARD, CONTENT_PAYOUT, TRANSFER, SWAP, OTHER_INFLOW
- every leaf in that tree has chain_id, tx_hash, log_index, block_number
- leaf order is declared and stable
- incomplete leaves are in a side list, not in the tree

MERKLE_ROOT = NOT_COMPUTED until a later gate freezes that ordered leaf set.

## Forbidden

No sum. No USD. No cost basis. No sale label without a decoded swap log. No join of 0x829a and 0xA380. No control promotion. No Coinbase import. No Sister answer. No encryption claim. No DEX object.

FACTS_PROMOTED = 0
AUTHORITY_CREATED = false
PNL = HOLD
