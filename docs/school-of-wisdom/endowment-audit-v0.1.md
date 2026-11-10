# School of Wisdom — Endowment Audit Standard v0.1

**DRAFT • Public-source framework, not a live audit • Authority false • Publication hold**

## What do we audit?

We audit a specific **institution and legal entity**, not a schoolchild, family surname, religion, ethnicity, or political identity. A school district, district foundation, university, university foundation, or related nonprofit can have separate books and governing rules. **An endowment is not every charitable donation.** Separate:

- Donor-restricted endowment and board-designated endowment
- Current-use unrestricted and restricted gifts
- Government grants and contracts, received gifts vs uncollected pledges
- Investments, income, losses, fees, appropriations and inter-entity transfers

## Three evidence judgments

1. **Bytes:** Does a digest match the exact captured record? (reproducibility, not truth)
2. **Source:** Did the identified institution actually issue that record, on the recorded date and in the claimed scope?
3. **Transaction/outcome:** Did money move and get spent for the claimed purpose? Reconcile contemporaneous bank/custody/ledger and redacted educational records.

Never treat a television report, shared ancestry, donor mention or a signed digest as a conviction. A legal violation requires applicable law, factual evidence, competent process and review. The **student can ask questions**; the librarian finds records, the mathematician checks dollars, and the auditor determines coverage, with human review.

## Twelve gates

| ID | Gate | Audit question |
|---|---|---|
| 01 | Institution/entity | Which distinct legal person owns the fund and which authority can audit? |
| 02 | Source custody | Where are original statements, gift instruments, capture dates and hashes? |
| 03 | Fund type | Gift, grant, pledge, endowment, investment return or inter-entity transfer? |
| 04 | Restrictions | What did the instrument and applicable law allow the school to spend? |
| 05 | Rollforward | Does beginning balance reconcile to ending balance, using integer cents? |
| 06 | Investments | Are custody statements, returns, investment fees and management policies supported? |
| 07 | Conflicts | Are interested-person payments disclosed, appropriately reviewed and recused? |
| 08 | Cross-entity | Can funds be traced between school, foundations and contractors without duplicate counting? |
| 09 | Educational purpose | Does lawful and privacy-safe evidence support the stated purpose or service? |
| 10 | Foreign funding | For eligible higher-ed institutions only, assess federal Section 117 source-level aggregation and reporting. |
| 11 | Privacy | Protect student education records, nonpublic donor details and minors. |
| 12 | Independent review | Reproduce each test, record exceptions, publish corrections and require a human conclusion. |

These are proposed project controls, **not** a claim that every gate is imposed by the same statute on every school.

## Math that students can replay

If investment return is expressed **gross of separately tracked fees**, use:

`closing_cents = opening_cents + received_gifts_cents + gross_return_cents + signed_transfers_cents − spending_cents − fees_cents`

A fictional classroom example: $1,000 opening + $300 received gifts + $100 gross return − $60 spending − $10 fees = **$1,330 closing**. Reverse the arithmetic and recover the $1,000 opening. **Do not double-subtract fees if a source already reports net investment return.**

For real institutions, this arithmetic must be matched to original ledger entries, bank/custody statements and donor restrictions. Use explicit fiscal dates and distinguish cash from accrual.

## Minnesota and U.S. law/source boundaries

- [Minnesota Department of Education independent financial audits](https://education.mn.gov/MDE/dse/schfin/fin/ifa/): School districts and covered LEAs submit annual audited financial statements and UFARS data.
- [Minnesota AG — institutional fund management](https://www.ag.state.mn.us/Consumer/Handbooks/CharitiesLaws/CH7.asp): Donor restrictions and prudent management under UPMIFA.
- [IRS 990 Schedule D](https://www.irs.gov/instructions/i990sd): Endowment fund disclosures where applicable.
- [IRS Schedule B](https://www.irs.gov/instructions/i990sb): Most Form 990 nonprofits need **not** publicly disclose contributor names and addresses.
- [IRS Schedule L](https://www.irs.gov/instructions/i990sl): Reportable transactions with interested persons when applicable.
- [HEA Section 117](https://fsapartners.ed.gov/knowledge-center/topics/section-117-foreign-gift-and-contract-reporting): Certain higher education schools must report foreign gifts/contracts reaching $250,000 per source per calendar year; **not a universal K–12 rule**.
- [FERPA](https://studentprivacy.ed.gov/ferpa): Education-record privacy and applicable exceptions.
- [Minnesota AG — nonprofit conflicts](https://www.ag.state.mn.us/consumer/publications/fiduciaryduties.asp): Appropriate disclosures, disinterested board decisions and fiduciary safeguards.

## Three-year daily findings: preserve, don't assume

The user's historical observations are **reported, not ingested into this specification**. Before testing patterns, create a separate authorized inventory of each exact artifact, day, issuing institution, claims, corrections, source byte digest and independent replication. Missing days remain UNKNOWN. A daily claim is not automatically a unique incident. No one gets to infer a 100% success rate from an incomplete dataset.

## Privacy and due process

Never build child or grandparent genealogy graphs. No private student records, donor home addresses or identification by religious or ethnic origin; no automated guilt or "pedophile network" classification from institutional associations. A documented donor relationship can be analyzed for institutional conflicts in authorized financial records; wrongdoing remains a separate evidence and legal question.

**CI-FIRST:** Draft schema and synthetic arithmetic may PASS their tests. Actual endowment flows, permission, school integration and publication are UNKNOWN / NOT AUTHORIZED. A PR is not government validation or legal judgment.

Structured rules and synthetic record: [endowment-audit-v0.1.json](endowment-audit-v0.1.json). Validation: [endowment-audit.test.mjs](endowment-audit.test.mjs).
