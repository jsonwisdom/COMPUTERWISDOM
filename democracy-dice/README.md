# Democracy Dice — v1.6 implementation

**STATUS=HOLD. AUTHORITY_CREATED=false. FINAL_AUTHORITY=JASON.**
Nothing here is merged, deployed, published, signed, or financially active. Promotion out of HOLD is Jason's call only.

A civic game: three fair six-sided dice pick one of 216 prompts. Every roll, replay, piece of evidence,
finance-provenance record, and human approval is a schema-checked, JCS-canonicalized, SHA-256-digested receipt.

## Components
| # | Component | Files |
|---|---|---|
| 1 | Strict JSON Schemas (2020-12) + semantic validators | `schemas/*.schema.json`, `src/validate.js` |
| 2 | RFC 8785 canonicalization + SHA-256 fixtures | `src/jcs.js`, `src/vectors.js`, `fixtures/` |
| 3 | Unbiased three-D6 selector (rejection at 252, 216 outcomes) | `src/dice.js` |
| 4 | Deterministic replay engine | `src/replay.js` |
| 5 | Append-only evidence ledger + independent finance provenance | `src/ledger.js`, `src/finance.js` |
| 6 | FEC / OpenSecrets / third-source adapters (read-only, honest availability) | `src/adapters.js` |
| 7 | Human approval: HMAC-authenticated, atomic single-use receipts | `src/approval.js` |
| 8 | Accessible civic game UI (SYNTHETIC demo) | `ui/index.html`, `ui/dice-ui.js` |
| 9 | Tests: unit, integration, negative, security, concurrency | `test/` |

## Data labels
Every data-bearing record carries one of `LIVE | MOCK | SYNTHETIC | LIVE_UNAVAILABLE`. A record can be labeled
`LIVE` only when every source reports `AVAILABLE` with a retrieved-content digest. By default, adapters make no
network calls and report `NOT_CONFIGURED` / `LIVE_UNAVAILABLE`. HTTP_200 ≠ CONTENT_VERIFIED.

## Approval states
`HUMAN_APPROVAL_RECORDED` and `CRYPTOGRAPHIC_IDENTITY_VERIFIED` are separate fields. The HMAC proves that this store
issued the receipt. It does **not** prove who the human is, so `CRYPTOGRAPHIC_IDENTITY_VERIFIED` is always `false`
here. Setting it to `true` requires `identityEvidence.verifiedBy`, and no identity verifier is built (see GAPS.md).

## Run
```
cd democracy-dice
npm ci
npm test            # node:test, 38 tests
npm run evidence    # writes evidence/junit.xml, test-output.tap, summary.json, SHA256SUMS
python3 scripts/crosscheck_syn002.py   # independent cross-check of the SYN-002 digest
```
Open `ui/index.html` in a browser for the demo. It works offline and has no paywall.

Env flags for adapters (default off): `DD_ENABLE_HTTP=1`, `DD_FEC_API_KEY`, `DD_OPENSECRETS_API_KEY`, `DD_THIRD_SOURCE_URL`.
