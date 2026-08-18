# SOURCE_BYTES lane directory contract — v0.1

## Governance posture

```text
BUILD_MODE             = DIRECTORIES_FIRST_CORRECTIVE_SUPERSESSION
VIOLATION_HEAD         = f9eeff160f3084c2740ffa02be6c4b9b845ef9a8
PREDECESSOR_LANE       = NONE_FOUND
PREDECESSOR_MUTATED    = FALSE
HISTORICAL_FILES_KEPT  = TRUE
AUTHORITY_CREATED      = FALSE
```

This contract explicitly supersedes the unguided directory state recorded at the violation head. It does not erase, rewrite, or claim that the original file-creation sequence was directory-first.

## Lane purpose

Admit synthetic fixtures and receipts that classify exact observed bytes, digest comparison, byte length, locator binding, and bounded source-identity posture.

## Admitted artifact classes

- `SOURCE_BYTES_RECEIPT_TEST_VECTORS_*.json` — synthetic deterministic test vectors.
- `SOURCE_BYTES_*_RECEIPT_*.json` — bounded build or replay receipts.
- `README.md` — this directory contract.

Schemas belong in `schemas/jaywisdom/`. Executable verifiers belong in `tools/`. Explanatory documents belong in `docs/jaywisdom/`.

## Prohibited promotions

```text
LOCATOR_EXISTS != BYTES_FETCHED
BYTES_MATCH_REFERENCE != SOURCE_IDENTITY_AUTHENTICATED
SOURCE_IDENTITY_AUTHENTICATED != CONTENT_ASSERTION_TRUE
SOURCE_BYTES_AUTHENTICATED != WORLD_FACT_PROVEN
RECEIPT != AUTHORITY
```

## Verification admission

Every admitted executable SOURCE_BYTES behavior must be invoked by an exact-head CI job. File presence alone is not verification.

