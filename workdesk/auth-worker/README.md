# BUILD 002 — YubiKey challenge/response (DRAFT ONLY)

**HOLD — NOT DEPLOYED, NOT AUDITED, NOT AUTHENTICATED.**

This change adds a standalone browser request page at `workdesk/yubikey-echo.html` and a Cloudflare Worker code scaffold in `workdesk/auth-worker/`. It does **not** replace the live homepage or the public gateway. No wallet signing or x402 payment code is added.

## Security boundary

- Public GitHub Pages is not capable of guarding secret content. Worker `/private` serves only a non-sensitive authenticated-session placeholder. Do not upload personal records to public repo paths.
- Server issues one-time 180-second D1-backed challenge and deletes it at verification.
- Registration is limited to an initially empty credential table and a separately configured Worker secret named `BOOTSTRAP_TOKEN`; no token is checked in. Use a long unpredictable secret and remove it after initial enrollment.
- WebAuthn assertions must verify RP ID `jsonwisdom.com`, HTTPS origin `https://jsonwisdom.com`, cryptographic signature, challenge and required user verification. Unknown credentials are rejected.
- Session is opaque, SHA-256 hashed in D1, HttpOnly/Secure/SameSite=Strict, 15 minutes; logout revokes it. YubiKey removal does **not** revoke sessions.
- D1 tables and secrets must be provisioned out of band. `wrangler.toml` deliberately has no database ID or active route. The initial worker must not serve a public private-data API until these are configured.
- CORS only accepts the expected homepage origin. Every authentication request must go to the dedicated custom-domain Worker, `auth.jsonwisdom.com`. TLS and DNS binding are required.
- Multiple security issues may remain in this untested scaffold, including credential counter race conditions, registration concurrency, logout CSRF controls, browser compatibility and recovery enrollment. Treat as engineering draft; require independent review before production.

## Provisioning / validation (not yet performed)

1. Provision isolated Cloudflare D1 database; apply `schema.sql`; create `AUTH_DB` binding in Wrangler. Configure dedicated Worker custom domain without modifying `jsonwisdom.com` DNS routes.
2. Set strong `BOOTSTRAP_TOKEN` via Wrangler secret workflow; never place in repository, HTML source, logs or this chat.
3. Install dependencies and run unit/integration verification in a disposable environment. This scaffold has not yet passed that gate.
4. Review and correct the WebAuthn implementation against pinned current `@simplewebauthn/server` APIs, credential encoding, safe registration limits, and replay protection.
5. Deploy in staging; test unauthenticated `/private` denial, wrong key, cancellation, expired/replayed challenge, origin mismatch, registration restriction, session expiration, logout and enrolled owner key success.
6. Record a Jason-approved human browser acceptance test; only then consider changing the homepage gateway navigation.
7. Keep wallet signing, payments and other privileged workflows on **HOLD** independently.

**Do not merge as “authentication complete.”** There is no user-facing live authentication until actual service configuration, safe enrollment and acceptance tests pass.
