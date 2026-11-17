# Computer Wisdom · CI-FIRST Eight-Agent Replay Harness

**State:** DRAFT, offline and deterministic. **CANON=false · AUTHORITY_CREATED=false**.

Eight explicit JavaScript agent roles: **intake → provenance → mathematics → contradiction → safety → replay → synthesis → supervisor**. Six independent audit roles run in a bounded fan-out (maximum concurrency 4); synthesis consumes all six signed-by-digest *data handoffs*; an independent supervisor validates seven handoff hashes and stops unsupported promotion. SHA-256 is an integrity digest, **not** a cryptographic signature or identity attestation.

## Run

Node.js 22+, no dependencies, network permissions or API keys.

```bash
npm test
npm run replay
node src/cli.mjs fixtures/io-worker-separation.json --expect FAIL --output audit-receipt.json
```

The fixture intentionally contains a **FAIL** for shared `.io` / `.com` Worker service IDs, a **PASS** for proposed separate script IDs, and **UNKNOWN** for live runtime verification. Those classifications are derived from *historical fixture bytes*, not live authenticated Cloudflare observation. The CI suite expects the known FAIL as a passing diagnostic test, not a deployment green light.

## Contract

Every agent emits `{status, verdict, confidence, sources, findings, memory_updates, sha256, canon:false, authority_created:false}`. The shared memory is typed into **facts**, **decisions with rationale**, and **open questions**. The first six roles all read a frozen case; results merge in a defined order, so concurrent writes cannot silently rewrite evidence. Evidence source bytes and each handoff carry SHA-256 digests. Sources are tagged `historical_fixture`, and **production_verification remains UNKNOWN**.

No paid model is invoked. These are deterministic specialized verification agents, **not 300 external Kimi K3 inference workers**. The next distinct, explicitly approved gate would be model adapters with strict cost ceiling, secure tool sandbox, request/response provenance and measured single-agent vs 8-agent benchmark. Neither the “5× cheaper” claim nor live Grokbot integration is established.

## CI-FIRST safety gates

- `PASS`, `FAIL`, `UNKNOWN` only. Never promote fixture PASS to live PASS.
- No shell execution from model text; no networking or API secrets.
- Reject SHA mismatches, forged handoffs, unauthorized flags, unsupported rules, missing sources, malformed memory.
- No wallet operations, payment authorization, ENS transfers, Cloudflare production routing changes or GitHub auto-merge.
- One isolated draft PR; independent CI receipts before any deployment.
