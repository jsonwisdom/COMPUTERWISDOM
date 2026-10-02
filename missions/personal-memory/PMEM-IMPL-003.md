# PMEM-IMPL-003 — Evidence Graph Query + Replay Contract

Depends on: `001..002`

A query may reason only from objects satisfying `USABLE(m,t)=VALID AND CURRENT AND AUTHORIZED`.

`STORED != RETRIEVABLE`  
`MATCHED != USABLE`  
`USABLE != EXPORTABLE`

Pipeline: `QUERY -> INDEX MATCH -> GRAPH EXPANSION -> VALIDITY FILTER -> CURRENT FILTER -> AUTHORITY FILTER -> TYPE PRESERVATION -> RESULT SET`. Filtering occurs before reasoning.

Historical replay evaluates the ledger and graph as they existed at the requested `as_of` time. Future corrections do not rewrite historical replay.

Reasoning outputs retain provenance links to materially supporting objects. Derived results remain `INFERRED` unless independent external evidence establishes another type.

Contradictory usable objects coexist. Allowed result states include `SUPPORTED`, `CONTRADICTED`, `DISPUTED`, `INSUFFICIENT_EVIDENCE`, `UNKNOWN`.

Confidence is metadata, not type, validity, truth, or authority.

Consequential queries produce receipts with candidate/usable counts, exclusions, evidence ids, result hash, and exact policy stack. Unknown authorization fails closed.

Core invariant: **NO REASONING FROM NON-USABLE MEMORY**.

`AUTHORITY_CREATED = FALSE`
