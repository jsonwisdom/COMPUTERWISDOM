// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Ownable} from "lib/openzeppelin-contracts/contracts/access/Ownable.sol";
import {IERC165} from "lib/openzeppelin-contracts/contracts/utils/introspection/IERC165.sol";

/**
 * @title ReputationRegistry
 * @dev Registry for managing reputation data and attestations
 */
contract ReputationRegistry is Ownable, IERC165 {
    struct ReputationData {
        bytes32 merkleRoot;
        uint256 timestamp;
        uint256 blockNumber;
        string ipfsHash;
        address notary;
    }
    
    struct Attestation {
        address attester;
        address subject;
        bytes32 schema;
        bytes data;
        uint256 timestamp;
        bool revoked;
    }
    
    /// @notice Mapping of reputation IDs to reputation data
    mapping(bytes32 => ReputationData) public reputations;
    
    /// @notice Mapping of attestation IDs to attestations
    mapping(bytes32 => Attestation) public attestations;
    
    /// @notice Mapping of addresses to their reputation scores
    mapping(address => uint256) public reputationScores;
    
    /// @notice Authorized notaries
    mapping(address => bool) public authorizedNotaries;
    
    /// @notice Events
    event ReputationUpdated(bytes32 indexed reputationId, bytes32 merkleRoot, string ipfsHash);
    event AttestationCreated(bytes32 indexed attestationId, address indexed attester, address indexed subject);
    event AttestationRevoked(bytes32 indexed attestationId);
    event NotaryAuthorized(address indexed notary);
    event NotaryRevoked(address indexed notary);
    
    constructor(address _owner) Ownable(_owner) {}
    
    /**
     * @notice Authorize a notary
     * @param notary The notary address to authorize
     */
    function authorizeNotary(address notary) external onlyOwner {
        authorizedNotaries[notary] = true;
        emit NotaryAuthorized(notary);
    }
    
    /**
     * @notice Revoke a notary
     * @param notary The notary address to revoke
     */
    function revokeNotary(address notary) external onlyOwner {
        authorizedNotaries[notary] = false;
        emit NotaryRevoked(notary);
    }
    
    /**
     * @notice Update reputation data
     * @param reputationId The reputation identifier
     * @param merkleRoot The merkle root of reputation data
     * @param ipfsHash The IPFS hash containing detailed data
     */
    function updateReputation(
        bytes32 reputationId,
        bytes32 merkleRoot,
        string calldata ipfsHash
    ) external {
        require(authorizedNotaries[msg.sender], "ReputationRegistry: unauthorized notary");
        
        reputations[reputationId] = ReputationData({
            merkleRoot: merkleRoot,
            timestamp: block.timestamp,
            blockNumber: block.number,
            ipfsHash: ipfsHash,
            notary: msg.sender
        });
        
        emit ReputationUpdated(reputationId, merkleRoot, ipfsHash);
    }
    
    /**
     * @notice Create an attestation
     * @param subject The subject of the attestation
     * @param schema The schema identifier
     * @param data The attestation data
     * @return attestationId The created attestation ID
     */
    function createAttestation(
        address subject,
        bytes32 schema,
        bytes calldata data
    ) external returns (bytes32 attestationId) {
        attestationId = keccak256(abi.encodePacked(msg.sender, subject, schema, data, block.timestamp));
        
        attestations[attestationId] = Attestation({
            attester: msg.sender,
            subject: subject,
            schema: schema,
            data: data,
            timestamp: block.timestamp,
            revoked: false
        });
        
        emit AttestationCreated(attestationId, msg.sender, subject);
    }
    
    /**
     * @notice Revoke an attestation
     * @param attestationId The attestation ID to revoke
     */
    function revokeAttestation(bytes32 attestationId) external {
        Attestation storage attestation = attestations[attestationId];
        require(attestation.attester == msg.sender, "ReputationRegistry: not attester");
        require(!attestation.revoked, "ReputationRegistry: already revoked");
        
        attestation.revoked = true;
        emit AttestationRevoked(attestationId);
    }
    
    /**
     * @notice Update reputation score for an address
     * @param account The account to update
     * @param score The new reputation score
     */
    function updateReputationScore(address account, uint256 score) external {
        require(authorizedNotaries[msg.sender], "ReputationRegistry: unauthorized notary");
        reputationScores[account] = score;
    }
    
    /**
     * @notice Check if contract supports an interface
     * @param interfaceId The interface identifier
     * @return True if supported
     */
    function supportsInterface(bytes4 interfaceId) public view virtual override returns (bool) {
        return interfaceId == type(IERC165).interfaceId;
    }
}