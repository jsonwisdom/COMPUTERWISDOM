# Amy K Career Full-Corpus ReverseReplay v0.2

SYSTEM: BoxD
CLASS: PUBLIC_RECORD_ACCESS_AND_AUTHORITY_REPLAY
AUTHORITY_CREATED: false
PROOF_INFERRED: false

## Scope correction

The unit of audit is Amy Klobuchar's full public-service career, not a single fraud statement or a 2022-2025 press-release sample.

Career rails:
1. Hennepin County Attorney, 1999-2006.
2. U.S. Senate, January 3, 2007-present.

The audit must enumerate the record classes before drawing narrative conclusions.

## Required corpus classes

COUNTY ERA:
- schedules
- travel records
- caseload statistics
- charging/prosecution policies
- public statements / releases
- court filings and appellate appearances
- data-practices requests and responses
- annual reports / budget / staffing

SENATE ERA:
- Congressional Record remarks
- Senate-site news releases
- floor speeches / prepared remarks
- committee hearing remarks and transcripts
- letters to agencies
- votes
- sponsored/cosponsored legislation
- appropriations / funding claims
- U.S. Attorney recommendation/confirmation statements
- Minnesota fraud-specific statements

## Bound official anchors as of 2026-08-19 replay

- Official congressional biography: Hennepin County Attorney 1999-2006; Senate service began January 3, 2007.
- Congress.gov member profile exposes at least 1,518 entries classified as Remarks in the Congressional Record and more than 8,400 total member-activity records. Total activity is NOT a speech count.
- Congress.gov provides a Member Remarks / Congressional Record retrieval path; therefore `NO_ACCESS_TO_ANY_SENATE_REMARKS` is rejected.
- A 2006 Minnesota Department of Administration Data Practices advisory opinion found that the Hennepin County Attorney's Office did not respond timely to multiple data requests, including Klobuchar schedules/travel records, labor-grievance information, Domestic Fatality Review Board matters, and caseload statistics. This is an official historical ACCESS_FRICTION receipt. It is not proof of fraud, motive, concealment, or DARVO.

## Career exposure math

County era = 8 calendar years. If treated as full calendar years for a stress-test only: 2,922 days.
Senate era, 2007-01-03 through 2026-08-19 inclusive = 7,169 days.
Combined stress-test exposure = approximately 10,091 public-service days.
Exact county first/last service dates remain to be independently bound before promoting the combined day count from BOUND to PROVEN.

Feeding Our Future communication window used by the prior allegation:
2022-01-20 through 2025-12-31 inclusive = 1,442 days.
If the user-supplied/secondary count of 1,085 press releases is accepted only as an input pending enumeration:
- 1,085 / 1,442 = 0.7524 releases per day
- 1 release every 1.329 days
This is publication-density math, not proof of what subjects were omitted.

## Jason quadratic access math

For each period t and record class c:

DECLARED(t,c) = number of records the official index/archive says exist
RETRIEVED(t,c) = number of primary records actually retrieved and bound
GAP(t,c) = DECLARED(t,c) - RETRIEVED(t,c)
P(t) = Minnesota population for that period
A(t,c) = authority/relevance weight declared before review

ACCESS_GAP_QUADRATIC(t,c) = A(t,c) * GAP(t,c)^2 / P(t)

Do NOT use a fixed 5,000,000 population across a 27-year career. Use contemporaneous annual Minnesota population when population normalization matters.

A high quadratic gap means the corpus is incomplete relative to an official declared/indexed count. It does NOT prove suppression, fraud, intent, or wrongdoing.

## Quad Onion

O1 RECORD / REALITY
Enumerate every record class and bind date, source URI, title/identifier, office held, and retrieval state.

O2 AUTHORITY
Map what Klobuchar could actually do on that date: county prosecutor authority vs legislative/oversight/appropriations/advice-and-consent authority.

O3 EXECUTION / MONEY / DATA
Bind appropriations, agency resources, prosecutions, case numbers, contracts, grants, staffing, payments, and measurable execution outputs. Statement != execution.

O4 OVERSIGHT / RECOVERY
Bind court review, inspectors general, Minnesota Legislative Auditor, Minnesota Data Practices opinions, Congressional oversight, corrections, and archive-access failures.

## Evidence states

PROVEN = primary receipt supports the proposition.
BOUND = proposition holds only within explicit limits.
HOLD = corpus incomplete or authority edge unbound.
CONFLICT = credible receipts materially disagree.
REJECT = required edge fails.

## Current corrections

- `ONE_ANSWER_FROM_ONE_STATEMENT = INSUFFICIENT_SCOPE`.
- `ALL_CAREER_AUDIT = REQUIRED`.
- `NO_ACCESS_TO_ANY_AMY_RECORDS = REJECT`; many Senate records are publicly indexed.
- `UNIFIED_COMPLETE_PUBLIC_CAREER_CORPUS_EXISTS = HOLD`; no complete corpus has yet been enumerated across county + Senate + committee + court + archive surfaces.
- `HISTORICAL_ACCESS_FRICTION_AT_HENNEPIN = PROVEN` for the specific 2005-2006 data requests addressed by Minnesota Advisory Opinion 06-029.
- `ACCESS_FRICTION = FRAUD` is REJECT.
- `SILENCE = DARVO` is REJECT unless Deny + Attack + Reverse is separately evidenced.

## Next deterministic gate

Build a career manifest before evaluating rhetoric:

YEAR -> OFFICE -> DAYS -> OFFICIAL OUTPUT CLASS -> DECLARED COUNT -> RETRIEVED COUNT -> FRAUD-SPECIFIC COUNT -> MINNESOTA-SPECIFIC COUNT -> AUTHORITY EDGE -> MONEY/EXECUTION EDGE -> OVERSIGHT RECEIPT -> EVIDENCE STATE

No narrative promotion until the manifest is populated.