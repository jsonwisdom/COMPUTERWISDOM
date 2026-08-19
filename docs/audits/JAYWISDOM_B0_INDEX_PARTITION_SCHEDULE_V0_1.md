# JAYWISDOM B0 Index Partition Schedule v0.1

Date: `2026-08-19`
Status: `B0_DENSE_FLOOR_BOUND / ACCOUNT_BIRTH_EXACT_BLOCK_HOLD`
Authority created: `FALSE`
Financial claim created: `FALSE`

## Canonical spine

```text
PRIMARY_TARGET = 0x829AdfEdBe565F9885a7eA6Bc78912acAef055E2
JAYWISDOM_TOKEN = 0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F
JAYWISDOM_BASE_OPERATIONAL = 0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8
NETWORK = Base / chainId 8453
```

## B0 typing

Do not collapse these states:

```text
B0_ACCOUNT_DEPLOYMENT = exact CoinbaseSmartWallet proxy creation block
B0_FIRST_RELEVANT_ACTIVITY = earliest transaction/log/transfer involving the audit spine
B0_DENSE_SCAN_FLOOR = conservative block floor for dense historical indexing
```

User-supplied Phase 0 observation:

```text
B0_FIRST_RELEVANT_ACTIVITY_CANDIDATE ~= 29,889,702
B0_DENSE_SCAN_FLOOR = 29,800,000
```

Current BaseScan observation independently confirms `0x829a...` is a CoinbaseSmartWallet proxy contract and exposes a contract-creation receipt. The creation receipt transaction hash observed from BaseScan navigation is:

```text
0x7239f942d4818821f88d24c63140ba0aaae1e096036d746e007b2f6f0c3789e6
```

The exact creation block/timestamp was not returned by the independent browser fetch in this replay. Therefore:

```text
B0_ACCOUNT_DEPLOYMENT_TX = BOUND_POINTER
B0_ACCOUNT_DEPLOYMENT_BLOCK = HOLD_EXACT_FETCH
B0_ACCOUNT_DEPLOYMENT_TIMESTAMP = HOLD_EXACT_FETCH
B0_FIRST_RELEVANT_ACTIVITY_CANDIDATE = USER_SUPPLIED / NEEDS_RPC_OR_EXPORT_MIN
B0_DENSE_SCAN_FLOOR = 29,800,000 / ACCEPTED_CONSERVATIVE_WORK_FLOOR
```

BaseScan also reports 31 regular transactions in its current address snapshot; visible regular rows extend at least to July 22, 2025. Regular transaction history is not a complete substitute for contract creation, internal calls, token transfers, or logs.

Primary public explorer pointers:
- https://basescan.org/address/0x829adfedbe565f9885a7ea6bc78912acaef055e2
- https://basescan.org/address/0x694ce46c64d9d1a5e9376a9febcf85ec05d72e9f

## Partition schedule

### Dense historical pass

```text
START_BLOCK = 29,800,000
FETCH_WINDOW_BLOCKS = 5,000
WINDOW_KEY = base:<fromBlock>-<toBlock>
ORDER = ascending blockNumber, transactionIndex, logIndex
END = observed HEAD at execution time
```

Each 5,000-block window is immutable after receipt generation. Re-fetches create a version delta; they do not overwrite prior receipts.

### Fortnight checkpoint layer

Fortnight checkpoints are defined by UTC timestamps rather than an assumed fixed block count:

```text
EPOCH = [00:00:00Z day_0, 00:00:00Z day_14)
ROOT = Merkle(events ordered by blockNumber, txIndex, logIndex, rail)
STORE = local SQLite + exported receipt
```

The ingest process resolves the first and last Base block actually falling inside each 14-day timestamp interval. Do not approximate a fortnight as a fixed number of blocks in the canonical receipt.

### Sparse completeness backstop

Run a lightweight Base-genesis-to-HEAD filter for only the canonical addresses and known protocol topics. Its purpose is to catch any event before the dense floor without scanning every transaction.

```text
ADDRESSES:
- 0x829AdfEdBe565F9885a7eA6Bc78912acAef055E2
- 0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F
- 0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8

PROTOCOL FAMILIES:
- Coinbase Smart Wallet deployment / ownership
- ERC-20 Transfer / Approval
- ZoraFactory / CreatorCoin
- Zora payout / creator rewards / referrer
- Uniswap v4 PoolManager / Initialize / ModifyLiquidity / Swap
- EAS attestation / schema events
- ENS / Basename identity-resolution checkpoints where historically resolvable
```

## Four-rail merger

```text
RAIL_1_BASE = transactions + internal calls + logs + transfers
RAIL_2_ZORA = profile + CreatorCoin + content coins + payouts + metadata/IPFS
RAIL_3_EAS = schema + attestation events tied to known addresses/UIDs
RAIL_4_IDENTITY = ENS/Basename resolution checkpoints

MERGE_KEY_PRIMARY = (chainId, blockNumber, txHash, logIndex, rail)
LEFT_JOIN_STORY_KEY = (blockNumber, txHash)
```

Never force two records into one relationship merely because they share a block or transaction.

## Gray Baby state stamping

Each merged row receives:

```text
PROVEN = direct primary receipt establishes the bounded event
BOUND = cross-surface pointer is receipt-linked but broader claim excluded
HOLD = missing dynamic/historical readback
CONFLICT = witnesses materially disagree
```

`HOLD` rows form the retro-signing / evidence-acquisition queue. A later receipt appends a state delta; historical rows remain preserved.

## Checkpoint object

```yaml
epoch_id: string
start_timestamp_utc: string
end_timestamp_utc: string
first_block: integer
last_block: integer
rows_by_rail: {}
merkle_root: string
source_receipts: []
holds: []
conflicts: []
created_at: string
```

## Promotion condition

The exact first relevant block is promoted only after a complete RPC/indexed-provider result or explorer export supports `MIN(blockNumber)` across the relevant event classes. Until then, `29,800,000` is the dense work floor—not a claim of wallet birth.

## Doctrine

```text
ACCOUNT DEPLOYMENT != FIRST FUNDING
FIRST REGULAR TX != FIRST LOG
DENSE FLOOR != CHAIN BIRTH
BLOCK CO-OCCURRENCE != RELATIONSHIP
SNAPSHOT != CURRENT STATE
MISSING HISTORICAL READBACK -> HOLD
```
