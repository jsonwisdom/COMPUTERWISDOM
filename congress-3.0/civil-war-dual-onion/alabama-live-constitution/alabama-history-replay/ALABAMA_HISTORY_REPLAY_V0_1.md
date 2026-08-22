# AlabamaHistoryReplay v0.1

**Parent:** Double Onion Civil War Alabama Live Constitution v0.1  
**Classification:** `SOURCE_BOUND_HISTORICAL_CONSTITUTIONAL_REPLAY`  
**Authority created:** `false`

## Purpose

Replay Alabama history as dated state changes instead of one continuous story.

```text
EVENT
-> SOURCE AT TIME
-> CLAIMED AUTHORITY AT TIME
-> ACTION
-> HUMAN CONSEQUENCE
-> LATER AMENDMENT / SUPERSESSION
-> PRESENT CONSTITUTIONAL STATE
-> RECEIPT
```

## Bound Civil War / Reconstruction spine

### January 11, 1861

Alabama Department of Archives and History preserves Alabama's Ordinance of Secession.

```text
OBJECT = HISTORICAL_PRIMARY_SOURCE
DATE = 1861-01-11
PRESENT_AUTHORITY = FALSE
```

### 1861 Alabama Constitution

Alabama Department of Archives and History preserves the 1861 state constitution.

```text
OBJECT = HISTORICAL_CONSTITUTIONAL_TEXT
CURRENT_LAW_STATUS = REQUIRES_SUPERSESSION_REPLAY
PRESENT_AUTHORITY_FROM_1861_TEXT_ALONE = FALSE
```

### Reconstruction amendments

Congress.gov / Constitution Annotated supplies the federal constitutional state-change rail for the Thirteenth, Fourteenth, and Fifteenth Amendments.

```text
THIRTEENTH = CONSTITUTIONAL_STATE_CHANGE
FOURTEENTH = CONSTITUTIONAL_STATE_CHANGE
FIFTEENTH = CONSTITUTIONAL_STATE_CHANGE
WAR_END != REPLAY_END
```

The source rail records Alabama approval of the Thirteenth Amendment on 1865-12-02 and the Fourteenth Amendment on 1868-07-13.

## Historical replay gates

```text
1. WHAT EXACT EVENT?
2. WHAT DATE?
3. WHAT PLACE?
4. WHAT PRIMARY SOURCE?
5. WHO HAD WHAT CLAIMED AUTHORITY THEN?
6. WHAT ACTION ACTUALLY OCCURRED?
7. WHAT HUMAN CONSEQUENCE IS SOURCE-BOUND?
8. WHAT LATER LAW / AMENDMENT CHANGED THE STATE?
9. WHAT PART, IF ANY, OPERATES TODAY?
10. WHAT RECEIPT PROVES EACH EDGE?
```

## ReverseReplay

Start with a modern claim and walk backward:

```text
MODERN CLAIM
<- CURRENT AUTHORITY
<- CURRENT TEXT
<- PRECEDENT / AMENDMENT / SUPERSESSION
<- PRIOR TEXT
<- HISTORICAL ACTION
<- PRIMARY SOURCE
```

If the chain stops, the modern claim stops.

## Membranes

```text
HISTORICAL_RECORD != CURRENT_AUTHORITY
SECESSION_CLAIM != CURRENT_STATE_STATUS
OLD_CONSTITUTION != CURRENT_LAW_WITHOUT_REPLAY
HISTORY != GENEALOGY
HISTORICAL_ACTOR != MODERN_DESCENDANT
CIVIL_WAR_CONTEXT != MODERN_CIVIL_WAR
OFFICIAL_RECORD != MORAL_CORRECTNESS
SOURCE != COMPLETE_CAUSAL_ACCOUNT
CONFLICT != FORCED_EQUIVALENCE
AUTHORITY_CREATED = FALSE
```

## Official anchors

- Alabama Department of Archives and History — Ordinance of Secession, January 11, 1861
- Alabama Department of Archives and History — Alabama Constitution of 1861
- Congress.gov / Constitution Annotated — Civil War / Reconstruction Amendments

Terminal states: `PASS | HOLD | CONFLICT | REJECT`.
