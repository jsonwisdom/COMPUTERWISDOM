# CONSTITUTION FOR PERSONAL MEMORY v1.0

Status: **FROZEN**

Checkpoint identifier: `PERSONAL-MEMORY-CONSTITUTION-v1.0 | NO-MUTATION | NO-EPISTEMIC-LAUNDERING | NO-AUTHORITY-LAUNDERING`

> The checkpoint identifier is a canonical label, not a cryptographic digest unless its exact bytes are hashed.

## 1. Canonical Object

`m = <id, tau, c, p, [t_s,t_e), A, s, conf>`

- `id`: immutable identity
- `tau`: immutable epistemic type
- `c`: content or content-addressed reference
- `p`: provenance DAG + derivation edges
- `[t_s,t_e)`: validity interval
- `A`: authority scope set
- `s`: lifecycle state
- `conf`: confidence metadata

## 2. Governing Predicate

`USABLE(m,t) = VALID(m) AND CURRENT(m,t) AND AUTHORIZED(m)`

Existence grants nothing. Only `USABLE` objects may participate in reasoning or action.

`BELIEF(t) = { m | USABLE(m,t) }`

## 3. Constitutional Invariants

### I1 — No Silent Mutation

`tau(m,t') = tau(m,t_creation)`

Type never changes. Stronger claims require a new object with new provenance.

### I2 — No Epistemic Laundering

`INFERRED` can never become `OBSERVED` by relabeling. `USER_ASSERTED` can never become `OBSERVED` without a new external evidence object.

### I3 — No Authority Laundering

`A_child subseteq intersection(A_dependency)`

No derived object may broaden permissions of its evidence base.

## 4. Lifecycle

Append-first. Correction, supersession, invalidation, revalidation, revocation, and forgetting are represented by new events rather than silent mutation.

## 5. Core Principle

`NO SILENT MUTATION + NO EPISTEMIC LAUNDERING + NO AUTHORITY LAUNDERING`

All lower policies may evolve only beneath these three laws.

`AUTHORITY_CREATED = FALSE`
