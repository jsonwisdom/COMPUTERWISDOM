# jaywisdom.base.eth Receipts Rail — Batch 001: Ladies First

Status: SCAFFOLD_ONLY / NO_PRIMARY_ROWS_INGESTED
Date: 2026-09-10
Target name: `jaywisdom.base.eth`
Target address: `0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8`
Authority created: false

## Gate

```text
LIVE_QUERY_ACCESS       = TRUE
RAIL_INGEST_RULE        = PRIMARY_EXPORT_REQUIRED
WEB_PAGE_SNIPPET        != PRIMARY_ROW
KNOWN_UID               != ENUMERATED_LEDGER
DESCRIPTION             != ROW
PRIMARY_DATA            = NOT_INGESTED
ROWS_EMITTED            = 0
```

No scrape-to-ledger. No memory-to-ledger. No narrative-to-row.

## Match rule

A primary-export row is admissible only when at least one condition is true:

```text
attestation.recipient == 0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8
OR attestation.data contains jaywisdom.base.eth
OR attestation.data contains 0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8
```

## Dedupe and order

```text
DEDUP_KEY = (tx_hash, schema_uid, attestation_uid)
ORDER     = block_time ASC
```

## Classes

```text
R1    = schema #1576 / identity binding
R2    = schema #1526 / operator provenance
R3    = schema #1578 / textual asset anchor
OTHER = every other schema
```

Class tags are mechanical labels only. They do not promote authority or create cross-rail links.

## Frozen output row

```text
uid | tx_hash | block_time | schema_uid | from | recipient | class | authority
```

`authority = FALSE` is hard-bound for every emitted row.

## Primary source gate

Accepted ingest sources:

1. EASScan/Base EAS address-page export
2. Base EAS subgraph/API dump containing the frozen row fields
3. Base RPC `Attested` event-log export with sufficient fields to reconstruct the frozen row without inference

A web snippet, prose description, remembered UID, screenshot transcription, or secondary index is not an admissible row source.

## Batch execution law

Batch 001 creates only the contract and validation surface. It MUST NOT fabricate or preload any attestation rows.

```text
ENUMERATION_PROTOCOL    = FROZEN
PRIMARY_DATA            = NOT_INGESTED
ROWS_EMITTED            = 0
LEDGER_STATE            = STARTED / NOT_COMPLETE
CROSS_RAIL_FTX          = NONE
CROSS_RAIL_DOGE         = NONE
AUTHORITY_CREATED       = FALSE
```

Future batches may ingest exported primary sets, validate required fields, dedupe, sort, and emit a reconstructed chronological ledger. Receipt presence does not imply global identity authority, ownership, legal authority, or cross-rail nexus.
