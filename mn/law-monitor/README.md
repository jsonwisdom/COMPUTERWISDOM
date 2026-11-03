# Minnesota Law Monitor ⚖️

**Status:** SCAFFOLD_V0_1  
**Authority:** false  
**Fraud status:** UNKNOWN  
**Parent:** COMPUTERWISDOM operational control plane  
**Surface:** Atomic civic updates — state first

> Atomic civic updates. State first. Official sources.  
> Phased by authority, status, and effective date.  
> COMPUTERWISDOM. ⚙️

## Purpose

Minnesota Law Monitor is a receipt-first civic observation surface for Minnesota legislative and statutory events.

It does **not**:

- declare law
- interpret intent
- assign political meaning
- claim enforcement authority
- invent bill text or status

It **does**:

- record atomic events from official public sources
- preserve source URL, observed_at, and status phase
- make every entry replayable and hashable
- stay machine-auditable under COMPUTERWISDOM doctrine

## Doctrine Alignment

```text
No receipt, no authority.
No official source, no docket entry.
No invented effective date.
Authority remains false by default.
```

## Official Source Roots (allowed)

| Root | Role |
|------|------|
| `https://www.revisor.mn.gov/` | Bill text, session laws, statutes |
| `https://www.house.mn.gov/` | House actions / journals |
| `https://www.senate.mn/` | Senate actions / journals |
| `https://www.leg.mn.gov/` | Session / calendar pointers |
| `https://mn.gov/` | Executive / agency effective-date notices |

Any other domain is rejected at intake until explicitly registered by a governance PR.

## Atomic Event Phases

Events are phased, not narrated:

```text
INTRODUCED
COMMITTEE
PASSED_HOUSE
PASSED_SENATE
CONFERENCE
ENROLLED
PRESENTED
SIGNED / VETOED
EFFECTIVE
CHAPTERED
```

Each phase requires its own source pointer when claimed.

## Directory Layout

```text
mn/law-monitor/
  README.md                 ← this file
  CHARTER.md                ← operating rules
  schema/
    bill_event.v0_1.schema.json
  examples/
    docket_feed_sample.v0_1.json
  docket/
    .gitkeep                ← live atomic events land here later
  surfaces/
    monitor.html            ← public read surface (v0.1 static)
```

## Quick Start

1. Read `CHARTER.md`
2. Validate an example against the schema (when validator lands)
3. Do **not** invent bill numbers, dates, or statuses
4. Every live entry must include `source_url`, `observed_at`, `phase`, and `authority: false`

## Relation to Existing MN Leaves

| Leaf / module | Relationship |
|---------------|--------------|
| LEAF_002 MN Anomaly Portal | Observation intake pattern reuse |
| angie-act | Bill-watch scorecards (separate; influence scoring) |
| docs/game/minnesota_map_v0_1.md | Game map; Law Monitor is the civic data rail |
| LEAF_005 Saint Cloud agenda | Local agenda receipts; Law Monitor is statewide |

Law Monitor is statewide statutory/legislative observation.  
It does not replace local agenda pilots or ANGIE scorecards.

## Next Build Order

1. ✅ Scaffold + schema + sample docket
2. Schema validator script
3. First real atomic entry from Revisor (manual evidence only)
4. Static monitor.html feed render from JSON
5. Replay receipt for each docket mutation
6. Optional: register as civic leaf under missions/

## Closing Rule

```text
Official source or no entry.
Atomic phase or no claim.
Receipt or no promotion.
Authority: false.
```

— Jay Wisdom / `jaywisdom.base.eth`
