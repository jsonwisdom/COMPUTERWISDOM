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
