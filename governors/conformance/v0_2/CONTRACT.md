# CI-FIRST / Governors 50-state conformance contract v0.2

Status: **DRAFT — UNMERGED — NO RELEASE — NO AUTHORITY**. This extension belongs to GitHub draft PR #765. Public-research code is not a deployed service, a payment rail, or a government credential.

## Separation of concerns

The evidence object has seven independent layers:

0. **Semantics:** each ACFR number carries scope (governmental, primary, business-type, component units), precise ACFR label, units, reporting period, source statement and source page.
1. **Intake/provenance:** capture original bytes before extraction. Record URL, observed UTC time, byte count, SHA-256 and immutable content-addressed object path \`sha256/<digest>\`. Hashes attest comparison of bytes, *not* the source's authenticity or signing authority.
2. **Reconciliation:** parse state-specific reported revenues, expenses, transfers and special items. Compute before-transfer and after-transfer values separately; never silently equate them.
3. **A4 / archival / accessibility:** output page box must be ISO 216 A4 = 210 x 297 mm = 595.27559 x 841.88976 pt (at 72 pt/in). Target PDF/A-2u; separate target PDF/UA-1; separate veraPDF evaluations. **Do not write a PASS without validator evidence.**
4. **EO-to-payment:** each link EO/statute -> appropriation -> payment warrant -> ACFR reporting is individually sourced, provenance-receipted and unambiguous. Aggregate ratio = complete audited samples / total audited samples; sample 0 means UNKNOWN, not 100%.
5. **Release/readback:** recompute digests from stored bytes and independently read emitted artifacts back. A source-side or packet-side hash kept only in the same mutable file is not a trust anchor.
6. **Registry:** 50 entries; for unresearched states dates and accounting conventions remain UNKNOWN. No assumptions copied from NY.

## Baseline New York — first reference instance

NYS FY 2025 governmental-activities statement, USD millions:
\`283957 - 266785 = 17172\` (before transfers)
\`17172 + (-5107) = 12065\` (change in net position)
\`128608 million = USD 128.608 billion = 1,286.08 hundred-million USD\` (public health).

**G1 arithmetic subcheck PASS** on these hand-typed reported values does **not** prove G1 source-bound PASS. G1 stays UNKNOWN until an original PDF is byte-captured and the exact labeled values are located on the hashed pages. It does not prove G0 intake or EO payment linkage. FY2025 governmental expenses are not the enacted FY2025-26 All Funds budget.

## Gates

| Gate | PASS requires | Default if evidence absent |
|---|---|---|
| G0 | Original source bytes captured, hash + count independently checked | UNKNOWN |
| G1 | Arithmetic residuals within tolerance **AND** exact labeled source-page excerpts bound to a validated G0 source SHA-256 | UNKNOWN |
| G2 | Correct before/after labels, unit, period and scope; no collapsed aliases | UNKNOWN |
| G3 | All pages A4 **and content bbox inside declared 15mm margins**, veraPDF A-2u/UA-1 separate reports, independent second PDF/UA reader such as PAC + human accessibility review | UNKNOWN |
| G4 | Denominator > 0 and complete four-hop hashed evidence for each counted numerator payment | UNKNOWN |
| G5 | Produced packet and sibling manifest independently retrieved and hash checked against an **external** receipt | UNKNOWN |

**RELEASE = CLOSED** unless G0, G1, G2, G3 and G5 PASS *and* G4 has a nonzero auditable denominator. This is stricter than merely generating 50 PDFs. A policy threshold on G4 can be set and versioned separately; no threshold has been authorized in this draft.

## Archival format nuance

PDF/A-2u permits Unicode extraction but does **not** confer PDF/UA accessibility. Use tagged, semantically ordered content, meaningful alt text, document language and a separate PDF/UA-1 validator + human assistive-tech review. Do not claim PDF/UA from veraPDF alone: machine checks do not replace human checkpoints.

NARA's 36 CFR §1236.48(b), Table 1 bars the PDF/A-3 / PDF/A-4 attachment feature for **digitized permanent paper records** within that rule. NARA's separate PDF Collections transfer guidance permits PDF/A-3 or PDF/A-4f with conditions. Sibling JSON/CSV files remain this project's interoperability policy, not a blanket legal interpretation.

## Corrective risk gates (2026-11-14 review)

**A4 resizing is not layout validation:** check the bounding boxes of all visible painted operations, including text, images and paths, against declared safe margins. A4 at 210 x 297 mm with 15 mm margins leaves a box of 42.51969 .. 552.75591 pt horizontally and 42.51969 .. 799.37008 pt vertically. A Letter-origin design cropped to A4 can still fail. This paint-box check is conservative: decorative bleed fails; it cannot detect content already clipped outside the page, so visual inspection is required. The prior A4 preview's full-width header painted to the trim edge; **A4 size PASS, safe-margin FAIL** under strict mode.

**Fixture tautology:** a mathematical regression on typed 283,957 and 266,785 proves arithmetic only, not provenance. G1 is UNKNOWN until exact numeric source excerpts are cross-checked against raw G0 hashed PDF bytes. Synthetic fixtures remain explicitly synthetic. No network download from GitHub CI is allowed merely to make G0 PASS.

**Scaffold labeling:** 50 metadata placeholder entries ≠ 50 registered/verified states. NY is 1/50 structurally; verified emergency source = 0/50; complete G0 source bundles = 0/50 at this checkpoint.

**Receipt authenticity:** SHA-256 and detached receipts demonstrate matching bytes, not source authenticity, nor trusted time. An RFC 3161 timestamp token or Sigstore/Rekor transparency entry can add independently checkable anchoring; none has been obtained or claimed. Preserve the detached root receipt separate from its manifest. The absence of such an anchor keeps promotion under human review.

**NARA pinned:** prohibition appears in **36 CFR § 1236.48(b), Table 1**, not § 1236.50. The latter covers digitization image quality. Separate transfer guidance is NARA Bulletin 2014-04.

## Packaging and command examples

Packet: \`NY-FY2025-evidence.pdf\` (target PDF/A-2u, A4; not claimed compliant until passed).  
Sibling: \`NY-FY2025.manifest.json\`.  
Detached root receipt: \`NY-FY2025.manifest.sha256\` placed outside the manifest or in a signed/versioned audit log.  
Source objects: \`sha256/<digest>\` plus retrieval receipts.  
Validator: \`verapdf -f 2u NY-FY2025-evidence.pdf\`, \`verapdf -f ua1 NY-FY2025-evidence.pdf\`; preserve full XML reports and tool versions.  
Geometry/readback: \`pdfinfo -box\` and a separate page-size test; no Letter fallback.

Current NY source note: https://www.osc.ny.gov/files/reports/finance/pdf/annual-comprehensive-financial-report-2025.pdf

Sources on standards:
- https://docs.verapdf.org/cli/validation/
- https://docs.verapdf.org/validation/
- https://www.archives.gov/records-mgmt/policy/transfer-guidance-tables.html
- https://www.ecfr.gov/current/title-36/section-1236.48
- https://www.archives.gov/records-mgmt/bulletins/2014/2014-04.html

No GitHub merge, release, production Cloudflare Worker, account signing, Stripe payout or public official filing is authorized by this contract.

Current release status: CLOSED; schema version v0.2 with corrective gate patch. No cryptographic source anchoring claimed.
