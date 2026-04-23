import { ethers } from "hardhat";

async function main() {
  const [deployer, user1, user2] = await ethers.getSigners();
  
  console.log("Seeding demo data...");
  
  // Load deployment addresses
  const fs = require("fs");
  const chainId = (await ethers.provider.getNetwork()).chainId.toString();
  const deploymentFile = `./deployments-${chainId}.json`;
  
  if (!fs.existsSync(deploymentFile)) {
    throw new Error(`Deployment file ${deploymentFile} not found. Run deploy script first.`);
  }
  
  const deployment = JSON.parse(fs.readFileSync(deploymentFile, "utf8"));
  
  // Get contract instances
  const config = await ethers.getContractAt("Config", deployment.contracts.Config);
  const reputationRegistry = await ethers.getContractAt("ReputationRegistry", deployment.contracts.ReputationRegistry);
  const rootNotary = await ethers.getContractAt("RootNotary", deployment.contracts.RootNotary);
  
  console.log("Creating demo reputation data...");
  
  // Create some demo reputation entries
  const reputationId1 = ethers.keccak256(ethers.toUtf8Bytes("user1-reputation"));
  const merkleRoot1 = ethers.keccak256(ethers.toUtf8Bytes("user1-merkle-root"));
  await reputationRegistry.connect(deployer).updateReputation(
    reputationId1,
    merkleRoot1,
    "QmUser1ReputationData"
  );
  
  const reputationId2 = ethers.keccak256(ethers.toUtf8Bytes("user2-reputation"));
  const merkleRoot2 = ethers.keccak256(ethers.toUtf8Bytes("user2-merkle-root"));
  await reputationRegistry.connect(deployer).updateReputation(
    reputationId2,
    merkleRoot2,
    "QmUser2ReputationData"
  );
  
  console.log("Creating demo attestations...");
  
  // Create some demo attestations
  const schema1 = ethers.keccak256(ethers.toUtf8Bytes("github-contribution"));
  const attestationData1 = ethers.AbiCoder.defaultAbiCoder().encode(
    ["string", "uint256"],
    ["contributed to reputation-kernel project", 100]
  );
  
  const attestationId1 = await reputationRegistry.connect(user1).createAttestation(
    user1.address,
    schema1,
    attestationData1
  );
  
  const schema2 = ethers.keccak256(ethers.toUtf8Bytes("code-review"));
  const attestationData2 = ethers.AbiCoder.defaultAbiCoder().encode(
    ["string", "uint256", "address"],
    ["reviewed smart contracts", 85, user1.address]
  );
  
  const attestationId2 = await reputationRegistry.connect(user2).createAttestation(
    user2.address,
    schema2,
    attestationData2
  );
  
  console.log("Setting reputation scores...");
  
  // Set some reputation scores
  await reputationRegistry.connect(deployer).updateReputationScore(user1.address, 750);
  await reputationRegistry.connect(deployer).updateReputationScore(user2.address, 650);
  
  console.log("Creating notary proofs...");
  
  // Create some demo notary proofs
  const dataHash1 = ethers.keccak256(ethers.toUtf8Bytes("cross-chain-data-1"));
  const signature1 = ethers.toUtf8Bytes("demo-signature-1");
  
  const proofId1 = await rootNotary.connect(deployer).submitProof(
    dataHash1,
    31337,
    signature1
  );
  
  const dataHash2 = ethers.keccak256(ethers.toUtf8Bytes("cross-chain-data-2"));
  const signature2 = ethers.toUtf8Bytes("demo-signature-2");
  
  const proofId2 = await rootNotary.connect(deployer).submitProof(
    dataHash2,
    8453,
    signature2
  );
  
  console.log("\n=== Demo Data Summary ===");
  console.log("Reputation entries created: 2");
  console.log("Attestations created: 2");
  console.log("Reputation scores set for:", user1.address, "and", user2.address);
  console.log("Notary proofs created: 2");
  console.log("========================");
  
  // Save demo data summary
  const demoData = {
    network: (await ethers.provider.getNetwork()).name,
    chainId: chainId,
    accounts: {
      deployer: deployer.address,
      user1: user1.address,
      user2: user2.address,
    },
    reputationIds: [reputationId1, reputationId2],
    reputationScores: {
      [user1.address]: 750,
      [user2.address]: 650,
    },
    timestamp: new Date().toISOString(),
  };
  
  fs.writeFileSync(
    `./demo-data-${chainId}.json`,
    JSON.stringify(demoData, null, 2)
  );
  console.log(`Demo data summary saved to demo-data-${chainId}.json`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});