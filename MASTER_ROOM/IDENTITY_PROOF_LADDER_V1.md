# MASTER ROOM IDENTITY PROOF LADDER V1

## Purpose

Separate identity display, namespace resolution, wallet control, signatures, attestations, and authority.

## Current observed evidence

### ENS / Base names

Declared identity surfaces:
- jaywisdom.eth
- jaywisdom.base.eth

Expected identity controller recorded in repo:
- 0xa380552a27b0a5a2874ea7aa52cac09f542002e8

### Legacy Computer Wisdom anchor

FINAL_ANCHOR_TOPOLOGY_v1.md currently records:
- state = ENS_POINTER_PREPARED_NOT_WRITTEN
- EAS attestation = submitted
- EAS network = base-sepolia
- ENS = optional discovery prepared
- mainnet_anchor = false

Therefore:
ENS_POINTER_PREPARED != ENS_RECORD_WRITTEN
EAS_WITNESS != ENS_ANCHOR
TESTNET_WITNESS != MAINNET_IDENTITY_PROOF

### Wallet binding receipt

receipts/wallet_binding_v2.md currently records:
- STATUS = PREPARED_NOT_SIGNED
- SHOW_WALLET_PROOF = PENDING

Therefore:
DECLARED_CONTROLLER != SIGNED_CONTROL_PROOF

### ENS / Chain Voice repo

jsonwisdom/ENS README currently describes:
- Base mainnet chain id 8453
- Base EAS control-proof flow
- expected controller 0xa380552a27b0a5a2874ea7aa52cac09f542002e8
- deployment status BLOCKED_PENDING_PAGES_ENABLEMENT

Therefore:
CODE_READY != DEPLOYED
DEPLOYED != TRANSACTION_CONFIRMED
TRANSACTION_CONFIRMED != ENS_RECORD_WRITTEN

## Proof ladder

I0 DISPLAYED_NAME
I1 FORWARD_RESOLUTION_VERIFIED
I2 REVERSE_PRIMARY_VERIFIED
I3 CONTROLLER_SIGNATURE_VERIFIED
I4 EAS_ATTESTATION_VERIFIED
I5 ENS_TEXT_RECORD_POINTER_VERIFIED
I6 MASTER_ROOM_OPERATOR_SESSION_BOUND

Master Room may report only the highest rung independently proven in the current replay.

## Non-collapse

ENS_NAME != PERSON
ENS_RESOLUTION != CONSENT
WALLET_CONTROL != GLOBAL_AUTHORITY
SIGNATURE != TRANSACTION
TRANSACTION != ATTESTATION
ATTESTATION != LEGAL_AUTHORITY
BIOMETRIC_UNLOCK != PUBLIC_BIOMETRIC_STORAGE

## Current status

CURRENT_PROVEN_RUNG_FROM_REPO_EVIDENCE = I0_PLUS_DECLARED_CONTROLLER_AND_TESTNET_EAS_RECEIPT
I1_LIVE_FORWARD_RESOLUTION = NOT_PROVEN_IN_THIS_GITHUB_ONLY_PASS
I2_REVERSE_PRIMARY = NOT_PROVEN_IN_THIS_GITHUB_ONLY_PASS
I3_CONTROLLER_SIGNATURE = HOLD
I4_EAS_TESTNET_WITNESS = REPO_RECORDED
I5_ENS_TEXT_RECORD_POINTER = HOLD_NOT_WRITTEN_PER_CANONICAL_TOPOLOGY
I6_MASTER_ROOM_OPERATOR_SESSION_BOUND = DESIGN_NOT_IMPLEMENTED

NO_FAKE_GREEN = TRUE


## External witness check — 2026-09-23

Public EAS explorer verification observed:

### Sepolia witness

UID:
0x23b3b97514fa232cfdbcdee7a5031ff11a5fcd36aa874a5f4067805cd0ad6c84

Observed state:
- created 2026-05-16
- expiration: never
- revoked: no
- attester: 0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5
- transaction: 0x4cef493d67d8744d2458fd82c169aa872b14cfe2ecaf13f03329b57bd93acc35
- raw boundary includes "not ENS anchored yet"

### Base mainnet evidence-only witness

UID:
0xed2eed117f8b888d597910ed88cda166217babfcdcfc54e4c70b02a49ee2dc25

Observed state:
- chain: Base
- attester: 0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5
- recipient / subject address: 0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8
- subject identity text: jaywisdom.eth / jaywisdom.base.eth
- attester role: delegated_recorder
- authority model: EVIDENCE_ONLY
- boundary explicitly does not claim jaywisdom.base.eth signed the schema freeze

### Current identity conclusion

EAS_WITNESS_EXISTS = PROVEN_EXTERNALLY
BASE_EAS_SUBJECT_BINDING_RECORD_EXISTS = PROVEN_EXTERNALLY
CONTROLLER_SIGNATURE_BY_0xA380... = NOT_PROVEN_BY_THESE_ATTESTATIONS
ENS_FORWARD_RESOLUTION = STILL_HOLD
ENS_REVERSE_PRIMARY = STILL_HOLD
ENS_TEXT_POINTER_WRITTEN = CONTRADICTED_BY_CURRENT_CANONICAL_TOPOLOGY (PREPARED_NOT_WRITTEN)

Do not collapse a delegated recorder's attestation into controller signature proof.


## Witness / controller membrane

The identity ladder MUST preserve this hard membrane:

WITNESS SIDE
- EAS_WITNESS_EXISTS
- BASE_EAS_SUBJECT_BINDING_RECORD

CONTROLLER SIDE
- ENS_FORWARD_RESOLUTION
- ENS_REVERSE_PRIMARY
- CONTROLLER_SIGNATURE
- MASTER_ROOM_OPERATOR_SESSION_BOUND

WITNESS_SIDE != CONTROLLER_SIDE

A delegated recorder may establish that a witness record exists and names a subject.
A delegated recorder cannot, by that act alone, establish that the subject controlled the named key, signed the declaration, consented to the declaration, or authorized a Master Room session.

EAS_EXISTS != IDENTITY_PROVEN
SUBJECT_NAMED != SUBJECT_SIGNED
ATTESTER_SIGNATURE != CONTROLLER_SIGNATURE
