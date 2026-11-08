# CI-FIRST | Flywheel of Trinity: Motion → Media → Attestation
**Candidate thesis v0.1 — 2026-11-08 | REVIEW ONLY | No production authority**

> **Scientific hypothesis:** Voluntary, consent-based movement traces can provide a useful *secondary behavioral signal* when measurements are calibrated, reproducible, accompanied by device provenance and independent human review. A dance pattern alone is not a passport, legal identity, proof of guilt, or cryptographic key.

## Audit first; accountabilities end to end

**A. Music (public-safe)**. Maintain separately sourced track metadata, 128 BPM *mix target*, 468.75 ms reference beat and provenance of recordings. Rhythm does not identify the dancer. Existing upstream draft: [Music Librarians PR #750](https://github.com/jsonwisdom/COMPUTERWISDOM/pull/750). Six feeling shelves are user interpretations, never inferred psychological diagnoses.

**B. Movies + Photos (source-limited).** Preserve original authorized files in a *private, access-controlled* capture folder; record exact byte length, SHA-256, capture/receipt timestamp, consent/rights scope, original vs edit provenance, and any transcription/caption version. Do not crawl people, publish identifiable biometric videos, use alleged victim footage, extract sensitive content without lawful grounds, or classify anyone as a suspect by movement. Derived previews get independent SHA-256 and explicit labels SATIRE | EDUCATION | VERIFIED_SOURCE | UNVERIFIED. Human approval to release.

**C. Measured dance (voluntary, research-only).** Define a coordinate system and units; capture paired (timestamp, calibrated 2D/3D body-point) observations for consented adult participants, not indiscriminate recording. Distinguish center-of-mass displacement velocity from path speed, step cadence, limb angular rate, and tempo synchronization. Quantify uncertainty from lens calibration, occlusion, FPS, tracking errors, surface, footwear, mobility and capture conditions. Voluntary self-identified groups are not proof of legal identity. Never require dancing as a condition of public services or border access; provide accessible alternatives. Treat any claimed identity recognition as UNKNOWN until external calibration + fairness/privacy evaluation; never auto-reject people or allege wrongdoing.

**D. Private Windows PC sync.** Proposed only, NOT ACTIVE. Stage locally after consent, preserve original bytes, derive a local manifest with hashes and permitted handling, encrypt end-to-end with authenticated recipient keys, transmit over an authenticated channel, independently rehash on the receiving side and compare a fresh challenge receipt. No automatic synchronization without a verified destination, client enrollment, exclusive local file permissions, encrypted-at-rest destination and revocation. This repo contains only synthetic trace data; no real media or biometric templates.

**E. TPM 2.0 quote.** The user's Windows TPM probe reported AMD TPM open successfully, with one PCR bank; it explicitly reported \`signed_quote_verified=false\`. Existing separate [attestor PR #749](https://github.com/jsonwisdom/COMPUTERWISDOM/pull/749) supports a nonce challenge and quote candidate, but independent EK↔AK manufacturer trust, registered baseline PCR policy and a nonreplayed hardware-bound quote have NOT been demonstrated. Do not create an attestation key, change firmware, clear TPM, touch BitLocker keys or reconfigure YubiKeys without separately informed approval.

**F. Public proof receipts.** Publish only limited, consent-appropriate *non-reversible metadata* and independently verified digest/receipt references, not motion vectors, face/voice embeddings, raw clips, endorsement keys or a traceable lifelong identifier. A SHA-256 digest is byte integrity evidence, not proof of authorship, safe capture, legality, or identity. Separate publication root from private raw evidence root. On ENS/BNS, publish nothing that could link an identifiable movement template to an immutable public identity.

**G. Named domains are not deployed:** Connected Cloudflare readback on 2026-11-08 showed \`jsonwisdom.com\` active but no individual DNS records, wildcard records, matching Worker-domain mappings or wildcard Worker routes for \`music.jsonwisdom.com\`, \`movies.jsonwisdom.com\`, \`live.jsonwisdom.com\`. A Worker called \`wisdom-live-observer\` exists, has D1, service and secret-text bindings, and a deployment history, but is NOT shown as mapped to any of the three hostnames. No DNS or Worker change authorized by this draft.

**H. ENS → BNS → DNS are separate identity rails.** Historical user Drive spec \`ReplayJay — ENS Before DNS\` explicitly distinguishes the public names from wallet signing control. Blockscout read-only resolution for \`jaywisdom.base.eth\` and \`computerwisdom.base.eth\` pointed to the *historical A380 wallet*, not to a proved signing session. Wallet ownership/signing authority = UNKNOWN. Historical Drive spec \`WisdomFamilyDocuments — BNS ENS DNS Family Recursive Replay\` explicitly defines **BNS = UNEXPANDED USER LABEL**; do NOT substitute the unrelated Stacks Bitcoin Name System by acronym alone. BNS authoritative binding = UNKNOWN. Resolver address does not prove the wallet owner is the individual, or that their PC controls its keys.

## Mathematical theorem, not an identification certificate

At 128 BPM, beat period \`T=60/128=0.46875 s\`. At 30 fps, one beat spans \`14.0625\` frames; temporal sample period is \`1/30 s\`, with an ideal nearest-frame quantization uncertainty up to \`1/60 s\`. If a **synthetic** dancer's measured 0.5 m forward step spans one beat, path speed = \`0.5/0.46875=16/15 m/s = 3.84 km/h\`. At the same BPM, a stationary dancer can have zero net center-of-mass travel.

A distinct thought experiment models a false match rate of 0.0001 in independent comparisons against a 100,000-person gallery: \`E=false candidates=10\`, \`P(at least one)=1-(1-0.0001)^100000≈0.9999546\`. This rate is **hypothetical**, NOT measured gait accuracy and not a valid extrapolation to all biometric systems. It illustrates why gallery search cannot safely act as a passport/automatic accusation. References: [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html), [NIST SP 800-63A-4](https://pages.nist.gov/800-63-4/sp800-63a/ial-general/), [Microsoft TPM](https://learn.microsoft.com/en-us/windows/security/hardware-security/tpm/how-windows-uses-the-tpm).

## Mandatory CI-FIRST verdict gates

| Scoped check | Verdict today | Proof needed to advance |
|---|---|---|
| 128 BPM reference math | PASS | Independently replayed Wolfram fractions |
| Existing draft catalog bytes | PASS | Wolfram Git blob SHA1 match in prior audit |
| Synthetic motion measurement logic | TEST REQUIRED | Run local standard-library replay + adversarial tests |
| Calibrated real dancer travel speed | UNKNOWN | Consent-based video, timestamps, calibration, error estimate |
| Lawful video/photo rights and consent | UNKNOWN | Original source + consent/rights record |
| Biometric identity against official record | UNKNOWN | Authoritative legal, technical and fairness validation; never automatic exclusion |
| Independent Windows TPM hardware trust | UNKNOWN | Fresh signed quote + EK→AK trust + approved PCR policy |
| Encrypted Windows PC media sync | UNKNOWN | Authenticated sender/receiver, test ciphertext, byte-by-byte readback |
| Music / Movies / Live hostname routing | FAIL | No configured exact/wildcard route observed; needs reviewed deployment |
| Public ENS resolver readback | PASS (resolution only) | Separate signing challenge to prove key control |
| BNS meaning and binding | UNKNOWN | Clarify the user-defined label and obtain direct receipt |
| Public evidence of misconduct | UNKNOWN | Original admissible provenance, legal process and human evaluation |

## Engineering constraints
- **No passport replacement claim**. Hardware-backed passkeys or a physical security key can serve as an independent authentication factor; dance is optional, revocable supporting research, not a credential.
- **No permanent public biometric index** or automated face/gait matching against people in video without permission and narrowly defined legal basis.
- **No presumption of crimes** from unspecified media. Criminal allegations and victim footage require appropriate authorized evidence handling, not public reposting.
- Event log: append-only CORRECTION/SUPERSEDED entries, never silently overwrite originals; PASS/FAIL/UNKNOWN only for engineering checks. Human final decision.
- **No action taken:** DNS, Worker deployment, git merge, wallet signature/payment, BitLocker, TPM enrollment, private Cloudflare bindings, secure sync, media upload or identity enrollment.

## Next executable research milestone
Run \`python3 security/trinity-motion-v1/replay.py --self-test\` then \`python3 security/trinity-motion-v1/replay.py\`. It uses **synthetic geometry only** and verifies SHA-256 of original fixture bytes. It cannot certify actual people, media content, TPM trust or deployed website.
