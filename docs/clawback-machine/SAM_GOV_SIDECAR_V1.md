# SAM.GOV SIDECAR V1

**Parent:** CLAWBACK_MACHINE_PROTOCOLS_V1  
**Class:** federal award / procurement / entity / exclusion / responsibility replay sidecar  
**Authority created:** false  
**Verdict created:** false  
**Runtime bind:** not yet bound

## Purpose

Add SAM.gov as a first-class federal-award surface inside ClawBackMachine so public replay can distinguish entity identity, eligibility, opportunities, award records, exclusions, responsibility/qualification records, and procurement clocks from the underlying agency action.

SAM.gov is the U.S. Government's official System for Award Management and is managed within GSA's Integrated Award Environment. It supports entity registration and Unique Entity IDs, entity/exclusion searches, contract opportunities, contract award data, assistance listings, reporting, and public data/API access.

## Position in the graph

```text
AGENCY NEED
→ PROCUREMENT AUTHORITY
→ NOTICE / SOLICITATION
→ OFFEROR / ENTITY
→ SAM ENTITY + UEI
→ RESPONSIBILITY / EXCLUSION CHECK
→ AWARD / MODIFICATION
→ PERFORMANCE / PAYMENT / CLOSEOUT
→ PUBLIC DATA SURFACES
→ CLAWBACK REPLAY
```

SAM.gov is a source surface for parts of that chain. It is not the whole chain and it is not the legal authority that caused every underlying agency decision.

## Required SAM atoms

```text
sam_record_id
record_class
agency
subtier
contracting_office
notice_id
award_id
uei
cage_code
entity_legal_name
naics
psc
set_aside
contracting_officer
published_clock
modified_clock
response_clock
award_clock
inactive_clock
source_url
attachments[]
related_notices[]
exclusion_state
responsibility_qualification_state
source_hash
capture_clock
unknowns[]
```

## Record classes

```text
ENTITY_REGISTRATION
UNIQUE_ENTITY_ID
EXCLUSION
RESPONSIBILITY_QUALIFICATION
CONTRACT_OPPORTUNITY
SOURCES_SOUGHT
SPECIAL_NOTICE
SOLE_SOURCE_NOTICE
SOLICITATION
AWARD_NOTICE
AWARD_DATA
SUBAWARD_REPORT
SERVICE_CONTRACT_REPORT
ASSISTANCE_LISTING
```

## Hard membranes

```text
SAM_LISTING != FEDERAL_ENDORSEMENT
ACTIVE_REGISTRATION != CONTRACT_AWARD
UEI != ELIGIBILITY_BY_ITSELF
OPPORTUNITY != AWARD
AWARD_NOTICE != PERFORMANCE_PROOF
AWARD_NOTICE != PAYMENT_PROOF
EXCLUSION != CRIMINAL_CONVICTION
NO_EXCLUSION != FITNESS_CERTIFICATION
RESPONSIBILITY_RECORD != GLOBAL_TRUTH
SAM_SEARCH_MISS != NO_CONTRACT
SAM_RECORD != AGENCY_FILE
SAM_PUBLIC_RECORD != ALL_NONPUBLIC_PROCUREMENT_RECORDS
CONTRACTING_OFFICE != PROGRAM_OFFICE
NOTICE_DATE != AWARD_DATE != PERFORMANCE_DATE != PAYMENT_DATE
AUTHORITY_CREATED = FALSE
```

## ClawBack mapping

```text
WAYBACK_MACHINE
  ↳ prior opportunity versions
  ↳ amendments
  ↳ inactive/active state transitions
  ↳ related notices
  ↳ award modifications

FULL_MATH_AUDIT
  ↳ searched terms
  ↳ agency filters
  ↳ date filters
  ↳ excluded results
  ↳ search misses
  ↳ attachment availability
  ↳ unresolved identifiers

WIKIATOM_BOMB
  ↳ ENTITY
  ↳ AGENCY
  ↳ CONTRACTING_OFFICE
  ↳ AUTHORITY
  ↳ NOTICE
  ↳ AWARD
  ↳ MONEY
  ↳ EXCLUSION
  ↳ RESPONSIBILITY
  ↳ CLOCK
  ↳ ATTACHMENT
  ↳ UNKNOWN

DELTA_LAYER
  ↳ notice amendment
  ↳ due-date change
  ↳ scope change
  ↳ set-aside change
  ↳ award-state change
  ↳ entity-state change
  ↳ exclusion-state change
```

