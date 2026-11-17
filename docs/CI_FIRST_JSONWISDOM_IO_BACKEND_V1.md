# JSONWisdom.IO backend — CI-FIRST deployment candidate
Date: 2026-11-08. Source of record: jsonwisdom/COMPUTERWISDOM.

Observed original Cloudflare config: proof.jsonwisdom.io and seymour.jsonwisdom.io share jasons-dns-burden-of-proof with .com. supreme.jsonwisdom.io shares seymour-supreme-public with .com. Both source Workers contain zero environment bindings.

The original public code was read directly from authenticated Cloudflare Worker script downloads and copied byte-for-byte to proof-origin.mjs and supreme-origin.mjs. Their hashes and byte counts are in backend-contract.json. Do not substitute a similarly named GitHub file.

The proof/seymour .io copy is jw-io-proof-seymour-v1. The supreme .io copy is jw-io-supreme-v1. Both are NEW, distinct script services, not replacement of current .com Workers. The wrappers preserve the existing applications and expose the read-only /.well-known/ci-first-backend.json identity endpoint for runtime evidence.

CI-FIRST sequence: (1) verify source SHA-256 and byte counts; (2) syntax and smoke tests; (3) upload new scripts WITHOUT rebinding any production hostname; (4) read back versions and test identity; (5) prepare exact .io-only route switch and rollback, separately approved after verified runtime results; (6) run the live Cloudflare domain mapping gate, which fails closed if mappings still share .com services.

Important: .com and .io will still be in ONE Cloudflare account. Separate Worker IDs do not prove independent Cloudflare provider failure domain, failover, storage, load-balancer health checks, R2 availability or x402 settlement. Those gates stay UNKNOWN/FAIL per observation.

No Base signing, wallets, secrets, payments, DNS changes, .com Worker modification, automatic promotion, PR merge, or authority creation. CANON=false; AUTHORITY_CREATED=false.
