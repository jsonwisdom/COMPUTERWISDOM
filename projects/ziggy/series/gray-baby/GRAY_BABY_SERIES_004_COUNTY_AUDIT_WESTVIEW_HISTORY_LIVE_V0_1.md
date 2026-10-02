# Gray Baby Series 004 — County Audit Layer

## Mission 004-001 — Westview Elementary History LIVE v0.1

Status: `LIVE_IN_DRAFT`  
History replay: `OPEN`  
Membrane intact: `TRUE`  
Authority created: `FALSE`

## Mission

Before auditing a levy line, prove what institution and building history we are talking about.

```text
LOOK → GUESS → SOURCE → RECEIPT → GAP → HOLD → REPLAY
```

## Boundary

Westview Elementary is a Platteville School District school currently listed at 1201 W. Camp Street, Platteville, Wisconsin. The district’s own referendum language identifies the School District of Platteville as spanning Grant, Iowa, and Lafayette Counties.

```text
SCHOOL_DISTRICT ≠ COUNTY_GOVERNMENT
COUNTY_AUDIT_LAYER = PROVENANCE_FRAME_NOT_JURISDICTION_CLAIM
DPI ≠ LOCAL_AUTHORIZATION
GAP ≠ FRAUD
ANOMALY ≠ MISCONDUCT
ASKING_FOR_SOURCE ≠ ACCUSATION
AUTHORITY_CREATED = FALSE
```

## LOOK

Current official district surfaces identify Westview Elementary as an active Platteville School District school. A district school-supply notice identifies Westview as serving grades 1–4.

## GUESS

It would be easy to treat the school’s origin year, additions, referenda, and current configuration as one clean story. The public record does not support doing that without qualification.

## SOURCE

Use official Platteville School District pages first for current identity, referendum scope, and completed district projects. Use local and construction reporting only for historical details the district’s current site does not reproduce.

## RECEIPT — history timeline

### 1966 / 1967 — opening year

`OPENING_YEAR = CONFLICTED / HOLD`

One local history report says Westview opened in 1967; another says it opened in 1966. Until an original board record, dedication program, construction record, or equivalent primary source resolves the conflict, the year stays `HOLD`.

- [SWNews4U — Moving fourth grade to Westview is favored option](https://www.swnews4u.com/local/education/moving-fourth-grade-to-westview-is-favored-option/)
- [SWNews4U — Decisions coming for school board on building project](https://www.swnews4u.com/local/education/decisions-coming-for-school-board-on-building-project/)

### 2013–14 — planning record reported

Secondary local reporting described Westview at roughly 234-student capacity and reported facility issues including multi-use space, entrance supervision, and drop-off circulation. This is reporting about the planning record, not the underlying planning record itself.

### 2015 — referendum history

The current Platteville School District referendum history says area voters approved facility projects that funded secure entrances at all four schools, an addition to Westview, and a new gymnasium.

- [Platteville School District — Referendum Information](https://www.platteville.k12.wi.us/page/referendum-information)

### 2015–16 — expansion and renovation

Construction reporting describes a `$9.6 million` Westview project totaling about `52,000 square feet`, including a `22,000-square-foot` expansion and `30,000-square-foot` renovation, with construction beginning in 2015 and completion in 2016. Those figures remain secondary-source bound until underlying contracts, board approvals, or audited capital records are replayed.

- [Daily Reporter — Westview expansion and renovation](https://dailyreporter.com/2016/10/05/building-blocks-westview-elementary-school-expansion-and-renovation/)

### 2022 — facility referendum

The district’s official referendum page records a ballot question authorizing up to `$36 million` in district facility work, including Westview parent-drive and parking safety upgrades. A later district article describes the referendum as supported by the community.

### 2023 — parent drive

The district announced that Westview’s new parent drive was open. This closes the `EXISTENCE_OF_PROJECT` edge, not the expenditure/audit edge.

- [Platteville School District — Westview New Parent Drive](https://www.platteville.k12.wi.us/article/1205981)

### Current identity

The district continues to list Westview Elementary at 1201 W. Camp Street. A district school-supply notice identifies Westview as grades 1–4.

- [Platteville School District — Current District surface](https://www.platteville.k12.wi.us/)
- [Platteville School District — Grades 1–4 school-supply notice](https://www.platteville.k12.wi.us/article/1662925)

## First gaps

```text
OPENING_YEAR = HOLD (1966 vs 1967 public-source conflict)
ORIGINAL_CONSTRUCTION_AUTHORIZATION = OPEN
2015_REFERENDUM_CERTIFIED_RESULT_RECEIPT = OPEN_FOR_PRIMARY_REPLAY
2015_16_WESTVIEW_CONTRACTS = OPEN
2015_16_WESTVIEW_FINAL_EXPENDITURE = OPEN
2015_16_WESTVIEW_AUDIT_RECONCILIATION = OPEN
2022_REFERENDUM_CERTIFIED_RESULT_RECEIPT = OPEN_FOR_PRIMARY_REPLAY
2023_PARENT_DRIVE_CONTRACT_FINAL_COST = OPEN
2023_PARENT_DRIVE_AUDIT_RECONCILIATION = OPEN
```

## HOLD

A historical gap is not evidence of wrongdoing. A secondary-source project cost is not an audited expenditure. A referendum description is not the same thing as a certified election result, contract, invoice, payment, or audit.

## REPLAY

```text
BUILDING_IDENTITY
  → ORIGINAL_AUTHORIZATION
  → ADDITION / RENOVATION
  → REFERENDUM
  → CONTRACT
  → PAYMENT
  → AUDIT
```

History first. Money second. Stop at the first unresolved edge. Resume only when a new public receipt appears.

## Parent-safe / public-safe rule

> “They said Westview opened then, cost this much, and voters approved that. Where does each part say that?”

## Canonical state

```text
SERIES = GRAY_BABY_004
MISSION = 004-001 / WESTVIEW_HISTORY_LIVE
HISTORY_REPLAY = LIVE
OPENING_YEAR = HOLD
PUBLIC_TRAIL_GAP = NEXT_AUDIT_EDGE
PARENT_SAFE = TRUE
PUBLIC_SAFE = TRUE
REPLAY_OPEN = TRUE
AUTHORITY_CREATED = FALSE
```
