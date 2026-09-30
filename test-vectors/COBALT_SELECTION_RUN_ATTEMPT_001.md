# COBALT_SELECTION_RUN_ATTEMPT_001

Append-only execution-attempt receipt. Does not edit `COBALT_SELECTION_VECTOR_V0_1`.

```text
SUBJECT:     COBALT_SELECTION_VECTOR_V0_1
RESULT:      NO_EXECUTION
CAUSE:       PIN_UNREACHABLE
PROCESS_STARTED: FALSE
PIN_FETCHED:     FALSE
BINARY_HASH:     ABSENT
CONFIG_HASH:     ABSENT
OUTPUT_BYTES:    ABSENT
LEG_A:           HOLD
LEG_B:           NOT_IN_SCOPE
VECTOR_MUTATED:  FALSE
HOLD_REASON:     PIN_UNREACHABLE
TEST_RESULT:     NONE
VERDICT:         NOT_REACHED
```

## Trace

```text
ATTEMPT
  → ENVIRONMENT CHECK     (git, rustc, cargo present)
  → FETCH FAILURE         (github.com:443 unreachable)
  → NO PROCESS
  → HOLD
```

Not a vector failure. The spec was not entered.

## Frozen distinctions

```text
EXPECTED_OUTPUT        ≠ OBSERVED_OUTPUT
REIMPLEMENTATION       ≠ PINNED_EXECUTION
TOOLCHAIN_PRESENT      ≠ SOURCE_AVAILABLE
BUILDABLE_IN_PRINCIPLE ≠ BINARY_BUILT
FAILED_FETCH           ≠ FAILED_VECTOR
NO_EXECUTION           ≠ TEST_FAILURE
HOLD_REASON            ≠ TEST_RESULT
```

This attempt is not a failed Cobalt test. The predicate never ran.

## Pipeline for ATTEMPT_001

```text
SPECIFICATION  PRESENT
ATTEMPT        PRESENT
ENVIRONMENT    INSUFFICIENT
EXECUTION      ABSENT
OBSERVATION    ABSENT
VERDICT        NOT_REACHED
STATE          HOLD
```

## Ledger

```text
VECTOR_V0_1
  definition:      DEFINED
  expected bytes:  DEFINED
  state:           HOLD

RUN_ATTEMPT_001
  execution:       ABSENT
  observation:     ABSENT
  verdict:         NOT_REACHED
  hold_reason:     PIN_UNREACHABLE
  state:           HOLD

PASS      = 0
FAIL      = 0
EXECUTED  = 0
ATTEMPTED = 1
```

## Parent objects unchanged

```text
COBALT_ACTIVATION_RECEIPT_V0_1          HOLD
COBALT_RULESET_SELECTION_RECEIPT_V0_1   HOLD
COBALT_SELECTION_VECTOR_V0_1            HOLD
```

PR #587 remains untouched. No promotion. No fake execution.
