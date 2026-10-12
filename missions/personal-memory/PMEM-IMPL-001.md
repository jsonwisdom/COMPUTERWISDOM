# PMEM-IMPL-001 — Memory Object Implementation Contract

Parent: `PERSONAL-MEMORY-CONSTITUTION-v1.0`  
Class: IMPLEMENTATION  
Constitution mutation: FALSE

## Canonical stored object

Fields: `id`, `type`, `content_ref`, `provenance{sources,dependencies,derivation}`, `validity{start,end}`, `authority{reason,action,export}`, `lifecycle`, `confidence{value,assessed_at}`.

Immutable after CREATE: `id`, `type`, `content_ref`, provenance, original creation record. Changed claims create new objects.

## Derivation gate

For child `x`: `A_x subseteq intersection(A_dependencies)` and derived children are `INFERRED` unless an independent external evidence source establishes another type.

`DERIVATION != OBSERVATION`  
`SUMMARY != OBSERVATION`  
`REPETITION != CONFIRMATION`

## Append-first events

`CREATE | CORRECT | SUPERSEDE | INVALIDATE | FORGET | REVALIDATE`

FORGET revokes/destroys protected material where controllable, creates a minimal tombstone, traverses transitive dependencies, invalidates affected descendants and reasoning caches, and prevents descendants from entering future USABLE sets.

Before reasoning: `USABLE = VALID AND CURRENT AND AUTHORIZED`. Any failed term means `OBJECT_USABLE=FALSE`.

Core: `OBJECT + DERIVATION GATE + APPEND-FIRST EVENTS + FORGET CASCADE`.

`AUTHORITY_CREATED = FALSE`
