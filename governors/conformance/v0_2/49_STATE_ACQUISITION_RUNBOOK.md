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
