# BUILD REPORT — Democracy Dice v1.6

**STATUS=HOLD · AUTHORITY_CREATED=false · FINAL_AUTHORITY=JASON**

| Field | Value |
|---|---|
| Branch | `feature/democracy-dice-impl-v1.6` |
| Base (master tip) | `626e10362581559cbbd1fb36ac1072947fccaf14` |
| Code commit tested | `7e432f155373d87d8ec62654956ece734fb0b239` (tests and evidence ran against this tree) |
| Run time | 2026-10-25, about 08:30 CDT (UTC-5); exact UTC in `evidence/summary.json` |
| Node / npm | v20.19.2 / 11.21.0 |
| Python | Python 3 (exact version in `evidence/summary.json`; used only for the SYN-002 cross-check) |
| Dependencies | ajv 8.17.1, ajv-formats 3.0.1 (pinned, `package-lock.json`). Test runner: built-in `node:test` |

## Command log
```
git clone --depth=50 https://github.com/jsonwisdom/COMPUTERWISDOM.git   # authorized CLI exception; local bare mirror had no refs
git checkout -b feature/democracy-dice-impl-v1.6                         # from 626e1036
git log -S <TV-001 hex>; git grep -e 4d576d0388 -e 492445467a47          # no hits (shallow 50)
cd democracy-dice && npm ci
npm test                                   # 38 pass / 0 fail
npm run evidence                           # writes evidence/*, exit 0
python3 scripts/crosscheck_syn002.py       # sha256:14cfa76e…0eff == JS digest
```
The first test run had 3 failures, all fixed before commit:
- An Ajv strict-mode union type: fixed with `allowUnionTypes`.
- A wrong expected string in the UTF-16 key-order test. The author's expectation was wrong, not the implementation: per RFC 8785, U+20AC sorts before the surrogate pair U+D83D.

## Results
| Suite | Tests | Pass | Fail |
|---|---|---|---|
| unit (JCS, vectors, dice, uniformity) | 11 | 11 | 0 |
| schema/semantic (incl. security invariants) | 8 | 8 | 0 |
| integration + negative (replay, ledger, adapters, finance, approval) | 8 | 8 | 0 |
| security + concurrency (approval reuse, MAC, subject, 500 async, 8 workers) | 8 | 8 | 0 |
| ui (a11y and labels, static) | 2 | 2 | 0 |
| **Total** | **38** | **38** | **0** |

The suite split is by file; `evidence/junit.xml` is authoritative. A few negative and security cases live inside the integration and schema files.

Vectors: TV-001 `SEARCH_MISS`, TV-002 `SEARCH_MISS` (fail-closed, not MATCH); SYN-001 `MATCH`, SYN-002 `MATCH`.
Uniformity: chi-square over 216,000 seeded rolls against 216 cells is below 300 (df=215).
Rejection: the exhaustive 256-byte map gives 42 bytes per face and 4 rejected.

## Evidence
`evidence/junit.xml`, `evidence/test-output.tap`, `evidence/summary.json`, `evidence/SHA256SUMS`. Re-run `npm run evidence` to regenerate.
Timestamps make the hashes differ between runs. Pass/fail counts and vector results must stay the same.

## Labels used
- Rolls: SYNTHETIC (seeded).
- Adapters: LIVE_UNAVAILABLE / NOT_CONFIGURED.
- Adapter status-mapping tests: MOCK fetch.
- No LIVE data anywhere.

## Not done (by rule)
No merge, deploy, publish, signing, wallet, or financial transaction. See `GAPS.md`.
