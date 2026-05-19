# Reputation Layer L1 · Compute Wisdom

Status: L1_CANDIDATE
Operator: jaywisdom.eth / jaywisdom.base.eth
Scope: reviewer reliability, trace quality, correction history, and receipt discipline.

## Purpose

L1 does not rank people by authority.
L1 ranks review events by proof quality.

A reviewer gains reputation only by:

- citing file paths
- citing commit hashes
- citing blob SHAs when available
- mapping fields to claims
- preserving boundary flags
- marking uncertainty as HELD
- correcting stale traces without ego
- producing receipts that can be replayed

## Reputation Inputs

| Signal | Meaning |
|---|---|
| TRACE_COMPLETE | file + branch/ref + commit + field/line supplied |
| BOUNDARY_CLEAN | no badge/onchain/legal/authority overclaim |
| HELD_DISCIPLINE | uncertainty labeled HELD instead of fake verified |
| CORRECTION_ACCEPTED | stale or wrong trace corrected with receipt |
| BATCH_READY | reviewer can consume batch packets |
| BYTE_AWARE | reviewer understands byte/blob/commit distinction |

## Reputation Penalties

| Signal | Meaning |
|---|---|
| HANDWAVE_VERDICT | conclusion before trace |
| WRONG_BRANCH | main/master or raw-cache mistake |
| POINTER_AS_PROOF | treats link/distribution as proof |
| AUTHORITY_LEAK | implies legal/government/institutional power without evidence |
| BADGE_LEAK | suggests public badge without promotion receipt |
| ONCHAIN_LEAK | suggests Base/Zora proof without tx or attestation receipt |

## Reviewer State Model

```json
{
  "reviewer": "Grok | DeepSeek | Jay | Other",
  "review_event": "PENDING",
  "trace_quality": "NONE | PARTIAL | COMPLETE | COMMIT_PINNED",
  "boundary_quality": "CLEAN | WARNING | VIOLATION",
  "held_discipline": true,
  "correction_history": [],
  "reputation_state": "UNSCORED | TRAINING | RELIABLE | NEEDS_REVIEW"
}
```

## Canon

Reputation is not clout.
Reputation is replay quality.
A reviewer earns trust by surviving correction.
