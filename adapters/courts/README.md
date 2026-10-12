# RePlay Genesis Court Adapter v0.1

Status: MATERIALIZED / NOT_PRODUCTION_READY  
Authority: false  
Branch: `replay-global-genesis-v0-1`

## Purpose

Court-source adapter for evidence-bounded retrieval, provenance receipts, deterministic hashing, and EAS dry-run mapping.

## Source routing

```text
COURT RECORD AUTHORITY -> court-issued filing / order / judgment
PACER / CM/ECF        -> official court-record distribution and filing surface
RECAP / CourtListener -> public index / mirror; never promoted to court authority by itself
UniCourt              -> enrichment only unless independently bound to official source
```

## Frozen EAS mapping

- Network: Base
- Chain ID: `8453`
- Schema UID: `0xc90097ca9f787edcc5fa2ce0920032abe4c4417cc8356198fa12d397c46a453c`
- Revocable: `false`
- Resolver: zero address

Schema:

```text
bytes32 receiptHash,bytes32 lineageHash,bytes32 previousReceiptHash,bytes32 subjectHash,bytes32 sourceRefHash,uint64 createdAt,uint8 evidenceState,uint8 retrievalState
```

## Current implementation boundary

`replay_court_adapter_v0_1.py` supports public RECAP/CourtListener retrieval, deterministic v0.1 receipt construction, self-hash validation, EAS dry-run mapping, and pending seal-envelope construction.

PACER authentication, persistent token cache, paid retrieval, receipt-store persistence, EAS signing, and transaction broadcast are intentionally NOT implemented in this module.

## Fail-closed rules

- failed retrieval -> `evidence_state=UNRESOLVED`
- failed retrieval -> `retrieval_state=FAILED`
- a retrieval-error artifact hash is never labeled as a court-document hash
- no floats in canonical receipt data
- no secret-bearing fields
- no mainnet attestation from a dry-run fixture
- `authority=false` always

## First fixture

`fixtures/court/RECAP_TEST_RECEIPT_001.json` records a genuine attempted public RECAP/CourtListener fetch for docket `1:26-cv-01417`. The fetch returned HTTP 403 in the execution environment, so the receipt remains `UNRESOLVED / FAILED`. This is intentional negative-control behavior, not a successful court-record retrieval.
