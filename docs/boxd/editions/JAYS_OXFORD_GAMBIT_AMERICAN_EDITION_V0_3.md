# Jay's Oxford Gambit — American Edition v0.3

**Class:** public-record audit game / education / non-authority  
**MATHEMATICALLY_SELF_TAUGHT:** project identity label, not an academic credential  
**AUTHORITY_CREATED:** false  
**PROOF_INFERRED:** false

## Purpose
Run American institutional claims backward from rhetoric to record, authority, money/execution, and oversight. Dice route inquiry; receipts determine evidence state.

## Locked dice map

### D8 — Authority gate
1. CONSTITUTION
2. STATUTE
3. APPROPRIATION
4. EXECUTIVE_INSTRUMENT
5. AGENCY_IMPLEMENTATION
6. FOREIGN_AFFAIRS_OR_MILITARY_AUTHORITY
7. JUDICIAL_REVIEW
8. CONGRESSIONAL_OR_INSPECTOR_OVERSIGHT

### D4 — Quad Onion
1. RECORD_REALITY
2. AUTHORITY
3. EXECUTION_MONEY_DATA
4. OVERSIGHT_RECOVERY

### D6 — Evidence die
1. HOLD_TEST
2. SOURCE_TEST
3. OBSERVATION_TEST
4. BOUND_TEST
5. PROOF_ATTEMPT
6. ADVERSARIAL_REPLAY

### Citizen die
`2 = EXISTING_DATA_ONLY`

## Corrected supplied roll

```text
D8 = 6 -> FOREIGN_AFFAIRS_OR_MILITARY_AUTHORITY
D4 = 4 -> OVERSIGHT_RECOVERY
D6 = 5 -> PROOF_ATTEMPT
Citizen = 2 -> REQUEST_EXISTING_DATA_ONLY
```

The Pentagon/Israel board is therefore an authority-and-proof test, not a SOURCE roll and not an OBSERVATION_TEST roll.

## Minnesota default rule
A game default may close a turn. It cannot waive, toll, extinguish, or create a real legal deadline.

```text
GAME_STATE = DEFAULTED_FOR_ROUND
LEGAL_RIGHTS = UNAFFECTED_BY_GAME
REDUCTION_IN_GAME_INITIATIVE != LOSS_OF_STATUTORY_RIGHTS
```

## X/Y plane

### X — Version / time

```text
DELTA_T = t_acquired - t_declared
VERSION_DELTA = HASH(new_bytes) != HASH(old_bytes)
```

Do not use `(T_acquired - T_declared) / T_declared`; calendar timestamps are not a meaningful denominator for that ratio.

### Y — Authority layer

```text
Y1 RECORD
Y2 AUTHORITY
Y3 EXECUTION_MONEY_DATA
Y4 OVERSIGHT_RECOVERY
```

### Quadratic corpus pressure

```text
Q[x,y] = A[x,y] * (D[x,y] - R[x,y])^2 / P[t]
```

- `D` = officially declared/known records
- `R` = records actually retrieved and integrity-checked
- `A` = relevance/authority weight declared before scoring
- `P[t]` = declared population denominator for the tested proposition/year

`Q` measures documentary incompleteness pressure. `Q != corruption score`, `Q != guilt`, `Q != legality`.

## Federal FOIA correction
5 U.S.C. § 552 generally requires an agency **determination within 20 working days**, subject to statutory tolling and unusual-circumstances rules. Ten working days is not the ordinary initial-decision deadline.

A requester need not pre-argue agency exemptions. FOIA Exemption 6 concerns personal privacy in personnel, medical, and similar files; it is not a rule that financial execution records are automatically releasable.

### Safe financial-oversight targets
- enacted appropriations and public-law text
- congressional reprogramming notifications that are public/releasable
- public foreign-assistance notifications
- public contract/award identifiers
- GAO reports
- DoD OIG reports
- State/DoD administrative records that can lawfully be released
- non-operational staffing/budget tables where releasable

Do not request operational war plans, targeting data, troop-movement details, classified intelligence, or tactical vulnerabilities.

## Public Accountability Page
This replaces any "shame" or "handcuff" page concept. The system does not create humiliation, punishment, or vigilante pages for politicians, judges, police, or private people. It may create neutral public-record accountability pages using one schema for everyone:

```text
ACTOR / OFFICE
JURISDICTION
PUBLIC_STATEMENT
SOURCE_URI
SOURCE_DATE
RAW_BYTES_OR_HASH_STATUS
AUTHORITY_SOURCE
MONEY_OR_EXECUTION_EDGE
OVERSIGHT_BODY
RECORD_REQUEST
RESPONSE_DATE
REDACTION_BASIS
APPEAL_OR_REVIEW_PATH
CORRECTION
FINAL_PUBLIC_FINDING
EVIDENCE_STATE = PROVEN | BOUND | HOLD | CONFLICT | REJECT
```

Hard rules:

```text
PUBLIC_OFFICIAL != PUBLIC_TARGET
ALLEGATION != FINDING
ARREST != GUILT
REDACTION != CONCEALMENT
NO_RESPONSE != DARVO
AUDIT_GAP != FRAUD
COURT != EXECUTIVE_COMMAND
POLICE_POWER != PERSONAL_AUTHORITY
PUBLIC_RECORD != LICENSE_TO_HARASS
```

FAFO remains **FIND ALGORITHMIC FACTS & OUTPUTS** with no retaliation or punishment meaning.

## American Edition replay

```text
CLAIM
-> ORIGINAL_WORDING
-> SOURCE + DATE + JURISDICTION
-> OFFICE_HELD
-> LEGAL_AUTHORITY
-> APPROPRIATION / MONEY_EDGE
-> EXECUTION_RECEIPT
-> OVERSIGHT / COURT / IG
-> VERSION_DELTA
-> COUNTER_RECEIPT
-> REVERSE_REPLAY
-> PROVEN | BOUND | HOLD | CONFLICT | REJECT
```

## Standing order
**SHOW ME THE EDGE.**

Ideas may travel freely. Authority does not. Dice route inquiry. Receipts determine evidence state.
