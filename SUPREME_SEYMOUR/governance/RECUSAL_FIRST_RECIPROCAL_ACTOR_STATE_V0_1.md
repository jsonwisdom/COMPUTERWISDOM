# RECUSAL_FIRST_RECIPROCAL_ACTOR_STATE_V0_1

STATUS = PROVISIONAL_INTEGRATION
AUTHORITY_CREATED = FALSE
FINAL_DECISION = HUMAN
SPINE = ACTOR_STATE -> OBJECT_IDENTITY -> RESOLUTION -> EVIDENCE -> POSTURE -> AUTHORITY
RULE = ENS_BEFORE_DNS
COLLABORATION_NOT_COLLISION = TRUE

## Purpose

Fold a reciprocal actor-state preflight into the U.S. Courts Hierarchy Watch so every judicial-recusal event can be evaluated on two separate rails:

1. the judicial actor-state rail; and
2. the initiating government/litigant actor-state rail.

Auditing the initiating actor does not negate the complaint. The complaint does not establish the initiating actor's impartiality. The rails may collaborate through shared case identity and receipts, but they must not collapse.

## Receipt-status boundary

The receipt classifications below are typed against current evidence. Two prior softer labels were upgraded only after direct primary-source readback: the DOJ Attorney General biography for prior representation and the DOJ Sept. 30, 2026 press release/complaint for the Minnesota recusal filing. Source type and corroboration count remain distinct properties.

| Assertion | Receipt status |
| --- | --- |
| Todd Blanche sworn in as Attorney General on Aug. 10, 2026 | PRIMARY (multiple sources) |
| DOJ Ethics Program Order dated Sept. 1, 2026 | PRIMARY (DOJ) |
| DAG or delegee is Agency Designee for the AG | PRIMARY |
| Only the President may grant the AG a financial-conflict waiver | PRIMARY |
| Formal ethics determination uses DDAEO recommendation then Agency Designee written decision | PRIMARY |
| DOJ sought Minnesota judges' recusal Sept. 30, 2026 | PRIMARY (DOJ press release + linked complaint) |
| OPR 2022 Investigative Summary 7 found recusal-boundary misconduct involving briefings | PRIMARY |
| Blanche prior Trump criminal representation | PRIMARY (DOJ Attorney General biography, updated Aug. 14, 2026) |

## Reciprocal rail

```text
JUDICIAL_RECUSAL_EVENT
        |
        +--> ACTOR_STATE (judge) --> normal typed spine
        |
        +--> RECIPROCAL_ACTOR_PREFLIGHT (government / litigant)
                  |
                  +--> ACTOR_STATE (AG / DOJ official / requesting party)
                            |
                            +--> RECUSAL_PREFLIGHT
                            +--> ETHICS_REVIEW
                            +--> DETERMINATION
```

### Invariant

```text
INITIATING_ACTOR_AUDIT != COMPLAINT_NEGATION
COMPLAINT != INITIATING_ACTOR_IMPARTIALITY
COLLABORATION != COLLISION
```

## RECUSAL_FIRST state machine

### PRECHECK

Function: prevention.

Output type:

```text
CONFLICT_INVENTORY
```

Screen matter-specific financial interests, former clients/employers, personal or political relationships, parties, and existing ethics commitments.

### RECUSAL_DECISION

Function: boundary creation.

Output type:

```text
RECUSAL_SCOPE {
  matter,
  state_interval,
  authority_transfer
}
```

Constraint:

```text
RECUSAL != GENERAL_DISQUALIFICATION_FROM_OFFICE
```

### INFORMATION_FIREWALL

Function: preserve the recusal boundary after the decision.

Output type:

```text
FIREWALL_STATE {
  briefings_blocked,
  access_revoked,
  information_flow_status
}
```

Invariant:

```text
SITUATIONAL_AWARENESS != FIREWALL_COMPLIANCE
```

### RETRIGGER

