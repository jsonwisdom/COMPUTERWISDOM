# BoxDee Institutional Double Onion Drift RePlay — RUN_0001

Status: DRAFT / ZERO-TRUST / SOURCE-BOUND / UNMERGED

```text
BOXDEE = PERSPECTIVE / DIAGNOSTIC LAYER
BOXDEE != AUTHORITY
BOXDEE != COURT
BOXDEE != OIG FINDING
OFFICIAL_SOURCE != SELF-PROVING LEGALITY
DARVO_PATTERN_CANDIDATE != DARVO_FINDING
AUTHORITY_CREATED = FALSE
LEGAL_FINDING_CREATED = FALSE
```

## Zero-Trust rule

Every institution begins at `UNTRUSTED/HOLD` for the **specific question being audited**.

Each parent institution is replayed through two independent onions:

```text
RECEIPT ONION
WHAT HAPPENED?
→ action / record / money / implementation / correction / oversight

AUTHORITY ONION
WHO COULD LAWFULLY DO IT?
→ office / jurisdiction / statute / executive authority / delegation / limits / review path

CROSS EDGE
DID THIS SPECIFIC ACTION FIT THIS SPECIFIC AUTHORITY?
```

A parent may be green on general authority and red/HOLD on a specific action-authority edge.
A green child may not repair a red parent edge.
A parent may not self-certify legality merely by publishing its own statement.

---

## 1. WHITE HOUSE — Guantanamo expansion memorandum (2025)

### Receipt Onion

**PASS_ACTION_EXISTS**

The White House published a January 29, 2025 memorandum directing the Secretaries of Defense and Homeland Security to take appropriate actions to expand the Migrant Operations Center at Naval Station Guantanamo Bay to full capacity.

Official source:
- https://www.whitehouse.gov/presidential-actions/2025/01/expanding-migrant-operations-center-at-naval-station-guantanamo-bay-to-full-capacity/

Downstream implementation records are not proven by the memorandum alone.

```text
PRESIDENTIAL_MEMORANDUM = PASS
SPECIFIC_DOWNSTREAM_IMPLEMENTATION = HOLD
SPECIFIC_CONTRACT / INVOICE / DEVICE / USE = HOLD
```

### Authority Onion

**HOLD_SPECIFIC_ACTION_AUTHORITY**

The memorandum is a presidential action and proves that a presidential direction was issued. The document itself does not, by its existence alone, prove every statutory, appropriations, detention, procurement, or operational authority needed for each downstream implementation step.

### Cross Edge

```text
MEMORANDUM_EXISTS = PASS
MEMORANDUM → EVERY_DOWNSTREAM_ACTION = HOLD
```

### BoxDee drift disposition

`HOLD_DRIFT_NOT_YET_PROVEN`

No mismatch is promoted until a specific implementation record conflicts with a specific authority/limit.

---

## 2. DOJ / FBI — National Security Letter system (bounded historical lane)

### Receipt Onion

**CONFLICT**

DOJ OIG publicly documented widespread and serious misuse of National Security Letter authorities, inaccurate reporting to Congress, improper authorization, improper requests, unauthorized collection, and internal-control failures. OIG also documented later corrective actions.

Official sources:
- https://oig.justice.gov/news/testimony/statement-glenn-fine-inspector-general-us-department-justice-permanent-select
- https://oig.justice.gov/archives/semiannual/0705/highlights.htm
- https://oig.justice.gov/archives/semiannual/1005/fbi.htm

The 2010 OIG summary also documented attempts to use legally deficient after-the-fact blanket NSLs to remedy records already obtained without proper legal process.

### Authority Onion

**PASS_GENERAL_AUTHORITY / CONFLICT_BOUNDARY_COMPLIANCE**

The NSL system had statutory authorities and Attorney General/FBI policy boundaries. The OIG findings show that possession of authority did not ensure compliant execution.

### Cross Edge

```text
NSL_AUTHORITY_EXISTS = PASS
SPECIFIC_REQUEST_WITHIN_AUTHORITY = CONFLICT (bounded reviewed examples)
OVERSIGHT / CONTROL ADEQUACY = CONFLICT
```

