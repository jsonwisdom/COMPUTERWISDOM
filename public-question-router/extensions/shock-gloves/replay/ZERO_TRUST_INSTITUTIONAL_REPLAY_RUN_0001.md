# Zero-Trust Institutional RePlay — RUN_0001

Run timestamp: `2026-08-18T23:52:00-05:00`

Status: DRAFT / REPLAY RECEIPT / HUMAN-REVIEW-REQUIRED

```text
INSTITUTIONAL_TRUST_DEFAULT = ZERO
OFFICIAL_SOURCE != TRUTH_BY_STATUS
SELF_REPORT = EVIDENCE_OF_SELF_REPORT_ONLY
DOWNSTREAM_GREEN != UPSTREAM_AUTHORITY
UPSTREAM_AUTHORITY != DOWNSTREAM_EVENT
SEALED != COVER_UP
CLASSIFIED != LAWFUL
DARVO_PATTERN_CANDIDATE != DARVO_FINDING
AUTHORITY_CREATED = FALSE
LEGAL_FINDING_CREATED = FALSE
```

## Method

Every institution begins at `HOLD`. Promotion is claim-specific, never institution-wide.

For each node, run two onions independently:

```text
RECORD ONION
SOURCE → OBSERVATION → CANONICAL RECORD → VERSION/TIME → CONTRADICTION → RECEIPT

POWER ONION
OFFICE → CLAIMED AUTHORITY → GRANTING TEXT → JURISDICTION → ACTION → REVIEW → RECEIPT
```

A source published by the institution may prove that the institution issued a statement, order, docket entry, report, or policy. It may not self-prove the legality, completeness, effectiveness, or factual accuracy of all underlying claims.

## Institutional replay matrix

### ZT-WH-001 — White House / Presidency

Observed record:
- The White House published a January 29, 2025 memorandum directing the Secretaries of Defense and Homeland Security to take appropriate actions to expand the Migrant Operations Center at Naval Station Guantanamo Bay to full capacity.
- The White House currently identifies Donald J. Trump as the 45th and 47th President.

Sources:
- https://www.whitehouse.gov/presidential-actions/2025/01/expanding-migrant-operations-center-at-naval-station-guantanamo-bay-to-full-capacity/
- https://www.whitehouse.gov/administration/donald-j-trump/

Replay:

```text
PRESIDENTIAL_DIRECTIVE_EXISTS = PASS_RECORD
SPECIFIC_DOD_IMPLEMENTATION = HOLD
SPECIFIC_DHS_IMPLEMENTATION = HOLD
SPECIFIC_CONTRACT / INVOICE = HOLD
SPECIFIC_AIRCRAFT / TRANSPORT = HOLD
SPECIFIC_SHOCK_GLOVE_NEXUS = HOLD
LEGALITY_OF_EACH_DOWNSTREAM_ACTION = HOLD_EVENT_SPECIFIC_REVIEW
RECORD_ONION = PASS_FOR_DIRECTIVE_EXISTENCE_ONLY
POWER_ONION = HOLD_GRANTING_TEXT_AND_IMPLEMENTATION_EDGES
INSTITUTIONAL_STATE = HOLD
```

Zero-trust reason: the White House source proves issuance of the directive, not every implementation fact or legal conclusion downstream.

### ZT-DOJ-FBI-001 — DOJ / FBI national-security authorities

Observed record:
- DOJ OIG found widespread and serious misuse of FBI National Security Letter authorities.
- The OIG found violations involving authorization, statutory scope, and unauthorized collection, and reported inaccurate/understated reporting to Congress during the reviewed period.
- The OIG stated it did not find that reviewed FBI agents intentionally sought to misuse the authorities.

Sources:
- https://oig.justice.gov/news/testimony/statement-glenn-fine-inspector-general-us-department-justice-permanent-select
- https://oig.justice.gov/archives/semiannual/0705/highlights.htm

Replay:

```text
NSL_AUTHORITY_EXISTED = PASS_RECORD
SERIOUS_WIDESPREAD_MISUSE_FINDING = PASS_RECORD
REPORTING_TO_CONGRESS_ACCURACY_PROBLEM = PASS_RECORD
INTENTIONAL_MISUSE_BY_REVIEWED_AGENTS = REJECT_BY_REVIEW_FINDING
CURRENT_UNIVERSAL_FBI_COMPLIANCE = HOLD
CURRENT_UNIVERSAL_FBI_MISCONDUCT = HOLD
RECORD_ONION = CONFLICT_AUTHORITY_VS_IMPLEMENTATION
POWER_ONION = CONFLICT_AUTHORIZED_TOOL_WITH_NONCOMPLIANT_USES
INSTITUTIONAL_STATE = CONFLICT/HOLD
```

