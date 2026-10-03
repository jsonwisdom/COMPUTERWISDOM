import {
  createPublicClient,
  createWalletClient,
  http,
  parseEventLogs,
  zeroAddress,
  type Hex,
} from "viem";
import { privateKeyToAccount } from "viem/accounts";
import {
  EAS_ADDRESS,
  RECEIPT_EXPIRATION_TIME,
  RECEIPT_REVOCABLE,
  SCHEMA_REGISTRY_ADDRESS,
  easAbi,
  encodeReceiptData,
  receiptResolverAbi,
  receiptToFields,
  schemaRegistryAbi,
} from "./baseReceiptSchema.js";
import {
  assertConnectedChain,
  requireBytes32,
  requireEnv,
  requireNonzeroResolver,
  selectReceiptRegistryChain,
} from "./chainConfig.js";
import { verifyResolverBinding } from "./resolverBinding.js";

// S05: explicit chain selection, no default, mainnet needs ALLOW_BASE_MAINNET="true".
const selected = selectReceiptRegistryChain();
// S01: the receipt schema must be bound to a nonzero resolver.
const resolver = requireNonzeroResolver(process.env.RESOLVER_ADDRESS);

const privateKey = requireEnv("PRIVATE_KEY") as Hex;
const rpcUrl = requireEnv("RPC_URL");
const receiptSchemaUID = requireBytes32("RECEIPT_SCHEMA_UID");
const sourceSchemaUID = requireBytes32("SOURCE_SCHEMA_UID");
const sourceAttestationUID = requireBytes32("SOURCE_ATTESTATION_UID");
const sourceTxHash = requireBytes32("SOURCE_TX_HASH");

const account = privateKeyToAccount(privateKey);

const publicClient = createPublicClient({
  chain: selected.chain,
  transport: http(rpcUrl),
});

const walletClient = createWalletClient({
  account,
  chain: selected.chain,
  transport: http(rpcUrl),
});

const chainId = BigInt(await publicClient.getChainId());
assertConnectedChain(selected, chainId);

// S06: RECEIPT_SCHEMA_UID must be exactly the schema the resolver binds to.
const binding = await verifyResolverBinding(publicClient, resolver, selected);
if (binding.receiptSchemaUID.toLowerCase() !== receiptSchemaUID.toLowerCase()) {
  throw new Error(
    `RECEIPT_SCHEMA_UID ${receiptSchemaUID} != resolver-bound schema UID ${binding.receiptSchemaUID}.`,
  );
}

// S01: the schema must be registered on-chain with this exact nonzero resolver.
const schemaRecord = await publicClient.readContract({
  address: SCHEMA_REGISTRY_ADDRESS,
  abi: schemaRegistryAbi,
  functionName: "getSchema",
  args: [receiptSchemaUID],
});
if (schemaRecord.uid.toLowerCase() !== receiptSchemaUID.toLowerCase()) {
  throw new Error(`Receipt schema ${receiptSchemaUID} is not registered on ${selected.name}.`);
}
if (schemaRecord.resolver.toLowerCase() !== resolver.toLowerCase()) {
  throw new Error(`Registered schema resolver ${schemaRecord.resolver} != RESOLVER_ADDRESS ${resolver}.`);
}
if (schemaRecord.revocable !== RECEIPT_REVOCABLE) {
  throw new Error("Registered schema revocability does not match the receipt lifecycle policy.");
}

// S03: fail early if this signer is not an authorized receipt attester.
const authorized = await publicClient.readContract({
  address: resolver,
  abi: receiptResolverAbi,
  functionName: "isAuthorizedAttester",
  args: [account.address],
});
if (!authorized) {
  throw new Error(`Signer ${account.address} is not an authorized attester on resolver ${resolver}.`);
}

const sourceReceipt = await publicClient.getTransactionReceipt({
  hash: sourceTxHash,
});

const fields = receiptToFields({
  receipt: sourceReceipt,
  sourceSchemaUID,
  sourceAttestationUID,
  chainId,
});

const encodedData = encodeReceiptData(fields);

const { request } = await publicClient.simulateContract({
  account,
  address: EAS_ADDRESS,
  abi: easAbi,
  functionName: "attest",
  args: [
    {
      schema: receiptSchemaUID,
      data: {
        recipient: zeroAddress,
        // S07: fixed lifecycle policy, enforced again by the resolver.
        expirationTime: RECEIPT_EXPIRATION_TIME,
        revocable: RECEIPT_REVOCABLE,
        refUID: sourceAttestationUID,
        data: encodedData,
        value: 0n,
      },
    },
  ],
  value: 0n,
});

const txHash = await walletClient.writeContract(request);
const attestationReceipt = await publicClient.waitForTransactionReceipt({
  hash: txHash,
});

if (attestationReceipt.status !== "success") {
  throw new Error(`EAS attestation reverted: ${txHash}`);
}

const attestedEvents = parseEventLogs({
  abi: easAbi,
  eventName: "Attested",
  logs: attestationReceipt.logs.filter(
    (log) => log.address.toLowerCase() === EAS_ADDRESS.toLowerCase(),
  ),
  strict: false,
});

const event = attestedEvents.find(
  (log) =>
    log.args.schemaUID?.toLowerCase() === receiptSchemaUID.toLowerCase(),
);

if (!event?.args.uid) {
  throw new Error("Attested event UID not found in EAS transaction logs.");
}

// S02: report current validity through the resolver's source re-check.
const receiptValidNow = await publicClient.readContract({
  address: resolver,
  abi: receiptResolverAbi,
  functionName: "isReceiptValid",
  args: [event.args.uid],
});

console.log(
  JSON.stringify(
    {
      chain: selected.name,
      chainId: chainId.toString(),
      resolver,
      receiptSchemaUID,
      attestationUID: event.args.uid,
      receiptValidNow,
      easTxHash: txHash,
      sourceTxHash,
      sourceSchemaUID,
      sourceAttestationUID,
      logsHash: fields.logsHash,
      blockNumber: attestationReceipt.blockNumber.toString(),
    },
    null,
    2,
  ),
);
