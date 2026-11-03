# STARCOM Delta 20 Identity Ledger v0.1

**Class:** MAX_REVERSE_REPLAY_IDENTITY_LEDGER  
**Checked:** 2026-08-19  
**Authority created:** false  
**Disposition:** PROVEN_REFERENCE / UNRESOLVED_IDENTITY / HOLD

## Purpose

Preserve the public-source mismatch in which Space Systems Command (SSC) explicitly references `Space Training and Readiness Command Mission Deltas 1, 11, 12 and 20`, while STARCOM's current public organizational surfaces identify five subordinate Space Deltas: 1, 10, 11, 12 and 13.

This ledger does not correct, infer, predict, or create a Delta 20 identity.

## Resolver discipline

```text
PERSON → TITLE → ORGANIZATION → PARENT → AUTHORITY → DATE → EVENT

REFERENCE ≠ IDENTITY
ALIGNMENT ≠ COMMAND
NUMBER_SIMILARITY ≠ SAME_UNIT
20 ≠ 10
TYPO ≠ PROVEN
PUBLICATION_LAG ≠ PROVEN
FUTURE_UNIT ≠ PROVEN
AUTHORITY_CREATED = FALSE
```

## O1 — SSC reference receipt

SSC's current System Deltas page states that System Delta 81 (Operational Test & Training Infrastructure) is operationally aligned with:

```text
Space Training and Readiness Command Mission Deltas 1, 11, 12 and 20
```

Disposition:

```text
SSC_REF_STARCOM_MD20 = PROVEN
SOURCE_CLASS = OFFICIAL_SSC_PUBLIC_WEB
```

Source checked 2026-08-19:
https://www.ssc.spaceforce.mil/About-Us/SSC-System-Deltas

## O2 — STARCOM organizational receipt

STARCOM's current About page states that STARCOM is comprised of five subordinate DELs and identifies their locations:

- Space Delta 1 — Vandenberg SFB, California
- Space Delta 10 — Patrick SFB, Florida
- Space Delta 11 — Schriever SFB, Colorado
- Space Delta 12 — Schriever SFB, Colorado
- Space Delta 13 — Joint Base Andrews, Maryland

STARCOM's current Units and Senior Leaders pages likewise expose Deltas 1, 10, 11, 12 and 13, with no public Delta 20 identity found in this 2026-08-19 check.

Disposition:

```text
STARCOM_PUBLIC_STACK_1_10_11_12_13 = PROVEN
STARCOM_MD20_PUBLIC_IDENTITY = UNRESOLVED
```

Sources checked 2026-08-19:
https://www.starcom.spaceforce.mil/About-Us/About-STARCOM/
https://www.starcom.spaceforce.mil/About-Us/Units/
https://www.starcom.spaceforce.mil/About-Us/Senior-Leaders/

## O3 — Identity fields

```text
MD20_MISSION = HOLD
MD20_COMMANDER = HOLD
MD20_ACTIVATION_DATE = HOLD
MD20_PARENT_EDGE = HOLD
MD20_LOCATION = HOLD
MD20_SUBORDINATE_UNITS = HOLD
MD20_ORGANIZATIONAL_CHART_EDGE = HOLD
MD20_REDESIGNATION_OR_ACTIVATION_MEMO = HOLD
```

No field above is promoted from the SSC alignment sentence alone.

## O4 — SYD81 anchor

System Delta 81 is independently source-bound:

- Parent: Space Systems Command
- Mission lane: Operational Test & Training Infrastructure (OTTI)
- Stand-up / assumption-of-command ceremony: 2025-09-09
- First commander: Col. Corey Klopstein
- Public mission includes high-fidelity simulation, distributed training, test/training ranges, HEAT3 development, and infrastructure supporting wargames/exercises.

Official SSC and USSF receipts establish Col. Corey Klopstein as the commander at SYD81 stand-up. SSC's leadership biography still labels him Commander, SYD81 and lists `September 2025 – Present`, but that biography is marked `Current as of October 2025`.

Therefore the 2026-current commander field remains deliberately version-bounded:

