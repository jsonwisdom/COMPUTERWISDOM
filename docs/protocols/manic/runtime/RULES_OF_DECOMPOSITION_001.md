# RULES_OF_DECOMPOSITION_001

**Replayable Manic – Rules of Decomposition**  
**Version:** 0.0.1  
**Status:** Controlling Replay Decomposition Invariant  
**Continuity Flag:** COHERENTLY_INVALID_UNTIL_REPLAYED

## Purpose

This document defines lawful structural extraction boundaries for MANIC replay nodes.

Decomposition may preserve structure.

Decomposition may not create meaning.

## Scope

These rules apply to replay nodes created from public root sources under the MANIC replay runtime.

They govern structural decomposition only. Interpretive claims must be created through claim-node receipts under the MANIC runtime, not replay nodes.

## Allowed Structural Units

A replay node may represent one and only one structural unit, including:

- title page
- section
- subsection
- paragraph
- footnote
- table
- appendix
- page-level locator when finer decomposition is not yet available
- byte-range locator when available

## Forbidden Actions

Replay decomposition must not perform:

- summarization
- semantic inference
- claim generation
- political conclusion
- confidence assignment beyond structural validation
- cross-source synthesis
- LLM interpretation
- external network fetch during replay
- merger of unrelated structural units

## Node Rule

One replay node per structural unit.

Initial decomposition must favor narrower structural units over broad narrative aggregation.

If exact byte offsets are unavailable, the replay node must preserve a page, section, table, footnote, appendix, or other explicit structural locator.

## Lineage Rule

Every replay node must declare:

- `node_id`
- `parent_root_id`
- `parent_hash`
- `source_locator`
- `transform_id`
- `content_hash`
- `constitutional_tags`

Every initial replay node must include only the `OBSERVED` constitutional tag.

## Transform Rule

Replay decomposition may use only transform identifiers admitted by:

```text
REPLAY_TRANSFORM_REGISTRY_001
```

A replay node using an unknown or unauthorized transform must fail validation.

## Refusal Conditions

Replay decomposition must refuse if:

- the source locator is missing
- the content hash is malformed
- the parent hash is malformed
- the transform is not registered
- interpretive tags are present
- multiple unrelated structural units are merged
- semantic meaning is introduced
- external network access is required during replay

## Status

Coherently Invalid until replayed.

Every map is incomplete.
