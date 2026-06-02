# Three-Repo Proof Stack v1

**Authority:** false  
**Purpose:** Split the proof system across AL, COMPUTERWISDOM, and ALMS.

---

## Repository Responsibilities

| Repository | Role | Contents |
|------------|------|----------|
| **AL** | Doctrine & Constitution | Authority rules, invariants, constitutional documents |
| **COMPUTERWISDOM** | Replay Surfaces & UI | Game, demo, replay client, user-facing verification |
| **ALMS** | Memory Surfaces | Receipts, drift logs, immutable event segments |

---

## Data Flow

```text
User interacts with COMPUTERWISDOM UI
│
▼
COMPUTERWISDOM fetches receipts from ALMS using public URLs or APIs
│
▼
COMPUTERWISDOM applies replay rules defined by AL doctrine
│
▼
Verification result displayed to user
```

---

## Cross-Repo Links

### COMPUTERWISDOM -> ALMS

Receipts are stored as JSON files in ALMS and served through GitHub Pages, raw GitHub URLs, IPFS, or another public mirror.

COMPUTERWISDOM reads them by URL and verifies them locally.

### COMPUTERWISDOM -> AL

COMPUTERWISDOM imports `authority: false` invariants and constitutional rules as documented constants, not as a hidden runtime dependency.

### AL -> ALMS

AL defines doctrine and schema boundaries. ALMS stores receipt instances and drift logs.

---

## Benefits

- **Separation of concerns:** UI, rules, and storage evolve independently.
- **Verifiability:** Each repo can be audited in isolation.
- **Scalability:** ALMS can host receipts without bloating COMPUTERWISDOM.
- **Resilience:** If one repo goes down, the others can still preserve their role through mirrors.

---

## Canon

> This site does not ask you to trust it. It gives you the math to verify it.  
> Not anti-news. Anti-drift. Public receipts from day one.
