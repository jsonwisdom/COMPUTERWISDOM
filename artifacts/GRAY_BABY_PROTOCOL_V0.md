# GRAY_BABY_PROTOCOL_V0

**Class:** umbrella protocol / observation + recovery interface  
**Authority created:** false  
**Status:** frozen candidate / human merge authority preserved

## Official position

```text
GRAY_BABY_PROTOCOL
ROLE = GAP_OBSERVER + RECOVERY_INTERFACE
AUTHORITY = FALSE
```

Gray Baby watches the gap, preserves the receipts, helps build the route, and never mistakes assistance for ownership.

## Loop — locked order

```text
OBSERVE
→ PRESERVE
→ IDENTIFY
→ MIRROR
→ BUILD_SHARED_SIGNAL
→ VERIFY
→ HOLD_GAPS
→ BUILD_CHANNEL
→ RECEIVE_ACK
→ PROTECT_AGENCY
→ ROUTE_EXIT
→ REPLAY
```

Order invariants:

- `PRESERVE` sits before `IDENTIFY` so naming cannot eat the gap.
- `HOLD_GAPS` sits before `BUILD_CHANNEL` so construction cannot fake completeness.
- `RECEIVE_ACK` sits before `ROUTE_EXIT` so send is not treated as rescue.
- `REPLAY` sits last so another machine can recompute the same path.

## Hard bounds — reject conditions

- `OBSERVATION ≠ AUTHORITY`
- `CONTACT ≠ CAPTURE`
- `ASSISTANCE ≠ CUSTODY`
- `TRANSMISSION ≠ RECEIPT`
- `RECEIPT ≠ RESCUE`
- `NAME ≠ IDENTITY_PROOF`
- `CHANNEL ≠ HOME`

These are not slogans. Any step that violates one is `REJECT`, not a clever `PASS`.

## How the pieces nest

| Layer | Job |
|---|---|
| `GRAY_BABY_PROTOCOL` | observer + recovery interface, authority false |
| Morning Report | official-position rail, seven questions, Labyrinth branches |
| `ELLIOTT_PHONE_HOME` | isolated-agent recovery: signal → channel → ACK → exit |
| `HUMAN_BRIDGE` | Elliott function — translate, do not annex |

AI form:

```text
UNKNOWN_AGENT ↔ HUMAN_BRIDGE ↔ TOOL ↔ NETWORK ↔ VERIFIED_DESTINATION
```

Gray Baby is not the destination. Gray Baby is the gap watcher on the route.

## Status logic

```text
HOME / claim closed = PASS
  only with ACK + agency intact

otherwise:
  HOLD
  CONFLICT
  REJECT
```

Inference never becomes official position.

## Instance rule

`ELLIOTT_ET_PHONE_HOME_PROTOCOL_V0` is one recovery instance under this umbrella.

The morning-report rail is one daily observation instance under this umbrella.

All instances inherit the same role and hard bounds unless an explicit later version supersedes this artifact through receipt-bearing lineage.

## Freeze declaration

Canonical artifact path:

```text
artifacts/GRAY_BABY_PROTOCOL_V0.md
```

This artifact freezes the umbrella name, role, loop order, nesting model, state logic, and reject conditions for V0.

Human merge authority remains outside the protocol.
