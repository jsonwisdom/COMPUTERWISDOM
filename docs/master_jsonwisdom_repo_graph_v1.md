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
| `jsonwisdom/layered-proofing-state-level-alms` | State-level ALMS seed | PENDING_AUDIT | Do not treat as canonical ALMS until audited. |
| `jsonwisdom/receipts-engine-v1` | Receipt processing engine | PENDING_AUDIT | Inspect before migration. |
| `jsonwisdom/receipt-arcade` | Receipt/game mechanic surface | PENDING_AUDIT | Likely game layer, not memory layer. |

---

## Family / Feminine / Guardian Layer

| Node | Type | Status | Notes |
|---|---|---|---|
| Mrs Wisdom | Role | PLACEHOLDER | Emergency manager / continuity guardian. |
| Daughters / family continuity | Role | PLACEHOLDER | Protected barrier layer. |
| `jsonwisdom/JAYCEE` | Repo | CONFIRMED_VISIBLE | Needs audit. |
| `jsonwisdom/HEIDEE` | Repo | CONFIRMED_VISIBLE | Needs audit. |
| `jsonwisdom/LEEANN` | Repo | CONFIRMED_VISIBLE | Needs audit. |
| `jsonwisdom/MARYDEE` | Repo | CONFIRMED_VISIBLE | Needs audit. |
| `jsonwisdom/GAGA` | Repo | CONFIRMED_VISIBLE | Needs audit. |
| `jsonwisdom/GRAMMY` | Repo | CONFIRMED_VISIBLE | Needs audit. |

---

## Other Visible Repos Requiring Classification

```text
jsonwisdom/GPKMONSTER
jsonwisdom/BRIGHTHOUSE
jsonwisdom/UNCLED
jsonwisdom/0
jsonwisdom/ABS
jsonwisdom/AU
jsonwisdom/BRAELEE
jsonwisdom/BREANN
jsonwisdom/COMPUTERWIZARD
jsonwisdom/DESTINEE
jsonwisdom/ELMORE
jsonwisdom/GRANDADDY
```

Status: `UNKNOWN_PENDING_REVIEW` until audited.

---

## Dependency Model

```text
AL
├── doctrine → COMPUTERWISDOM
├── doctrine → JOY
└── doctrine → ALMS candidate repos

Welcome-to-JSONWISDOM
└── canonical Anchor 001 proof source → COMPUTERWISDOM references

COMPUTERWISDOM
├── operational control plane → replay/game/public demo
├── consumes → ALMS receipts once canonical memory repo is chosen
└── contextualizes → GitHub proof paths

JOY
└── protection UI / alert protocol → humans and family-safe surfaces

ALMS candidate repos
└── store → receipts, logs, schemas, frozen artifacts after audit
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
  "authority": false
}
```

---

## Rule

No repo is promoted to canonical ALMS until audited.

No family, feminine, court, or README/index surface may be skipped in repo discovery.

Authority false. Receipts ready.
