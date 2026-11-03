# Gray Baby Reports

This directory implements the Gray Baby report series as a **verification ledger**, not as a claim that a historical program named Gray Baby existed.

## Canonical series

- `GRAY_BABY_REPORTS_1950_2027.md` — human-readable full-span ledger.
- `GRAY_BABY_REPORT_RECORD_SCHEMA_V0_1.json` — record contract for future machine-readable annual entries.

## Invariants

```text
YEAR_SLOT             != EXISTENCE_CLAIM
NO_PUBLIC_RECEIPT     != CLASSIFIED
CONTEXT_EVENT         != GRAY_BABY_PROVENANCE
JASON_BINDING         = NONE
DARPA_PROGRAM_BINDING = NONE
UAP_BINDING           = NONE
AUTHORITY_CREATED     = FALSE
```

The internal Gray Baby project may observe gaps and preserve receipts. It does not inherit provenance, authority, classification, or identity from JASON, DARPA, FAS, a FOIA denial, or a historical year merely because those objects are indexed here.

## Report states

- `PRE_JASON` — the year predates JASON's 1960 beginning.
- `CONTEXT_EVENT` — a public institutional/report/receipt event is recorded with no Gray Baby binding.
- `UNPOPULATED` — no year-specific receipt has been entered in this version.
- `PROJECT_ARTIFACT` — the internal Gray Baby project has a repository artifact in that year.
- `FUTURE_RESERVED` — future year; no historical event asserted.

Every report record keeps `authority_created=false`.