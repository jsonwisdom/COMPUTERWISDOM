// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface ICanonReceiptRegistryV0_1 {
    event ReceiptAnchored(
        bytes32 indexed receiptId,
        address indexed submitter,
        string actionType,
        string al,
        string joy,
        string computerWisdom,
        uint256 timestamp
    );

    event CanonSignalEmitted(
        bytes32 indexed receiptId,
        address indexed submitter,
        string signalType,
        string payload,
        uint256 timestamp
    );

    function setGenesis(bytes32 genesisReceiptId) external;

    function getGenesis() external view returns (bytes32);

    function anchorReceipt(
        bytes32 receiptId,
        string calldata actionType,
        string calldata al,
        string calldata joy,
        string calldata computerWisdom
    ) external;

    function emitCanonSignal(
        bytes32 receiptId,
        string calldata signalType,
        string calldata payload
    ) external;
}