```text
SYD81_FIRST_COMMANDER = COL_COREY_KLOPSTEIN / PROVEN
SYD81_COMMANDER_AS_OF_2025_10 = COL_COREY_KLOPSTEIN / PROVEN
SYD81_CURRENT_COMMANDER_2026_08_19 = HOLD
MARGARET_MAGGIE_SULLIVAN_SYD81_COMMANDER = NOT_SOURCE_BOUND
```

No official SSC/USSF source was found in this pass establishing an August 2026 SYD81 command handoff to Col. Margaret "Maggie" Sullivan.

Sources:
https://www.ssc.spaceforce.mil/Newsroom/Article/4304610/space-systems-command-stands-up-new-operational-test-training-infrastructure-ot
https://www.spaceforce.mil/News/Article-Display/Article/4307722/ssc-stands-up-new-operational-test-training-infrastructure-system-delta/
https://www.ssc.spaceforce.mil/About-Us/Leadership/Display/Article/3555646/corey-j-klopstein

## Temporal inconsistency note

The September 2025 SSC stand-up article describes STARCOM's Space Deltas as 1, 10, 11, 12 and 13. The later/current SSC System Deltas page describes SYD81 as operationally aligned with STARCOM Mission Deltas 1, 11, 12 and 20.

This is a public-surface delta that must be preserved rather than silently reconciled:

```text
2025_SSC_STARCOM_STACK = 1 / 10 / 11 / 12 / 13
CURRENT_SSC_SYD81_ALIGNMENT = 1 / 11 / 12 / 20
CURRENT_STARCOM_PUBLIC_STACK = 1 / 10 / 11 / 12 / 13

CROSS_SURFACE_CONSISTENCY = FAIL_PARTIAL
IDENTITY_RESOLUTION = HOLD
```

## Hypothesis quarantine

The following explanations are possible but not established:

```text
TYPO_20_FOR_10 = POSSIBLE / NOT_PROVEN
PUBLICATION_LAG = POSSIBLE / NOT_PROVEN
FUTURE_OR_TRANSITION_UNIT = POSSIBLE / NOT_PROVEN
MISSION_DELTA_REDESIGNATION = POSSIBLE / NOT_PROVEN
INTERNAL_OR_NONPUBLIC_UNIT = POSSIBLE / NOT_PROVEN
```

None may be promoted without an official receipt.

## Resolution witnesses

Any of the following could move the identity from HOLD if issued by an authoritative USSF/STARCOM source and internally consistent:

- Mission Delta 20 public webpage
- mission statement
- commander / senior enlisted leader listing
- activation or redesignation date
- assumption/change-of-command announcement
- STARCOM organizational chart
- official fact sheet
- parent-command statement
- subordinate-unit listing
- activation/redesignation memorandum or equivalent public release

## LeahPrime / Gray Baby membrane

```text
FICTIONAL_LEAHPRIME ≠ USSF_PERSON
LEAHPRIME_STORY_ROLE ≠ STARCOM_COMMAND
STRUCTURAL_RHYME ≠ INSTITUTIONAL_EQUIVALENCE
ARTWORK ≠ COMMAND
INSPIRED_NOT_AFFILIATED = TRUE
AUTHORITY_CREATED = FALSE
```

## Canonical MAX object

```json
{
  "object": "STARCOM_MD20_IDENTITY",
  "version": "0.1",
  "checked": "2026-08-19",
  "ssc_reference": "PROVEN",
  "starcom_public_identity": "HOLD",
  "mission": "HOLD",
  "commander": "HOLD",
  "activation_date": "HOLD",
  "parent_edge": "HOLD",
  "location": "HOLD",
  "typo": "NOT_PROVEN",
  "publication_lag": "POSSIBLE_NOT_PROVEN",
  "future_transition_unit": "POSSIBLE_NOT_PROVEN",
  "authority_created": false
}
```

## End state

`REFERENCE_BOUND / IDENTITY_UNRESOLVED / CONTRADICTION_PRESERVED / AUTHORITY_SEPARATED / REPLAY_OPEN`
