# CONSISTENCY_CONSTITUTIONAL_BUILD_V1

Anti-Drift News — Cross-Repo Constitutional Doctrine  
Ratified: 2026-06-02 by Jay Wisdom  
Authority: false  
Public from day one

---

## Purpose

This document binds Anti-Drift News to the existing Jay Wisdom replay lineage across AL, COMPUTERWISDOM, JOY, ENS, and ALMS.

It defines consistency as a constitutional property, not a feature.

The system does not decide truth.  
The system preserves replayable evidence, public standing, and verifiable divergence.

---

## Cross-Repo Constitutional Lineage

```txt
AL -> COMPUTERWISDOM -> JOY -> ENS -> ALMS
```

### Roles

- **AL** supplies doctrine, court logic, and replay protocol.
- **COMPUTERWISDOM** supplies the public civic verification surface.
- **JOY** supplies protection, voice, custody, continuity, and safety membrane.
- **ENS** supplies display identity only; it is not authority.
- **ALMS** supplies append-only memory, receipt routing, and replay substrate.

### Core Cross-Repo Rule

Memory is allowed.  
Promotion is blocked until receipt.

No repository becomes authority over the others.

---

## Article I — Authority Prohibition

`authority:false` is constitutional, not configurable.

No event, replay output, badge, score, leaderboard, snapshot, client, server, UI, anchor, or maintainer action may elevate itself into authority.

Forbidden:

- admin override
- privileged mutation
- hidden state
- last-write-wins history
- unreviewable score changes
- authority by identity anchor

---

## Article II — Append-Only Log

The event log is append-only.

Duplicate event handling:

```txt
same event_id + same event_hash = duplicate delivery, apply once
same event_id + different event_hash = corruption or replay conflict
```

A duplicate `event_id` is never an update.

Mutation Operator 8 is constitutional law:

```txt
DUPLICATE_EVENT_ID_CONFLICT
```

No event may be edited, deleted, merged, replaced, or silently compacted.

---

## Article III — Replay Supremacy

The replay engine is the only lawful way to derive state.

The website is a view.  
The server is convenience.  
The client is verification.

Replay output must be:

- deterministic
- idempotent
- hash-verifiable
- schema-verifiable
- reproducible across independent clients

If two lawful clients replay the same valid event stream and produce different state, the system is in dispute.

---

## Article IV — Standing

Standing is derived from verification, not permission.

A participant has standing when they can demonstrate replay-relevant divergence.

Standing sources include:

- `DIRECT_REPLAY_DIVERGENCE`
- `HASH_MISMATCH`
- `AUTHORITY_ESCALATION_OBSERVED`
- `PUBLIC_INTEREST`

Injury-in-fact may be represented as:

```txt
local_hash != server_hash
```

Any correct replay has standing.

No gatekeeper is required.

---

## Article V — Reputation Layer

Reputation is evidence of reliability, not authority.

Reputation may be derived from:

- correct anomaly reports
- consensus matches across independent replay clients
- accurate receipt submissions
- valid dispute reports
- repeated hash agreement

Reputation must never become permission to override replay.

A reputation field may be attached to anomalies as context:

```txt
standing.reputation_at_detection
```

Jay Wisdom Principle:

Knowing what is up is verifiable standing only when the evidence replays.

---

## Article VI — Anomalies as Evidence

Anomalies are replay-derived observations.

They do not mutate state.

Required anomaly classes include:

- `DUPLICATE_EVENT_ID_CONFLICT`
- `HASH_MISMATCH`
- `AUTHORITY_TRUE`
- `SCHEMA_INVALID`
- `MISSING_REQUIRED_FIELD`
- `INVALID_ENUM`
- `INVALID_TIMESTAMP`
- `SEGMENT_CORRUPTED`
- `MANIFEST_CORRUPTED`

Anomalies may generate receipts.  
Anomalies may support disputes.  
Anomalies may not become authority.

---

## Article VII — Consistency Guarantees

The core consistency guarantees are:

```txt
INVALID EVENTS NEVER CHANGE STATE
VALID EVENTS ALWAYS PRODUCE DETERMINISTIC STATE
UNKNOWN REMAINS UNKNOWN UNTIL SUPPORTED BY RECEIPTS OR VALID EVENTS
```

No hidden inference is allowed.

No missing data may become `LOW`, `MEDIUM`, or `HIGH` drift risk.

Missing drift metadata must remain:

```txt
UNKNOWN
```

unless valid events support a stronger classification.

---

## Article VIII — Public Verification

The open-source replay client completes the public verification contract.

Any participant must be able to:

- fetch the manifest
- verify manifest hash
- fetch event segments
- verify segment hashes
- validate events
- replay events
- compute GAME_STATE
- verify badges
- verify leaderboard
- verify receipts
- verify drift risk
- produce snapshot receipts

No login may be required for verification.

---

## Article IX — Dispute by Replay

Disputes are resolved by replay, not status.

A dispute must identify:

- the event or segment involved
- the expected hash
- the observed hash
- the replay boundary
- the client or validator version
- the derived divergence

Disputes may enter the event log as events.

No dispute creates authority by itself.

---

## Article X — Amendment Process

Amendments must preserve the constitutional invariants.

Required amendment checks:

1. No authority elevation.
2. No hidden mutation.
3. No loss of replay determinism.
4. No private verification dependency.
5. No regression in public standing.
6. No reputation-to-authority conversion.
7. No broken cross-repo lineage.

For major constitutional changes, require three independent implementation paths before promotion.

---

## Article XI — Cross-Repo Promotion Rule

AL may supply doctrine.  
COMPUTERWISDOM may publish public replay surfaces.  
JOY may protect continuity and custody.  
ENS may display identity.  
ALMS may remember routes and receipts.

None of these layers may silently promote a claim, state, score, badge, identity, or dispute into authority.

Promotion requires a receipt.

---

## Bound Artifacts

This constitution binds and contextualizes:

- `EVENT_SCHEMA_V1`
- `REPLAY_ENGINE_SPEC_V1`
- `UI_WIREFRAME_SPEC_V1`
- `OPEN_SOURCE_REPLAY_CLIENT_SPEC_V1`
- `EVENT_SCHEMA_EDGE_CASE_TEST_SPEC_V1`
- `REPLAY_ANOMALY_INTERFACE_V1`
- `REPLAY_ANOMALY_SCHEMA_V1`
- Standing doctrine
- Reputation layer
- Cross-repo AL / COMPUTERWISDOM / JOY / ENS / ALMS lineage

---

## Canon Phrase

This site does not ask you to trust it.  
It gives you the math to verify it.

Not anti-news.  
Anti-drift.  
Public receipts from day one.

---

## Final Line

AL gives doctrine.  
COMPUTERWISDOM gives public replay.  
JOY protects continuity.  
ALMS remembers.  
ENS displays.  
None of them becomes authority.
