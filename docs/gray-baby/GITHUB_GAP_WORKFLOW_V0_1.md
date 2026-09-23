# GitHub Gap Workflow v0.1

**Former story label:** The Gap Watcher  
**Runtime label:** GitHub Gap Workflow  
**Observer:** Gray Baby / LeahPrime story form  
**AUTHORITY_CREATED:** false  
**PROOF_INFERRED:** false

## Purpose

Convert the Gap Watcher from passive visual metaphor into a fail-closed repository workflow for public-record gaps.

The workflow does not decide whether Congress, DOJ, FBI, a court, contractor, records office, or public official acted lawfully. It validates whether a proposed gap record contains the minimum receipts needed to make that claim testable.

## Quad Onion runtime

```text
O1 RECORD / REALITY
PUBLIC URL -> RESPONSE -> DOCUMENT ID -> SYSTEM OF RECORD

O2 AUTHORITY
STATUTE / APPROPRIATION / RULE -> OFFICE -> DELEGATION

O3 EXECUTION / MONEY / DATA
PROGRAM -> CONTRACT -> SYSTEM -> CUSTODIAN -> RETENTION / MIGRATION

O4 OVERSIGHT / RECOVERY
OIG / CONGRESS / COURT / ARCHIVE -> CORRECTION / RESTORATION / HOLD
```

## Gap split

```text
G0 = public access gap
G1 = record existence gap
G2 = custody gap
G3 = authority gap
G4 = budget gap
G5 = execution gap
G6 = oversight gap
```

A single HTTP error may populate `G0`; it cannot automatically populate `G1-G6`.

## Required replay

### Forward

```text
APPROPRIATION / LAW
-> OFFICE
-> PROGRAM
-> CONTRACT / SYSTEM
-> CUSTODIAN
-> RECORD
-> PUBLIC ACCESS
```

### Reverse

```text
BROKEN / MISSING PUBLIC RECORD
-> SYSTEM OF RECORD
-> CUSTODIAN
-> RETENTION / MIGRATION
-> CONTRACT / PROGRAM
-> APPROPRIATION
-> AUTHORITY
```

The pincer closes only when both directions hit the same source-bound edge.

## Congress / FBI challenge lane

The current user challenge is preserved as a proposition, not a finding:

> Can a claimed `$50,000` budget item be traced byte-by-byte from Congress/public budget authority through any FBI-related execution edge and back to an accessible public record?

Canonical machine label: `TOMS_50000`.

Until an exact bill, appropriation, report, contract, transaction, or official source is attached:

```text
BUDGET_AMOUNT_STATE = HOLD
FBI_EDGE_STATE = HOLD
AUTHORITY_EDGE_STATE = HOLD
```

## Hard rules

```text
404 != DELETED
DELETED != DESTROYED
DESTROYED != UNLAWFULLY_DESTROYED
BUDGET_CLAIM != APPROPRIATION_RECEIPT
APPROPRIATION != EXPENDITURE
EXPENDITURE != OUTCOME
DOMAIN != AUTHORITY
FBI_REFERENCE != FBI_AUTHORITY
PUBLIC_PAGE != SYSTEM_OF_RECORD
MISSING_RECORD = NEW_CUSTODY_PROPOSITION
```

## GitHub Actions gate

`.github/workflows/gap-watcher.yml` validates every JSON manifest under `data/gap-watch/`.

The gate fails closed when a manifest:

- omits required provenance/authority/status fields;
- claims authority creation;
- claims proof inference;
- promotes a `404` directly to deletion, destruction, or concealment;
- promotes a budget amount without a receipt URI;
- promotes an authority edge without an authority source;
- silently treats unresolved source labels such as `doj.gov` or `dow.gov` as canonical government authority.

## Story-to-runtime conversion

The original Gap Watcher story form says:

> Nothing crosses until the gate receives a valid key.

The GitHub implementation translates that into:

```text
NO REQUIRED RECEIPT -> HOLD
INVALID PROMOTION -> CI FAIL
VALID STRUCTURE -> PASS_STRUCTURE_ONLY
PASS_STRUCTURE_ONLY != TRUTH
```

## Standing order

> Watch the gap. Name the layer. Show the budget. Show the authority. Show the system of record. Show the custody chain. Keep the correction.
