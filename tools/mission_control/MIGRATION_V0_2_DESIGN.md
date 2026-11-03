# Mission Control Migration v0.2 — Design Boundary

This file records the migration design boundary only. It does not authorize migration.

```text
COPY != AUTHORITY
PROVENANCE_RECEIPT != AUTHORITY_GRANT
MIGRATION_AUTHORIZED = FALSE
AUTHORITY_CREATED = FALSE
```

A reviewed migration unit must have explicit `ARTIFACT_ID`, `SOURCE_PATHS`, and `DESTINATION_SUBDIR`. Multi-artifact branches must be split into multiple registry rows before any copy operation.

The executable v0.2 migration engine belongs on a separate stacked branch/PR and must fail closed unless an explicit migration authorization gate is satisfied.
