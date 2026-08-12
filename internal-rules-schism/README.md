# INTERNAL RULES SCHISM — POC 0001

Status: `SPECIMEN_FROZEN / PRIMARY_SOURCE_PENDING`

This directory proves the rule-object invariant **before** any ingestion pipeline exists.

## Specimen

`poc/0001/rule.json` models the reported August 2026 OLC presidential-communications privilege development as a versioned rule object.

The specimen intentionally separates:

```text
SPECIMEN_INTEGRITY_PASS != PRIMARY_LEGAL_SOURCE_VERIFIED
```

The official DOJ OLC opinions index currently lists July 16, 2026 as its latest indexed opinion. Secondary reporting on August 11, 2026 describes a newer opinion concerning communications with private advisers, but the primary opinion bytes are not yet bound to this object.

Therefore:

```text
PRIMARY_SOURCE_VERIFIED = FALSE
AUTOMATIC_RELIANCE      = HOLD
FINAL_STATE             = HOLD_PRIMARY_BYTES
AUTHORITY_CREATED       = FALSE
```

## Five invariant checks

The root executable `executables/internal_rules_schism_validate_v0_1.py` checks:

1. required specimen structure and core types;
2. hash/verification consistency;
3. date ordering;
4. typed delta coherence;
5. fail-closed CI cascade.

`poc/0001/ci_output.json` is the deterministic output for the frozen specimen.

## Epistemic protection

Fields derived from secondary reporting or machine assessment are explicitly typed in `epistemic_status`. A structural PASS must never promote those fields to primary observation.

## No pipeline

There is no fetch/scrape/ingestion routine in POC 0001. `rules/` is reserved for later promoted rule objects after the specimen and retrieval invariants are proven.
