# DOJ CrissCross PlayBookPincer — Glossary v0.1

**Author label:** `jaywisdom.base.eth`  
**Classification:** public-record audit vocabulary  
**Authority created:** `false`

> These labels are analytical mechanics, not Department of Justice terminology, findings, accusations, or grants of authority.

## Core membrane

```text
REPLAY != VERDICT
AUDIT != ACCUSATION
OFFICIAL_STATEMENT != PROOF
NO CLAIM OUTRANKS ITS RECEIPTS
PERSON != OFFICE != AUTHORITY
AUTHORITY_CREATED = FALSE
```

## Glossary

### CRISSCROSS
Compare the same claim across independent institutional surfaces: DOJ ↔ FBI ↔ OIG ↔ Congress ↔ courts ↔ archives.

### PLAYBOOK
Reusable sequence for testing a claim without deciding guilt in advance.

### PINCER
Attack a claim from two directions:

```text
TOP_DOWN: LAW → AUTHORITY → OFFICIAL → ACTION → RECORD
BOTTOM_UP: RECORD → ACTION → OFFICIAL → AUTHORITY → LAW
```

### REVERSE_REPLAY
Begin with the newest statement or document and reconstruct its provenance backward.

### FORWARD_REPLAY
Begin with original authority/event and follow subsequent actions forward.

### CLAIM_NODE
Exact proposition being tested. Never silently broaden it.

### SOURCE_NODE
Document, testimony, dataset, filing, video, release, or other evidence supporting a claim.

### AUTHORITY_NODE
Statute, regulation, court order, delegation, office, or constitutional power authorizing an action.

### ACTION_NODE
What an identified actor actually did.

### RECEIPT_NODE
Evidence that the action occurred.

### ACTOR_BINDING
Proof connecting a particular person or office to an action.

### OFFICE_BINDING
Separates the human from the governmental office:

```text
PERSON != OFFICE != AUTHORITY
```

### TODDBLANCHE_APPROVED
Custom checkpoint meaning: there is source-bound evidence that Todd Blanche personally or officially approved the specific action.

Absent that receipt → `HOLD`.

`TODDBLANCHE_APPROVED` is not itself evidence that approval occurred.

### BONDI_LANE
Actions, statements, directives, or releases attributable specifically to Pam Bondi during the time period being replayed.

Attribution and office state must be bound to date and source.

### TRUMPFILES
Research label for Epstein-record claims involving Donald Trump. It is not an official DOJ evidence category and does not itself imply wrongdoing.

### EPSTEIN_FILES
Public-record corpus relating to Jeffrey Epstein investigations, litigation, evidence, releases, redactions, and oversight.

### RELEASE_STATE
Distinguishes:

```text
IDENTIFIED != COLLECTED != REVIEWED != REDACTED != RELEASED != COMPLETE
```

### REDACTION_GATE
Ask what legal authority permitted information to be withheld and whether the stated reason is documented.

### MISSING_RECORD
Absence from a release.

```text
MISSING != DESTROYED != CONCEALED
```

### 702_SWITCHEROO
Custom anomaly flag for a suspected authority substitution involving FISA §702 or another surveillance authority.

It remains `HYPOTHESIS_ONLY` until the actual legal authority and records are bound.

### SUPERSECRET_SYNTAX
Parsing mechanic for separating public facts, sealed/classified possibilities, inference, and unknowns without pretending access to secret systems.

### INTERNAL_THREAT_FLAG
Audit hypothesis requiring evidence.

```text
FLAG != THREAT_FINDING != CRIME
```

### OIG_GATE
Independent Inspector General evidence lane:

```text
announcement → scope → methodology → report → findings → recommendations → agency response
```

### CONGRESSIONAL_GATE
Hearing/testimony/subpoena/report lane.

```text
HEARING != FACT_PROVEN
```

### COURT_GATE
Complaint → evidence → ruling → appeal.

```text
ALLEGATION != JUDICIAL_FINDING
```

### SWITCHEROO_DETECTOR
Tests whether names, offices, authorities, dates, document states, or evidentiary standards changed mid-chain.

### DIRTY_MATH
State/provenance collapse requiring reconciliation; not corruption by itself.

### PINKY_PROMISE
Every promoted claim must preserve its source, authority, action, receipt, and uncertainty state.

## Terminals

```text
PASS     = chain reconciles
HOLD     = evidence missing
CONFLICT = valid records disagree
REJECT   = evidence contradicts claim
```

## Promotion rule

A glossary term may classify or route evidence. A glossary term may not create the evidence it requests.

```text
CUSTOM_LABEL != OFFICIAL_DOJ_TERM
FLAG != FINDING
CHECKPOINT != APPROVAL
MISSING != CONCEALED
REPLAY != VERDICT
```

## Master rule

```text
REPLAY != VERDICT
AUDIT != ACCUSATION
OFFICIAL_STATEMENT != PROOF
NO CLAIM OUTRANKS ITS RECEIPTS
```
