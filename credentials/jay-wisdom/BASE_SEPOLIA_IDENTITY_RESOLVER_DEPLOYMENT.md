# Base Sepolia Identity Resolver Deployment Runbook

Status: `PREPARED_NOT_DEPLOYED`
Target: `IdentityBindingResolver`
Network: `Base Sepolia` (`chainId = 84532`)

## Locked deployment parameters

```text
EAS                = 0x4200000000000000000000000000000000000021
SchemaRegistry     = 0x4200000000000000000000000000000000000020
EXPECTED_ATTESTER  = 0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5
```

The deployment script hard-codes the chain ID, EAS address, and expected attester. It does not read or store a private key.

Script:

```text
contracts/jaywisdom/script/DeployIdentityResolverBaseSepolia.s.sol
```

## Security rule

Use an encrypted Foundry keystore for Base Sepolia. Do not paste a raw private key into the repository, a command transcript intended for publication, or a GitHub issue/PR.

Example local keystore creation:

```powershell
cast wallet import jsonwisdom-base-sepolia --interactive
```

## PowerShell deployment sequence

From repository root:

```powershell
Set-Location .\contracts\jaywisdom

$env:BASE_SEPOLIA_RPC_URL = "https://sepolia.base.org"
$env:FOUNDRY_ACCOUNT = "jsonwisdom-base-sepolia"

# Gate 1: confirm RPC chain before doing anything else.
$chainId = cast chain-id --rpc-url $env:BASE_SEPOLIA_RPC_URL
if ($chainId -ne "84532") { throw "FAIL_CLOSED: expected Base Sepolia chainId 84532, got $chainId" }

# Gate 2: compile and run the full local suite.
forge test -vvv

# Gate 3: dry run only. No --broadcast flag.
forge script .\script\DeployIdentityResolverBaseSepolia.s.sol:DeployIdentityResolverBaseSepolia `
  --rpc-url $env:BASE_SEPOLIA_RPC_URL `
  --account $env:FOUNDRY_ACCOUNT `
  -vvvv
```

Only after the dry run succeeds and the deploying account has Base Sepolia ETH:

```powershell
forge script .\script\DeployIdentityResolverBaseSepolia.s.sol:DeployIdentityResolverBaseSepolia `
  --rpc-url $env:BASE_SEPOLIA_RPC_URL `
  --account $env:FOUNDRY_ACCOUNT `
  --broadcast `
  -vvvv
```

Capture from the broadcast output before any next transition:

```text
DEPLOYER_ADDRESS=
IDENTITY_RESOLVER_ADDRESS=
DEPLOY_TX_HASH=
BLOCK_NUMBER=
CHAIN_ID=84532
```

Do not commit Foundry `broadcast/` output. It is intentionally ignored by git.

## Post-deployment fail-closed verification

Set the deployed address only after obtaining it from the broadcast receipt:

```powershell
$env:IDENTITY_RESOLVER_ADDRESS = "0x..."
```

### V1 — Runtime bytecode exists

```powershell
$code = cast code $env:IDENTITY_RESOLVER_ADDRESS --rpc-url $env:BASE_SEPOLIA_RPC_URL
if ($code -eq "0x" -or [string]::IsNullOrWhiteSpace($code)) {
  throw "FAIL_CLOSED: no runtime bytecode at resolver address"
}
```

### V2 — Immutable expected attester matches

```powershell
$actualAttester = cast call $env:IDENTITY_RESOLVER_ADDRESS `
  "expectedAttester()(address)" `
  --rpc-url $env:BASE_SEPOLIA_RPC_URL

$expectedAttester = "0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5"
if ($actualAttester.ToLower() -ne $expectedAttester.ToLower()) {
  throw "FAIL_CLOSED: expectedAttester mismatch"
}
```

### V3 — Resolver is non-payable

```powershell
$isPayable = cast call $env:IDENTITY_RESOLVER_ADDRESS `
  "isPayable()(bool)" `
  --rpc-url $env:BASE_SEPOLIA_RPC_URL

if ($isPayable -ne "false") { throw "FAIL_CLOSED: resolver unexpectedly payable" }
```

### V4 — Source verification

After V1-V3 pass, attempt source verification separately:

```powershell
forge verify-contract $env:IDENTITY_RESOLVER_ADDRESS `
  .\src\IdentityBindingResolver.sol:IdentityBindingResolver `
  --chain 84532 `
  --rpc-url $env:BASE_SEPOLIA_RPC_URL `
  --guess-constructor-args `
  --watch
```

If source verification does not succeed, record `SOURCE_VERIFIED=FALSE` and stop promotion until the discrepancy is resolved. A successful transaction alone is not enough to advance to schema registration under this runbook.

## Required deployment receipt

After verification, create a receipt containing only public deployment facts:

```json
{
  "network": "base-sepolia",
  "chain_id": 84532,
  "resolver": "0x...",
  "deploy_tx_hash": "0x...",
  "deployer": "0x...",
  "eas": "0x4200000000000000000000000000000000000021",
  "expected_attester": "0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5",
  "runtime_code_present": true,
  "expected_attester_verified": true,
  "is_payable": false,
  "source_verified": true,
  "identity_schema_registered": false,
  "authority_created": false
}
```

No key material, RPC credentials, keystore passwords, or seed phrases belong in the receipt.

## State gate

```text
DEPLOYMENT_PREPARED             = TRUE
IDENTITY_RESOLVER_DEPLOYED      = FALSE
IDENTITY_SCHEMA_REGISTERED      = FALSE
ATTESTATION_CREATED             = FALSE
AUTHORITY_CREATED               = FALSE

NEXT_AFTER_VERIFIED_DEPLOYMENT  = CAPTURE_RESOLVER_ADDRESS
```

This runbook authorizes preparation only. It does not authorize a broadcast transaction by itself.
