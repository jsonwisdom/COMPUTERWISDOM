# Minnesota Quad Onion Ledger Schema v0.1

Status: DRAFT / MACHINE-CHECKABLE / SOURCE-BOUND / UNMERGED

```text
BOXD = INSTITUTIONAL REPLAY CONTAINER
MAX_GRAY_BABY = EPISTEMIC / DRIFT-CHECK EXPLAINER
LEELOO_MULTI_PASS = FAIL-CLOSED PROMOTION GATE
AUTHORITY_CREATED = FALSE
LEGAL_FINDING_CREATED = FALSE
BANK_CULPABILITY_CREATED = FALSE
MERCHANT_CULPABILITY_CREATED = FALSE
FOREIGN_NEXUS != FOREIGN_CULPABILITY
```

## Purpose

Convert the Minnesota banking / merchant / foreign-links Quad Onion from narrative into a machine-checkable ledger. Every edge must point to a source receipt and carry its own state.

## Ledger object

```text
LEDGER
├── O1 criminal_receipts[]
├── O2 payment_control_edges[]
├── O3 financial_rail_edges[]
├── O4 oversight_recovery_edges[]
├── cross_onion_edges[]
└── boxd_disposition
```

## O1 — Record / Criminal

Required fields:

```text
case_id
actor_id
actor_type
program
proceeding_type
adjudication_status
conduct_summary
source_receipt_ids[]
state
```

Allowed adjudication states explicitly distinguish allegation from guilt:

```text
CHARGED
PLEADED_GUILTY
CONVICTED_TRIAL
SENTENCED
DISMISSED
ACQUITTED
OTHER
```

Rule:

```text
CHARGED != GUILTY
INVESTIGATED != GUILTY
PLEA / CONVICTION = CASE-BOUND ONLY
```

## O2 — Authority / Payment Control

Required fields:

```text
edge_id
program
payor
approval_actor_or_system
recipient_entity
payment_authority_basis
source_receipt_ids[]
state
```

Optional deep-rail fields include claim ID, payment/remittance ID, approving office, delegated authority, and control flags.

Rule:

```text
PROGRAM_AUTHORITY != CRIMINAL_LIABILITY
PAYOR_NAMED != PAYOR_COMPLICITY
OFFICE_HOLDER != TRANSACTION_ACTOR
```

## O3 — Execution / Financial Rails

Each rail edge has a typed `rail_type`:

```text
BANK_ACCOUNT
CARD
MERCHANT
WIRE
ACH
CHECK
CASH
CRYPTO
ASSET_PURCHASE
PROPERTY
FOREIGN_TRANSFER
OTHER
```

Core fields:

```text
edge_id
case_id
rail_type
origin
counterparty
amount
currency
transaction_date
bank
card_network
merchant
mcc
acquirer
processor_gateway
foreign_destination
asset
source_receipt_ids[]
state
```

Unknown fields remain null/HOLD; they are never inferred from neighboring edges.

Rule:

```text
ACCOUNT_IN_CASE != BANK_WRONGDOING
CARD_NETWORK_NAMED != NETWORK_COMPLICITY
MERCHANT_PAYMENT != MERCHANT_COMPLICITY
FOREIGN_DESTINATION != FOREIGN_CULPABILITY
TRAVEL_DESTINATION != FOREIGN_BANK
```

## O4 — Oversight / Recovery

Required fields:

```text
edge_id
case_id
action_type
actor_or_agency
amount
asset_or_account
order_or_docket_id
source_receipt_ids[]
state
```

Action types include:

```text
INVESTIGATION
SUBPOENA
SEIZURE
FORFEITURE
RESTITUTION
SENTENCE
PROGRAM_FREEZE
PROGRAM_TERMINATION
CONTROL_CHANGE
OTHER
```

Rule:

```text
SEIZURE != FINAL_FORFEITURE
FORFEITURE != FULL_RECOVERY
CORRECTION != ERASURE_OF_PRIOR_FAILURE
```

## Cross-onion joins

```text
O1_TO_O2: criminal event / claim → lawful payment-control path
O2_TO_O3: payment authority → actual money rail
O3_TO_O4: money rail → investigation / recovery trail
O4_TO_O1: correction / adjudication → preserved record delta
```

Each join is independently `PASS | HOLD | CONFLICT | REJECT`.

## Institution finding gate

The ledger may name banks, card networks, processors, merchants, managed-care organizations, foreign recipients, or countries as rail participants. It may not promote any of them to wrongdoing without an explicit finding object:

```text
institution_finding = {
  institution_id,
  finding_type,
  finding_authority,
  source_receipt_ids[],
  state
}
```

No finding object means no culpability promotion.

## LeeLoo Multi Pass

```text
ALL FOUR ONIONS PASS
AND ALL REQUIRED CROSS-EDGES PASS
AND NO UNSOURCED PROMOTIONS
= MULTI_PASS_PASS

ANY HOLD     → MULTI_PASS_HOLD
ANY CONFLICT → MULTI_PASS_CONFLICT
ANY REJECT   → MULTI_PASS_REJECT
```

## Current Minnesota fixture

`MN_QUAD_ONION_LEDGER_HOLD_0001.json` intentionally remains HOLD because the public record does not yet bind a complete merchant/MCC/acquirer/processor ledger, most foreign receiving-bank details, or a complete recovery-vs-loss map.

## Core rule

**FOLLOW THE MONEY WITHOUT PROMOTING THE RAIL INTO THE CRIME.**
