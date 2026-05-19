# Computer Wisdom · Manifest Index

**Purpose:** One map of every candidate, receipt, Merkle key, court ruling, service layer, and reward artifact.  
**Rule:** Update this file whenever a new artifact is promoted or committed.  
**Canon:** No more scattered receipts. Make the map. Then build from the map. 🧾🗺️

---

## Legend

| Tag | Meaning |
|-----|---------|
| `CANDIDATE` | Proposed, not live |
| `PROMOTED_CANDIDATE` | Approved as module, still not live |
| `PARTIAL` | Evidence incomplete |
| `VERIFIED_WITH_LIMITATION` | Verified while preserving disclosed evidence limitation |
| `PENDING_REVIEW` | Awaiting Jay decision |
| `PENDING_EXACT_CAPTURE` | Session staged with exact-capture discipline before model run |
| `MERKLED` | Anchored in Merkle receipt |
| `REWARD_ARTIFACT` | Visual/format reward generated after eligible verification |
| `REWARD_RECEIPT` | Receipt recording a reward artifact and its boundaries |
| `HOLD` | Deliberately paused |

---

## 1. Candidate Files (`/candidates/`)

| File | Status | Notes |
|------|--------|-------|
| `funding_portal_candidate.html` | `HOLD` | Sponsor pathway HELD. No donation rails. |
| `rd_access_policy_candidate.md` | `HOLD` | No citizenship claims. Immutability softened. |
| `badge_challenge_candidate.html` | `HOLD` | Machine-readable improvement. No attack on live badge. |
| `compute_wisdom_knowledge_proofs_candidate.md` | `PROMOTED_CANDIDATE` | Core proof layer. No badge without proof. |
| `power_proof_deep_seek_candidate.md` | `PROMOTED_CANDIDATE` | First training-session proof object. |
| `confucius_compute_wisdom_service_candidate.md` | `CANDIDATE` | Service spec. DeepSeek as analysis engine. |
| `confucius_compute_wisdom_widget_candidate.html` | `CANDIDATE` | Public mockup. No backend. |

---

## 2. Receipts (`/receipts/` and `/receipts/merkle/`)

| Receipt | Status | Commit / Hash |
|---------|--------|----------------|
| `power_proof_deep_seek_promotion_receipt_v1.json` | `PROMOTED_CANDIDATE` | `b15158a1` |
| `deep_seek_session_001_receipt.json` | `EVIDENCE_CHAIN_REPAIRED` | `e2dd1b2` |
| `deep_seek_session_001_prompt_normalized.txt` | `ACCEPTED_WITH_LIMITATION` | `814a1d0` |
| `deep_seek_session_001_output.md` | `FULLY_ACCEPTED` | `29cd633` |
| `deep_seek_session_001_court_ruling.json` | `REQUEST_ALTERNATIVE_EVIDENCE` | `6ce06f5` |
| `deep_seek_session_001_verdict.json` | `VERIFIED_WITH_LIMITATION` | `c54d85a` |
| `confucius_deep_seek_session_001_reward_artifact_receipt.json` | `REWARD_RECEIPT` | `2b77059` |
| `deep_seek_session_002_prompt_exact.txt` | `PENDING_EXACT_CAPTURE` | `99e3d7b` |
| `deep_seek_session_002_output_exact.md` | `PENDING_CAPTURE` | `3c790d3` |
| `deep_seek_session_002_receipt.json` | `PENDING_EXACT_CAPTURE` | `3b7f079` |
| `merkle/confucius_compute_wisdom_merkle_purpose_key_v1.json` | `MERKLED` | `d0abe0a` |
| `merkle/base_batches_confucius_purpose_extension_v1.json` | `PURPOSE_EXTENSION_CREATED` | `edcd365` |
| `court_reporter/tweet_2056596286099402905_alignment_report.json` | `ANALYSIS_COMPLETE` | `c79cc42` |

---

## 3. Service Layers (`/services/`)

| Service | Path | Status |
|---------|------|--------|
| Confucius Compute Wisdom | `services/confucius-compute-wisdom/README.md` | `CANDIDATE` |
| Confucius Visual Reward Spec | `services/confucius-compute-wisdom/visual_reward_spec.md` | `CANDIDATE_ONLY` |
| Base Batches Purpose Rail | `services/confucius-compute-wisdom/base_batches_purpose_candidate.md` | `CANDIDATE_ONLY` |
| Constitutional Substrate / AL Reference | `services/constitutional-substrate/al_repo_machine_speed_productivity_candidate.md` | `CANDIDATE_ONLY` |