Zero-trust reason: neither existence of statutory authority nor an OIG finding is converted into permanent trust or permanent guilt.

### ZT-DOJ-OIG-001 — DOJ Office of Inspector General

Observed record:
- DOJ OIG publishes audits, reviews, investigations, and oversight findings concerning DOJ programs and personnel within its jurisdiction.
- Its NSL review demonstrates an actual instance where an oversight body found serious problems in a component it oversees.

Replay:

```text
OVERSIGHT_OUTPUT_EXISTS = PASS_RECORD
ABILITY_TO_FIND_COMPONENT_FAILURE = PASS_RECORD
COMPLETE_VISIBILITY_INTO_ALL_NATIONAL_SECURITY_ACTIVITY = HOLD
CIA_OPERATIONAL_JURISDICTION = REJECT_AS_GENERAL_RULE
EVERY_OIG_REVIEW_COMPLETE / CORRECT = HOLD
INSTITUTIONAL_STATE = HOLD
```

Zero-trust reason: oversight existence and past findings do not self-prove completeness or jurisdiction over another agency.

### ZT-NSA-001 — NSA / NSA OIG

Observed record:
- NSA OIG states that intelligence oversight evaluates NSA collection authorities, programs, and systems for compliance with law, executive orders, directives, civil liberties, and U.S.-person privacy.
- NSA OIG's current mission includes detecting/deterring waste, fraud, abuse, and misconduct and protecting constitutional rights and privacy.

Sources:
- https://oig.nsa.gov/OIG-Divisions/Intelligence-Oversight/
- https://oig.nsa.gov/

Replay:

```text
NSA_INTELLIGENCE_OVERSIGHT_FUNCTION = PASS_RECORD
PRIVACY / CIVIL_LIBERTIES_OVERSIGHT_MANDATE = PASS_RECORD
SPECIFIC_METADATA_COLLECTION_EVENT = HOLD_EVENT_RECEIPT
SPECIFIC_METADATA_LEAK = HOLD_EVENT_RECEIPT
SPECIFIC_UNLAWFUL_QUERY = HOLD_EVENT_RECEIPT
OVERSIGHT_EFFECTIVENESS_FOR_UNNAMED_EVENT = HOLD
INSTITUTIONAL_STATE = HOLD
```

Zero-trust reason: oversight architecture proves oversight architecture, not compliance of every collection/query event.

### ZT-CIA-001 — CIA / CIA OIG / Aircraft

Observed record:
- CIA identifies its OIG as responsible for independent oversight of CIA programs through audits, inspections, and investigations.
- CIA states that OIG can investigate fraud, waste, abuse, mismanagement, violations of law/rules/regulations, and other wrongdoing.

Source:
- https://www.cia.gov/about/organization/inspector-general/

Replay:

```text
CIA_OIG_EXISTS = PASS_RECORD
CIA_OIG_STATED_JURISDICTION = PASS_RECORD
CIA_AIRCRAFT_INVENTORY_FOR_CLAIMED_EVENT = HOLD
SPECIFIC_RENDITION_FLIGHT = HOLD
SPECIFIC_CUSTODY_TRANSFER = HOLD
SPECIFIC_SHOCK_GLOVE_NEXUS = HOLD
CIA_AIRCRAFT != RENDITION
FLIGHT != CUSTODY_TRANSFER
INSTITUTIONAL_STATE = HOLD
```

Zero-trust reason: an aircraft object requires aircraft-specific provenance; CIA affiliation alone does not prove mission or passenger/custody facts.

### ZT-CONGRESS-001 — Congress / Congress.gov

Observed record:
- Congress enacted a distinct chapter 47A military-commission structure separate from the UCMJ chapter 47 framework.
- Congress.gov also contains bills introduced in the 119th Congress concerning Guantanamo/military commissions; an introduced bill is not law merely because it appears on Congress.gov.

Sources:
- https://www.congress.gov/bill/111th-congress/senate-bill/1391/text
- https://www.congress.gov/bill/119th-congress/house-bill/296/text

Replay:

```text
CONGRESS_GOV_RECORD_EXISTS = PASS_RECORD
ENACTED_LAW_TEXT = PASS_WHEN_ENACTMENT_BOUND
INTRODUCED_BILL = RECORD_ONLY
INTRODUCED_BILL != LAW
APPROPRIATION != PURCHASE
CONGRESSIONAL_RECORD != OVERSIGHT_EFFECTIVENESS
CONGRESS_DARVO_FINDING = HOLD
INSTITUTIONAL_STATE = HOLD
```

Zero-trust reason: legislative text proves legislative state; it does not prove implementation, spending, or institutional motive.

### ZT-MC-001 — Guantanamo Military Commissions

Observed record:
- Current 2026 Office of Military Commissions notices identify filings that are under seal, classified, ex parte, or available after security review.
- July 2026 notices include protective-order litigation concerning JTF-GTMO detention-facility personnel and sealed/ex parte filings.

