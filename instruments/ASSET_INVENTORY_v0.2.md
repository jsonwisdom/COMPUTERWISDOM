# COMPUTERWISDOM Asset Inventory v0.2

Class: `COMPUTERWISDOM_INSTRUMENT`

## Purpose

Produce a read-only candidate inventory for reusable repository assets while distinguishing canonical roots, legitimate native homes, and buried candidates.

v0.2 adds two corrections learned from the first full-repository audit:

1. Native execution surfaces such as `.github/workflows/` are not automatically treated as misplaced instruments.
2. Markdown can become a whitepaper candidate from content structure, not filename alone.

Every classification includes a machine-readable `classification_basis` and remains review-only.

```text
CLASSIFICATION_REQUIRES_REVIEW=true
MOVES_PERFORMED=false
AUTHORITY_CREATED=false
```

Canonical executable: `executables/asset_inventory_v0_2.py`
