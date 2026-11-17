# CW TPM Attestor v0.1 — CI-FIRST

**Status:** SOURCE-CANDIDATE / REVIEW-ONLY until cross-platform CI builds.
**Scope:** Windows 11 Home x64, TPM 2.0, Windows Platform Crypto Provider.
**No TPM changes by default.** This project is not an accredited certificate authority.

Uses the [Google go-attestation](https://github.com/google/go-attestation) library
(v0.6.4, Apache-2.0) and Windows PCP API. Source + build evidence go to GitHub
Actions; no credentials, TPM private keys, wallet data or BitLocker keys go to GitHub.

## Architecture / commands

* `cw-tpm-v1-windows-amd64.exe probe` — **read-only** TPM capability inspection. Reports
  the TPM vendor and PCR bank count, with `signed_quote_verified=false`.
* `cw-tpm-v1-linux-amd64 challenge --out nonce.json` — independent **verifier** creates a
  random 160-bit challenge and a 5-minute validity window; refuses overwrite. Keep the
  original challenge on the verifier. Transfer a copy to the Windows client over a
  trusted channel.
* `cw-tpm-v1-windows-amd64.exe enroll --allow-create-ak --out ak.opaque` — **explicit**
  opt-in that creates a persistent Windows PCP attestation key (AK). This modifies the
  Windows TPM key store, but does **not** clear TPM, flash BIOS, change BitLocker or
  install root trust. Don't run without explicit review and approval. The opaque
  handle file must remain private; the key persists on this machine.
* `cw-tpm-v1-windows-amd64.exe quote --ak ak.opaque --challenge nonce.json --out quote.json`
  — loads the AK, signs a TPM2 quote with the verifier's nonce, reads PCRs and collects
  the current TCG measurement log. Writes locally, refuses overwrite.
* `cw-tpm-v1-linux-amd64 verify --challenge nonce.json --evidence quote.json --out verified.json --spent-dir private-spent`
  — on a **separate verifier host**, checks nonce, quote signature, signed PCR
  contents, and measured-boot log replay. Consumes each nonce once. This is a
  cryptographic proof **relative to the supplied AK public key**; it cannot yet
  establish that this AK was made by a manufacturer-trusted TPM.

## Important trust boundaries

1. **Creating an AK is a persistent TPM action** — deliberately disabled unless
   `--allow-create-ak` is set. If creating an AK or saving its opaque handle fails,
   do not attempt repeated random provisioning; inspect the first error.
2. A signed quote verified using an **untrusted embedded public key** can be
   fabricated by ordinary software. A valid quote **cannot certify a PC** until
   EK-to-AK binding via credential activation / independently authenticated
   certificate chain and approved PCR policy are established. The verifier
   correctly reports these as UNKNOWN even after cryptographic checks PASS.
3. `--trusted-ak-sha256` can pin a previously enrolled public AK key hash,
   but it **does not establish** EK-to-AK binding or external certification.
4. The original 5-minute challenge, verification and nonce-spent ledger must be
   maintained by the independent verifier. If `--spent-dir` is absent,
   replay prevention remains UNKNOWN.
5. TPM event logs, PCR measurements, AK public key and evidence might identify
   device configuration and are **PRIVATE BY DEFAULT**. Review and redact before
   any public issue, commit, DNS TXT, IPFS upload, or email.
6. Never paste wallet seeds, TPM private materials, BitLocker recovery keys or
   Windows device serial numbers into chat or CI logs.
7. We do not install AMDTPM roots to make `UntrustedRoot` disappear. The user's
   previously observed `UntrustedRoot` and kernel DMA OFF remain unresolved.
8. Windows PCP support is less mature than Linux; a **successful Go cross-compile
   does not prove runtime interoperability on this particular PC**.

## Build (developer review, not first user action)

Windows uses Go 1.24+:
```powershell
cd tools/cw-tpm-attestor-v1
go mod tidy
go test ./...
go build -o cw-tpm-v1-windows-amd64.exe .
```
The Actions build additionally produces a Linux verifier and SHA-256 manifest.
It is **not code-signed**. Do not bypass Windows SmartScreen or policy blocks.

## Readiness ladder

| Gate | Required evidence | State before PC run |
|---|---|---|
| Source in GitHub draft PR | exact commit + file integrity | Candidate |
| Windows cross-compile + negative tests | GitHub Actions logs | UNKNOWN |
| Live Windows read-only probe | `probe` output | UNKNOWN |
| Fresh verifier challenge | independently issued nonce | UNKNOWN |
| User-approved AK creation / persisted handle | local successful `enroll` | NOT AUTHORIZED YET |
| TPM2 quote signature | `quote` blob + `verify` | UNKNOWN |
| PCR/event log replay | verifier checks | UNKNOWN |
| EK/AK identity chain, trusted AMD root | remote EK credential activation and trusted roots | UNKNOWN |
| Boot policy / external certification | independent accredited verifier | UNKNOWN |

**CI-FIRST verdicts:** PASS, FAIL, UNKNOWN. No fake green.