---

## 4. Reward Artifacts (`/assets/rewards/`)

| Artifact | Status | Commit | Notes |
|----------|--------|--------|-------|
| `confucius_deep_seek_session_001_reward.svg` | `REWARD_ARTIFACT` | `5b72569` | SVG receipt-card poster. Celebrates `VERIFIED_WITH_LIMITATION`; badge still denied; portal untouched. |

---

## 5. Court Rulings

| Ruling | Date (UTC) | Outcome |
|--------|------------|---------|
| Power Proof Deep Seek promotion | 2026-05-18 | `PROMOTED_AS_CANDIDATE_MODULE` |
| Deep Seek Session 001 review | 2026-05-18 | `REQUEST_CHANGES` to `PARTIAL_PASS` |
| Deep Seek Session 001 court ruling | 2026-05-18 | `REQUEST_ALTERNATIVE_EVIDENCE` |
| Deep Seek Session 001 final verdict | 2026-05-19 | `VERIFIED_WITH_LIMITATION` |
| Widget placement and Merkle key | 2026-05-19 | `MERKLED` |
| Tweet alignment analysis | 2026-05-19 | `PUBLIC_STATEMENT_ALIGNS_WITH_CANDIDATE_WORK` |
| Reward SVG creation | 2026-05-19 | `REWARD_ARTIFACT_CREATED` |
| Reward artifact receipt | 2026-05-19 | `REWARD_RECEIPT_CREATED` |
| Session 002 starter files | 2026-05-19 | `PENDING_EXACT_CAPTURE` |

---

## 6. Protected Surface

| File | Status |
|------|--------|
| `portal.html` | **NOT MUTATED** — protected surface |

---

## 7. Current Lock State

```json
{
  "status": "SESSION_002_EXACT_CAPTURE_STARTER_FILES_CREATED",
  "latest_session": "DEEP_SEEK_SESSION_002",
  "session_002_topic": "Compute Wisdom Claim Parser Badge — KP-001 candidate design",
  "session_002_prompt_commit": "99e3d7b6a6bb83bd02f47d330aff4f26c580aedc",
  "session_002_output_placeholder_commit": "3c790d3318862a7a4b1dc4420acd0ca055a7207f",
  "session_002_receipt_template_commit": "3b7f07946e30ee37c06aecbd57184eb034493764",
  "portal_html_mutated": false,
  "public_badge_granted": false,
  "backend_claimed_live": false,
  "onchain_claimed_live": false,
  "image_generation_unlocked": true
}
```

---

## 8. Next Actions From the Map

- Jay runs the exact prompt from `receipts/deep_seek_session_002_prompt_exact.txt` through DeepSeek or an alternative model.
- Paste the exact output into `receipts/deep_seek_session_002_output_exact.md`.
- Hash prompt and output.
- Update `receipts/deep_seek_session_002_receipt.json` with hashes and timestamp.
- Submit Session 002 for review.
- Candidate badge design may begin, but no public badge is granted.
- `portal.html` remains untouched unless explicitly promoted by separate receipt.
- Update this manifest with every new artifact.

---

## Canon Lock Phrase

No more scattered receipts.  
Make the map.  
Then build from the map.  
Portal untouched.  
Badge waits for proof.  
Merkle roots the memory. 🧾🗺️

---

## Verdict Lock Phrase

Verified with limitation.  
Truth preserved.  
Image unlocked.  
Badge still denied.  
Portal untouched.  
Build continues.

---

## Reward Lock Phrase

Image created.  
Badge still denied.  
Portal untouched.  
Receipt records the reward.  
The image celebrates proof; it does not replace proof.

---

## Session 002 Lock Phrase

Session 001 proved the chain.  
Session 002 perfects the capture.  
Exact prompt first. Output second. Hash third. Receipt fourth. Review fifth.  
Claim Parser badge remains candidate until verified.  
Build from the map.

---

## Manifest Boundary

A manifest is not a badge.  
Indexing is not promotion.  
Verification with limitation is not a live backend claim.  
A reward image is not a badge.  
A receipt for the reward is not a public credential claim.  
A starter file is not a verified session.  
The gate still holds.  
Build from the map.
