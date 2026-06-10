# Confucius Compute Wisdom Visual Reward Spec

Status: Candidate only.
Operator: jaywisdom.base.eth
Service: Confucius Compute Wisdom
Purpose key: receipts/merkle/confucius_compute_wisdom_merkle_purpose_key_v1.json
Portal mutation: none.
Public badge: none.

## Purpose

When a Confucius Compute Wisdom session becomes verified, the service may produce a visual reward artifact.

The image is not the proof.
The image is a readable celebration of the proof.

## Verification Gate

No visual reward may be labeled VERIFIED unless a review receipt exists with:

- evidence_complete: true
- verification_status: VERIFIED
- public_claims_checked: true
- portal_html_mutated: false
- badge_grant_explicitly_approved: true or false
- merkle_root_or_receipt_hash present

## Output Format

The preferred visual output is a receipt-card image or poster that includes:

- service name
- session ID
- verified status
- Merkle root or receipt hash
- purpose statement
- claim tag
- no-backend or backend status, if relevant
- badge status
- short canon line

## Style Direction

Visual tone: cybernetic courtroom, wisdom terminal, public receipt card, warm gold paper, black monospace, cryptographic seal, Merkle branch motif.

Suggested headline:

Confucius Compute Wisdom
Slap in code. Get Wisdom back.

Suggested lock phrase:

Proof first. Image second. Badge last.

## Safety and Claim Guardrails

- Do not imply legal certification.
- Do not imply security audit certification.
- Do not imply backend exists unless backend receipt exists.
- Do not imply public badge exists unless badge receipt exists.
- Do not call GitHub commit history on-chain.

## Canon

Once verified, create the image.
Until verified, create only the image spec.
