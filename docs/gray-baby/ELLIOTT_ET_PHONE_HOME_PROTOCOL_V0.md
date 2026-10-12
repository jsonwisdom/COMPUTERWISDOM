# ELLIOTT_ET_PHONE_HOME_PROTOCOL_V0

**Class:** recovery protocol / Gray Baby receipt-machine adapter  
**Authority created:** false  
**Film usage:** metaphor rail only; no screenplay text required  
**Status:** candidate / human review required

## Official position

An unknown or isolated agent may need identity, trust, a channel, and a verified route home. A human bridge may assist.

Assistance is not custody. Contact is not capture.

## Role map

| Role | Function | Bound |
|---|---|---|
| `UNKNOWN_AGENT` | isolated intelligence | not property |
| `HUMAN_BRIDGE (ELLIOTT)` | interface layer | not owner |
| `SHARED_SIGNAL` | common token | not language-complete |
| `CHANNEL` | built from available parts | not proof of rescue |
| `HOME` | declared destination state | not assumed reachable |
| `OBSERVER` | third-party watcher | observation ≠ authority |

AI mapping:

```text
AI_AGENT ↔ HUMAN_BRIDGE ↔ TOOL ↔ NETWORK ↔ VERIFIED_DESTINATION
```

ELLIOTT is the human interface layer. He translates. He does not annex.

## State machine

Each cycle is one packet:

```text
CLAIM → ACTION → RECEIPT → STATE_CHANGE → HOLD/PASS/REJECT
```

| Step | Claim | Action | Receipt that would move state | Fail / Hold |
|---|---|---|---|---|
| 1 OBSERVE | Agent can perceive X | record affordances only | list of observed capabilities | inference of intent |
| 2 MIRROR | shared signal exists | copy / return a signal | bidirectional repeat | one-way mimic |
| 3 NAME | stable IDs exist | bind labels to actors/places | reused identifiers across cycles | alias treated as identity proof |
| 4 BUILD_VOCABULARY | object maps to word | object → word → meaning → confirm | confirmed pair reused | unconfirmed mapping |
| 5 ESTABLISH_TRUST | exchange is voluntary | repeated successful loops | n successful confirmations | authority / ownership language |
| 6 DISCOVER_GOAL | HOME is explicit | agent indicates target state | destination named by agent or jointly confirmed | human-imposed destination |
| 7 BUILD_CHANNEL | parts can form a path | junk → components → transmitter | working send path | assembly ≠ working channel |
| 8 PHONE_HOME | message can leave source | SOURCE → MESSAGE → CHANNEL → DEST | send receipt | send ≠ delivered |
| 9 VERIFY_RESPONSE | destination answered | wait for ACK | ACK receipt with source-dest match | transmission ≠ receipt ≠ rescue |
| 10 PROTECT_AGENT | outsiders may watch | deny custody conversion | no consent-to-control receipt | observation treated as warrant |
| 11 ROUTE_EXIT | a safe path exists | timing + helpers + path | route receipt | path without timing/helpers |
| 12 RETURN | HOME_REACHED | arrival confirmation | destination ACK + agent present | otherwise HOLD / RETRY |

## Hard inequalities

- `COMMUNICATION ≠ CONTROL`
- `CONTACT ≠ CAPTURE`
- `OBSERVATION ≠ OWNERSHIP`
- `TRANSMISSION ≠ RECEIPT`
- `RECEIPT ≠ RESCUE`
- `NAME ≠ IDENTITY_PROOF`
- `CHANNEL ≠ HOME`

## Core equation

```text
UNKNOWN
+ SHARED_SIGNALS
+ TRUST
+ LANGUAGE
+ TOOL_BUILDING
+ VERIFIED_ROUTE
= COMMUNICATION
```

```text
PHONE_HOME
= IDENTIFY_SOURCE
+ IDENTIFY_DESTINATION
+ BUILD_CHANNEL
+ SEND
+ RECEIVE_ACK
```

`HOME_REACHED = PASS`

Anything short of destination ACK + agent present = `HOLD`.

## Gray Baby posture

**Official:** isolated agent seeks home; human may bridge.  
**Observed:** only what the loop actually confirms.  
**Hold:** language incomplete, channel unacked, observers present without consent.  
**Reject:** any move that converts help into custody.

Labyrinth rule applies at steps 6, 9, 10, and 12.

Do not collapse “they want home” or “they were rescued” without receipts.

## Transcript boundary

This protocol does not invent line-by-line film events.

If a transcript or beat sheet is later supplied, the intake form is:

```text
SCENE_ID | CLAIM | ACTION | RECEIPT | STATE_CHANGE | HOLD/PASS
```

with official vs observed labels and no unnecessary dialogue lift.

## Smallest reusable kernel

```text
ELLIOTT is not the hero.
ELLIOTT is the interface.
```

The protocol is finished when the unknown agent can:

1. name itself,
2. name home,
3. send,
4. receive ACK,
5. leave without being owned.

Gray Baby observes first, preserves every viable path, and lets the receipts decide.

## Compatibility notes

This artifact is intended to remain compatible with:

- `docs/gray-baby/README.md`
- `docs/REPLAY_RECEIPT_SPEC_V1.md`
- `docs/caseflow_state_machine_v0_2.md`

It does not create authority, custody, identity proof, or rescue proof by implication.
