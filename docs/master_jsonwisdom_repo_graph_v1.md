# MASTER_JSONWISDOM_REPO_GRAPH_V1

**Authority:** false  
**Purpose:** Master inventory of confirmed JSONWisdom repositories, roles, and pending audit lanes.

**Scan rule (2026-10-22):** Only the four confirmed core repositories are scanned. All other observed repositories are SCAN_EXCLUDED so they do not burn API or scan budget. Exclusion is not deletion and not a disposal finding.

---

## Confirmed Core Repos — CORE_SCAN

| Repo | Role | Status | Notes |
|---|---|---|---|
| `jsonwisdom/AL` | Doctrine / constitutional rules | CORE_SCAN | Authority:false doctrine layer. |
| `jsonwisdom/COMPUTERWISDOM` | Operational control plane / replay / UI / verification game | CORE_SCAN | Operational backbone, not canonical Anchor 001 proof source. |
| `jsonwisdom/JOY` | Protection UI / alert protocol | CORE_SCAN | Included in future maps and audits. |
| `jsonwisdom/Welcome-to-JSONWISDOM` | Entry / canon / Anchor 001 source | CORE_SCAN | Canonical Anchor 001 proof source. |

---

## SCAN_EXCLUDED — all other observed repositories

These are not scanned. They remain in the ledger. Purpose is not established by this exclusion.

```json
{
  "scan_core": ["AL", "COMPUTERWISDOM", "JOY", "Welcome-to-JSONWISDOM"],
  "scan_exclude": [
    "-jasonwisdom-data", "-replayos-receiptos-spec", "0", "ABS", "AU", "BRAELEE", "BREANN",
    "BRIGHTHOUSE", "CITIZEN_ROOT", "COMPUTERWIZARD", "DDR", "DESTINEE", "Direct-Mail", "ELMORE",
    "ENS", "EV-012-ZORA-MARKET-SNAPSHOT", "GAGA", "GENESIS", "GPKMONSTER", "GRAMMY", "GRANDADDY",
    "HEIDEE", "JAYCEE", "JSONWisdom-Control-Center", "Jason-USB-OFFICE-PC", "Jason-s-Private-Stash",
    "Jason-t-PL3X", "Jasons-1st-repository", "LEEANN", "Learning-GitHub", "MARYDEE", "MONTGOMERY",
    "NASTYNICK", "PAPA", "PRATTVILLE", "Plesk-Onyx-17.0.17", "RMT", "ReceiptOS", "Server", "UNCLED",
    "agentos", "base", "base-live", "boss-brenda-crawler", "computerwisdom-site", "crp-v0.1",
    "debate-judge-tee-v1", "desktop-tutorial", "fafo-briefings", "fastenal", "flywheel-of-wisdom",
    "global-zne-hybrid", "jason-parallel-drift-auditor", "jay-zora-portal", "jsonwisdom-packet-workbench",
    "layered-proofing-state-level-alms", "mint-engine-zero", "mn-ago-entropy-ledger", "nuke-launchpad",
    "prism-brush-spruce-lake", "project-c-note", "prooflayer-repo", "provenance-audit-kit", "public-proof",
    "receipt-arcade", "receiptos-base", "receiptos-replay-proof", "receipts-engine-v1", "replay-membrane",
    "replay-membrane-v0", "signal-multisig-zora", "snapback-mirror", "software", "sovereign-copilot",
    "system-risk-detector", "the-gap", "verifygate"
  ],
  "authority": false
}
```

Count: 4 core, 77 excluded, 81 observed. Claimed estate of 87 is still unresolved.

---

## Rule

Scan only CORE_SCAN repositories.

SCAN_EXCLUDED repositories are not scanned. They remain visible in the exclusion list.

No repo is promoted to canonical ALMS until audited.

Authority false. Receipts ready.
