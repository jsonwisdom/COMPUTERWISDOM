# JAYWISDOM B0 Index Partition Schedule v0.1.1

Date: `2026-08-19`
Status: `B0_SEALED / ACCOUNT_DEPLOYMENT_PROVEN / DENSE_FLOOR_BOUND`
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

## B0 exact anchor — PROVEN

Canonical machine-readable receipt:

`artifacts/JAYWISDOM_B0_ANCHOR.json`

User-supplied Base RPC receipt (`eth_getTransactionReceipt` + `eth_getBlockByNumber`) establishes:

```text
B0_ACCOUNT_DEPLOYMENT_TX = 0x7239f942d4818821f88d24c63140ba0aaae1e096036d746e007b2f6f0c3789e6
B0_ACCOUNT_DEPLOYMENT_BLOCK_HEX = 0x183afe0
B0_ACCOUNT_DEPLOYMENT_BLOCK = 25,407,456
B0_ACCOUNT_DEPLOYMENT_BLOCK_HASH = 0x4686285c9bd01010b52fe9748693898e6ed50193f9743abe44f653ddffa22e81
B0_ACCOUNT_DEPLOYMENT_TIMESTAMP_UNIX = 1737604259
B0_ACCOUNT_DEPLOYMENT_TIMESTAMP_UTC = 2025-01-23T03:50:59Z
B0_TX_FROM = 0x8611d9722ec5089f974eb48a7b5ccdb97e8978fb
B0_TX_TO = 0x0ba958a449701907302e28f5955fa9d16ddc45c3
B0_TX_STATUS = 0x1 / SUCCESS
B0_GAS_USED = 0x442ce
B0_PROXY_ADDRESS = 0x829AdfEdBe565F9885a7eA6Bc78912acAef055E2
B0_ACCOUNT_DEPLOYMENT_STATE = PROVEN
```

This flips the prior exact-fetch hold:

```text
B0_ACCOUNT_DEPLOYMENT_TX: BOUND_POINTER -> PROVEN
B0_ACCOUNT_DEPLOYMENT_BLOCK: HOLD_EXACT_FETCH -> PROVEN / 25,407,456
B0_ACCOUNT_DEPLOYMENT_TIMESTAMP: HOLD_EXACT_FETCH -> PROVEN / 2025-01-23T03:50:59Z
```

Provenance boundary:

```text
PRIMARY_RECEIPT = user-supplied Base RPC result
PUBLIC_POINTER = BaseScan transaction hash already independently observed
BROWSER_EXACT_BLOCK_TIMESTAMP_CROSSCHECK = NOT_COMPLETED_IN_THIS_REPLAY
```

The RPC receipt is the promoted primary receipt for this v0.1.1 delta. The public-browser cross-check remains a distinct witness class and is not silently claimed.

## First relevant activity / dense floor

The previously supplied explorer-window observation remains independently typed:

```text
B0_FIRST_RELEVANT_ACTIVITY_CANDIDATE ~= 29,889,702
B0_FIRST_RELEVANT_ACTIVITY_STATE = CANDIDATE / NEEDS_COMPLETE_MIN_ACROSS_EVENT_CLASSES
B0_DENSE_SCAN_FLOOR = 29,800,000
B0_DENSE_SCAN_FLOOR_STATE = LOCKED_WORK_FLOOR
```

The exact account deployment at block 25,407,456 is earlier than the dense floor. This is expected and does not require moving the dense floor. The sparse completeness backstop covers the interval before dense indexing.

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

The interval `25,407,456 -> 29,799,999` is now an explicit sparse-backfill region. Any matching rows found there are appended as PROVEN / BOUND / HOLD / CONFLICT according to their receipts; they do not retroactively alter B0.

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

## Current promotion state

```text
B0_ACCOUNT_DEPLOYMENT = PROVEN
B0_ACCOUNT_DEPLOYMENT_BLOCK = 25,407,456
B0_ACCOUNT_DEPLOYMENT_TIMESTAMP = 2025-01-23T03:50:59Z
B0_FIRST_RELEVANT_ACTIVITY_CANDIDATE = ~29,889,702 / NOT YET PROMOTED
B0_DENSE_SCAN_FLOOR = 29,800,000 / LOCKED
DENSE_SCANNER_EXECUTION = NOT_CLAIMED_BY_THIS_ARTIFACT
BACKGROUND_EXECUTION = NOT_CLAIMED
```

## Doctrine

```text
ACCOUNT DEPLOYMENT != FIRST FUNDING
ACCOUNT DEPLOYMENT != DENSE FLOOR
FIRST REGULAR TX != FIRST LOG
DENSE FLOOR != CHAIN BIRTH
BLOCK CO-OCCURRENCE != RELATIONSHIP
SNAPSHOT != CURRENT STATE
USER-SUPPLIED RPC RECEIPT != INDEPENDENT BROWSER FETCH
MISSING HISTORICAL READBACK -> HOLD
```
