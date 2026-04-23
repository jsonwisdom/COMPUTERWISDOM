// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Test, console} from "forge-std/Test.sol";
import {Config} from "../src/Config.sol";
import {ReputationRegistry} from "../src/ReputationRegistry.sol";
import {RootNotary} from "../src/RootNotary.sol";

contract ReputationTest is Test {
    Config public config;
    ReputationRegistry public reputationRegistry;
    RootNotary public rootNotary;
    
    address public owner = makeAddr("owner");
    address public notary = makeAddr("notary");
    address public user = makeAddr("user");
    
    function setUp() public {
        vm.startPrank(owner);
        
        config = new Config(owner);
        reputationRegistry = new ReputationRegistry(owner);
        rootNotary = new RootNotary(owner);
        
        // Configure contracts
        config.setConfig("REPUTATION_REGISTRY", abi.encode(address(reputationRegistry)));
        config.setConfig("ROOT_NOTARY", abi.encode(address(rootNotary)));
        
        // Authorize notary
        reputationRegistry.authorizeNotary(notary);
        rootNotary.addSupportedChain(31337);
        rootNotary.authorizeNotary(notary, 31337);
        
        vm.stopPrank();
    }
    
    function testConfigSetAndGet() public {
        vm.prank(owner);
        config.setConfig("TEST_KEY", abi.encode(uint256(12345)));
        
        uint256 value = config.getUint256("TEST_KEY");
        assertEq(value, 12345);
    }
    
    function testReputationUpdate() public {
        bytes32 reputationId = keccak256("test-reputation");
        bytes32 merkleRoot = keccak256("test-merkle-root");
        string memory ipfsHash = "QmTestHash";
        
        vm.prank(notary);
        reputationRegistry.updateReputation(reputationId, merkleRoot, ipfsHash);
        
        (bytes32 storedRoot, uint256 timestamp, , string memory storedHash, address storedNotary) = 
            reputationRegistry.reputations(reputationId);
        
        assertEq(storedRoot, merkleRoot);
        assertEq(storedHash, ipfsHash);
        assertEq(storedNotary, notary);
        assertGt(timestamp, 0);
    }
    
    function testAttestationCreation() public {
        bytes32 schema = keccak256("test-schema");
        bytes memory data = abi.encode("test attestation data");
        
        vm.prank(user);
        bytes32 attestationId = reputationRegistry.createAttestation(user, schema, data);
        
        (address attester, address subject, bytes32 storedSchema, bytes memory storedData, uint256 timestamp, bool revoked) = 
            reputationRegistry.attestations(attestationId);
        
        assertEq(attester, user);
        assertEq(subject, user);
        assertEq(storedSchema, schema);
        assertEq(storedData, data);
        assertFalse(revoked);
        assertGt(timestamp, 0);
    }
    
    function testNotaryProofSubmission() public {
        bytes32 dataHash = keccak256("test-data");
        uint256 chainId = 31337;
        bytes memory signature = "test-signature";
        
        vm.prank(notary);
        bytes32 proofId = rootNotary.submitProof(dataHash, chainId, signature);
        
        (bytes32 storedHash, uint256 timestamp, uint256 storedChainId, address storedNotary, bytes memory storedSignature, bool verified) = 
            rootNotary.notaryProofs(proofId);
        
        assertEq(storedHash, dataHash);
        assertEq(storedChainId, chainId);
        assertEq(storedNotary, notary);
        assertEq(storedSignature, signature);
        assertFalse(verified);
        assertGt(timestamp, 0);
    }
}