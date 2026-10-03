import type { Address, Hex, PublicClient } from "viem";
import {
  BASE_RECEIPT_SCHEMA,
  EAS_ADDRESS,
  RECEIPT_EXPIRATION_TIME,
  RECEIPT_REVOCABLE,
  computeSchemaUID,
  receiptResolverAbi,
} from "./baseReceiptSchema.js";
import type { ReceiptRegistryChain } from "./chainConfig.js";

/**
 * S01 / S05 / S06 / S07: before any write, prove that RESOLVER_ADDRESS is a
 * deployed BaseReceiptResolverV0_1 bound to the selected chain, the EAS
 * predeploy, the exact 15-field schema string, and the fixed lifecycle
 * policy. Any mismatch throws (fail closed).
 */
export async function verifyResolverBinding(
  publicClient: PublicClient,
  resolver: Address,
  selected: ReceiptRegistryChain,
): Promise<{ receiptSchemaUID: Hex }> {
  const code = await publicClient.getCode({ address: resolver });
  if (!code || code === "0x") {
    throw new Error(`No contract code at RESOLVER_ADDRESS ${resolver} on ${selected.name}.`);
  }

  const contract = { address: resolver, abi: receiptResolverAbi } as const;
  const [eas, chainId, schema, revocable, expirationTime, onchainSchemaUID] = await Promise.all([
    publicClient.readContract({ ...contract, functionName: "EAS" }),
    publicClient.readContract({ ...contract, functionName: "CHAIN_ID" }),
    publicClient.readContract({ ...contract, functionName: "RECEIPT_SCHEMA" }),
    publicClient.readContract({ ...contract, functionName: "RECEIPT_REVOCABLE" }),
    publicClient.readContract({ ...contract, functionName: "RECEIPT_EXPIRATION_TIME" }),
    publicClient.readContract({ ...contract, functionName: "RECEIPT_SCHEMA_UID" }),
  ]);

  if (eas.toLowerCase() !== EAS_ADDRESS.toLowerCase()) {
    throw new Error(`Resolver EAS ${eas} != EAS predeploy ${EAS_ADDRESS}.`);
  }
  if (chainId !== selected.chainId) {
    throw new Error(`Resolver CHAIN_ID ${chainId} != selected ${selected.name} (${selected.chainId}).`);
  }
  if (schema !== BASE_RECEIPT_SCHEMA) {
    throw new Error("Resolver RECEIPT_SCHEMA does not equal the local 15-field schema string.");
  }
  if (revocable !== RECEIPT_REVOCABLE) {
    throw new Error(`Resolver RECEIPT_REVOCABLE ${revocable} != policy ${RECEIPT_REVOCABLE}.`);
  }
  if (expirationTime !== RECEIPT_EXPIRATION_TIME) {
    throw new Error(`Resolver RECEIPT_EXPIRATION_TIME ${expirationTime} != policy ${RECEIPT_EXPIRATION_TIME}.`);
  }

  const receiptSchemaUID = computeSchemaUID(resolver, RECEIPT_REVOCABLE);
  if (onchainSchemaUID.toLowerCase() !== receiptSchemaUID.toLowerCase()) {
    throw new Error(`Resolver RECEIPT_SCHEMA_UID ${onchainSchemaUID} != locally computed ${receiptSchemaUID}.`);
  }

  return { receiptSchemaUID };
}
