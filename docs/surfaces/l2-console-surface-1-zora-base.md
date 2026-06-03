# L2 Console Surface 1: Zora Base Replay Spine

Status: OBSERVE_AND_RECEIPT_ONLY
Authority: false
Membrane: HOLDS

## Purpose

Define Surface 1 for live external observation of a Zora ContentCoin on Base.

Contract:
0x17c7f908a0cbd2d415c44fb4098f229878e3ea7c

Chain:
Base, chain id 8453

Relationship to COMPUTERWISDOM replay spine:
UNVERIFIED_EXTERNAL_OBSERVATION

## Surfaces

### Zora Native

Primary coin surface:
https://zora.co/coin/base:0x17c7f908a0cbd2d415c44fb4098f229878e3ea7c

Observed fields:
- coin_exists
- name
- symbol
- creatorAddress
- createdAt
- tokenPrice
- marketCap
- volume24h
- uniqueHolders
- rewards if visible

### DexScreener

Token pairs endpoint:
https://api.dexscreener.com/token-pairs/v1/base/0x17c7f908a0cbd2d415c44fb4098f229878e3ea7c

Token endpoint:
https://api.dexscreener.com/tokens/v1/base/0x17c7f908a0cbd2d415c44fb4098f229878e3ea7c

Observed fields:
- pairs_found
- dexId
- pairAddress
- priceNative
- priceUsd
- liquidity
- volume
- fdv
- marketCap
- pairCreatedAt

### BaseScan

Chain proof surface:
https://basescan.org/address/0x17c7f908a0cbd2d415c44fb4098f229878e3ea7c

Observed fields:
- contract_exists
- deployer
- creation_tx
- transfers
- holders when indexed

## Rules

- No ownership claim.
- No trading advice.
- No on-chain action.
- No authority upgrade.
- Do not connect this token to PR 165 or Jay identity without deployer, metadata, timestamp, and source receipts.

Final line: External surfaces are observed, not absorbed.
