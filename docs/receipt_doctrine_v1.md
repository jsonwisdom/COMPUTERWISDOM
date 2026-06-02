# Receipt Doctrine v1

**Authority:** false  
**Purpose:** AL doctrine artifact defining the lifecycle of a receipt.

---

## Core Principles

1. **A receipt is an immutable claim with a verifiable hash.**
2. **A receipt must include the exact claim text and its SHA-256 hash.**
3. **A receipt must reference its source, such as a URL or document.**
4. **A receipt must have `authority: false`.**
5. **A receipt may be corrected by publishing a new receipt that supersedes it.**

---

## Receipt Lifecycle

```text
Create -> Validate -> Publish -> Reference -> Optional Supersede
```

- **Create:** Author writes claim, source, and hash.
- **Validate:** CI checks schema and hash consistency.
- **Publish:** Receipt becomes available at a stable public URL.
- **Reference:** Other systems, including games and dashboards, link to it.
- **Supersede:** If drift is found, a new receipt is published and the old one remains as history.

---

## Drift Handling

- **Drift is not deletion.** The original receipt stays visible.
- **Correction creates a new receipt** with a `supersedes` field pointing to the old one.
- **Drift repair log** documents why the change was made.

---

## Receipt Schema: Minimal

```json
{
  "receipt_type": "PUBLIC_RECORD_VERIFICATION_V1",
  "authority": false,
  "claim": "...",
  "claim_hash": "sha256:...",
  "source_uri": "https://...",
  "timestamp_utc": "ISO8601",
  "supersedes": "REC-XXXXXX"
}
```

`supersedes` is optional and should be omitted when there is no prior receipt.

---

## Canon

A receipt is a promise you can verify. Authority is false.
