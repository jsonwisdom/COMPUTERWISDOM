import { ethers } from "ethers";

export interface ReputationData {
  merkleRoot: string;
  timestamp: number;
  blockNumber: number;
  ipfsHash: string;
  notary: string;
}

export interface Attestation {
  attester: string;
  subject: string;
  schema: string;
  data: string;
  timestamp: number;
  revoked: boolean;
}

export class ReputationKernelSDK {
  private provider: ethers.Provider;
  private config: ethers.Contract;
  private reputationRegistry: ethers.Contract;
  private rootNotary: ethers.Contract;

  constructor(
    provider: ethers.Provider,
    configAddress: string,
    reputationRegistryAddress: string,
    rootNotaryAddress: string
  ) {
    this.provider = provider;
    
    // Contract ABIs (simplified for demo)
    const configABI = [
      "function getConfig(string key) view returns (bytes)",
      "function getAddress(string key) view returns (address)",
      "function getUint256(string key) view returns (uint256)"
    ];
    
    const reputationRegistryABI = [
      "function reputations(bytes32) view returns (bytes32, uint256, uint256, string, address)",
      "function attestations(bytes32) view returns (address, address, bytes32, bytes, uint256, bool)",
      "function reputationScores(address) view returns (uint256)",
      "function createAttestation(address, bytes32, bytes) returns (bytes32)",
      "function updateReputation(bytes32, bytes32, string)",
      "function updateReputationScore(address, uint256)"
    ];
    
    const rootNotaryABI = [
      "function notaryProofs(bytes32) view returns (bytes32, uint256, uint256, address, bytes, bool)",
      "function crossChainAttestations(bytes32) view returns (uint256, address, bytes32, bytes32, uint256, bool)",
      "function submitProof(bytes32, uint256, bytes) returns (bytes32)",
      "function verifyProof(bytes32)"
    ];
    
    this.config = new ethers.Contract(configAddress, configABI, provider);
    this.reputationRegistry = new ethers.Contract(reputationRegistryAddress, reputationRegistryABI, provider);
    this.rootNotary = new ethers.Contract(rootNotaryAddress, rootNotaryABI, provider);
  }

  async getReputationData(reputationId: string): Promise<ReputationData | null> {
    try {
      const result = await this.reputationRegistry.reputations(reputationId);
      if (result[0] === ethers.ZeroHash) return null;
      
      return {
        merkleRoot: result[0],
        timestamp: Number(result[1]),
        blockNumber: Number(result[2]),
        ipfsHash: result[3],
        notary: result[4]
      };
    } catch (error) {
      console.error("Error fetching reputation data:", error);
      return null;
    }
  }

  async getReputationScore(address: string): Promise<number> {
    try {
      const score = await this.reputationRegistry.reputationScores(address);
      return Number(score);
    } catch (error) {
      console.error("Error fetching reputation score:", error);
      return 0;
    }
  }

  async getAttestation(attestationId: string): Promise<Attestation | null> {
    try {
      const result = await this.reputationRegistry.attestations(attestationId);
      if (result[0] === ethers.ZeroAddress) return null;
      
      return {
        attester: result[0],
        subject: result[1],
        schema: result[2],
        data: result[3],
        timestamp: Number(result[4]),
        revoked: result[5]
      };
    } catch (error) {
      console.error("Error fetching attestation:", error);
      return null;
    }
  }

  async createAttestation(
    signer: ethers.Signer,
    subject: string,
    schema: string,
    data: string
  ): Promise<string> {
    try {
      const registryWithSigner = this.reputationRegistry.connect(signer);
      const schemaBytes = ethers.keccak256(ethers.toUtf8Bytes(schema));
      const dataBytes = ethers.toUtf8Bytes(data);
      
      const tx = await registryWithSigner.createAttestation(subject, schemaBytes, dataBytes);
      const receipt = await tx.wait();
      
      // Extract attestation ID from events
      const event = receipt.logs.find((log: any) => 
        log.topics[0] === ethers.keccak256(ethers.toUtf8Bytes("AttestationCreated(bytes32,address,address)"))
      );
      
      return event ? event.topics[1] : "";
    } catch (error) {
      console.error("Error creating attestation:", error);
      throw error;
    }
  }

  async submitNotaryProof(
    signer: ethers.Signer,
    dataHash: string,
    chainId: number,
    signature: string
  ): Promise<string> {
    try {
      const notaryWithSigner = this.rootNotary.connect(signer);
      const signatureBytes = ethers.toUtf8Bytes(signature);
      
      const tx = await notaryWithSigner.submitProof(dataHash, chainId, signatureBytes);
      const receipt = await tx.wait();
      
      // Extract proof ID from events
      const event = receipt.logs.find((log: any) => 
        log.topics[0] === ethers.keccak256(ethers.toUtf8Bytes("ProofSubmitted(bytes32,address,uint256)"))
      );
      
      return event ? event.topics[1] : "";
    } catch (error) {
      console.error("Error submitting notary proof:", error);
      throw error;
    }
  }

  async resolveENSReputation(ensName: string): Promise<ReputationData | null> {
    // Simulate ENS resolution - in a real implementation this would query ENS
    // and then resolve the CCIP-Read gateway
    const reputationId = ethers.keccak256(ethers.toUtf8Bytes(ensName));
    return this.getReputationData(reputationId);
  }
}

export default ReputationKernelSDK;