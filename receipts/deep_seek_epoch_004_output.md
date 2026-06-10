# Compute Wisdom Direct · Repo-Native Receipt Machine

**Status:** CANDIDATE IMPLEMENTATION PLAN — not live  
**Session:** DEEP_SEEK_EPOCH_004  
**Canon:** Compute Wisdom Direct turns the repo into a receipt machine. No piece moves without a receipt.

---

## 1. Purpose Statement

Compute Wisdom Direct is the native receipt engine inside the COMPUTERWISDOM repo. It ingests prompts, repo files, Zora drops, court cases, and manifests; parses, tags, hashes, receipts, reviews, Merkle-roots, and rewards. It does not issue public badges, mutate portal.html, make onchain claims, or assert official authority without separate receipted approval.

---

## 2. Directory Map (Proposed)

```
COMPUTERWISDOM/
├── candidates/           # Incoming proposals (badges, services, policies)
├── services/             # Reusable service surfaces
│   ├── zora-flywheel/    # Factory schema + crawler spec
│   └── meme-court/       # Court integration
├── receipts/             # All receipts
│   ├── zora_factory/     # Factory mint receipts
│   ├── epochs/           # Epoch receipts
│   └── merkle/           # Merkle purpose keys
├── epochs/               # Epoch definitions (5D Chinese Checkers)
├── governance/           # Move-validation rules (candidate)
├── audits/               # Audit reports (secret scan, repo surface)
├── manifests/            # MANIFEST.md and future state locks
├── sessions/             # Session purpose candidates
├── _truth/               # (linked from AL) — IPFS audit manifests
├── portal.html           # PROTECTED — no mutation
└── README.md
```

---

## 3. Input Types

| Input Type | Source | Handling |
|------------|--------|----------|
| Prompts | User / Deep Seek | Capture exact, hash, store in receipts/ |
| Repo files | Git | SHA‑256 per commit, track in manifest |
| Zora drops | Zora API | Crawl, metadata hash, candidate receipt |
| Court cases | AL `_truth/meme_court/` | Cross-reference, tag, Merkle anchor |
| Receipts | Previous outputs | Chain via `previous_receipt_hash` |
| Manifests | MANIFEST.md | Single source of lock state |

---

## 4. Processing Stages

```
CAPTURE → PARSE → TAG → HASH → RECEIPT → REVIEW → MERKLE → REWARD
```

| Stage | Action | Gate |
|-------|--------|------|
| CAPTURE | Save exact prompt/output | File exists |
| PARSE | Extract claims (Confucius Indexer) | Parsing schema |
| TAG | PUBLIC/HELD/PENDING/REJECTED | No untagged claims |
| HASH | SHA‑256 of content | Hash computed |
| RECEIPT | JSON receipt with schema | Schema valid |
| REVIEW | Jay approval / changes | Manual or documented |
| MERKLE | Append to purpose key | Receipt hash included |
| REWARD | Image / badge candidate | Only after VERIFIED |

---

## 5. Gate Rules (No Exceptions)

| Rule | Enforcement |
|------|-------------|
| No public badge without VERIFIED session | `public_badge_granted: false` until promotion receipt |
| No portal.html mutation | Protected file — commit rejected if changed |
| No onchain claim without separate receipt | `onchain_claimed_live: false` |
| No official authority claim without receipted approval | `official_agency_claim: false` |
| Secret scan before any Zora image output | `secret_scan_status: COMPLETE` required |

---

## 6. Zora Factory Integration

**Current state:** Schema + example + crawler spec committed (candidate)  
**Next:** Run secret scan → verify session 003 → unlock crawler execution → generate candidate receipts for actual drops → Jay reviews → VERIFIED → Merkle append

**Factory rule:** The factory mints receipts, not delusions.

---

## 7. Meme Court Integration

**Current state:** AL repo has court infrastructure; COMPUTERWISDOM has open court candidate  
**Integration path:**  
- Cross-reference court verdicts as receipts  
- Tag verdict claims (PUBLIC/HELD)  
- Option: Meme Court receipts become Merkle leaves  
- Rule: Funny is allowed. Fake verified is not.

---

## 8. Secret Scan Integration

**Required before Zora image lane unlocks:**

```bash
git rev-list --all | xargs git grep -E "(key|secret|token|password|api_key|private_key|-----BEGIN|sk-[a-zA-Z0-9])" > receipts/secret_scan_raw_epoch_004.txt
sha256sum receipts/secret_scan_raw_epoch_004.txt
```

**Receipt:** `receipts/secret_scan_epoch_004_receipt.json` with findings (redacted if any)

---

## 9. Epoch 004 Five-Axis Move Validation

| Axis | Validation Rule | Receipt Required |
|------|----------------|------------------|
| **Time** | Past moves → future projections | Session receipt |
| **Space** | Service boundaries respected | Move-validation rule |
| **Jurisdiction** | CN/US/RU/EU/UK → Option 4 | Firewall receipt |
| **Vernacular** | Humor separated from claim | Indexer output |
| **Receipt** | Merkle root includes all moves | Merkle purpose key |

**Move rule:** No piece moves without a receipt.

---

## 10. Next Artifact List (Candidate)

| Artifact | Purpose | Status |
|----------|---------|--------|
| Secret scan receipt | Gate Zora image lane | PENDING |
| Move-validation rules (committed) | Govern dual-purpose paths | CANDIDATE EXISTS |
| Session 003 verification (Jay) | Close Girl Math case | PENDING |
| First actual Zora drop receipt | Test factory crawler | WAITING SCAN |
| Compute Wisdom Direct manifest | Lock entire machine state | PENDING |

---

## Epoch 004 Lock

> Compute Wisdom Direct turns the repo into a receipt machine.  
> Deep Seek proposes. Computer Wisdom validates.  
> Jay's Wisdom promotes.  
> No piece moves without a receipt.  
> The board remembers. The gate holds. 🧾⚙️
