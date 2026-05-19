# Computer Wisdom Public Verifier Report · 2026-05-20

**Repository:** `jsonwisdom/COMPUTERWISDOM`  
**Visibility:** Public  
**Default branch:** `master`  
**Verifier:** Compute Wisdom public verifier  
**Status:** PASS_WITH_HELD_CANDIDATE_BOUNDARIES

---

## Public Links

- Repository: https://github.com/jsonwisdom/COMPUTERWISDOM
- Public site: https://jsonwisdom.github.io/COMPUTERWISDOM/portal.html
- Portal source: https://github.com/jsonwisdom/COMPUTERWISDOM/blob/master/portal.html

---

## Verified Public Surfaces

| Surface | File | Commit / Blob | Status |
|---|---|---|---|
| Public Portal | `portal.html` | blob `54e8a3702d182cdf2936031a6233336c86643632` | PUBLIC_SURFACE_UPDATED |
| L0-L5 Index | `services/layer-index/COMPUTE_WISDOM_L0_L5_INDEX.md` | commit `3ded4d0f27fbbe94a89557b4d6fa162e8ede753f` / blob `eecfd3052eef28aabb666524bbf7f4f7afa66064` | PUBLIC |
| L1 Reputation | `services/reputation-layer/REPUTATION_LAYER_L1_CANDIDATE.md` | commit `83b2fc21b77863b42e9f920f21552d392f67317a` / blob `fd59910d99c79b2a3002913c870372dd050821bd` | PUBLIC_CANDIDATE |
| L3 Batch Schema | `services/grok-batch-receipts/grok_batch_packet_schema_v1.json` | commit `836c958b2abdb71e2c5b9f967f14ca2bf7325c44` / blob `0bc34dfe792fc51751b84306271018563abf6fa8` | PUBLIC_CANDIDATE |
| L4 Byte Verification | `services/byte-verification/README.md` | commit `d132eb262c6dd59a2c71d61afec5d055dab18d7d` / blob `fe644dfb4d04873ae12b841eeae487d09608a8c5` | PUBLIC_CANDIDATE |

---

## Public Portal Verification

The public page exposes these proof paths:

- Compute Wisdom Layers
- L0-L5 Layer Index
- L1 Reputation Layer
- Weekly Byte Verification
- Grok Evidence
- Grok Batch Receipt Shortcuts
- Active Constraints
- Daily Civic Ledger

The portal remains bounded: it displays evidence paths and candidate infrastructure, not authority claims.

---

## Art of War 2026 Daily Epoch Verification

Verified public proof chain:

- 05-20 Final Court Lock: `receipts/daily/art_of_war_2026_daily_ledger_2026_05_20_final_court_lock_confirmation.json`
- Commit-Pinned Snapshot Review: `receipts/counters/grok_05_20_commit_pinned_snapshot_review_2026_05_19.json`
- Batch Packet: `receipts/batch/grok_batch_packet_art_of_war_2026_05_20_v1.json`
- 05-21 Candidate: `receipts/daily/art_of_war_2026_daily_ledger_2026_05_21_candidate.json`

---

## Boundary Verdict

```json
{
  "public_badge_granted": false,
  "onchain_claimed_live": false,
  "legal_authority_claimed": false,
  "military_authority_claimed": false,
  "official_government_claim": false,
  "external_affiliation_claimed": false,
  "zora_treated_as_proof": false
}
```

---

## Final Verifier Verdict

```json
{
  "verdict": "PASS_WITH_HELD_CANDIDATE_BOUNDARIES",
  "repo_public": true,
  "portal_public_surface_updated": true,
  "l0_l5_index_public": true,
  "l1_reputation_layer_public": true,
  "grok_evidence_public": true,
  "weekly_byte_verification_public": true,
  "final_05_20_epoch_commit_pinned": true,
  "public_badge_granted": false,
  "onchain_claimed_live": false,
  "authority_claimed": false
}
```

## Canon

Byte by byte.  
Receipt by receipt.  
Public link by public link.  
Compute Wisdom verifies the surface without inflating the claim.
