# FULLMATH_REPLAY_PEPE_POLICY_V0_1

Status: ACTIVE_METHOD / NON-AUTHORITY  
Authority created: FALSE  
Canon: FALSE  
Policy created: FALSE

## Objective

Replay PEPE-related policy claims without turning a machine-local search miss into global absence and without turning a schema, fixture, or repository object into an employment/payroll fact.

## FullMath equation

```text
FULLMATH_REPLAY =
INPUTS
+ EXCLUSIONS
+ CLOCKS
+ RECEIPTS
+ CONTRADICTIONS
+ FAILED_SEARCHES
+ UNRESOLVED_EDGES
+ TRANSITION_AUTHORITY
```

## Required source typing

Every search event MUST bind:

```text
MACHINE_OR_SURFACE_ID
SOURCE_CLASS
QUERY
REF_OR_SCOPE
OBSERVED_AT
RESULT_STATE
RESULT_POINTERS
```

Allowed result states:

```text
PRESENT
SEARCH_MISS
NOT_SEARCHED
UNREACHABLE
CONFLICT
```

## Non-collapse laws

```text
SEARCH_MISS(machine_A) != ABSENT_EVERYWHERE
DEFAULT_BRANCH_MISS != REPOSITORY_HISTORY_MISS
DRIVE_ACCOUNT_A_MISS != DRIVE_ACCOUNT_B_MISS
WORKSPACE != USER_LOCAL_MACHINE
SCHEMA_VALID != POLICY_EXISTS
FIXTURE_PASS != REAL_RELATIONSHIP
POLICY_TEXT != EMPLOYMENT_RELATIONSHIP
EMPLOYMENT_RELATIONSHIP != PAYROLL_AUTHORITY
PAYROLL_AUTHORITY != BONUS_SCHEDULE
TOKEN_RELATIONSHIP != EMPLOYMENT_RELATIONSHIP
```

## Transition spine

```text
DECLARED
 -> OBSERVED
 -> ENCODED
 -> EXECUTED
 -> VERIFIED
```

A later state may not be inferred from an earlier one.

For a real PEPE policy candidate to leave HOLD, the replay must bind the source object, relevant content, source boundary, clock, and transition authority.

## Fail-closed rule

```text
MISSING_REQUIRED_RECEIPT -> HOLD
CONFLICTING_RECEIPTS -> CONFLICT
LOCAL_SEARCH_MISS -> SEARCH_MISS
UNSEARCHED_MACHINE -> NOT_SEARCHED
```

No state above creates legal, employment, payroll, trading, token, or governmental authority.
