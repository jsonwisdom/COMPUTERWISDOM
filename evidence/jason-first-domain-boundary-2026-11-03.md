# JASON FIRST — Domain Boundary Evidence
**Date:** 2026-11-03 · **State:** CONFIGURATION_DOCUMENTED / SIX_ORG_NAMES_ATTEMPTED_BLOCKED
**Classification:** read-only configuration evidence, not organization certification.

## Source and scope
Authenticated Cloudflare API read of accounts, zones, DNS records, Worker route patterns, Worker custom-domain bindings, and Worker scripts. GitHub repository inspection. Connector-normalized responses, NOT captured raw HTTP bytes. No registrar exports, independent authoritative DNS, RDAP, public-log witness, on-chain ownership signatures, or successful independent HTTP health fetch.

## Observations (only the connected Cloudflare account)
- **1 account; 2 active zones:** jsonwisdom.com, jsonwisdom.io.
- **DNS returned:** 14 records for .com (including 4 apex GitHub Pages A records, www CNAME, and 9 proxied AAAA 100:: placeholders); 0 for .io.
- **16 Worker scripts; 0 conventional Worker route patterns; 9 enabled Worker custom domains.**
- Custom domains, verified as *configuration bindings*, not independently fetched live responses:
  - evidence.jsonwisdom.com → minnesota-zero-day-evidence-v1
  - audit.jsonwisdom.com → cwaas-receipt-first-audit
  - wallet.jsonwisdom.com → jsonwisdom-wallet-connect
  - auth.jsonwisdom.com → jsonwisdom-workdesk-auth-staging
  - classes.jsonwisdom.com → classes-with-glasses
  - triggerdeck.jsonwisdom.com → political-triggerdeck-2026
  - gallery.jsonwisdom.com → jasons-art-gallery
  - game.jsonwisdom.com → wisdom-live-observer
  - inventory.jsonwisdom.com → wisdom-catalog-curator
- **Why 0 routes is not a missing-Worker finding:** Cloudflare Custom Domains bind hostnames directly to a Worker; they are distinct from route patterns. See https://developers.cloudflare.com/workers/configuration/routing/custom-domains/ .
- **Pages listing:** an API attempt failed because of rejected page/per_page options. No claim about presence or absence of Pages deployments.
- **HTTP health:** independent webpage fetch to evidence.jsonwisdom.com and audit.jsonwisdom.com was attempted and unavailable; binding is NOT an HTTP proof.

## Claimed six .org domains — scope-blocked
`count_reported: 6`; `count_verified: null`; `names: null`; `status: attempted_blocked`; `blocker: no names or authorized alternate registrar/account inventory supplied`. No .org zone appears in the returned connected-account inventory. **This is not a finding that the domains do not exist elsewhere.**

## Governance finding (positive)
A proposed direct commit to `master` was rejected with GitHub policy HTTP 409: “Changes must be made through a pull request. Required status check \"verify\" is expected.” The protected branch is not bypassed; this evidence is submitted via a separate branch and PR.

## From on-chain to organization and back — verification boundary
Wallet activity, DNS control, and registered organization identity require separate evidentiary chains. Before linking them: capture original bytes; SHA-256 BEFORE parse; dated RDAP/registrar records; canonical DNS/TXT ownership challenge; authorized operator attestation; on-chain signed message with chain ID and address; independent third-party witness; independent return verification. All these steps remain **pending** for six unnamed .org domains.

## Limitations / release
`inventory_completeness: connected_account_only`; `raw_http_sha256: null`; `independent_dns_verified: false`; `registrar_verified: false`; `organization_verified: false`; `onchain_org_binding_verified: false`; `external_anchor: null`. A GitHub PR is evidence publication, **not proof of correctness or production deployment**. Do not overwrite the existing `evidence.jsonwisdom.com` Worker without inspecting and preserving its existing behavior.

**No privileged domain. No privileged Worker. No privileged auditor.**

## Receipt clarification — seven-item amendment closure
- The nine-binding SHA-256 covers **connector-normalized selected fields**; the raw upstream Cloudflare HTTP response was **not preserved** and has no claimed raw-byte hash.
- The attempted HTTP probe has failure class `reader_access_error`; DNS RCODE, resolver, status, and precise probe timestamp remain `null`. This is **not** a verified NXDOMAIN or outage.
- The organizational ownership scheme list is **empty because no qualifying scheme has yet been defined**; no on-chain ownership assertion can qualify.
- **The `completed_discrepant` finding concerns the connected-account inventory boundary, not whether six reported .org domains exist.** The six names remain `null`.
- The receipt's `original_reviewed_commit_sha` and `reviewed_at_commit` both pin `1c7c948892dfeafc2532e12fc8ebaee8e0f75ae5`, the prior PR head, while subsequent amendments form new commits.
- The GitHub `verify` workflow checks selected repository proof-artifact JSON and honesty flags; **passing it does not authenticate Cloudflare observations, domain ownership, or the evidence receipt's factual findings**.
