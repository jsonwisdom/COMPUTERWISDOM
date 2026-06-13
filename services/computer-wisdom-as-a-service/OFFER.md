# Computer Wisdom as a Service

## 7-Day Repo Replay Audit

Your repo may look active while hiding stale PRs, failed checks, blocked merges, missing receipts, and unsupported claims.

Computer Wisdom as a Service runs a read-only audit loop and turns repo chaos into replayable receipts.

## What You Get

- repo weather report
- blocked PR map
- stale PR list
- failed check inventory
- missing receipt report
- repair plan

## What We Do Not Do

- no force pushes
- no silent merges
- no authority claims
- no fake green
- no mutation during the audit collection phase

## How It Works

1. You provide repository access or exported GitHub data.
2. The collector runs in read-only mode for seven days.
3. JSON dumps are preserved.
4. Computer Wisdom classifies blockers, stale work, failed checks, and missing evidence.
5. You receive a repair plan with evidence-backed recommendations.

## Evidence Boundary

```json
{
  "package": "7_DAY_REPO_REPLAY_AUDIT",
  "mode": "READ_ONLY_COLLECTION",
  "client_run_completed": false,
  "repair_performed": false,
  "authority": false,
  "no_fake_green": true
}
```

## Client Command

```bash
chmod +x run.sh
./run.sh config.json
```

After seven days:

```bash
tar -czf audit-dumps.tgz dumps/
```

## Tagline

We do not ask your repo to look healthy. We make it replay its own receipts.
