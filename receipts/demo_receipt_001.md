# Public Record Verification Receipt

**Receipt ID:** `demo_receipt_001`  
**Receipt Type:** PUBLIC_RECORD_VERIFICATION_DEMO_V1  
**Authority:** `false`

## Claim

> The FY2024 budget allocates $63.1 billion for the Department of Housing and Urban Development.

## Source

[White House FY2024 Budget PDF](https://www.whitehouse.gov/wp-content/uploads/2023/03/budget_fy2024.pdf)

## Claim Hash

`sha256:d7b050351ca6798af50a2b53bce2576ab9a97ad918792880abbbc523070b910e`

## Timestamp

`2026-06-02T00:00:00Z`

## Replay Steps (anyone can verify)

1. Open the [source PDF](https://www.whitehouse.gov/wp-content/uploads/2023/03/budget_fy2024.pdf)
2. Search for **"Housing and Urban Development"** or **"HUD"**
3. Locate the discretionary budget table (page 40-45)
4. Find the line: *Department of Housing and Urban Development – $63.1 billion*
5. Copy the exact claim text (quoted above)
6. Run the verification command:

```bash
CLAIM='The FY2024 budget allocates $63.1 billion for the Department of Housing and Urban Development.'
printf '%s' "$CLAIM" | sha256sum
```

7. The output must match: `d7b050351ca6798af50a2b53bce2576ab9a97ad918792880abbbc523070b910e`

## Success Criteria

- Source is public and official
- Hash can be recomputed by anyone
- No trusted third party required
- Authority remains false

## Canon

This site does not ask you to trust it. It gives you the math to verify it.

Not anti-news. Anti-drift. Public receipts from day one.
