# JASON GITHUB SIDECAR V0.1

**Class:** isolated GitHub navigation, inspection, review and proposed-change lane  
**State:** DESIGN / DRAFT PR / NOT DEPLOYED  
**Root:** JASON; final decision authority: JASON  
**Upstream:** `jsonwisdom/COMPUTERWISDOM`; extension to other repositories is read-only until separately scoped.

## Mission

Traverse GitHub **down** from account/organization -> repository -> protected branch/ruleset -> workflow/Pages/environment -> commit/tree/file/line -> test/log/receipt, and **up** from a finding -> reproducible evidence -> bounded correction -> review -> human release decision. The sidecar must NOT change the main mission simply by being consulted or invoked.

## Current target: Pages CNAME incident (2026-10-16)

- User's GitHub Pages settings showed: `Unable to commit CNAME because the Pages branch is protected.`
- `master` was verified protected, SHA `e954c165a5d18dba78e6e63dd86f84b1428a31a8`.
- Rulesets: `OBSERVER_REFUSAL_MEMBRANE_001` (16924885), `Verify` (17085224). Do not disable or bypass either.
- The repository has `.github/workflows/static.yml`, a Pages deployment workflow on push to `master`.
- Root `CNAME` was absent. GitHub's documented behavior: branch-publishing settings can write a CNAME file, while **GitHub Actions publishing does not need or use one**.
- The screenshot suggests a *publishing-source mismatch*; exact Pages publishing-source setting remains `NOT_INDEPENDENTLY_READ`, because the GitHub Pages settings API is unavailable to the connected GitHub tool.
- **Safe correction to review:** inspect `Settings > Pages > Build and deployment > Source`. If currently `Deploy from a branch`, switch to `GitHub Actions` through an authorized admin session, confirm the custom workflow and production endpoint, then set custom domain `jsonwisdom.com`. Do not pretend a draft CNAME commit fixes GitHub Actions domain binding.
- DNS prerequisite: do not point a GitHub hostname until the Pages custom domain is claimed/verified. After claim, configure Cloudflare DNS in a separately scoped, approved action; preserve existing public site until HTTPS smoke tests pass.
- `jsonwisdom.com` and `jsonwisdom.io` are registered to the connected Cloudflare account with active zones. On initial read, each zone contained zero DNS records. Future reads supersede this observation **only by timestamped new observations**, not historical overwrite.

Sources: 
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/troubleshooting-custom-domains-and-github-pages
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

## Layer map and two-way traversal

| Level | Read-only descent | Ascending evidence |
| --- | --- | --- |
| L0 | Human mandate, scope, account | Jason human acceptance/rejection |
| L1 | Organization/account, repository | Repo/path identity and permissions |
| L2 | Default branch, tags, protected rulesets | Exact SHA, ruleset IDs, policy conflicts |
| L3 | PRs, workflow YAML, environments and Pages | Trigger, branch source and deployment status |
| L4 | Files, path/line, artifacts and CI jobs | Content digest, diff, test/log links |
| L5 | Proposed remediation branch and draft PR | Limited change-set and counter-receipt |
| L6 | Independent replay and reviewer decision | Evidence-bound disposition: PASS/HOLD/FAIL |
| L7 | Post-approval merge/deploy verification | Production observed, not implied |

Descent never grants permission. Ascent cannot skip scope, version, source, independent checks, or the final human gate.

## Capability rules

**Always allowed read-only with connected permissions:** retrieve repository files and metadata, inspect commit/tree/PR diff, rulesets, CI status and logs, compare candidate against baseline, query provider configuration without mutation.

**Allowed as an isolated proposal only when requested/authorized:** create a clearly named review branch from an exact SHA, make scoped changes on that branch, open a **draft** pull request, record checks and fail-closed blockers. Creation of a PR is not a request to merge.

**Separate explicit Jason approval for each impactful action:** DNS records; repository Pages settings; branch-protection or ruleset administration; pushing to protected branch; merging a PR; deployments, publications and redirects; updating canon/receipts; wallet signatures, authorizations, transactions, approvals or cryptographic releases.

**Forbidden automatic transitions:** disable rulesets; direct `master` edits; merge/deploy/fan-out on CI green; copy secrets or private wallet receipts to public files; silently replace historical evidence; convert observed addresses or domain records into human identity.

## Typed reducer

```text
SIDECAR_EXISTS          = DRAFT_PROPOSAL
DEFAULT_BRANCH_MUTATION = FALSE
PRODUCTION_MUTATION     = FALSE
RULESETS_DISABLED       = FALSE
CNAME_ERROR             = OBSERVED_IN_USER_SCREENSHOT
PAGES_SOURCE_CONFIRMED  = HOLD
DNS_DOMAIN_CLAIM        = HOLD
CLOUDFLARE_DNS_CHANGE   = NOT_PERFORMED
MERGE                   = NOT_PERFORMED
DEPLOY                  = NOT_PERFORMED
MAIN_MISSION            = UNMODIFIED
SYSTEM_GREEN            = FALSE
AUTHORITY_CREATED       = FALSE
CANON                   = FALSE
FINAL_DECISION          = JASON
```

## Rollback and historical immutability

A branch-only proposal can be closed without merging. Changing an external setting or deployment must carry a rollback plan *before* execution. `NEW_OBSERVATION != PRIOR_HISTORY_REWRITE != AUTHORITY`. This document is not an operational agent, an external service credential, an approved policy change, or a claim of successful production configuration.
