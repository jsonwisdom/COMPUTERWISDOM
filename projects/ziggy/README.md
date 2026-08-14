# Ziggy — Quantum RePlay v0.1

Status: prototype / sanitized public implementation concept  
Authority created: false

Ziggy is a bounded AI-enabled family tool represented as a square handheld 2D object.

## Roles

- **Child:** explorer / creator
- **Parent:** boundary authority
- **Ziggy:** reasoning assistant inside the corridor
- **BoxD:** preserved original
- **Mind the Gap:** missing metadata/context detector
- **GirlMath:** mandatory non-compensatory gate
- **RePlay:** output-to-origin trace
- **Ziggy Print:** optional physical-output feature

## Core flow

`IDEA → MAKE → BOXD → ASK ZIGGY → GIRLMATH → MIND THE GAP → PARENT CONTROL → REPLAY → OPTIONAL PRINT`

## Privacy boundary

This public branch must contain no child identity, private family photos, face data, home addresses, or private family metadata. Public examples are fictional/sanitized. AI inference never silently becomes family history.

## Family-memory model

`PHOTO ↔ PERSON ↔ PLACE ↔ DATE ↔ EVENT ↔ ART ↔ STORY`

Every edge requires provenance and a permission state. Missing edges remain unknown.

## Release identity

- **Operator:** `jaywisdom.eth`
- **Preservation layer:** `BoxD`
- **Intelligence label:** `100th Intelligence`
- **Source commit:** `5aa886746ec08adcbbbad2c5f758b64324066d66`
- **BoxD release payload SHA-256:** `ad22599ef68bca96af1328ed0ab60cc0ff488af21db1139db954098400146447`
- **Release manifest:** `projects/ziggy/ziggy-release-v0.1.json`
- **On-chain status:** signature required / not submitted

## Human signature gate

Live GitHub Pages signer:

**https://jsonwisdom.github.io/COMPUTERWISDOM/projects/ziggy/sign-v0.1.html**

The signer is deliberately bounded:

- connects an injected EVM wallet
- requires Base Sepolia (`84532`) before signing
- uses `personal_sign` over an explicit Ziggy release message
- binds the BoxD payload hash, source commit, repository, operator label, network target, timestamp, and `authority_created=false`
- creates a downloadable JSON signature receipt
- does **not** call `eth_sendTransaction`, submit EAS, spend gas, or claim an attestation UID / transaction hash

A wallet signature is a separate state from an on-chain attestation:

`PUBLISHED ≠ PRESERVED ≠ SIGNED ≠ ATTESTED`

Canonical purpose:

> ZIGGY = a bounded reasoning companion that helps a child explore possibilities while preserving originals, exposing missing information, respecting parent-defined boundaries, and making the reasoning path replayable.

No chain attestation is claimed until a wallet signature and transaction receipt are independently verified.

## Version rule

v0.1 is preserved as the first prototype. Later versions improve by explicit revision rather than overwriting provenance.
