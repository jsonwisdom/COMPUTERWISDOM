# JASON'S CITIZEN-FIRST PUBLIC AUDIT STANDARD — V1.0

**Status:** Proposed, independently published civic/engineering standard. **Not** a statute, binding court rule, CMS policy, adjudication, or government adoption.
**Date:** 2026-11-16
**Owner:** Jason Wisdom / Computer Wisdom
**Case profile:** CMS Minnesota FFP disallowance MN/2027/001/MAP

## 1. Constitutional design: citizen may question; institutions must explain

This standard must NEVER make a citizen obtain an identity credential, wallet signature, hash, delegation receipt, preapproval, burden-of-proof score, or agency permission merely to ask a public question, reproduce published arithmetic, publish criticism, or request accessible government records.

No internal **HOLD** status may be interpreted as restraining citizen speech or participation. Verification labels describe only the current strength and scope of a *particular claim*. They are not licenses to speak.

This document creates no new legal compulsion to disclose protected records, nor does it waive lawful exemptions or change legal burdens of proof.

## 2. Evidence lanes shall be separate

| Lane | Question | Allowed output |
|---|---|---|
| **CITIZEN / MATH** | Is the stated mathematical operation reproducible from stated inputs? | ARITHMETIC_PASS / ARITHMETIC_FAIL / NOT_EVALUATED |
| **SOURCE / INPUTS** | Is each input confirmed against the identified original record? | SOURCE_VERIFIED / REPORTED / UNKNOWN |
| **FEDERAL / METHOD** | Can CMS's actual sampling, stratification, weighting and expansion calculation be independently replicated? | METHOD_REPRODUCED / METHOD_DISPUTED / METHOD_UNKNOWN |
| **STATE / ALLOWABILITY** | Are FFP claims supported as legally allowable under the governing Medicaid rules? | ESTABLISHED / CONTESTED / UNKNOWN |
| **CRIMINAL** | Is fraud proved by applicable evidence and adjudication? | ESTABLISHED / ALLEGED / NOT_ESTABLISHED |
| **AGENT / ACTION** | Is a *consequential automated action* authorized? | ACTION_AUTHORIZED / ACTION_BLOCKED / NOT_APPLICABLE |

**No cross-lane promotion:** ARITHMETIC_PASS does not prove a CMS estimator, a program violation, criminal fraud, an agency's compliance, or permission for an automated action. Conversely, METHOD_UNKNOWN or ACTION_BLOCKED cannot cancel correct arithmetic or gate a citizen's speech.

## 3. Citizen arithmetic acceptance rule

For a fully specified deterministic operation, independently recompute with ordinary arithmetic. If equal within the expressly specified rounding rule, record **ARITHMETIC_PASS immediately**. No citizen identity or signature verification is required.

An input's documentary provenance is tracked separately; uncertainties in provenance do not change the mathematical truth of a *conditional* computation.

**Minnesota case snapshot (inputs under audit):**

```text
case_id: MN/2027/001/MAP
reported_frame_usd: approximately 478,800,000
reported_sample_size: 330
reported_deficient_claims: 78
reported_CMS_FFP_disallowance_usd: 112,752,702
simple_unweighted_proxy_usd:
  478,800,000 * (78 / 330) = 113,170,909.090909...
proxy_minus_reported_CMS_usd: 418,207.090909...
difference_as_percent_of_reported_CMS: approximately 0.37090649%
arithmetic_status: ARITHMETIC_PASS
method_reproduction_status: METHOD_UNKNOWN
criminal_fraud_status: NOT_ESTABLISHED
```

This proxy is *not* a reconstruction of the actual CMS estimator. The roughly $478.8 million input is approximate. Numerical proximity is not evidence that CMS used the simple count ratio.

## 4. Public-actor answerability, within existing law