Function: detect a changed actor state.

Triggers may include a new party, new matter, new financial relationship, changed role, changed recusal interval, newly discovered relationship, or changed authority.

```text
ACTOR_STATE[t+1]
  -> NEW_RECUSAL_PREFLIGHT
  -> NEW_RESOLUTION_CYCLE
```

A later actor-state change does not rewrite the earlier resolution cycle.

### MISCONDUCT_AUDIT

Function: independent accountability and routing.

Output type:

```text
OPR_OIG_ROUTING {
  forum,
  jurisdiction,
  evidence_state,
  next_gate
}
```

Do not collapse professional-misconduct review, systemic review, ethics determination, disciplinary action, or criminal process.

## Reciprocal trigger

```text
DOJ_REQUESTS_OTHER_ACTOR_RECUSAL
        |
        +--> JUDGE_RAIL: JUDICIAL_RECUSAL_EVENT
        |
        +--> DOJ_RAIL: RECIPROCAL_ACTOR_PREFLIGHT
```

Example typing for the government/litigant rail:

```yaml
actor_class: PARTY
actor_role: Attorney General / DOJ
relationship_fact: PRIOR_REPRESENTATION_VERIFIED
conflict_state: UNKNOWN
composition_delta: NOT_APPLICABLE
affects_resolution: UNRESOLVED
```

The verified prior-representation fact is a screening input only. It does not itself establish a matter-specific conflict, misconduct, or a required recusal outcome.

## AG recusal authority path

```text
AG_ACTOR_STATE
        |
        +--> AG_SELF_APPROVES_FORMAL_DETERMINATION? INVALID
        |
        +--> AGENCY_DESIGNEE = DAG_OR_DELEGEE
                   |
                   +--> STEP_1 = DDAEO_WRITTEN_RECOMMENDATION
                   |
                   +--> STEP_2 = AGENCY_DESIGNEE_WRITTEN_DETERMINATION
                                  |
                                  +--> FINANCIAL_CONFLICT_WAIVER = PRESIDENT_ONLY
```

Invariant:

```text
ETHICS_RECOMMENDATION != ETHICS_DETERMINATION
RECUSALS_FIRST -> AUTHORITY_SECOND
```

## Integration into the U.S. Courts Hierarchy Watch

Every admitted JUDICIAL_RECUSAL_EVENT now opens, as a separate rail:

```text
RECIPROCAL_ACTOR_PREFLIGHT
```

The watcher should track:

- actor identity and class;
- matter-specific conflict inventory;
- recusal scope and interval;
- authority-transfer path;
- information-firewall state;
- retrigger events;
- ethics recommendation versus formal determination;
- OPR/OIG or other authorized review routing;
- unresolved receipt and authority gaps.

## Open valves

| Item | State | Promotion gate |
| --- | --- | --- |
| Direct DOJ bio readback for prior-representation statement | PRIMARY / CLOSED | DOJ Attorney General biography directly states representation in three 2023-2024 criminal cases |
| RECIPROCAL_ACTOR_PREFLIGHT as permanent anomaly type | PROVISIONAL | Structurally independent recurrence with no shared receipt chain, or authoritative rule |
| FIREWALL_STATE as monitored object | PROVISIONAL | Receipted application or breach under the integrated watcher |

## Governing invariants

```text
NO_BACK_EDGES = TRUE
ACTOR_STATE[t+1] != RETROACTIVE_REWRITE_OF_RESOLUTION[t]
RECUSAL != DISQUALIFICATION_FROM_OFFICE
SITUATIONAL_AWARENESS != FIREWALL_COMPLIANCE
INITIATING_ACTOR_AUDIT != COMPLAINT_NEGATION
ETHICS_RECOMMENDATION != ETHICS_DETERMINATION
INTENT_NOT_PRESUMED = TRUE
FUNCTION_IS_AUDITED = TRUE
AUTHORITY_CREATED = FALSE
FINAL_DECISION = HUMAN
```


