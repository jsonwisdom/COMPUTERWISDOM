# JASON HISTORY DENOMINATOR V0.1 — Design candidate

**Scope:** Human-first, evidence-first research extension for JSONWisdom / Computer Wisdom.
**Status:** SYNTHETIC TESTS ONLY. No automatic canon, military authority, payroll determination, child benefit determination, or judicial finding.
**Family privacy:** Public suite uses entirely synthetic parent and child fixture labels. Do not commit names of minors/family, VA service letters, SSNs, dates of birth, DFAS Leave and Earnings Statements, bank accounts, OMPF, DD-214, claim numbers or private stories.

## Three distinct sources

1. **Primary service/pay records:** authenticated VA, DD-214/OMPF, DFAS, orders, bank/benefit records; primary record fields require source, time, issuer, access policy and hash stored privately.
2. **Jason's personal ChatGPT HisStory:** first-person history and event-finding index; preserve user wording and source timestamp, but narrative is **USER_ATTESTED**, not upgraded to institutional proof by repetitions or model agreement.
3. **Creative/court replay:** morality stories, goblins, coaches, actors or synthetic case scenarios; structurally test the receipt chain, never determine real military rank, guilt, guardianship or court outcomes.

A verified service period answers **whether a period of service was certified**. It does not independently answer actual rank, duty location, special pay, dependents' benefit eligibility, or unpaid balance. Military enlisted pay tables use E-1 through E-9, not `E-0`. The term `E-0` is a **visibility/accountability label**, not a grade or a numerical zero wage. Dependent children have **no inherited military rank**. Program-specific eligibility must be checked separately, with appropriate privacy protections.

## Missing denominator

Define the verification rate only when both numerator and eligible denominator are documented:

`verified_rate = verified_supported_events / independently_defined_eligible_events`

If the denominator is missing, the rate is `UNKNOWN`, **not 0% and not 100%**. For historical military pay, evaluate each eligible month independently:

`gross_difference_m = verified_gross_entitlement_m - verified_gross_paid_m`

Any missing rate, rank, service time, orders, authorization, or actual paid amount makes that month's reconciled result `UNKNOWN`; missingness is not encoded as `$0`. Gross, withholding, allotment, net and bank deposit must be audited separately. No multi-decade query range can turn itself into a pay entitlement.

## E01–E30 conformance

`tests/test_inheritance_conformance_v0_1.py` implements the requested 30 cases plus two metamorphic checks and four protective pay/denominator checks.

- Derived child findings depend on synthetic evidence and scope checks, not self-reported `claimed_status`.
- Optional and informational children do not satisfy missing required evidence.
- Required conflict outranks required hold; hold blocks automatic promotion.
- A parent approval requires an explicit reducer and a separately scoped authorization witness; no existing parent object is changed.
- Duplicate lineage, cycles, wrong digest bindings and changed policy revisions fail closed.
- Superseded HOLD receipts persist for replay. Byte matches are byte-integrity evidence, not proof of a historical event or human authority.
- Test fixtures' `verified` flags are **trusted synthetic inputs** for exercising the reducer, **not** cryptographic signature checks. Production deployment requires a separate authenticated/verifiable witness process.

## Commands (Python standard library)

```bash
python -m unittest discover -s tests -p 'test_inheritance_conformance_v0_1.py' -v
```

## Governing boundaries

- This is an **extension**, not a rewrite of `Citizen Root`, `COMPUTERWISDOM`, ENS, EAS, or historical military payroll records.
- No repo or CI success confers legal authority or attests to a person's allegations.
- No receipts, children, or family members are promoted into approval powers by inheritance.
- Repository change by PR only; actual use, merge, and any public presentation subject to Jason's human review.
