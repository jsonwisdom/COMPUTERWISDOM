import {
  createPublicClient,
  createWalletClient,
  http,
  zeroAddress,
  type Address,
  type Hex,
} from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";
import {
  BASE_RECEIPT_SCHEMA,
  SCHEMA_REGISTRY_ADDRESS,
  computeSchemaUID,
  schemaRegistryAbi,
} from "./baseReceiptSchema.js";
import { parseExplicitBoolean } from "./explicitBoolean.js";

const privateKey = process.env.PRIVATE_KEY as Hex | undefined;
const rpcUrl = process.env.BASE_RPC_URL;
const resolver = (process.env.RESOLVER_ADDRESS ?? zeroAddress) as Address;
const revocable = parseExplicitBoolean("SCHEMA_REVOCABLE", process.env.SCHEMA_REVOCABLE, "true");

if (!privateKey) throw new Error("Missing PRIVATE_KEY.");
if (!rpcUrl) throw new Error("Missing BASE_RPC_URL.");

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

const expectedSchemaUID = computeSchemaUID(resolver, revocable);

const { request } = await publicClient.simulateContract({
  account,
  address: SCHEMA_REGISTRY_ADDRESS,
  abi: schemaRegistryAbi,
  functionName: "register",
  args: [BASE_RECEIPT_SCHEMA, resolver, revocable],
});

const txHash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash: txHash });

if (receipt.status !== "success") {
  throw new Error(`Schema registration reverted: ${txHash}`);
}

const record = await publicClient.readContract({
  address: SCHEMA_REGISTRY_ADDRESS,
  abi: schemaRegistryAbi,
  functionName: "getSchema",
  args: [expectedSchemaUID],
});

if (record.uid.toLowerCase() !== expectedSchemaUID.toLowerCase()) {
  throw new Error("Registered schema UID did not match deterministic UID.");
}
if (record.schema !== BASE_RECEIPT_SCHEMA) {
  throw new Error("Registered schema string did not match local schema.");
}
if (record.resolver.toLowerCase() !== resolver.toLowerCase()) {
  throw new Error("Registered resolver did not match requested resolver.");
}
if (record.revocable !== revocable) {
  throw new Error("Registered revocable flag did not match requested flag.");
}

console.log(
  JSON.stringify(
    {
      chainId: base.id,
      schemaRegistry: SCHEMA_REGISTRY_ADDRESS,
      resolver,
      revocable,
      schema: BASE_RECEIPT_SCHEMA,
      schemaUID: expectedSchemaUID,
      txHash,
      blockNumber: receipt.blockNumber.toString(),
    },
    null,
    2,
  ),
);
