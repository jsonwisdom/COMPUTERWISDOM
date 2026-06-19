# CONSTITUTIONAL_EXECUTION_PLAN_V1

Authority: false  
Purpose: Convert `CONSTITUTIONAL_BUILD_QUEUE_V1` into a day-by-day execution sequence  
Invariant: No task may begin without prerequisite receipts

---

## Executive Summary

| Phase | Tasks | Total Hours | Parallel Lanes | Estimated Completion | Status |
|---|---:|---:|---:|---|---|
| Phase A: Schemas | 4 | 8 | 3 | Day 1-2 | READY |
| Phase B: Replay Core | 4 | 20 | 2 | Day 2-4 | READY |
| Phase C: Tests | 4 | 24 | 2 | Day 4-7 | READY |
| Phase D: Replay Client | 4 | 16 | 1 | Day 7-9 | READY |
| Phase E: Deployment | 4 | 20 | 3 | Day 9-12 | READY |
| **Total** | **20** | **88** | **3** | **12 days** | **READY_TO_BUILD** |

Important boundary:

```json
{
  "runtime_items_complete": 0,
  "docs_schema_receipts_complete": true,
  "authority": false
}
```

No runtime artifact is marked complete without a repository receipt.

---

## Phase A: Schemas

Purpose: define all data structures before implementation.  
Gate condition: all schemas validate with Ajv against valid and invalid fixtures.

| task_id | queue_id | artifact_path | est_hours | prerequisite_receipts | completion_receipt | rollback_plan |
|---|---|---|---:|---|---|---|
| T-A-01 | Q-001 | `schemas/adn_event.v1.schema.json` | 2 | none | Ajv valid/invalid fixture receipt | revert commit |
| T-A-02 | Q-002 | `schemas/adn_game_state.v1.schema.json` | 2 | T-A-01 | Ajv replay-output fixture receipt | revert commit |
| T-A-03 | Q-003 | `schemas/segment_manifest.v1.schema.json` | 2 | none | Ajv manifest fixture receipt | revert commit |
| T-A-04 | Q-004 | `schemas/snapshot.v1.schema.json` | 2 | T-A-02 | Ajv snapshot fixture receipt | revert commit |

Phase A verification gate:

```bash
npm run validate:schemas
```

Expected receipt:

```txt
PHASE_A_COMPLETE
```

---

## Phase B: Replay Core

Purpose: implement core replay engine components.  
Gate condition: deterministic replay tests pass.

| task_id | queue_id | artifact_path | est_hours | prerequisite_receipts | completion_receipt | rollback_plan |
|---|---|---|---:|---|---|---|
| T-B-01 | Q-005 | `src/anti_drift_news/events.ts` | 4 | T-A-01 | TypeScript compile receipt | revert commit |
| T-B-02 | Q-006 | `src/anti_drift_news/canonicalizer.ts` | 4 | T-A-01 | hash fixture test receipt | revert commit |
| T-B-03 | Q-007 | `src/anti_drift_news/replay.ts` | 8 | T-A-02, T-B-01, T-B-02 | replay determinism test receipt | revert commit |
| T-B-04 | Q-008 | `src/anti_drift_news/segment_reader.ts` | 4 | T-A-03, T-B-02 | segment hash verification receipt | revert commit |

Phase B verification gate:

```bash
npm run test:core
```

Expected receipt:

```txt
PHASE_B_COMPLETE
```

---

## Phase C: Tests

Purpose: achieve executable coverage for documented edge cases.  
Gate condition: edge-case tests pass.

| task_id | queue_id | artifact_path | est_hours | prerequisite_receipts | completion_receipt | rollback_plan |
|---|---|---|---:|---|---|---|
| T-C-01 | Q-009 | `tests/anti_drift_news/replay_engine_v1.test.ts` | 6 | T-B-03 | replay tests pass | delete/revert test file |
| T-C-02 | Q-010 | `tests/anti_drift_news/event_schema_edge_cases_v1.test.ts` | 8 | T-A-01, T-B-03 | edge-case tests pass | delete/revert test file |
| T-C-03 | Q-011 | `tests/anti_drift_news/replay_anomaly_v1.test.ts` | 4 | T-B-03, existing anomaly schema | anomaly tests pass | delete/revert test file |
| T-C-04 | Q-012 | `scripts/assert-event-order-determinism.js` | 6 | T-B-03 | repeated deterministic replay receipt | revert script |

Phase C verification gate:

```bash
npm run test:anti-drift
node scripts/assert-event-order-determinism.js
```

Expected receipt:

```txt
PHASE_C_COMPLETE
```

---

## Phase D: Replay Client

Purpose: complete open-source verification client.  
Gate condition: all required CLI commands exist and pass mock verification.

| task_id | queue_id | artifact_path | est_hours | prerequisite_receipts | completion_receipt | rollback_plan |
|---|---|---|---:|---|---|---|
| T-D-01 | Q-013 | `clients/adn_replay_client_v1/package.json` | 2 | T-B-03 | package install/build receipt | revert client folder |
| T-D-02 | Q-014 | `clients/adn_replay_client_v1/src/cli.ts` | 6 | T-D-01 | CLI help and command tests | revert cli |
| T-D-03 | Q-015 | `clients/adn_replay_client_v1/src/manifest_loader.ts` | 4 | T-A-03, T-B-02 | manifest verification tests | revert file |
| T-D-04 | Q-016 | `clients/adn_replay_client_v1/src/snapshot_generator.ts` | 4 | T-A-04, T-B-03 | snapshot hash tests | revert file |

