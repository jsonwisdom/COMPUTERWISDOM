# Base EAS Receipt Registry V0.1

Status: CODE_CANDIDATE_NOT_DEPLOYED  
Networks: Base Sepolia (84532) first, then Base mainnet (8453), selected explicitly  
Authority: NONE  
No Fake Green: TRUE

## Field-count correction

The request was titled "12 Receipt Slots," but the supplied field map contains **14 fields before `logsHash`**. Adding `logsHash` makes the actual schema **15 fields**.

Nothing is silently dropped.

## Canonical EAS schema string

~~~text
uint256 chainId,bytes32 schemaUID,bytes32 attestationUID,bytes32 txHash,uint256 blockNumber,bytes32 blockHash,uint256 transactionIndex,address from,address to,uint256 gasUsed,uint256 cumulativeGasUsed,uint256 effectiveGasPrice,uint8 status,address contractAddress,bytes32 logsHash
~~~

Field semantics:

~~~text
chainId          = chain containing the source transaction; must equal the
                   resolver's CHAIN_ID (8453 Base or 84532 Base Sepolia)
schemaUID        = source EAS schema UID being referenced
attestationUID   = source EAS attestation UID being referenced
txHash           = source transaction hash
blockNumber      = source receipt block number
blockHash        = source receipt block hash
transactionIndex = source transaction index in the block
from             = source transaction sender
to               = source transaction recipient; zero address for contract creation
gasUsed          = source receipt gas used
cumulativeGasUsed= source receipt cumulative gas used
effectiveGasPrice= source receipt effective gas price
status           = 1 success, 0 failure
contractAddress  = created contract or zero address
logsHash         = custom canonical hash of ordered receipt logs
~~~

## Base EAS contracts

~~~text
SchemaRegistry = 0x4200000000000000000000000000000000000020
EAS            = 0x4200000000000000000000000000000000000021
~~~

These are the EAS predeploys. Base and Base Sepolia (both OP Stack chains)
use the same predeploy addresses.

## logsHash definition

Ethereum/Base transaction receipts do not expose a standard `logsHash` field. V0.1 defines it as:

~~~text
logsHash =
keccak256(
  abi.encode(
    tuple(address emitter, bytes32[] topics, bytes data)[]
  )
)
~~~

The tuple array is kept in receipt-log order.

This makes the hash deterministic across clients that use the same normalization.

## Trust-model policy (SHOULD_SET_V0_1)

Every rule below is enforced in code. "Resolver" means
`contracts/jaywisdom/src/BaseReceiptResolverV0_1.sol`.

~~~text
S01 RESOLVER_BINDING_REQUIRED
    Zero-resolver receipt schemas are not supported. registerSchema.ts and
    attestReceipt.ts require RESOLVER_ADDRESS, reject the zero address, and
    verify on-chain that it is a deployed BaseReceiptResolverV0_1 bound to the
    selected chain, the EAS predeploy, this schema string and this lifecycle
    policy before sending anything. A schema registered with any other
    resolver (including zero) has a different UID and fails isReceiptValid
    with WRONG_RECEIPT_SCHEMA.

S02 SOURCE_VALIDITY_MUST_REMAIN_ENFORCED
    Chosen path: a public, permissionless view, receiptStatus(receiptUID) /
    isReceiptValid(receiptUID), which re-reads the receipt AND its source
    attestation from EAS at call time. Once the source is revoked, or
    block.timestamp >= source.expirationTime, the receipt reports
    SOURCE_REVOKED / SOURCE_EXPIRED and isReceiptValid returns false.
    No state-changing invalidation function exists: EAS only lets the
    original attester revoke, so a third party cannot revoke the receipt in
    EAS, and a resolver-side flag would only duplicate what the view derives.
    Consumers MUST use isReceiptValid, not EAS validity alone.

S03 AUTHORIZED_ATTESTER_POLICY
    The receipt attester set is fixed in the constructor (non-empty, no zero,
    no duplicates). There is no admin and no setter. Any other attester
    reverts with UnauthorizedAttester.
    source.attester is NOT constrained (SOURCE_ATTESTER_CONSTRAINED = false):
    the source is constrained only by existence, schema match,
    non-revocation and non-expiry.

