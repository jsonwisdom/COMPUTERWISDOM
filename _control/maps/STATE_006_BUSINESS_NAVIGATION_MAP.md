# STATE_006_BUSINESS_NAVIGATION_MAP

Status: DRAFT_MAP_FROM_RECOVERED_ARCHIVE  
Rule: No deletion. No rename. No movement until public/evidence role is confirmed.

## 1. Public Front Door

| Path | Role | Status |
|---|---|---|
| README.md | Repo introduction | REVIEW |
| index.html | Public website entry | REVIEW |
| index 4.html | Alternate website entry | REVIEW |
| proposal.en.md | English proposal | BUSINESS_CORE |
| proposal.cn.md | Chinese proposal | BUSINESS_CORE |
| sovereign_os_proposal.pdf | Institutional proposal | BUSINESS_CORE |
| CW Messenger Contact.pdf | Contact/business artifact | BUSINESS_CORE |

## 2. Evidence Spine

| Path | Role | Status |
|---|---|---|
| receipts/ | Receipt records | PRESERVE |
| receipts/anchor/ | Anchor receipts | PRESERVE |
| receipts/continuity/ | Continuity receipts | PRESERVE |
| attestation/ | Attestation scripts | PRESERVE |
| test-vectors/ | Verification inputs | PRESERVE |
| FINAL_ANCHOR_TOPOLOGY_v1.md | Anchor topology | PRESERVE |
| SECURITY_BOUNDARY.md | Security boundary | PRESERVE |

## 3. Doctrine / Specs

| Path | Role | Status |
|---|---|---|
| docs/ | Main documentation | REVIEW |
| docs/EXECUTION_CONTINUITY_MODEL_V1.md | Continuity model | CORE |
| docs/REPLAY_RECEIPT_SPEC_V1.md | Replay receipt spec | CORE |
| docs/REPUTATION_CONTINUITY_SPEC_V1.md | Reputation continuity | CORE |
| docs/SOVEREIGN_OS_SPEC_V1.md | Sovereign OS spec | CORE |
| docs/COMPUTER_WISDOM_MICROSOFT_BRIEF_V1.md | Microsoft brief | BUSINESS_CORE |

## 4. Subprojects

| Path | Role | Status |
|---|---|---|
| angie-act/ | ACT/schema/tests project | MODULE |
| scaling-solutions/ | OS/signing/anchor code | MODULE |
| snapback/ | Recovery/autopush system | MODULE |
| snapback-mirror/ | Mirror/recovery artifact | NEEDS_PATH_REVIEW |
| royal-design-chess/ | Strategy/design system | MODULE |
| Trigger_Deck/ | Trigger deck cards/artifacts | MODULE |
| ztws/ | Zero Trust Wisdom/System layer | MODULE |
| wave-1/ | Reviewer/outreach layer | BUSINESS_OUTREACH |

## 5. Media / Cards

| Path | Role | Status |
|---|---|---|
| cards/ | Lowercase card asset folder | DUPLICATE_CANDIDATE |
| Cards/ | Uppercase card asset folder | DUPLICATE_CANDIDATE |
| root PNG files | Public/card assets | DUPLICATE_CANDIDATE |
| Trigger_Deck/*.PNG | Trigger Deck primary images | PRESERVE |

## 6. Cleanup Candidates — HOLD

| Path | Issue | Action |
|---|---|---|
| duplicated PNGs | byte-identical across root/cards/Cards | HOLD |
| empty files | detected by SHA256 empty hash | HOLD |
| snapback-mirror weird tree path | likely pasted-tree artifact | HOLD |

## Next Action

Build a local navigation page that links to public docs, evidence spine, subprojects, and recovery receipts without moving existing files.
