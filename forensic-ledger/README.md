# COMPUTER WISDOM · CI-FIRST Financial Forensics (public code, no private evidence)

**Status:** candidate development; **authority:** false; **reconciliation:** OPEN; **publication of personal evidence:** prohibited.

The private evidence index is kept in access-controlled Google Drive. Do not copy Gmail messages, private account data, wallet recovery material, bank information, personally identifying transaction trails, or secret-bearing URLs to this public GitHub repository, pull requests, workflow logs, or issue comments.

## What the validator establishes
- Each record has a source reference, dated observation, reported event type, provider, asset and a decimal amount (not floats).
- Separate states are kept separate: requested ≠ approved ≠ confirmed; email receipt ≠ chain settlement; old balance snapshot ≠ present balance.
- Multiple notices for one provider order/event/asset are flagged as possible duplicates, not summed.
- Sensitive direct credential fields and unsourced current-balance assertions are rejected.
- Output contains explicit `portfolio_total: null`, `asset_recovered: null`, `loss_inferred: false`, `signing_authority: false`, and `reconciliation_complete: false`.

**Limit:** A passing schema check does not authenticate the originating email, prove wallet ownership, guarantee record completeness, or classify a transfer as fraud. Source hashes and metadata must be verified separately. There is intentionally no portfolio-total calculation.

## Event schema v0.1
Each row is a JSON object with required strings: `event_id`, `date_utc`, `provider`, `asset`, `event_type`, `state`, `amount`, `source_ref`.
- `event_type`: `purchase`, `deposit`, `withdrawal`, `transfer`, `balance_snapshot`, `claim`, `dispute`
- `state`: `reported`, `requested`, `approved`, `confirmed`, `unknown`
- `amount`: nonnegative finite decimal encoded as string, denominated in `asset`
- Optional: `provider_order_ref`, `source_sha256` (64 lowercase hex)
- `source_ref` in this public software's test data must be **synthetic only**. Do not place real Gmail IDs or personal financial identifiers in public fixtures.

## Run (synthetic examples only)
```bash
python -m unittest discover -s forensic-ledger -p 'test_*.py' -v
python forensic-ledger/validator.py /path/to/SYNTHETIC-events.json
```

## Evidence separation and promotion gates
- **PRIVATE:** Google Drive and connected Gmail: raw records, originals, header provenance, account IDs, full addresses, transaction links, protected timeline.
- **PUBLIC:** code, rules, blank schema, synthetic tests, de-identified aggregate QA methodology (not amounts or identifying traces).
- **PASS arithmetic:** numeric operations on explicitly defined, like-for-like inputs.
- **HOLD chain reconciliation:** no original immutable confirmation, owner linkage, destination provenance, full pagination and account coverage, or exact event deduplication.
- **NO MERGE OR DEPLOY:** Draft PR and code checks do not authorize changes to `master`, financial activity, public evidence release, or wallet operations.

Existing related repository control: `audits/COINBASE_HISTORY_MEMBRANE_AUDIT_V0_1.md` (private Drive source data, public control plane, no fake green).
