# AGENT_ACTION_RECEIPT_V1

Status: DRAFT_LOCKED  
Lane: CWaaS / Agent Governance  
Depends on:
- RECEIPT_SCHEMA_V1
- TREASURY_GATE_V0_2
- REPLAY_TRACE_FORMAT_V1
- BASE_ATTESTATION_FLOW_V1

## 1. Purpose

Agent Action Receipt defines the minimum admissible record for any AI agent, automation, script, MCP tool, or treasury-adjacent process operating inside CWaaS.

A model response is not an action receipt.  
A tool call is not an action receipt.  
A claimed outcome is not an action receipt.

Only a structured, hashable, replay-verifiable record can become authority.

## 2. Core Invariant

```text
AGENT_INTENT + TOOL_SURFACE + INPUTS + POLICY_GATE + RESULT
  → RECEIPT
  → HASH
  → REPLAY_TRACE
  → VERDICT
```

No agent action may be marked green unless the receipt proves what was requested, what was allowed, what happened, and what did not happen.

## 3. Required Fields

```yaml
receipt_version: AGENT_ACTION_RECEIPT_V1
receipt_id: AGENT_ACTION_0001
receipt_type: AGENT_ACTION

agent:
  agent_id: COMPUTERWISDOM-AGENT-01
  agent_name: <agent_name>
  agent_surface: CHATGPT|MCP|SCRIPT|GITHUB_ACTION|MANUAL_OPERATOR|OTHER
  operator: <github_user_or_human_operator>

intent:
  requested_action: <plain_language_action>
  action_class: READ|WRITE|PREVIEW|EXECUTE|ATTEST|VERIFY|REJECT
  user_authorized: true|false
  human_approval_required: true|false
  human_approval_status: APPROVED|DENIED|NOT_REQUIRED|MISSING

execution:
  tool_surface: COINBASE_MCP|GITHUB|BASE|AL|LOCAL_SCRIPT|NONE|OTHER
  execution_state: NONE|PREVIEWED|EXECUTED|BLOCKED|FAILED|REJECTED
  command_or_call_hash: <sha256|null>
  input_hash: <sha256|null>
  output_hash: <sha256|null>

policy:
  schema_version: RECEIPT_SCHEMA_V1
  treasury_gate_version: TREASURY_GATE_V0_2|null
  replay_trace_required: true
  base_attestation_allowed: true|false

result:
  status: PASS|FAIL|DRIFT|BLOCKED|REJECTED
  failure_class: <failure_class|null>
  disposition: SETTLED|QUARANTINED|NEEDS_REVIEW|REJECTED|BLOCKED

lineage:
  previous_receipt_hash: <sha256|null>
  receipt_hash: <sha256>
  github_commit: <commit_sha|null>
  replay_trace_id: <trace_id|null>
  base_attestation_uid: <uid|null>

timestamp_utc: <iso8601>
notes: <bounded_human_notes|null>
```

## 4. Allowed Action Classes

```text
READ
WRITE
PREVIEW
EXECUTE
ATTEST
VERIFY
REJECT
```

## 5. Treasury Rule

Any Coinbase-connected action must obey:

```text
If action_class = EXECUTE
then human_approval_required = true
and human_approval_status = APPROVED
and treasury_gate_version = TREASURY_GATE_V0_2
```

If this is not true:

```text
status = BLOCKED
failure_class = MISSING_HUMAN_APPROVAL
execution_state = BLOCKED
```

## 6. Preview Rule

Preview actions may inspect, quote, simulate, or prepare an action, but may not move funds.

```text
action_class = PREVIEW
execution_state = PREVIEWED|NONE
```

A preview receipt may never imply execution.

## 7. Read-Only Rule

Read-only actions may inspect state but may not mutate GitHub, Base, Coinbase, AL, or local receipt history.

```text
action_class = READ
execution_state = NONE
```

## 8. Write Rule

Write actions may mutate GitHub files, receipt ledgers, or local artifacts only when the target surface and operator are declared.

Required for WRITE:

```text
tool_surface != NONE
command_or_call_hash != null
output_hash != null
```

## 9. Prohibited Claims

An Agent Action Receipt may not claim:

```text
Coinbase endorsement
Base endorsement
GitHub endorsement
funds moved without execution evidence
human approval without approval evidence
settlement without replay trace
PASS with missing required checks
```

## 10. Replay Binding

Every settled agent action must produce or reference a replay trace.

```text
status = PASS
and disposition = SETTLED
requires replay_trace_id != null
```

If no replay trace exists:

```text
status != PASS
```

## 11. Base Attestation Binding

A Base attestation may only be attached after replay verification.

```text
base_attestation_uid != null
requires replay_trace_id != null
and status = PASS
and disposition = SETTLED
```

Base anchors the result.  
Base does not replace replay.

## 12. Example

```yaml
receipt_version: AGENT_ACTION_RECEIPT_V1
receipt_id: AGENT_ACTION_0001
receipt_type: AGENT_ACTION

agent:
  agent_id: COMPUTERWISDOM-AGENT-01
  agent_name: cwaas-coinbase-reader
  agent_surface: MCP
  operator: jsonwisdom

intent:
  requested_action: Inspect Coinbase BTC-USD product data
  action_class: READ
  user_authorized: true
  human_approval_required: false
  human_approval_status: NOT_REQUIRED

execution:
  tool_surface: COINBASE_MCP
  execution_state: NONE
  command_or_call_hash: sha256:example
  input_hash: sha256:example
  output_hash: sha256:example

policy:
  schema_version: RECEIPT_SCHEMA_V1
  treasury_gate_version: TREASURY_GATE_V0_2
  replay_trace_required: true
  base_attestation_allowed: true

result:
  status: PASS
  failure_class: null
  disposition: SETTLED

lineage:
  previous_receipt_hash: null
  receipt_hash: sha256:example
  github_commit: <commit_sha>
  replay_trace_id: TRACE_0001
  base_attestation_uid: null

timestamp_utc: 2026-06-19T00:00:00Z
notes: Read-only inspection. No funds moved. No order placed.
```

## 13. Boss Brenda Lock

```text
No declared intent, no action receipt.
No tool surface, no authority.
No human approval, no treasury execution.
No replay trace, no settlement.
No endorsement by implication.
No fake green.
```
