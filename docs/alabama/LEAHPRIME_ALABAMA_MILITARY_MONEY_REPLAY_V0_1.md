# LEAHPRIME_ALABAMA_MILITARY_MONEY_REPLAY_V0_1

STATUS: R&D / SOURCE-BOUND
OBSERVER: jaywisdom.base.eth
AUTHORITY_CREATED: FALSE
PRODUCTION_GREEN: FALSE
NO_FAKE_GREEN: TRUE

## Purpose
Replay Alabama military power from the money layer, not the website layer.

## Core boundary

BASE WEBSITE != BASE BUDGET
PUBLIC PAGE != FINANCIAL SYSTEM
CLAIM != APPROPRIATION
APPROPRIATION != OBLIGATION
OBLIGATION != EXPENDITURE
EXPENDITURE != AUDIT_RECEIPT
COUNTY_TOTAL != INSTALLATION_BUDGET
STATE_MILITARY_DEPARTMENT != TOTAL_DOD_SPEND_IN_ALABAMA

## Source-bound starting claims

USER_REPORTED_PENDING_DIRECT_SOURCE_BINDING:
- FY2024 DoD Alabama total: $16,968,602,953
- National rank: #9
- GDP share: about 5.3%
- Defense personnel: about 50,294
- Payroll: almost $3.8B
- Madison / Huntsville: $8.302B
- Mobile: $1.247B
- Montgomery: $1.119B
- Dale / Fort Rucker: $1.019B
- Calhoun / Anniston: $476M
- Alabama Military Department FY2026 report total: $136,215,514
- State General Fund: $26.982M
- Other funds: $109.234M
- FY2026 appropriation baseline reported: $16.932M General Fund + $109.234M earmarked funds

OFFICIAL_DOD_VERIFIED:
- FY2026 DoD request: $961.6B
- discretionary: $848.3B
- mandatory / reconciliation: $113.3B
- FY2024 DoD Agency Financial Report exists as a separate audit layer.
- Defense Spending by State methodology includes contract obligations, payroll, and grants; official FY2023 release identifies DMDC and USAspending as inputs.

## Replay graph

APPROPRIATION
↓
AGENCY
↓
SERVICE
↓
COMMAND
↓
INSTALLATION
↓
PROGRAM
↓
AWARD
↓
RECIPIENT
↓
PLACE_OF_PERFORMANCE
↓
OBLIGATION
↓
EXPENDITURE
↓
AUDIT / RECEIPT

## Alabama financial nodes

- Redstone / Huntsville / Madison
- Mobile
- Montgomery / Maxwell / Dannelly / 187th
- Dale / Fort Rucker
- Calhoun / Anniston

These are financial graph nodes, not claims of installation-level budgets.

## Truth rules

1. Installation websites are not budgets.
2. Alabama Military Department appropriations are not total military spending in Alabama.
3. Federal DoD spending and state Military Department spending remain separate source classes.
4. County-level DoD totals are not individual installation budgets.
5. Every money edge must bind source identity, fiscal year, amount class, geography, and provenance before promotion.
6. REQUEST != APPROPRIATED != OBLIGATED != EXPENDED != AUDITED.

## Next bounded task

Bind the FY2024 Alabama OLDCC state source and FY2026 Alabama state budget / appropriation source objects directly, preserve source bytes or immutable references, then materialize typed money edges.

MONEY_EDGES: SOURCE_BOUND
AUTHORITY_CREATED: FALSE
NO_FAKE_GREEN: TRUE
