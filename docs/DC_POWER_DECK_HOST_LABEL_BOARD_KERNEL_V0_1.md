# DC Power Deck — Host / Label / Board Kernel V0.1

## Status axes

```text
CLAIM.status = VERIFIED / ALLEGED / CONTESTED / HOLD
CARD.status  = LIVE / RETIRED / SATIRE
BOARD.status = SOLO / COMPOSITE / SIMULATION / HISTORICAL
```

These axes are independent.

- CLAIM.status is evidentiary.
- CARD.status is object lifecycle.
- BOARD.status describes the relation between objects currently on the table.
- PARODY never mutates CLAIM.status.

## Board semantics

```text
SOLO       = one HOST in play, no composite
COMPOSITE  = multiple HOSTs/LABELs combined; convergence not claimed
SIMULATION = composite used for play; convergence not asserted
HISTORICAL = every inter-object link in the historical sub-cluster has a receipt
```

A board may be HISTORICAL in a receipt-closed core and SIMULATION at unreceipted edges.

```text
SIMULATION -> HISTORICAL
requires a receipt.

HISTORICAL -> SIMULATION
requires discovery that a required link was unreceipted.
```

Downgrades are cheap. Upgrades cost evidence.

## Locked kernel

```text
PERSON -> occupies / funds / advises / controls / reports on
HOST   -> owns mechanics; exists independently
LABEL  -> modifies HOST; cannot create authority
CLAIM  -> receipt gate; VERIFIED / ALLEGED / CONTESTED / HOLD
BOARD  -> SOLO / COMPOSITE / SIMULATION / HISTORICAL
PARODY -> presentation only; never mutates CLAIM.status
```

## Shared mechanics are intentional

```text
PURSE           = House Appropriations / Senate Appropriations
CLASSIFIED_VIEW = House Intelligence / Senate Intelligence
COUNT_VOTES     = House Whip / Senate Whip
```

Same verb; different HOST.

## D stress test — HOST/LABEL collision threat

Objects:

```text
Lobbyist + Leadership PAC + Committee Chair + Platform
```

Existing Core 52 HOST candidates:

- Lobbyist
- Leadership PAC
- Committee Chair

LABEL candidate:

- Platform

### Result

```text
D_RESULT = DELTA_CANDIDATE
FROZEN   = FALSE
```

**Platform** is ambiguous because **Social Platform** already exists as a HOST. If “Platform” denotes an entity, it collides with HOST. If it denotes a relationship or amplification state, the LABEL should be relation-shaped, for example:

```text
PLATFORM_AMPLIFIED
PLATFORM_BACKED
```

**Chair** remains a valid LABEL only when it describes a relation to a separate HOST. It must not silently duplicate the **Committee Chair** HOST mechanic.

### Proposed non-collision rule

```text
LABEL should describe group membership, role, or relation to a HOST.
LABEL must not name an entity already represented as a HOST.
```

Examples:

- Gang of Eight = group label
- Freedom Caucus = group label
- Leadership = role/group modifier
- Chair = role relation
- Ranking Member = role relation
- PLATFORM_AMPLIFIED = relation modifier
- Lobby Shop = group/organizational modifier only if no Lobby Shop HOST exists
- Coalition = group label
- Task Force = group label

```text
D BOARD.status = SIMULATION
until every claimed real-world inter-object link is separately receipted.

PARODY may render the board at any time
but never upgrades CLAIM.status or BOARD.status.
```

## Core invariant

```text
CARD = POINTER
CARD != RESEARCH DUMP

MECHANIC = GAME FUNCTION
MECHANIC != CLAIM OF REAL-WORLD POWER

REAL-WORLD POWER
= VERIFIED FROM LAW / RULE / RECORD
```