Phase D verification gate:

```bash
cd clients/adn_replay_client_v1
npm run build
npm test
./bin/adn --help
```

Expected receipt:

```txt
PHASE_D_COMPLETE
```

---

## Phase E: Deployment

Purpose: make public verification available outside the repo.  
Gate condition: public endpoints return valid, independently verifiable receipts.

| task_id | queue_id | artifact_path | est_hours | prerequisite_receipts | completion_receipt | rollback_plan |
|---|---|---|---:|---|---|---|
| T-E-01 | Q-017 | public manifest endpoint | 4 | T-D-03 | curl returns valid manifest | remove endpoint |
| T-E-02 | Q-018 | immutable event segment storage | 6 | T-B-04, T-E-01 | segment hash matches manifest | rollback storage path |
| T-E-03 | Q-019 | root manifest anchor | 4 | T-E-01, T-E-02 | anchor receipt recorded | publish revocation/rollback note |
| T-E-04 | Q-020 | public client release | 6 | T-D-01 through T-D-04 | install and verify command receipt | unpublish/deprecate release |

Phase E verification gate:

```bash
adn verify --game-id ADN-000001 --server <public-endpoint>
```

Expected receipt:

```txt
PHASE_E_COMPLETE
```

---

## Dependency Timeline

```txt
Day 1-2: Phase A schemas
Day 2-4: Phase B replay core
Day 4-7: Phase C tests
Day 7-9: Phase D replay client
Day 9-12: Phase E public verification deployment
```

---

## Critical Path

```txt
T-A-01 -> T-B-01 -> T-B-02 -> T-A-02 -> T-B-03 -> T-C-01/T-C-04 -> T-D-01 -> T-D-02 -> T-E-04
```

No step may begin unless prerequisite receipts exist.

---

## Parallel Work Lanes

Lane 1: Event schema → events → canonicalizer → replay core  
Lane 2: Segment manifest schema → segment reader → manifest loader  
Lane 3: Snapshot schema → snapshot generator  
Lane 4: Tests after replay core receipt  
Lane 5: Deployment after client and manifest receipts

---

## Verification Gates

| Gate | Phase | Command | Pass Criteria |
|---|---|---|---|
| G-01 | A | `npm run validate:schemas` | all schemas valid |
| G-02 | B | `npm run test:core` | replay core tests pass |
| G-03 | C | `npm run test:anti-drift` | edge/anomaly tests pass |
| G-04 | D | `npm run build && npm test` | client builds and tests pass |
| G-05 | E | `adn verify --game-id ADN-000001` | public state verifies |

---

## Merge Gates

| Gate | Condition | Target |
|---|---|---|
| M-01 | G-01 complete | schema PR merge |
| M-02 | G-02 complete | replay core PR merge |
| M-03 | G-03 complete | test hardening PR merge |
| M-04 | G-04 complete | replay client PR merge |
| M-05 | G-05 complete | production verification release |

---

## Production Gates

| Gate | Requirement | Rollback Condition |
|---|---|---|
| P-01 | public manifest validates | manifest mismatch |
| P-02 | segment hashes match manifest | segment corruption |
| P-03 | public replay client verifies game state | state hash mismatch |
| P-04 | root manifest anchor receipt exists | anchor missing or wrong hash |

---

## Completion Receipts Registry

| Receipt | Tasks | Verification |
|---|---|---|
| PHASE_A_COMPLETE | T-A-01 through T-A-04 | schema validation |
| PHASE_B_COMPLETE | T-B-01 through T-B-04 | core replay tests |
| PHASE_C_COMPLETE | T-C-01 through T-C-04 | edge/anomaly tests |
| PHASE_D_COMPLETE | T-D-01 through T-D-04 | client build/tests |
| PHASE_E_COMPLETE | T-E-01 through T-E-04 | public verification |

---

## Rollback Procedures

Task-level rollback:

```bash
git revert <task_commit> --no-commit
git commit -m "rollback: <task_id> - <reason>"
```

Phase-level rollback:

```bash
git revert <phase_start_commit>..<phase_end_commit> --no-commit
git commit -m "rollback: <phase_name> - <reason>"
```

Production rollback must publish a public rollback receipt.

---

## Next Actions

Immediate next build:

1. T-A-01 — `schemas/adn_event.v1.schema.json`
2. T-A-02 — `schemas/adn_game_state.v1.schema.json`
3. T-A-03 — `schemas/segment_manifest.v1.schema.json`
4. T-A-04 — `schemas/snapshot.v1.schema.json`

Blocked items: none.  
Runtime completion: not yet started.

---

## Canon

Receipts unlock work.  
Work creates receipts.  
Authority creates neither.

This site does not ask you to trust it.  
It gives you the math to verify it.

Not anti-news.  
Anti-drift.  
Public receipts from day one.
