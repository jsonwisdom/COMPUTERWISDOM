# Maxwell's Demon — MN Borders v1
School of Wisdom / Computer Wisdom · 2026-11-14 · draft implementation
State: MANUAL_READ_ONLY_SANDBOX. No daemon, global rollout, network fetch, or payment authorization.

## Six enforced borders
1. Scope: US-MN-EDUCATION, no national/global expansion.
2. Input: manually supplied public records, classroom fixtures, lessons; reject private or restricted material.
3. Network/action: no fetching, crawling, time triggers, publishing, wallets, or payment writes.
4. Compute: at most 50 records/batch, 32768 bytes/record, zero recursion.
5. Evidence: URL + timestamp + supplied bytes + SHA-256; digest match proves only these supplied bytes match, not external authenticity or legal truth.
6. Governance: human review; no official authority or automated escalation.

Gate → Sort → Resolver → Packet. REJECT for boundary breaches, HOLD for missing records, CONFLICT for digest mismatch, BOUND_READ_ONLY for matching supplied bytes.

Run independently with Node 20+: node --test research/maxwell/borders/maxwell-gate.test.mjs
Tests are synthetic fixtures. No one should claim a production monitor, measured throughput, or real-world finding from their execution.

Thermodynamic border: count the system, measuring controller, memory, and environment. Landauer ideal erasure lower bound at 300 K ≈ 2.87e-21 joule/bit. This is a physical principle, not measured Worker energy usage.
Science: https://www.nature.com/articles/s42254-021-00400-8
History: Existing DeepSeek-Zora ingestion filter and Maxwell's Joystick Agenda remain unmodified.
Expansion requires independent security/legal review and explicit human authorization; it is a separate change.