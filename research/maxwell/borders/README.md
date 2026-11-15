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

## 2026-11-14 Air University / Shannon replay
Official Air University publication: José R. Davis, **Disinformation and Entropy: Leveraging AI in the Information Environment**, *Air & Space Operations Review* 3(2), Summer 2024, printed p.26.
Primary source: https://www.airuniversity.af.edu/Portals/10/ASOR/Journals/Volume-3_Number-2/Davis.pdf

The article prints H(P) = -Sum_i p(i) log2 p(i). A Maxwell Demon research gate must **permit Shannon information**. Entropy measures uncertainty of a declared distribution, not whether a source is truthful or dangerous. High Shannon entropy is NOT a reject reason.

Wolfram independent replay:
- H(fair binary source) = 1 bit.
- Binary symmetric error channel e=0.1: h2(e) = 0.4689955935892812 bits.
- With uniform input: mutual information I(X;Y)=1-h2(e)=0.5310044064107188 bits.
- Expected posterior uncertainty H(X|Y)=0.4689955935892812 bits, less than prior H(X)=1 bit.
- Binary entropy h2(p) is strictly concave for 0<p<1. An informative observation can reduce conditional entropy; adding information does not universally increase uncertainty.
- Shannon model statistics NEVER promote a source's authenticity, historical truth, government authority, or lawfulness.
- Landauer ideal erasure bound at 300 K is ~2.870978885e-21 joules per bit. It is not a measured operating energy budget.

Code: shannonBits() + shannonChannel() (pure educational functions). No network, global activation, or automatic source processing is authorized. Air University publication is a source document, not operational endorsement or affiliation.
