# MN State Snapshot v0.1

Author: Jay Wisdom  
Repo: jsonwisdom/COMPUTERWISDOM  
Branch: feature/leaf-003-memory-drift-schema-v0-1  
Purpose: Recover Minnesota / Saint Cloud operator state after chat reset  
Authority: false  
Fraud status: UNKNOWN

## Why This Exists

Jay works on this build every day.

Chat resets break operator state.

This snapshot preserves the current Minnesota / Saint Cloud game build so future chats can recover from repo artifacts instead of forcing Jay to reconstruct memory.

## Operator Problem

When state lives only in chat:

```text
prompt -> response -> prompt -> response -> scroll -> lost state
```

This harms:

- the operator
- the builder
- the game
- the repo
- the receipt chain

The fix is persistent state:

```text
intent -> work item -> artifact -> receipt -> dashboard -> next work item
```

## Current Leaf Stack

```json
{
  "leaf_001": "Minnesota Budget Forecast Foundation",
  "leaf_002": "MN Anomaly Framework / MN portal bootstrap",
  "leaf_003": "Public Memory Drift Observatory / Public Receipt Arcade",
  "leaf_004": "Drift Resolution Protocol",
  "leaf_005": "Saint Cloud Public Agenda Drift Pilot",
  "authority": false,
  "fraud_status": "UNKNOWN"
}
```

## Active GitHub Surfaces

- Issue #97: LEAF_005 — Saint Cloud Public Agenda Drift Pilot
- Issue #96: LEAF_004 — Drift Resolution Protocol v0.1
- PR #95: Leaf #003: Public Receipt Arcade MVP schema and game docs
- PR #93: Leaf #002: Add MN anomaly portal bootstrap + replay vectors

## Minnesota / Saint Cloud Scan Result

Connector scan found broad MN-related artifacts, but did not find a completed Saint Cloud public agenda receipt system by exact name.

### Found MN-related artifacts

- `receipts/drafts/MN_MITCHELL_MCRO_REGISTER_OF_ACTIONS_RECEIPT_V0_1_WITH_NAVIGATOR.html`
- `angie-act/README.md`
- `angie-act/README_COMPARISON.md`
- `angie-act/schema/angie_act.schema.json`
- `angie-act/examples/claim_001.clean.json`
- `angie-act/examples/hf4122_kraft_xcel.watch.json`
- `angie-act/examples/hf4122_kraft_xcel_influence_flagged.json`
- `angie-act/examples/hf4122_kraft_xcel_whatif.plausible_not_proven.json`
- `docs/WAVE1_REVIEWER_PACKET_v1_3.md`
- `docs/observer_alignment/INDEX.md`

### Found receipt / replay infrastructure

- `docs/REPLAY_RECEIPT_SPEC_V1.md`
- `scripts/verify_canon_chain_receipt_001.ts`
- `docs/agent_action_receipt_v0_1.md`
- `docs/EXECUTION_RECEIPT_SCHEMA_V1.md`
- `docs/protocols/manic/replay/generate_deterministic_receipt.js`
- `docs/protocols/manic/validators/validate_deterministic_receipt.js`
- `schemas/agent_action_receipt.v0_1.schema.json`
- `schemas/replay_score_receipt.v0_1.schema.json`
- `schemas/classification_receipt.v0_1.schema.json`

### Found crawler-adjacent artifact

- `services/zora-flywheel/factory_crawler_spec_candidate.md`

This is not a confirmed Saint Cloud public-record agenda crawler.

## Current Reuse Verdict

```json
{
  "saint_cloud_public_agenda_system_found": false,
  "mn_related_artifacts_found": true,
  "receipt_replay_infrastructure_found": true,
  "crawler_reuse": "PARTIAL_NON_AGENDA_ONLY",
  "leaf_005_reuse_decision": "REUSE_RECEIPT_PATTERNS_MANUAL_FIRST",
  "authority": false,
  "fraud_status": "UNKNOWN"
}
```

## Leaf 005 State

Leaf #005 exists to move from internal workflow drift to public-memory drift.

Target:

```text
City of Saint Cloud public meeting agenda PDF
```

Current work items:

