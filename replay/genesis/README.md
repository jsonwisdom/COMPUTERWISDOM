# RePlay Genesis — Global Jurisdiction Shell

Status: `SHELL_ONLY`
Authority: `false`
Data populated: `false`
Genesis keys issued: `0`

Purpose: provide one deterministic jurisdiction-routing namespace for RePlay instances without creating governmental, legal, or political authority.

Core invariant:

`same engine + different genesis key + different source adapters = different jurisdiction`

Planned files:
- `GENESIS_NAMESPACE_V1.json`
- `GENESIS_KEY_SCHEMA_V1.json`
- `JURISDICTION_TYPES_V1.json`
- `SUCCESSION_RULES_V1.json`

Planned flow:

`authoritative source -> adapter -> verified delta -> 128x128 sparse map -> quadratic priority signal -> append-only receipt -> parent jurisdiction root`

Boundaries:
- place existence does not prove government existence
- source adapters do not create authority
- QV is a nonbinding preference signal
- official civic acts remain external and unchanged
- empty/unverified slots remain unresolved
- historical nodes are never overwritten
