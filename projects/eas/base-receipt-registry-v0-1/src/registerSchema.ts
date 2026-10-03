import { createPublicClient, createWalletClient, http, type Hex } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import {
  BASE_RECEIPT_SCHEMA,
  RECEIPT_REVOCABLE,
  SCHEMA_REGISTRY_ADDRESS,
  schemaRegistryAbi,
} from "./baseReceiptSchema.js";
import {
  assertConnectedChain,
  requireEnv,
  requireNonzeroResolver,
  selectReceiptRegistryChain,
} from "./chainConfig.js";
import { verifyResolverBinding } from "./resolverBinding.js";

// S05: explicit chain selection, no default, mainnet needs ALLOW_BASE_MAINNET="true".
const selected = selectReceiptRegistryChain();
// S01: a nonzero resolver is required; there is no zero-address fallback.
const resolver = requireNonzeroResolver(process.env.RESOLVER_ADDRESS);
// S07: revocability is the fixed receipt policy, not an environment default.
const revocable = RECEIPT_REVOCABLE;

const privateKey = requireEnv("PRIVATE_KEY") as Hex;
const rpcUrl = requireEnv("RPC_URL");

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

assertConnectedChain(selected, await publicClient.getChainId());

// S01 / S06 / S07: the resolver must be deployed, bound to this chain, and
// must compute the same receipt schema UID we are about to register.
const { receiptSchemaUID: expectedSchemaUID } = await verifyResolverBinding(
  publicClient,
  resolver,
  selected,
);

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
      chain: selected.name,
      chainId: selected.chainId.toString(),
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
