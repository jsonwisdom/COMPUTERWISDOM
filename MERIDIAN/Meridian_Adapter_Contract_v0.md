# Meridian Adapter Contract v0

**Status:** FROZEN  
**Version:** 0.1.0  
**Purpose:** Source-preserving ingestion with no inference and no silent enrichment.

## Pure-function contract

```text
fetch(cursor) -> [RawReceipt]
normalize(RawReceipt) -> Meridian_Event_v0
```

## RawReceipt

```yaml
raw_receipt:
  adapter_id: "courtlistener.v0"
  fetched_at: "ISO8601"
  request: {url, params, cursor}
  response_bytes_ref: "storage://..."
  content_hash: "sha256:..."
  source_class: primary | secondary | tip | social
  http_status: 200
```

## Adapter MUST

- Preserve raw bytes before parsing.
- Emit `observed` status only.
- Leave `verification.verifier = null`.
- Leave `collide` empty.
- Emit `event_time: null` if the source does not state it.
- Be idempotent on `content_hash`.

## Adapter MUST NOT

- Summarize.
- Resolve entity names to ids.
- Fill `collide`.
- Set `corroborated`.
- Rewrite a prior event.

## Registry v0

| adapter_id | source | cursor | cadence |
|---|---|---|---|
| courtlistener.v0 | CourtListener / RECAP | docket cursor | poll |
| pacer.v0 | PACER | case cursor | manual/auth |
| regulations.v0 | Regulations.gov | doc cursor | poll |
| congress.v0 | Congress.gov | bill/hearing cursor | poll |
| lobbying.v0 | Senate LDA | filing cursor | poll |
| usaspending.v0 | USAspending | award cursor | poll |
| sam.v0 | SAM.gov | entity cursor | poll |
| mn_courts.v0 | MN Judicial Branch | case cursor | poll |
| mn_cfb.v0 | MN Campaign Finance Board | filing cursor | poll |
| agency_press.v0 | Agency RSS/HTML | feed cursor | poll |

## Separation rule

`collide` is populated only by a separate Collider service that reads entity ids and queries the graph. Collider never mutates `verification.status`.
