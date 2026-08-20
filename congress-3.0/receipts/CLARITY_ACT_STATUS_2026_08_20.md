# CLARITY Act — Legislative Status Receipt — 2026-08-20

**Bill:** H.R. 3633 — Digital Asset Market Clarity Act of 2025  
**Operator label:** `jaywisdom.base.eth`  
**Repository:** `jsonwisdom/COMPUTERWISDOM`  
**Lane:** `congress-3.0`  
**Classification:** `PUBLIC_SOURCE_LEGISLATIVE_STATUS_RECEIPT`  
**Observed through:** `2026-08-20`  
**Authority created:** `false`

## Current state

```text
HOUSE_PASSED              = YES
HOUSE_VOTE                = 294-134
HOUSE_PASSAGE_DATE        = 2025-07-17

SENATE_BANKING_ADVANCED   = YES
SENATE_BANKING_VOTE       = 15-9
SENATE_BANKING_DATE       = 2026-05-14

SENATE_PASSED             = NO
ENACTED                   = NO
LAW                       = NO
```

## Next official receipt edge

On August 8, 2026, Senate Majority Leader John Thune filed cloture on the motion to proceed to Calendar No. 423, H.R. 3633. The Senate schedule states that the cloture motion ripens on Tuesday, September 15, 2026 at 2:15 PM Eastern / 1:15 PM Central.

```text
NEXT_EVENT = CLOTURE_ON_MOTION_TO_PROCEED
NEXT_EVENT_TIME_ET = 2026-09-15T14:15:00-04:00
NEXT_EVENT_TIME_CT = 2026-09-15T13:15:00-05:00
FINAL_PASSAGE_VOTE = NO
```

## BoxDee membranes

```text
CLOTURE != FINAL_PASSAGE
MOTION_TO_PROCEED != BILL_PASSAGE
PASSED_HOUSE != LAW
COMMITTEE_ADVANCE != LAW
CALENDAR_EVENT != PROOF
MARKET_ODDS != LEGISLATIVE_STATE
MODEL_OUTPUT != LEGISLATIVE_ACTION
AUTHORITY_CREATED = FALSE
```

## Official source pointers

1. Congress.gov — H.R. 3633 actions / House passage:
   https://www.congress.gov/bill/119th-congress/house-bill/3633/all-actions

2. Congressional Record — House vote 294-134, Roll No. 199:
   https://www.congress.gov/congressional-record/volume-171/issue-123/house-section/article/H3449-1

3. Senate Banking Committee — advanced 15-9 on May 14, 2026:
   https://www.banking.senate.gov/newsroom/majority/chairman-scott-senate-banking-committee-advance-clarity-act-in-historic-bipartisan-vote

4. U.S. Senate — cloture motions, 119th Congress; H.R. 3633 motion to proceed filed August 8, 2026:
   https://www.senate.gov/legislative/cloture/119.htm

5. Senate schedule — cloture motion ripens September 15, 2026 at 2:15 PM:
   https://www.democrats.senate.gov/2026/08/08/schedule-for-pro-forma-sessions-and-monday-september-14-2026

## Source-surface note

The Congress.gov bill tracker currently exposes the House passage and an older Senate referral state, while the Senate's current cloture and schedule pages expose later 2026 procedural activity. This is a source-surface freshness delta, not evidence that the two official sources conflict about enactment.

```text
CONGRESS_GOV_BILL_TRACKER_FRESHNESS = LAGGING_RELATIVE_TO_SENATE_SCHEDULE
SENATE_CLOTURE_PAGE = CURRENT_PROCEDURAL_SOURCE
LAW_STATUS = NOT_ENACTED
```

## User-supplied outlook fields — not promoted

The supplied market-probability estimates and CFTC fallback characterization are not part of this receipt's verified legislative state unless separately source-bound.

```text
MARKET_ODDS = HOLD / USER_SUPPLIED / NOT_REPLAYED_HERE
CFTC_FALLBACK = HOLD / NOT_PROMOTED_BY_THIS_RECEIPT
```

## Replay rule

After the next Senate action, record only the observed delta:

```text
SOURCE -> ACTION -> VOTE/RESULT -> NEW_LEGISLATIVE_STATE -> RECEIPT -> REPLAY
```

No later state is inferred from the scheduled vote itself.
