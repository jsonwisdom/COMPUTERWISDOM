# JOY ALMS Base MCP Plugin V0.1

## Doctrine Preamble V0.1

Binary systems decide too soon.  
Trinity systems preserve replay.

A claim must be allowed to stand.  
A challenge must be allowed to answer.  
A witness must be allowed to preserve context.

Memory precedes verdict.  
Continuity precedes closure.  
Authority remains false.

Installation semantics: non-binding, non-authoritative, non-executing, non-promotional, non-merging, non-review-advancing.

Status: DRAFT_AGENT_PLUGIN_SPEC
Authority: false
Mutation model: append-only
Membrane: HOLDS

> IMPORTANT: Complete Base MCP onboarding before using this plugin. The user wallet address must be detected through the Base MCP wallet flow before preparing calldata.

## Purpose

This plugin teaches an assistant how to use the JOY/ALMS Base MCP adapter without granting the plugin authority. The plugin prepares unsigned calldata and maps it to Base MCP `send_calls`.

This document is a child of:

- `base-mcp-agent-ecology-v0-1.json`
- `docs/COMPUTERWISDOM_EPISTEMIC_STACK_V0_1.md`
- `docs/base_mcp/joy_alms_base_mcp_plugin_openapi_v0_1.yaml`
- AL parent witness and action receipt schemas

## Role split

```json
{
  "plugin_role": "untrusted_compiler",
  "wallet_role": "approval_boundary",
  "base_mcp_role": "transport_runtime",
  "chain_role": "receipt_surface",
  "authority": false
}
```

## Read endpoint

```text
GET /state/{address}?limit=50&cursor=<optional>
```

Returns receipt DAG state for UI rendering. It does not decide truth.

## Prepare endpoints

```text
GET /prepare/anchor?from=<address>&claim=<claim>&evidence_uri=<uri>&content_sha256=<hash>&dry_run=false
GET /prepare/dispute?from=<address>&target_claim_hash=<hash>&dispute_type=<type>&reason_uri=<uri>&reason_sha256=<hash>
GET /prepare/witness?from=<address>&target_type=<CLAIM|DISPUTE>&target_hash=<hash>&witness_position=<position>&witness_uri=<uri>&witness_sha256=<hash>&reputation_stake=0x0
```

Allowed truth statuses:

```json
[
  "CLAIM_ANCHORED_NOT_PROVEN",
  "DISPUTE_RECORDED_NOT_ADJUDICATED",
  "WITNESS_RECORDED_NOT_VERDICT"
]
```

Blocked statuses:

```json
[
  "VERIFIED",
  "FALSE",
  "FRAUD",
  "ADJUDICATED"
]
```

## send_calls mapping

Prepare responses include both `transactions` and `send_calls`. Use `send_calls` directly when invoking Base MCP.

```json
{
  "chain": "base",
  "calls": [
    {
      "to": "0xALMS_CONTRACT_PLACEHOLDER",
      "value": "0x0",
      "data": "0xNOT_EXECUTABLE_PLACEHOLDER"
    }
  ]
}
```

The placeholder above is not executable and must never be broadcast.

## Orchestration

1. Complete Base MCP onboarding and wallet detection.
2. Read state if needed.
3. Call one prepare endpoint.
4. Validate `authority: false` and allowed `truth_status`.
5. Pass the returned `send_calls.calls` to Base MCP.
6. User approves in wallet.
7. Verify chain receipt after execution.

## Final invariant

```json
{
  "mutation_model": "append_only",
  "plugin_can_execute": false,
  "wallet_must_approve": true,
  "authority": false,
  "membrane": "HOLDS"
}
```
