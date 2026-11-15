# CI-FIRST · New York G0 Acquisition Attempt · 2026-11-14

**Status: G0 UNKNOWN · G1 SOURCE-BOUND UNKNOWN · RELEASE CLOSED**

## Requested source
- Issuer: New York State Office of the State Comptroller (OSC)
- Original sought: New York State **FY 2025 Annual Comprehensive Financial Report**
- Declared URL: https://www.osc.ny.gov/files/reports/finance/pdf/annual-comprehensive-financial-report-2025.pdf
- Fiscal year ended: 2025-03-31
- Original PDF SHA-256: **UNKNOWN / NOT CAPTURED**
- Original byte count: **UNKNOWN / NOT CAPTURED**
- Original CAS path: **NOT CREATED**
- Provenance authentication: **UNKNOWN**
- RFC 3161 or Sigstore/Rekor independent attestation: **NONE**

## Acquisition attempts this session
1. Direct web browser open of OSC's original ACFR URL failed with HTTP 403.
2. Container download of the same exact URL failed.
3. Container Python requests to osc.ny.gov, and separately to NY OpenBudget, failed name resolution. No original PDF bytes were written into the working container.
4. **DO NOT** invent a digest from web text, scraped excerpts, search snippets, or screenshots. No G0 promotion.

## Public visual / textual verification without original bytes
- OSC's separately published **2025 Financial Condition Report**:
  https://www.osc.ny.gov/files/reports/finance/pdf/2025-financial-condition-report.pdf
  - Printed report page **3**, “Condensed Statement of Activities – Primary Government”: governmental expenses **266,785**, program revenues **133,802**; education **50,679**, public health **128,608**, welfare **22,592**, safety **10,962**, transportation **16,211** (USD millions).
  - Page image visually reviewed online during this session. It is a different document from the targeted ACFR and does **not** supply the target ACFR's byte digest.
- Official NY OpenBudget **FY2025 Basic Financial Statements / Single Audit Reporting Package**:
  https://openbudget.ny.gov/covid-funding/fsa/nys-single-audit-reporting-package-fy2025.pdf
  - Web text shows Table 2 (FY ended March 31, 2025): revenues **283,957**, expenses **266,785**, before-transfer change **17,172**, transfers **(5,107)**, after-transfer change **12,065** (USD millions).
  - Its original PDF bytes were **not** downloaded or hashed. Web PDF screenshot retrieval failed (cache miss). Keep it as corroborating public-source text only.
- *Primary ACFR page-index claims for the five reconciliation line receipts are not assigned here.* Do not borrow page indices from the Financial Condition Report or NY OpenBudget report and represent them as original ACFR page numbers.

## Precisely blocked release edge
`original ACFR PDF bytes → first-acquisition SHA-256 → CAS byte readback → ACFR exact page-index / excerpt cross-check`

**Result:** Source observations support the arithmetic and category labels, but only arithmetic-only PASS is established. G0 and full G1 remain UNKNOWN. No EO-to-payment linkage, external timestamp, certified PDF/A/UA, government authority, production deployment or payment is claimed.

**AUTHORITY_CREATED=false · PR #765 DRAFT / UNMERGED · RELEASE CLOSED**
