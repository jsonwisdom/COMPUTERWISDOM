# ZORA_FACTORY_PRODUCTION_MANUAL_V0_1

Author: jaywisdom  
Scope: DeepSeek -> Computer Wisdom -> Zora Factory production runs for zora.co/@jaywisdom and descendants  
Status: Draft production manual  
Authority: false  
Membrane: HOLDS  

## 0. Purpose

This manual defines the safe production path for converting DeepSeek candidate work into Computer Wisdom receipts and then, only after receipt validation, into Zora public surfaces.

It is a factory manual, not a financial recommendation, not a trading strategy, and not a claim that any coin has value.

## 1. Operator Jay Routing Map

Operator Jay is the routing authority for the production run, but does not convert claims into verified truth without receipts.

### DeepSeek

Use for:

- candidate analysis
- symbolic drafts
- speculative concepts
- narrative compression
- Zora production run ideas
- naming, lore, captions, and early pattern discovery

Output class:

- SYMBOLIC
- SPECULATIVE
- CANDIDATE

Do not use DeepSeek output as final evidence unless it is separately receipt-backed.

### ChatGPT / Computer Wisdom

Use for:

- structuring DeepSeek output
- writing manuals and schemas
- enforcing reversibility classes
- checking inference boundaries
- creating operator commands
- preparing PR language

Output class:

- STRUCTURED_CANDIDATE
- RECEIPT_GATE
- OPERATOR_GUIDANCE

### Codex / Cloud Shell

Use for:

- executable scripts
- metadata fetchers
- hash recompute
- schema validation
- local repo commands
- real acquisition runs

Output class:

- EXECUTION_OUTPUT
- OBSERVED if stdout/stderr is pasted or committed

### GitHub / COMPUTERWISDOM

Use for:

- doctrine
- schemas
- receipts
- pull requests
- review gates
- commit history

Output class:

- REPOSITORY_RECEIPT
- REVIEW_SURFACE

### Zora

Use for:

- public creator coin surface
- contract deployment
- onchain publication
- public metadata surface

Output class:

- PUBLIC_SURFACE
- CHAIN_OBSERVATION only after tx/block/metadata receipts exist

### Operator Jay

Use for:

- deciding what moves forward
- selecting candidate outputs
- approving promotion
- rejecting drift
- preserving family/business boundaries
- deciding when something becomes public

Output class:

- PROMOTION_DECISION
- HOLD_DECISION
- REJECTION_DECISION

## 2. Three-Layer Stack

- DeepSeek: candidate analysis engine. Outputs inference, symbolic structure, speculative framing, and draft production concepts.
- Computer Wisdom: operational control plane. Converts candidates into receipts, validates replayability, marks reversibility class, and blocks silent promotion.
- Zora: public creator-coin surface. Receives only receipt-backed outputs after approval.

Operator Jay routes between all layers.

## 3. Core Law

NO RECEIPT -> NO CLAIM  
NO SOURCE -> NO PUBLIC POST  
NO REPLAY -> NO INGESTION

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

## 4. Intake Pipeline

1. DeepSeek generates candidate material.
2. Operator Jay selects or rejects candidate material.
3. Candidate is marked SYMBOLIC or SPECULATIVE unless directly observed.
4. Computer Wisdom validates candidate against inference marking and replay rules.
5. Validated candidate becomes a draft receipt under receipts/drafts/.
6. Real Zora acquisition receipts are stored under receipts/zora_factory/.
7. Operator Jay acts as promotion gate.
8. Zora public surface happens only after receipt exists.

## 5. Receipt Types

- replay_acquisition_receipt: OBSERVED layer receipt for metadata fetches, tx logs, and contract acquisition.
- derived_receipt: computed from OBSERVED evidence.
- symbolic_receipt: interpretation or lore; must carry model_version or source engine.
- speculative_receipt: hypothesis only; never promoted to authority.

## 6. What Goes Where

| Work Item | Correct System | Output Path |
| --- | --- | --- |
| Raw idea, lore, meme direction | DeepSeek | candidate text |
| Boundary check, schema, manual | Computer Wisdom / ChatGPT | docs/ or schemas/ |
| Real command execution | Cloud Shell / Codex | stdout/stderr or committed file |
| Replayable receipt | COMPUTERWISDOM repo | receipts/zora_factory/ |
| Draft candidate receipt | COMPUTERWISDOM repo | receipts/drafts/ |
| Public mint or coin | Zora | onchain/public URL |
| Promotion decision | Operator Jay | PR comment / receipt transition |

## 7. Factory Stages

### Stage 0 — Concept

Output:

- card_id
- series_id
- proposed symbol
- proposed title
- proposed description
- image candidate
- source_engine, if generated from DeepSeek or another model

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
- Source Engine

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

No orphan factory outputs.

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

## 8. Reversibility Classes

- OBSERVED: directly fetched or seen from source
- DERIVED: computed from observed evidence
- SYMBOLIC: lore/canon/story layer
- SPECULATIVE: future, expected, or unconfirmed claim

No class may silently promote itself.

## 9. Failure Modes

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

### DeepSeek output lacks source boundary

Mark as SYMBOLIC or SPECULATIVE. Do not route to Zora until receipt-backed.

### Operator confusion between systems

Return to the What Goes Where table. Do not publish, mint, or commit until the output path is clear.

## 10. Required Repository Artifacts

- docs/zora/ZFD-GOBLIN-ACQ-LAYER-V0_1.md
- docs/zora/ZORA_FACTORY_PRODUCTION_MANUAL_V0_1.md
- schemas/zora_goblin_acquisition.v0_1.schema.json
- receipts/drafts/zfd_goblin_acq_layer_fixture_v0_1.json
- receipts/zora_factory/replay_acquisition_receipt_001.json, once real acquisition exists
- services/zora-flywheel/factory_crawler_spec_candidate.md
- services/zora-flywheel/factory_receipt_schema_candidate.json

## 11. Operator Commands

Example acquisition command:

```bash
python tools/acquisition/metadata_fetcher_v0.py <contract_address> > receipts/zora_factory/replay_acquisition_receipt_001.json
```

Validation command, if JSON Schema tooling is available:

```bash
python -m json.tool receipts/zora_factory/replay_acquisition_receipt_001.json
```

Commit command:

```bash
git add receipts/zora_factory/replay_acquisition_receipt_001.json
git commit -m "Add real replay acquisition receipt 001"
```

## 12. Production Merge Rule

Do not merge as production-ready while any of the following remain true:

- placeholder tx_hash exists
- placeholder metadata_hash exists
- placeholder CID exists
- block_number is synthetic
- metadata_json is synthetic
- acquisition was not replayed
- DeepSeek candidate text is promoted without source boundary

## 13. Final Invariant

Operator Jay routes.  
DeepSeek proposes.  
Computer Wisdom structures.  
Receipts constrain.  
Zora publishes.  
Replay creates confidence.  
Authority remains false.
