# COMPUTERWISDOM_REPLAY_BLOCKED_CONTINUITY_V1

## Status

`REPLAY_BLOCKED_CONTINUITY_ACTIVE`

## Purpose

This record preserves Computer Wisdom continuity when replay is blocked by missing custody, missing execution, missing verification, or unavailable primary evidence.

The rule is simple:

> Continuity may be preserved, but authority may not be promoted without replayable evidence.

## Continuity Finding

Computer Wisdom work may be acknowledged as procedurally staged when the conversation, repository state, or operator record shows intent, design, or preparation.

That acknowledgement does **not** equal execution, verification, deployment, liquidity proof, source verification, or attestation success.

## Replay Boundary

A claim remains blocked when any required replay field is missing:

- observed hash
- expected hash
- transaction hash
- attestation UID
- schema UID
- source artifact
- compiled bytecode match
- receipt URL
- custody timestamp
- independent verifier result

If replay evidence is absent, the correct state is:

```text
PREPARED = allowed
EXECUTED = false unless proven
VERIFIED = false unless proven
PROMOTED = false unless proven
```

## No Fake Green Rule

Computer Wisdom must not convert narrative confidence into green status.

Green requires public, replayable, independently checkable evidence.

Yellow may preserve continuity.
Red may record contradiction or failure.
Blocked may record missing evidence.

## Operational Rule

When continuity exists but replay is incomplete, the system must emit:

```json
{
  "continuity": true,
  "replay_complete": false,
  "authority": false,
  "promotion_allowed": false,
  "status": "REPLAY_BLOCKED_CONTINUITY_ACTIVE"
}
```

## Matching Receipt

See:

`receipts/COMPUTERWISDOM_REPLAY_BLOCKED_CONTINUITY_V1.receipt.json`

## Closing Statement

This file protects the membrane.

It allows the project to remember staged work without pretending that staged work has been executed, verified, or promoted.

Truth stays testable.
