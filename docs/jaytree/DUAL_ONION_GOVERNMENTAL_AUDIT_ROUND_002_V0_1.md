# Round 002 — Jay's Dual Onion Governmental Audit

**Surface:** `CONGRESS_GOV`  
**Question:** `CORRECTION`  
**Receipt:** `LEGISLATIVE_RECORD`  
**Direction:** `REVERSE`  
**Burden:** `AUTHORITY`

Dice select the question. Dice do not determine the finding.

## Selected claim

On June 11, 2025, H.Res. 492 was considered passed by the House pursuant to H.Res. 499. H.Res. 492 directed the Clerk of the House to make 20 corrections in the engrossment of H.R. 1.

This round isolates one replayable delta:

```text
H.R. 1 §20005(17)
```

### Before — source-bound reported House text (`RH`)

```text
$90,000,000 for the development of reusable hypersonic technology
for military strikes and intelligence;
```

### Correction instruction — H.Res. 492

```text
In paragraph (17) of section 20005, strike "and intelligence".
```

### After — source-bound engrossed House text (`EH`)

```text
$90,000,000 for the development of reusable hypersonic technology
for military strikes;
```

## Authority chain

```text
H.RES.499 §3
  -> HOUSE RESOLUTION 492 IS HEREBY ADOPTED
  -> H.RES.492 DIRECTS CLERK CORRECTIONS TO H.R.1 ENGROSSMENT
  -> CONGRESSIONAL RECORD 2025-06-11 H2647 RECORDS THE ACTION
  -> CONGRESS.GOV PRESERVES RH + EH TEXT SURFACES
```

## Onion A — Public Government Record

```text
CURRENT / PRESERVED CONGRESS.GOV RECORD
  ↓
WHAT WAS CORRECTED?
  ↓
"and intelligence" removed from §20005(17)
  ↓
WHAT DID THE EARLIER SOURCE-BOUND VERSION SAY?
  ↓
RH = "military strikes and intelligence"
  ↓
PRIMARY LEGISLATIVE AUTHORITY
  ↓
H.RES.492
  ↓
ADOPTION AUTHORITY
  ↓
H.RES.499 §3
  ↓
HOUSE ACTION RECEIPT
  ↓
CONGRESSIONAL RECORD H2647
  ↓
PUBLICATION
  ↓
CONGRESS.GOV / LIBRARY OF CONGRESS + GPO RECORD
  ↓
ARCHIVED VERSION
  ↓
RH + EH REMAIN REPLAYABLE
  ↓
TECHNICAL CHANGE / DEPLOYMENT LOG
  ↓
NOT_PUBLICLY_BOUND_IN_THIS_ROUND
  ↓
HUMAN / INSTITUTIONAL REVIEW
  ↓
HOUSE_ACTION + CLERK_CORRECTION_AUTHORITY = BOUND
CMS_EDITOR / LOGIN / DEPLOYMENT_ACTOR = NOT_BOUND
```

## Onion B — How the record got there

```text
PUBLISHER / IDENTITY       = LIBRARY_OF_CONGRESS / GPO_PUBLIC_SURFACES
LEGISLATIVE_AUTHORITY      = HOUSE_ACTION_BOUND
CLERK_CORRECTION_AUTHORITY = BOUND
LOGIN                      = NOT_BOUND
CMS / API                  = NOT_BOUND
EDIT / ACTION              = LEGISLATIVE_TEXT_CHANGE_BOUND
DEPLOYMENT                 = PUBLICATION_OBSERVED_INTERNAL_LOG_NOT_BOUND
HOSTING / CLOUD            = NOT_BOUND
AZURE                      = NOT_BOUND
MICROSOFT                  = NOT_BOUND
ACTIVITY / AUDIT LOG       = NOT_BOUND
REVIEW                     = LEGISLATIVE_ACTION_BOUND_CMS_REVIEW_NOT_BOUND
```

## Membranes

```text
AZURE != ASSUMED
MICROSOFT != LAW
LOGIN != ACTION
ACTION != INTENT
TYPO != MISCONDUCT
CORRECTION != ORIGINAL_RECORD_DELETED
REPORTED_TEXT != ENGROSSED_TEXT
TEXT_DELTA != ERROR_CAUSE_PROVEN
CORRECTION_AUTHORIZED != MISCONDUCT_PROVEN
PUBLICATION_PLATFORM != LEGISLATIVE_AUTHORITY
```

## Round 002 disposition

```text
CLAIM_SELECTED          = TRUE
LIVE_RECORD_FETCHED     = TRUE
BEFORE_VERSION_BOUND    = TRUE
CORRECTION_BOUND        = TRUE
AFTER_VERSION_BOUND     = TRUE
HOUSE_AUTHORITY_BOUND   = TRUE
CLERK_AUTHORITY_BOUND   = TRUE
AZURE_BOUND             = FALSE
MICROSOFT_BOUND         = FALSE
LOGIN_BOUND             = FALSE
CMS_EDITOR_BOUND        = FALSE
DEPLOYMENT_LOG_BOUND    = FALSE
ERROR_CAUSE_PROVEN      = FALSE
MISCONDUCT_PROVEN       = FALSE
INTENT_PROVEN           = FALSE
GAME_STATE              = ROUND_002_REPLAYABLE
AUTHORITY_CREATED       = FALSE
```

## Official source rails

- https://www.congress.gov/bill/119th-congress/house-resolution/492
- https://www.congress.gov/bill/119th-congress/house-resolution/499
- https://www.congress.gov/congressional-record/volume-171/issue-100/house-section/article/H2647-1
- https://www.congress.gov/bill/119th-congress/house-bill/1/text/rh
- https://www.congress.gov/bill/119th-congress/house-bill/1/text/eh

Out of chaos -> source -> authority -> action -> receipt -> replay -> order.