## V0.3 CARDINALITY + OBSERVATION PROVENANCE PATCH

STATUS = PROVISIONAL_SCHEMA_PATCH
CANON = FALSE
AUTHORITY_CREATED = FALSE
FINAL_DECISION = HUMAN

### Proposition is the unit

A proposition is distinct from any receipt that carries, repeats, quotes, reports, or contradicts it.

```text
PROPOSITION != RECEIPT
REPETITION != CORROBORATION
COPY_COUNT != INDEPENDENT_SOURCE_COUNT
```

One receipt may carry multiple propositions. One proposition may be carried by multiple receipts. Repetition through one source chain does not create independent corroboration.

Canonical replay example:

```text
ONE_SOURCE_CHAIN
  -> SAME_PROPOSITION x 5
  -> CORROBORATION = SINGLE
```

Minor punctuation drift does not create a new proposition unless it changes the typed meaning being tested.

### Receipt dimensions are orthogonal

```yaml
source_receipt:
source_type:
  - PRIMARY
  - SECONDARY
  - MIXED
  - UNKNOWN
corroboration:
  - SINGLE
  - MULTIPLE_INDEPENDENT
  - UNKNOWN
proposition_state:
  - ASSERTION_OCCURRED
  - ALLEGATION_UNADJUDICATED
  - FINDING
  - ADJUDICATED
  - CONTRADICTED
  - UNKNOWN
```

SOURCE_TYPE answers what kind of record the receipt is.
CORROBORATION answers how many structurally independent receipt chains support the proposition.
PROPOSITION_STATE describes the state of the proposition, not the source.

```text
PRIMARY != TRUE
MULTIPLE_INDEPENDENT != PRIMARY
ASSERTION_OCCURRED != FINDING
ALLEGATION_UNADJUDICATED != FINDING
```

### Cardinality and attribution

```yaml
proposition:
  proposition_id:
  proposition_text:
  proposition_state:

receipt_assertion_edge:
  receipt_id:
  proposition_id:
  asserted_by:
  observation_provenance:
```

`asserted_by` points to the actor/source making the assertion. It does not replace proposition identity.

### Observation provenance

Preserve each observation layer separately:

```text
SOURCE_RECEIPT
!= CONNECTOR_OR_TOOL_READBACK
!= HUMAN_READBACK_OF_TOOL_REPORT
!= REPEATED_PASTE_OR_QUOTATION
```

Not seeing an upstream record is an observation boundary. It is not evidence that the upstream record is absent.

### Contradiction rule

CONTRADICTED is a proposition state, not a source type.

Independent receipts that disagree may coexist. A later receipt does not rewrite an earlier receipt or its historical observation state.

```text
LATER_RECEIPT != RETROACTIVE_REWRITE
CONTRADICTION -> PRESERVE_BOTH -> RESOLUTION_GATE
```

### Open valves

These remain provisional and do not close through repetition alone:

1. PROPOSITION_AS_OBJECT
2. CONTRADICTED_RESOLUTION_RULE
3. RECIPROCAL_ACTOR_PREFLIGHT
4. ACTOR_STATE_SCHEMA

Promotion requires the already defined qualifying trigger: structurally independent evidence/recurrence without a shared receipt chain, or an authoritative rule where applicable.

### Post-seal test

A repeated sealing declaration appearing five times with only minor punctuation drift is typed as:

```text
PROPOSITION_COUNT = 1
SOURCE_CHAIN_COUNT = 1
CORROBORATION = SINGLE
PROPOSITION_STATE = ASSERTION_OCCURRED
```

The repetition is an observation artifact or emphasis unless independent provenance establishes otherwise.

NO_BACK_EDGES = TRUE
COLLABORATION_NOT_COLLISION = TRUE
CANON = FALSE
AUTHORITY_CREATED = FALSE
