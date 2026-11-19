# Computer Wisdom — Cloudflare isolated front-door preview receipt

- **Observed deployment UTC:** 2026-11-19T04:56:14.388801Z (Cloudflare API result)
- **Platform:** Cloudflare Workers, new standalone script, separate from all pre-existing Workers and Pages projects
- **Worker ID:** `cw-ci-first-frontdoor-pr774-preview`
- **Preview URL:** https://cw-ci-first-frontdoor-pr774-preview.jaywisdom44.workers.dev/
- **Deployment ID:** `f3f9c4b7-b6ad-44c3-9a84-f669295557e7`
- **Version ID:** `63706904-fc31-43e6-978b-08090430d611`
- **Cloudflare API status:** deployment 100% targeted to this version; workers.dev subdomain enabled, separate version-preview endpoints disabled
- **GitHub review:** https://github.com/jsonwisdom/COMPUTERWISDOM/pull/774 (draft, unmerged)

## Served assets and Git blob integrity anchors

- `ci-first/live-builder-v0.4/site/index.html` — git blob SHA `4ae551c93e5baf5574c096fe5f2e37bf58b46020`
- `ci-first/live-builder-v0.4/site/styles.css` — git blob SHA `74bcb8593886077c2e47b6377fdd324107f98849`
- `ci-first/live-builder-v0.4/site/app.js` — git blob SHA `9a40a3413aac34cd19388478d8303705b097a338`
- `ci-first/live-builder-v0.4/site/projects.json` — git blob SHA `2fafd46fba2779b85ed83b0fe87d254d93963302`
- `ci-first/live-builder-v0.4/site/forest.json` — git blob SHA `714831a985066da9c4eb91d58f1ac8521ad32c77`

All five files were fetched from `ci-first/live-builder-inclusive-v0.4` through the authenticated GitHub connector and embedded as immutable static response content in the Worker script. Cloudflare deployment is independent of private repositories; no Cloudflare runtime bindings or credentials were configured.

## Privacy and publication

- GitHub inventory snapshot: 81 public repository records; identities of 7 private repositories omitted
- Merkle forest: 5 candidate trees / 3 groves; PENDING_HASH not represented as verified proof
- No private Google Drive records, minors' personal information, wallet signatures, or secrets copied into Worker
- Static HTTP GET/HEAD only; Content Security Policy, noindex headers, robots disallow all, no cookies, payments, uploads, or authentication required
- URL is publicly reachable **if Cloudflare network routing completes**, despite noindex; noindex is not access control. Public content only.
- No changes to production domains, DNS, existing Pages projects, old Workers, or protected GitHub branches
- **Verification limit:** Cloudflare provider API confirmed version and workers.dev enablement. Independent browser HTTP fetch failed in the execution environment due DNS/network access restrictions; do not claim browser end-to-end PASS until independently checked.

## Roll-forward plan

1. Validate live browser network responses and mobile behavior.
2. Refresh public-only project snapshots, then query real last-commit timestamps as separate fields.
3. Check accessibility at iPhone widths and run link/provenance audits.
4. Promote only after Jay authorizes production integration.
