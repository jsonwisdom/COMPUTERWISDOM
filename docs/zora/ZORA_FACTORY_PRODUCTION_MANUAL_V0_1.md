# ZORA_FACTORY_PRODUCTION_MANUAL_V0_1

Author: jaywisdom  
Scope: Zora Creator Coin factory operations for zora.co/@jaywisdom and descendants  
Status: Draft production manual  
Authority: false  
Membrane: HOLDS  

## 0. Purpose

This manual defines the safe production path for creating, acquiring, indexing, and replaying Zora Creator Coin artifacts without silent promotion from claim to receipt.

It is a factory manual, not a financial recommendation, not a trading strategy, and not a claim that any coin has value.

## 1. Core Rule

No Zora Creator Coin enters canon unless it has a replayable acquisition receipt.

Required minimum receipt fields:

- chain_id
- contract_address
- symbol
- block_number
- tx_hash
- metadata_resolution
- metadata_snapshot
- metadata_hash
- acquisition_class
- authority: false

## 2. Factory Stages

### Stage 0 — Concept

Output:

- card_id
- series_id
- proposed symbol
- proposed title
- proposed description
- image candidate

Allowed status:

- SYMBOLIC
- SPECULATIVE

Forbidden status:

- VERIFIED_RECEIPT

### Stage 1 — Metadata Build

Create metadata JSON before mint/deployment.

Required fields:

- name
- description
- image
- external_url
- attributes

Recommended attributes:

- Court
- Series
- Role
- Reversibility Class
- Authority
- Membrane

### Stage 2 — Preflight Hash

Before upload or mint, compute SHA-256 over canonical metadata JSON.

Record:

- metadata_hash
- metadata_hash_method
- canonicalization_method
- operator
- timestamp_utc

Status remains OBSERVED or DRAFT until on-chain binding exists.

### Stage 3 — Upload / Pin

Allowed URI classes:

- https://
- ipfs://

If ipfs:// is used:

- store raw ipfs:// URI
- store resolved gateway URL
- mark gateway_class as MIRROR_GATEWAY unless fetched directly from local/IPFS-native tooling

No black-box mirror is production canon unless the hop is logged.

### Stage 4 — Zora Create / Deploy

After creation, capture:

- chain_id
- contract_address
- tx_hash
- block_number
- block_timestamp
- creator wallet
- referrer wallet, if present

Do not infer canon from page appearance alone.

### Stage 5 — Direct RPC Acquisition

Acquisition class must be DIRECT_RPC.

Resolution order:

1. contractURI()
2. tokenURI(0)
3. uri(0)

No assumption about ERC-721 or ERC-1155 behavior is allowed. Only observed contract behavior may be recorded.

### Stage 6 — Metadata Fetch

Fetch resolved metadata JSON.

Record:

- raw_uri
- resolved_metadata_url
- metadata_json
- metadata_hash
- image_uri
- resolved_image_url, if applicable
- fetch_timestamp_iso

### Stage 7 — Replay Acquisition Receipt

Create receipt:

```json
{
  "receipt_id": "REPLAY_ACQUISITION_RECEIPT_001",
  "acquisition_class": "DIRECT_RPC",
  "reversibility_class": "OBSERVED",
  "authority": false
}
```

Receipt must include:

- metadata_snapshot
- tx_receipt
- evidence_chain
- replay_instructions

### Stage 8 — Symbol Index

No orphan goblins.

Maintain bidirectional mapping:

- card_symbol -> contract_address + contractURI
- contract_address -> card_id + series_id

### Stage 9 — Review Gate

A production candidate must pass:

- schema validation
- hash recompute
- block/tx verification
- metadata URI replay
- image URI replay or explicit UNKNOWN label

### Stage 10 — Canon Promotion

Only after real receipts exist may status move:

CLAIM -> RECEIPT -> VERIFIED_RECEIPT

Promotion requires an explicit transition record.

## 3. Reversibility Classes

- OBSERVED: directly fetched or seen from source
- DERIVED: computed from observed evidence
- SYMBOLIC: lore/canon/story layer
- SPECULATIVE: future, expected, or unconfirmed claim

No class may silently promote itself.

## 4. Failure Modes

### Missing contractURI()

Try tokenURI(0), then uri(0). Record failed attempts.

### IPFS gateway failure

Keep raw ipfs://. Mark resolved URL as unavailable. Do not discard evidence.

### Hash mismatch

Set hash_status to MISMATCH or PENDING_LOCAL_RECOMPUTE. Do not promote.

### Page exists but RPC fails

Page appearance is OBSERVATION only. It is not a replayable receipt.

### RPC succeeds but metadata fetch fails

Record tx and URI evidence. Metadata remains UNKNOWN.

## 5. Required Repository Artifacts

- docs/zora/ZFD-GOBLIN-ACQ-LAYER-V0_1.md
- docs/zora/ZORA_FACTORY_PRODUCTION_MANUAL_V0_1.md
- schemas/zora_goblin_acquisition.v0_1.schema.json
- receipts/drafts/zfd_goblin_acq_layer_fixture_v0_1.json
- receipts/drafts/replay_acquisition_receipt_001.json, once real acquisition exists

## 6. Operator Commands

Example acquisition command:

```bash
python tools/acquisition/metadata_fetcher_v0.py <contract_address> > receipts/drafts/replay_acquisition_receipt_001.json
```

Validation command, if JSON Schema tooling is available:

```bash
python -m json.tool receipts/drafts/replay_acquisition_receipt_001.json
```

Commit command:

```bash
git add receipts/drafts/replay_acquisition_receipt_001.json
git commit -m "Add real replay acquisition receipt 001"
```

## 7. Production Merge Rule

Do not merge as production-ready while any of the following remain true:

- placeholder tx_hash exists
- placeholder metadata_hash exists
- placeholder CID exists
- block_number is synthetic
- metadata_json is synthetic
- acquisition was not replayed

## 8. Final Invariant

The factory creates surfaces.  
The chain creates receipts.  
Replay creates confidence.  
Authority remains false.
