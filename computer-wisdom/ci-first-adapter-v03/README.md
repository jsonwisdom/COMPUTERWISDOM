# Computer Wisdom · CI-FIRST Model Adapter v0.3 · Gate A

**DRAFT · MOCK-ONLY · CANON=false · AUTHORITY_CREATED=false.** This is a *runnable, zero-third-party-dependency* Node.js 22 mock provider and verification harness for [CI-FIRST Swarm PR #753](https://github.com/jsonwisdom/COMPUTERWISDOM/pull/753). It does not execute inference, access provider credentials, authorize payments, sign wallets, or deploy. It does **not** prove live Kimi, Grok, 300 agents, or any token-pricing claim.

## Run

```sh
cd computer-wisdom/ci-first-adapter-v03
npm test
npm run demo
```

CI produces an `ci-first-artifacts/mock-adapter-receipt.json` and `mock-ledger-checkpoint.json` and archives both as **mock evidence**. Those outputs must not be interpreted as authenticated external-model traces.

## Contract and trust boundaries

- The six `schema/*.schema.json` files describe v0.3 budget, price, invocation, ledger event, receipt and checkpoint records. `src/contracts.mjs` provides strict mock runtime checks; these are not claims that a general-purpose JSON Schema engine is installed.
- Runtime accepts exactly **one `MockProvider` instance**. The `provider` envelope field must equal `mock`; no network or paid provider adapter is imported.
- Budget authority is a trusted **locally provisioned mock fixture**, not the caller's envelope. The authenticated caller is injected by the test harness and cannot be self-asserted inside the envelope. Envelope caps must exactly match stored record caps, or the request fails. Gate B requires authenticated external identity and a durable authoritative budget service.
- Pricing is an immutable, hashed, server-configured schedule (USD per 1,000 tokens) with source URL, effective range and fetch age ≤24h. This test uses `example.com/mock-pricing-no-claim` as **fictional price data**; no actual vendor pricing is asserted.
- Money is represented as integer **micro-USD** (`1 USD = 1,000,000 micro-USD`). Worst-case reservation uses all input tokens at uncached price and all output tokens at uncached price. Cache savings never justify a smaller reservation in this mock. Decimal prices are strings with six digits precision. JavaScript floating values are rejected in canonical JSON; fractional model parameters must be decimal strings.
- Prompt hash covers `system_prompt` and `user_prompt` in the declared order, parameter hash covers the parameter object, tool allowlist hash covers the sorted allowlist plus full tool schemas. All use sorted-key UTF-8 JSON restricted to safe integer numerics. The prohibited tool-name list blocks sign, wallet, payment, shell, exec patterns, with an empty allowlist in the fixture.
- The journal is append-only `events.jsonl` with a single exclusive filesystem writer lock (`open(wx)`) and `fsync` before dispatch. **A crashed writer leaves a lock and requires human reconciliation, never silent lock stealing.** This design is suitable for Gate A on one shared filesystem only, **not** a distributed/global multi-host budget authority. In the real system, use serializable transactions or compare-and-swap in a separately provisioned budget database.
- Idempotency keys and invocation IDs are unique. Exact retries return the prior receipt or unresolved state; conflicting reuse fails. Journal write failure before DISPATCHED prevents a provider invocation and keeps reserved capacity held.
- Missing usage, changed quote, partial stream, wrong revision/endpoint, or ambiguous dispatch keeps the full reservation held. **Timeout does not release funds.** Expiry release requires both a never-dispatched state and a mock authoritative absence check. No such mock proof is transferable to live provider operations.
- Received response bytes are hashed exactly. A model's self-reported revision remains `unverified` and the receipt's **provenance verdict is UNKNOWN** despite successful cost reconciliation. Mismatch is FAIL. `verified` requires an independent real observer, not present in Gate A.
- Case receipts form an ordered SHA-256 chain from a zero genesis hash. The global journal forms a separate ordered chain. `checkpoint()` computes case heads and journal head; the GitHub CI artifact is an **external copy**, not a cryptographically signed audit authority. Gate B requires a genuinely independent signed/committed anchor plus external reconciliation and verification.

## Fail-closed evidence semantics

A passing test can *correctly observe a FAIL* for tampering or an **UNKNOWN** for model provenance. PASS means the corresponding test assertion was satisfied, **not** that an external model's behavior is verified or a real expenditure is authorized.

**Known deliberate limits:** no immutable third-party invoice or model-build identifier; no provider auth; no external reconciliation credentials; breaker state is in-memory only; no distributed budget service or real service-level deadlines; mock absence proofs only; no self-healing stale lock. Do not promote to Gate B until those controls are implemented independently.

## Gate B and Gate C

See `docs/GATE_B_C_VERIFICATION.md` for exact observer API, trust sources, reconciliation windows, and quantitative benchmark metrics. No automatic promotion, authority creation, signing, or charging is present.
