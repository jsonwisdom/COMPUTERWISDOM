# SUPREME_SEYMOUR — CNN Money / Ownership / Control Dashboard
## 2026-09-21 live replay

AUTHORITY = FALSE
NO_CARD_LEVEL_VERDICT = TRUE
MONEY_PRESENT ≠ EDITORIAL_CONTROL
OWNERSHIP ≠ VOTING_CONTROL
SETTLEMENT_TERM ≠ EFFECTIVENESS
PRESS_ACCESS ≠ MERGER_GOVERNANCE

## 1. WBD parent money base — FY2025 actual

Source: WBD 2025 Form 10-K / FY2025 earnings release.

| Revenue line | FY2025 ($M) | Share of $37,296M |
|---|---:|---:|
| Distribution | 19,262 | 51.6% |
| Content | 9,647 | 25.9% |
| Advertising | 7,306 | 19.6% |
| Other | 1,081 | 2.9% |
| Total | 37,296 | 100.0% |

Primary source:
https://www.sec.gov/Archives/edgar/data/1437107/000143710726000020/wbd-20251231.htm

## 2. CNN standalone projection — not FY2025 actual

WBD transaction proxy materials disclose prospective Discovery Global figures:
- CNN 2026E revenue: $1.8B
- CNN 2026E Adjusted EBITDA Pre-SBC: $0.6B

These are projections, not FY2025 actuals and not GAAP actual results.

Primary sources:
https://www.sec.gov/Archives/edgar/data/1437107/000119312526108369/d115093dprem14a.htm
https://www.sec.gov/Archives/edgar/data/1437107/000119312526053002/d304272ddefm14a.htm

Scale-only arithmetic:
$1.8B / $37.296B ≈ 4.8%

This is a cross-year, cross-document comparison. It does not establish CNN advertising share, government share, or 2025 realized revenue.

## 3. Foreign equity / governance — proposition split

Reported FCC-approved structure distinguishes equity ownership from voting control.

Current replay state:
- disclosed foreign equity line: separate from authorized ceiling
- three Gulf sovereign wealth funds: major indirect non-voting equity
- Ellison family + RedBird: voting control under disclosed structure
- foreign investors: no disclosed voting rights or management/content-control rights

Public-source anchors:
https://www.reuters.com/business/media-telecom/us-fcc-approves-foreign-investment-paramount-warner-merger-deal-2026-09-17/
https://apnews.com/article/d8172aef73431968412ec33f2f0a78ce

Do not collapse:
ACTUAL_DISCLOSED_FOREIGN_EQUITY ≠ MAX_AUTHORIZED_FOREIGN_EQUITY
NON_VOTING_EQUITY ≠ EDITORIAL_CONTROL
NO_DISCLOSED_CONTROL_RIGHTS ≠ PROOF_NO_HIDDEN_SIDE_AGREEMENT

## 4. Editorial-board edge

2026-09-21 settlement reporting states that the agreement requires independent editorial boards for CNN and CBS News, subject to court approval.

Public-source anchors:
https://www.reuters.com/legal/litigation/paramount-settles-with-california-other-states-clearing-major-hurdle-warner-bros-2026-09-21/
https://apnews.com/article/1aaa7c471d8ba286ccfad92b18bc1ecf

State:
BOARD_REQUIRED = CLOSED as settlement term
COURT_APPROVED = OPEN
BOARD_EFFECTIVE = OPEN
EDITORIAL_INDEPENDENCE_PRESERVED = OPEN
EDITORIAL_CONTROL_BY_GULF_FUNDS = OPEN

## 5. Direct government-funding edge

CNN government-revenue share is not disclosed in the WBD FY2025 revenue table above.

Current state:
CNN_GOVERNMENT_REVENUE_SHARE = HOLD
CNN_AD_REVENUE_SHARE = HOLD
DIRECT_US_GOV_CNN_EDITORIAL_FUNDING = NOT ESTABLISHED IN THIS PASS

Government purchase / subscription / advertising / procurement, if found, must be split from editorial subsidy or editorial control.

GOVERNMENT_PURCHASE ≠ EDITORIAL_SUBSIDY
EDITORIAL_SUBSIDY ≠ EDITORIAL_CONTROL

## 6. Press-access rail — separate proposition family

CNN, MS NOW, and Politico filed suit on 2026-09-21 challenging White House access restrictions.

Source:
https://www.reuters.com/world/cnn-ms-now-politico-file-lawsuit-against-trump-administration-over-white-house-2026-09-21/

This does not populate merger-ownership, foreign-equity, editorial-board, or funding edges.

WHITE_HOUSE_ACCESS_CASE = SEPARATE / LIVE

## 7. Live Seymour dashboard

| Proposition | State | Source class |
|---|---|---|
| WBD_PARENT_REVENUE = $37.296B | CLOSED as FY2025 actual | SEC 10-K |
| CNN_STANDALONE_REVENUE = $1.8B | CLOSED as 2026 projection only | SEC proxy |
| CNN_STANDALONE_ADJ_EBITDA_PRE_SBC = $0.6B | CLOSED as 2026 projection only | SEC proxy |
| FOREIGN_EQUITY / AUTHORIZED_CEILING | SEPARATE propositions | FCC / reporting |
| GULF_COMMITTED_CAPITAL ≈ $24B | documented in transaction coverage | AP |
| GULF_VOTING_CONTROL | no voting rights disclosed | FCC / reporting |
| DIRECT_US_GOV_CNN_EDITORIAL_FUNDING | NOT ESTABLISHED IN THIS PASS | open |
| BOARD_TERM | CLOSED as settlement term | settlement reporting |
| BOARD_EFFECTIVENESS | OPEN | future court + practice |
| MONEY → EDITORIAL_CONTROL | OPEN | causal receipt absent |
| WHITE_HOUSE_ACCESS_CASE | SEPARATE / LIVE | federal complaint reporting |

## 8. Frozen invariants

MONEY = OBSERVABLE
OWNERSHIP = OBSERVABLE
VOTING_RIGHTS = OBSERVABLE
CONTROL_EDGE = NOT_AUTO_CLOSED
HEADLINE ≠ DENOMINATOR
NO_CARD_LEVEL_VERDICT = TRUE

The machine records disclosed money, ownership, rights, and governance separately. It does not infer editorial control from capital alone.
