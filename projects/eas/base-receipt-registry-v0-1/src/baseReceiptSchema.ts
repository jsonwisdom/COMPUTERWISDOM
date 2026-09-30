import {
  encodeAbiParameters,
  encodePacked,
  keccak256,
  parseAbiParameters,
  zeroAddress,
  type Address,
  type Hex,
  type TransactionReceipt,
} from "viem";

export const BASE_CHAIN_ID = 8453n;

export const EAS_ADDRESS =
  "0x4200000000000000000000000000000000000021" as const;

export const SCHEMA_REGISTRY_ADDRESS =
  "0x4200000000000000000000000000000000000020" as const;

export const BASE_RECEIPT_SCHEMA =
  "uint256 chainId,bytes32 schemaUID,bytes32 attestationUID,bytes32 txHash,uint256 blockNumber,bytes32 blockHash,uint256 transactionIndex,address from,address to,uint256 gasUsed,uint256 cumulativeGasUsed,uint256 effectiveGasPrice,uint8 status,address contractAddress,bytes32 logsHash";

export const BASE_RECEIPT_SCHEMA_FIELD_COUNT = 15;

export const BASE_RECEIPT_PARAMS = parseAbiParameters(BASE_RECEIPT_SCHEMA);

const LOGS_HASH_PARAMS = parseAbiParameters(
  "(address emitter,bytes32[] topics,bytes data)[] logs",
);

export type BaseReceiptFields = {
  chainId: bigint;
  schemaUID: Hex;
  attestationUID: Hex;
  txHash: Hex;
  blockNumber: bigint;
  blockHash: Hex;
  transactionIndex: bigint;
  from: Address;
  to: Address;
  gasUsed: bigint;
  cumulativeGasUsed: bigint;
  effectiveGasPrice: bigint;
  status: 0 | 1;
  contractAddress: Address;
  logsHash: Hex;
};

export const schemaRegistryAbi = [
  {
    type: "function",
    name: "register",
    stateMutability: "nonpayable",
    inputs: [
      { name: "schema", type: "string" },
      { name: "resolver", type: "address" },
      { name: "revocable", type: "bool" },
    ],
    outputs: [{ name: "", type: "bytes32" }],
  },
  {
    type: "function",
    name: "getSchema",
    stateMutability: "view",
    inputs: [{ name: "uid", type: "bytes32" }],
    outputs: [
      {
        name: "",
        type: "tuple",
        components: [
          { name: "uid", type: "bytes32" },
          { name: "resolver", type: "address" },
          { name: "revocable", type: "bool" },
          { name: "schema", type: "string" },
        ],
      },
    ],
  },
] as const;

export const easAbi = [
  {
    type: "function",
    name: "attest",
    stateMutability: "payable",
    inputs: [
      {
        name: "request",
        type: "tuple",
        components: [
          { name: "schema", type: "bytes32" },
          {
            name: "data",
            type: "tuple",
            components: [
              { name: "recipient", type: "address" },
              { name: "expirationTime", type: "uint64" },
              { name: "revocable", type: "bool" },
              { name: "refUID", type: "bytes32" },
              { name: "data", type: "bytes" },
              { name: "value", type: "uint256" },
            ],
          },
        ],
      },
    ],
    outputs: [{ name: "", type: "bytes32" }],
  },
  {
    type: "event",
    name: "Attested",
    anonymous: false,
    inputs: [
      { indexed: true, name: "recipient", type: "address" },
      { indexed: true, name: "attester", type: "address" },
      { indexed: false, name: "uid", type: "bytes32" },
      { indexed: true, name: "schemaUID", type: "bytes32" },
    ],
  },
] as const;

export function computeSchemaUID(
  resolver: Address = zeroAddress,
  revocable = true,
): Hex {
  return keccak256(
    encodePacked(
      ["string", "address", "bool"],
      [BASE_RECEIPT_SCHEMA, resolver, revocable],
    ),
  );
}

export function computeLogsHash(
  logs: TransactionReceipt["logs"],
): Hex {
  const normalized = logs.map((log) => ({
    emitter: log.address,
    topics: [...log.topics] as Hex[],
    data: log.data,
  }));

  return keccak256(encodeAbiParameters(LOGS_HASH_PARAMS, [normalized]));
}

export function receiptToFields(args: {
  receipt: TransactionReceipt;
  sourceSchemaUID: Hex;
  sourceAttestationUID: Hex;
  chainId?: bigint;
}): BaseReceiptFields {
  const { receipt, sourceSchemaUID, sourceAttestationUID } = args;

  if (!receipt.blockHash) {
    throw new Error("Receipt has no blockHash.");
  }

  if (receipt.effectiveGasPrice === undefined) {
    throw new Error("Receipt has no effectiveGasPrice.");
  }

  return {
    chainId: args.chainId ?? BASE_CHAIN_ID,
    schemaUID: sourceSchemaUID,
    attestationUID: sourceAttestationUID,
    txHash: receipt.transactionHash,
    blockNumber: receipt.blockNumber,
    blockHash: receipt.blockHash,
    transactionIndex: BigInt(receipt.transactionIndex),
    from: receipt.from,
    to: receipt.to ?? zeroAddress,
    gasUsed: receipt.gasUsed,
    cumulativeGasUsed: receipt.cumulativeGasUsed,
    effectiveGasPrice: receipt.effectiveGasPrice,
    status: receipt.status === "success" ? 1 : 0,
    contractAddress: receipt.contractAddress ?? zeroAddress,
    logsHash: computeLogsHash(receipt.logs),
  };
}

export function encodeReceiptData(fields: BaseReceiptFields): Hex {
  return encodeAbiParameters(BASE_RECEIPT_PARAMS, [
    fields.chainId,
    fields.schemaUID,
    fields.attestationUID,
    fields.txHash,
    fields.blockNumber,
    fields.blockHash,
    fields.transactionIndex,
    fields.from,
    fields.to,
    fields.gasUsed,
    fields.cumulativeGasUsed,
    fields.effectiveGasPrice,
    fields.status,
    fields.contractAddress,
    fields.logsHash,
  ]);
}