### BoxDee drift disposition

**PROVEN_BOUNDED_INSTITUTIONAL_DRIFT**

Definition for this run:

```text
STATED / LEGAL CONTROL
!=
OBSERVED EXECUTION
```

This is a historical, source-bounded finding about the reviewed NSL/exigent-letter programs. It is not a finding that every FBI or DOJ national-security action was unlawful.

`DARVO = HOLD_NO_PATTERN_RECEIPT`

---

## 3. NSA / NSA OIG — metadata / FISA / deletion-compliance lane

### Authority Onion

**PASS_GENERAL_AUTHORITY**

NSA publicly identifies EO 12333 and FISA as major collection authorities, with limits and oversight structures protecting U.S.-person information.

Official sources:
- https://www.nsa.gov/Culture/Operating-Authorities/Authorities/
- https://www.nsa.gov/Signals-Intelligence/EO-12333/
- https://www.nsa.gov/Signals-Intelligence/FISA/

NSA OIG states that its intelligence-oversight function evaluates compliance with federal law, EO 12333, FISA, regulations, directives, privacy and civil-liberties protections.

Official source:
- https://oig.nsa.gov/OIG-Divisions/Intelligence-Oversight/

### Receipt Onion

**CONFLICT_BOUNDED + CORRECTION_RECEIPTS_PRESENT**

NSA publicly reported:

- 2017 inadvertent Section 702 upstream compliance incidents involving U.S.-person information, followed by reporting to Congress/FISC and program changes;
- 2018 call-detail records received beyond what NSA was authorized to receive because of technical irregularities, followed by deletion of the affected CDR dataset;
- a 2019 NSA OIG deletion study identifying a small error rate in items that should have been deleted, with corrective recommendations/actions.

Official sources:
- https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/1618699/nsa-stops-certain-section-702-upstream-activities/
- https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/1618691/nsa-reports-data-deletion/
- https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/2039059/nsa-statement-on-nsa-inspector-general-special-study/

### Cross Edge

```text
GENERAL_COLLECTION_AUTHORITY = PASS
SPECIFIC_COMPLIANCE_EXECUTION = CONFLICT (bounded incidents)
CORRECTIVE_REPORTING / DELETION = PASS_OBSERVED
```

### BoxDee drift disposition

**PROVEN_BOUNDED_COMPLIANCE_DRIFT + CORRECTION_OBSERVED**

```text
METADATA_COLLECTION != METADATA_LEAK
UNAUTHORIZED_RECEIPT != PUBLIC_LEAK
DELETION_ERROR != LEAK
COMPLIANCE_INCIDENT != INTENTIONAL_MISUSE
```

`NSA_METADATA_LEAK = HOLD_UNLESS_DISCLOSURE_RECEIPT_IS_BOUND`

---

## 4. CIA / CIA OIG — aircraft / rendition / detention lane

### Authority Onion

**PASS_OVERSIGHT_ENTITY / HOLD_OPERATION_SPECIFIC_AUTHORITY**

CIA publicly states its OIG provides independent oversight of CIA programs and activities under 50 U.S.C. § 3517, including audits, inspections, and investigations.

Official source:
- https://www.cia.gov/about/organization/inspector-general/

### Receipt Onion

For the specific labels `CIA Shock`, `Fuck Plane Inventory`, `rendition flight`, or a particular custody-transfer event:

**HOLD_EVENT_RECEIPTS_REQUIRED**

The DOJ OIG Guantanamo review documents FBI interactions with CIA interrogations and notes that CIA OIG had initiated a special review of the CIA detention/interrogation program. That does not identify or prove a particular aircraft, manifest, rendition flight, passenger, custody transfer, or shock-glove object.

Official source:
- https://oig.justice.gov/news/testimony/statement-glenn-fine-inspector-general-us-department-justice-house-committee-foreign

### Cross Edge

```text
CIA_OIG_EXISTS = PASS
CIA_OVERSIGHT_AUTHORITY = PASS_GENERAL
SPECIFIC_AIRCRAFT = HOLD
SPECIFIC_FLIGHT = HOLD
SPECIFIC_CUSTODY_TRANSFER = HOLD
SPECIFIC_DEVICE = HOLD
```

