# ODNI-2.0-CLASSIFICATION-COST-PINCER-001 — Execution Ledger v0.1

**Class:** public-source budget / FOIA replay architecture  
**Authority created:** FALSE  
**Proof inferred:** FALSE

## Equation

```text
NET_RECURRING_SAVINGS = (ΔP + ΔC + ΔF + ΔPr) − (T + R + I_sec + D)
```

## Evidence state

```text
$700M ODNI claim                = BOUND_AS_OFFICIAL_CLAIM
$1.3B IC-wide claim             = BOUND_AS_OFFICIAL_CLAIM
40%+ workforce reduction        = BOUND_AS_OFFICIAL_CLAIM
ODNI-specific security costs    = HOLD
Facility delta ΔF               = HOLD
Contract/program deltas         = PARTIAL / NOT_REPRODUCIBLY_CLOSED
Net savings reproduction        = HOLD
```

## Step 0 — USAspending public baseline

**Status:** PARTIAL / STRUCTURAL PUBLIC-DATA LIMIT

USAspending's current top-tier agency reference endpoint does not list ODNI / Office of the Director of National Intelligence as a top-tier agency. Therefore the proposed direct pattern

```text
/api/v2/agency/<ODNI_TOPTIER_CODE>/...
```

cannot presently be executed as written because no ODNI top-tier code is exposed in that reference list.

USAspending does expose award-, federal-account-, object-class-, program-activity-, and agency-level data for agencies present in its reporting structure. Public-source reporting also identifies a 2023 Leidos prime contract supporting ODNI with an announced $375 million value and one base year plus six option years. That contract existence/value claim is not promoted into a complete ODNI FY2024–FY2026 ΔC or ΔPr baseline without a reproducible award/funding-account crosswalk.

**Result:** Step 0 remains PARTIAL. No contract or program delta is promoted from incomplete public mapping.

## FOIA execution receipts — 2026-08-20

### Step 1 — ODNI FOIA

```text
TO = ODNI_FOIA@odni.gov
SUBJECT = FOIA Request – ODNI 2.0 Cost Methodology & Personnel Records
GMAIL_SEND_RECEIPT = 1a01da831b772e7b
STATUS = SENT / AWAITING_AGENCY_ACKNOWLEDGMENT
```

Scope: ΔP + T + R + I_sec + D + records supporting the $700M annual-savings methodology.

### Step 2 — GSA FOIA

```text
TO = gsa.foia@gsa.gov
SUBJECT = FOIA Request – ODNI Facility Costs (Reston & HQ)
GMAIL_SEND_RECEIPT = 1a01da84d7103892
STATUS = SENT / AWAITING_AGENCY_ACKNOWLEDGMENT
```

Scope: ΔF + recurring occupancy/facility costs + transition/relocation/lease actions + related contract changes.

### Step 3 — NARA / ISOO FOIA

```text
TO = foia@nara.gov
CC = isoo@nara.gov
SUBJECT = FOIA Request – ODNI Security Classification Cost Estimates
GMAIL_SEND_RECEIPT = 1a01da86e09901ae
STATUS = SENT / AWAITING_AGENCY_ACKNOWLEDGMENT
```

Scope: SF-716 or successor/equivalent classification-cost submissions, supporting worksheets, ODNI/ISOO methodology correspondence, and ODNI-specific classification/security cost categories where existing records permit segregation.

## Parallel pass — 2026-08-20

### FOIA acknowledgment check

Immediate Gmail check found no new ODNI, GSA, or NARA/ISOO acknowledgment or agency response.

```text
T_transmitted   = 3
A_acknowledged  = 0
R_retrieved     = 0
```

A recurring FOIA acknowledgment watch is active. It should notify only on a new acknowledgment, tracking number, clarification request, fee notice, denial, referral, or records response.

### USAspending alternate-route test

USAspending's API documentation confirms alternate POST routes that do not depend exclusively on the `/agency/<TOPTIER_CODE>/...` family:

```text
/api/v2/autocomplete/awarding_agency/
/api/v2/autocomplete/funding_agency/
/api/v2/search/spending_by_award/
```

The API supports agency-name and subtier filtering in Advanced Award Search. However, the indexed public surface did not yield a clean ODNI-specific awarding/funding-agency binding sufficient to close FY2024–FY2026 ΔC or ΔPr. Recipient-name searches for Leidos remain noisy across unrelated agencies.

```text
ALTERNATE_QUERY_PATH = CONFIRMED_BY_API_DOCUMENTATION
ODNI_AGENCY_BIND     = NOT_YET_REPRODUCIBLY_RESOLVED
ΔC                   = PARTIAL
ΔPr                  = PARTIAL
NO_DELTA_PROMOTED    = TRUE
```

## Filing sequence

```text
0 USAspending ΔC + ΔPr baseline = PARTIAL / ALT ROUTE IDENTIFIED
1 ODNI FOIA                     = SENT / ACK PENDING
2 GSA FOIA                      = SENT / ACK PENDING
3 NARA/ISOO FOIA                = SENT / ACK PENDING
4 CRISSCROSS                    = WAITING_ON_RECORDS
5 RECOMPUTE                     = WAITING
6 COMPARE ↔ ODNI $700M          = WAITING
```

## Standing order

> Show the numerator, show the offsets, show the fiscal baseline, and let another observer reproduce the savings.

```text
FOIA_TRANSMISSION != RETRIEVAL
EMAIL_SENT != AGENCY_RECEIVED_ACK
CLAIMED != PROVEN
CLASSIFIED != WRONGDOING
SOURCE_POINTER != FROZEN_MIRROR
AUTHORITY_CREATED = FALSE
PROOF_INFERRED = FALSE
```
