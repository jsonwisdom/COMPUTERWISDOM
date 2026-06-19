# AGENT_PAY_CONFIRMED_PAYMENT_RECEIPT_0001_TEMPLATE

type: AGENT_PAY_CONFIRMED_PAYMENT_RECEIPT_V1  
status: TEMPLATE_ONLY  
lane: AGENT_PAY / CONFIRMED_PAYMENT  
preview_receipt_id: PREVIEW_1_V2  
approval_id: APPROVAL_0001  
payment_receipt_id: PAYMENT_0001  

## Purpose

This template defines the required receipt for a confirmed Agent Pay payment event.

It activates only after a real transaction witness exists.

This template does not claim that payment has occurred.

## Required Preconditions

- Preview receipt exists
- Preview replay trace is PASS
- Human approval receipt exists
- `/approve-agent-pay` was issued by a human
- Payment adapter execution was explicitly authorized
- Transaction witness exists
- Confirmed receipt hash is computed

## Preview Reference

preview_receipt_path: projects/cwaas/receipts/preview-dispatch/PREVIEW_1_V2.json  
preview_hash: 9a9ffe769241b85b2561917988c56454437eed786286317bce94a1ff3a32344b  
work_id: 1  
developer_basename: jaywisdom.base.eth  
github_identity: jsonwisdom  
asset: USDC  

## Approval Reference

approval_command: /approve-agent-pay  
approval_receipt: AGENT_PAY_APPROVAL_RECEIPT_0001  
approver: <github_handle>  
approval_timestamp_utc: <iso8601>  

## Payment Witness

payment_adapter: <coinbase_or_base_adapter>  
network: base-mainnet  
transaction_hash: <required_real_tx_hash>  
transaction_timestamp_utc: <iso8601>  
from_identity: <operator_or_treasury_identity>  
to_identity: <developer_basename_or_wallet>  
amount: <decimal>  
asset: USDC  

## Replay Reference

payment_replay_trace_id: <trace_id>  
payment_replay_verdict: PASS  
payment_replay_disposition: SETTLED  

## Confirmed Receipt Hash

confirmed_payment_receipt_hash: <sha256>  

## Prohibited Claims

This receipt must not claim:

- payment without transaction witness
- Coinbase endorsement
- Base endorsement
- GitHub endorsement
- legal approval
- identity verification by third parties
- treasury authority beyond the signed/approved payment event

## Boss Brenda Lock

No preview receipt, no approval target.  
No human approval, no payment adapter eligibility.  
No transaction witness, no confirmed payment.  
No replay trace, no settlement.  
No endorsement by implication.  
No fake green.
