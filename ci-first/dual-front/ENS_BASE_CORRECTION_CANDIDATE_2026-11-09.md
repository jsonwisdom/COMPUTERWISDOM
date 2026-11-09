# CI-FIRST — ENS and Base attestation correction candidate
Date: 2026-11-09. Status: DRAFT ONLY / READ-ONLY / NO TRANSACTIONS.

## Established evidence
1. The two names `jaywisdom.eth` and `jaywisdom.base.eth` were read through Blockscout and each resolved to `0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8` at query time. This is **resolution evidence**, not evidence of ownership or signer control. Provider/block snapshot not yet pinned in that read.
2. GitHub `CI_FIRST_BASE_BATCH_2026-11-07.json` contains the full original message, EIP-191 signature, expected PC signer `0x65891F97db01C8fC9F76f4DFE65Bd44F8261f1B0`. GitHub `CI_FIRST_BASE_RECEIPT_2026-11-07.json` records historical signer PASS, but not current session control, ENS ownership or chain tx authorization.
3. EAS attestation references and historical 0xA380 address must remain separate from PC operator signer proof. Existing hardware EK certificate fingerprints do not establish a PC-to-wallet or PC-to-ENS link.
4. One human/project may assert multiple credentials, while each credential's control and permissions are tested separately. No external identity service is granted ultimate authority by this candidate.

## Proposed correction WITHOUT changing ownership
- Keep existing ENS resolution and ownership records unchanged pending registry/resolver and access checks.
- Add *off-chain* evidence links in the append-only CI ledger that say (a) both ENS names observed resolving to A380; (b) PC operator evidence historic EIP-191 verified for 0x6589; (c) TPM manufacturer EK trust and fresh AK quote not yet verified.
- If the intended desired forward address for either ENS name differs from the recorded A380 address, record it as a **requested target**, not as a fact, and require an approved, name-controller-signed resolver transaction and independently confirmed receipt.
- If the intended update is an EAS attestation tying the ENS record, operator signer and hardware evidence together, create *new* scoped attestation only after verifying (a) the attester/recipient roles, (b) signed authority for each claim, (c) subject ENS registry entries, and (d) actual TPM trust proof; no rewrite of historical attestations.
- Never silently replace name ownership, smart-contract wallet controller, payment recipient, Base builder code or delegated operator roles.

## Automated gates (all read-only first)
A1 Record chain ID, RPC endpoint, block height/hash for Ethereum ENS and Base Basename separately.
A2 Read registry owner, resolver, TTL, text records, address records, expiry/wrapper contract state, reverse mapping; reproduce via second independent provider.
A3 Decode matching EAS UIDs, schema ID, attester, recipient, reference UID, revoked/expiry state, tx receipt and indexed block.
A4 Re-run independent EIP-191 signature recovery from exact bytes already committed; preserve message/signature and repo commit SHA.
B1 Independently validate original TPM EK DER chain to authenticated AMD trust root and revocation.
B2 Independently verify verifier-issued EK-to-AK activation and AK quote after separate explicit owner approval.
C1 Produce canonical JSON observations and SHA-256 evidence manifest, with provenance and no implied human identity certification.
C2 Human approval of exact proposed ENS record/attestation write, fees and target contract before any chain transaction.

## CI-FIRST
Observed resolution = PASS. Recorded historical PC EIP-191 = PASS (historical receipt, independent recheck pending).
Owner/resolver/reverse/expiry and any currently valid name-controller signature = UNKNOWN.
Actual live ENS/Base changes = NOT EXECUTED.
No signing, spending, TPM operation or production deployment authorized by this text.
