# AGENT_ACTION_RECEIPT_V0_1

Status: SCHEMA_FIRST  
Issue: #86  
Parent: #67  
Authority: false  
Membrane: HOLDS

## Purpose

`AGENT_ACTION_RECEIPT_V0_1` records bounded agent actions in the Constitutional Game Stack v0.2.

It records what an agent did, what inputs it used, what output it produced, and which receipts support the action.

It does not authorize agents, grant autonomous merge rights, create wallet signing authority, or turn agent outputs into truth.

## Allowed Agent Actions

- `observe_public_claim`
- `summarize_context`
- `propose_case_intake`
- `draft_spec`
- `prepare_anchor_payload`
- `produce_runtime_log`
- `open_dispute_state`
- `emit_boundary_observation`

## Required Fields

- `action_receipt_id`
- `agent_id`
- `action_type`
- `artifact_ref`
- `input_refs`
- `output_ref`
- `supporting_receipts`
- `authority: false`
- `timestamp_utc`

## Core Rule

Agent action is observable. Agent action is not authority.

## Forbidden Promotions

- Agent action to verified truth
- Agent action to legal conclusion
- Agent action to wallet signing authority
- Agent action to ENS/Base authority
- Agent action to autonomous merge authority
- Agent action to human approval

## Closing Rule

Agents play. Receipts replay. Humans merge. Authority remains false.
