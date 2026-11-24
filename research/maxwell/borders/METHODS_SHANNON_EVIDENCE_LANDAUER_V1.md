# Maxwell's Demon: Four-Layer Methods Note v1
**School of Wisdom / Computer Wisdom | 2026-11-14**
**Scope:** Minnesota educational research sandbox only. This is a methods note, not operational Air University affiliation, a deployment, or legal authority.

## 1. Shannon entropy: quantify uncertainty
For a declared discrete probability distribution P, with sum(p_i)=1 and the convention 0 log2(0)=0:

H(X) = -sum_i p_i log2(p_i) [bits].

For a fair binary variable P=(1/2,1/2), H(X)=1 bit. For deterministic P=(1,0), H(X)=0 bits. High entropy means a less predictable variable under the declared probability model; it does NOT mean false information, misinformation, fraud, or unacceptable evidence.

## 2. Mutual information: quantify reduction of uncertainty
I(X;Y) = H(X) - H(X|Y) = H(Y) - H(Y|X) [bits].

For a *hypothetical* binary symmetric channel with uniform input X, independent crossover error e=0.1, and Y received:

H(X)=1 bit.
h2(e) = -0.1 log2(0.1)-0.9 log2(0.9) = 0.4689955935892812 bits.
H(X|Y)=h2(e)=0.4689955935892812 bits.
I(X;Y)=1-h2(e)=0.5310044064107188 bits.

These are Wolfram-replayed mathematical results under stated assumptions. They are not measured channel performance, measured research speed, or proof that Y is accurate in a real system. Conditional uncertainty decreases *in expectation* for informative observations.

## 3. Provenance and evidence: evaluate what a claim establishes
A source receipt should preserve source URI, retrieval/observation time, complete relevant content bytes, SHA-256 digest, document identity/version, issuer/custodian, retrieval method, and review limitations. An independent reviewer should retrieve the original source when possible and test relevant contextual and contradictory evidence.

SHA-256 agreement establishes input-byte consistency **relative to supplied bytes**, NOT independent source authenticity, a complete chain of custody, truth, legal authority, causation, or guilt. A source may have high entropy and still be authentic. A low-entropy source may be false. Never use Shannon entropy, mutual information, or a cryptographic digest as a veracity classifier.

Status gates:
- REJECT: explicit scope or information safety boundary crossed.
- HOLD: required source fields or independent source confirmation missing.
- CONFLICT: supplied evidence contradicts the expected digest or another authenticated, proposition-relevant record.
- BOUND_READ_ONLY: supplied byte content matches its supplied digest; external authenticity and truth remain unresolved until independently assessed.

Human review is required for promotion of real-world factual/legal claims. No automatic accusations, publication, payments, on-chain writes, or authority.

## 4. Landauer's principle: account for physical cost
In an ideal thermodynamic model, resetting one bit of memory at temperature T has a minimal dissipated heat scale:

Q_min = k_B T ln(2).

At 300 kelvin, using k_B=1.380649e-23 J/K:
Q_min ≈ 2.870978885e-21 joules per erased bit.

This is a theoretical lower bound for logically irreversible bit erasure under the model. It is not a benchmark of actual device, model-training, Wolfram, Cloudflare, or Air University energy consumption. Maxwell's demon does not exempt information acquisition, memory, reset, controller, and surroundings from thermodynamic accounting.

## Boundaries between all four layers
- H(X) is not a truth score.
- I(X;Y) is not an authenticity score.
- A digest is not a court finding.
- A thermodynamic lower bound is not an operational electricity bill.
- A verified mathematical identity is not a claim that an Air University system has implemented it.

## Reference
Capt. José R. Davis, USAF, "Disinformation and Entropy: Leveraging AI in the Information Environment," *Air & Space Operations Review*, vol. 3, no. 2 (Summer 2024), pp. 15-29. Air University PDF: https://www.airuniversity.af.edu/Portals/10/ASOR/Journals/Volume-3_Number-2/Davis.pdf

Mathematical implementation in this PR: shannonBits() and shannonChannel() in maxwell-gate.mjs, with synthetic fixture tests. This note is descriptive, not evidence of passing CI or production deployment.
