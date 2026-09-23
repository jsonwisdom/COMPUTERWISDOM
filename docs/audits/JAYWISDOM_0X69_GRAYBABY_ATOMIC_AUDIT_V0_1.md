# JAYWISDOM 0x69 — Gray Baby Atomic Audit v0.1

Date: `2026-08-19`  
Status: `CROSS_SURFACE_BOUND_DRAFT`  
Audit mode: `OBSERVE -> RECEIPT -> VERIFY -> AUTHORITY -> REPLAY -> HOLD / PROVEN`  
Authority created: `FALSE`  
Financial claim created: `FALSE`

Drive mirror: https://docs.google.com/document/d/1XTdWUiPSvWjUdHI39AS8C_XVJQAHRC9zKDDO0fb1tog/edit

## Root object

```text
NETWORK = Base
TOKEN_CONTRACT = 0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F
NAME = jaywisdom
SYMBOL = jaywisdom
STANDARD = ERC-20 CreatorCoin minimal proxy
DECIMALS = 18
MAX_TOTAL_SUPPLY_DISPLAYED = 1,000,000,000
CREATION_TX = 0x49c29d9b305a297c6a754f068fbf8ec4921e5e038b3c037757d99635da477a10
CREATION_BLOCK = 31825577
CREATION_TIMESTAMP = 2025-06-20T17:28:21Z
CREATION_STATUS = SUCCESS
FACTORY = 0x777777751622c0d3258f214F9DF38E35BF45baF3 (ZoraFactory)
CREATORCOIN_VERSION = 1.1.0
METADATA_URI = ipfs://bafybeibdshmigqm56zayjuhgyiniatzpexmamgoxhfeadhjujmvjspbksa
```

Primary chain sources:
- https://basescan.org/token/0x694ce46c64d9d1a5e9376a9febcf85ec05d72e9f
- https://basescan.org/tx/0x49c29d9b305a297c6a754f068fbf8ec4921e5e038b3c037757d99635da477a10

## 0x829a role correction

Address: `0x829AdfEdBe565F9885a7eA6Bc78912acAef055E2`

| Relationship | State |
|---|---|
| `CreatorCoinCreated.caller` | `PROVEN` |
| `CreatorCoinCreated.payoutRecipient` | `PROVEN` |
| initial `OwnerUpdated.newOwner` | `PROVEN` |
| `CoinPayoutRecipientUpdated.newRecipient` | `PROVEN` |
| later `CreatorCoinRewards.creator` | `PROVEN` |
| GitHub public-index role: Zora wallet pointer | `REPO_BOUND` |
| creation-time `platformReferrer` | `FALSE` — event value is zero address |
| generic/user label `referrer` | `HOLD_ROLE_AMBIGUITY` until a specific referral/trade receipt binds it |

**Correction:** do not serialize `0x829a...` as the creation-time platform referrer. The chain event proves caller + payout recipient, and later creator-reward role.

## Initial ownership

Creation transaction emits owner additions for:

```text
0x829AdfEdBe565F9885a7eA6Bc78912acAef055E2
0xb3B9CC668e997209e914309FF525535203EaD4dA
0xd88A5b3622cc1708eb8E8F5c57744DFfb0B93db1
```

`0xd88A...` is publicly labeled `computerwisdom.base.eth` on BaseScan.

```text
INITIAL_OWNER_SET = PROVEN
CURRENT_OWNER_SET = HOLD_CURRENT_READBACK
```

Initialization events do not prove that no later ownership mutations occurred.

## Account-abstraction deployment path

The outer transaction is an ERC-4337 bundle:

```text
Pimlico ERC-4337 Bundler 56
  -> Entry Point 0.6.0
    -> ZoraFactory CREATE2
      -> JAYWISDOM CreatorCoin
```

Boundary:

```text
BUNDLER != CREATOR
OUTER_TX_FROM != APPLICATION_CALLER
```

The `CreatorCoinCreated` event is the authoritative receipt for the application caller/payout relationship.

The same outer bundle also created a separate coin, `Brielle’s beauty ritual`. This establishes **bundle co-occurrence only**. It does not prove shared creator, ownership, purpose, or project identity.

## Uniswap v4 relationship

```text
POOL_MANAGER = 0x498581fF718922c3f8e6A244956aF099B2652b2b
POOL_ID = 0xC3107E6D53CC9FA38C90A58F307094E754CCC6E7653411308C8CEB5ACE8E57FA
CURRENCY_0 = 0x1111111111166b7FE7bd91427724B487980aFc69 ($ZORA)
CURRENCY_1 = 0x694cE46C64D9D1a5e9376A9feBcF85Ec05D72e9F (jaywisdom)
FEE_PIPS = 30000
FEE = 3.00%
TICK_SPACING = 200
HOOK = 0xffF800B76768dA8AB6aab527021e4a6A91219040
POOL_INITIALIZED = PROVEN
INITIAL_LIQUIDITY_EVENT = PROVEN
CURRENT_LIQUIDITY = HOLD_DYNAMIC_READBACK
```

