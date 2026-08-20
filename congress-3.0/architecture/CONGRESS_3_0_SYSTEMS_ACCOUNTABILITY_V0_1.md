# Congress 3.0 — Congressional Systems Accountability v0.1

**Operator label:** `jaywisdom.base.eth`  
**Classification:** `CITIZEN_SYSTEMS_ACCOUNTABILITY_RESEARCH_ARCHITECTURE`  
**Government adoption claimed:** `false`  
**Authority created:** `false`

## The upgrade

The existing Congressional Accountability Membrane classifies records and prevents semantic promotion. Congress 3.0 adds the missing execution chain: how enacted authority becomes a machine rule, how that rule produces an action, how the action changes an official record, how a citizen experiences the consequence, and how the system proves correction.

```text
CONGRESS / ENACTED AUTHORITY
  -> DELEGATION
  -> POLICY / RULE
  -> MACHINE IMPLEMENTATION
  -> EXECUTION IDENTITY
  -> PERMISSION
  -> PROMOTION AUTHORITY
  -> ACTION
  -> RECORD DELTA
  -> CITIZEN CONSEQUENCE
  -> NOTICE / EXPLANATION
  -> REVIEW / CORRECTION
  -> REPLAY
```

The system does not accept `SYSTEM_ALLOWED_IT` as proof that the action was authorized or correct.

## Twelve independent accountability lanes

1. **Legal authority** — exact enacted authority or other controlling source.
2. **Delegation** — who was empowered to implement or execute it.
3. **Policy/rule** — the human-readable implementing rule and version.
4. **Machine rule** — code, configuration, decision table, model policy, or other executable representation.
5. **Execution identity** — human, service account, contractor, bot, or model that technically acted.
6. **Permission** — credential or technical capability used.
7. **Promotion authority** — separate authority to mutate a canonical record or consequential state.
8. **Record delta** — before/after state plus write receipt.
9. **Citizen consequence** — bounded effect produced by the state change.
10. **Notice/explanation** — what the affected person was told and what source supports it.
11. **Review/correction** — appeal, review, correction, and authority for the reviewer.
12. **Replay/accountability** — forward and reverse reconstruction of the complete chain.

No lane may silently stand in for another.

## Core membranes

```text
CAPABILITY != AUTHORITY
PERMISSION != LAWFUL_AUTHORIZATION
AUTOMATION != ACCOUNTABILITY
DATABASE_STATE != LEGAL_STATE
GREEN_CHECK != CORRECT_GOVERNMENT_ACTION
SYSTEM_FUNCTIONS_AS_DESIGNED != SYSTEM_IMPLEMENTS_LAW_CORRECTLY
SYSTEM_IMPLEMENTS_LAW_CORRECTLY != CITIZEN_TREATED_LAWFULLY
CONTRACTOR_EXECUTION != GOVERNMENT_RESPONSIBILITY_EXTINGUISHED
MODEL_OUTPUT != GOVERNMENT_DECISION
TECHNICAL_ACTOR != PROMOTION_AUTHORITY
```

## Accountability ladder

```text
SYSTEM_RAN
  != SYSTEM_RAN_AS_CONFIGURED
  != MACHINE_RULE_MATCHES_POLICY
  != POLICY_MATCHES_AUTHORITY
  != ACTION_MATCHES_RULE
  != RECORD_MATCHES_ACTION
  != NOTICE_MATCHES_RECORD
  != REVIEW_IS_AVAILABLE
  != CORRECTION_IS_REPLAYABLE
```

`ACCOUNTABILITY_CHAIN = RECONCILED` only when the required receipts for the applicable lanes reconcile.

## Recursive burden audit

Congress 3.0 adds a burden-allocation signal without turning it into a constitutional conclusion.

```text
GOVERNMENT_RECORD_CONFLICT
  + CITIZEN_ASKED_TO_REPROVE
  + REPEAT_COUNT > 1
  + NO_GOVERNMENT_RECONCILIATION_RECEIPT
  -> RECURSIVE_CITIZEN_REPROOF
  -> HOLD
```

This means the provenance chain is not reconciled. It does **not** by itself prove a due-process violation, illegality, discrimination, intent, fraud, or misconduct.

```text
RECURSIVE_CITIZEN_REPROOF != CONSTITUTIONAL_VIOLATION_PROVEN
BURDEN_SIGNAL != GUILT
DIRTY_MATH_SIGNAL != FRAUD
```

## Deterministic terminals

```text
PASS     = applicable lanes are source-bound and forward/reverse replay reconciles
HOLD     = required provenance, authority, review, correction, or reconciliation is missing
CONFLICT = valid bound records disagree or replay directions do not reconcile
REJECT   = an explicit semantic promotion attempts to collapse capability/permission/database/model state into authority or legal state
```

Fail-closed precedence:

```text
REJECT > CONFLICT > HOLD > PASS
```

## Machine-readable case object

The v0.1 case contract binds:

```text
CASE_ID
CLAIM
AUTHORITY
IMPLEMENTATION
EXECUTION
RECORD_DELTA
CITIZEN_EFFECT
REVIEW
BURDEN
REPLAY
MODEL
ATTEMPTED_PROMOTIONS
GOVERNMENT_RECORDS_CONFLICT
```

Dollar claims may additionally invoke Jay's Recursive Burden / Dirty Math Algorithm from PR #488; Congress 3.0 does not collapse money-state evidence into the systems-state evidence above.

## OpenAI boundary

The OpenAI layer is optional and subordinate to the deterministic verifier.

```text
MODEL_EXTRACTION != VERIFICATION
TOOL_CALL != GOVERNMENT_ACTION
MODEL_OUTPUT != LEGAL_FINDING
AGENT_PERMISSION != PROMOTION_AUTHORITY
VERIFIER_PASS != UNDERLYING_WORLD_TRUTH
```

The allowed runtime pattern is one bounded agent plus one deterministic verification function. The tool receipt should terminate the agent run without a second model turn that could widen its semantics.

Consequential publication, agency contact, congressional submission, record mutation, or citizen-facing decision remains `HOLD_FOR_HUMAN_AUTHORIZATION`.

## America Has Questions — Congress 3.0 kernel

For any automated government-facing consequence, ask:

```text
WHO AUTHORIZED THE RULE?
WHAT EXACT TEXT DID THE MACHINE IMPLEMENT?
WHO OR WHAT EXECUTED IT?
WHAT PERMISSION DID IT USE?
WHO AUTHORIZED CANONICAL PROMOTION?
WHAT RECORD CHANGED?
WHAT CONSEQUENCE FOLLOWED?
WHAT NOTICE EXPLAINED IT?
WHO CAN REVIEW IT?
HOW IS CORRECTION PROVEN?
CAN THE CHAIN REPLAY BOTH DIRECTIONS?
WHO CARRIES THE BURDEN WHEN GOVERNMENT RECORDS CONFLICT?
```

## Boundary

Congress 3.0 is a citizen research and software-audit architecture. It is not Congress, not a congressional finding, not legislation, not an agency rule, not a court, and not proof that any government system has violated law.

```text
CONGRESSIONAL_SUBMISSION = NOT_PERFORMED
MODEL_EXECUTION_PERFORMED = FALSE
LEGAL_VIOLATION_PROVEN = FALSE
AUTHORITY_CREATED = FALSE
```
