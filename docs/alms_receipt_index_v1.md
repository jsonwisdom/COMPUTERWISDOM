# ALMS Receipt Index v1

**Authority:** false  
**Purpose:** Specification for the receipt index file that maps receipt IDs to their storage locations.

---

## Index File Location

`https://alms.example.com/receipts/index.json`

Initial hosting may use GitHub Pages, raw GitHub URLs, IPFS, or another public mirror.

---

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "additionalProperties": false,
  "required": ["version", "receipts"],
  "properties": {
    "version": { "type": "string", "const": "1" },
    "updated_at": { "type": "string", "format": "date-time" },
    "receipts": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["id", "name", "path", "hash"],
        "properties": {
          "id": { "type": "string", "pattern": "^REC-[0-9]{6}$" },
          "name": { "type": "string" },
          "path": { "type": "string" },
          "hash": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" },
          "timestamp": { "type": "string", "format": "date-time" }
        }
      }
    }
  }
}
```

---

## Example `index.json`

```json
{
  "version": "1",
  "updated_at": "2026-06-02T23:30:00Z",
  "receipts": [
    {
      "id": "REC-000001",
      "name": "HUD FY2024 Budget Request",
      "path": "receipts/hud_fy2024_budget_receipt.json",
      "hash": "sha256:5ece344efd4d5f5b83c53bfd0e03bd518694f8c4c5f5200b44913c14c2c23bfc",
      "timestamp": "2026-06-02T23:30:00Z"
    }
  ]
}
```

---

## Usage in COMPUTERWISDOM

```javascript
const index = await fetch('https://alms.example.com/receipts/index.json').then((r) => r.json());
const receipt = await fetch(index.receipts[0].path).then((r) => r.json());
```

---

## Canon

An index is not a receipt. It is a map to receipts. Authority is false.
