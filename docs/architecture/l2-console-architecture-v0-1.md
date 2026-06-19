# L2 Console Architecture V0.1

Status: OBSERVE_AND_RECEIPT_ONLY
Authority: false
Membrane: HOLDS

## Purpose

Define the L2 Console as the live observation cockpit for the active COMPUTERWISDOM replay runway after PR 165 merged.

## Source Chain

AL -> COMPUTERWISDOM -> JOY -> ENS -> EAS -> ALMS -> External Surfaces

## Console Panels

1. Runtime Status
2. Replay Spine
3. External Watchers
4. Surface 1 Live Price and Liquidity
5. GitHub Governance
6. Risk Boundary
7. ALMS Watcher Queue
8. Promotion Rules

## Runtime Status

- PR 165: MERGED
- Runtime: ACTIVE
- Authority: false
- Membrane: HOLDS

## External Watchers

- Zora Native
- BaseScan
- DexScreener

## Surface 1

Contract:
0x17c7f908a0cbd2d415c44fb4098f229878e3ea7c

Chain:
Base, chain id 8453

Relationship:
UNVERIFIED_EXTERNAL_OBSERVATION

## Telemetry Mode

Option A is active for v0.2:
client-side JavaScript fetch from DexScreener.

Telemetry is read-only.
Telemetry does not write to chain.
Telemetry does not create ownership claims.
Telemetry does not provide financial advice.

## Promotion Rules

Observation -> Receipt
Receipt -> Verified Receipt only after independent validation
External Token -> Machine Link only after deployer, metadata, timestamp, and source receipts

Final line: Active runway. Live console. External surfaces observed, not absorbed.
