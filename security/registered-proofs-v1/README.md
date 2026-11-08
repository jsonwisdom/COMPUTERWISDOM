# CI-FIRST Registered Proofs v1

Development candidate for proof.jsonwisdom.com. No deployment, wallet signing, TPM provisioning, BitLocker change, production DNS edit, payment, legal finding or third-party certificate is authorized or performed.

## Full developmental cycle

1. AUDIT the existing domain, Worker bindings, GitHub evidence and FullMath burden specification.
2. DECLARE one typed claim and exact required checks per new public JSON record.
3. CREATE new records with source URLs and exact-byte SHA-256 or null when bytes were not captured.
4. HASH the exact raw record files, build deterministic, domain-separated SHA-256 Merkle tree and inclusion proofs.
5. REGISTER the manifest under a GitHub draft PR; preserve original records.
6. TEST forged credentials/authority promotion, unknown precedence, hash tampering, incorrect sibling paths, and illegal POST writes.
7. REPLAY the manifest and inclusion proofs from independent checked-out bytes; GitHub Actions uploads a receipt even if other checks fail.
8. WITNESS source assertions separately through GitHub, Cloudflare, live HTTP, or a nonce-bound TPM quote with independent AK/EK trust. Missing proof remains UNKNOWN.
9. PUBLISH only after human review, an independent delivery probe and explicit release authorization. worker.mjs is candidate GET/HEAD only; the deployed proof.jsonwisdom.com site remains unchanged.
10. CORRECT by appending new superseding records, never silently rewriting a previous observation. PR CI blocks changes to previously recorded base-branch proofs, but does not establish immutable storage or external timestamping.

## CI-FIRST and civic FullMath

Engineering statuses are PASS / FAIL / UNKNOWN and do not replace the civic/legal HOLD / CONFLICT states in BURDEN_OF_PROOF_FULLMATH_ONLY_V0_1. AUDIT_RECEIPT_DEMAND is not LEGAL_BURDEN. A hash proves only byte equality and not authorship, fraud, secure custody, legal authority or validity of a TPM key.

## Privacy

No unique endorsement keys, event logs, recovery passwords, wallet secrets, personal records, paid client data, or payment authority in this public branch. The record of a successful GitHub client build does not establish signed TPM hardware attestation. A Cloudflare domain mapping is not verified HTTPS delivery.

## Independent replay

Run: node --test security/registered-proofs-v1/proof.test.mjs security/registered-proofs-v1/worker.test.mjs
Then: node security/registered-proofs-v1/proof-core.mjs verify

Expected scoped root SHA-256: 138b54e72f8999659cbfd3f952b33ad78630811edba60730f56dfd3461835f3e

Existing draft PR #742 security/jasons-dns-ci remains a separate fail-closed domain/TLS/registrar gate. This proof-registry candidate does not bypass its security findings.
