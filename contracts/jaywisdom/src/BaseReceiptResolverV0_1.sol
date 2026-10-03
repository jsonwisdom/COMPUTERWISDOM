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
///
///      Trust-model policy enforced by this contract (SHOULD_SET_V0_1):
///      - S03 attester policy: only addresses fixed in the constructor may
///        attest receipts. There is no admin and no setter; the set is
///        immutable for the life of the deployment. The attester of the
///        referenced SOURCE attestation is NOT constrained
///        (SOURCE_ATTESTER_CONSTRAINED = false); the source is constrained
///        only by existence, schema match, non-revocation and non-expiry.
///      - S05 chain policy: the expected chain id (8453 Base or 84532 Base
///        Sepolia) is fixed in the constructor, must equal block.chainid at
///        deployment, and every payload must carry exactly that chain id.
///      - S06 receipt-schema binding: RECEIPT_SCHEMA_UID is computed in the
///        constructor exactly as the EAS SchemaRegistry computes it:
///        keccak256(abi.encodePacked(RECEIPT_SCHEMA, address(this), RECEIPT_REVOCABLE)).
///        No setter exists. Attestations under any other schema revert.
///      - S07 lifecycle policy: receipts MUST be revocable
///        (RECEIPT_REVOCABLE = true) and MUST NOT carry an EAS expiration
///        (RECEIPT_EXPIRATION_TIME = 0). Receipt validity over time is derived
///        from the source via receiptStatus / isReceiptValid (S02).
///      - S02 source-validity path: receiptStatus(receiptUID) and
///        isReceiptValid(receiptUID) re-read the receipt and its source from
///        EAS at call time and return invalid once the source is revoked or
///        expired. Consumers MUST use isReceiptValid, not EAS validity alone.
///      - Time: block.timestamp only. block.number is never used.
contract BaseReceiptResolverV0_1 {
    uint256 public constant BASE_CHAIN_ID = 8453;
    uint256 public constant BASE_SEPOLIA_CHAIN_ID = 84532;

    /// @notice Exact EAS schema string for the receipt registry (15 fields).
    string public constant RECEIPT_SCHEMA =
        "uint256 chainId,bytes32 schemaUID,bytes32 attestationUID,bytes32 txHash,uint256 blockNumber,bytes32 blockHash,uint256 transactionIndex,address from,address to,uint256 gasUsed,uint256 cumulativeGasUsed,uint256 effectiveGasPrice,uint8 status,address contractAddress,bytes32 logsHash";

    /// @notice S07: receipts must be registered and attested as revocable.
    bool public constant RECEIPT_REVOCABLE = true;

    /// @notice S07: receipts must not carry an EAS expiration time.
    uint64 public constant RECEIPT_EXPIRATION_TIME = 0;

    /// @notice S03: the source attestation's attester is not constrained.
    bool public constant SOURCE_ATTESTER_CONSTRAINED = false;

    address public immutable EAS;

    /// @notice S05: the only chain id this deployment accepts.
    uint256 public immutable CHAIN_ID;

    /// @notice S06: the only receipt schema UID this deployment accepts.
    bytes32 public immutable RECEIPT_SCHEMA_UID;

    /// @notice S03: number of authorized receipt attesters (fixed at deploy).
    uint256 public immutable ATTESTER_COUNT;

    mapping(address => bool) private _authorizedAttester;

    enum ReceiptStatus {
        VALID,
        RECEIPT_NOT_FOUND,
        WRONG_RECEIPT_SCHEMA,
        UNAUTHORIZED_ATTESTER,
        RECEIPT_REVOKED,
        RECEIPT_EXPIRED,
        SOURCE_NOT_FOUND,
        SOURCE_REVOKED,
        SOURCE_EXPIRED
    }

    event AttesterAuthorized(address indexed attester);

    error AccessDenied();
    error InvalidEAS();
    error UnsupportedChainId(uint256 chainId);
    error DeploymentChainMismatch(uint256 expected, uint256 actual);
    error EmptyAttesterSet();
    error InvalidAttester(address attester);
    error DuplicateAttester(address attester);
    error InvalidLength();
    error InvalidValue();
    error InvalidChainId(uint256 supplied, uint256 actual);
    error WrongReceiptSchema(bytes32 supplied, bytes32 expected);
    error UnauthorizedAttester(address attester);
    error ReceiptMustBeRevocable();
    error ReceiptExpirationNotAllowed(uint64 expirationTime);
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

    constructor(address eas, uint256 expectedChainId, address[] memory attesters) {
        if (eas == address(0)) revert InvalidEAS();
        if (expectedChainId != BASE_CHAIN_ID && expectedChainId != BASE_SEPOLIA_CHAIN_ID) {
            revert UnsupportedChainId(expectedChainId);
        }
        if (expectedChainId != block.chainid) {
            revert DeploymentChainMismatch(expectedChainId, block.chainid);
        }
        if (attesters.length == 0) revert EmptyAttesterSet();

        for (uint256 i = 0; i < attesters.length; ++i) {
            address attester = attesters[i];
            if (attester == address(0)) revert InvalidAttester(attester);
            if (_authorizedAttester[attester]) revert DuplicateAttester(attester);
            _authorizedAttester[attester] = true;
            emit AttesterAuthorized(attester);
        }

        EAS = eas;
        CHAIN_ID = expectedChainId;
        ATTESTER_COUNT = attesters.length;
        RECEIPT_SCHEMA_UID = keccak256(abi.encodePacked(RECEIPT_SCHEMA, address(this), RECEIPT_REVOCABLE));
    }

    modifier onlyEAS() {
        if (msg.sender != EAS) revert AccessDenied();
        _;
    }

    function version() external pure returns (string memory) {
        return "1.1.0";
    }

    function isPayable() external pure returns (bool) {
        return false;
    }

    receive() external payable {
        revert InvalidValue();
    }

    /// @notice S03: whether `attester` may create receipts under this resolver.
    function isAuthorizedAttester(address attester) external view returns (bool) {
        return _authorizedAttester[attester];
    }

    function attest(EASAttestationV0_1 calldata attestation) external payable onlyEAS returns (bool) {
        if (msg.value != 0) revert InvalidValue();
        _validate(attestation);
        return true;
    }

    function multiAttest(EASAttestationV0_1[] calldata attestations, uint256[] calldata values)
        external
        payable
        onlyEAS
        returns (bool)
    {
        if (msg.value != 0) revert InvalidValue();
        if (attestations.length != values.length) revert InvalidLength();

        for (uint256 i = 0; i < attestations.length; ++i) {
            if (values[i] != 0) revert InvalidValue();
            _validate(attestations[i]);
        }

        return true;
    }

    /// @dev EAS itself only lets the original attester revoke, and only when
    ///      both the schema and the attestation are revocable. The resolver
    ///      additionally fails closed on any attestation outside its schema.
    function revoke(EASAttestationV0_1 calldata attestation) external payable onlyEAS returns (bool) {
        if (msg.value != 0) revert InvalidValue();
        _requireReceiptSchema(attestation.schema);
        return true;
    }

    function multiRevoke(EASAttestationV0_1[] calldata attestations, uint256[] calldata values)
        external
        payable
        onlyEAS
        returns (bool)
    {
        if (msg.value != 0) revert InvalidValue();
        if (attestations.length != values.length) revert InvalidLength();

        for (uint256 i = 0; i < attestations.length; ++i) {
            if (values[i] != 0) revert InvalidValue();
            _requireReceiptSchema(attestations[i].schema);
        }

        return true;
    }

    /// @notice S02: deterministic, permissionless re-check of a receipt.
    /// @dev Re-reads the receipt and its source attestation from EAS at call
    ///      time. A receipt whose source has since been revoked or has reached
    ///      its expiration time (now >= expirationTime) is reported invalid.
    function receiptStatus(bytes32 receiptUID) public view returns (ReceiptStatus) {
        if (receiptUID == bytes32(0)) return ReceiptStatus.RECEIPT_NOT_FOUND;

        EASAttestationV0_1 memory receipt = IEASReceiptLookupV0_1(EAS).getAttestation(receiptUID);
        if (receipt.uid != receiptUID) return ReceiptStatus.RECEIPT_NOT_FOUND;
        if (receipt.schema != RECEIPT_SCHEMA_UID) return ReceiptStatus.WRONG_RECEIPT_SCHEMA;
        if (!_authorizedAttester[receipt.attester]) return ReceiptStatus.UNAUTHORIZED_ATTESTER;
        if (receipt.revocationTime != 0) return ReceiptStatus.RECEIPT_REVOKED;
        if (_isExpired(receipt.expirationTime)) return ReceiptStatus.RECEIPT_EXPIRED;

        // attest-time validation guarantees refUID == payload.sourceAttestationUID.
        bytes32 sourceUID = receipt.refUID;
        if (sourceUID == bytes32(0)) return ReceiptStatus.SOURCE_NOT_FOUND;

        EASAttestationV0_1 memory source = IEASReceiptLookupV0_1(EAS).getAttestation(sourceUID);
        if (source.uid != sourceUID) return ReceiptStatus.SOURCE_NOT_FOUND;
        if (source.revocationTime != 0) return ReceiptStatus.SOURCE_REVOKED;
        if (_isExpired(source.expirationTime)) return ReceiptStatus.SOURCE_EXPIRED;

        return ReceiptStatus.VALID;
    }

    /// @notice S02: true only if receiptStatus(receiptUID) == VALID.
    function isReceiptValid(bytes32 receiptUID) external view returns (bool) {
        return receiptStatus(receiptUID) == ReceiptStatus.VALID;
    }

    function _requireReceiptSchema(bytes32 schema) internal view {
        if (schema != RECEIPT_SCHEMA_UID) revert WrongReceiptSchema(schema, RECEIPT_SCHEMA_UID);
    }

    function _isExpired(uint64 expirationTime) internal view returns (bool) {
        return expirationTime != 0 && expirationTime <= block.timestamp;
    }

    function _validate(EASAttestationV0_1 calldata attestation) internal view {
        // S06: the receipt itself must belong to the bound receipt schema.
        _requireReceiptSchema(attestation.schema);

        // S03: only constructor-fixed attesters may create receipts.
        if (!_authorizedAttester[attestation.attester]) {
            revert UnauthorizedAttester(attestation.attester);
        }

        // S07: explicit receipt lifecycle policy.
        if (attestation.revocable != RECEIPT_REVOCABLE) revert ReceiptMustBeRevocable();
        if (attestation.expirationTime != RECEIPT_EXPIRATION_TIME) {
            revert ReceiptExpirationNotAllowed(attestation.expirationTime);
        }

        BaseReceiptPayloadV0_1 memory payload = abi.decode(attestation.data, (BaseReceiptPayloadV0_1));

        // S05: payload chain id must equal the deployment chain and the
        // executing chain. A Base (8453) deployment never accepts 84532.
        if (payload.chainId != CHAIN_ID || block.chainid != CHAIN_ID) {
            revert InvalidChainId(payload.chainId, block.chainid);
        }

        if (payload.sourceSchemaUID == bytes32(0) || payload.sourceAttestationUID == bytes32(0)) {
            revert MissingSourceReference();
        }

        if (attestation.refUID != payload.sourceAttestationUID) {
            revert RefUIDMismatch();
        }

        _validateSource(payload.sourceSchemaUID, payload.sourceAttestationUID);
        _validateReceipt(payload);
    }

    function _validateSource(bytes32 sourceSchemaUID, bytes32 sourceAttestationUID) internal view {
        EASAttestationV0_1 memory source = IEASReceiptLookupV0_1(EAS).getAttestation(sourceAttestationUID);

        if (source.uid != sourceAttestationUID) {
            revert SourceAttestationNotFound();
        }
        if (source.schema != sourceSchemaUID) {
            revert SourceSchemaMismatch();
        }
        if (source.revocationTime != 0) {
            revert SourceAttestationRevoked();
        }
        if (_isExpired(source.expirationTime)) {
            revert SourceAttestationExpired();
        }
    }

    /// @dev blockNumber, transactionIndex and effectiveGasPrice are decoded
    ///      as data but are not independently checked by this resolver.
    function _validateReceipt(BaseReceiptPayloadV0_1 memory payload) internal pure {
        if (payload.txHash == bytes32(0) || payload.blockHash == bytes32(0) || payload.logsHash == bytes32(0)) {
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
