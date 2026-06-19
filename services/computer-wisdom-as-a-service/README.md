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

Computer Wisdom as a Service helps turn repo chaos into replayable candidate receipts.

It does not ask a client to believe a dashboard. It collects structured evidence, classifies blocker candidates, and reports what the repository dumps can support after replay.

## First Package: 7-Day Repo Replay Audit

The client runs a read-only collector for seven days and returns JSON dumps.

Deliverables are candidate reports until independently replayed:

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
  "outputs_are_candidates_until_replayed": true,
  "authority": false,
  "no_fake_green": true
}
```

## Evidence Ladder

```text
UNKNOWN -> OBSERVED -> PRESERVED -> REPLAYABLE -> VERIFIED
```

## Posture States

```text
OFFERED -> CONFIGURED -> COLLECTION_RUNNING -> DUMPS_PRESERVED -> CANDIDATE_REPORTED -> CLIENT_REPLAYED
```

## What It Detects as Candidates

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
