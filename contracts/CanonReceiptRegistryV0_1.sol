// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import "./interfaces/ICanonReceiptRegistryV0_1.sol";

/// @title CanonReceiptRegistryV0_1
/// @notice V0_1 SCAFFOLD ONLY. Non-cryptographically bound evidence registry.
/// @dev Per Deprecation Notice: actor must be msg.sender. No EIP-712. Authority false.
/// Records append-only witness events and overlay signals. Replay is the judge.
contract CanonReceiptRegistryV0_1 is ICanonReceiptRegistryV0_1 {
    bytes32 public override genesisCommit;
    bool public override genesisSet;

    mapping(bytes32 => bool) private _receiptExists;
    mapping(bytes32 => address) private _receiptActor;
    mapping(bytes32 => CanonSignal) private _signalOverlay;
    mapping(bytes32 => string) private _signalReason;
    uint256 public override receiptCount;

    mapping(bytes32 => bool) private _blockedTruth;

    constructor() {
        _blockedTruth[keccak256("VERIFIED")] = true;
        _blockedTruth[keccak256("FALSE")] = true;
        _blockedTruth[keccak256("FRAUD")] = true;
        _blockedTruth[keccak256("ADJUDICATED")] = true;
    }

    function setGenesis(bytes32 initialCommit) external override {
        require(!genesisSet, "Genesis: locked_once");
        require(initialCommit!= bytes32(0), "Genesis: zero commit");
        genesisCommit = initialCommit;
        genesisSet = true;
        emit GenesisLocked(initialCommit, msg.sender);
    }

    function anchorReceipt(Receipt calldata r) external override returns (bytes32 receiptHash) {
        require(genesisSet, "Genesis required");
        if (receiptCount == 0) require(r.mergeCommit == genesisCommit, "First receipt must match genesis");
        require(bytes(r.al).length!= 0, "AL missing");
        require(bytes(r.joy).length!= 0, "JOY missing");
        require(keccak256(bytes(r.computerWisdom)) == keccak256("APPEND_ONLY"), "CW must be APPEND_ONLY");
        require(!_blockedTruth[keccak256(bytes(r.status))], "BlockedTruth");
        require(r.actor == msg.sender, "V0_1: actor must be msg.sender");

        receiptHash = keccak256(abi.encode(
            r.actor,
            r.actionType,
            r.evidenceHash,
            r.al,
            r.joy,
            r.computerWisdom,
            r.proofRef,
            r.mergeCommit,
            r.status
        ));
        require(!_receiptExists[receiptHash], "Append_only: exists");

        _receiptExists[receiptHash] = true;
        _receiptActor[receiptHash] = r.actor;
        receiptCount++;

        emit ReceiptAnchored(receiptHash, r.actor, r.mergeCommit, r.proofRef, r.actionType, r.status);
    }

    function emitCanonSignal(bytes32 targetReceipt, CanonSignal signal, string calldata reasonRef) external override {
        require(_receiptExists[targetReceipt], "Target!exists");
        _signalOverlay[targetReceipt] = signal;
        _signalReason[targetReceipt] = reasonRef;
        emit CanonSignalEmitted(targetReceipt, signal, reasonRef, msg.sender);
    }

    function receiptExists(bytes32 receiptHash) external view override returns (bool) {
        return _receiptExists[receiptHash];
    }

    function receiptActor(bytes32 receiptHash) external view override returns (address) {
        return _receiptActor[receiptHash];
    }

    function getSignal(bytes32 targetReceipt) external view returns (CanonSignal, string memory) {
        return (_signalOverlay[targetReceipt], _signalReason[targetReceipt]);
    }
}
