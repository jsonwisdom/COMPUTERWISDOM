# COINBASE_MCP_ADAPTER_DRYRUN_0001_REPLAY_TRACE.md

**CWaaS Coinbase MCP Adapter Dry-Run Replay Trace**

## Header

date: 2026-06-20
reviewer: Boss Bre / jaywisdom.base.eth
status: ADAPTER_DRY_RUN_REPLAY_TRACE_RECORDED
schema: CWAAS_RECEIPT_SCHEMA_v1

## Bound References

adapter_receipt: projects/cwaas/receipts/agent-pay/COINBASE_MCP_ADAPTER_DRYRUN_0001.md
preview_receipt: projects/cwaas/receipts/agent-pay/coinbase-mcp/coinbase_mcp_preview_20260620-030434.json
approval_required_receipt: projects/cwaas/receipts/agent-pay/coinbase-mcp/coinbase_mcp_approval_required_20260620-030434.json
expected_preview_hash: b42dfb20df7a5cffd2cfa352f38ba0c249d573f210e7a096aa91e7346c70b570
recomputed_preview_hash: b42dfb20df7a5cffd2cfa352f38ba0c249d573f210e7a096aa91e7346c70b570
hash_match: true
root_identity: jaywisdom.base.eth

## Replay Method

The committed preview JSON was hashed with SHA-256 using the repository file bytes, including the trailing newline. The recomputed hash matched the hash recorded in the adapter dry-run receipt.

## Replay Result

adapter_dry_run_replay: PASS
preview_hash_match: true
approval_required_present: true
funds_moved: false
chain_action: false
payment_execution: false
external_adapter_call: false
onchain_movement: false
no_fake_green: true

## Boundary

This replay trace verifies the dry-run receipt hash only. It does not execute payment, call an external adapter for settlement, move funds, create settlement finality, or imply Coinbase/Base endorsement.

## Boss Bre Lock

No hash match, no replay green.
No human approval, no adapter execution.
No real witness, no confirmed payment.
No funds moved, no chain action.
No fake green.