## Live Treasury/OCC/FinCEN use

For a Treasury/OCC/FinCEN rail, SAM.gov is the procurement sidecar, not a substitute for OCC, FinCEN, OFAC, DOJ, Treasury, court, or on-chain receipts.

```text
TREASURY / OCC / FINCEN OBJECT
→ search SAM by agency + office + notice/award/entity identifiers
→ freeze returned notices and attachments
→ bind UEI / entity / NAICS / PSC / contracting office
→ reconstruct amendments and award transitions
→ compare with agency-side records
→ emit PASS | DELTA | HOLD
```

Questions the sidecar can test:

```text
WAS A PROCUREMENT NOTICE PUBLISHED?
WHICH OFFICE PUBLISHED IT?
WHAT DID THE NOTICE SAY AT EACH VERSION?
WAS IT COMPETED / SET ASIDE / SOLE SOURCE?
WHICH ENTITY IDENTIFIER WAS USED?
WAS AN AWARD NOTICE PUBLISHED?
DID THE NOTICE OR AWARD CHANGE?
WERE EXCLUSION OR RESPONSIBILITY RECORDS PRESENT?
WHAT ATTACHMENTS WERE PUBLIC?
WHAT REQUIRED PROCUREMENT RECEIPT IS STILL MISSING?
```

Questions SAM.gov alone cannot answer:

```text
DID AGENCY LEADERS DIRECT THE PROCUREMENT?
DID A CRIME OCCUR?
DID AN AWARD PERFORM SUCCESSFULLY?
DID PAYMENT ACTUALLY SETTLE?
DID A CONTRACTOR CAUSE A POLICY DECISION?
DID TREASURY OBSERVE A SPECIFIC PRIVATE TRANSACTION?
```

## Live public examples observed during integration

1. FinCEN procurement surface: SAM.gov Special Notice `SS-FIN-25-017` stated that Bureau of the Fiscal Service Procurement, on behalf of FinCEN, intended a sole-source award to AnChain.ai for crypto-wallet / smart-contract intelligence capabilities. This proves a public procurement notice exists; it does not prove a relationship to any specific USD1 transaction.

2. OCC procurement surface: SAM.gov opportunity `2031JW26Q00068` identified Treasury / Office of the Comptroller of the Currency / Comptroller of Currency Acquisitions as the contracting chain for a macroeconomic forecasting tool. This demonstrates that OCC procurement lineage is visible on SAM.gov; it does not prove that every OCC operational or regulatory action is procurement-derived.

## Source pointers

- SAM.gov — About This Site: https://sam.gov/about/this-site
- SAM.gov — Entity Information: https://sam.gov/entity-information
- SAM.gov — Contract Opportunities: https://sam.gov/opportunities
- SAM.gov — Exclusion Types: https://sam.gov/entity-information/resources/exclusion-types
- GSA — SAM.gov / acquisition resources: https://www.gsa.gov/resources/how-we-help-government-customers
- GSA — Entity registration / UEI overview: https://www.gsa.gov/small-business/find-opportunities/register-your-business
- GSA Open Technology — Contract Awards API: https://open.gsa.gov/api/contract-awards/
- SAM.gov — FinCEN AnChain.ai notice SS-FIN-25-017: https://sam.gov/workspace/contract/opp/3ea51ee0823244e49256a4ee256c6e96/view
- SAM.gov — OCC opportunity 2031JW26Q00068: https://sam.gov/workspace/contract/opp/96234a1218554c219833215b785cd4a8/view

## State

```text
SAM_GOV_SIDECAR_V1 = DEFINED
SAM_GOV_PUBLIC_SURFACE = BOUND
SAM_GOV_LIVE_QUERY_OPERATOR = NOT_YET_BOUND
SAM_GOV_API_RUNTIME = NOT_YET_BOUND
TREASURY_USD1_SPECIFIC_PROCUREMENT_EDGE = HOLD
AUTHORITY_CREATED = FALSE
NO_FAKE_GREEN = TRUE
```