**Federal CMS:** 42 CFR § 430.42(a)(4) requires the disallowance notice to state amounts claimed, allowed and disallowed **and the manner of their computation**. Section 430.42(a)(5)-(6) addresses factual findings/supporting documents and legal authorities. A civic audit may demand an intelligible explanation and pursue accessible records, with lawful redactions. This standard does not assert that all internal workpapers are automatically public.

**State of Minnesota:** 42 CFR § 430.42(b)(2)(ii) and (g)(1) assign the **state** the burden of documenting the allowability of its FFP claims in the administrative process. This statutory/regulatory obligation must not be confused with, or shifted to, an ordinary citizen auditing numbers.

**Public:** Citizens may request information under applicable federal or state disclosure channels, comment, inspect published records and run independent arithmetic without first satisfying an institutional chain-of-custody gate. Public access remains subject to privacy laws, legal exemptions, and applicable record classifications.

## 5. Minimum agency-facing method disclosure request

For independent replication of a stratified projection, request, to the extent releasable:

1. Exact sampling frame and data cut-off, with total eligible dollars and exclusions.
2. Fifteen stratum boundaries, population counts and dollar totals.
3. Sampling method, seed or randomization protocol where releasable, selection probabilities and replacement rules.
4. De-identified claim-level observations, audit outcome codes and allowability decisions.
5. Stratum expansion weights, estimator formula, error bounds, variance and confidence interval assumptions.
6. Reconciliation from each stratum to the stated $112,752,702 federal disallowance.

The request is an **agency explanation / transparency task**, not a citizen proof prerequisite. Withheld data must be marked WITHHELD or UNKNOWN and the legal reason recorded when known. Do not infer fraud or defective sampling merely because records are missing.

## 6. Automation boundary

The repository's `artifacts/AUTHORITY_REPLAY_MVP` receipts and authorization gates govern delegated actions by agents; they **do not apply** as preconditions for citizen arithmetic, public criticism, reading public records or proposing audit hypotheses.

If an agent is asked to write to an account/repository, deploy infrastructure, sign, spend, modify credentials or perform other consequential acts, apply the distinct authorization rules then. **Mathematical correctness is not action authority; action authority is not mathematical correctness.**

## 7. Public display and corrections

- Public banner: **CITIZEN ARITHMETIC — PASS**.
- Federal sampling banner: **METHOD REPRODUCTION — UNKNOWN** until underlying methodology is reproduced, not because the citizen lacks credentials.
- Minnesota FFP allowability: **ADMINISTRATIVE DETERMINATION DISPUTED / UNDER REVIEW**, according to documented procedural status; do not declare criminal fraud by extrapolation.
- Corrections must name the affected claim/input and preserve the prior version or append an explicit correction.
- Do not publish beneficiary identifiers or protected medical records.

## 8. Minimal acceptance tests

1. Citizen submits `478800000 * 78 / 330`: **ARITHMETIC_PASS**, without identity proof.
2. Citizen lacks CMS sampling worksheet: arithmetic stays PASS; methodology remains UNKNOWN.
3. Auditor alleges criminal fraud using only deficient-claim counts: fraud NOT_ESTABLISHED.
4. Agent attempts a consequential modification with no authorization: ACTION_BLOCKED; arithmetic remains PASS.
5. A state contests an FFP disallowance: record the dispute; retain the state allowability burden specified by § 430.42.
6. Confidential individual health record is requested: apply lawful privacy and access limitations; do not claim universal automatic disclosure.

**Normative core:** A citizen need not prove an institutional case to exercise civic oversight. A government decision must be explained to the extent required by law; statistical reconstruction and criminal attribution are separate evidentiary questions.

## Sources

- [42 CFR § 430.42 — Medicaid FFP disallowance, notice, reconsideration and appeal](https://www.ecfr.gov/current/title-42/section-430.42)
- [42 U.S.C. § 1396b — Payments to States](https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title42-section1396b&num=0&edition=prelim)

_Proposal only. No existing federal or state legal burden is altered by this document._
