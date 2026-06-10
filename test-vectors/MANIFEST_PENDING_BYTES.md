# Compute Wisdom v1.3 Test Vectors — PENDING BYTE INSPECTION

**Status:** PENDING_BYTE_INSPECTION — files not yet committed  
**Expected zip SHA-256:** `3c6a3bd80d3f569917a114da8d73100083094c72ca0569fe25aa6ba104d58354`

## Expected file list with SHA-256

- `verifier.py` — `d6ff4685568434dee47eb209679f2aec0ae956ad4f2008a7acb4474fab29f042`
- `run_all_vectors.py` — `7f787ac4bf52f1b57dc22a3074ad9d6aba29df2728173e0767fe397676d6d2e3`
- `README.md` — `d75979da7c45fd0df3d700f3eae55ea28e13585bdde09800ff70c2fa58a3eed3`
- `requirements.txt` — `9b4948198d5a2ee0184d8b91c9689727d235ce80ae2f5bebad9f0f7b5cfe5ddc`
- `vector_01_no_kb.json` — `93e3b836c7ad804914041b2daa5a9f0b6b2439db971767d18aa5fa05759e71af`
- `vector_02_valid_kb.json` — `3eb244ee1dcaa3d69ed6ee2cdba3decdce5a94597465e03a09ca92bd02bb103b`
- `vector_03_tampered_sd_hash.json` — `0a3a013f23dadf87c6e52dd738562319dd88c2a80638066b6ab34a59d3758e19`
- `vector_04_wrong_audience.json` — `9467a56c860ee9c694ebd0103d51899dfb45551e744d08675059a42ec5525370`
- `vector_05_expired_issuer.json` — `1f46debab159aa2e811c29548b1903df6ccdf2cb93df86b386e92564ca7506a5`

## Boundary requirements

- TOY VERIFIER — HS256 shared-secret only, for test simplicity
- Production MUST use ES256/EdDSA with public JWK verification
- No network calls, no PII, all vectors synthetic
- README must state: `RESEARCH ONLY — NOT IDENTITY CREDENTIALS — TOY VERIFIER`

## Audit checklist

- [ ] Files match SHA-256 above
- [ ] `python run_all_vectors.py` outputs WARN/PASS/FAIL/FAIL/FAIL offline
- [ ] No imports beyond jwt, hashlib, base64, json
- [ ] No hardcoded secrets beyond test keys
- [ ] No runtime authority claims

## Merge rule

Do not merge until all files are present and hashes verify.

## Constitutional boundary

No ghost replay harness.  
No unverified bytes.  
No unseen zip.
