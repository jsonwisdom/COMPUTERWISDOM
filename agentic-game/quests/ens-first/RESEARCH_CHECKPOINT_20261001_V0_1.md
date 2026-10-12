# ENS First — research checkpoint 2026-10-01

Record: ENS_FIRST_RESEARCH_CHECKPOINT_20261001_V0_1
Classification: RESEARCH_NOTE / NON_CANONICAL_GAMIFICATION
Authority created: false
Quest points awarded: 0

## GitHub observation before this appendix

PR: https://github.com/jsonwisdom/COMPUTERWISDOM/pull/591
Observed head: d8c8ba640ded4c409f233f8b65aadf5ab1aa66da
Observed state: open, draft=true, merged=false, merged_at=null.
Four existing added files under agentic-game/quests/ens-first/: board.mjs, board.test.mjs, quests.json, README.md.

The current connector returned eight completed successful pull-request workflow runs on its first page, including Agentic Game Receipt Renderer. The supplied report describes ten successful check runs. Workflow runs and check runs are different objects and denominators. This record does not claim complete coverage.
No local tests were rerun for this documentation appendix. The four passing local tests belong to the earlier board build.
A new appendix commit changes the head; old-head successes do not establish success on the new head.
No quest is completed by CI success, this research note, or its storage.

## Protocol sources retrieved this turn

- ENSIP-15: https://docs.ens.domains/ensip/15/
- Registry: https://docs.ens.domains/registry/ens/
- ENSIP-3: https://docs.ens.domains/ensip/3/
- ERC-1271: https://eips.ethereum.org/EIPS/eip-1271
- Reverse registrar reference: https://docs.ens.domains/registry/reverse/

These are retrieved page text, not immutable captures with source-byte hashes. No registry RPC was called. No name-specific ownership was checked.

## Normalization boundary

ENSIP-15 is final, authored by raffy.eth, created April 3, 2023. The retrieved page lists Unicode 17.0.0 and describes normalization as living.
Normalization precedes hashing and is idempotent. Leading/trailing whitespace may be trimmed for convenience; inner input must not be otherwise preprocessed. ASCII case mapping belongs to the algorithm, not a separate blanket lowercase step.
Tokenization handles text and emoji, NFC applies to text, and normalized emoji output strips FE0F. Validation uses script groups, combining-mark restrictions and whole-script confusable data.
Beautification is a display operation, separate from normalized hashing input.
spec.json and nf.json provide the data tables. Neither was fetched here. The supplied September 9, 2025 date and 4febc8f5d285cbf80d2320fb0c1777ac25e378eb72910c34ec963d0a4e319c84 hash remain reported and unverified. Searches did not find those strings in the retrieved ENSIP-15 page.
The detailed confusable examples in the supplied narrative remain explanatory reported material; no table-based execution was run. Passing normalization does not guarantee visual distinctness in every font.

## Registry and namehash boundary

The registry documentation describes owner, resolver and TTL, with getters and authorized update methods. It describes the root ownership chain through ENS Root and the ENS DAO wallet; current contract ownership was not read onchain.
The supplied registry address and ownership-address values are not independently verified by this appendix. ENSv2 deployment status was not established here.

For already-normalized labels:
namehash("") = 32 zero bytes
labelhash(label) = Ethereum Keccak-256(UTF-8 label)
namehash(label.parent) = Keccak-256(namehash(parent) || labelhash(label))

Ethereum Keccak-256 must not be replaced by standardized SHA3-256. Hashing computes a node; it does not read a registry.
The supplied eth and ens.eth numeric vectors remain reported. A local replay attempt could not import Crypto.Hash.keccak; no numeric replay was completed.
The addr.reverse parent node in the supplied narrative matches the literal in the retrieved ENSIP-3 example; that comparison is not a registry lookup.

## Reverse-name correction

For the ENSIP-3 address-specific reverse node:
namehash("<40 lowercase hexadecimal address digits>.addr.reverse")
Remove the 0x prefix. Hashing ".addr.reverse" omits the address and is not the address-specific lookup.
namehash("addr.reverse") identifies the parent, not an account's reverse result.
Record the reverse name and a forward match separately. For multichain primary names, bind the applicable standard and chain/coin type; do not assume the v1 Ethereum reverse path covers every chain.
No reverse name for a user wallet was queried here.

## Control-proof corrections and scope

Resolution target, name-management authority, and signer can differ. A session-key signature requires its delegation scope to be established; a session key is not automatically the name controller.
An EOA signature verifies the exact message under the declared signing scheme. Typed-data domain, hash algorithm and message bytes matter. Smart-contract wallets require applicable contract signature validation, such as ERC-1271, rather than EOA recovery alone.
The proposed challenge-review fields are message, repository, name, chain, nonce, expiration and signer. They are a learning checklist, not a complete implemented verifier.
Nonce inclusion alone does not prevent replay. The verifier must issue/bind the challenge and enforce nonce uniqueness/consumption, audience/domain scope and expiration.
A wallet proof does not independently establish ENS management authority or GitHub account control. Those require separate scoped checks at recorded block/time context.

## Preserved state

NAME_INPUT = jaywisdom.eth (label only)
NORMALIZATION_EXECUTED = FALSE
NAMEHASH_REPLAY = NOT_COMPLETED
ENS_FORWARD_QUERY = NOT_RUN
ENS_REVERSE_QUERY = NOT_RUN
SIGNATURE_REQUEST = NONE
SIGNATURE_VERIFICATION = NOT_RUN
ENS_CONTROL = UNRESOLVED
GITHUB_ACCOUNT_WALLET_BINDING = NONE
QUEST_LEDGER_CHANGE = NONE
LEARNING_POINTS_AWARDED = 0
ENS_TRANSACTION = NONE
MERGE_ACTION = NONE
TRADE_ACTION = NONE

## Next evidence needed for ENS_MAP

Capture normalized input with pinned normalizer/data version, chain, block/hash, registry/resolver context, forward answer, reverse answer and forward-confirmation result. Preserve failures and missing records distinctly. A learning review may then discuss the receipt; the board still does not authenticate it.
