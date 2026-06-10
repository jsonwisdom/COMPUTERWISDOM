# MANIC_REPLAY_BRANCHING_SCHEMA_001

**Replayable Manic – Replay Branching Schema**  
**Version:** 0.0.1  
**Status:** Branching Schema / No Interpretation  
**Continuity Flag:** COHERENTLY_INVALID_UNTIL_REPLAYED

## Purpose

This schema defines the first deterministic branching surface for MANIC replay decomposition.

It does not interpret source material. It defines identifiers, lineage rules, admissibility constraints, and failure modes for structurally decomposing a public root source into replayable nodes.

## 1. Root Source Decomposition

| Field | Value |
|---|---|
| `root_id` | `ROOT_SOURCE_PCLOB_001` |
| `source_type` | `PCLOB_2026_S702_REPORT` |
| `ingest_hash` | SHA-256 of original PDF content when independently materialized |
| `decomposition_rule` | Split by structural unit: section, subsection, footnote, table, appendix, or other explicit document boundary |
| `offset_rule` | Preserve source offsets when feasible; if byte offsets are unavailable, preserve page and structural locator |
| `output_rule` | One replay node per structural unit; no merging during initial decomposition |

## 2. Replay Node Identifiers

Replay node identifiers must be deterministic within a cycle.

```text
RPL-<CYCLE>-<SOURCE>-<SEQ>
```

Example:

```text
RPL-001-PCLOB-00042
```

### Required Node Fields

| Field | Requirement |
|---|---|
| `node_id` | Deterministic replay node identifier |
| `parent_root_id` | Root source identifier |
| `parent_hash` | Hash reference to parent content or parent node |
| `source_locator` | Page, section, table, footnote, appendix, or byte-offset reference |
| `source_offset_start` | Byte or structural offset start when feasible |
| `source_offset_end` | Byte or structural offset end when feasible |
| `transform_id` | Whitelisted deterministic transform identifier |
| `content_hash` | SHA-256 hash of extracted node content |
| `constitutional_tags` | Initial tag must be `OBSERVED` unless derived later |

## 3. Replay Lineage Rules

1. Every replay node must reference exactly one parent.
2. Parent may be the root source or a prior replay node.
3. Lineage verification rule:

```text
hash(parent.content + transform_id) == node.parent_hash
```

4. Branching is allowed only through an explicit fork directive recorded under `branches/`.
5. No silent overwrites are allowed.
6. All updates append new nodes or receipts.

## 4. Replay Admissibility Constraints

A replay transform is admissible only if:

- it is deterministic and pure
- it performs no external network fetch during replay
- it performs no LLM interpretation
- it performs only structural extraction, normalization, hashing, or validation
- it emits validation receipts with timestamp, validator version, and result code
- its outputs validate against the MANIC validation pipeline

## 5. Failure Modes and Refusal Codes

| Refusal Code | Trigger |
|---|---|
| `DRIFT_DETECTED` | Content hash mismatch on replay |
| `NON_DETERMINISTIC_OUTPUT` | Same input yields different output |
| `MISSING_LINEAGE` | Parent hash or parent node cannot be found |
| `UNAUTHORIZED_TRANSFORM` | Transform ID is not whitelisted |
| `INCOMPLETE_RECEIPT` | Receipt is missing required fields |
| `OFFSET_UNAVAILABLE` | Source offsets cannot be reconstructed and no structural locator is provided |
| `INTERPRETATION_ATTEMPTED` | Transform attempts semantic analysis, inference, or LLM summarization |

All failures must fail loudly and preserve `COHERENTLY_INVALID_UNTIL_REPLAYED` state.

## 6. Whitelisted Initial Transform Classes

| Transform Class | Allowed? | Notes |
|---|---:|---|
| `STRUCTURAL_SPLIT` | Yes | Section/page/table/footnote extraction |
| `CONTENT_HASH` | Yes | SHA-256 content hashing |
| `LOCATOR_CAPTURE` | Yes | Page, section, byte, or structural locator preservation |
| `SCHEMA_VALIDATE` | Yes | JSON schema validation |
| `LLM_SUMMARY` | No | Interpretation forbidden in initial branch decomposition |
| `SEMANTIC_CLASSIFICATION` | No | Requires later schema and explicit interpretive boundary |

## 7. Replay Surface Boundary

The branching schema creates replayable structure only.

It does not decide:

- what the report means
- whether a claim is true
- whether an institution is good or bad
- whether a dispute is resolved

It only determines whether a document can be decomposed into deterministic, replayable, hashable units.

## Status

Coherently Invalid until replayed.

Every map is incomplete.
