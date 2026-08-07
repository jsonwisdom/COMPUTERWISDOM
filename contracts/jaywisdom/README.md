# JAYWISDOM Revenue Contracts V0.1

This package implements the money-and-receipt rail for `JAYWISDOM_VELOCITY_ARCS_V0.1`.

## Product architecture

```text
CLARITY SERVICE = PRODUCT
USDC PAYMENT    = REVENUE
JWIS            = CAPPED SERVICE REWARD
REPLAY HASH     = VERIFICATION SURFACE
```

The customer purchases one of four products priced in a six-decimal USD stablecoin:

| Service | Price | JWIS reward after fulfillment |
|---|---:|---:|
| CLARITY rubric result | $1 | 1 JWIS |
| ENS enablement lesson | $5 | 5 JWIS |
| Guided RePlay exercise | $10 | 10 JWIS |
| Enablement audit | $25 | 25 JWIS |

Payment is escrowed when an order is created. A designated fulfiller commits a complete CLARITY result before the deadline. Fulfillment atomically:

1. records the CLARITY commitment and result hashes;
2. releases payment to Jay's treasury;
3. mints the capped JWIS reward when cap room remains; and
4. emits human and machine receipt references.

If fulfillment does not occur by the deadline, the customer may reclaim the escrowed payment.

## Security and authority posture

```text
MAINNET_READY               = FALSE
BASE_SEPOLIA_TARGET         = TRUE
UPGRADEABLE                 = FALSE
LEGAL_AUTHORITY_CREATED     = FALSE
ADMIN_CONTROL_CREATED       = TRUE_ON_DEPLOYMENT
INDEPENDENT_AUDIT_COMPLETE  = FALSE
```

The owner may update prices, treasury, fulfiller, rubric version, and fulfillment window. Ownership uses a two-step transfer. The code is intentionally non-upgradeable in V0.1.

`JWIS` does not represent equity, debt, revenue share, legal rights, or a guaranteed market value.

## Build

```bash
cd contracts/jaywisdom
git clone --depth 1 --branch v5.6.1 \
  https://github.com/OpenZeppelin/openzeppelin-contracts.git \
  lib/openzeppelin-contracts
forge fmt --check
forge test -vvv
```

## Base Sepolia deployment

Set public configuration values only:

```bash
export PAYMENT_TOKEN=<BASE_SEPOLIA_USDC_OR_MOCK_ADDRESS>
export JAY_OWNER=<OWNER_ADDRESS>
export JAY_TREASURY=<TREASURY_ADDRESS>
export JAY_FULFILLER=<FULFILLER_ADDRESS>
export RUBRIC_VERSION=$(cast keccak 'JAY_CLARITY_V0_1')
```

Keep signing keys in a Foundry keystore, never in Git.

```bash
forge script script/DeployBaseSepolia.s.sol:DeployBaseSepolia \
  --rpc-url https://sepolia.base.org \
  --account deployer \
  --broadcast
```

Deployment is not authorized by this repository package. A separate human deployment decision and receipt are required.
