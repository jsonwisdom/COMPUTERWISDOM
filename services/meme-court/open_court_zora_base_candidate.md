# Meme Court · Open Court to Zora + Base Candidate

Status: Candidate only, not live.
Operator: jaywisdom.base.eth
Source audit: `audits/meme_court_zora_base_repo_audit_2026_05_19.md`
Portal mutation: none.
Public badge: none.
Backend claim: none.
Onchain claim: none.
Official authority claim: none.

## Purpose

Open Meme Court as a candidate workflow that can route reviewed artifacts toward Zora cards and Base public pointers.

The court is cultural, evidentiary, and receipt-bound.

It is not a legal court, government office, public agency, or official enforcement body.

## Court Path

```text
Daily Drop -> Meme Court Case -> Claim Tags -> Verdict -> Receipt -> Zora Card Candidate -> Base Pointer Candidate -> Public Review
```

## Allowed Moves

- Create Meme Court cases from Jay Wisdom daily drops.
- Attach claim tags: PUBLIC / HELD / PENDING / REJECTED.
- Link AL court artifacts.
- Link COMPUTERWISDOM receipts.
- Create Zora card candidates after receipt review.
- Create Base pointer candidates after receipt review.

## Forbidden Moves

- No fake verified labels.
- No official authority claims.
- No legal-judgment claims.
- No public badge grants by implication.
- No portal mutation by audit alone.
- No Zora card as proof by itself.
- No Base pointer as proof by itself.

## Gate Requirements

Before a Zora card or Base pointer can leave candidate state:

1. Case exists.
2. Verdict exists.
3. Receipt exists.
4. Secret scan is PASS or reviewed WARN.
5. Repo-chain check is complete.
6. Public wording avoids fake authority.
7. Jay approval receipt exists.

## Output Schema

```json
{
  "court_opening_id": "MEME_COURT_ZORA_BASE_OPEN_COURT_V1",
  "status": "CANDIDATE_OPEN",
  "source_audit": "audits/meme_court_zora_base_repo_audit_2026_05_19.md",
  "daily_drop": "PENDING",
  "meme_court_case": "PENDING",
  "zora_card_candidate": "PENDING",
  "base_pointer_candidate": "PENDING",
  "public_badge_granted": false,
  "portal_html_mutated": false,
  "official_authority_claim": false
}
```

## Canon

Meme Court opens as candidate.
Zora distributes cards.
Base points to evidence.
Computer Wisdom records receipts.
AL preserves court memory.

Open court does not mean open authority.
Receipts decide what leaves the floor.
