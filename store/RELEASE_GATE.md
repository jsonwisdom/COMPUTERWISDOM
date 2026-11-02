# CWaaS Order-to-Delivery Implementation — STAGING / HOLD

Files: `store/cwaas-reconcile-worker.mjs`; D1 `cwaas_orders_staging` (Cloudflare account). This code is prepared for separate review: it is **not** currently deployed as the live Flywheel settlement server.

## Provenance and boundaries
- Website PR #726: `jsonwisdom/COMPUTERWISDOM`.
- Payment-rail PR #8: `jsonwisdom/flywheel-of-wisdom`. Existing $1 routes unaffected.
- Cloudflare staging worker `cwaas-order-gate-staging` remains a read-only HOLD worker.
- D1 table `orders` now has `payer_address`, `report_body`, `download_token_sha256` in addition to existing receipt/order fields.

## Security contract
- Admin-only POST `/internal/orders` creates a unique order bound to the specified paying wallet. Must require server-side `ADMIN_TOKEN`.
- Admin-only POST `/internal/reconcile` takes order ID plus Base transaction hash; checks real JSON-RPC `eth_chainId` = 8453, successful receipt, minimum block confirmations, exactly one Base USDC Transfer of 89,000,000 units from the pre-bound payer to owner-approved payee. Unique `settlement_tx` and conditional D1 update reject duplicate mapping.
- Admin-only POST `/internal/deliver` accepts a **real operator-provided completed research report**, hashes/stores the JSON in D1 and issues a one-time-created random download capability; it refuses unpaid orders. A customer can GET `/report/:order_id` with `x-cwaas-delivery-token` header; returned SHA-256 must match stored report.
- `/health` and `/release` expose staging status only. No public checkout or payment request created.
- All state mutation is blocked without `ADMIN_TOKEN`, `BASE_RPC_URL`, verified `PAY_TO`, and `MIN_CONFIRMATIONS`. Secrets must be injected at deployment, never committed.
- The deployed staging Worker is still the earlier read-only HOLD implementation. The new Worker source is a proposal only until reviewed and separately deployed.

## Verification still required before release
1. Ensure RPC is trustworthy and independently verify USDC token and recipient address. ENS is a label, not sufficient authorization.
2. Run syntactic/type tests, mocked RPC negative scenarios (wrong chain, missing tx, failure receipt, insufficient confirmations, wrong payer, wrong contract, wrong value, wrong recipient, duplicate tx, double report delivery).
3. Validate auth rejection and token-only report access. Inspect data-retention and privacy rules for potentially sensitive customer reports.
4. Integrate official x402 facilitator proof and durable order correlation, rather than treating generic token transfer as synonymous with an x402 authorization.
5. Prove actual report content creation/quality and customer handoff, not just JSON storage.
6. Independently replay a specifically authorized real settlement and fulfillment before live release.

**Disposition: HOLD / not independently verified / no production settlement enablement.**
