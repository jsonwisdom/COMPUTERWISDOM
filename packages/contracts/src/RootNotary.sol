// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Ownable} from "lib/openzeppelin-contracts/contracts/access/Ownable.sol";
import {ECDSA} from "lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol";
import {MessageHashUtils} from "lib/openzeppelin-contracts/contracts/utils/cryptography/MessageHashUtils.sol";

/**
 * @title RootNotary
 * @dev Root notary contract for managing cross-chain reputation verification
 */
contract RootNotary is Ownable {
    using ECDSA for bytes32;
    using MessageHashUtils for bytes32;
    
    struct NotaryProof {
        bytes32 dataHash;
        uint256 timestamp;
        uint256 chainId;
        address notary;
        bytes signature;
        bool verified;
    }
    
    struct CrossChainAttestation {
        uint256 sourceChainId;
        address sourceContract;
        bytes32 attestationId;
        bytes32 dataHash;
        uint256 timestamp;
        bool verified;
    }
    
    /// @notice Mapping of proof IDs to notary proofs
    mapping(bytes32 => NotaryProof) public notaryProofs;
    
    /// @notice Mapping of cross-chain attestation IDs to attestations
    mapping(bytes32 => CrossChainAttestation) public crossChainAttestations;
    
    /// @notice Authorized cross-chain notaries
    mapping(address => mapping(uint256 => bool)) public authorizedNotaries;
    
    /// @notice Supported chain IDs
    mapping(uint256 => bool) public supportedChains;
    
    /// @notice Events
    event ProofSubmitted(bytes32 indexed proofId, address indexed notary, uint256 indexed chainId);
    event ProofVerified(bytes32 indexed proofId);
    event CrossChainAttestationReceived(bytes32 indexed attestationId, uint256 indexed sourceChainId);
    event NotaryAuthorized(address indexed notary, uint256 indexed chainId);
    event ChainSupported(uint256 indexed chainId);
    
    constructor(address _owner) Ownable(_owner) {}
    
    /**
     * @notice Add support for a chain
     * @param chainId The chain ID to support
     */
    function addSupportedChain(uint256 chainId) external onlyOwner {
        supportedChains[chainId] = true;
        emit ChainSupported(chainId);
    }
    
    /**
     * @notice Authorize a notary for a specific chain
     * @param notary The notary address
     * @param chainId The chain ID
     */
    function authorizeNotary(address notary, uint256 chainId) external onlyOwner {
        require(supportedChains[chainId], "RootNotary: unsupported chain");
        authorizedNotaries[notary][chainId] = true;
        emit NotaryAuthorized(notary, chainId);
    }
    
    /**
     * @notice Submit a notarized proof
     * @param dataHash The hash of the data being notarized
     * @param chainId The source chain ID
     * @param signature The notary signature
     * @return proofId The generated proof ID
     */
    function submitProof(
        bytes32 dataHash,
        uint256 chainId,
        bytes calldata signature
    ) external returns (bytes32 proofId) {
        require(supportedChains[chainId], "RootNotary: unsupported chain");
        require(authorizedNotaries[msg.sender][chainId], "RootNotary: unauthorized notary");
        
        proofId = keccak256(abi.encodePacked(dataHash, chainId, msg.sender, block.timestamp));
        
        notaryProofs[proofId] = NotaryProof({
            dataHash: dataHash,
            timestamp: block.timestamp,
            chainId: chainId,
            notary: msg.sender,
            signature: signature,
            verified: false
        });
        
        emit ProofSubmitted(proofId, msg.sender, chainId);
    }
    
    /**
     * @notice Verify a notary proof
     * @param proofId The proof ID to verify
     */
    function verifyProof(bytes32 proofId) external {
        NotaryProof storage proof = notaryProofs[proofId];
        require(proof.timestamp > 0, "RootNotary: proof not found");
        require(!proof.verified, "RootNotary: already verified");
        
        // Verify the signature
        bytes32 messageHash = keccak256(abi.encodePacked(proof.dataHash, proof.chainId, proof.timestamp));
        bytes32 ethSignedMessageHash = messageHash.toEthSignedMessageHash();
        
        address signer = ethSignedMessageHash.recover(proof.signature);
        require(signer == proof.notary, "RootNotary: invalid signature");
        require(authorizedNotaries[signer][proof.chainId], "RootNotary: unauthorized signer");
        
        proof.verified = true;
        emit ProofVerified(proofId);
    }
    
    /**
     * @notice Submit a cross-chain attestation
     * @param sourceChainId The source chain ID
     * @param sourceContract The source contract address
     * @param attestationId The attestation ID from source chain
     * @param dataHash The hash of attestation data
     * @return crossChainId The generated cross-chain attestation ID
     */
    function submitCrossChainAttestation(
        uint256 sourceChainId,
        address sourceContract,
        bytes32 attestationId,
        bytes32 dataHash
    ) external returns (bytes32 crossChainId) {
        require(supportedChains[sourceChainId], "RootNotary: unsupported source chain");
        require(authorizedNotaries[msg.sender][sourceChainId], "RootNotary: unauthorized notary");
        
        crossChainId = keccak256(abi.encodePacked(sourceChainId, sourceContract, attestationId));
        
        crossChainAttestations[crossChainId] = CrossChainAttestation({
            sourceChainId: sourceChainId,
            sourceContract: sourceContract,
            attestationId: attestationId,
            dataHash: dataHash,
            timestamp: block.timestamp,
            verified: true
        });
        
        emit CrossChainAttestationReceived(crossChainId, sourceChainId);
    }
    
    /**
     * @notice Get proof details
     * @param proofId The proof ID
     * @return The notary proof data
     */
    function getProof(bytes32 proofId) external view returns (NotaryProof memory) {
        return notaryProofs[proofId];
    }
    
    /**
     * @notice Get cross-chain attestation details
     * @param crossChainId The cross-chain attestation ID
     * @return The cross-chain attestation data
     */
    function getCrossChainAttestation(bytes32 crossChainId) external view returns (CrossChainAttestation memory) {
        return crossChainAttestations[crossChainId];
    }
}