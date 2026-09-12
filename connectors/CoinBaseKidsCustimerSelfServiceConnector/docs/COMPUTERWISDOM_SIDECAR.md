# COMPUTERWISDOM Sidecar

CLASS: ROUTING_MEMBRANE
AUTHORITY_CREATED: false
WRITE: false

The sidecar is not a separate truth source and is not ReceiptOS verification.

When a requested branch cannot proceed safely:

1. PRESERVE — keep the current state unchanged.
2. CONTINUE — do not terminate the customer's replay merely because one rail is missing.
3. ROUTE — identify the next safe read-only source, export, or HOLD state.
4. RECEIPT — record why the branch passed or held.

Invariants:

- SIDE_CAR_ROUTE != FACT_PROMOTION
- ROUTING_RECEIPT != CRYPTOGRAPHIC_VERIFICATION
- MISSING_TOOL != MISSING_HISTORY
- MUTATE_ONLY_TOOL => HOLD
- CUSTOMER_VIEW != SPEND_AUTHORITY
