# Jurisdiction Adapters

Status: `SHELL_ONLY`
Authority: `false`

Adapters translate authoritative public jurisdiction sources into normalized RePlay observations. They do not create jurisdiction, legal authority, or political conclusions.

Required adapter contract:
- source identity
- retrieval method
- observed timestamp
- source hash when captured
- parser/version identifier
- normalized output
- unresolved/error state

Planned starter packs:
- `_template/`
- `us/`
- `fr/`
- `ke/`

No jurisdiction adapter is production-ready merely because its directory exists.
