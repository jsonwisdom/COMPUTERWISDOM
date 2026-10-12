# PMEM-IMPL-010 — Policy Versioning + Migration Contract

Depends on: `001..009`

`CURRENT POLICY != HISTORICAL POLICY`.

Every consequential operation binds exact policy identifiers, versions, and content references used at execution. Replay evaluates the policy stack recorded for that event, not today's policy.

Canonical policy objects bind `policy_id`, name, semantic version, content hash/reference, effective interval, parent references, and status (`DRAFT|ACTIVE|SUPERSEDED|RETIRED`). Activated policy bytes are immutable.

New policies may change future behavior but may not rewrite historical outcomes. `REEVALUATE != REWRITE`.

Migration requires source/target versions, migration rule, affected objects, authority basis, result, and receipt. Migration creates derived state; it does not edit original representation.

Candidate policies must pass I1/I2/I3. Lower layers cannot amend the constitution through versioning.

Policy conflicts resolve by constitution, explicit precedence, narrower authority, then fail-closed. If deterministic resolution is impossible: `POLICY_STATE=DISPUTED_POLICY`, `EXECUTION=FALSE`.

Retirement blocks future use while preserving historical replay. Re-evaluation records original result/stack and new evaluation/stack separately.

Core: **POLICY UPDATE != HISTORY REWRITE; MIGRATION != MUTATION; LOWER POLICY != CONSTITUTIONAL AMENDMENT**.

`AUTHORITY_CREATED = FALSE`
