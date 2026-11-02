# School of Wisdom — live multi-Worker prototype

Status: LIVE PROTOTYPE / AUTHORED-CONTENT VALIDATION PENDING / PAYMENTS HOLD.

## Running surfaces

- https://game.jsonwisdom.com/ — system-check leaderboard and inventory perspectives.
- https://game.jsonwisdom.com/arena — free five-card practice game, real catalog titles, explicitly synthetic roles.
- https://game.jsonwisdom.com/method — nonnumeric Classes with Glasses method definition.
- https://inventory.jsonwisdom.com/inventory?view=learning — 500 source-backed catalog records.
- Other views: readiness, commerce, provenance. An optional exact sku parameter narrows the view.

Three Workers separate responsibilities: jasons-game-fixture-e2e (authenticated fixture scoring / immutable attempt receipts / archived replay); wisdom-catalog-curator (source catalog projections / authenticated staged metadata proposals); wisdom-live-observer (read-only service/network probes / operational leaderboard / free arena). They use service bindings and a dedicated prototype D1 database, separate from order/settlement databases. They share the prototype database; database-level per-Worker permissions are not asserted.

## Preserved intent

The recovered original game branch defines five cards, +100 per card, +40 per distinct synthetic role, +100 for five roles, and +100 for the correct evidence answer. Those rules remain unchanged: five roles score 800, then 900 with the answer. These are local practice points, not authenticated mastery, real-money rewards, truth or legal authority. The arena now fetches actual supplied catalog names/purposes rather than showing SKU-only cards.

Classes with Glasses uses ASK → FIND → PROTECT → COMPARE → LABEL → RECEIPT → REPLAY → EXPLAIN. Its proposed review dimensions are ESTABLISHED / NOT_ESTABLISHED / CONFLICT / NOT_APPLICABLE, with no adopted numeric weights. wisdom-method.mjs implements review-completeness HOLD gates. It does not independently authenticate evidence or classify legal/financial events. Its ten adverse scenarios are declared synthetic inputs with expected HOLD, not a fraud detector.

The system leaderboard lists scoped operational PASS/HOLD/FAIL observations and timestamps. It does not rank people. Actual learner rankings remain disabled pending identity, consent and versioned season/scoring policies. CH-002's four content labels are distinct from the review method's four dimension states.

## Versioned inventory and store proposals

inventory.mjs preserves 500 unique supplied SKU records and the SHA-256 identities of both source catalogs. Learning, readiness, commerce and provenance are separate projections. Purpose comes from supplied description; functions remain UNAUTHORED until a reviewed change exists. Unknown live Stripe state is never inferred from a supplied DRAFT catalog.

POST /proposals on the curator requires ADMIN_TOKEN and exactly sku, expected_source_sha256, basis, changes. Changes may propose title, purpose, functions and price_cents. The current source digest is checked before writing. Each proposal stores prior record, proposed fields, basis, actor scope, timestamp, status PROPOSED, approval=null, applied=false and a receipt digest. No apply endpoint exists. Retries currently create separate proposal events; proposal-key deduplication is a remaining enhancement. No Stripe prices, product titles, active flags or checkout settings were changed.

A future store writer must preserve old price IDs and link previous revision → reviewed proposal → authorization → API result → readback receipt. It must not convert a practice score into financial eligibility, content verification or a live price.

## Corrections made

- Missing/empty game credential now fails closed with 503; wrong credentials return 401.
- Strict nested fixture types prevent secret objects from entering public arrays or text maps.
- archive-bundle-v1.mjs preserves existing bundle bytes. registry.mjs is an immutable digest/scorer registry. Local regression proves an A receipt replays while active B differs. Actual live receipts also survived the engine update; arbitrary historical scorer versions are not supported automatically.
- JavaScript whitespace fraction fix from the preceding release is retained.
- Observer DNS requests include Accept: application/dns-json. global_fetch_strictly_public enables the intended public Worker probe, separate from service-binding health. The initial monitor returned DNS 405 and public Worker 404; corrected live probes passed. Earlier records remain in D1.

## Monitoring and automation

Cloudflare Cron is installed as */5 * * * *. All triggers run bounded light probes. The top-of-hour invocation is labelled hourly, and midnight UTC additionally observes x402 source; manual audits also include that source observation. Deeper daily D1/authentication/load suites are not implied. Last actual finished_at and FRESH/STALE are exposed; after 15 minutes observations become STALE. Material comparison includes service state/build identities and the x402 source digest; stable observations record NO_MATERIAL_DELTA.

Wolfram independently evaluated the cadence arithmetic: six checks every five minutes imply 1,728 planned probe invocations/day; every minute would imply 8,640. These are workload estimates, not measured billable requests or performance capacity. Five minutes was chosen instead of unnecessary minute polling. Browser refresh occurs once per minute only while the page is visible.

A separate hourly ChatGPT audit creation was attempted and rejected because five of five task slots are occupied. No existing task was changed. Cloudflare Cron installation is independent of that task cap. Distinguish installed schedule from an observed scheduled execution; the checkpoint records what was actually read back. Manual audit execution and persistence were observed.

## Verification

- node regressions.mjs: 6 local authentication/privacy/history/integrity regression groups.
- node method-tests.mjs: 14 local synthetic method checks.
- python http-e2e.py: 9 actual HTTP/D1 fixture groups passed, 14 persisted receipts replayed in this run.
- python integration.py: 5 live inventory/proposal/observer/leaderboard/page groups passed.
- Browser: real titles and SKU-500 present; five roles 800→900; search preserved selections; sixth-card alert preserved five cards and score; dashboard showed live timestamps and scoped HOLDs. Mobile and full accessibility certification were not run.
- All nine deployed module digests matched local source bytes. The large inventory module was hashed before tool-response truncation; truncated response text is not an integrity baseline.

Controllers require local credential files: test-token.private, audit-token.private and curator-token.private. These are intentionally excluded from Git and saved deliverables. Supply authorized dedicated test secrets before replay. HTTP scripts write synthetic attempt/proposal/audit rows only to the dedicated prototype database. Preserve prior output reports before rerunning, since controllers overwrite their local report filenames.

## Remaining gates and scale work

Approved CH-001/002/003 bundles/mappings were not located; only three explicitly synthetic fixtures are validated. The old branch and prior family-game intentions do not authorize manufacturing 500 authored lessons. Production user authentication, consent/child privacy flows, certified learner leaderboard, authored curricula, store apply/rollback reconciliation, x402 facilitator/settlement replay, measured load/cost budgets, queue/backoff policies, and disaster-recovery exercises remain separate work. The current x402 GitHub source describes Base-mainnet payments, but no verified public x402 URL or settlement replay was established by this audit. No funds were accessed or moved.

No raw private Drive source document was published by this build. Earlier proof packages remain unchanged; this is a new versioned checkpoint. Hashes identify artifacts under a trusted baseline, not authority or independent audit certification. The source PR is a draft, not a merged release or an installed GitHub Actions workflow.
