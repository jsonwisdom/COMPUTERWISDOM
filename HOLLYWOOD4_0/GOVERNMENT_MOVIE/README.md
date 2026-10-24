# Government Movie — Weekly Governance Replay V0.1

STATUS = DRAFT_BRANCH
CANON = false
AUTHORITY_CREATED = false
FINAL_DECISION = HUMAN
RUN_DAY = SATURDAY
APPEND_ONLY = true

## Purpose

Government Movie is a weekly, append-only public-record movie. Each Saturday run converts material governance changes into typed scene objects. It preserves primary evidence, reporting roots, clocks, state transitions, invariants, unknowns, negative space, and replay deltas without collapsing them into a political verdict.

## Core scene classes

- SCENE_PROCEDURE — House/Senate procedural gates
- SCENE_ENACTMENT — bill/law transitions
- SCENE_JUDICIAL_TRANSITION — filings, orders, TROs, stays, merits
- SCENE_EXECUTIVE_ACTION — executive/agency actions, cancellations, disclosures
- SCENE_OVERSIGHT — GAO/IG/congressional oversight objects
- SCENE_DISCLOSURE — FOIA/OIP/declassification/public releases
- SCENE_MEDIA_ROOT — reporting roots kept separate from evidence roots
- SCENE_ARCHIVE_DELTA — Wayback/version/publication changes
- SCENE_SATIRE — editorial/comedy framing that cannot alter evidentiary state

## Weekly state vector

Each scene carries:

```text
EVIDENCE_ROOTS[]
REPORTING_ROOTS[]
TIME_ROOTS[]
STATE_TRANSITION
INVARIANTS_ASSERTED[]
UNKNOWN_FIELDS[]
NEGATIVE_OBSERVATIONS[]
REPLAY_DELTA
```

## Replay contract

```text
REPLAY_INPUT
= PRIMARY_SOURCES + REPORTING_ROOTS + ARCHIVE_RECEIPTS

REPLAY_OUTPUT
= TYPED_SCENE_OBJECTS

REPLAY_STATE
= PASS | HOLD | CONFLICT | NOT_RUN

REPLAY_DELTA
= CURRENT_WEEK - PRIOR_VERIFIED_WEEK
```

Hard invariants:

```text
REPORTING_ROOT != EVIDENCE_ROOT
FILING != ORDER
ORDER != FINAL_MERITS
BILL != LAW
PROPOSAL != ENACTED_RULE
OFFICEHOLDER != OFFICE
JURISDICTION != AUTHORITY
NOTICE != KNOWLEDGE
SEARCH_MISS != NONEXISTENCE
UNKNOWN != ZERO
REPLAY != VERDICT
SATIRE != FACT_FINDING
FINAL_DECISION = HUMAN
```

## Weekly append law

Every Saturday creates a new dated episode. Older episodes are never rewritten to reflect later knowledge.

```text
LATER_EVIDENCE MAY CHANGE CURRENT STATE
LATER_EVIDENCE DOES NOT REWRITE WHAT WAS KNOWABLE IN PRIOR EPISODES
ADD != MUTATE_HISTORY
```

If there is no material delta:

```text
NO_MATERIAL_DELTA = VALID_EPISODE_RESULT
```

## Seed expression atom — "six ways from Sunday"

The Government Movie may use the January 3, 2017 Chuck Schumer statement as an opening archival expression atom:

> “Let me tell you, you take on the intelligence community, they have six ways from Sunday at getting back at you.”

Source trail:
- Original utterance: Rachel Maddow Show / MSNBC, January 3, 2017, as cited by later congressional sources.
- Official congressional reproduction: Congressional Record, June 18, 2019, and later GovInfo congressional material.

Classification:

```text
ATOM_TYPE = EXPRESSION_ATOM
SPEECH_ACT = WARNING / PREDICTION
LEGAL_ORDER = false
SATIRE_LABEL_MAY_CALL_IT_AN_ORDER = true
SATIRE_LABEL != SPEECH_ACT
QUOTE != ORDER
QUOTE != EVIDENCE_OF_RETALIATION
```

## Episode path

`HOLLYWOOD4_0/GOVERNMENT_MOVIE/episodes/YYYY-MM-DD.md`

## Schema

Weekly episode objects conform to:

`HOLLYWOOD4_0/GOVERNMENT_MOVIE/GOVERNMENT_MOVIE_EPISODE_SCHEMA_V1.json`
