# PEPE Policy Replay v0.1

Status: DIRECTORY_FIRST_SCAFFOLD
Authority created: FALSE
Canon: FALSE
Policy created: FALSE
Employment relationship created: FALSE
Payroll authority created: FALSE
Bonus schedule created: FALSE

## Purpose

Provide a fail-closed receiving structure for future PEPE-related policy, relationship, payroll, bonus, and replay evidence without converting a search miss into absence or fabricating a missing policy.

## Machine boundary

This project must name every searched machine or source surface. A miss on one surface never becomes global absence.

```text
SEARCH_MISS(surface_A) != ABSENT_EVERYWHERE
WORKSPACE != USER_LOCAL_MACHINE
DEFAULT_BRANCH != ENTIRE_REPOSITORY_HISTORY
DRIVE_ACCOUNT_A != DRIVE_ACCOUNT_B
```

## Directory contract

- `schema/` — shape and type constraints only.
- `framework/` — replay rules and state-transition law.
- `infrastructure/` — named source/machine boundaries and routing objects.
- `instrumentation/` — probes, search traces, and reproducible observation formats.
- `fixtures/` — synthetic positive/negative/conflict examples only.

No directory may create a real PEPE policy merely by existing.
