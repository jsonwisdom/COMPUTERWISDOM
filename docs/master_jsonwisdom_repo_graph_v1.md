# MASTER_JSONWISDOM_REPO_GRAPH_V1

**Authority:** false  
**Purpose:** Master inventory of confirmed JSONWisdom repositories, roles, and pending audit lanes.

---

## Confirmed Core Repos

| Repo | Role | Status | Notes |
|---|---|---|---|
| `jsonwisdom/AL` | Doctrine / constitutional rules | CONFIRMED | Authority:false doctrine layer. |
| `jsonwisdom/COMPUTERWISDOM` | Operational control plane / replay / UI / verification game | CONFIRMED | README identifies this repo as operational backbone, not canonical Anchor 001 proof source. |
| `jsonwisdom/JOY` | Protection UI / alert protocol | CONFIRMED | Must be included in future maps and audits. |
| `jsonwisdom/Welcome-to-JSONWISDOM` | Entry / canon / Anchor 001 source | CONFIRMED | COMPUTERWISDOM README names this as canonical Anchor 001 proof source. |

---

## ALMS / Receipt Candidates

| Repo | Candidate Role | Status | Rule |
|---|---|---|---|
| `jsonwisdom/receipts-engine-v1` | Visible receipt engine candidate | VISIBLE_RECEIPT_ENGINE_PENDING_AUDIT | Inspect before migration or canonical promotion. |
| `jsonwisdom/receipt-arcade` | Receipt/game mechanic surface | PENDING_AUDIT | Likely game layer, not memory layer. |
| `jsonwisdom/layered-proofing-state-level-alms` | State-level ALMS seed | PARKED_UNTIL_UI_CONFIRMED | Do not treat as active/canonical until Jay confirms it is visible/openable in GitHub UI. |

---

## Family / Feminine / Guardian Layer

| Node | Type | Status | Notes |
|---|---|---|---|
| Mrs Wisdom | Role | ROLE_PLACEHOLDER_NOT_CONFIRMED | Emergency manager / continuity guardian. No dedicated repo confirmed. |
| Daughters / family continuity | Role | CONTINUITY_ROLE | Protected barrier layer. |
| `jsonwisdom/JAYCEE` | Repo | CONFIRMED_REPO_PENDING_AUDIT | Real repo. Audit next. |
| `jsonwisdom/HEIDEE` | Repo | CONFIRMED_REPO_PENDING_AUDIT | Real repo. Needs audit. |
| `jsonwisdom/LEEANN` | Repo | CONFIRMED_REPO_PENDING_AUDIT | Real repo. Needs audit. |
| `jsonwisdom/MARYDEE` | Repo | CONFIRMED_REPO_PENDING_AUDIT | Real repo. Needs audit. |
| `jsonwisdom/BRAELEE` | Repo | CONFIRMED_REPO_PENDING_AUDIT | Real repo. Needs audit. |
| `jsonwisdom/BREANN` | Repo | CONFIRMED_REPO_PENDING_AUDIT | Real repo. Needs audit. |
| `jsonwisdom/GAGA` | Repo | CONFIRMED_REPO_PENDING_AUDIT | Real repo. Needs audit. |
| `jsonwisdom/GRAMMY` | Repo | CONFIRMED_REPO_PENDING_AUDIT | Real repo. Needs audit. |

---

## Other Visible Repos Requiring Classification

```text
jsonwisdom/GPKMONSTER
jsonwisdom/0
jsonwisdom/COMPUTERWIZARD
jsonwisdom/DESTINEE
jsonwisdom/software
```

Status: `UNKNOWN_PENDING_REVIEW` until audited.

---

## Empty — SCAN_EXCLUDED (2026-10-22)

Observed empty: no commits (HTTP 409) and zero branches. Removed from future scan lanes so they do not burn API/scan budget. Not deleted. Not a disposal finding. Purpose still unknown.

```text
jsonwisdom/UNCLED
jsonwisdom/global-zne-hybrid
jsonwisdom/PRATTVILLE
jsonwisdom/Jason-USB-OFFICE-PC
jsonwisdom/ABS
jsonwisdom/AU
jsonwisdom/GRANDADDY
jsonwisdom/BRIGHTHOUSE
jsonwisdom/mint-engine-zero
jsonwisdom/ELMORE
jsonwisdom/NASTYNICK
jsonwisdom/MONTGOMERY
jsonwisdom/PAPA
```

Status: `SCAN_EXCLUDED` / `EMPTY_REPOSITORY`.

---

## Dependency Model

```text
AL
├── doctrine → COMPUTERWISDOM
├── doctrine → JOY
└── doctrine → ALMS candidate repos after audit

Welcome-to-JSONWISDOM
└── canonical Anchor 001 proof source → COMPUTERWISDOM references

COMPUTERWISDOM
├── operational control plane → replay/game/public demo
├── consumes → ALMS receipts once canonical memory repo is chosen
└── contextualizes → GitHub proof paths

JOY
└── protection UI / alert protocol → humans and family-safe surfaces

Family repos
└── continuity surfaces → audit before assigning operational role

ALMS candidate repos
└── store → receipts, logs, schemas, frozen artifacts only after audit
```

---

## Search Lanes Required For Future Audits

```json
{
  "lanes": [
    "feminine_guardian",
    "girl_logical_search",
    "family_continuity",
    "courts_dispute",
    "index_repo_readme",
    "receipt_memory"
  ],
  "authority": false,
  "scan_exclude": [
    "UNCLED",
    "global-zne-hybrid",
    "PRATTVILLE",
    "Jason-USB-OFFICE-PC",
    "ABS",
    "AU",
    "GRANDADDY",
    "BRIGHTHOUSE",
    "mint-engine-zero",
    "ELMORE",
    "NASTYNICK",
    "MONTGOMERY",
    "PAPA"
  ]
}
```

---

## Rule

No repo is promoted to canonical ALMS until audited.

No family, feminine, court, or README/index surface may be skipped in repo discovery.

SCAN_EXCLUDED empty repositories are not scanned. They remain visible in the exclusion list.

Mrs Wisdom remains a role placeholder unless and until a dedicated repo is found or created.

Authority false. Receipts ready.
