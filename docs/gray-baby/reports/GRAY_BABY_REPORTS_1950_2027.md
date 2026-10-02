# Gray Baby Reports — 1950–2027

**Series:** `GRAY_BABY_REPORTS_1950_2027`  
**Version:** `v0.1`  
**Class:** verification ledger / historical-context index  
**Authority created:** false  
**Implementation state:** branch implementation; merge not implied

## Purpose

This series gives the years **1950 through 2027** an explicit evidence span without claiming that a historical JASON, DARPA, FAS, medical, UAP, or other object named **Gray Baby** existed in any of those years.

A year or range appearing here is a review slot, not an existence claim.

```text
NO_PUBLIC_RECEIPT != CLASSIFIED
ABSENCE            != NONEXISTENCE
CONTEXT            != PROVENANCE
PARALLEL_FUNCTION  != SHARED_IDENTITY
JASON              != GRAY_BABY
DARPA              != GRAY_BABY
FAS_SGP            != GRAY_BABY
UAP                != GRAY_BABY
AUTHORITY_CREATED   = FALSE
```

## Coverage map

| Year / range | Record class | Receipt state | Gray Baby ↔ JASON binding |
|---|---|---|---|
| 1950–1959 | `PRE_JASON` | JASON did not yet exist; context slots only | `NONE` |
| 1960 | `CONTEXT_EVENT` | JASON begins in 1960; institutional context only | `NONE` |
| 1961–1990 | `UNPOPULATED` | No year-specific receipt entered in v0.1 | `NONE` |
| 1991 | `CONTEXT_EVENT` | FAS Project on Government Secrecy begins; public receipt-layer context | `NONE` |
| 1992–1999 | `UNPOPULATED` | No year-specific receipt entered in v0.1 | `NONE` |
| 2000 | `CONTEXT_EVENT` | Secrecy News publication begins under FAS SGP | `NONE` |
| 2001 | `UNPOPULATED` | No year-specific receipt entered in v0.1 | `NONE` |
| 2002 | `CONTEXT_EVENT` | Public JASON–DARPA membership-control dispute; contract pipe later moves to DDR&E | `NONE` |
| 2003–2008 | `UNPOPULATED` | No year-specific receipt entered in v0.1 | `NONE` |
| 2009 | `CONTEXT_EVENT` | `JSR-08-146` S&T for National Security enters FOIA/withholding receipt trail | `NONE` |
| 2010 | `CONTEXT_EVENT` | Appeal/public-release chain for `JSR-08-146` | `NONE` |
| 2011 | `CONTEXT_EVENT` | JASON space-weather withholding/release episode appears in Secrecy News | `NONE` |
| 2012–2014 | `UNPOPULATED` | No year-specific receipt entered in v0.1 | `NONE` |
| 2015 | `CONTEXT_EVENT` | FAS JASON title index lists Counterspace `15-Task-010` as restricted FOUO and appendix `15-Task-010A` as classified SCI | `NONE` |
| 2016 | `UNPOPULATED` | No Gray Baby public JASON title entered | `NONE` |
| 2017 | `CONTEXT_EVENT` | `JSR-16-Task-003` publicly released; Secrecy News issue dated 2017-01-11 covers the report | `NONE` |
| 2018 | `CONTEXT_EVENT` | DARPA COMPASS gray-zone program and AI Next campaign are separate public programs | `NONE` |
| 2019 | `CONTEXT_EVENT` | JASON IDIQ/contract controversy; institutional vehicle context only | `NONE` |
| 2020 | `CONTEXT_EVENT` | Public JASON reporting continues; no Gray Baby public JASON title established here | `NONE` |
| 2021 | `CONTEXT_EVENT` | FAS Project on Government Secrecy closes its 1991–2021 named-project run and remains archived | `NONE` |
| 2022–2025 | `UNPOPULATED` | No year-specific receipt entered in v0.1 | `NONE` |
| 2026 | `PROJECT_ARTIFACT` | Gray Baby exists in COMPUTERWISDOM as a documentation / verification architecture and gap-observer project label | `NONE` |
| 2027 | `FUTURE_RESERVED` | Future year; no event asserted | `NONE` |

