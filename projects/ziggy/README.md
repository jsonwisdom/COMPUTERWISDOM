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
- **Repository / system identity:** `jsonwisdom/COMPUTERWISDOM`
- **Preservation layer:** `BoxD`
- **Intelligence label:** `100th Intelligence`
- **Source commit:** `5aa886746ec08adcbbbad2c5f758b64324066d66`
- **BoxD release payload SHA-256:** `ad22599ef68bca96af1328ed0ab60cc0ff488af21db1139db954098400146447`
- **Release manifest:** `projects/ziggy/ziggy-release-v0.1.json`
- **On-chain status:** signature required / not submitted

### COMPUTERWISDOM boundary

GitHub is the host and transport for this public release. It does not replace the repository/system identity.

`COMPUTERWISDOM` must remain explicit in Ziggy receipts, signer messages, manifests, and replay paths as:

`repository = jsonwisdom/COMPUTERWISDOM`

User-supplied signer claim:

`0x73ad550dcb47d254a5b3c335ae39d8999c42ff12`

Current verification state:

`USER_SUPPLIED_UNVERIFIED`

The address must not be promoted to verified operator control merely because it was supplied in conversation. Verification requires an actual wallet signature from that address over the bounded Ziggy release message. See `computerwisdom-signer-binding-v0.1.json`.

## Directories-first control architecture

Ziggy's next control layer is intentionally directory-first:

- [`DIRECTORY_MAP.md`](./DIRECTORY_MAP.md)
- [`natural-language/`](./natural-language/)
- [`identity/`](./identity/)
- [`ens/`](./ens/)
- [`voice/`](./voice/)
- [`imagination/`](./imagination/)
- [`profiles/ziggyprime/`](./profiles/ziggyprime/)
- [`lessons/wisconsin/`](./lessons/wisconsin/)
- [`github-control/`](./github-control/)
- [`launches/main/`](./launches/main/)
- [`test-runs/base-sepolia/`](./test-runs/base-sepolia/)
- [`receipts/`](./receipts/)
- [`replay/`](./replay/)

Natural language may propose. ENS may resolve. Voice may transcribe. Imagination may sandbox. Applied profiles may extend bounded skills. Lessons may exercise those skills. GitHub may gate. The human remains the promotion authority.

Address claims are preserved without inference in [`ens/claims.v0.1.json`](./ens/claims.v0.1.json), including:

- `0x73ad550dcb47d254a5b3c335ae39d8999c42ff12`
- `0xa380552a27b0a5a2874ea7aa52cac09f542002e8`

Both are currently `USER_SUPPLIED / UNVERIFIED / UNASSIGNED`; their relationship is `UNDEFINED` until cryptographic evidence says otherwise.

## Applied profile: ZiggyPrime

`ZIGGYPRIME` is Ziggy's advanced applied-skill profile for public-source provenance work. It is not a new character, identity, operator, or authority.

`ZIGGYPRIME = QUESTION + NAVIGATE + MEASURE + COMPARE + REPLAY`

With LeahPrime's bounded classifier/explainer rail:

`LEAHPRIME = CLASSIFY + GAP_CHECK + EXPLAIN + ROUTE + HOLD`

Applied cross:

`ZIGGYPRIME × LEAHPRIME = CHILD_PROVENANCE_ENGINE`

See [`profiles/ziggyprime/README.md`](./profiles/ziggyprime/README.md) and [`lessons/wisconsin/WISCONSIN_LESSON_002_FOLLOW_THE_DOLLAR_V0_1.md`](./lessons/wisconsin/WISCONSIN_LESSON_002_FOLLOW_THE_DOLLAR_V0_1.md).

## Human signature gate

### Current signer — v0.2

**https://jsonwisdom.github.io/COMPUTERWISDOM/projects/ziggy/sign-v0.2.html**

Signer v0.2 removes the injected-provider dead end while preserving the same Ziggy v0.1 release boundary:

- uses an injected EIP-1193 provider when one is actually present
- otherwise creates an EIP-1193 provider with the official Base Account SDK browser build
- pins `@base-org/account` to `2.5.7` for replayability
- targets Base Sepolia (`84532`)
- uses `personal_sign` over the explicit Ziggy release message
- records which provider path was used
- compares the connected signer address with the user-supplied address claims without promoting ownership
- creates a downloadable JSON signature receipt
- leaves signature verification as `NOT_PERFORMED` until independently checked
- does **not** call `eth_sendTransaction`, submit EAS, spend gas, or invent an attestation UID / transaction hash

### Preserved signer — v0.1

`sign-v0.1.html` remains preserved as the injected-only implementation that exposed the iPhone / in-app-browser compatibility gap. It is not the current recommended signing surface.

For the iPhone compatibility history and current path, read:

**[WALLET_SIGNING_IOS.md](./WALLET_SIGNING_IOS.md)**

A wallet connection is a separate state from a wallet signature, and a signature is separate from an on-chain attestation:

`PUBLISHED ≠ PRESERVED ≠ CONNECTED ≠ SIGNED ≠ ATTESTED`

Canonical purpose:

> ZIGGY = a bounded reasoning companion that helps a child explore possibilities while preserving originals, exposing missing information, respecting parent-defined boundaries, and making the reasoning path replayable.

No chain attestation is claimed until a wallet signature and transaction receipt are independently verified.

## Version rule

v0.1 is preserved as the first prototype. Later implementations improve by explicit revision rather than overwriting provenance.
