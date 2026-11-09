# CI-FIRST Quadruple Onion Standard v1
2026-11-09 · Base chain 8453 · no ETH registration

Required verdicts are PASS / FAIL / UNKNOWN, per-scope. Never automatically promote an unresolved check.

ONION 1 / PIXELS: Preserve original screenshots, file hashes, size, timestamps, visible labels and buttons. Separate what is actually visible from interpretation. Screenshots cannot prove onchain state.

ONION 2 / AUTHORITY: Independently check connected account, chain, origin, name/controller roles, exact message, expiry and consent. EIP-191 proves a scoped message, not ENS/Basename or Coinbase smart-wallet authority. The project's requested new operator/destination is 0x65891F97db01C8fC9F76f4DFE65Bd44F8261f1B0; funded A380 remains historical.

ONION 3 / CRYPTO: Recover the actual EIP-191 address from the original signature and message using an independent cryptographic library, with negative tests for altered bytes, signer, chain, nonce, origin and dates. Hash the exact JSON receipt. A locally random nonce is NOT globally one-time until a verifier issues and consumes it. For a contract signer, test ERC-1271/6492 separately.

ONION 4 / RECONCILIATION: Check source commit, workflow test results, deployed Cloudflare version and actual browser readback, and any blockchain changes via chain ID, block hash, transaction receipt and independent replay. No payment or ENS status may be asserted from an offchain signature.

NO FALSE GREEN: An aggregate PASS requires all four scoped gates to pass; synthetic test signatures are not Jason's signatures. Record FAILs as repair tasks; leave historical originals unchanged.

Screenshot pair:
- IMG_6506.png SHA256 64dc5c204b82ad91cb325719da872ae533911138a106c5571e846a89f18170f2, 1170x2532.
- IMG_6507.png SHA256 aa5a210c25454f7cc4436fe5f68f1af81744960c59ebf7d2a391529dbdd3d790, 1170x2532.

Observed: Sign button enabled; Save/Copy JSON disabled; prepared message names A380 as historical and 0x6589 as future Base Play/Build. No completed signature shown. Critically, "one-time declaration" is overstated because only locally generated random nonces exist. The evidence pane misleadingly shows generic review text instead of "Awaiting signature." Independent signature recovery is absent from deployed page.

ENSv2 already supports fine-grained ROLE_SET_ADDRESS at resolver root or coin-type 60, see https://docs.ens.domains/ensv2/permissioned-resolver/ . A Base message signature does not grant that role or change mainnet ENS records. Upgrading our verifier is appropriate; altering ENS protocol is not necessary to support permissions.

Cloudflare before repair: cw-base-play-sign-20261109 version 87b0a14f-1490-45d0-b0df-7615e9c79e8e. GitHub source blob SHA 668c38b18ab90648158c158bb6b46ed87ddd79ba.