S05 BASE_SEPOLIA_PATH
    Chain selection is explicit with no default:
      RECEIPT_REGISTRY_CHAIN=base-sepolia   -> 84532
      RECEIPT_REGISTRY_CHAIN=base           -> 8453, and ALLOW_BASE_MAINNET="true"
    The scripts check the RPC's chain id against the selection. The resolver
    takes its chain id in the constructor (only 8453 or 84532, and it must
    equal block.chainid at deploy) and requires payload.chainId ==
    CHAIN_ID == block.chainid, so a Base deployment never accepts 84532.

S06 RECEIPT_SCHEMA_BINDING
    The resolver requires attestation.schema == RECEIPT_SCHEMA_UID.
    The circular dependency (the schema UID depends on the resolver address)
    is resolved deterministically, with no setter: the constructor computes
      RECEIPT_SCHEMA_UID = keccak256(abi.encodePacked(
          RECEIPT_SCHEMA, address(this), RECEIPT_REVOCABLE))
    which is exactly how the EAS SchemaRegistry derives schema UIDs.
    revoke/multiRevoke also reject attestations from any other schema.

S07 EXPLICIT_RECEIPT_LIFECYCLE_POLICY
    RECEIPT_REVOCABLE       = true  (schema and every attestation)
    RECEIPT_EXPIRATION_TIME = 0     (receipts never carry an EAS expiry)
    The resolver rejects revocable == false and any nonzero expirationTime.
    The scripts take these values from code constants, not the environment,
    and check them against the deployed resolver. Over time, receipt validity
    comes from the S02 source re-check, not from a receipt expiry.

INVARIANTS
    Time source is block.timestamp only; block.number is never used as a
    duration. The payload has no approval flag. Every failed check reverts.
~~~

## Important resolver boundary

The resolver validates at attestation time:

~~~text
attestation.schema == RECEIPT_SCHEMA_UID
attestation.attester is in the constructor-fixed attester set
attestation.revocable == true and attestation.expirationTime == 0
chainId == CHAIN_ID == block.chainid
source schema UID != zero
source attestation UID != zero
attestation.refUID == source attestation UID
source EAS attestation exists
source EAS attestation schema == schemaUID
source EAS attestation is not revoked or expired (now >= expirationTime is expired)
txHash / blockHash / logsHash != zero
status in {0,1}
from != zero
normal-call contractAddress == zero
gasUsed <= cumulativeGasUsed
~~~

The resolver **cannot independently prove** that `txHash`, `blockHash`,
gas fields, status, addresses, or `logsHash` match an arbitrary historical
Base receipt. EVM contracts cannot directly query historical transaction
receipts by transaction hash.

Therefore:

~~~text
RESOLVER_PASS
= STRUCTURE + EAS_REFERENCE CONSISTENCY

RESOLVER_PASS
!= HISTORICAL_RECEIPT_INCLUSION_PROOF
~~~

A stronger future version would need a receipt-inclusion proof, trusted oracle,
or other authenticated execution-layer proof.

## Files

~~~text
src/baseReceiptSchema.ts
src/chainConfig.ts
src/resolverBinding.ts
src/explicitBoolean.ts
src/registerSchema.ts
src/attestReceipt.ts
../../../contracts/jaywisdom/src/BaseReceiptResolverV0_1.sol
../../../contracts/jaywisdom/test/BaseReceiptResolverV0_1.t.sol
~~~

## Install TypeScript dependencies

~~~bash
cd projects/eas/base-receipt-registry-v0-1
npm install
npm run typecheck
~~~

Never commit a private key.

## Build and test the resolver

~~~bash
cd contracts/jaywisdom
forge test -vvv
~~~

The test suite includes a Base Sepolia (84532) path
(`BaseReceiptResolverV0_1SepoliaTest`) alongside the Base (8453) path.

## Deploy the resolver (Base Sepolia first)

The resolver is required. Constructor arguments are the EAS predeploy, the
expected chain id, and the receipt attester set:

~~~bash
cd contracts/jaywisdom
forge create src/BaseReceiptResolverV0_1.sol:BaseReceiptResolverV0_1 \
  --rpc-url "$RPC_URL" \
  --account deployer \
  --broadcast \
  --constructor-args 0x4200000000000000000000000000000000000021 84532 "[0xATTESTER]"
~~~

Use `8453` instead of `84532` for Base mainnet only after the Base Sepolia
path has been exercised and a human has reviewed it. The constructor reverts
if the chain id argument is not 8453/84532 or does not match the chain.

