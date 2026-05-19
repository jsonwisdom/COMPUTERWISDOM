# Zora Factory Crawler · Candidate Spec

Status: Candidate only, not live.
Operator: jaywisdom.base.eth
Zora profile: https://zora.co/@jaywisdom
Portal mutation: none.
Public badge: none.
Backend claim: none.
Onchain claim: none.

## Purpose

Periodically crawl `https://zora.co/@jaywisdom` drops, fetch metadata, compute SHA-256, generate candidate receipts, and stage them for review.

The crawler is a candidate design, not a live crawler.

## Input

- Zora profile API or public feed
- Approved artifact list
- Existing Zora portal metadata
- Manual drop records supplied by Jay

## Output

`receipts/zora_factory/drop_<token_id>_receipt.json`

## Constraints

- No live claims about ownership.
- All receipts start as `CANDIDATE`.
- Jay must verify each receipt before it becomes `VERIFIED`.
- Verified receipts can be appended to a Merkle tree.
- No portal mutation.
- No secret data in metadata.
- No claim that a Zora image is proof by itself.

## Candidate Pseudocode

```python
# Example only — not live
for drop in zora_api.get_drops_by_creator("jaywisdom.base.eth"):
    metadata = fetch_metadata(drop.metadata_uri)
    metadata_hash = sha256(metadata)
    create_receipt(
        receipt_id=f"ZORA_FACTORY_{drop.token_id}",
        status="CANDIDATE",
        zora_drop={
            "chain": drop.chain,
            "contract_address": drop.contract_address,
            "token_id": str(drop.token_id),
            "drop_title": metadata.title,
            "drop_description": metadata.description,
            "mint_tx_hash": drop.mint_tx_hash or "PENDING"
        },
        receipt_anchor={
            "sha256_of_metadata": metadata_hash,
            "merkle_root": get_current_merkle_root(),
            "previous_receipt_hash": get_previous_receipt_hash()
        },
        claim_tags={
            "ownership_claim": "HELD",
            "authorship_claim": "HELD",
            "receipt_integrity": "HELD"
        }
    )
    stage_in_candidates()
```

## Factory Gate

Factory output can advance only after:

1. Secret scan receipt is PASS or reviewed WARN.
2. Repo chain check is complete.
3. Factory receipt schema is reviewed.
4. Candidate receipt validates against schema.
5. Jay approval receipt exists.

## Canon

The factory mints receipts, not delusions.

Crawl first.
Hash second.
Receipt third.
Review fourth.
Merkle fifth.
Image last.
