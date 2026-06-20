# AGENT_PAY_REAL_TRANSACTION_WITNESS_SCHEMA_V1.md

status: SCHEMA_ONLY
execution: FALSE

## Purpose

Defines the required shape of a future real Agent Pay transaction witness.

This schema does not record a real witness, confirm payment, authorize execution, call an adapter, move funds, or claim settlement.

## Required Fields For Future Real Witness

```text
transaction_hash: REQUIRED
network: REQUIRED
from_address: REQUIRED
to_address: REQUIRED
asset: REQUIRED
amount: REQUIRED
timestamp: REQUIRED
receipt_hash: REQUIRED
witness_reviewer: REQUIRED
boss_bre_review: REQUIRED
no_fake_green: REQUIRED
```

## Current State

```text
schema_present: true
real_transaction_witness_present: false
confirmed_payment: false
execution_authority: false
adapter_call_allowed: false
payment_execution: false
onchain_movement: false
settlement_claimed: false
no_fake_green: true
```

## Boss Bre Lock

```text
No real witness schema, no real witness review.
No real transaction witness, no confirmed payment.
Schema defines the lane; it does not prove a payment.
No adapter call, no execution.
No onchain movement, no settlement.
No fake green.
```

## Boundary

This artifact defines structure only. It does not authorize anything.
