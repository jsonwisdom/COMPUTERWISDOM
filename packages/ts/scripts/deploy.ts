import { ethers } from "hardhat";

async function main() {
  const [deployer] = await ethers.getSigners();
  
  console.log("Deploying contracts with the account:", deployer.address);
  console.log("Account balance:", (await deployer.provider.getBalance(deployer.address)).toString());

  // Deploy Config
  const Config = await ethers.getContractFactory("Config");
  const config = await Config.deploy(deployer.address);
  await config.waitForDeployment();
  console.log("Config deployed to:", await config.getAddress());

  // Deploy ReputationRegistry
  const ReputationRegistry = await ethers.getContractFactory("ReputationRegistry");
  const reputationRegistry = await ReputationRegistry.deploy(deployer.address);
  await reputationRegistry.waitForDeployment();
  console.log("ReputationRegistry deployed to:", await reputationRegistry.getAddress());

  // Deploy RootNotary
  const RootNotary = await ethers.getContractFactory("RootNotary");
  const rootNotary = await RootNotary.deploy(deployer.address);
  await rootNotary.waitForDeployment();
  console.log("RootNotary deployed to:", await rootNotary.getAddress());

  // Configure contracts
  const reputationRegistryAddress = await reputationRegistry.getAddress();
  const rootNotaryAddress = await rootNotary.getAddress();
  
  await config.setConfig("REPUTATION_REGISTRY", ethers.AbiCoder.defaultAbiCoder().encode(["address"], [reputationRegistryAddress]));
  await config.setConfig("ROOT_NOTARY", ethers.AbiCoder.defaultAbiCoder().encode(["address"], [rootNotaryAddress]));
  await config.setConfig("DEPLOYER", ethers.AbiCoder.defaultAbiCoder().encode(["address"], [deployer.address]));

  // Authorize notary
  await reputationRegistry.authorizeNotary(deployer.address);
  await rootNotary.addSupportedChain(1); // Ethereum
  await rootNotary.addSupportedChain(8453); // Base
  await rootNotary.addSupportedChain(31337); // Local
  await rootNotary.authorizeNotary(deployer.address, 1);
  await rootNotary.authorizeNotary(deployer.address, 8453);
  await rootNotary.authorizeNotary(deployer.address, 31337);

  console.log("\n=== Deployment Summary ===");
  console.log("Config:", await config.getAddress());
  console.log("ReputationRegistry:", await reputationRegistry.getAddress());
  console.log("RootNotary:", await rootNotary.getAddress());
  console.log("==========================");

  // Save deployment addresses
  const fs = require("fs");
  const deploymentData = {
    network: (await ethers.provider.getNetwork()).name,
    chainId: (await ethers.provider.getNetwork()).chainId.toString(),
    deployer: deployer.address,
    contracts: {
      Config: await config.getAddress(),
      ReputationRegistry: await reputationRegistry.getAddress(),
      RootNotary: await rootNotary.getAddress(),
    },
    timestamp: new Date().toISOString(),
  };

  fs.writeFileSync(
    `./deployments-${deploymentData.chainId}.json`,
    JSON.stringify(deploymentData, null, 2)
  );
  console.log(`Deployment data saved to deployments-${deploymentData.chainId}.json`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});