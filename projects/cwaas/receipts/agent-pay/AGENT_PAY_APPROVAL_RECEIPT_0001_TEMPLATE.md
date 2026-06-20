# AGENT_PAY_APPROVAL_RECEIPT_0001_TEMPLATE

type: AGENT_PAY_APPROVAL_RECEIPT_V1  
status: TEMPLATE_ONLY  
lane: AGENT_PAY  
preview_receipt_id: PREVIEW_1_V2  
approval_id: APPROVAL_0001

## Purpose

This template defines the receipt shape for a human approval of an Agent Pay preview receipt.

It does not assert that approval has occurred.  
It does not execute payment.  
It does not call Coinbase.  
It does not submit a Base transaction.  
It does not claim treasury movement.

## Preview Reference

preview_hash: e4b4f5e46acaef8b5aceb23c9f6f41d085f79cea9ff1ad955cfc0f848e691dc7  
work_id: 1  
developer_basename: jaywisdom.base.eth  
github_identity: jsonwisdom  
proposed_amount: 0 (preview)  
asset: USDC

## Approval Details

approval_command: /approve-agent-pay  
approver: <github_handle>  
approval_timestamp_utc: <iso8601>  
approval_source: github-comment-or-file

## Replay Reference

replay_trace_id: TRACE_PREVIEW_1_V2  
replay_trace_path: projects/cwaas/receipts/agent-pay/PREVIEW_1_V2_REPLAY_TRACE.json  
replay_verdict: PASS  
replay_disposition: DRYRUN_READ_ONLY

## Payment Adapter Eligibility

eligibility_status: ELIGIBLE_FOR_PAYMENT_ADAPTER_AFTER_HUMAN_APPROVAL  
payment_execution: PENDING_CONFIRMED_SUBMISSION

notes:
- Human approval must be explicitly granted before this receipt can become active.
- Preview-only path must be preserved.
- No payment is executed by this template.

## Prohibited Claims

This approval receipt template does NOT assert:

- payment execution
- Coinbase transaction
- Base settlement
- EAS witness finality
- financial transfer
- treasury movement
- third-party endorsement

## Boss Brenda Lock

No preview receipt, no approval target.  
No replay PASS, no approval target.  
No human approval, no payment adapter eligibility.  
No transaction witness, no confirmed payment.  
No fake green.