## Corrected 2017 receipt

A prior provisional note said no dedicated Secrecy News issue had been located for `JSR-16-Task-003`. The public archive contains **Secrecy News, Volume 2017, Issue No. 4, January 11, 2017**, covering the JASON AI report.

This ledger therefore records:

```text
JSR-16-TASK-003_REPORT = VERIFIED_PUBLIC
SECRECY_NEWS_2017_01_11 = VERIFIED_PUBLIC_RECEIPT
GRAY_BABY_BINDING        = NONE
```

## Evidence classes

### `PRE_JASON`
The year predates JASON's 1960 beginning. Nothing about the slot creates a retroactive JASON or Gray Baby object.

### `CONTEXT_EVENT`
A public institutional, report, FOIA, contracting, or program event is useful to the surrounding research. It remains a separate object unless a primary artifact explicitly binds it.

### `UNPOPULATED`
No year-specific receipt has been entered in this version. This means only **not entered here**.

```text
UNPOPULATED != CLASSIFIED
UNPOPULATED != NOTHING_EXISTED
UNPOPULATED != GRAY_BABY_EXISTED
```

### `PROJECT_ARTIFACT`
The internal Gray Baby project is documented in this repository. Repository provenance does not back-propagate into earlier government records.

### `FUTURE_RESERVED`
The slot exists for schema continuity only. No prediction or historical statement is made.

## Source map

Primary/public receipts used for populated context rows:

- JASON 2017 AI report: `https://irp.fas.org/agency/dod/jason/ai-dod.pdf`
- Secrecy News 2017-01-11 issue: `https://sgp.fas.org/news/secrecy/2017/01/011117.html`
- FAS JASON report shelf: `https://irp.fas.org/agency/dod/jason/`
- FAS Project on Government Secrecy archive: `https://sgp.fas.org/`
- Secrecy News archive: `https://sgp.fas.org/news/secrecy/index.html`
- Physics Today, 2002 JASON/DARPA membership controversy: `https://physicstoday.aip.org/news/jason-courts-new-sponsor-after-darpa-cancels-contract`
- DARPA COMPASS: `https://www.darpa.mil/news/2018/gray-zone-activity`
- DARPA AI Next: `https://www.darpa.mil/news/2018/next-wave-ai`
- Existing internal project definition: `../README.md`

## Negative-evidence state

```text
GRAY_BABY_PUBLIC_JASON_TITLE          = NOT_FOUND_IN_CURRENT_RECORD
GRAY_BABY_PUBLIC_DARPA_PROGRAM        = NOT_FOUND_IN_CURRENT_RECORD
CLASSIFIED_NICKNAME_EXISTENCE         = UNKNOWN
GRAY_BABY_FAS_SGP_BINDING             = NONE
GRAY_BABY_UAP_BINDING                 = NONE
GRAY_BABY_MEDICAL_BINDING             = NONE
AUTHORITY_CREATED                      = FALSE
```

`NOT_FOUND_IN_CURRENT_RECORD` is deliberately weaker than `DOES_NOT_EXIST`.

## Record contract

Future annual records must conform conceptually to `GRAY_BABY_REPORT_RECORD_SCHEMA_V0_1.json` and preserve:

```text
ONE YEAR / RECORD
ONE CLAIM CLASS
SOURCE TYPE DECLARED
NO SILENT BINDING
CORRECTIONS FIRST-CLASS
AUTHORITY_CREATED = FALSE
```

## Merge boundary

This file is an implementation artifact on a feature branch. Its existence does not itself promote the report series to the repository's protected/default branch. Human review and merge remain separate events.
