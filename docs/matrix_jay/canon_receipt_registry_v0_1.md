# Matrix Jay Canon Receipt Registry V0_1

## Doctrine
Receipts are the source. Signals are the overlay. Replay is the judge.

## V0_1 Deprecation and Migration Protocol
NOTICE: V0_1 IS SCAFFOLD ONLY.

CanonReceiptRegistryV0_1 is a non-cryptographically bound evidence registry.
It records append-only witness events and overlay signals.

Identity Status: DEFERRED.
No EIP-712 signature verification is implemented.
V0_1 requires msg.sender == receipt.actor for audit trail only.

Security Warning:
V0_1 events are unverified witness data. Indexers must not treat submitter
identity as protocol-authenticated. The `actor` field reflects the transaction
sender, not a cryptographic proof of intent.

Migration Goal:
V0_2 supersedes V0_1 with anchorSignedReceipt(...) and EIP-712 typed-data
signature recovery for non-repudiable Canon receipts.

V0_1 remains valid as historical evidence, not identity-bound proof.
Authority remains false.

## Invariants
- I1: Append-only. No receipt deletion or mutation. Only new receipts via anchorReceipt.
- I2: Trinity before verdict. AL!=NONE, JOY!=NONE, CW==APPEND_ONLY required.
- I3: Authority false. No authority flips in V0_1. All receipts observer-only.
- I4: Verdicts blocked. Status VERIFIED, FALSE, FRAUD, ADJUDICATED revert on anchor.
- I5: Genesis locked_once. setGenesis required before anchoring. First receipt must match genesis.

## Repo Precedent Compliance
- AL #147: Schema-first. V0_1 freezes receipt format before chains.
- COMPUTERWISDOM #31: Disputes as overlays. CanonSignal does not mutate receipts.
- COMPUTERWISDOM #40: No bypass. No receipt, no gate pass, no action. All actions emit events.
- COMPUTERWISDOM #29: Observer-only. Authority false. Evidence-only. No conclusions.

## Usage
1. Deploy CanonReceiptRegistryV0_1
2. Call setGenesis(0x0b58518ad17b73252be9a5fbfef7d74d8dc57254)
3. Actors call anchorReceipt with msg.sender == receipt.actor
4. Any address may call emitCanonSignal on existing receipts
5. Off-chain replay indexes ReceiptAnchored + CanonSignalEmitted events

## Membrane
HOLDS. Observer-only posture. Evidence, never conclusions. No identity binding.
