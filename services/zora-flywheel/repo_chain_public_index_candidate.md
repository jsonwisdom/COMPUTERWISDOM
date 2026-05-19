# Repo Chain Public Index Candidate

Status: Candidate only, not live.
Operator: jaywisdom.base.eth
Purpose: double-back indexing map for Jay's public Fly/Zora/GitHub chain.
Portal mutation: none.
Public badge: none.
Backend claim: none.
Onchain claim: none.

## Confirmed Public Surfaces

### 1. Zora Profile

- Profile: `https://zora.co/@jaywisdom`
- Status: public pointer
- Use: cultural/artifact distribution surface
- Boundary: Zora profile is not a secret-scan proof by itself.

### 2. Zora Wallet

- Wallet: `0x829adfedbe565f9885a7ea6bc78912acaef055e2`
- Source: `jsonwisdom/jay-zora-portal` README
- Status: public indexing pointer
- Use: Zora drop indexing, metadata search, receipt linking
- Boundary: wallet pointer is public index data, not private key material.

### 3. Jay Zora Portal Repo

- Repo: `jsonwisdom/jay-zora-portal`
- Visibility: public
- Default branch: `live-zora-ingestion`
- README purpose: crawl Jay's Zora drops, store metadata and receipts, search by title/description/visual aliases/themes/contract/token ID/tx hash, render public portal.
- Boundary: repo is not currently treated as secret-scan PASS. It is an index target.

### 4. AL Repo

- Repo: `jsonwisdom/AL`
- Visibility: public
- Use: constitutional/replay discipline reference
- Boundary: AL contributes replay/discipline context. It does not automatically approve COMPUTERWISDOM artifacts.

### 5. COMPUTERWISDOM Repo

- Repo: `jsonwisdom/COMPUTERWISDOM`
- Visibility: public
- Use: audit, receipt, service, session, reward, Zora adapter, and manifest surface
- Boundary: candidate artifacts are not public badges.

## Double-Back Checks

Before any Zora image output or public index promotion:

1. Confirm repo path exists.
2. Confirm branch/ref exists.
3. Confirm public pointer is intentional.
4. Confirm no private secret appears in metadata.
5. Confirm secret scan status is PASS or reviewed WARN.
6. Confirm image mode is declared:
   - RANDOM_ZORA_ARTIFACT
   - PURPOSE_BOUND_ZORA_ARTIFACT
7. Confirm output is a pointer/reward, not proof itself.
8. Confirm portal.html remains untouched unless separately promoted.

## Indexing Schema

```json
{
  "index_id": "REPO_CHAIN_PUBLIC_INDEX_CANDIDATE_V1",
  "zora_profile": "https://zora.co/@jaywisdom",
  "zora_wallet": "0x829adfedbe565f9885a7ea6bc78912acaef055e2",
  "repos": [
    "jsonwisdom/jay-zora-portal",
    "jsonwisdom/AL",
    "jsonwisdom/COMPUTERWISDOM"
  ],
  "required_before_image_output": [
    "secret_scan_receipt",
    "repo_path_check",
    "public_pointer_check",
    "metadata_safety_check"
  ],
  "zora_image_lane_unlocked": false,
  "portal_html_mutated": false,
  "public_badge_granted": false
}
```

## Canon

Public pointers can index the chain.
They do not prove the chain.

Secret scan first.
Repo chain check second.
Zora image third.
Public claim last, if ever.
