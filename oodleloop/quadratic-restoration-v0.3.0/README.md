# OODLELOOP / COMPUTER WISDOM — Quadratic Architecture Restoration v0.3.0

## Restored rails (based on original repository sources)

- `jaywisdom.eth`: **secure-by-design private identity, governance, confidential source/IP and recovery metadata rail**. This is an architectural role, not proof that the ENS name itself secures any device or account.
- `jaywisdom.base.eth`: **public-by-design** Base execution, discovery, publication, receipt links and deterministic replay rail. “Unsecure” means **publicly observable**, not unprotected or vulnerable.
- `jsonwisdom/AL`: replay/receipt substrate; `jsonwisdom/COMPUTERWISDOM`: observability / cockpit / operations. Explicit links only.
- Jason Wisdom has operational authority over his builds. Broad local AI creation and test capability is enabled. External signing, spending, identity/security changes and consequential publication require scoped human permission.

## Non-conflation

- The `0x65891F97...1f1B0` PC-wallet EIP-191 receipt does **not** certify A380 ownership.
- `0xA380552a...002E8` A380 historical access incidents are independent of the PC-wallet evidence.
- `receipts/wallet_binding_v2.md` explicitly states `PREPARED_NOT_SIGNED`. It is **not** proof that the two names are actively cryptographically bound to A380.
- Ethereum mainnet ENS and Base names are separate identity registries; naming conventions do not establish onchain control or security.
- GitHub success is evidence a job completed, not a proof of secure live custody.

## Quadratic evidence matrix

For each candidate relation between two identity/evidence nodes, collect **source → assertion → receipt → independent check → outcome**. Four nodes yield 4×3/2 = **6 pairwise edges**. Missing edges are scoped missing evidence, never a reason to freeze unrelated builds.

Nodes: human intent, `.eth` identity, `.base.eth` public identity, wallet-signing evidence.

## Run locally

```bash
python3 audit.py architecture.json
python3 -m unittest test_audit.py -v
```

Read-only, stdlib-only; no network calls, credentials, transactions or deployments.

## Source anchors retrieved from GitHub

- https://github.com/jsonwisdom/COMPUTERWISDOM/blob/master/docs/jaywisdom/JAYWISDOM_VELOCITY_ARCS_V0_1.md
- https://github.com/jsonwisdom/COMPUTERWISDOM/blob/master/docs/layered-machine-speed-scale-blueprint-v0-1.md
- https://github.com/jsonwisdom/COMPUTERWISDOM/blob/master/docs/base_has_purpose_v0_1.md
- https://github.com/jsonwisdom/COMPUTERWISDOM/blob/master/receipts/wallet_binding_v2.md

## Jason Command Center and v0.3.1 owner scaffolds

- `OWNER_POLICY.json`: declarative ownership and permission policy. Jason Wisdom is the human command authority; JSONWisdom is the draft-branch builder/tester. This file does not change GitHub account ownership or prove private-key control.
- `quadratic_edges.json`: four nodes and exactly six *candidate* pairwise identity relationships. All six are `UNKNOWN` pending independent cryptographic/onchain verification; architectural roles are not cryptographic attestations.
- `quadratic.py`: deterministic standard-library-only six-edge and governance invariants; `test_quadratic.py`: ten regression tests (including six edge subtests), in addition to six existing tests.
- `command_center.html`: local read-only dashboard. It refreshes public GitHub PR and master status when internet access is available. This is not a deployed or hosted web application; no server is deployed.
- `OWNER_INTENT_MESSAGE.txt`: optional EIP-191-compatible personal-sign *message text* scoped solely to declaring operator intent. **Not required to build.** It is not a wallet-name binding, funds authorization, or proof of who controls a key. The HTML UI can copy the message and, if a trusted browser wallet is available, request a personal signature and save a receipt **locally**; it does not upload the signature.
- `.github/workflows/ci-first-quadratic.yml`: read-only branch/PR CI. No deployments or spending.

Windows PowerShell — run from the scaffold folder after checking out this PR branch:

```powershell
python -m unittest -v test_audit test_quadratic
python audit.py architecture.json
python quadratic.py
Start-Process .\command_center.html
```

**Evidence boundary:** 16/16 regression tests passing means *the code and invariant checks* pass. It does not mean six identity links are verified. The PC EIP-191 historical receipt remains message-specific; A380 remains independently unresolved; dual-name binding remains `PREPARED_NOT_SIGNED`.

**Release policy:** Keep PR #773 draft. No merge into `master`, external publication, identity change, token transfer, account modification or deployment without Jason's explicit scoped authorization. Development and testing continue without signing or blanket HOLD.
