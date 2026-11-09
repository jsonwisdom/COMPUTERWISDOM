# CI-FIRST · Model Adapter v0.3 · Gate B & C release boundary

**Design specification only. Gate A implementation does NOT satisfy these real-provider requirements.**

## Gate B: source of truth and independent observer

1. **Authoritative budget record**: a server-side table keyed by `budget_context_id`, storing `owner`, authenticated caller scopes, agent caps, global cap, currency in integer micro-USD, creation/expiry, and administrator-approved authorization. A caller cannot modify this table by sending an envelope. Authenticate with short-lived identities bound to an exact audience and validated against an identity issuer; verify owner delegation explicitly and reject mismatches. No wallet or payment authorization in this service.
2. **Serializable reservation**: one global writer or a database transaction/compare-and-swap that atomically checks all active holds + reconciled spend before appending. Distributed agents must share that same authoritative ledger. Journal records include `budget_remaining_micro_usd`, reservation TTL, event signature/commit revision, and replayable chain hashes. Local process locks are insufficient for Gate B.
3. **External provider request**: capture provider-issued request ID, authenticated endpoint, model requested/reported revision, provider attestation where available, raw request/response hashes and actual usage. Accept revision as `verified` *only* when a separate signed provider attestation or a separately credentialed observer confirms the exact build; an echoed model string remains `unverified`.
4. **Independent observer interface** (read-only; separate credentials from dispatch): `observe({invocation_id, idempotency_key, provider_request_id, provider, time_window})` → `{observation_id, provider_event_status, model_revision_attestation, usage_input_tokens, usage_output_tokens, provider_charge_micro_usd, source_url, fetched_at, evidence_sha256, observer_identity}`. Observer MUST independently query provider records and compare against the locked price schedule, budget ledger and receipt chain; never simply echo dispatch-system data. Evidence hash alone does not establish authenticity.
5. **Reconciliation**: define `reconciliation_window_seconds=86400` as an initial bounded review interval (policy proposal, not provider guarantee). `NOT_FOUND` is not sufficient if the provider's records may be eventually consistent. Require a trusted provider idempotency lookup after the provider's retention/consistency horizon with authenticated negative result, plus no provider request ID, before non-dispatch release. Otherwise retain `UNKNOWN_COST` through window expiry and escalate for manual reconciliation. **Never automatically release a possibly dispatched reservation on timeout or TTL alone.**
6. **Price version**: quote is pinned with currency, token units, cache rate, effective period, source, fetched-at, issuer and collection method. A mid-flight mismatch is `UNKNOWN_COST` until independent reconciliation; never silently reprice. Timestamp comparison needs a declared tolerance and clock source.
7. **Receipt integrity**: case-specific ordered genesis root (`000...0`) + `prev_receipt_sha256` with no fork, periodic global checkpoint and independent signed/external anchor. Verify the original received stream bytes, `stream_completed`, `response_truncated`, actual usage and provider ID. Attestation must bind receipt hash to observer evidence, not just copy its body.
8. **Breakers**: record state in the authoritative shared store. Configuration `(failure_count, window_ms, open_ms, reset_mode, half_open_probe_count=1)` must be versioned; no silent reset after crash. Three deadline types: connect, first-byte and total. Retry only if idempotent provider response evidence prevents double spending; no retries on auth, exhausted budget or price mismatch.
9. **Security**: strict separate identities, no accessible wallet/signing credentials, no payment transports, allowlisted tools only. Ensure request/response source bytes stay private with separate access controls; publish hashes and minimal receipts rather than sensitive prompts.

Gate B PASS requires a separately provisioned observer and durable source of truth, independently replayed for: known success, provider mismatch, missing usage, ambiguous dispatch, duplicate ID, price drift, truncated response, ledger write failure, circuit open, restart, and provider-record absence. Gate B remains **UNKNOWN** until those live records exist.

## Gate C: benchmark measurements (NOT judgments)

For identical audited case sets, randomize case order and measure both one-agent and eight-agent modes under the same output-quality rubric, budget policy and hardware/provider constraints. Predeclare primary metrics and confidence intervals:

- `latency_p50_ms` and `latency_p95_ms`, per-case wall clock.
- `cost_micro_usd_per_case` from independently reconciled usage/bills, not estimated price tables.
- `input_tokens_per_case`, `output_tokens_per_case`, and `cached_input_tokens_per_case`.
- `failure_rate` and `unknown_rate`, counting all attempted cases including timeouts and rejected dispatches.
- `source_attribution_accuracy` and `verifier_disagreement_rate`, against human-reviewed held-out cases.

No claim of “5× cheaper,” improvement, or independent failover without real samples, error bars, and a recorded comparison. Reproducibility requires immutable case hashes, parameter hashes and observer-backed model revision evidence.

**CANON=false · AUTHORITY_CREATED=false · Gate B UNKNOWN · Gate C UNKNOWN.**
