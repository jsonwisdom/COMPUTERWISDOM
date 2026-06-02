# Public Record Verification Receipt

**Receipt ID:** `demo_receipt_001`  
**Receipt Type:** PUBLIC_RECORD_VERIFICATION_DEMO_V1  
**Authority:** `false`

## Claim

> ~~The FY2024 budget allocates $63.1 billion for the Department of Housing and Urban Development.~~ *(incorrect — drift detected and corrected)*  
> **CORRECTED CLAIM:** The FY2024 Budget requests $73.3 billion in gross discretionary appropriations for the Department of Housing and Urban Development.

## Source

**Primary Source:** [CRS Report IF12278 – HUD Appropriations, FY2024](https://crsreports.congress.gov/product/pdf/IF/IF12278)

**Archive Backup:** [Wayback Machine](https://web.archive.org/web/20230315000000/https://crsreports.congress.gov/product/pdf/IF/IF12278)

**Source Status:** User-reported source quote and archive candidate pending independent source-page confirmation.

## Claim Hash

`sha256:5ece344efd4d5f5b83c53bfd0e03bd518694f8c4c5f5200b44913c14c2c23bfc`

## Timestamp

`2026-06-02T23:30:00Z`

## Replay Steps (anyone can verify)

1. Open the [CRS source](https://crsreports.congress.gov/product/pdf/IF/IF12278) or archive backup.
2. Locate the HUD FY2024 budget request figure.
3. Confirm the figure: **$73.3 billion**.
4. Copy the exact corrected claim text:

> "The FY2024 Budget requests $73.3 billion in gross discretionary appropriations for the Department of Housing and Urban Development."

5. Run the verification command:

```bash
CLAIM='The FY2024 Budget requests $73.3 billion in gross discretionary appropriations for the Department of Housing and Urban Development.'
printf '%s' "$CLAIM" | sha256sum
```

6. The output must match: `5ece344efd4d5f5b83c53bfd0e03bd518694f8c4c5f5200b44913c14c2c23bfc`

## Drift Correction Log

| Field | Original Incorrect Value | Corrected Value |
|-------|---------------------------|-----------------|
| Claim | $63.1 billion | $73.3 billion |
| Hash | d7b050351ca6798af50a2b53bce2576ab9a97ad918792880abbbc523070b910e | 5ece344efd4d5f5b83c53bfd0e03bd518694f8c4c5f5200b44913c14c2c23bfc |
| Source | White House PDF | CRS IF12278 / archive candidate |

Drift detected: The original claim did not match the reported official-source figure.

Drift resolved: Receipt now uses the corrected claim text and independently recomputed SHA-256 hash.

Drift documented: This entry preserves the before/after correction path.

## Success Criteria

- Source is public and authoritative candidate
- Hash can be recomputed by anyone
- No trusted third party required
- Drift documented with before/after
- Authority remains false

## Canon

This site does not ask you to trust it. It gives you the math to verify it.

Not anti-news. Anti-drift. Public receipts from day one.
