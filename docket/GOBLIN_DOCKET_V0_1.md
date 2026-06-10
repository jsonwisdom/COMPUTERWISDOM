# Goblin Court V0.1 — Docket

## Status

```json
{
  "artifact": "GOBLIN_DOCKET_V0_1",
  "system": "Goblin Court",
  "version": "0.1.0",
  "authority": false,
  "replay_native": true,
  "membrane": "HOLDS"
}
```

## Purpose

The docket records cases, claims, receipts, replay references, and disputes without declaring truth, liability, or winners.

## Docket Entry Format

```json
{
  "case_id": "GC-0001",
  "entry_type": "CLAIM|OBSERVATION|RECEIPT|ANCHOR|REPLAY|DISPUTE|SETTLEMENT_SURFACE",
  "source": "human|agent|system|external",
  "observed_at": "ISO-8601 timestamp or declared observation time",
  "evidence_refs": [],
  "receipt_refs": [],
  "replay_refs": [],
  "dispute_refs": [],
  "truth_status": "UNDETERMINED",
  "authority": false
}
```

## Case ID Rule

Case IDs use the form `GC-0001`, incrementing by docket order. A case ID is an index key, not an adjudication marker.

## Evidence References

Evidence references may include file paths, commit SHAs, blob SHAs, issue URLs, PR URLs, EAS UIDs, transaction hashes, or external document references. Evidence reference presence does not imply truth.

## Replay References

Replay references identify reconstruction attempts. Replay output may be MATCH, MISMATCH, INCOMPLETE, or BLOCKED.

## Dispute References

Disputes are first-class states. A dispute applies pressure to a receipt graph but does not declare a bad actor or winner.

## Non-Authority Rule

The docket records what was claimed, observed, receipted, anchored, replayed, or disputed. It does not decide what is true.
