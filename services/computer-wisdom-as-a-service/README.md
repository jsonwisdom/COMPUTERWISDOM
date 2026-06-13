# Computer Wisdom as a Service

## Status

```json
{
  "service": "COMPUTER_WISDOM_AS_A_SERVICE",
  "version": "0.1",
  "mode": "READ_ONLY_FIRST",
  "authority": false,
  "no_fake_green": true
}
```

## Promise

Computer Wisdom as a Service turns repo chaos into replayable receipts.

It does not ask a client to believe a dashboard. It collects structured evidence, classifies blockers, and reports what the repository can actually prove.

## First Package: 7-Day Repo Replay Audit

The client runs a read-only collector for seven days and returns JSON dumps.

Deliverables:

- `audit_summary.md`
- `repo_weather.json`
- `blocked_prs.json`
- `failed_checks.json`
- `stale_prs.json`
- `repair_plan.md`

## Boundary

```json
{
  "collect": true,
  "repair": false,
  "open_prs": false,
  "merge": false,
  "delete": false,
  "force_push": false,
  "authority": false
}
```

## Evidence Ladder

```text
UNKNOWN -> OBSERVED -> PRESERVED -> REPLAYABLE -> VERIFIED
```

## What It Detects

- stale pull requests
- failed checks
- missing required checks
- mergeability blockers
- review-thread blockers
- missing receipts
- claims without replay paths
- repo rule violations

## Tagline

We do not ask your repo to look healthy. We make it replay its own receipts.
