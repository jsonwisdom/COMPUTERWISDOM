# MULTI-OVERSIGHT MESH v0.1

**Project state:** v0.3 scoring model locked into mesh operational standard  
**Repository:** `jsonwisdom/COMPUTERWISDOM`  
**PR target:** `#512`  
**Source head before this bind:** `311ed1c373d65bc337d8f270bffd735e89328dd6`  
**AUTHORITY_CREATED:** false  
**PROOF_INFERRED:** false

## Purpose

This file separates **review depth** from **evidence depth** and **novelty depth** so repeated institutional review cannot masquerade as independent corroboration.

> **Independent review is not independent evidence.**  
> **10 desks × 1 receipt = 10 reviews ≠ 10 receipts.**

The mesh counts who reviewed a proposition, what independent receipt families exist, and whether a later source adds genuinely new evidentiary content.

## Typed independence classes

Every reviewer / institution / source-family edge must be typed as one of:

```text
INTERNAL
DEPARTMENTAL
STATUTORILY_INSULATED
JUDICIAL
LEGISLATIVE
EXTERNAL_AUDIT
PUBLIC_REPLAY
```

A change of class increases institutional diversity only. It does **not** automatically increase evidence depth or novelty depth.

## Depth axes

### REVIEW_DEPTH

Number of meaningfully distinct review layers that have handled, referenced, challenged, supervised, adjudicated, audited, or replayed the proposition.

```text
REVIEW_DEPTH += 1
only when a distinct review layer is independently documented.
```

Review depth measures institutional processing, not factual corroboration.

### EVIDENCE_DEPTH

Number of distinct evidentiary families materially supporting or testing the proposition.

Examples of distinct families may include:

```text
original flight log / manifest
contemporaneous email summarizing records
witness interview / proffer
registration record
court exhibit
financial record
independent audit record
```

Two documents derived from the same underlying source family do not automatically count twice.

### NOVELTY_DEPTH

Number of evidentiary families that add materially new facts, fields, dates, actors, routes, custody information, or contradictions not already present in prior receipt families.

```text
NEW REVIEWER + SAME RECEIPT = NOVELTY_DEPTH +0
NEW FORMAT + SAME UNDERLYING DATA = NOVELTY_DEPTH +0
DISTINCT WITNESS / DISTINCT PRIMARY RECORD = candidate +1
```

Novelty must be source-bound.

## Central theorem

```text
INDEPENDENT_REVIEW != INDEPENDENT_EVIDENCE
```

Corollaries:

```text
REVIEW_DEPTH != EVIDENCE_DEPTH
EVIDENCE_DEPTH != NOVELTY_DEPTH
HIGH_REVIEW_DEPTH != HIGH_CONFIDENCE_BY_ITSELF
MULTIPLE_AGENCIES_REPEATING_ONE_RECORD != MULTIPLE_RECEIPTS
OFFICIAL_REPETITION != INDEPENDENT_CORROBORATION
```

## Hard institutional separations

```text
OIG != COURT
COURT != CONGRESS
CONGRESS != PROSECUTOR
PROSECUTOR != FBI_INTERNAL
INTELLIGENCE_OVERSIGHT != CRIMINAL_ADJUDICATION
```

These separations are authority and review-layer distinctions. They do not create new facts.

## Current scoring — supplied v0.3 state

| Asset | REVIEW_DEPTH | EVIDENCE_DEPTH | NOVELTY_DEPTH | Status |
|---|---:|---:|---:|---|
| `EFTA00028716` — SDNY AUSA Email | `>=3–4` | `1` | `0` | `BOUND (aggregate only)` |
| Maxwell NDFL Proffer — Jul 2025 | `1` | `+1` | `+1` | `PROVEN (witness layer only)` |
| Combined Mesh | `4–5` | `2` | `1` | `PARTIAL — context rich, row-level poor` |

### Interpretation

