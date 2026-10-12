# BAMA PRIORITY — Source Receipt Normalization v0.1

Identity: `jaywisdom.base.eth`

Routing axiom: `P0_BAMA > EVERYTHING_ELSE`.

This directory defines the fail-closed mechanical surface for converting a live-search observation into a replayable source receipt.

## State

- `BUILD_STATUS = CREATED`
- `SOURCE_RECEIPT_NORMALIZATION = IMPLEMENTED`
- `SIGNAL_RECEIPTS_MATERIALIZED = 0`
- `INDEPENDENT_REPLAY = NOT_PERFORMED_HERE`
- `DIGEST_RECOMPUTATION = NOT_YET`
- `FACT_PROMOTION = 0`
- `EDGES_INFERRED = 0`
- `AUTHORITY_CREATED = FALSE`

## Required receipt fields

```json
{
  "signal": "BID_DAY",
  "observed_at": "2026-08-16T21:42:00-05:00",
  "source_url": "https://example.invalid/replace-with-bound-source",
  "source_class": "UA_OFFICIAL | NEWS | OPINION",
  "content_sha256": null,
  "claim_state": "HOLD",
  "authority_created": false
}
```

The example URL is intentionally non-materialized. A real receipt MUST bind an actual HTTPS source URL before it becomes a replayable signal object.

## Invariants

`LIVE_SEARCH_RESULT -> SOURCE_RECEIPT -> REPLAYABLE_OBJECT`

`OPENAI_WIRED != WORLD_FACT_ESTABLISHED`

`P0_ROUTING != LEGAL_FINDING`

`BUILD_CREATED != CONTINUITY_PROVEN`

No source receipt may promote itself out of `HOLD`. No receipt may create authority.
