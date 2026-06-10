# FIRST_PUBLIC_INGESTION_TEMPLATE

**Replayable Manic – First Public Ingestion Template**  
**Status:** Template / No live claim made  
**Purpose:** Provide a safe pattern for the first real-world public document ingestion under MANIC validation rules.

## Boundary

This template is for public-source ingestion only.

It must not ingest classified, leaked, private, sealed, or otherwise unverifiable material.

## Required Inputs

| Field | Requirement |
|---|---|
| Public source URL | Direct public link to document or official page |
| Source tier | T1 or T2 preferred for first ingestion |
| Local title | Human-readable artifact title |
| Source date | Publication or hearing date, if available |
| Retrieved at | UTC ISO-8601 timestamp |
| Content hash | SHA-256 of stable downloaded content when feasible |
| Constitutional tags | OBSERVED required for root source |
| Confidence qualifier | Root source confidence must describe anchoring only, not truth of interpretations |

## Recommended First Ingestion Class

Use a stable public oversight document, such as:

- official congressional hearing transcript
- public statute or legislative text
- declassified court opinion published by an official source
- inspector general report
- PCLOB report
- ODNI public release

## First Receipt Shape

The first real-world object should be a `ROOT_SOURCE` receipt conforming to:

```text
../schemas/manic_reference_receipt.v1.schema.json
```

It should not make broad analytical claims. It should only anchor the public document.

## Process

1. Select public T1/T2 source.
2. Capture source URL and retrieval timestamp.
3. Hash content if feasible.
4. Create `ROOT_SOURCE` receipt.
5. Validate with:

```bash
node docs/protocols/manic/validators/validate_receipt.js <receipt.json>
```

6. Add claim nodes only after root source validates.
7. Preserve all updates as append-only receipts.

## Refusal Conditions

Do not ingest if:

- the source is not public
- the source cannot be linked
- the source depends on leaked/private/classified material
- the object attempts to adjudicate truth instead of anchoring replayable evidence
- the object blends observation and interpretation without tags

## Status Phrase

Coherently Invalid until replayed.

Every map is incomplete.
