# UI_WIREFRAME_SPEC_V1

Anti-Drift News — Public Evidence UX  
Public From Day One • No Authority • No Hidden State

---

## 1. Purpose

Define the public interface for Anti-Drift News:

- What users see
- What actions they can take
- How the game loop becomes visible
- How receipts, claims, and drift risk are surfaced
- How the UI stays aligned with the replay engine: no hidden state, no privileged mutation

This spec is not a design mockup.  
It is a deterministic UI contract.

---

## 2. UI Principles

1. Receipt-first  
   Every screen shows receipts, missing receipts, or the hunt for receipts.

2. No authority  
   UI never declares truth. UI only shows coverage, gaps, and drift risk.

3. Replay supremacy  
   Every visible element must be derivable from the replay engine.

4. Public from day one  
   No private dashboards, no admin panels, no hidden moderation.

5. Fun beats homework  
   The UI must feel like a game, not a civics lecture.

---

## 3. Core Screens

### 3.1 Homepage — Daily Receipt Hunts

Purpose: instantly communicate the game: find receipts for today's claims.

```txt
---------------------------------------------------------
ANTI-DRIFT NEWS  🧾⚙️
Public Receipt Hunts — Updated Daily
---------------------------------------------------------

[ Submit an Article URL ]

Today's Hunts:
---------------------------------------------------------
1. "The program saved taxpayers $2B."
   Status: 🔴 NO_RECEIPTS_FOUND
   Drift Risk: HIGH
   → View Hunt

2. "Crime dropped 40% last year."
   Status: 🟡 TRUST_ME_BRO_ZONE
   Drift Risk: MEDIUM
   → View Hunt

3. "This policy will create 1M jobs."
   Status: 🌌 QUANTUM_CLAIM
   Drift Risk: UNKNOWN
   → View Hunt
---------------------------------------------------------

Leaderboard:
Top Receipt Goblins Today
→ View Leaderboard
```

Key UI elements:

- Submit URL button
- List of active hunts
- Badges surfaced immediately
- Drift risk as a visual cue
- Zero authority language

---

### 3.2 Article Submission Page

```txt
---------------------------------------------------------
Submit an Article URL
---------------------------------------------------------

[ https://example.com/news-story ]  (input)

[ Start Receipt Hunt ]
```

On submit:

- UI creates a new hunt.
- UI redirects to `/hunt/:game_id`.
- Replay engine reconstructs state.
- UI displays claims extracted once events land.

---

### 3.3 Hunt Page — Claim + Receipt Game Board

This is the core gameplay screen.

```txt
---------------------------------------------------------
Receipt Hunt: ADN-000001
Article: https://example.com/news-story
Status: ACTIVE_RECEIPT_HUNT
---------------------------------------------------------

Claims:
---------------------------------------------------------
CLAIM-001
"The program saved taxpayers $2 billion."
Type: NUMERIC_PUBLIC_CLAIM
Receipt Status: 🔴 NO_RECEIPTS_FOUND
Drift Risk: HIGH

[ Submit Receipt ]
[ View Claim Details ]
---------------------------------------------------------

CLAIM-002
...
---------------------------------------------------------
```

Actions:

- Submit receipt
- View claim details
- See drift risk
- See badges

---

### 3.4 Claim Detail Page

```txt
---------------------------------------------------------
Claim: CLAIM-001
"The program saved taxpayers $2 billion."
---------------------------------------------------------

Receipts:
---------------------------------------------------------
R-001  PRIMARY_SOURCE
https://agency.gov/report.pdf
Status: PENDING_REVIEW
---------------------------------------------------------

Badges:
🔴 NO_RECEIPTS_FOUND
💅 GIRL_MATH_ALERT
```

UI rule: badges are derived, not stored.

---

### 3.5 Receipt Detail Page

```txt
---------------------------------------------------------
Receipt: R-001
---------------------------------------------------------

URL: https://agency.gov/report.pdf
Type: PRIMARY_SOURCE
Submitted By: receipt_goblin
Verification Status: PENDING_REVIEW
Hash: (null)
```

---

### 3.6 Leaderboard

```txt
---------------------------------------------------------
Receipt Goblin Leaderboard
---------------------------------------------------------

1. receipt_goblin — 12 receipts today
2. spreadsheet_summoner — 9 receipts
3. girl_math_enjoyer — 7 receipts
```

Rule: leaderboard is derived from events, not stored.

---

## 4. UI to Replay Engine Contract

Every UI element must map to:

- A replay query
- A subset of events
- A derived state field

No UI element may:

- Store state
- Mutate state
- Infer truth
- Override events

---

## 5. UI Actions to Event Emission

### 5.1 Submit Article

Emits:

```txt
ARTICLE_SUBMITTED
```

### 5.2 Submit Receipt

Emits:

```txt
RECEIPT_SUBMITTED
```

### 5.3 System-Driven Updates, Non-Authoritative

- `CLAIMS_EXTRACTED`
- `SCORE_UPDATED`
- `BADGE_ASSIGNED`

UI never emits these directly.

---

## 6. Badge Display Rules

Badges appear whenever their conditions are met:

- 🟢 GOBLIN_APPROVED — Verified primary source
- 🟡 TRUST_ME_BRO_ZONE — Claim with only tertiary sources
- 🔴 NO_RECEIPTS_FOUND — Zero receipts
- 💅 GIRL_MATH_ALERT — Math claim with no numbers
- 🌌 QUANTUM_CLAIM — Prediction claims
- 📊 SPREADSHEET_SUMMONED — Numeric claim with at least one spreadsheet source

Badges are fun, non-authoritative, and derived.

---

## 7. Accessibility and Constraints

- No infinite scroll
- No hidden UI states
- No admin mode
- All pages must be reachable without login
- All data must be replay-derivable

---

## 8. Canon Phrase

Not anti-news. Anti-drift. Public receipts from day one.

---

## Next Layer

- GAME_STATE_SCHEMA_V1
- ALMS_RECEIPT_CONTRACT_V1
