// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract LapisRootRegistry {
    event RootAnchored(bytes32 indexed merkleRoot, uint256 timestamp, address indexed signer);

    bytes32 public lastRoot;

    function anchor(bytes32 merkleRoot) external {
        lastRoot = merkleRoot;
        emit RootAnchored(merkleRoot, block.timestamp, msg.sender);
    }
}