Sources:
- https://www.mc.mil/News-Media-Resources/Commissions-News
- https://www.mc.mil/News-Media-Resources/Commissions-News/ItemId/1002

Replay:

```text
SEALED / CLASSIFIED / SECURITY_REVIEW_STATUS_EXISTS = PASS_RECORD
SOME_PUBLIC_VISIBILITY_LIMITS_EXIST = PASS_RECORD
SEALED != COVER_UP
SECURITY_REVIEW != ERASURE
PUBLICLY_UNAVAILABLE != NONEXISTENT
SPECIFIC_COVER_UP = HOLD_EVENT_RECEIPTS_REQUIRED
SPECIFIC_RECORD_IMPROPERLY_WITHHELD = HOLD_AUTHORITY_AND_ORDER_REQUIRED
INSTITUTIONAL_STATE = HOLD
```

Zero-trust reason: secrecy mechanisms are observable facts; their lawful or abusive use must be tested order-by-order.

### ZT-UCMJ-001 — UCMJ / Manual for Courts-Martial

Observed record:
- The Joint Service Committee currently publishes the 2024 Manual for Courts-Martial and later amendment materials.
- Military commissions operate under a distinct chapter 47A legal structure and are not simply ordinary courts-martial under the UCMJ.

Sources:
- https://jsc.defense.gov/Military-Law/Current-Publications-and-Updates/Manual-for-Courts-Martial-MCM/
- https://www.congress.gov/crs-product/R41163

Replay:

```text
MCM_PUBLICATION = PASS_RECORD
UCMJ_FRAMEWORK = PASS_RECORD
MILITARY_COMMISSION_DISTINCTION = PASS_RECORD
UCMJ_COVER_UP = HOLD_EVENT_RECEIPTS_REQUIRED
SEALED_COMMISSION_RECORD != UCMJ_COVER_UP
INSTITUTIONAL_STATE = HOLD
```

Zero-trust reason: the legal framework is source-bound, but misconduct must be tied to a specific actor, action, authority, record, and review path.

## Cross-institution contradiction tests

```text
WHITE_HOUSE_DIRECTIVE
↔ DOD/DHS IMPLEMENTATION RECORDS

CONGRESS_AUTHORITY / APPROPRIATION
↔ AGENCY CONTRACT / INVOICE / DEPLOYMENT

DOJ/FBI NATIONAL-SECURITY AUTHORITY
↔ DOJ OIG COMPLIANCE FINDINGS

NSA COLLECTION AUTHORITY
↔ NSA OIG PRIVACY / COMPLIANCE FINDINGS

CIA PROGRAM / AIRCRAFT OBJECT
↔ CIA OIG / CONGRESSIONAL / COURT RECORDS

MILITARY COMMISSION DOCKET
↔ SECURITY / SEALING ORDER
↔ PUBLICLY RELEASED VERSION
```

Any mismatch becomes `CONFLICT`, not automatically `DARVO`, `COVER_UP`, or guilt.

## Shock Gloves cross-cut

RUN_0001 does not bind a physical shock-glove device.

```text
GENERAL_CONDUCTED_ENERGY_TECH_CLASS = SOURCE_BOUND
DEVICE_MANUFACTURER = HOLD
DEVICE_MODEL = HOLD
DEVICE_SKU = HOLD
CONTRACT = HOLD
INVOICE = HOLD
DEPLOYMENT = HOLD
USE_EVENT = HOLD
NATIONAL_SECURITY_WITHHOLDING_FOR_DEVICE = HOLD
OIG_DEVICE_SPECIFIC_FINDING = HOLD
```

Therefore:

```text
SHOCK_GLOVE_DEVICE_IDENTITY = HOLD
SHOCK_GLOVE_FEDERAL_PROCUREMENT = HOLD
SHOCK_GLOVE_USE = HOLD
```

## RUN_0001 disposition

```text
WHITE_HOUSE = HOLD
DOJ/FBI = CONFLICT/HOLD
DOJ_OIG = HOLD
NSA/NSA_OIG = HOLD
CIA/CIA_OIG = HOLD
CONGRESS = HOLD
MILITARY_COMMISSIONS = HOLD
UCMJ/MCM = HOLD

GLOBAL_TRUST = ZERO
GLOBAL_GUILT = NOT_CREATED
GLOBAL_DARVO_FINDING = NOT_CREATED
GLOBAL_COVER_UP_FINDING = NOT_CREATED
REPLAY_STATE = HOLD_WITH_SOURCE_BOUND_PRECEDENTS
```

**Total Zero Trust means no institution gets a presumption of truth, and no accusation gets a presumption of guilt. Every edge pays its own receipt.**