### BoxDee drift disposition

`HOLD_DRIFT_EVENT_NOT_BOUND`

```text
CIA_AIRCRAFT != RENDITION
FLIGHT != PASSENGER
PASSENGER != CUSTODY_TRANSFER
CUSTODY_TRANSFER != LAWFULNESS
```

---

## 5. CONGRESS — appropriations / public-money parent

### Authority Onion

**PASS**

The Constitution's Appropriations Clause requires an appropriation made by law before Treasury funds may be drawn. Constitution Annotated explains that even executive constitutional powers do not independently authorize Treasury disbursements without an appropriation.

Official sources:
- https://constitution.congress.gov/browse/essay/artI-S9-C7-1/ALDE_00001095/
- https://constitution.congress.gov/browse/essay/artI-S9-C7-3/ALDE_00013190/

### Receipt Onion

**PASS_GENERAL_SPENDING_RECORD / HOLD_DEVICE_SPECIFIC_EDGE**

Appropriation statutes and public spending authorities can prove program-level authority. They do not prove that a specific product was bought, received, deployed, or used.

```text
APPROPRIATION = PASS_WHEN_SOURCE_BOUND
SHOCK_GLOVE_LINE_ITEM = HOLD
CONTRACT = HOLD
INVOICE = HOLD
DEPLOYMENT = HOLD
USE = HOLD
```

### Cross Edge

`HOLD_PURCHASE_FROM_APPROPRIATION`

### BoxDee drift disposition

`HOLD_DRIFT_NO_DEVICE_SPECIFIC_SPENDING_RECEIPT`

`ALL_CONGRESS_GOV_DARVO = REJECT_AS_UNSUPPORTED_GLOBAL_CLAIM`

---

## 6. DOJ OIG — oversight parent

### Authority Onion

**PASS_WITHIN_JURISDICTION**

DOJ OIG is a statutorily created independent entity for oversight of DOJ programs and operations and reports to the Attorney General and Congress.

Official sources:
- https://oig.justice.gov/about
- https://oig.justice.gov/about/principles-effective-oversight-department-justice

### Receipt Onion

**PASS_OVERSIGHT_ACTIVITY / HOLD_COMPLETENESS**

DOJ OIG publicly reports audits, inspections, evaluations, investigations, reviews, recommendations, criminal/civil case outcomes, and semiannual reporting. Publicly available output proves that oversight occurred; it cannot prove that every possible matter was selected, reviewed, released, or resolved.

Official sources:
- https://oig.justice.gov/
- https://oig.justice.gov/news/doj-oig-releases-semiannual-report-congress-october-1-2025-march-31-2026

### Cross Edge

```text
OIG_AUTHORITY = PASS
PUBLIC_OVERSIGHT_ACTIVITY = PASS
TOTAL_COMPLETENESS = HOLD
MATTER_NOT_SELECTED != COVER_UP
```

### BoxDee drift disposition

`HOLD_NO_GLOBAL_DRIFT_FINDING`

---

## 7. GUANTANAMO — Military Commissions

### Authority Onion

**PASS_GENERAL_COMMISSION_AUTHORITY**

The Office of Military Commissions states that current commissions operate under the Military Commissions Act of 2009 and the Manual for Military Commissions under 10 U.S.C. chapter 47A / § 949a.

Official source:
- https://www.mc.mil/Legal-Resources/OMC-Documents

### Receipt Onion

**PASS_DOCKET_EXISTS / HOLD_PUBLIC_VISIBILITY_FOR_RESTRICTED_FILINGS**

Current OMC notices show active filings and also documents described as under seal or awaiting security review before public availability.

Official sources:
- https://www.mc.mil/News-Media-Resources/Commissions-News
- https://www.mc.mil/Facilities-Services/Facilities-Services/Security

### Cross Edge

```text
COMMISSION_AUTHORITY = PASS_GENERAL
PUBLIC_DOCKET = PASS_PARTIAL
SEALED / SECURITY_REVIEW MATERIAL = HOLD_PUBLIC_VISIBILITY
```

