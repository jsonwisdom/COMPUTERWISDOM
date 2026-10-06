# HC 584 GOV.UK Primary-Source Pin V0.1

**Receipt ID:** `HC_584_GOVUK_PRIMARY_SOURCE_PIN_V0_1`  
**Receipt Type:** `PUBLIC_RECORD_PRIMARY_SOURCE_PIN_V0_1`  
**Authority Created:** `false`  
**Canon:** `false`  
**Retrieved:** `2026-10-06`  
**Full Source Byte Hash:** `NOT_CAPTURED`  
**Immutable Source Excerpt Snapshot:** `receipts/sources/HC_584_GOVUK_IMPLEMENTATION_EXCERPT_SNAPSHOT_V0_1.txt`  
**Snapshot Bytes:** `2327`  
**Snapshot SHA-256:** `a44da7358fa266bfb504604c8a187426c85b58332d67590c3c3ff9b9e09cfe75`

## Bounded Claim

> HC 584 was published by the Home Office on 3 September 2026 and states that specified changes take effect on 8 October 2026, with additional specified changes taking effect on 29 October, 30 November, and 9 December 2026.

**Claim SHA-256:** `41a48956d9f0b325fff0923e311c89cf903ee3e020b74318a8896f206e1e1a9c`

## Primary Source

**Publisher:** Home Office  
**Title:** Statement of changes to the Immigration Rules: HC 584, 3 September 2026  
**Publication date:** 3 September 2026  
**Source URL:** https://www.gov.uk/government/publications/statement-of-changes-to-the-immigration-rules-hc-584-3-september-2026  
**Accessible text URL:** https://www.gov.uk/government/publications/statement-of-changes-to-the-immigration-rules-hc-584-3-september-2026/statement-of-changes-to-the-immigration-rules-hc-584-3-september-2026-accessible

## Source-Bound Findings

- The GOV.UK publication page identifies the document as HC 584 and states it was published on 3 September 2026 by the Home Office.
- The preserved source excerpt snapshot contains the `Implementation` section used for the implementation-date finding.
- That excerpt states that specified paragraphs take effect on 8 October 2026.
- It further states that other specified paragraphs take effect on 29 October 2026, 30 November 2026, and 9 December 2026.
- For one set of 8 October changes, applications made before 8 October 2026 are to be decided under the Immigration Rules in force on 7 October 2026.

## Snapshot Boundary

The repository preserves the **retrieved implementation excerpt**, not the complete GOV.UK response bytes.

`EXCERPT_SNAPSHOT_HASHED = true`  
`FULL_SOURCE_BYTES_HASHED = false`  
`EXCERPT_PIN != FULL_PAGE_BYTE_PIN`

The bounded implementation-date finding is replayable from the immutable excerpt snapshot. A future change to the live GOV.UK page does not rewrite this snapshot.

## Scope Boundary

This receipt verifies what the preserved primary-source excerpt says. It does **not** establish:

- any section 40 British-citizenship deprivation order;
- any U.S. denaturalization action;
- any extradition request;
- any finding about the contents of the reported 5 October complaints;
- any legal conclusion about a specific person.

## Invariants

`US_COMPLAINT != SECTION_40_ORDER`  
`EXTRADITION != DENATURALIZATION`  
`TRAVEL_AUTHORISATION != CITIZENSHIP`  
`SOURCE_PIN != PERSON_SPECIFIC_FINDING`  
`SEARCH_MISS != ABSENCE`

## Replay

1. Read `receipts/sources/HC_584_GOVUK_IMPLEMENTATION_EXCERPT_SNAPSHOT_V0_1.txt`.
2. Recompute SHA-256 over its exact UTF-8 bytes; it must equal `a44da7358fa266bfb504604c8a187426c85b58332d67590c3c3ff9b9e09cfe75`.
3. Locate the `Implementation` heading in the snapshot.
4. Confirm the listed effective dates: 8 October, 29 October, 30 November, and 9 December 2026.
5. Hash the bounded claim above as UTF-8 with no trailing newline; it must equal `41a48956d9f0b325fff0923e311c89cf903ee3e020b74318a8896f206e1e1a9c`.

## State

`HC_584_IMPLEMENTATION = PRIMARY_SOURCE_VERIFIED_BY_EXCERPT_PIN`  
`FULL_SOURCE_BYTE_IDENTITY = NOT_CAPTURED`  
`PERSON_SPECIFIC_APPLICATION = NOT_EVALUATED`  
`AUTHORITY_CREATED = false`  
`CANON = false`