Uniswap v4 uses a PoolManager singleton: pools are uniquely identified by `PoolKey` / `PoolId`, not separate pool contract addresses. The historical requirement to find a separate pool address is therefore superseded by a schema correction.

Primary protocol references:
- https://developers.uniswap.org/docs/protocols/v4/concepts/poolmanager
- https://developers.uniswap.org/docs/protocols/v4/guides/create-pool
- https://developers.uniswap.org/docs/protocols/v4/deployments
- https://support.zora.co/en/articles/5654721

## Initial supply flow observed

```text
Null -> JAYWISDOM token
  1,000,000,000 jaywisdom

JAYWISDOM token -> 0xffF800... hook
  500,000,000 jaywisdom

0xffF800... hook -> Uniswap v4 PoolManager
  499,999,999.999999999999999999 jaywisdom
```

This proves initialization transfers. It does **not** prove present balances, present liquidity, price, market value, or investment performance.

## GitHub reverse replay

Historical source: `jsonwisdom/JOY/artifacts/L2_JAYWISDOM_TOKEN_IDENTITY_CORRECTION_V0_1.json`

That receipt correctly treated `0x694c...` as a reported token contract rather than a pool, then requested independent explorer evidence. This audit closes several of those gates:

```text
TOKEN_IDENTITY: REPORTED -> PROVEN_ONCHAIN
TOKEN_CREATION: NOT_INDEPENDENTLY_REPLAYED -> PROVEN_ONCHAIN
POOL: UNCONFIRMED -> POOL_ID_PROVEN
INITIAL_LIQUIDITY: UNCONFIRMED -> PROVEN_ONCHAIN
CURRENT_LIQUIDITY: HOLD_DYNAMIC
```

Historical source: `jsonwisdom/JOY/artifacts/L0_JAY_ATOMIC_REPUTATION_RECEIPT_V0_1.json`

Its historical `REPORTED / NOT_PROVEN / UNCONFIRMED` states remain preserved in-place and are superseded by this stronger direct-chain replay rather than rewritten.

### Portal metadata membrane

`jsonwisdom/jay-zora-portal/frontend/public/zora-index.json` currently maps this contract to `GIRTH`, `token_id: 1`, and tx hash `0xdbb81126...`.

Classification:

```text
PORTAL_INDEX_ENTRY = OBSERVED
TOKEN_ID_1_ONCHAIN = HOLD
PORTAL_TX_HASH = HOLD_INDEPENDENT_CHAIN_REPLAY
```

This root object is an ERC-20 CreatorCoin. A portal `token_id` field is interface/index metadata unless a separate onchain object proves token-ID semantics.

## Gray Baby relationship

Gray Baby receipt standard PR #509 records a **different** user-confirmed Base address:

`0x0bd63fe9e476bae76a334dfb94d6f3d31d49a076`

PR #509 keeps independent explorer verification pending for that address.

Therefore:

```text
JAYWISDOM_TOKEN == GRAYBABY_TOKEN = FALSE
GRAYBABY_RELATION = AUDITOR / WITNESS METHOD
DIRECT_ECONOMIC_RELATION = NOT_PROVEN
DIRECT_CONTRACT_RELATION = NOT_PROVEN
```

Gray Baby is the audit membrane here, not silently a token relationship.

## Drive replay

Exact Drive searches for the JAYWISDOM token address and `0x829a...` returned no pre-existing object in this replay. The Drive mirror linked above is the new dedicated audit witness.

## OpenAI Platform replay

Visible target topology during replay:
- Computer Wisdom / Default project
- Computer Wisdom / Default project
- Personal / Default project

```text
PLATFORM_ROLE = ACCESS / TOPOLOGY CONTEXT ONLY
ONCHAIN_PROOF_WEIGHT = 0
API_KEY_CREATED_BY_THIS_REPLAY = FALSE
```

## Atomic state

```text
TOKEN_CONTRACT = PROVEN
CREATORCOIN_TYPE = PROVEN
CREATION_TX = PROVEN
ZORA_FACTORY_DEPLOYMENT = PROVEN
0x829_CALLER = PROVEN
0x829_PAYOUT_RECIPIENT = PROVEN
0x829_CREATOR_REWARD_ROLE = PROVEN
0x829_PLATFORM_REFERRER_AT_CREATION = FALSE
INITIAL_OWNER_SET = PROVEN
CURRENT_OWNER_SET = HOLD
UNISWAP_V4_POOL_ID = PROVEN
INITIAL_LIQUIDITY = PROVEN
CURRENT_LIQUIDITY = HOLD
GRAYBABY_AUDIT_RELATION = BOUND_METHOD
GRAYBABY_TOKEN_RELATION = SEPARATE
AUTHORITY = FALSE
```

## Doctrine

```text
CHAIN EVENT > REPO LABEL > USER LABEL
BUNDLER != CREATOR
POOL ID != TOKEN CONTRACT
PUBLIC INDEX != CHAIN FACT
SAME TRANSACTION != SAME OWNER
TOKEN != AUTHORITY
MISSING CURRENT READBACK -> HOLD
```
