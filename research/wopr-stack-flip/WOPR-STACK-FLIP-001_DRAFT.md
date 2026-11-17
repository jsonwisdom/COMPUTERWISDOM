# WOPR-STACK-FLIP-001 — Consumer Billing Evidence Challenge

**Status:** DRAFT / SYNTHETIC ANALYSIS ONLY / NOT A FRAUD FINDING  
**Date:** 2026-11-16  
**Scope:** archival methodology and independent replay design; no live transactions, deployment, credential use, or payments.  
**Authority:** Human review required. No actual allegation against an identified vendor is established here.

## Source/provenance boundary
- Basis: user-authored three-round fictional evidence exercise and subsequent correction of the loss model, in the conversation. This file is an **analytical archive**, not an authenticated billing-evidence intake.
- **Real customer billing records examined: NONE.** Reports of a particular customer's service frustration are not independently authenticated as charge/refund proof.
- The four-customer scenario is hypothetical unless four independently authenticated original receipts arrive.
- GitHub search for exact case ID yielded no matching existing indexed record; search miss does not establish absence elsewhere.
- Wolfram Language calculation independently executed in ChatGPT: charges {100,100}, refunds {0,120} => net 80, floored per-customer loss 100, excess refund 20. The test verifies arithmetic, not national claims or legal findings.

## Math: explicitly separate the estimands
For independently established unjustified charges C_i and refunds/credits actually received R_i, compute a nonnegative **documented individual-loss ledger**:
```text
L_documented = SUM over individually verified cases i of MAX(0, C_i - R_i)
E_overrefund = SUM over those cases i of MAX(0, R_i - C_i)
B_net        = SUM over those cases i of (C_i - R_i)
```
Here C_i must be limited to unjustified amounts **after** assessing payment method, contract terms, service delivery, dispute status, charge reversals and duplicate entries. A pending or promised refund is not an issued refund. These variables and records are UNKNOWN for real customers in this case.

**Counterexample:** C={100,100}, R={0,120}. L_documented=100; E_overrefund=20; B_net=80. Cross-customer offset destroys the nonnegative loss interpretation.

**Endogenous N problem:** The count of already substantiated complainants is a valid case-ledger count, not a valid population sampling frame. Nationwide prevalence requires a separately defined eligible population, unbiased/defensible sampling mechanism, payment-method stratification, verified positive/negative classifications, and uncertainty bounds. Do not extrapolate from four selected complaints.

**$34.2B scenario:** 342,000,000 × $100 = $34,200,000,000, assuming no more than 342 million affected persons, at most one unjustified $100 loss each. It is a conditional illustrative cap, **not an empirical upper bound** without those assumptions, and not an observed finding.

## Evidence matrix
| Claim | Disposition | Required next evidence |
|---|---|---|
| Loss model floor correct | PASS (synthetic counterexample) | Extend tests to duplicates, refunds, partial service and missing fields |
| Four matching complaints establish possible pattern | CONDITIONAL / scenario only | Original payment and service records, source provenance |
| Four complaints show 342M affected | FAIL | Independently sampled population denominator |
| Vendor theft or intent | NOT ESTABLISHED | Authenticated evidence meeting applicable legal elements |
| Documented affected count | UNKNOWN | Individual verified customer records |
| Documented unjustified net charges | UNKNOWN | Billing, service terms, reversals, refunds |
| National dollar loss | UNKNOWN | Valid denominator, unbiased design and uncertainty |
| $34.2B illustrative calculation | PASS ARITHMETIC / CONDITIONED | Do not describe as discovered theft |
| Availability of individual remedies | CASE-SPECIFIC | Payment instrument, dates, jurisdiction, applicable rules |

## Legal boundary — NOT independently verified in this archive
Named research leads, not legal conclusions: FTC Act §5 (15 USC §45), FCBA (15 USC §1666), Regulation E, ROSCA and its related rule litigation, Minnesota Stat. §325F.69, and Minnesota conciliation-court limits. No specific statutory deadline, remedy status, or court limit is established here. A failed or expired procedural remedy does not logically prove that the underlying event never occurred; precise consequences vary with the governing rule and individual facts.

## Deterministic replay gates (proposed; NOT executed against actual records)
1. Canonicalize itemized charge/refund objects with stable IDs, dates, currency, payment method, and provenance.
2. Fail on missing amounts, impossible dates, invalid units, duplicate IDs or undocumented adjustments.
3. Recompute each nonnegative loss, each over-refund, and the separate net balance.
4. Demonstrate that over-refunds cannot offset another customer's loss.
5. Draw sampling frame independently of observed favorable outcomes; report coverage, nonresponse and uncertainty.
6. Compare output hash against reproducible canonical input and recorded execution version.
7. Inject mutated input, deleted receipt and broken chain link; each must fail closed.
8. Require explicit human review before any public accusation or production use.

## Release gate
**BUILD: DOCUMENTATION ONLY** · **VERIFY: SYNTHETIC ARITHMETIC ONLY** · **PAY: NO** · **PUBLIC DEPLOYMENT: NO** · **MERGE: HOLD**.

Owner decides whether to promote a later version after authentic receipts, legal-source checks and independent tests. The record must not label actual customers harmed, a company guilty, national losses proven, or this archive a real investigation finding.
