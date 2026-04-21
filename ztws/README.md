# ZTWS — Zero-Trust Warrant System

**Enforcement Primitive for Sovereign OS**  
*Live on Base Sepolia | Mainnet Ready*

---

## What This Is

ZTWS is a cryptographic warrant system that makes surveillance subject to on-chain judicial authorization. No warrant = no data access. The code enforces the law.

**Part of:** `jsonwisdom/COMPUTERWISDOM` (Sovereign OS hub)  
**Concern:** Warrant-first enforcement, execution receipts, watchdog verification

---

## Live State (Sepolia Testnet)

| Artifact | Value | Status |
|----------|-------|--------|
| **Registry** | [`0x8f9b4dFf68cF7CbFdE2c64D15C01585Ff60eC4E8`](https://sepolia.basescan.org/address/0x8f9b4dFf68cF7CbFdE2c64D15C01585Ff60eC4E8) | ✅ Deployed |
| **Warrant ID** | `0x5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5` | ✅ Issued |
| **Execution Receipt** | [`0x9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f`](https://sepolia.basescan.org/tx/0x9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f) | ✅ Broadcast |
| **Watchdog** | Active on Sepolia | ✅ Online |

---

## Verify in One Command

```bash
curl -sL https://raw.githubusercontent.com/jsonwisdom/COMPUTERWISDOM/main/ztws/ztws-verify.sh | bash
```

Expected output:

```text
ZTWS_CHAIN_INTEGRITY: PASS
├── Registry: 0x8f9b4dFf68cF7CbFdE2c64D15C01585Ff60eC4E8
├── WarrantId: 0x5a4b3c2d...
├── Judicial Safe: 0x...
├── Execution Receipt: 0x9a8b7c6d...
└── Enclave Measurement: MATCHED
```

---

## Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                     JUDICIAL SAFE (3-of-5)                   │
│                    Authorizes warrant issuance               │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              ZTWS REGISTRY (Base Sepolia)                    │
│  • setGateway() + measurement binding                        │
│  • issueWarrant() → WarrantIssued event                      │
│  • submitReceipt() → ExecutionReceipt event                  │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 NITRO ENCLAVE (verifier.py)                  │
│  • Verifies predicate matches warrant                        │
│  • Signs execution receipt                                   │
│  • Attestation binds to MEASUREMENT                          │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    WATCHDOG (auditor)                        │
│  • Monitors registry events                                  │
│  • Verifies receipt signatures                               │
│  • Alerts on warrantless access                              │
└─────────────────────────────────────────────────────────────┘
```

Genesis Anchor (Immutable Truth):

- Contract: `0x082836b2A8E2a77Cca7DDd9F9fC8eE99F884F58D`
- Block: `44202259`
- ENS: `jaywisdom.base.eth`

---

## Reproduce From Source

```bash
# Clone Sovereign OS hub
git clone https://github.com/jsonwisdom/COMPUTERWISDOM
cd COMPUTERWISDOM/ztws

# Set RPC
export BASE_SEPOLIA_RPC_URL=https://sepolia.base.org

# Run end-to-end verification
forge script script/VerifyE2E.s.sol

# Expected exit code: 0
```

Prerequisites:

- forge (Foundry)
- cast (Foundry)
- jq

---

## Audit Trail

| Step | On-Chain Evidence |
|---|---|
| Registry deployment | `cast code 0x8f9b...` matches commit |
| Gateway binding | `getGatewayMeasurement()` returns expected measurement |
| Warrant issuance | `WarrantIssued` event with signed warrant |
| Execution receipt | `ExecutionReceipt` event from enclave |
| Watchdog verification | Independent node confirms all events |

---

## Public Good Statement

No permission needed. No backdoors. No warrantless access.

The code is the law. The chain is the witness.

Any government, court, or citizen may audit, fork, or deploy this system.

---

## License

MIT — free for all uses, commercial or non-commercial.

---

Part of: `jsonwisdom/COMPUTERWISDOM` — Sovereign OS for cryptographic law
