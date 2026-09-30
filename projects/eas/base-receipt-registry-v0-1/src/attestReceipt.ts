import {
  createPublicClient,
  createWalletClient,
  http,
  parseEventLogs,
  zeroAddress,
  type Hex,
} from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";
import {
  EAS_ADDRESS,
  easAbi,
  encodeReceiptData,
  receiptToFields,
} from "./baseReceiptSchema.js";

const privateKey = process.env.PRIVATE_KEY as Hex | undefined;
const rpcUrl = process.env.BASE_RPC_URL;
const receiptSchemaUID = process.env.RECEIPT_SCHEMA_UID as Hex | undefined;
const sourceSchemaUID = process.env.SOURCE_SCHEMA_UID as Hex | undefined;
const sourceAttestationUID = process.env.SOURCE_ATTESTATION_UID as Hex | undefined;
const sourceTxHash = process.env.SOURCE_TX_HASH as Hex | undefined;
const revocable = (process.env.ATTESTATION_REVOCABLE ?? "true") === "true";

if (!privateKey) throw new Error("Missing PRIVATE_KEY.");
if (!rpcUrl) throw new Error("Missing BASE_RPC_URL.");
if (!receiptSchemaUID) throw new Error("Missing RECEIPT_SCHEMA_UID.");
if (!sourceSchemaUID) throw new Error("Missing SOURCE_SCHEMA_UID.");
if (!sourceAttestationUID) throw new Error("Missing SOURCE_ATTESTATION_UID.");
if (!sourceTxHash) throw new Error("Missing SOURCE_TX_HASH.");

const account = privateKeyToAccount(privateKey);

const publicClient = createPublicClient({
  chain: base,
  transport: http(rpcUrl),
});

const walletClient = createWalletClient({
  account,
  chain: base,
  transport: http(rpcUrl),
});

const chainId = BigInt(await publicClient.getChainId());
if (chainId !== 8453n) {
  throw new Error(`Wrong chain: expected 8453, got ${chainId}`);
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
        expirationTime: 0n,
        revocable,
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

console.log(
  JSON.stringify(
    {
      receiptSchemaUID,
      attestationUID: event.args.uid,
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
