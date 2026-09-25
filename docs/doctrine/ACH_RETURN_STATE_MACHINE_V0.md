# ACH RETURN STATE MACHINE V0
Date: 2026-09-25
STATUS: LOCAL_WORKING_SHEET
CANON: false
AUTHORITY_CREATED: false

Three facts, not one:
AUTHORIZATION → EXECUTION → FINALITY

R10 fails at authorization.
R11 can pass authorization and fail execution.
A later return can happen after apparent settlement.

LEARNED ≠ CONCLUDED
AUTHORIZED ≠ EXECUTED
SUCCEEDED ≠ FINAL

---

## Receipt ladder

MANDATE_VALID?
↓
ENTRY_CONFORMS?
↓
PAYMENT_SUCCEEDED?
↓
PAYOUT_BANKED?
↓
RETURN_WINDOW_CLOSED?

---

## Split

R10
NO AUTHORIZATION / ORIGINATOR NOT KNOWN
→ STOP
→ DO NOT REINITIATE
→ NEW AUTHORIZATION REQUIRED

R11
AUTHORIZATION EXISTS
BUT ENTRY ≠ AUTHORIZATION (wrong amount, wrong date, or other nonconformance)
→ CORRECT DEFECT
→ MAY RESUBMIT WITHOUT NEW AUTHORIZATION
  if the corrected entry conforms to the existing authorization
  and is originated within the permitted timeframe

---

## $980 machine

AUTHORIZED
→ SUBMITTED
→ PROCESSING
→ SUCCEEDED
→ PAYOUT
→ BANKED

RETURN?
  R01 / R09 → controlled retry lane (reinitiation regulated and limited)
  R02 / R03 / R04 → new account information
  R07 / R10 / R05 / R29 → authorization stop; do not reinitiate on the old mandate
  R08 → stop-payment lane; no automatic reinitiation; human/customer confirmation required
  R11 → fix mismatch, then corrected submission permitted without a new authorization
  R51 → authorization/compliance review; no automatic retry; HOLD pending scheme-specific classification
  OTHER_VALID_R_CODE → NO_AUTO_RETRY → MANUAL_CLASSIFICATION → HOLD
  UNKNOWN_OR_UNMAPPED_CODE → HOLD → SOURCE / SCHEME CHECK REQUIRED

CODE_OBSERVED ≠ CODE_CLASSIFIED ≠ ACTION_AUTHORIZED

Unauthorized entries cannot simply be retried.
R01/R09 may be reinitiated only inside Nacha retry limits.
No fallback lane authorizes retry by itself.

Unauthorized-return monitoring bucket historically: R05, R07, R10, R29, R51.
R11 was subsequently brought into the unauthorized-return-rate framework.
Threshold cited: 0.5% unauthorized. Administrative and overall-return monitoring are separate.
R10 is a COMPLIANCE / AUTHORIZATION EVENT, not a legal-liability finding.
A return code by itself does not establish legal liability or wrongdoing.

---

## Two clocks

PAYMENT_INTENT.SUCCEEDED ≠ SAFE MONEY
STRIPE BALANCE ≠ BANKED
BANKED ≠ IMMUNE FROM RETURN

DID_JASON_MAKE_A_DOLLAR?
  BANKED = TRUE | FALSE | UNKNOWN
DID_JASON_KEEP_THE_DOLLAR?
  RETURN_WINDOW_CLOSED = TRUE | FALSE | UNKNOWN

Until those receipts exist:
MAKE_DOLLAR = HOLD
KEEP_DOLLAR = HOLD
CANON = FALSE
MONEY_IN_PROVEN = $0