The SDNY email has accumulated substantial **REVIEW_DEPTH**, but it remains one receipt family for the aggregate flight proposition. Re-review, republication, congressional reference, DOJ processing, or public replay of that same email does not increase `EVIDENCE_DEPTH` or `NOVELTY_DEPTH` unless a distinct source family enters the mesh.

The Maxwell NDFL proffer adds a distinct witness-derived source family. It therefore raises `EVIDENCE_DEPTH` and `NOVELTY_DEPTH` for contextual propositions supported by that interview. It does **not** authenticate row-level flight dates, tails, routes, or passenger manifests merely by discussing people or events associated with the broader corpus.

## Row-level flight membrane

```text
AGGREGATE EMAIL CLAIM
!= ROW-LEVEL MANIFEST

WITNESS PROFFER
!= FLIGHT-ROW AUTHENTICATION

TRUMP / EPSTEIN / MAXWELL CONTEXT
!= SAME-FLIGHT PROOF

SAME TIME WINDOW
!= SAME ROW

PASSENGER LISTING
!= MISCONDUCT
```

Current row-level state remains:

```text
EXACT_FLIGHT_DATE              = HOLD unless source-bound row exists
EXACT_TAIL_NUMBER              = HOLD unless source-bound row exists
EXACT_ORIGIN_DESTINATION       = HOLD unless source-bound row exists
TRUMP_MAXWELL_EPSTEIN_SAME_ROW = HOLD unless same manifest row binds all three
GEOJSON_ROUTE                  = HOLD unless endpoints bind to same row
```

## Source-ID collision guard

The current v0.3 scoring supplied for this mesh identifies the SDNY AUSA email as `EFTA00028716`.

A prior replay thread identified the aggregate Jan. 2020 SDNY flight-record email as `EFTA00016732`.

The mesh must **not silently merge those identifiers**.

```text
EFTA00028716 == EFTA00016732
= HOLD_PENDING_PRIMARY_BYTE_COMPARISON
```

Required resolution:

```text
FETCH BOTH PRIMARY BYTES
→ HASH EACH FILE
→ COMPARE PAGE CONTENT
→ COMPARE EMAIL TIMESTAMP / SUBJECT / TEXT
→ RESOLVE SAME_OBJECT | DISTINCT_OBJECT | VERSION_RELATION
```

Until that comparison is complete, each identifier remains a distinct source pointer even if narrative descriptions appear similar.

## Mesh promotion rules

```text
NEW REVIEW LAYER
→ REVIEW_DEPTH candidate

NEW DOCUMENT FROM SAME RECEIPT FAMILY
→ REVIEW_DEPTH candidate
→ EVIDENCE_DEPTH +0 unless independently sourced
→ NOVELTY_DEPTH +0 unless materially new evidence

DISTINCT PRIMARY RECORD / DISTINCT WITNESS FAMILY
→ EVIDENCE_DEPTH candidate +1
→ NOVELTY_DEPTH candidate +1 only if materially new

ROW-LEVEL PRIMARY RECEIPT
→ may promote row-specific date/tail/route fields

NO ROW-LEVEL RECEIPT
→ aggregate remains aggregate
```

## Mesh scoring object

```json
{
  "mesh_version": "MULTI_OVERSIGHT_MESH_V0_1",
  "scoring_model": "v0.3",
  "review_depth": null,
  "evidence_depth": null,
  "novelty_depth": null,
  "independence_classes": [],
  "receipt_families": [],
  "row_level_receipts": [],
  "authority_created": false,
  "proof_inferred": false
}
```

## Operational rule

A mesh is not a vote.

A proposition does not become true because more offices touch it. Review layers increase visibility into institutional handling. Only distinct, source-bound evidence can increase evidentiary depth, and only genuinely new information can increase novelty depth.

## Standing order

> **Count the desks. Count the receipts. Never confuse the two.**

And for the aircraft corpus:

> **Context can deepen before the rows do. Do not draw the route until the row earns the line.**
