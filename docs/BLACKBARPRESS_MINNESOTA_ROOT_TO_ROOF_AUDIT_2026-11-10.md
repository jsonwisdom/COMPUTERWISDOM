# BLACKBARPRESS — Minnesota Root-to-Roof Audit

**Audit ID:** BLACKBARPRESS-MN-ROOT-TO-ROOF-20261110  
**Snapshot:** November 10, 2026  
**Status:** Initial source-backed audit; incomplete statewide contract-level reconciliation.  
**Machine-readable evidence:** [JSON ledger](../../audits/minnesota/root-to-roof-2026-11-10.json)  
**Arithmetic check:** [Wolfram](../../proofs/mn_root_to_roof_october2026.wl)

## Questions

Which Minnesota public investments and job announcements resulted in signed agreements, payouts, actual hiring, closures or repayments? Which subsidies failed and which companies were flagged in separate PPP/EIDL fraud programs? Can any specific false jobs statement be documented?

**Do not equate** an announced award, an executed business subsidy agreement, a cash disbursement, audited employment, a grant cancellation, an SBA suspension, or a criminal conviction. These are distinct record classes.

## PASS — Established by primary records (as scoped)

1. [DEED 2025 Business Assistance Report](https://mn.gov/deed/government/business-subsidy/legislative-reports/) reports **1,418** business-assistance agreements for 1999–2024: **1,174** achieved obligations, **152** still active with time remaining, **92** discontinued. The terminated count alone does not establish fraud, nonpayment, or project cancellation in October 2026.
2. [October 21, 2026 DEED press announcement](https://mn.gov/deed/newscenter/press-releases/?id=1045-772342) announces five Minnesota projects with an itemized **$2,065,000** in JCF/MIF support and headline **141 projected jobs**. None of these figures is independently verified realized 2026 payroll.
3. [SBA annual report](https://www.sba.gov/annual-report/) reports **6,900 suspended Minnesota borrowers associated with approximately $400 million** in suspected fraudulent PPP/EIDL loans. A suspension or agency fraud flag is not a court finding about every named borrower.
4. [Minnesota Management and Budget tracking](https://mn.gov/mmb/budget/federal-investments/data-and-reporting/) displays **$157,195,889** in permanently canceled federal funds at state agencies. This is an incomplete, distinct federal-grant scope; do not add it to business-assistance terminated agreements or treat it as the same sort of contract.

## FAIL — One bounded numerical consistency test

The October 21 source gives individual job projections of **14 + 15 + 7 + 75 + "over 30"**. On a literal integer interpretation, the minimum is **142**, while its headline says **141**. A reporter should ask whether "over 30" was rounded/imprecise, or whether the headline was wrong. This tests **arithmetic of published descriptions**, not whether the companies exist or have defrauded anyone.

## UNKNOWN — Records still needed

- Signed local council approvals and full DEED subsidy agreements for the five October 21 announcements.
- Requested vs actually disbursed dollar amounts, repayment and clawbacks, verified payroll/job counts, and capital spending documentation. [DEED's Job Creation Fund FAQs](https://mn.gov/deed/business/financing-business/deed-programs/mn-jcf/faqs.jsp) say JCF awards/rebates require performance documentation; a press announcement is not proof of payment.
- Names, dates, agencies and outcomes of individual terminated assistance agreements. A [DEED public page](https://mn.gov/deed/government/business-subsidy/legislative-reports/2025/five-year-goals.jsp) links to data on recipients who did not meet terms and had unpaid repayment obligations, but this snapshot has **not** yet inspected the full underlying download.
- Actual dated October–November 2026 terminations across federal contracts, state/local grants, private projects and job losses; these categories require separate denominators and source datasets.
- Claim that any specific senator or president inflated official employment by inventing company contracts. The [BLS monthly jobs survey](https://www.bls.gov/news.release/empsit.faq.htm) is based on establishment payroll samples and modeled births/deaths, revised against additional employer and unemployment insurance data. State development press releases are not an input table of authorized jobs.

## Full audit join — per project

```text
County + municipality + legal entity ID + program + agreement ID
  -> council authorizing vote -> award approval -> executed agreement
  -> payment voucher -> employer payroll evidence -> actual verified jobs
  -> amendments/terminations -> recovery or forgiveness -> public report
```

For each claim, record document URL, public-record locator, record date, original bytes hash SHA-256, capture timestamp, source authority, exact proposition, PASS/FAIL/UNKNOWN, and bounded limitations. **A future digest cannot prove preservation of an original not yet downloaded**. Redact private employee identifiers before publication. Record evidence changes as append-only supplements.

## Practical next document request

Ask DEED and the five relevant local governments for signed agreements, award/payment ledgers, amendments, annual performance and payroll-verification summaries (aggregate only), terminated/canceled designations, recoupment decisions, and dated job counts for each named project. Keep the request focused on **publicly releasable records** and preserve statutory privacy exclusions.

**CI-FIRST:** model arithmetic PASS; documented agency aggregates PASS; one press-release arithmetic-consistency check FAIL; individualized fraud, disbursement, politician intent and statewide cancellations UNKNOWN until scoped records are reviewed.

**No merge, claims of independent review, production deployment, or authority elevation from this draft.**
