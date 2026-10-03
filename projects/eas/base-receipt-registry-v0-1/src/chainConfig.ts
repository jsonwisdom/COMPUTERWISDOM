import { isAddress, zeroAddress, type Address, type Chain, type Hex } from "viem";
import { base, baseSepolia } from "viem/chains";
import { parseExplicitBoolean } from "./explicitBoolean.js";

/**
 * S05: explicit, env-selected chain with NO default.
 *
 *   RECEIPT_REGISTRY_CHAIN=base-sepolia  -> chain id 84532 (test path, use first)
 *   RECEIPT_REGISTRY_CHAIN=base          -> chain id 8453 (production)
 *
 * Production additionally requires ALLOW_BASE_MAINNET="true". Anything else
 * (unset, empty, other names, mainnet without the extra flag) throws.
 * After connecting, the RPC's reported chain id must equal the selection.
 */
export type ReceiptRegistryChainName = "base-sepolia" | "base";

export type ReceiptRegistryChain = {
  name: ReceiptRegistryChainName;
  chain: Chain;
  chainId: bigint;
};

const CHAINS: Record<ReceiptRegistryChainName, ReceiptRegistryChain> = {
  "base-sepolia": { name: "base-sepolia", chain: baseSepolia, chainId: 84532n },
  base: { name: "base", chain: base, chainId: 8453n },
};

export function selectReceiptRegistryChain(env: NodeJS.ProcessEnv = process.env): ReceiptRegistryChain {
  const raw = env.RECEIPT_REGISTRY_CHAIN;
  if (raw !== "base-sepolia" && raw !== "base") {
    throw new Error(
      `RECEIPT_REGISTRY_CHAIN is required and has no default; set it to "base-sepolia" (84532) or "base" (8453). Got: ${JSON.stringify(raw)}`,
    );
  }
  const selected = CHAINS[raw];
  if (selected.chain.id !== Number(selected.chainId)) {
    throw new Error(`Internal chain table mismatch for ${raw}.`);
  }
  if (raw === "base") {
    const allowed = parseExplicitBoolean("ALLOW_BASE_MAINNET", env.ALLOW_BASE_MAINNET);
    if (!allowed) {
      throw new Error("Base mainnet selected but ALLOW_BASE_MAINNET is not \"true\". Run the base-sepolia path first.");
    }
  }
  return selected;
}

export function assertConnectedChain(selected: ReceiptRegistryChain, reportedChainId: number | bigint): void {
  if (BigInt(reportedChainId) !== selected.chainId) {
    throw new Error(
      `RPC chain mismatch: selected ${selected.name} (${selected.chainId}) but RPC reports ${reportedChainId}.`,
    );
  }
}

/** S01: a resolver address is required, must be well formed, and must not be zero. */
export function requireNonzeroResolver(raw: string | undefined): Address {
  if (!raw) {
    throw new Error("RESOLVER_ADDRESS is required. Zero-resolver receipt schemas are not supported.");
  }
  if (!isAddress(raw, { strict: false })) {
    throw new Error(`RESOLVER_ADDRESS is not a valid address: ${raw}`);
  }
  if (raw.toLowerCase() === zeroAddress) {
    throw new Error("RESOLVER_ADDRESS must not be the zero address (S01 RESOLVER_BINDING_REQUIRED).");
  }
  return raw as Address;
}

export function requireEnv(name: string, env: NodeJS.ProcessEnv = process.env): string {
  const value = env[name];
  if (!value) throw new Error(`Missing ${name}.`);
  return value;
}

export function requireBytes32(name: string, env: NodeJS.ProcessEnv = process.env): Hex {
  const value = requireEnv(name, env);
  if (!/^0x[0-9a-fA-F]{64}$/.test(value)) {
    throw new Error(`${name} must be a 0x-prefixed 32-byte hex value.`);
  }
  if (/^0x0{64}$/.test(value)) {
    throw new Error(`${name} must not be zero.`);
  }
  return value as Hex;
}
