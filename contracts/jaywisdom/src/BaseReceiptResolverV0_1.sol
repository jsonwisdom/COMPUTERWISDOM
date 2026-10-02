// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @notice ABI-compatible subset of the EAS Attestation struct.
struct EASAttestationV0_1 {
    bytes32 uid;
    bytes32 schema;
    uint64 time;
    uint64 expirationTime;
    uint64 revocationTime;
    bytes32 refUID;
    address recipient;
    address attester;
    bool revocable;
    bytes data;
}

/// @notice Exact field order of the Base receipt-registry attestation payload.
struct BaseReceiptPayloadV0_1 {
    uint256 chainId;
    bytes32 sourceSchemaUID;
    bytes32 sourceAttestationUID;
    bytes32 txHash;
    uint256 blockNumber;
    bytes32 blockHash;
    uint256 transactionIndex;
    address from;
    address to;
    uint256 gasUsed;
    uint256 cumulativeGasUsed;
    uint256 effectiveGasPrice;
    uint8 status;
    address contractAddress;
    bytes32 logsHash;
}

interface IEASReceiptLookupV0_1 {
    function getAttestation(bytes32 uid) external view returns (EASAttestationV0_1 memory);
}

/// @title BaseReceiptResolverV0_1
/// @notice Resolver for the Base receipt-registry schema.
/// @dev Validates typed invariants and the referenced EAS source attestation.
///      It cannot independently prove arbitrary historical transaction-receipt
///      fields against Base consensus because EVM contracts cannot read old
///      transaction receipts by tx hash.
contract BaseReceiptResolverV0_1 {
    uint256 public constant BASE_CHAIN_ID = 8453;

    address public immutable EAS;

    error AccessDenied();
    error InvalidEAS();
    error InvalidLength();
    error InvalidValue();
    error InvalidChainId(uint256 supplied, uint256 actual);
    error MissingSourceReference();
    error RefUIDMismatch();
    error SourceAttestationNotFound();
    error SourceSchemaMismatch();
    error SourceAttestationRevoked();
    error SourceAttestationExpired();
    error MissingReceiptHash();
    error InvalidStatus(uint8 status);
    error InvalidSender();
    error InvalidContractAddress();
    error InvalidGasAccounting();

    constructor(address eas) {
        if (eas == address(0)) revert InvalidEAS();
        EAS = eas;
    }

    modifier onlyEAS() {
        if (msg.sender != EAS) revert AccessDenied();
        _;
    }

    function version() external pure returns (string memory) {
        return "1.0.0";
    }

    function isPayable() external pure returns (bool) {
        return false;
    }

    receive() external payable {
        revert InvalidValue();
    }

    function attest(
        EASAttestationV0_1 calldata attestation
    ) external payable onlyEAS returns (bool) {
        if (msg.value != 0) revert InvalidValue();
        _validate(attestation);
        return true;
    }

    function multiAttest(
        EASAttestationV0_1[] calldata attestations,
        uint256[] calldata values
    ) external payable onlyEAS returns (bool) {
        if (msg.value != 0) revert InvalidValue();
        if (attestations.length != values.length) revert InvalidLength();

        for (uint256 i = 0; i < attestations.length; ++i) {
            if (values[i] != 0) revert InvalidValue();
            _validate(attestations[i]);
        }

        return true;
    }

    function revoke(
        EASAttestationV0_1 calldata
    ) external payable onlyEAS returns (bool) {
        if (msg.value != 0) revert InvalidValue();
        return true;
    }

    function multiRevoke(
        EASAttestationV0_1[] calldata attestations,
        uint256[] calldata values
    ) external payable onlyEAS returns (bool) {
        if (msg.value != 0) revert InvalidValue();
        if (attestations.length != values.length) revert InvalidLength();

        for (uint256 i = 0; i < values.length; ++i) {
            if (values[i] != 0) revert InvalidValue();
        }

        return true;
    }

    function _validate(EASAttestationV0_1 calldata attestation) internal view {
        BaseReceiptPayloadV0_1 memory payload = abi.decode(
            attestation.data,
            (BaseReceiptPayloadV0_1)
        );

        // Preserve exact schema decoding. These fields are part of the payload
        // and are not independently checked in this resolver.
        payload.blockNumber;
        payload.transactionIndex;
        payload.effectiveGasPrice;

        if (payload.chainId != BASE_CHAIN_ID || payload.chainId != block.chainid) {
            revert InvalidChainId(payload.chainId, block.chainid);
        }

        if (
            payload.sourceSchemaUID == bytes32(0) ||
            payload.sourceAttestationUID == bytes32(0)
        ) {
            revert MissingSourceReference();
        }

        if (attestation.refUID != payload.sourceAttestationUID) {
            revert RefUIDMismatch();
        }

        _validateSource(payload.sourceSchemaUID, payload.sourceAttestationUID);
        _validateReceipt(payload);
    }

    function _validateSource(
        bytes32 sourceSchemaUID,
        bytes32 sourceAttestationUID
    ) internal view {
        EASAttestationV0_1 memory source = IEASReceiptLookupV0_1(EAS)
            .getAttestation(sourceAttestationUID);

        if (source.uid != sourceAttestationUID) {
            revert SourceAttestationNotFound();
        }
        if (source.schema != sourceSchemaUID) {
            revert SourceSchemaMismatch();
        }
        if (source.revocationTime != 0) {
            revert SourceAttestationRevoked();
        }
        if (
            source.expirationTime != 0 &&
            source.expirationTime < uint64(block.timestamp)
        ) {
            revert SourceAttestationExpired();
        }
    }

    function _validateReceipt(BaseReceiptPayloadV0_1 memory payload) internal pure {
        if (
            payload.txHash == bytes32(0) ||
            payload.blockHash == bytes32(0) ||
            payload.logsHash == bytes32(0)
        ) {
            revert MissingReceiptHash();
        }

        if (payload.status > 1) revert InvalidStatus(payload.status);
        if (payload.from == address(0)) revert InvalidSender();

        // For a normal call, contractAddress must be zero.
        // For a contract-creation transaction, "to" is represented as zero.
        // A failed contract creation may legitimately have both as zero.
        if (payload.to != address(0) && payload.contractAddress != address(0)) {
            revert InvalidContractAddress();
        }

        if (payload.gasUsed > payload.cumulativeGasUsed) {
            revert InvalidGasAccounting();
        }
    }
}
