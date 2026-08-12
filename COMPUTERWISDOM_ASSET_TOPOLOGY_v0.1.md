# COMPUTERWISDOM Asset Topology v0.1

Status: `CANONICAL_TOPOLOGY_PROPOSAL`

## Purpose

Reusable repository assets must be discoverable by class at the COMPUTERWISDOM root. A project, mission, receipt bundle, workflow, or experiment may consume a reusable asset; it must not silently become that asset's canonical home merely because the asset was first created there.

```text
REPOSITORY_CAPABILITY != PROJECT_SUBSTRATE
LOCATION != AUTHORITY
LABEL != EVIDENCE
DISCOVERY != PROMOTION
```

## First-class asset classes

| Class | Canonical root | Contract |
|---|---|---|
| Executables | `executables/` | Runnable entrypoints and operator-facing commands. Libraries may remain in package/module trees. |
| Fixtures | `fixtures/` | Immutable or versioned test/replay inputs. A fixture is input evidence for a test, not a proof of the test result. |
| Instruments | `instruments/` | Auditors, validators, meters, routers, evaluators, scanners, and their measurement contracts. |
| Proofs | `proofs/` | Reproducible verification outputs, proof packets, and proof indexes. A filename containing `proof` does not make a claim true. |
| Whitepapers | `whitepapers/` | Research papers and architecture papers intended to stand independently of one implementation directory. |

## Ownership law

A reusable asset belongs to COMPUTERWISDOM when its semantics apply across projects.

A project directory may contain only project-specific implementation, configuration, local fixtures, or a thin adapter that invokes a canonical repository asset. If a project-local artifact becomes reusable, promotion requires a new repository-level canonical path and a provenance-preserving migration record.

## Migration law

No bulk move is authorized by this document.

Migration is append-first and fail-closed:

1. Discover candidate assets without changing files.
2. Classify each candidate by semantics, not filename alone.
3. Establish the canonical repository path.
4. Preserve the original blob SHA and source path in the migration receipt.
5. Update imports, workflows, docs, and project adapters.
6. Run project and repository tests.
7. Only then remove or replace the old path.

```text
SOURCE_BLOB_KNOWN=true
TARGET_CLASS_VERIFIED=true
DEPENDENCIES_UPDATED=true
TESTS_PASS=true
    -> relocation may be eligible
otherwise
    -> HOLD
```

## Project adapter rule

A mission such as `missions/SSA_PUBLIC_REPLAY_CORPUS_v0.1/` may test CrissCross against SSA-specific receipts, but the CrissCross Auditor itself is a COMPUTERWISDOM instrument/executable and must not be defined solely inside the SSA mission tree.

## Discovery

`executables/asset_inventory_v0_1.py` performs a read-only heuristic inventory and marks canonical and buried candidates. Its classifications are candidate labels requiring semantic review; it performs no moves and creates no authority.

```text
CLASSIFICATION_REQUIRES_REVIEW=true
MOVES_PERFORMED=false
AUTHORITY_CREATED=false
```
