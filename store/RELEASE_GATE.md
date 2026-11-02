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
- Optional `facilitator_proof` object is accepted (scaffold). When `REQUIRE_FACILITATOR_PROOF=true` it becomes mandatory. On-chain USDC remains ground truth.
- Admin-only POST `/internal/deliver` accepts a **real operator-provided completed research report**, hashes/stores the JSON in D1 and issues a one-time-created random download capability; it refuses unpaid orders. A customer can GET `/report/:order_id` with `x-cwaas-delivery-token` header; returned SHA-256 must match stored report.
- `/health` and `/release` expose staging status only. No public checkout or payment request created.
- All state mutation is blocked without `ADMIN_TOKEN`, `BASE_RPC_URL`, verified `PAY_TO`, and `MIN_CONFIRMATIONS`. Secrets must be injected at deployment, never committed.
- The deployed staging Worker is still the earlier read-only HOLD implementation. The new Worker source is a proposal only until reviewed and separately deployed.

## Negative-path test matrix (required before release)

| Case | Expected result |
|------|-----------------|
| Missing / invalid ADMIN_TOKEN | 401 UNAUTHORIZED |
| Wrong chain ID | 422 WRONG_RPC_CHAIN |
| Missing / failed receipt / wrong tx hash | 422 NOT_SETTLED |
| Insufficient confirmations | 409 CONFIRMATIONS_PENDING |
| Wrong payer address | 422 PAYMENT_MATCH_FAILED |
| Wrong recipient (PAY_TO) | 422 PAYMENT_MATCH_FAILED |
| Wrong USDC contract or amount | 422 PAYMENT_MATCH_FAILED |
| Multiple matching transfers | 422 PAYMENT_MATCH_FAILED |
| Same tx mapped to second order | 409 DUPLICATE_SETTLEMENT_OR_DB_FAILURE or RECONCILIATION_CONFLICT |
| Reconcile already verified order | 409 ALREADY_VERIFIED |
| Deliver unpaid order | 409 PAYMENT_NOT_VERIFIED |
| Deliver twice | 409 DELIVERY_CONFLICT |
| Report GET without / wrong token | 403 NOT_AUTHORIZED |
| Tampered report body | 503 INTEGRITY_FAILURE |
| Facilitator proof invalid / wrong network / tx mismatch (when provided or required) | 422 FACILITATOR_* |
| Public POST to payment endpoints | 503 PAYMENT_DISABLED |

## Verification still required before release
1. Establish externally reachable HTTPS endpoints (Custom Domain or confirmed workers.dev).
2. Ensure RPC is trustworthy and independently verify USDC token and recipient address. ENS is a label, not sufficient authorization.
3. Run the negative-path matrix above (mocked RPC + real staging).
4. Replace facilitator scaffold with official x402 facilitator `/verify` + order-specific correlation. On-chain check remains final ground truth.
5. Prove actual report content creation/quality and customer handoff, not just JSON storage.
6. Independently replay a specifically authorized real settlement and fulfillment before live release.

**Disposition: HOLD / not independently verified / no production settlement enablement.**
