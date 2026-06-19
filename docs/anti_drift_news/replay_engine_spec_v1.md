# REPLAY_ENGINE_SPEC_V1  
Anti-Drift News — Deterministic Replay Engine Specification  
Public From Day One • No Authority • Append-Only

---

## 1. Purpose

The Replay Engine reconstructs all Anti-Drift News game state from the public append-only event log.  
It is the only legitimate way to derive state.  
It guarantees:

- Deterministic reconstruction  
- No hidden writes  
- No privileged mutation  
- Full public verifiability  
- ALMS compatibility  

The website is a view.  
The replay engine is the truth-preserving mechanism (without making truth claims).

---

## 2. Inputs and Outputs

### 2.1 Inputs

#### Event Log (ALMS-backed)

```json
{
  "format": "jsonl",
  "schema": "adn_event.v1.schema.json",
  "source": "ALMS_append_only_log"
}
```

Each line is a full `EVENT_SCHEMA_V1` object.

#### Replay Query

```json
{
  "game_id": "ADN-000001",
  "up_to_event_id": "EVT-000123",
  "up_to_timestamp": "2026-06-02T08:00:00Z"
}
```

Rules:

- At most one of `up_to_event_id` or `up_to_timestamp` may be set.
- If neither is set → replay to latest event.

---

### 2.2 Outputs

Derived `GAME_STATE`:

```json
{
  "game_id": "ADN-000001",
  "url": "https://example.com/news-story",
  "status": "ACTIVE_RECEIPT_HUNT",
  "claims": [],
  "receipts": [],
  "score": {
    "receipt_coverage": 0.75,
    "drift_risk": "MEDIUM"
  },
  "badges": [],
  "events_applied": {
    "count": 42,
    "last_event_id": "EVT-000123",
    "last_timestamp": "2026-06-02T07:59:59Z"
  }
}
```

This object is purely derived.  
No field exists unless produced by replay.

---

## 3. Determinism and Ordering

### 3.1 Canonical Ordering

Events are sorted by:

1. `timestamp` (ascending)  
2. `event_id` (lexicographic ascending)  

This ensures stable replay across machines, time, and implementations.

### 3.2 Determinism Invariant

For a fixed:

- event log  
- game_id  
- replay boundary  

the replay engine must produce bit-identical state.

---

## 4. Validation Pipeline

### 4.1 Per-Event Validation

Each event must pass:

1. Schema validation (`EVENT_SCHEMA_V1`)
2. Authority invariant (`authority === false`)
3. Hash verification  
   - Canonicalize JSON (sorted keys, UTF-8)  
   - Remove `event_hash`  
   - Compute `SHA-256`  
   - Compare to stored hash  

Invalid events are not applied.

### 4.2 Log-Level Validation Result

```json
{
  "log_valid": true,
  "invalid_events": []
}
```

or:

```json
{
  "log_valid": false,
  "invalid_events": [
    {
      "event_id": "EVT-000042",
      "reason": "HASH_MISMATCH"
    }
  ]
}
```

Replay modes:

- strict: abort on first invalid event  
- lenient: skip invalid events but record them  

---

## 5. Internal State Model

The replay engine maintains an internal accumulator:

```json
{
  "game_id": "ADN-000001",
  "url": null,
  "status": "PENDING",
  "claims": {},
  "receipts": {},
  "score": {
    "receipt_coverage": 0,
    "drift_risk": "UNKNOWN"
  },
  "badges": [],
  "events_applied": {
    "count": 0,
    "last_event_id": null,
    "last_timestamp": null
  }
}
```

Notes:

- `claims` and `receipts` are maps internally  
- Public API exposes them as arrays  
- No field is ever mutated outside event application  

---

## 6. Event Application Rules

Each event type has a deterministic transition.

### 6.1 ARTICLE_SUBMITTED

Set:

- `state.url = payload.url`
- `state.status = "ACTIVE_RECEIPT_HUNT"`

### 6.2 CLAIMS_EXTRACTED

For each claim:

- If new → insert with default fields  
- If exists → idempotent (no overwrite)

### 6.3 RECEIPT_SUBMITTED

If new:

- Insert receipt with `PENDING_REVIEW` status  
- Do not overwrite existing receipts  

### 6.4 RECEIPT_ACCEPTED

If receipt exists:

- `verification_status = "VERIFIED"`  
- `hash = payload.hash_sha256`  

### 6.5 RECEIPT_REJECTED

If receipt exists:

- `verification_status = "REJECTED"`  

### 6.6 SCORE_UPDATED

Set:

- `state.score.receipt_coverage`  
- `state.score.drift_risk`  

### 6.7 BADGE_ASSIGNED

Append badge if not already present.

---

## 7. Score Semantics

V1 uses explicit score events:

- Replay engine does not compute coverage  
- It accepts `SCORE_UPDATED` as a non-authoritative view  
- Future versions may support derived scoring  

---

## 8. Replay Algorithm

### High-Level Steps

1. Load events  
2. Validate events  
3. Sort canonically  
4. Filter by `game_id` and replay boundary  
5. Apply events sequentially  
6. Emit final state  

### Conceptual API

```ts
function loadEvents(stream): Event[];
function validateEvents(events): ValidationResult;
function filterAndOrderEvents(events, game_id, up_to): Event[];
function replayGame(events): GameState;
```

---

## 9. ALMS Integration

- ALMS provides the append-only log  
- Replay engine verifies each event hash  
- Replay output may itself be wrapped in a state receipt:

```json
{
  "type": "GAME_STATE_SNAPSHOT",
  "game_id": "ADN-000001",
  "up_to_event_id": "EVT-000123",
  "snapshot_hash": "sha256_of_canonical_game_state",
  "derived_by": "replay_engine_v1"
}
```

This is a reproducible view, not an authority.

---

## 10. Invariants

- No hidden writes  
- No authority elevation  
- Replay supremacy  
- Idempotent application  
- Public from day one  

---

## Canon Phrase

Not anti-news. Anti-drift. Public receipts from day one.
