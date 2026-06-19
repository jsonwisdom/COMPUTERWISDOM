# ZFD-GOBLIN-ACQ-LAYER-V0_1

Author: jaywisdom  
Scope: Zora Creator Coins for zora.co/@jaywisdom and descendants  
Authority: false  
Membrane: HOLDS  

## Purpose

Create a replay-safe acquisition layer for Zora Creator Coins using direct RPC, block-number binding, transaction receipt binding, metadata resolution, and hash verification.

## Acquisition Class

- acquisition_class: DIRECT_RPC
- chain_id: 8453
- chain_source: canonical RPC
- replay requirement: block_number + tx_hash mandatory

## Metadata Resolution Order

1. contractURI()
2. tokenURI(0)
3. uri(0)

No ERC-721 or ERC-1155 assumption is allowed. Only observed behavior may be recorded.

## Gateway Policy

- Direct HTTP(S) preferred
- ipfs:// must store raw URI
- gateway-resolved URL must be logged
- gateway_class must be DIRECT or MIRROR_GATEWAY
- no black-box mirrors

## Symbol Index Rule

No orphan goblins.

Every card symbol must map to a contract.
Every contract must map back to canon.

## Proof-007 Replay Chain

Required bundle:

- metadata_snapshot
- tx_receipt
- replay_instructions
- metadata_hash
- block_number
- block_timestamp

## Core Invariant

Claim to canon requires replayable evidence.

Authority remains false.