- `examples/work_items/wi-005-hash-agenda.json`
- `examples/work_items/wi-006-create-agenda-receipt.json`

Current status:

```json
{
  "leaf_005": "PENDING_REAL_EVIDENCE",
  "missing": [
    "real source_url",
    "observed_at timestamp",
    "sha256 hash",
    "file_name",
    "byte_size"
  ],
  "next_operator_action": "Jay manually downloads agenda PDF and records evidence fields",
  "crawler": "DISABLED",
  "authority": false,
  "fraud_status": "UNKNOWN"
}
```

## Manual Evidence Instructions

Current manual evidence doc:

```text
docs/operator/LEAF_005_MANUAL_EVIDENCE_INSTRUCTIONS.md
```

Jay must collect:

- `source_url`
- `observed_at`
- `sha256`
- `file_name`
- `byte_size`

No invented URL.  
No invented hash.  
No invented timestamp.

## Game State

The current game is Public Receipt Arcade.

Core loop:

```text
Quest -> Public Record -> Snapshot -> Hash -> Receipt -> Replay -> Court Check -> Reward -> Dashboard
```

MVP target:

```text
Saint Cloud Loon Cabinet
```

MVP rule:

```text
One cabinet. One town. One receipt. One replay. One quarter.
```

## Built Game Docs In PR #95

- `docs/game/game_of_growth_v0_1.md`
- `docs/game/governance_by_joystick_v0_1.md`
- `docs/game/three_courts_multi_vector_v0_1.md`
- `docs/game/three_courts_reputation_v0_1.md`
- `docs/game/quest_rewards_v0_1.md`
- `docs/game/first_10_minutes_v0_1.md`
- `docs/game/minnesota_map_v0_1.md`
- `docs/game/cabinet_system_v0_1.md`
- `docs/game/player_hud_v0_1.md`
- `docs/game/mvp_build_order_v0_1.md`

## Workflow / Operator Architecture Built In PR #95

- `schemas/work_item.v0_1.schema.json`
- `schemas/workflow_dashboard.v0_1.schema.json`
- `schemas/drift_resolution.v0_1.schema.json`
- `examples/work_items/wi-001-hash-pdf.json`
- `examples/work_items/wi-002-create-receipt.json`
- `examples/work_items/wi-003-replay-check.json`
- `examples/work_items/wi-004-courts-click.json`
- `examples/work_items/wi-004-v2-courts-click.json`
- `examples/work_items/wi-005-hash-agenda.json`
- `examples/work_items/wi-006-create-agenda-receipt.json`
- `examples/work_items/lineage-example.json`
- `examples/workflow_dashboard/dashboard-example.json`
- `examples/workflow_dashboard/dashboard-resolved-example.json`
- `docs/operator/workflow_engine_v0_1.md`

## Drift / Resolution Artifacts

- `receipts/memory/leaf_003_drift_receipt_001.json`
- `examples/drift_resolutions/res-20250601-001.json`

## Current Physics Rule

If the data shows a mismatch, the system records it as drift.

```json
{
  "suspicion": "NOT_A_VERDICT",
  "observable_drift": "RECEIPT_ELIGIBLE",
  "history": "LIVE_IF_HASHED_AND_REPLAYABLE",
  "public_tools": true,
  "authority": false,
  "fraud_status": "UNKNOWN"
}
```

The public can see tools, means, records, and receipts of history.

The system does not declare fraud.

It exposes replayable evidence.

## Next Operator Action

Jay should complete Leaf #005 evidence collection:

1. Open official City of Saint Cloud agenda page.
2. Download agenda PDF manually.
3. Record `source_url`.
4. Record `observed_at` in ISO8601 UTC.
5. Compute SHA-256.
6. Record `file_name`.
7. Record `byte_size`.
8. Paste the values into ChatGPT.

Then create:

```text
receipts/memory/public_agenda_receipt_001.json
```

## Do Not Do Yet

- Do not build crawler.
- Do not invent URL.
- Do not invent hash.
- Do not invent timestamp.
- Do not declare fraud.
- Do not merge PR #95 as complete until review/verify.

## Closing Rule

Jay should never again have to reconstruct the Minnesota game state from chat.

Load this file first.

Authority remains false.
Fraud status remains UNKNOWN.
