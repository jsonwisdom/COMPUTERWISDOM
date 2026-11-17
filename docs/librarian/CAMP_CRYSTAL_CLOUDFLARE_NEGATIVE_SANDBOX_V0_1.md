# Camp Crystal NEGATIVE Sandbox — Cloudflare Registration V0.1

Date: 2026-11-16 (America/New_York)
Class: FICTIONAL STORY SANDBOX / TECHNICAL DEPLOYMENT RECORD
Status: WORKER_UPLOADED_NO_PUBLIC_ROUTE
Authority: false
Owner: Jason Wisdom, review required
Cloudflare Worker: `cw-camp-crystal-negative-sandbox-v01`
Zone candidates: jsonwisdom.com / jsonwisdom.io — NO NEW DNS RECORDS
Git branch: quad-onion-librarian-20261116-v1

## Verified execution
- Cloudflare uploaded a **new** isolated Worker successfully.
- Existing Workers and DNS entries were not modified by this operation.
- Checked: no zone route for this Worker in either zone, no Worker domain, Worker subdomain enabled=false and previews_enabled=false.
- This is NOT a live web site or active voice service.
- No Cloudflare R2, KV, D1, or other storage bindings were created.

## Paths (Worker dispatch map, NOT DNS records or physical folders)
- / — intro
- /eu/ — Europe Lake Node; original fiction
- /cn/ — China Ninth Copy; fictional draft
- /ru/ — Russia Winter Archive; fictional draft
- /us/ — America Wisconsin Camp Crystal; fictional draft
- /bletchley/ — one verified lake-naming anchor, separate from Bletchley history
- /kernel/prime/ — prime checkpoint convention
- /children/ — parent review HOLD (403)
- /health — internal status JSON
- /manifest — read-only path manifest

**DEFAULT DENY:** unspecified paths 404. Methods except GET and POST /voice/preview return 405.

## Voice-command design
The sandbox exposes only a text-transcribed dry-run interface: `POST /voice/preview` with JSON `{"command":"shannon design"}` or the allowlisted strings below.
- shannon design → design
- shannon speak → preview
- shannon build → build-proposal
- shannon review → review
- shannon negative → default-deny

All recognized commands reply with `PREVIEW_ONLY`, `executed:false`, `mutation:false`, `voice_capture:false`. This does not access microphones or authenticate a speaker. No command changes DNS, routes, files, custody, wallet state, military or other external systems.

## Later design review gates
1. Check script source and security constraints before enabling a public route.
2. Review browser voice support and privacy/permission prompts for a possible opt-in speech-to-text UI; no always-on listening.
3. Confirm the precise hostname for a proposed isolated subdomain; do not alter existing domain traffic until authorized.
4. If durable folders/files are needed, choose GitHub repository paths and/or R2 object prefixes with an explicit save/cleanup and retention policy. Object prefixes are not DNS.
5. Add synthetic tests for known/unknown paths, rejected methods and parent HOLD.
6. Copyright/trademark review before using Camp Crystal as commercial branding.

## Foundational source / fictional authority restrictions
- [European original canon](../../ARCHIVE/GB-EUROPEAN-80S-ALIEN-REBOOT-v0.1.md)
- [Bletchley one-anchor record](BLETCHLEY_DELTA17_ONE_CRYSTAL_LAKE_ANCHOR_V0_1.md)
- [Parental gate](JASON_QUAD_ONION_PARENT_GATE_V0_1.md)

No NATO/RAF/USAF activation or authority. American Royal Air Force is a fictional project name only. No operational war functions.

## Deletion and cleanup
DO NOT automatically delete files. Propose what to archive/retain; perform deletion only upon explicit review. Keep Git history as evidence of created files.
