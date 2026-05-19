# Compute Wisdom v1.3 Test Vectors

**RESEARCH ONLY — NOT IDENTITY CREDENTIALS**

These vectors exist to test replayability, verification transparency, and failure detectability.
They are not identity credentials, access credentials, legal documents, or production attestations.

## Purpose
Independent replay from public materials without network access, private APIs, or proprietary runtimes.

Tests:
- FM-03 Replay Theater
- FM-04 Offline Redress  
- FM-06 Vendor Dependency
- Replay determinism
- Authority expiration semantics

## Usage
```bash
pip install -r requirements.txt
python run_all_vectors.py
```

Expected output:
```
WARN: no_key_binding (vector_01)
PASS: valid_kb (vector_02)
FAIL: tampered_sd_hash (vector_03)
FAIL: wrong_audience (vector_04)
FAIL: expired_issuer (vector_05)
```

## Boundaries
- All vectors are ephemeral, synthetic, non-identifying
- No real citizen data
- No production issuer semantics
- No government branding
- HS256 used for test simplicity (production would use ES256)

A receipt is a pointer to replayable legitimacy, not legitimacy itself.
