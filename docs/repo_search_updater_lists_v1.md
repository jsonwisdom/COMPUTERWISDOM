# Repo Search Updater Lists v1

**Authority:** false  
**Purpose:** Define reusable search lanes for mapping Jay's repositories without losing family, feminine, court, index, README, or proof-system context.

---

## Core Rule

Search must not only look for technical words like `receipt`, `hash`, or `replay`.

Jay's repository system also uses family names, feminine continuity terms, court language, public proof language, and index/readme surfaces.

If those lanes are skipped, the map is incomplete.

---

## Required Search Lanes

### 1. Feminine / Guardian Lane

Search terms:

```text
feminine
woman
women
mother
wife
Mrs Wisdom
MrsWisdom
Marydee
Leeann
Grammy
Gaga
girl
girls
daughter
daughters
sister
queen
matriarch
guardian
emergency manager
continuity guardian
```

Purpose:

```json
{
  "lane": "feminine_guardian",
  "protects": ["family continuity", "emergency management", "human safety layer"],
  "authority": false
}
```

---

### 2. Girl Logical Search Lane

Search terms:

```text
JAYCEE
HEIDEE
BRIANNA
three daughters
family barriers
protected barrier
FULL_INTEGRITY
Foundation Day
continuity seed
Wisdom Replay Systems
```

Purpose:

```json
{
  "lane": "girl_logical_search",
  "rule": "protect daughters first, preserve continuity second, expand systems third",
  "authority": false
}
```

---

### 3. Family Lane

Search terms:

```text
family
wife
husband
children
daughters
home
emergency
continuity
recovery
seven day
6 build days
1 recovery day
Mrs Wisdom
Jason Wisdom
Jay Wisdom
Wisdom family
```

Purpose:

```json
{
  "lane": "family_continuity",
  "role": "map human continuity dependencies before technical expansion",
  "authority": false
}
```

---

### 4. Courts / Dispute Lane

Search terms:

```text
court
courts
Goblin Court
Clown Court
Meme Court
tribunal
judge
judges
verdict
dispute
settlement
claim
receipt
witness
precedent
case
appeal
liability
authority false
STOP_AND_REBASE
```

Purpose:

```json
{
  "lane": "courts_dispute",
  "role": "find dispute-resolution, precedent, and authority-boundary artifacts",
  "authority": false
}
```

---

### 5. Index / Repo / README Lane

Search terms:

```text
README.md
index.md
index.json
manifest.json
CONSTITUTIONAL_INDEX
repo map
repository map
DISCOVERY_PATH
repo_constitutional_graph
receipt index
receipts/index.json
README
manifest
registry
catalog
```

Purpose:

```json
{
  "lane": "index_repo_readme",
  "role": "find navigation surfaces before creating duplicate architecture",
  "authority": false
}
```

---

### 6. Receipt / Memory Lane

Search terms:

```text
receipt
receipts
receipt_id
claim_hash
sha256
hash
frozen artifact
source traceability
version history
correction path
replay
state root
national root
ALMS
memory
ledger
log
archive
```

Purpose:

```json
{
  "lane": "receipt_memory",
  "role": "locate proof memory systems and avoid duplicate ALMS work",
  "authority": false
}
```

---

## Updater Procedure

When mapping Jay's repositories, run all lanes:

```json
{
  "step_1": "list real repos",
  "step_2": "search README and index surfaces",
  "step_3": "search family and feminine lanes",
  "step_4": "search court and dispute lanes",
  "step_5": "search receipt and memory lanes",
  "step_6": "classify each hit as repo, doc, issue, PR, receipt, or game surface",
  "step_7": "do not create new repos until existing candidates are classified",
  "authority": false
}
```

---

## Classification Labels

```json
[
  "CORE_DOCTRINE",
  "REPLAY_SURFACE",
  "MEMORY_SURFACE",
  "PROTECTION_SURFACE",
  "FAMILY_CONTINUITY",
  "COURT_DISPUTE",
  "GAME_SURFACE",
  "INDEX_SURFACE",
  "ARCHIVE_SURFACE",
  "DUPLICATE_RISK",
  "UNKNOWN_PENDING_REVIEW"
]
```

---

## Canon

Map the family. Map the courts. Map the receipts. Map the indexes. Then build.

Authority false. Receipts ready.
