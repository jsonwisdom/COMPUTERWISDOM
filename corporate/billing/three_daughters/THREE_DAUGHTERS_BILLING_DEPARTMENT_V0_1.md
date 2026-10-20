# COMPUTERWISDOM Three Daughters Billing Department v0.1

```yaml
status: DRAFT_OBSERVER_ORGANIZER
audience: COMPUTERWISDOM Family
family_layer: Three Daughters
authority: false
execution: none
default_disposition: HOLD
private_content_in_public_repo: false
```

## Purpose

The Three Daughters Billing Department is a family-safe learning and paperwork-organization layer above the existing CWaaS payment rail.

“Billing Department” is a playful organizational label. It is not an employer, legal office, treasury, bank, collection agency, tax preparer, or grant of corporate authority. No daughter is assigned a job, financial responsibility, account access, signature power, or duty.

The layer organizes public-safe pointers and questions. It never executes payment.

```text
RECEIVE POINTER
-> CLASSIFY
-> PRIVACY GATE
-> MATCH RECEIPTS
-> HUMAN REVIEW
-> WITNESS
-> REPLAY
-> ARCHIVE
```

## Paperwork classes

```text
UNKNOWN
QUOTE
INVOICE
PURCHASE_ORDER
CONTRACT_NOTICE
REIMBURSEMENT_REQUEST
PAYMENT_APPROVAL
PAYMENT_WITNESS
RECEIPT
TAX_RECORD
BANK_RECORD
OTHER
```

The public repository may store schemas, validators, opaque pointers, hashes, and redacted examples only. It must not store invoices, bank statements, tax records, account numbers, addresses, private family records, credentials, or unredacted corporate paperwork.

## Four Onion review

| Lane | Billing question | Fail-closed boundary |
|---|---|---|
| O1 Record / Reality | What document or pointer is actually present? Are amount, date, party, and version supported? | Presence is not legitimacy or amount owed |
| O2 Authority / Law | Who may review, approve, sign, dispute, file, or pay? | Only an explicitly authorized adult/human may act |
| O3 Execution / Resources / Money | Would this spend money, change an account, transmit data, or create an irreversible action? | The family layer has no execution path |
| O4 Oversight / Correction | Can a human stop, correct, dispute, reverse, or replay the classification? | No correction path means HOLD |
| Sidecar Time / Gap / Version | Is the version current? What is missing, stale, duplicated, or conflicting? | UNKNOWN and conflict remain visible |

## Payment separation law

```text
DOCUMENT PRESENT != DOCUMENT VALID
INVOICE PRESENT != AMOUNT OWED
CLASSIFIED != APPROVED
APPROVED != PAYMENT AUTHORIZED
PAYMENT ELIGIBLE != PAYMENT EXECUTED
TRANSACTION HASH != SETTLEMENT BY ITSELF
CI PASS != PAYMENT AUTHORITY
MODEL PASS != HUMAN AUTHORIZATION
```

Existing CWaaS law remains controlling:

1. Preview receipt.
2. Replay-verified preview.
3. Explicit human approval.
4. Payment-adapter eligibility.
5. Explicit execution authorization outside this layer.
6. Real transaction witness.
7. Payment replay receipt.
8. Confirmed payment receipt.

No missing step may be inferred.

## Three blank mirrors

Three blank mirrors are available. They are not assigned to named people.

- Receipt Reader: notices what the document actually says.
- Question Keeper: preserves UNKNOWN, conflicts, and questions.
- Replay Witness: checks whether the receipt chain can be replayed.
- None: pause, refuse, rest, or do something else without penalty.

All mirrors remain `UNASSIGNED` in public artifacts. Any private, session-local participation must be voluntary, age-appropriate, supervised by an authorized adult, and unable to reach accounts, payments, signatures, tax filing, credentials, or private corporate systems.

## Connector boundaries

| Surface | Permitted role | Prohibited inference |
|---|---|---|
| GitHub | Public-safe schemas, validators, CI, hashes, and replay receipts | GitHub is not the truth or payment surface |
| Google Drive | Private paperwork storage and working folders after an exact destination is authorized | Drive presence is not validity, approval, or consent |
| OpenAI / LeeLoo MULTI-PASS | Advisory classification and conflict detection on redacted/public-safe inputs | Model output is not approval, payment authority, or family consent |

Connector accounts are not assumed unified. No connector mutation is authorized by this artifact.

## Organized private folder proposal

This is a naming proposal only; it creates no Drive folders.

```text
COMPUTERWISDOM / Corporate Paperwork /
  00_INBOX
  10_CLASSIFIED
  20_MATCHED_TO_RECEIPTS
  30_HUMAN_REVIEW
  40_APPROVAL_RECEIPTS
  50_PAYMENT_WITNESSES
  60_REPLAYED
  90_HOLD_CONFLICT_UNKNOWN
  99_ARCHIVE
```

## Terminal state

```ini
PAPERWORK_ORGANIZED = SCHEMA_READY
DAUGHTER_IDENTITIES_RECORDED = FALSE
PUBLIC_ROLE_ASSIGNMENTS = 0
ACCOUNT_ACCESS_CREATED = FALSE
PAYMENT_AUTHORIZED = FALSE
PAYMENT_EXECUTED = FALSE
DRIVE_MUTATED = FALSE
MERGE_AUTHORIZED = FALSE
AUTHORITY_CREATED = FALSE
```


