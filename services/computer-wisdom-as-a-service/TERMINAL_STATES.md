# CWaaS Terminal States

## Evidence Boundary

```json
{
  "service": "COMPUTER_WISDOM_AS_A_SERVICE",
  "mode": "READ_ONLY_COLLECTION",
  "authority": false,
  "no_fake_green": true
}
```

## States

| State | Triggering Condition | Halt? | Manifest Recorded? |
| --- | --- | --- | --- |
| `BLOCKED` | Missing config, missing dependency, or invalid config shape | yes | yes |
| `COLLECTION_RUNNING` | Config accepted and collection started | no | yes |
| `FAILED` | GitHub CLI command fails during collection | yes | yes |
| `MISSING_RECEIPT` | Expected manifest or receipt file is absent after collection | yes | yes |
| `DUMPS_PRESERVED` | Collection completed and dumps were written | no | yes |
| `STALE` | A preserved dump is later judged outside the accepted replay window | no, report-layer state | yes, in candidate report |
| `CANDIDATE_REPORTED` | An audit summary was produced from preserved dumps | no | yes, in report |
| `CLIENT_REPLAYED` | Client or independent reviewer replays the preserved dumps | no | yes, in report |

## Rule

No client-facing output may promote beyond `CANDIDATE_REPORTED` until the preserved dumps are replayed by the client or an independent reviewer.
