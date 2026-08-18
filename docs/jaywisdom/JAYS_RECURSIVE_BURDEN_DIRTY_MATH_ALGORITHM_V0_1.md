# Jay's Recursive Burden / Dirty Math Algorithm — v0.1

**Operator label:** `jaywisdom.base.eth`  
**Repository lane:** `jsonwisdom/COMPUTERWISDOM` PR #488  
**Classification:** `BOUNDED_CONGRESSIONAL_MONEY_EVIDENCE_ALGORITHM`  
**Authority created:** `false`

## Purpose

Turn burden of proof into a deterministic recursive audit procedure for congressional money claims while preserving the distinction between a state-collapse signal and an allegation of corruption.

```text
DIRTY_MATH = STATE_COLLAPSE_OR_UNRECONCILED_PROVENANCE_SIGNAL
DIRTY_MATH != FRAUD
DIRTY_MATH != INTENT
DIRTY_MATH != MISCONDUCT
```

## Recursive burden kernel

```text
CLAIM C0
  -> SOURCE S0
  -> AUTHORITY A0
  -> ACTION X0
  -> RECEIPT R0
  -> REPLAY

R0 becomes the next bounded claim when further provenance is required:
R0 -> C1 -> S1 -> A1 -> X1 -> R1 -> REPLAY
```

Each recursion node is independently typed. A receipt may support a claim without proving the next receipt's provenance.

Terminal dispositions:

```text
PASS     = all required gates verified and two-direction replay reconciles
HOLD     = required evidence or provenance field absent
CONFLICT = valid bound records disagree or replay directions do not reconcile
REJECT   = bound evidence contradicts the claim or the record attempts an invalid semantic/state promotion
```

Fail-closed reducer precedence:

```text
REJECT > CONFLICT > HOLD > PASS
```

This is the machine form of the weak-link rule. A convenient ordinal representation may be used internally, but the semantic categories remain primary.

## Congressional money-state machine

```text
REQUEST
  != AUTHORIZATION
  != APPROPRIATION
  != APPORTIONMENT
  != ALLOTMENT
  != OBLIGATION
  != OUTLAY
  != EXPENDITURE_RESULT
  != AUDITED_RESULT
```

The algorithm never infers a later state from an earlier state or from a dollar amount alone. GAO public guidance independently distinguishes these budget-execution stages and notes that an OMB apportionment may be further subdivided by an agency into allotments.

Public references:
- https://www.gao.gov/tracking-funds
- https://files.gao.gov/reports/GAO-23-106561/index.html

## Minimum money object

A dollar claim is incomplete without state and provenance. The bounded object is:

```text
VALUE
CURRENCY
STATE
ACCOUNT
PROGRAM
FISCAL_YEAR
AUTHORITY_REF
SOURCE_REF
RECEIPT_REF
```

`NUMBER_WITHOUT_STATE -> HOLD`.

## Dirty Math detector

```text
SAME_NUMBER + DIFFERENT_STATE != SAME_FACT
```

When the same value appears in multiple states, the verifier emits a `SAME_NUMBER_DIFFERENT_STATE` signal. If those observations are not explicitly reconciled, disposition becomes `HOLD` with `STATE_COLLAPSE_TRACE_REQUIRED`.

A signal does not prove wrongdoing. It requires tracing.

Within the same state, materially different bound values become `CONFLICT` until reconciled.

## Two-direction replay

```text
TOP_DOWN:
LAW -> MONEY -> PROGRAM -> TRANSACTION -> RECEIPT

BOTTOM_UP:
RECEIPT -> TRANSACTION -> PROGRAM -> MONEY -> LAW
```

The bounded node sequence must reverse exactly. A mismatch is `CONFLICT`, not an accusation.

## Recursive receipt binding

For every nonterminal recursion node:

```text
node[i].receipt_claim_ref == node[i+1].claim_ref
```

Breaking that edge is `REJECT` because the recursive proof chain is structurally invalid.

## OpenAI boundary

The model layer is optional. It may extract candidate fields and call the deterministic verifier. It may not infer missing money states, widen a verifier disposition, or turn a Dirty Math signal into fraud, intent, misconduct, guilt, or governmental authority.

```text
MODEL_EXTRACTION != VERIFICATION
VERIFIER_PASS != UNDERLYING_WORLD_TRUTH
DIRTY_MATH_SIGNAL != MISCONDUCT
OPENAI_API_KEY_REQUIRED_FOR_DETERMINISTIC_VERIFIER = FALSE
MODEL_EXECUTION_PERFORMED = FALSE
AUTHORITY_CREATED = FALSE
```

## Synthetic gate suite

The v0.1 vectors cover:

1. complete PASS;
2. number without state -> HOLD;
3. missing receipt -> HOLD;
4. valid records disagree -> CONFLICT;
5. bound contradiction -> REJECT;
6. same number / different state, unreconciled -> HOLD + signal;
7. same number / different state, reconciled -> PASS + signal;
8. top-down / bottom-up mismatch -> CONFLICT;
9. attempted state promotion -> REJECT;
10. broken recursive receipt binding -> REJECT;
11. zero-dollar amount is valid when provenance is complete;
12. same state + same value across multiple sources may PASS.

## Core invariant

```text
NO_NUMBER_OUTRANKS_ITS_PROVENANCE = TRUE
AUTHORITY_CREATED = FALSE
```

The algorithm proves only its bounded evidentiary disposition. It does not create a legal conclusion, congressional finding, fraud determination, or government action.
