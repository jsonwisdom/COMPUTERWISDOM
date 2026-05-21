# MANIC Replay Governance

**Status:** Replay Gate Surface / Structural Decomposition Only  
**Continuity Flag:** COHERENTLY_INVALID_UNTIL_REPLAYED

## Purpose

This directory governs active MANIC replay decomposition.

Replay transforms convert public root sources into deterministic, hashable, append-only structural nodes. Replay does not interpret the source. Replay only proves whether structural extraction can be reconstructed.

## Directory Layout

```text
replay/
  branches/              # decomposed replay nodes
  README.md              # governance rules
  validate_replay.js     # replay-fidelity gate
```

## Decomposition vs. Interpretation

### Allowed in Replay

- structural extraction
- section/page/table/footnote splitting
- locator capture
- SHA-256 content hashing
- schema validation
- lineage preservation

### Forbidden in Replay

- LLM summarization
- semantic interpretation
- political conclusions
- truth adjudication
- synthetic confidence claims
- external network fetches during replay

## Replay Node Requirements

Every replay node must include:

- `node_id`
- `parent_root_id`
- `parent_hash`
- `source_locator`
- `transform_id`
- `content_hash`
- `constitutional_tags`

The initial replay node tag must be `OBSERVED` unless a later interpretive schema explicitly authorizes derived tags.

## Failure Behavior

Replay validation must fail loudly when it detects:

- missing lineage
- missing source locator
- unauthorized transform
- non-observed initial replay tag
- missing content hash
- attempted interpretation

## Core Rule

Replay creates structure.

Interpretation creates claims.

Those layers must not collapse.