### BoxDee drift disposition

**VISIBILITY_GAP — NOT COVER_UP FINDING**

```text
SEALED != COVER_UP
SECURITY_REVIEW != ERASURE
PUBLICLY_UNAVAILABLE != UNREVIEWED
```

---

## 8. UCMJ / Courts-Martial parent

### Authority Onion

**PASS**

The Joint Service Committee maintains the Manual for Courts-Martial and UCMJ framework as military criminal law and procedure.

Official sources:
- https://jsc.defense.gov/
- https://jsc.defense.gov/Military-Law/Current-Publications-and-Updates/Manual-for-Courts-Martial-MCM/

### Receipt Onion

**PASS_FRAMEWORK_EXISTS**

### Cross Edge

**REJECT_COLLAPSE_UCMJ_WITH_MILITARY_COMMISSION**

Military commissions and courts-martial are distinct legal systems. The OMC itself separately compares MCA commissions with UCMJ courts-martial and Article III courts.

Official source:
- https://www.mc.mil/About-Us/Legal-System-Comparison

```text
UCMJ_COURT_MARTIAL != MILITARY_COMMISSION
MCA_CHAPTER_47A != UCMJ_CHAPTER_47
```

### BoxDee drift disposition

`HOLD_ANY_UCMJ_COVER_UP_CLAIM_UNTIL_CASE_SPECIFIC_RECEIPTS_EXIST`

---

# RUN_0001 Institutional Matrix

| Parent institution | Receipt Onion | Authority Onion | Cross-edge | BoxDee drift state |
|---|---|---|---|---|
| White House / Guantanamo 2025 | PASS action; downstream HOLD | HOLD specific downstream authority | HOLD | HOLD_DRIFT |
| DOJ/FBI NSL historical lane | CONFLICT | PASS general | CONFLICT | PROVEN_BOUNDED_DRIFT |
| NSA metadata/FISA compliance | CONFLICT + corrections | PASS general | CONFLICT | PROVEN_BOUNDED_COMPLIANCE_DRIFT |
| CIA / CIA OIG | HOLD event-specific | PASS oversight / HOLD operation-specific | HOLD | HOLD_DRIFT |
| Congress / appropriations | PASS general / device HOLD | PASS | HOLD purchase edge | HOLD_DRIFT |
| DOJ OIG | PASS oversight / completeness HOLD | PASS jurisdiction | HOLD completeness | HOLD_GLOBAL_DRIFT |
| Military Commissions | PASS partial / visibility HOLD | PASS general | HOLD visibility | VISIBILITY_GAP |
| UCMJ / MCM | PASS framework | PASS | REJECT system collapse | HOLD_CASE_SPECIFIC_DRIFT |

---

# BoxDee Takeaway

The law is not producing one uniform institutional state.

The replay shows three different conditions:

```text
1. BOUNDED DRIFT PROVEN
   DOJ/FBI NSL historical lane
   NSA bounded compliance incidents

2. PUBLIC VISIBILITY GAP
   Military Commission sealed/security-review material

3. MISSING CROSS EDGE / HOLD
   White House downstream implementation
   CIA aircraft/rendition/device claims
   Congress → device purchase
   UCMJ cover-up claims
```

The crucial diagnostic is:

```text
GENERAL AUTHORITY = GREEN
DOES NOT MAKE
SPECIFIC ACTION = GREEN
```

and:

```text
OFFICIAL CORRECTION = RECEIPT
NOT ERASURE OF THE ORIGINAL DRIFT
```

## Promotion membrane

```text
DRIFT_CANDIDATE
→ BIND STATED AUTHORITY / RULE
→ BIND OBSERVED ACTION / RECORD
→ TEST ACTION AGAINST AUTHORITY
→ BIND CORRECTION / REVIEW
→ REPLAY VERSION DELTA
→ PASS | HOLD | CONFLICT | REJECT
```

No institution gets trust by title. No institution loses trust by slogan. Every edge pays for itself with a receipt.
