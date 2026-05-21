# ALMS_REFERENCE_MAPPING_V1

**Replayable Manic – ALMS Reference Mapping**  
**Version:** 1.0  
**Status:** Reference Mapping / Not a Settlement Object  
**Date:** 2026

## Purpose

This document defines how MANIC protocol objects may map into an ALMS-compatible ledger model without claiming that MANIC is itself an ALMS settlement runtime.

MANIC provides constitutional observability primitives for public reasoning. ALMS provides receipt, lineage, and ledger-memory concepts for replayable state. This mapping preserves separation while enabling future interoperability.

## Boundary Statement

MANIC is not a truth oracle, payment rail, legal adjudicator, or settlement state machine.

MANIC objects become ALMS-compatible only when they produce replayable public evidence records with stable identifiers, source lineage, timestamps, contribution metadata, and append-only revision behavior.

## Core Object Mapping

| MANIC Object | ALMS-Compatible Role | Notes |
|---|---|---|
| Root Source | Evidence Anchor | Public document, transcript, statute, report, or official release |
| Replay Thread | Lineage Chain | Append-only chronology of claims, forks, corrections, and syntheses |
| Claim Node | Evidence-Linked Assertion | Must include source tier, grammar tag, confidence, contributor, and timestamp |
| Correction Node | Supersession Receipt | Does not delete prior claim; appends corrected interpretation |
| DISPUTED Branch | Contradiction Surface | Preserves unresolved counter-evidence without forced resolution |
| Synthesis Node | Derived Interpretation | Must declare incompleteness and cite all upstream nodes |
| Opacity Index Release | Versioned Measurement Receipt | Forkable public observability metric with methodology and confidence interval |
| Visual Graph State | Replay View | Non-authoritative rendering of underlying lineage objects |

## Minimal MANIC Receipt Fields

A MANIC-compatible ALMS reference receipt should include:

```json
{
  "schema_id": "MANIC_ALMS_REFERENCE_RECEIPT_V1",
  "receipt_id": "sha256:jcs(receipt_body)",
  "protocol": "MANIC",
  "protocol_version": "0.1",
  "object_type": "ROOT_SOURCE | CLAIM_NODE | CORRECTION_NODE | DISPUTED_BRANCH | SYNTHESIS_NODE | OPACITY_INDEX_RELEASE",
  "created_at": "UTC_ISO_8601",
  "created_by": "contributor_identifier",
  "public_source_refs": [],
  "source_tiers": [],
  "constitutional_tags": [],
  "confidence": {
    "value": null,
    "qualifier": "string",
    "ceiling_basis": "source_tier | explicit_support"
  },
  "parent_receipts": [],
  "supersedes": [],
  "disputes": [],
  "content_hash": "sha256:...",
  "replay_requirements": {
    "public_source_only": true,
    "append_only": true,
    "forkable": true,
    "full_chain_reconstructable": true
  },
  "status": "COHERENTLY_INVALID_UNTIL_REPLAYED"
}
```

## Canonicalization Guidance

- Receipt bodies should use deterministic JSON canonicalization before hashing.
- Timestamps must be UTC ISO-8601.
- Parent and supersession references must use stable receipt identifiers.
- Rendered UI state is not canonical unless separately hashed as a view artifact.
- Public source links should be accompanied by content hashes when feasible.

## Promotion Rules

A MANIC object may be promoted into an ALMS-compatible receipt only if:

1. It anchors to public evidence or explicitly declares itself as interpretation.
2. It separates OBSERVED, INTERPRETED, SYNTHESIZED, DISPUTED, and SUPERSEDED material.
3. It includes confidence metadata within source-tier ceilings.
4. It preserves chronology through append-only updates.
5. It remains challengeable through visible forks or disputes.
6. It can be reconstructed from public roots.

## Refusal Rules

A MANIC object must not be promoted if it:

- Depends on classified, private, leaked, or unverifiable material.
- Claims final truth rather than replayable reasoning.
- Deletes or hides prior claims during correction.
- Suppresses lawful forks or contradiction branches.
- Exceeds confidence ceilings without higher-tier public support.
- Blends observation, interpretation, and synthesis without tags.

## Relationship to ALMS

This mapping is intentionally conservative.

ALMS remains the ledger-memory and receipt architecture. MANIC remains the constitutional observability protocol. Interoperability begins only at the receipt boundary, where MANIC outputs are made deterministic, hashable, append-only, and replayable.

## Status

Coherently Invalid until proven replayable.

Every map is incomplete.
