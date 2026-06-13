# Computer Wisdom as a Service

## 7-Day Repo Replay Audit

Your repo may look active while hiding stale pull requests, failed checks, blocked merges, missing receipts, and unsupported claims.

Computer Wisdom as a Service offers a read-only collection loop that can turn repo activity into candidate replay receipts. Final findings depend on the JSON dumps produced by a completed client run.

## What You Get

All deliverables are candidate reports until a reviewer replays the dumps.

- repo weather report candidate
- blocked PR map candidate
- stale PR list candidate
- failed check inventory candidate
- missing receipt report candidate
- repair plan candidate

## What We Do Not Do

- no force pushes
- no silent merges
- no authority claims
- no fake green
- no mutation during the audit collection phase
- no claim that a repo is healthy or unhealthy without replayed dumps

## How It Works

1. You provide repository access or exported GitHub data.
2. The collector runs in read-only mode for seven days.
3. JSON dumps and a run manifest are preserved.
4. Computer Wisdom classifies blocker candidates, stale-work candidates, failed-check candidates, and missing-evidence candidates.
5. You receive candidate recommendations mapped to dump files.

## Evidence Boundary

```json
{
  "package": "7_DAY_REPO_REPLAY_AUDIT",
  "mode": "READ_ONLY_COLLECTION",
  "client_run_completed": false,
  "outputs_are_candidates_until_replayed": true,
  "repair_performed": false,
  "authority": false,
  "no_fake_green": true
}
```

## Posture States

```text
OFFERED -> CONFIGURED -> COLLECTION_RUNNING -> DUMPS_PRESERVED -> CANDIDATE_REPORTED -> CLIENT_REPLAYED
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
