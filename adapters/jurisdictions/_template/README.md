# Jurisdiction Adapter Template

Status: `SHELL_ONLY`
Authority: `false`

Copy this directory only after authoritative source endpoints for the target jurisdiction are identified.

Expected fields:
- adapter_id
- jurisdiction_scope
- authoritative_sources[]
- retrieval_mode
- parser_version
- output_schema
- source_hash_policy
- fail_closed_behavior

Default behavior: `UNRESOLVED` on missing, ambiguous, stale, or unauthenticated source material.
