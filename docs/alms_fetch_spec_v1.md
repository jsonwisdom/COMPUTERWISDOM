# ALMS Fetch Spec v1

**Authority:** false  
**Purpose:** Define how COMPUTERWISDOM retrieves receipts from ALMS.

---

## Fetch Flow

```text
COMPUTERWISDOM Game
│
├─► 1. Fetch index.json from ALMS
│
├─► 2. Find receipt by ID or name
│
├─► 3. Fetch receipt JSON from ALMS path
│
├─► 4. Validate receipt hash matches claim
│
└─► 5. Display verification result to user
```

---

## API Endpoints: Conceptual

| Endpoint | Method | Response |
|----------|--------|----------|
| `https://alms.example.com/receipts/index.json` | GET | Index of all receipts |
| `https://alms.example.com/receipts/{id}.json` | GET | Individual receipt JSON |
| `https://alms.example.com/receipts/latest/{name}.json` | GET | Latest version of a named receipt |

---

## Caching and Performance

- Index is cached for 5 minutes.
- Individual receipts are cached for 1 hour.
- Receipts are treated as immutable once published.
- Game surfaces may preload the index at startup.

---

## Error Handling

| HTTP Status | Meaning | Game Action |
|-------------|---------|-------------|
| 200 | Success | Use receipt data |
| 404 | Receipt not found | Show missing receipt error and fallback to local stub if available |
| 500 | ALMS error | Retry with exponential backoff |

---

## Fallback Mechanism

If ALMS is unreachable, COMPUTERWISDOM may fall back to a local copy of `index.json` and cached receipts.

Fallback must be visibly labeled so users know the source is cached rather than live.

---

## Verification Rule

COMPUTERWISDOM must not trust ALMS blindly.

It must:

1. Fetch receipt bytes.
2. Read the claim string exactly.
3. Compute SHA-256 over the exact claim string.
4. Compare computed hash to `claim_hash`.
5. Display MATCH or MISMATCH.

---

## Canon

> ALMS holds the memory. COMPUTERWISDOM asks for it. Authority is false.
