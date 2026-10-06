# HC 584 GOV.UK Primary-Source Pin V0.1

**Receipt ID:** `HC_584_GOVUK_PRIMARY_SOURCE_PIN_V0_1`  
**Receipt Type:** `PUBLIC_RECORD_PRIMARY_SOURCE_PIN_V0_1`  
**Authority Created:** `false`  
**Canon:** `false`  
**Retrieved:** `2026-10-06`  
**Source Byte Hash:** `NOT_CAPTURED`

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
- The accessible HC 584 text has an `Implementation` section.
- That section states that specified paragraphs take effect on 8 October 2026.
- It further states that other specified paragraphs take effect on 29 October 2026, 30 November 2026, and 9 December 2026.
- For one set of 8 October changes, applications made before 8 October 2026 are to be decided under the Immigration Rules in force on 7 October 2026.

## Scope Boundary

This receipt verifies what the primary GOV.UK HC 584 source says. It does **not** establish:

- any section 40 British-citizenship deprivation order;
- any U.S. denaturalization action;
- any extradition request;
- any finding about the contents of the reported 5 October complaints;
- any legal conclusion about a specific person.

`PRIMARY_SOURCE_VERIFIED` here is source-bounded to HC 584 and its implementation dates.

## Invariants

`US_COMPLAINT != SECTION_40_ORDER`  
`EXTRADITION != DENATURALIZATION`  
`TRAVEL_AUTHORISATION != CITIZENSHIP`  
`SOURCE_PIN != PERSON_SPECIFIC_FINDING`  
`SEARCH_MISS != ABSENCE`

## Replay

1. Open the GOV.UK HC 584 publication.
2. Confirm the Home Office publication date is 3 September 2026.
3. Open the accessible text.
4. Locate the heading `Implementation`.
5. Confirm the listed effective dates: 8 October, 29 October, 30 November, and 9 December 2026.
6. Hash the bounded claim above as UTF-8 with no trailing newline; it must equal `41a48956d9f0b325fff0923e311c89cf903ee3e020b74318a8896f206e1e1a9c`.

## State

`HC_584 = PRIMARY_SOURCE_VERIFIED_BY_PIN`  
`PERSON_SPECIFIC_APPLICATION = NOT_EVALUATED`  
`AUTHORITY_CREATED = false`  
`CANON = false`
