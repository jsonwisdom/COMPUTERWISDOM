# Graphiti Read-Only Ingest Prototype v0.1

This directory contains a safe COMPUTERWISDOM memory-ingest prototype.

It does **not** connect to Graphiti, Neo4j, FalkorDB, EAS, Base, GitHub write APIs, wallets, or any runtime executor.

It prepares deterministic, Graphiti-shaped memory episodes from sealed local receipt artifacts only.

## Invariant

```text
memory is not authority
```

## Boundary

```text
authority: NONE
runtime: NOT_PERMITTED
wallet_authority: false
signing_authority: false
execution_authority: false
merge_authority: false
eas_attestation_authority: false
llm_extraction: false
network_required: false
```

## Inputs

The prototype reads only local repo files:

```text
jaytree/memory/graphiti-memory-v0.1.json
jaytree/memory/receipts/graphiti-memory-v0.1.eas-receipt.json
jaytree/operations-manual/receipt-log-v0.1.json
jaytree/operations-manual/lattice-snapshot-v0.1.json
jaytree/external-roots/receipts/al-base-mcp-v0.1.eas-receipt.json
```

Missing optional files are reported but do not create authority.

## Output

```text
jaytree/memory/ingest-ro/out/episodes.jsonl
jaytree/memory/ingest-ro/out/index.json
```

These outputs are rebuildable memory artifacts only.

## Run

From repo root:

```bash
python3 jaytree/memory/ingest-ro/prototype.py
python3 jaytree/memory/ingest-ro/query.py receipt_id vr:sha256:c027a4129b426c47a2d373936bc005c1eacc00f3f10b0d7a5c0deea498fcbc1e
python3 jaytree/memory/ingest-ro/query.py invariant "memory is not authority"
```