Record the deployed resolver address.

## Register the schema with viem

~~~bash
cd projects/eas/base-receipt-registry-v0-1

export RECEIPT_REGISTRY_CHAIN="base-sepolia"   # or "base" (no default)
# export ALLOW_BASE_MAINNET="true"             # required only for "base"
export RPC_URL="https://..."
export PRIVATE_KEY="0x..."                     # local environment only
export RESOLVER_ADDRESS="0x..."                # required, nonzero

npm run register
~~~

The script:

1. refuses to run without an explicit chain selection, and refuses mainnet
   without `ALLOW_BASE_MAINNET="true"`;
2. refuses a missing, malformed, or zero `RESOLVER_ADDRESS`;
3. checks the RPC chain id against the selection;
4. reads the resolver and checks `EAS`, `CHAIN_ID`, `RECEIPT_SCHEMA`,
   `RECEIPT_REVOCABLE`, `RECEIPT_EXPIRATION_TIME` and `RECEIPT_SCHEMA_UID`;
5. simulates and sends `register(schema,resolver,true)`;
6. waits for confirmation; and
7. reads the schema back and fails if schema, resolver, revocability, or UID differ.

## Make a receipt attestation with viem

~~~bash
export RECEIPT_REGISTRY_CHAIN="base-sepolia"   # or "base" + ALLOW_BASE_MAINNET="true"
export RPC_URL="https://..."
export PRIVATE_KEY="0x..."                     # must be an authorized attester
export RESOLVER_ADDRESS="0x..."
export RECEIPT_SCHEMA_UID="0x..."              # must equal resolver RECEIPT_SCHEMA_UID
export SOURCE_SCHEMA_UID="0x..."               # referenced source EAS schema
export SOURCE_ATTESTATION_UID="0x..."          # referenced source EAS attestation
export SOURCE_TX_HASH="0x..."                  # transaction receipt to encode

npm run attest
~~~

The script verifies the resolver binding, checks that `RECEIPT_SCHEMA_UID` is
registered with that resolver, checks that the signer is an authorized
attester, fetches the receipt, computes `logsHash`, ABI-encodes all 15 fields
in schema order, sets EAS `refUID` equal to the source attestation UID,
uses the fixed lifecycle policy (`revocable = true`, `expirationTime = 0`),
simulates the EAS call, sends it, waits for the transaction, extracts the
new attestation UID from the EAS `Attested` event, and reports
`isReceiptValid` for it.

## Check a receipt later (S02)

~~~bash
cast call "$RESOLVER_ADDRESS" "isReceiptValid(bytes32)(bool)" "$RECEIPT_UID" --rpc-url "$RPC_URL"
cast call "$RESOLVER_ADDRESS" "receiptStatus(bytes32)(uint8)" "$RECEIPT_UID" --rpc-url "$RPC_URL"
~~~

`receiptStatus` codes: 0 VALID, 1 RECEIPT_NOT_FOUND, 2 WRONG_RECEIPT_SCHEMA,
3 UNAUTHORIZED_ATTESTER, 4 RECEIPT_REVOKED, 5 RECEIPT_EXPIRED,
6 SOURCE_NOT_FOUND, 7 SOURCE_REVOKED, 8 SOURCE_EXPIRED.

## Revocability and expiration (S07)

~~~text
schema revocable       = true (fixed; part of RECEIPT_SCHEMA_UID)
attestation revocable  = true (enforced by the resolver)
attestation expiration = 0    (enforced by the resolver)
~~~

Revocation means "superseded / no longer valid", not erasure. Only the
original attester can revoke, via EAS. Append-only history should still
preserve the old UID and the correction link.

## One-button mainnet page: removed

`register-one-button.html` was removed in repair round 1. It registered a
zero-resolver schema on Base mainnet (S01), showed "Registered" before
on-chain confirmation, loaded a third-party script from unpkg without SRI,
and would have been auto-published to GitHub Pages on merge. There is no
browser registration path in V0.1. The Pages workflow (`static.yml`) also
excludes this whole directory from the published artifact.

## State

~~~text
SCHEMA_REGISTERED       = FALSE
RESOLVER_DEPLOYED       = FALSE
ATTESTATION_SUBMITTED   = FALSE
CODE_GENERATED          = TRUE
AUTHORITY_CREATED       = FALSE
NO_FAKE_GREEN           = TRUE
~~~
