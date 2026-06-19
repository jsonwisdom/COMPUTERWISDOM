# Workflow Engine v0.1

Leaf: LEAF_003_PUBLIC_MEMORY_DRIFT_OBSERVATORY_V0_1  
Game: Public Receipt Arcade  
Status: Draft  
Authority: false  
Fraud status: UNKNOWN

## Purpose

Turn completed Work Items into the next Work Item deterministically.

The workflow engine makes the dashboard executable.

It reads current state, verifies artifacts, applies the transition table, and creates the next file.

No AI guesses the next move.

## Inputs

- `dashboard.json`
- `last_work_item.json`
- `artifacts/` folder listing
- `intent_ref`

The `intent_ref` is the mission hash and never changes during a workflow chain.

## Outputs

- `next_work_item.json`
- `updated_dashboard.json`
- `engine_log.txt`

## Transition Table

The transition table is the law.

```text
hash_pdf + completed -> create_receipt assigned to ChatGPT
create_receipt + completed -> replay_check assigned to Claude
replay_check + completed -> courts_click assigned to Jay
courts_click + completed -> drop_quarter assigned to Jay
drop_quarter + completed -> render_card assigned to Meta
```

## Failure Rules

If `current_status` is not `completed`, the engine stops.

No next Work Item is generated.

The dashboard continues showing current work as in progress.

If `current_status` is `blocked`, the engine stops and copies `blocked_reason` to the log.

The operator must fix the input and reset status to `assigned`.

If `output_artifact` is missing, the engine creates a blocked next item:

```json
{
  "status": "blocked",
  "blocked_reason": "missing artifact"
}
```

The dashboard records the missing output.

If `sha256` does not match, the engine creates a blocked next item:

```json
{
  "status": "blocked",
  "blocked_reason": "sha256 mismatch"
}
```

## Example Execution

Input:

```text
wi-003 replay_check completed by Claude
```

Engine reads the transition table:

```text
replay_check + completed -> courts_click assigned to Jay
```

Output:

```text
wi-004 courts_click assigned to Jay
```

Engine log:

```text
read wi-003 status completed, matched transition to courts_click, verified artifact exists, created wi-004 assigned to Jay
```

## Safety Membrane

```json
{
  "deterministic_next_action": true,
  "ai_guessing_next_action": false,
  "artifact_verification_required": true,
  "missing_artifact_blocks": true,
  "sha256_mismatch_blocks": true,
  "authority": false,
  "fraud_status": "UNKNOWN"
}
```

## Closing Rule

The workflow engine does not decide truth.

It decides the next task.

Authority remains false.
