# CI-FIRST v2 — SOURCE-ONLY, REVIEW HOLD

**Proposed repository:** `jsonwisdom/COMPUTERWISDOM` / `master`.

This is **v2**, a separate artifact correcting the two identified input-validation defects. It does not overwrite the locked v1 ZIP or modify any repository, Cloudflare, wallet, Stripe, or x402 surface.

## Fixes

- The Python `eligible` and `classify` functions require a list/tuple of **exactly four** states drawn from PASS, FAIL, UNKNOWN, HOLD.
- Human approval and signed authorization must have literal Python `bool` types. Strings (including `"False"`), integers, `None`, dictionaries, and lists are invalid.
- Any invalid input is ineligible, and `classify` reports `FAIL` for input-schema violations. Do not confuse malformed-input FAIL with a claim of malicious activity.
- 1,024 exhaustive valid input combinations remain; expanded malformed tests, a missing-signature mutant, and a missing-schema mutant are included.

## Files

- `.github/workflows/ci-first-authority-invariant.yml`: proposed CI workflow using read-only permissions; not committed.
- `scripts/ci-first/authority_invariant.py`: local Python verifier, deterministic JSON receipt.
- `scripts/ci-first/authority_invariant.wl`: independently authored Wolfram replay model; **not executed by GitHub Actions**.
- `authority-model-receipt-v2.json`, `.sha256`: local Python evidence output only.
- `wolfram-replay-observation-v2.json`: assistant-recorded independent Wolfram evaluator results; not independently signed.
- `manifest-sha256.txt`: hashes of package source and receipt files; no external signature.

## Replay

```bash
python3 scripts/ci-first/authority_invariant.py --out authority-model-receipt-v2.json
sha256sum -c authority-model-receipt-v2.sha256
# Optional independent Wolfram Engine:
wolframscript -file scripts/ci-first/authority_invariant.wl
```

The checksum proves local byte consistency relative to the recorded digest; not authorship, provenance, deployed byte identity, or independent custody. Wolfram results obtained via a separate Wolfram tool are not proof that this bundled file was executed in GitHub Actions. `PASS` applies to the source-only model and malformed tests, not production controls.

**No automatic promotion, no financial transfer, no new authority.** To block merge on failed tests, a repository admin must separately configure and verify a required status check and protections on workflow changes. Even a required check does not grant authority or establish live enforcement.

`AUTHORITY_CREATED=false` · `LIVE_ENFORCEMENT=UNKNOWN` · `RELEASE=HOLD`.
