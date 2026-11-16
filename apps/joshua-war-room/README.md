# JOSHUA WAR ROOM v1

Case: CW-JOSHUA-STACK-001

## Deployment
- Public site: https://joshua-war-room.vercel.app
- Vercel project: `joshua-war-room` (owned by team `jsonwisdoms-projects`)
- Deployment: `dpl_3f6q7xyVofnFpNJGMan6S8DCvUXv` (READY, production)
- Source archived on this review branch; the live deployment is an inline Vercel deployment, **not** yet linked to Git CI.

## Wallet sign-in
- Expected wallet: Computer Wisdom PC, `0x65891F97db01C8fC9F76f4DFE65Bd44F8261f1B0`
- Network: Base (chain ID 8453).
- Browser: Coinbase Wallet extension / injected EIP-1193 provider.
- Server: short-lived SIWE-formatted EIP-191 `personal_sign` challenge, address equality check, cryptographic verification via viem (EOA, with Base smart-wallet verification fallback), HMAC-sealed HttpOnly session.
- Vercel encrypted project variable required: `JOSHUA_SESSION_SECRET`; do not commit its value.
- Expiration: challenge 5 minutes, session 30 minutes.
- Wallet key control at signing time is **not** legal title, GitHub repository ownership, domain ownership, smart-contract ownership, permission to spend, access to the historical 0xA380 wallet, or an on-chain deployment.

## Gameplay
- Non-operational fictional strategy lab, D20 rolls, Falken narrative counter-moves, local replay export.
- Current simulation not a production AI agent; points are off-chain and have no monetary value.
- No billing, transfers, payments, or smart-contract transactions.
- Business pricing cards are proposals only.

## Evidence checkpoint
- Vercel deployment state: READY.
- GET `/api/auth?mode=session` without session responded HTTP 200, `{"authenticated":false}`.
- Browser wallet authentication and valid signature have not yet been tested with the user's wallet.
- Source publication to this branch does not merge or alter the local `JOSHUA-CONTRACT` registry or JOSHUA/Falken PR #768.

## Review required before extended release
- Authenticated real-wallet browser end-to-end test, expired/replayed challenge and origin rejection tests, verification of EIP-1271/6492 behavior if the account is smart-contract based.
- Cookie/session threat model, rate limits, dependency audit, CI, deterministic scenario replay and receipt provenance.

## Explicit replay selection gate (review branch only)
- The owner action requires an explicitly previewed **and confirmed** replay; it no longer silently uses browser localStorage.
- **LOAD VERIFIED 7-TURN FIXTURE** calls read-only `GET /api/fixture`, checks the full original file bytes against SHA-256 `397ea9f7240523f436c4abf3db2a9e115b833a1a7e658fc3a8f728b8095dada3`, previews the seven-turn totals, and requires **CONFIRM THIS REPLAY**.
- **PREVIEW LOCAL GAME** snapshots the current browser game separately; changes to the local game invalidate that pending/confirmed local selection.
- `POST /api/auth?mode=attest` requires `source` and `sourceDigest`; the server verifies game rules, compares archived selections to the exact pinned JSON, and binds source + digest into its HMAC-backed receipt.
- An archive selector does not prove an original human game action; a browser-local selector does not prove original exported file bytes. Neither selector creates public signatures or durable receipts.
- The live Vercel site remains an inline deployment, not linked to Git CI; publishing these branch edits does **not** change production.
- Run Node tests and verify Vercel serverless fixture inclusion/end-to-end behavior before considering deployment.
