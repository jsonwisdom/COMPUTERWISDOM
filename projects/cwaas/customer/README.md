# CUSTOMER_RECEIPT_SCHEMA_V0_1

Schema object only. Not canon. Not authority. Not a customer receipt.

```text
CANON             = false
AUTHORITY_CREATED = false
EXECUTION         = NONE
MERGE             = NONE
DRIVE_WRITE       = false
CUSTOMER_RECEIPTS = 0
PAID_CUSTOMER_EVIDENCE      = NOT_ESTABLISHED
COMMITTED_CUSTOMER_EVIDENCE = NOT_ESTABLISHED
WILLINGNESS_TO_PAY          = NOT_ESTABLISHED
PROVEN_DEMAND               = NOT_ESTABLISHED
```

## What this is

A customer-side receipt grammar. It records payment, commitment, and permission to speak as separate fields. It does not create any of them.

## What this is not

- Not `projects/cwaas/specs/RECEIPT_SCHEMA_V1.md` (blob `bc08c2374589f9fb4a1894ec3e40d6fcc793ee03`). That file is the generic structured receipt primitive, including Coinbase read-only / preview boundaries.
- Not `projects/cwaas/receipts/CWAAS_RECEIPT_SCHEMA_v1.md` (blob `9eb2ddbf42f3d523e89e42042791f3922cd77395`). That file says a receipt does not create payment authority.
- Not `receipts/sales/SALE_VERIFY_0001.canonical.json` (blob `cb3097efa818c450f6aae699a22ee6106f6850b2`). That object has `payment_status: NOT_ROUTED` and does not define commitment semantics.
- Not the Coinbase 01–04 rail. `05_ORDERS` is not opened here.

Repo search on 2026-10-02 returned no `CUSTOMER_SIDE_RECEIPTS` and no `COMMITMENT_STATUS` in `jsonwisdom/COMPUTERWISDOM`. Search miss is not proof of absence outside that search.

## Membrane

```text
PAYMENT_STATUS ≠ COMMITMENT_STATUS
COMMITMENT_STATUS > INTEREST → COMMITMENT_ARTIFACT_REF REQUIRED
PAYMENT ⇏ CLAIM_ALLOWED
PAYMENT ⇏ TESTIMONIAL_ALLOWED
PUBLIC_CLAIM_SCOPE = NAMED    → CLAIM_ALLOWED = TRUE
PUBLIC_CLAIM_SCOPE = VERBATIM → TESTIMONIAL_ALLOWED = TRUE
REPO_RECEIPT ≠ CUSTOMER_RECEIPT
ONE_CUSTOMER ≠ MARKET_SIZE
```

No field upgrades another. A filled example in this directory would still be a schema fixture, not a customer receipt.
