# Base EAS Receipt Registry V0.1

Status: CODE_CANDIDATE_NOT_DEPLOYED  
Network: Base mainnet  
Chain ID: 8453  
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
chainId          = chain containing the source transaction; Base mainnet is 8453
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

These Base addresses are the EAS predeploys.

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

## Important resolver boundary

The resolver validates:

~~~text
chainId == 8453 == block.chainid
source schema UID != zero
source attestation UID != zero
attestation.refUID == source attestation UID
source EAS attestation exists
source EAS attestation schema == schemaUID
source EAS attestation is not revoked or expired
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
src/registerSchema.ts
src/attestReceipt.ts
../../../contracts/jaywisdom/src/BaseReceiptResolverV0_1.sol
../../../contracts/jaywisdom/test/BaseReceiptResolverV0_1.t.sol
~~~

## Install TypeScript dependencies

~~~bash
cd projects/eas/base-receipt-registry-v0-1
npm install
~~~

Never commit a private key.

## Deploy the resolver

The resolver is optional. If you want a zero-resolver schema, register with the
zero address.

To use the custom resolver, build from the existing Foundry package:

~~~bash
cd contracts/jaywisdom
forge test -vvv
~~~

Deploy on Base mainnet only after human review:

~~~bash
forge create src/BaseReceiptResolverV0_1.sol:BaseReceiptResolverV0_1 \
  --rpc-url "$BASE_RPC_URL" \
  --account deployer \
  --constructor-args 0x4200000000000000000000000000000000000021
~~~

Record the deployed resolver address.

## Register the schema with viem

~~~bash
cd projects/eas/base-receipt-registry-v0-1

export BASE_RPC_URL="https://..."
export PRIVATE_KEY="0x..."                 # local environment only
export RESOLVER_ADDRESS="0x..."            # or zero address
export SCHEMA_REVOCABLE="true"

npm run register
~~~

The script:

1. simulates the call;
2. sends `register(schema,resolver,revocable)`;
3. waits for confirmation;
4. computes the deterministic schema UID;
5. reads the schema back from the registry; and
6. fails if schema, resolver, revocability, or UID differ.

## Make a receipt attestation with viem

~~~bash
export BASE_RPC_URL="https://..."
export PRIVATE_KEY="0x..."                  # local environment only
export RECEIPT_SCHEMA_UID="0x..."           # new 15-field registry schema
export SOURCE_SCHEMA_UID="0x..."            # referenced source EAS schema
export SOURCE_ATTESTATION_UID="0x..."       # referenced source EAS attestation
export SOURCE_TX_HASH="0x..."               # transaction receipt to encode
export ATTESTATION_REVOCABLE="true"

npm run attest
~~~

The script fetches the Base receipt, computes `logsHash`, ABI-encodes all
15 fields in schema order, sets EAS `refUID` equal to the source attestation
UID, simulates the EAS call, sends it, waits for the transaction, and extracts
the new attestation UID from the EAS `Attested` event.

## Revocability

~~~text
schema revocable = true
→ individual attestations may opt into revocation

schema revocable = false
→ attestations under that schema cannot be revoked
~~~

For correction-oriented receipts, `true` is appropriate when your governance
model treats revocation as "superseded / no longer valid" rather than erasure.

Append-only history should still preserve the old UID and the correction link.

## State

~~~text
SCHEMA_REGISTERED       = FALSE
RESOLVER_DEPLOYED       = FALSE
ATTESTATION_SUBMITTED   = FALSE
CODE_GENERATED          = TRUE
AUTHORITY_CREATED       = FALSE
NO_FAKE_GREEN           = TRUE
~~~
