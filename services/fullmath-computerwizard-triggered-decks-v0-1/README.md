# FullMath ComputerWizard Batching Send — Triggered Decks V0.1

**Status: CANDIDATE / DESIGN_HOLD / PRODUCTION_HOLD.**
Operator declaration: **JAY APPROVED** for design preparation only. Final human decision **JASON** is **NOT_OBSERVED**.

This is a separate adult-run political football satire candidate and **not** frozen TriggerDeck canon. No family data, Heidee/JOY commercial use, publishing, orders, minting, wallet actions, or Base transactions are authorized.

Source contracts (read-only):
- [ComputerWizard control panel](../../../index.html): INPUT → CLASSIFY → TEST → COMPARE → GATE → EMIT → REPLAY.
- [Base Batches candidate purpose](../confucius-compute-wisdom/base_batches_purpose_candidate.md): group receipt hashes, form offline Merkle roots, require receipts before any onchain assertion.
- [TriggerDeck immutability notice](../../../TRIGGER_DECK_IMMUTABILITY_NOTICE.md): terminal anchor dcbd862c3501dfcd349aa878180fb13114c7d039, no direct lineage edits.
- [Base Has Purpose](../../../docs/base_has_purpose_v0_1.md): jaywisdom.base.eth is a discovery/receipt context, not wallet ownership or authority proof.

Offline candidate batching tool:
1. Only strict schema, JAY design-candidate lane, family_data=false, separate lineage.
2. Multiple-of-three distinct card IDs; explicit FICTION / SATIRE — NOT PREDICTIONS OR FACTS.
3. SHA256-bound local PNG files, checked file paths/symlinks, PNG CRC/decompression, exact 3:4 portrait.
4. Deterministic per-instance domain-separated SHA256 leaves, Merkle root, offline recomputation.
5. Report always production_status=HOLD, publication=false, onchain=false, sales=false, external_send=false, JASON final gate missing.
6. Max 9,000 local candidate instances/run (memory/fixture bound, not throughput proof).

Run: \`python3 -m unittest discover -s tests -v\`.

Create a new synthetic fixture directory: \`python3 tests/make_synthetic_fixture.py /tmp/cwtd-fixture\`.
Build: \`python3 batcher.py build --manifest /tmp/cwtd-fixture/manifest.json --root /tmp/cwtd-fixture --report /tmp/cwtd-fixture/candidate.json\`.
Verify: \`python3 batcher.py verify --manifest /tmp/cwtd-fixture/manifest.json --root /tmp/cwtd-fixture --report /tmp/cwtd-fixture/candidate.json\`.

**Local pre-submission run:** 24/24 unit checks passed and 3-card/9-instance synthetic end-to-end replay passed. This is **not independent GitHub CI**, human visual review, licensing review, onchain proof, benchmark, or production authorization.

### FullMath target distinction

- 1,000,000 instances/minute = 50,000/3 per second is an **unmeasured future goal**.
- 1,000,000 % 3 = 1, so 999,999 grouped instances + one unassigned carry is the strict three-divisibility bookkeeping case.
- 83% soft cap and 17% reserve are planning policies only; provider terms, meters, actual budgets and economics are unverified.
- Asset checks do not prove border/font/visual quality, legal rights, truth, authorization, consent, or real-world delivery.

The word SEND here means sending **this code/design to a draft review branch**, not cards/products to the public.

Merkle: leaf SHA256("CWTD-LEAF-V1\0" + sorted compact UTF-8 JSON); inner node SHA256("CWTD-NODE-V1\0" + left digest bytes + right digest bytes); duplicate last node on odd levels. This is a project-specific **candidate** and must not be presented as ReceiptOS/JCS equivalence.