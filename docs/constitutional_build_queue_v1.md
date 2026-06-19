# CONSTITUTIONAL_BUILD_QUEUE_V1

Authority: false  
Purpose: Convert CONSTITUTIONAL_IMPLEMENTATION_GAP_REPORT_V1 into an executable build queue  
Invariant: Every build item must produce a receipt

---

## Queue Summary

| Phase | Items | Ready | In Progress | Complete | Blocked | Completion |
|---|---:|---:|---:|---:|---:|---:|
| Phase 1: Schemas | 4 | 4 | 0 | 0 | 0 | 0% |
| Phase 2: Replay Core | 4 | 4 | 0 | 0 | 0 | 0% |
| Phase 3: Tests | 4 | 4 | 0 | 0 | 0 | 0% |
| Phase 4: Replay Client | 4 | 4 | 0 | 0 | 0 | 0% |
| Phase 5: Deployment | 4 | 4 | 0 | 0 | 0 | 0% |
| Phase 6: Existing Schema Receipt | 1 | 0 | 0 | 1 | 0 | 100% |
| **Total** | **21** | **20** | **0** | **1** | **0** | **5%** |

Overall status:

```json
{
  "status": "READY_TO_BUILD",
  "completed_runtime_items": 0,
  "completed_schema_items": 1,
  "authority": false
}
```

No executable replay engine, client CLI, or test suite is marked complete without a repository receipt.

---

## Phase 1: Schemas

Purpose: define all machine data structures before implementation.

| queue_id | artifact | prerequisite | complexity | verification method | status | receipt |
|---|---|---|---|---|---|---|
| Q-001 | `schemas/adn_event.v1.schema.json` | REPLAY_ENGINE_SPEC_V1 | MEDIUM | Ajv validation against valid/invalid fixtures | READY | pending |
| Q-002 | `schemas/adn_game_state.v1.schema.json` | Q-001 | MEDIUM | Ajv validation against replay output fixtures | READY | pending |
| Q-003 | `schemas/segment_manifest.v1.schema.json` | OPEN_SOURCE_REPLAY_CLIENT_SPEC_V1 | LOW | Ajv validation against manifest fixture | READY | pending |
| Q-004 | `schemas/snapshot.v1.schema.json` | Q-002 | LOW | Ajv validation against snapshot fixture | READY | pending |

Completion criteria:

- all schemas use `additionalProperties:false`
- all applicable schemas include `authority:false`
- all schemas have valid and invalid fixtures
- all schemas pass Ajv validation

---

## Phase 2: Replay Core

Purpose: implement the deterministic replay engine.

| queue_id | artifact | prerequisite | complexity | verification method | status | receipt |
|---|---|---|---|---|---|---|
| Q-005 | `src/anti_drift_news/events.ts` | Q-001 | MEDIUM | TypeScript compile and unit tests | READY | pending |
| Q-006 | `src/anti_drift_news/canonicalizer.ts` | Q-001 | MEDIUM | hash fixture tests | READY | pending |
| Q-007 | `src/anti_drift_news/replay.ts` | Q-005, Q-006, Q-002 | HIGH | deterministic replay tests | READY | pending |
| Q-008 | `src/anti_drift_news/segment_reader.ts` | Q-003 | MEDIUM | segment hash verification tests | READY | pending |

Completion criteria:

- replay is deterministic
- invalid events never change state
- duplicate `event_id` conflict is detected
- missing `drift_risk` follows strict/lenient rules
- authority remains false

---

## Phase 3: Tests

Purpose: turn invariants into executable receipts.

| queue_id | artifact | prerequisite | complexity | verification method | status | receipt |
|---|---|---|---|---|---|---|
| Q-009 | `tests/anti_drift_news/replay_engine_v1.test.ts` | Q-007 | HIGH | test runner pass | READY | pending |
| Q-010 | `tests/anti_drift_news/event_schema_edge_cases_v1.test.ts` | Q-001, Q-007 | HIGH | adversarial edge-case tests | READY | pending |
| Q-011 | `tests/anti_drift_news/replay_anomaly_v1.test.ts` | Q-007, Q-021 | MEDIUM | anomaly behavior tests | READY | pending |
| Q-012 | `scripts/assert-event-order-determinism.js` | Q-007 | MEDIUM | repeated replay hash match | READY | pending |

Completion criteria:

- authority flip test passes
- canonicalization permutation tests pass
- duplicate event conflict tests pass
- enum and drift risk strictness tests pass
- empty stream returns minimal valid state

---

## Phase 4: Replay Client

Purpose: let the public verify without trusting the server.

