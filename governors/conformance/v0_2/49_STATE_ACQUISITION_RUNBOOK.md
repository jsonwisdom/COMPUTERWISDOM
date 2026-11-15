# CI-FIRST · 49-state original ACFR provenance onboarding · v0.1

**DRAFT: no G0 state promoted. No production, payment, or governmental authority.**

## Wolfram coverage checkpoint — November 14, 2026
- 50 states total; one NY structural reference with 3 distinct accounting scopes.
- 49 non-NY states with original-byte provenance UNKNOWN.
- FY2025 official publisher/PDF URL candidates: SC, DE, NC and MD (4/49). These are LINK-ONLY candidates, not acquired PDFs.
- 45 non-NY state publisher mappings not yet researched.
- Actual original ACFR PDFs captured by this workflow: 0/50; verified emergency-source coverage: 0/50.

## Verified official publication indexes
- SC Comptroller General: https://cg.sc.gov/financial-reports/annual-comprehensive-financial-reports-acfrs
- DE Division of Accounting: https://accounting.delaware.gov/reports-transparency/annual-comprehensive-financial-reports/
- NC Office of the State Controller: https://www.ncosc.gov/public-information/2025-annual-comprehensive-financial-report
- MD Comptroller: https://www.marylandcomptroller.gov/reports/annual-comprehensive-financial-report-acfr.html

Official PDF candidates and exact allowed HTTPS hostnames: official_pdf_candidates_v0_1.json. MD FY2025 is publicly available; only older years beyond those listed are request-only per the official index.

## Operator procedure: one state, explicit action
1. Independently inspect publisher index, FY, entity and complete original report URL. Never substitute a secondary aggregator or an excerpt.
2. On a host with network access, run exactly one authorized read-only fetch:
   python3 governors/conformance/v0_2/capture_one.py --state SC --root ./source-cas --ack-remote-access
3. Review locally emitted receipt and CAS path; offline verify:
   python3 governors/conformance/v0_2/capture_one.py --root ./source-cas --verify-receipt ./source-cas/receipts/SC_<sha256>.json
4. Preserve the raw original bytes, exact URL, observed timestamp, byte length, SHA-256 digest and readback. Never claim the agency issued or signed your SHA-256.
5. A digest and detached local receipt are self-attested observations. RFC3161/Sigstore independent timestamping may attest the observation, not magically prove publisher authenticity.
6. Bind fiscal scope, value, unit, sign, page index AND printed page number to the CAS digest. GOV, BUS and PRIMARY totals are separate scope rows. Do not clone NY accounting conventions across states.
7. Independently validate generated ISO A4 safe-margin geometry, PDF/A-2u preservation, PDF/UA-1 accessibility and PAC/second reader. Preserve full validator reports.
8. EO → enacted appropriation → payment warrant → ACFR reporting are four distinct evidentiary links. Linkage sampling denominator zero means UNKNOWN.

## Allowed evidence-state progression (not a release authorization)
OFFICIAL_URL_CANDIDATE → SOURCE_BYTE_CAPTURED_SELF_ATTESTED → SOURCE_PAGE_EXCERPTS_BOUND → ARITHMETIC_CHECKED → ARCHIVAL_VALIDATED → PAYMENT_LINKAGE_COVERAGE_MEASURED

States never advance merely because a tool runs. GitHub CI uses offline synthetic tests and registry consistency checks. No GitHub workflow makes live requests to state servers or writes production storage.

**RELEASE CLOSED · AUTHORITY_CREATED=false · NY STRUCTURAL 1/50 · ORIGINAL SOURCE G0 0/50 · EMERGENCY SOURCE 0/50.**

## South Carolina G0 CAPTURE UPDATE — 2026-11-15 UTC
Single-state acquisition GitHub Actions run `43670925379`: SUCCESS, original ACFR 316 pages, 8,651,483 bytes, SHA-256 `5aab29d6a6d5f3561e7870339180594bbe2e068428772712ec538ddaff7a36b1`.
Cross-environment artifact download and rehash: PASS. Printed page 28, Exhibit 2: five source rows × three accounting scopes, 15 figures with row-label and page-coordinate checks: PASS. Printed pages 42–43 (Exhibit A-2): located.
Immutable original bytes and first-receipt ZIP are retained in Google Drive: https://drive.google.com/file/d/186hkpuy2yUtKl2FQxhpeDpvQwE4q0fkx/view
Downloaded ZIP SHA-256 `64c7c01f010526655679cf336c64331ef829322f1480b63edb800e03740ff64f`; independently computed page-binding manifest SHA-256 `1706a8183effd34e5f9f64fe0745b666f4f82d5c2f876b85fa94c06c051e9ff8`.
**COUNTERS UPDATED:** official PDF URL mapped 4/49 (SC, DE, NC, MD), state G0 source-byte acquisition+readback **1/50 SC**; NY structural **1/50**; verified emergency-source payments **0/50**; publisher mapping pending **45/49**. The remaining 3 mapped states are URL-only. External agency-signed digest and trusted timestamp: UNKNOWN.
**No production, merge, payment, government authority or archival PDF/A certification. RELEASE=CLOSED.**
