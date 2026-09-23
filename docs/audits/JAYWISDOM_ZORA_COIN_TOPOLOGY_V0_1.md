# JAYWISDOM — Zora Coin Topology v0.1

Date: `2026-08-19`  
Parent audit: `JAYWISDOM_0X69_GRAYBABY_ATOMIC_AUDIT_V0_1` / PR `#511`  
Status: `REPO_SNAPSHOT_BOUND / CURRENT_INVENTORY_HOLD`  
Authority created: `FALSE`

## Purpose

Keep Jay Wisdom's Zora coin surface inside the atomic identity replay without collapsing distinct coin contracts, profile identity, wallets, or platform referral roles into one object.

## Root topology

```text
JAY WISDOM / JSONWISDOM
  |
  +-- Zora profile: @jaywisdom
  |     |
  |     +-- profile Creator Coin
  |     |     `-- 0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F
  |     |
  |     `-- created Content Coins[]
  |           +-- independent ERC-20/post coin contract
  |           +-- independent metadata/IPFS object
  |           +-- independent creator/payout/referrer fields
  |           +-- independent market/pool relationship
  |           `-- independent receipt state
  |
  +-- creator/payout address seen in snapshot
  |     `-- 0x829AdfEdBe565F9885a7eA6Bc78912acAef055E2
  |
  +-- GitHub index/mirror
  |     `-- jsonwisdom/jay-zora-portal
  |
  `-- Base chain receipts
        `-- each coin must replay independently
```

## Repository snapshot

Source: `jsonwisdom/jay-zora-portal/discovery/zora/latest_profile_coins_response.json`

Observed snapshot fields:

```text
PROFILE_HANDLE = jaywisdom
PROFILE_CREATOR_COIN = 0x694ce46c64d9d1a5e9376a9febcf85ec05d72e9f
CREATED_COINS_COUNT_SNAPSHOT = 923
CREATED_COINS_COUNT_CURRENT = HOLD_DYNAMIC_READBACK
```

The count of `923` is a repository-captured Zora API/GraphQL snapshot. It must not be promoted to a present-time inventory count without a new live readback.

## Sample content-coin relationship from the snapshot

```text
CONTENT_COIN = 0xc178f471cb74bf026809bf5632d3c9abc5a1fae7
COIN_TYPE = CONTENT
CHAIN_ID = 8453 / Base
TOTAL_SUPPLY_SNAPSHOT = 1,000,000,000
CREATOR_ADDRESS = 0x829adfedbe565f9885a7ea6bc78912acaef055e2
PAYOUT_RECIPIENT = 0x829adfedbe565f9885a7ea6bc78912acaef055e2
PLATFORM_REFERRER = 0x7bf90111ad7c22bec9e9dff8a01a44713cc1b1b6
POOL_CURRENCY_SNAPSHOT = WETH / 0x4200000000000000000000000000000000000006
```

This proves why `referrer` cannot be treated as one identity-wide role. Referral fields are coin/event specific. For this sampled content coin, the snapshot records a nonzero platform referrer that is different from `0x829a...`. For the JAYWISDOM Creator Coin creation receipt, creation-time `platformReferrer` was the zero address.

## Coin classes must remain distinct

```text
CREATOR_COIN != CONTENT_COIN
PROFILE != WALLET
WALLET != COIN
COIN_A != COIN_B
PLATFORM_REFERRER_A != GLOBAL_REFERRER
METADATA != CURRENT_CHAIN_STATE
REPO_SNAPSHOT != LIVE_INVENTORY
```

## Zora platform relationship

Current Zora architecture treats profiles and posts as tradable coins. Zora's public documentation states that each post is a coin with a one-billion supply, and profile Creator Coins are separately represented. The public platform also describes the broader relationship among post coins, Creator Coins, and `$ZORA`.

This architecture description is platform context; it does not prove any particular Jay coin's current balance, holders, liquidity, price, rewards, or ownership.

## Atomic checkpoint schema

Each Zora coin should replay as:

```yaml
coin_address: string
coin_class: CREATOR | CONTENT | OTHER
chain_id: 8453
creator_address: string | HOLD
payout_recipient: string | HOLD
platform_referrer: string | ZERO | HOLD
metadata_uri: string | HOLD
creation_tx: string | HOLD
creation_block: integer | HOLD
pool_or_pool_id: string | HOLD
current_owner_or_admin: HOLD | value
current_liquidity: HOLD | value
current_holders: HOLD | value
repo_snapshot_state: OBSERVED | BOUND
chain_state: PROVEN | BOUND | HOLD | CONFLICT
```

## Relationship to Gray Baby

Gray Baby remains the witness/replay method. It does not make every Zora coin a Gray Baby object and does not infer economic linkage between separate contracts.

```text
GRAYBABY_METHOD -> AUDITS EACH COIN
GRAYBABY_TOKEN != JAYWISDOM_CREATOR_COIN
GRAYBABY_TOKEN != ALL_CONTENT_COINS
```

## One story, multiple checkpoints

```text
JAY WISDOM
  -> identity labels
  -> ENS / Basename checkpoints
  -> wallets
  -> Zora profile
  -> Creator Coin
  -> Content Coins[]
  -> Base transactions / pools
  -> GitHub receipts
  -> Drive mirrors
  -> Farcaster/X publication witnesses
  -> OpenAI Platform topology context
  -> GrayBabyWitness replay
```

The story may be singular. The evidence remains atomic.
