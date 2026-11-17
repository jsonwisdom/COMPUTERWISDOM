# CI-FIRST Dual Front — draft, 2026-11-09

No TPM command, wallet signature, payment, DNS change, EAS submission, or Cloudflare deployment is authorized by this draft.

## Front A: ENS + EAS evidence
- Inspect Ethereum mainnet `jaywisdom.eth` and Base mainnet `jaywisdom.base.eth` **separately**, at pinned block heights and RPC endpoints.
- Preserve original DNS/ENS resolver, owner, controller, address, chain ID, transaction hash and event evidence. Require independent chain replay. Never infer owner from an attestation's recipient.
- EAS Base schema #1535 attestation `0xed2eed117f8b888d597910ed88cda166217babfcdcfc54e4c70b02a49ee2dc25` names both identities but explicitly limits authority to evidence-only validator status.
- EAS Base `0x0e60a3cc445f273d8af207cbec821d45f4731f2eeca04b02e5d01553847c4d93` refers to historic 0xA380 address and PR #314, with Authority Claimed=false.
- Existing merged COMPUTERWISDOM PR #745 records *historical* EIP-191 proof for PC 0x65891F97db01C8fC9F76f4DFE65Bd44F8261f1B0. This does NOT confer ENS or current wallet control.
- Do not merge historical A380 / current Basename resolution with PC Wallet2 0x6589. Onchain identity ownership, wallet signing, TPM provenance and operator approval are four distinct checks.

## Front B: hardware attestation
- Input original EK/intermediate/root DER bytes; independently rehash and compare fingerprints, verify signature chain, appropriate AMD trust anchor, validity, revocation. **A hash string alone is insufficient.**
- Verifier issues 32 cryptographically random bytes, unique challenge ID, 300s expiration, atomic single use; records AK Name and EK public key.
- After explicit human authorization, existing Windows TPM performs EK-to-AK credential activation; independent verifier compares recovered secret in constant time.
- Separately verify fresh TPM2_Quote (SHA256 PCR0–7 where supported), signed nonce, AK public key and measured-boot event log. Detect wrong AK/EK, replay/expiry/tamper/software stand-in.
- Do not create persistent TPM keys, modify firmware, clear TPM, export secrets, change BitLocker or initiate wallet signing in this draft.

## Aggregate policy
PASS only when each mandatory gate has original independently replayed evidence. FAIL when a test has observed contradictory evidence. UNKNOWN for uncollected/not-executed checks. No 'HOLD' as evidence classification; human deployment approval is a separate control.
No production change, payments, funds, signing, EAS publication or DNS mutation. On-chain publishing would require separate consent and transaction receipt.
Reference: private Drive COMPUTER_WISDOM_ALMS_PC_SIGNER_PROOF_GATE_V2_2026-11-09; review-only CI_FIRST_PC_TPM_REVIEW_2026-11-09.json.