| queue_id | artifact | prerequisite | complexity | verification method | status | receipt |
|---|---|---|---|---|---|---|
| Q-013 | `clients/adn_replay_client_v1/package.json` | Q-007 | LOW | package install/build | READY | pending |
| Q-014 | `clients/adn_replay_client_v1/src/cli.ts` | Q-013 | MEDIUM | CLI command tests | READY | pending |
| Q-015 | `clients/adn_replay_client_v1/src/manifest_loader.ts` | Q-003 | MEDIUM | manifest verification tests | READY | pending |
| Q-016 | `clients/adn_replay_client_v1/src/snapshot_generator.ts` | Q-004, Q-007 | MEDIUM | snapshot hash tests | READY | pending |

Completion criteria:

- `adn verify --game-id ADN-000001`
- `adn leaderboard`
- `adn receipts --claim CLAIM-001`
- `adn manifest verify`
- `adn segment verify --segment-id SEG-000001`
- `adn snapshot generate --game-id ADN-000001`

---

## Phase 5: Deployment

Purpose: make public verification available outside the repo.

| queue_id | artifact | prerequisite | complexity | verification method | status | receipt |
|---|---|---|---|---|---|---|
| Q-017 | public manifest endpoint | Q-003, Q-015 | MEDIUM | curl returns valid manifest | READY | pending |
| Q-018 | immutable event segment storage | Q-003, Q-008 | MEDIUM | segment hash matches manifest | READY | pending |
| Q-019 | root manifest anchor | Q-017, Q-018 | MEDIUM | anchor receipt recorded | READY | pending |
| Q-020 | public client release | Q-013, Q-014, Q-015, Q-016 | MEDIUM | package install and verify command | READY | pending |

Completion criteria:

- public manifest exists
- public segments exist
- independent client can verify a game
- root manifest anchor has receipt

---

## Phase 6: Existing Schema Receipt

| queue_id | artifact | prerequisite | complexity | verification method | status | receipt |
|---|---|---|---|---|---|---|
| Q-021 | `schemas/replay_anomaly.v1.schema.json` | none | LOW | file committed on PR branch | COMPLETE | `a0c6da10c8fe27b9e036f61afb6b5e0b0dd97fc7` |

---

## Dependency DAG

```txt
Q-001 adn_event schema
 ├─ Q-005 events.ts
 ├─ Q-006 canonicalizer.ts
 └─ Q-010 edge-case tests

Q-002 game_state schema
 └─ Q-007 replay.ts
     ├─ Q-009 replay tests
     ├─ Q-011 anomaly tests
     ├─ Q-012 determinism script
     ├─ Q-013 replay client package
     └─ Q-016 snapshot generator

Q-003 segment manifest schema
 ├─ Q-008 segment_reader.ts
 ├─ Q-015 manifest_loader.ts
 ├─ Q-017 public manifest endpoint
 └─ Q-018 segment storage

Q-004 snapshot schema
 └─ Q-016 snapshot generator

Q-013 + Q-014 + Q-015 + Q-016
 └─ Q-020 public client release

Q-017 + Q-018
 └─ Q-019 root manifest anchor
```

Critical path:

```txt
Q-001 -> Q-005 -> Q-006 -> Q-002 -> Q-007 -> Q-009/Q-012 -> Q-013 -> Q-014 -> Q-020
```

---

## Completion Criteria

Every build item must produce one of:

- committed file receipt
- test pass receipt
- CI receipt
- deployment receipt
- anchor receipt

No item may be marked complete without a receipt.

---

## Execution Tracker

| queue_id | status | assignee | started | completed | receipt |
|---|---|---|---|---|---|
| Q-001 | READY | — | — | — | pending |
| Q-002 | READY | — | — | — | pending |
| Q-003 | READY | — | — | — | pending |
| Q-004 | READY | — | — | — | pending |
| Q-005 | READY | — | — | — | pending |
| Q-006 | READY | — | — | — | pending |
| Q-007 | READY | — | — | — | pending |
| Q-008 | READY | — | — | — | pending |
| Q-009 | READY | — | — | — | pending |
| Q-010 | READY | — | — | — | pending |
| Q-011 | READY | — | — | — | pending |
| Q-012 | READY | — | — | — | pending |
| Q-013 | READY | — | — | — | pending |
| Q-014 | READY | — | — | — | pending |
| Q-015 | READY | — | — | — | pending |
| Q-016 | READY | — | — | — | pending |
| Q-017 | READY | — | — | — | pending |
| Q-018 | READY | — | — | — | pending |
| Q-019 | READY | — | — | — | pending |
| Q-020 | READY | — | — | — | pending |
| Q-021 | COMPLETE | pr202 | 2026-06-02 | 2026-06-02 | `a0c6da10c8fe27b9e036f61afb6b5e0b0dd97fc7` |

---

## Canon

Intent becomes implementation.  
Implementation becomes verification.  
Verification becomes receipt.  
Authority remains false.

This site does not ask you to trust it.  
It gives you the math to verify it.

Not anti-news.  
Anti-drift.  
Public receipts from day one.
