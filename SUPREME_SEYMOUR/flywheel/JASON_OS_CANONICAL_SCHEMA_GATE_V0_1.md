# JASON_OS — Historical canonical schema gate v0.1

**Status:** DRAFT repair only. JASON = denominator. Audit verdicts are evidence/computation-driven, not subject to a human audit-signoff.

The September 21, 2026 JASON_OS Conversation Compiler status record lists SHA-256 commitments for CEO, GRAPH, FOLD, and QUERY schemas, but the four original schema files were **not recovered** in the inspected indexed GitHub and Library results. These reported hashes are reference commitments, not independently authenticated source custody. Do **not** substitute new schemas and call them canonical.

## Validation contract

- `JASON_CANONICAL_SCHEMA_ROOT` is an explicitly configured **private/local** directory.
- Adapter expects `ceo.schema.json`, `graph.schema.json`, `fold.schema.json`, and `query.schema.json`. These are **input adapter names**, not claimed historical canonical filenames.
- Compute SHA-256 of **exact local file bytes** and compare to the historical commitment for that layer. Missing source yields **UNKNOWN**, mismatch yields **FAIL**.
- When hash matches, decode strict UTF-8 JSON with duplicate-key rejection; disallow external schema references; validate the existing candidate stage using pinned `jsonschema==4.23.0`. A validation error yields **FAIL**. Validator not installed or offline dependencies missing yield **UNKNOWN**.
- Only exact pinned bytes **and** successful schema validation yield `canonical_compatibility=PASS`. Even then `truth_verdict=UNKNOWN` and `history_complete=UNKNOWN`. Canonical compatibility does not prove authorship, historical completeness, private original identity, consent, or adoption.
- Synthetic test schemas use a separately marked `SYNTHETIC_TEST_ONLY` profile with injected test digests. Even a fully valid fixture yields `FIXTURE_PASS_ONLY`, **never** canonical PASS.
- No private original bytes, candidate text, IDs, filenames, local pointers or digests are returned by the public summary. Private details are written to `build/supreme-seymour-flywheel/private/` and are excluded from existing GitHub Actions artifact upload paths.

## Private candidate ingestion receipt

When an explicit local manifest is supplied, a separate private receipt records per-source:
- type (voice/chat), SHA-256 of observed source bytes if available, and local-only original pointer;
- UTC ingestion timestamp and candidate parser version;
- declared transcriber version separately from verified status;
- candidate claim status UNKNOWN and schema status UNKNOWN;
- event time declaration distinct from ingestion, delivery and acknowledgment.

A timestamp or digest does not establish original provenance by itself. Detailed source recovery continues to use existing PR #731 and #733 code. This gate does not load private originals into GitHub CI and does not modify the frozen JASON_OS kernel.

## Tests and boundaries

`python -m unittest discover -s SUPREME_SEYMOUR/flywheel/tests -p "test_*.py" -v`

The new test module adds **14 synthetic cases** to the prior **35**, for **49 planned tests on each OS**. CI is the verification authority for their actual execution, not this documentation. Safety gates remain scoped; unrelated GitHub observations continue if one schema is missing or invalid.

## Evidence still needed

Acquire the four original schema byte streams, independently establish their version/custody, bind them to the historical SHA-256 commitments, then check the actual candidate mapping. Only after that can canonical schema compatibility change from UNKNOWN/FAIL to scoped PASS. Original full ChatGPT export and voice/audio custody remain OPEN.
