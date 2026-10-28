# BUILDER_CONTRACT_V2.md
# Classes With Glasses — Append-Only Builder v2
# Delta relative to conversational Builder v1 only.
# AUTHORITY_CREATED = false

## Scope of this version
This contract records only additions and changes. It does not rewrite v1 history.

## Predecessor status
PREDECESSOR_UNVERIFIED
No verified v1 package bytes or SHA-256 recovered.
No manufactured predecessor hash.

## New / changed requirements (v2)
1. Explicit numbered receipt linkage required (CWG-BUILDER-NNNN).
2. Predecessor field must be either a verified receipt_id + content SHA-256 or the literal string PREDECESSOR_UNVERIFIED.
3. Public classroom surfaces (Classes With Glasses) are reference material only; they do not constitute the Builder package.
4. AL Lineage and Receipt Vault Semantics V2 are separately attributed prior art and must be cited as such, never absorbed.
5. Local hash-chain test must be reproducible from the exact bytes of the receipt being appended.
6. Supreme Seymour V1–V4 replay must be executed and recorded; output may be HOLD.
7. Production, website deployment, payments, advertising, auto-trading, and wallet signing remain FALSE until separate human-authorized verification.

## Unchanged invariants (carried forward)
- APPEND_ONLY = TRUE
- Never overwrite original evidence
- Store source content by SHA-256
- Append corrections; link new receipts
- PRIVATE_COINBASE_DATA_PUBLICATION = FALSE
- Independent blockchain receipts required before any on-chain PASS
- Classroom results separated from trading / wallet / publishing authority
- HUMAN_APPROVAL_REQUIRED = TRUE
- CLAIM ≠ PROOF · NO RECEIPT → HOLD

## Acceptance for local V2 PASS
- Verified package bytes present, OR explicit PREDECESSOR_UNVERIFIED recorded
- Valid append-only receipt with content digests
- Reproducible local hash-chain + schema checks
- Supreme Seymour replay executed (result may be HOLD)

Production remains HOLD.

## Linked receipt
CWG-BUILDER-0002 — disposition HOLD — no deployment, no promotion.
