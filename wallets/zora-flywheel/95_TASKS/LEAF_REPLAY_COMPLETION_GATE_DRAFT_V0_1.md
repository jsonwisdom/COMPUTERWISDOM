# NEXT TECHNICAL GATE — LEAF REPLAY COMPLETION — DRAFT

STATUS = DRAFT
RUN = false
PROMOTION = false
PNL_LICENSED = false

## Purpose

Replay-complete existing economic leaves from source transaction and log coordinates. Do not promote their economic interpretation.

## Pass rule

A leaf is replay-complete only when all are present:

- chain_id = 8453
- tx_hash
- log_index
- block_number
- event_class
- quarter, timezone UTC

Missing any field => LEAF_INCOMPLETE, not a root input.

## Event classes

CREATOR_REWARD, CONTENT_PAYOUT, TRANSFER, SWAP, OTHER_INFLOW.

TRANSFER != SALE. Do not retitle a transfer as SWAP or SALE unless that event is decoded on the cited log.

## Scope

Existing receipts under wallets/zora-flywheel/10_ADD/ and the unread October 4 listed row. One leaf per receipt. Do not sum. Do not collapse CreatorCoinRewards with CoinMarketRewardsV4.

October 4 row 6030952547106756 from 0x0469a4Bd3724DC86C9542F4694c976DA13C450c0 stays INPUT_GAP until a log page contains it.

## Procedure

1. Read the existing receipt. Do not edit it in place.
2. Fetch the transaction logs. Record the page index used.
3. Match amount, emitter, and event name to one log.
4. Append a leaf file with the six required fields plus source URL.
5. If the log page does not contain the match, write LEAF_INCOMPLETE and keep the prior receipt.

## Forbidden

No Merkle root. No USD. No cost basis inference. No wallet join. No control promotion. No Coinbase import. No Sister answer.

FACTS_PROMOTED = 0
AUTHORITY_CREATED = false
