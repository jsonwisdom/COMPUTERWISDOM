# ALISON Alabama Audit — BoxD v0.1

Operator: `jaywisdom.base.eth`
Parent: `Double Onion Alabama DARVO / Maneuver Audit`
Classification: `LEGISLATIVE_SOURCE_REPLAY`
Authority created: `false`
Legal finding created: `false`

## Purpose

Use **ALISON / Alabama Legislature** as the source-of-law onion and **BoxD** as the preservation/receipt onion.

```text
ALISON = WHAT DID ALABAMA ACTUALLY ENACT / CODIFY / AMEND / SUPERSEDE?
BOXD   = WHAT EXACT SOURCE DID WE OBSERVE, WHEN, AT WHAT VERSION, AND WAS IT FROZEN/HASHED?
```

## Double Onion

### Onion A — ALISON / law state

```text
CENTER CLAIM
<- ALABAMA CONSTITUTION 2022
<- CODE OF ALABAMA
<- BILL TEXT
<- ACT TEXT
<- ACT DISPOSITION
<- EFFECTIVE DATE
<- AMENDMENT / REPEAL / SUPERSESSION
<- SESSION STATUS
<- RECEIPT
```

### Onion B — BoxD / source state

```text
CENTER CLAIM
<- SOURCE URL
<- SOURCE TYPE
<- OBSERVED TIMESTAMP
<- SECTION / BILL / ACT IDENTIFIER
<- DISPLAYED EFFECTIVE-DATE STATE
<- RAW BYTES IF CAPTURED
<- SHA-256 IF COMPUTED
<- ARCHIVED COPY / PDF IF CREATED
<- LOGGER ROW
<- READ-BACK VERIFICATION
```

The onions cross only through a BoxD receipt.

```text
ALISON_PAGE != FROZEN_BYTES
ALISON_TEXT != CASE_APPLICATION
CODE_SECTION != COURT_FINDING
BILL != LAW
ACT != CURRENT_CODE_WITHOUT_EFFECTIVE_DATE_CHECK
CURRENT_CODE != PRIOR_VERSION
BOXD_PRESENCE != LEGAL_TRUTH
HASH != SEMANTIC_TRUTH
```

## ALISON surfaces

- Alabama Legislature home / session state
- Code of Alabama
- Constitution of Alabama 2022
- Bill Search
- Acts
- Legal Division Act Disposition Tables, including disposition by Code section

## Version / time gate

ALISON exposes separate effective-date states on amended sections. Every time-sensitive legal replay therefore records:

```text
OBSERVED_DATE
SECTION
DISPLAYED_VERSION
EFFECTIVE_UNTIL
EFFECTIVE_FROM
AMENDING_ACT
```

Rule:

```text
EVENT_DATE < FUTURE_EFFECTIVE_DATE -> USE THEN-CURRENT TEXT
EVENT_DATE >= EFFECTIVE_DATE       -> USE NEW TEXT
```

`NO_SILENT_FUTURE_LAW_PROMOTION = TRUE`

## Alabama family / military watch set

- `§30-3-152` — joint-custody / best-interest factors.
- `§30-3-169.4` — relocation burden allocation and statutory burden shift.
- `§26-14-3` — mandatory child-abuse reporting; ALISON currently shows amendment by Act 2026-375 with separate effective states and a DHR-to-DoD Family Advocacy Program notification edge when a parent/guardian is determined to be military.
- `§30-3-9` — military-deployment custody-protection lane; source-bind the exact text before application.
- `Title 31` — Military Affairs and Civil Defense; keep separate from Title 30 domestic-relations authority.

## Maneuver test

When a private actor, lawyer, school, DHR worker, judge, employer, or military-adjacent actor invokes Alabama law:

```text
CLAIMED_RULE
-> EXACT_ALISON_SECTION
-> VERSION_AT_EVENT_DATE
-> ACT / AMENDMENT_HISTORY
-> ACT_DISPOSITION_CHECK
-> AUTHORITY / JURISDICTION
-> APPLICATION_TO_EVENT
-> RECEIPT
```

BoxD freezes the crossing.

## BoxD receipt schema

```json
{
  "artifact_id": "ALISON_ALABAMA_AUDIT_BOXD_V0_1",
  "source_surface": "ALISON",
  "source_url": "<url>",
  "source_type": "CONSTITUTION|CODE|BILL|ACT|DISPOSITION|SESSION",
  "identifier": "<section/bill/act>",
  "observed_minute": "<iso-minute>",
  "displayed_effective_state": "<text-or-null>",
  "amending_act": "<act-or-null>",
  "raw_bytes_captured": false,
  "sha256": null,
  "hash_status": "NOT_COMPUTED",
  "archived_copy_id": null,
  "readback_verified": false,
  "authority_created": false
}
```

## Promotion gates

```text
SOURCE_URL_BOUND = DISCOVERY
SOURCE_TEXT_READ = OBSERVED
VERSION_BOUND = REQUIRED_FOR_TIME_SENSITIVE_LAW
RAW_BYTES_CAPTURED = PRESERVATION
SHA256_COMPUTED = BYTE_INTEGRITY
ACT_DISPOSITION_RECONCILED = AMENDMENT_HISTORY
CASE_APPLICATION_PROVEN = SEPARATE_ANALYSIS
```

```text
SOURCE_URL_BOUND != SOURCE_BYTES_PROVEN
SOURCE_BYTES_PROVEN != LEGAL_INTERPRETATION_PROVEN
LEGAL_INTERPRETATION != COURT_HOLDING
```

## Current terminal

```text
ALISON_OFFICIAL_SURFACE = PASS
ALISON_CODE_VERSIONING_VISIBLE = PASS
ALISON_ACT_DISPOSITION_SURFACE = PASS
BOXD_PROTOCOL_BOUND = PASS
ALISON_SOURCE_BYTES_FROZEN = HOLD
ALISON_SOURCE_HASHES = HOLD_NOT_COMPUTED
CASE_SPECIFIC_APPLICATION = HOLD_EVENT_REQUIRED
DARVO_FINDING = HOLD
COORDINATION_FINDING = HOLD
AUTHORITY_CREATED = FALSE
```

## Official source anchors

- `https://alison.legislature.state.al.us/`
- `https://alison.legislature.state.al.us/code-of-alabama`
- `https://alison.legislature.state.al.us/constitution/search`
- `https://alison.legislature.state.al.us/bill-search`
- `https://alison.legislature.state.al.us/acts`
- `https://alison.legislature.state.al.us/legal-division-publications`

## BoxD boundary

BoxD preserves what was observed. It does not certify witness truth, legality of a ruling, actor intent, or correctness of a legal interpretation.
