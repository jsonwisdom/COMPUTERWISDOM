// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Script, console} from "forge-std/Script.sol";
import {Config} from "../src/Config.sol";
import {ReputationRegistry} from "../src/ReputationRegistry.sol";
import {RootNotary} from "../src/RootNotary.sol";

/**
 * @title DeployLocal
 * @dev Deployment script for local development
 */
contract DeployLocal is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        address deployer = vm.addr(deployerPrivateKey);
        
        console.log("Deploying contracts with deployer:", deployer);
        console.log("Deployer balance:", deployer.balance);
        
        vm.startBroadcast(deployerPrivateKey);
        
        // Deploy Config contract
        Config config = new Config(deployer);
        console.log("Config deployed at:", address(config));
        
        // Deploy ReputationRegistry contract
        ReputationRegistry reputationRegistry = new ReputationRegistry(deployer);
        console.log("ReputationRegistry deployed at:", address(reputationRegistry));
        
        // Deploy RootNotary contract
        RootNotary rootNotary = new RootNotary(deployer);
        console.log("RootNotary deployed at:", address(rootNotary));
        
        // Configure initial settings
        config.setConfig("REPUTATION_REGISTRY", abi.encode(address(reputationRegistry)));
        config.setConfig("ROOT_NOTARY", abi.encode(address(rootNotary)));
        config.setConfig("DEPLOYER", abi.encode(deployer));
        
        // Authorize the deployer as a notary
        reputationRegistry.authorizeNotary(deployer);
        rootNotary.addSupportedChain(1); // Ethereum mainnet
        rootNotary.addSupportedChain(8453); // Base mainnet
        rootNotary.addSupportedChain(31337); // Local development
        rootNotary.authorizeNotary(deployer, 1);
        rootNotary.authorizeNotary(deployer, 8453);
        rootNotary.authorizeNotary(deployer, 31337);
        
        vm.stopBroadcast();
        
        console.log("=== Deployment Summary ===");
        console.log("Config:", address(config));
        console.log("ReputationRegistry:", address(reputationRegistry));
        console.log("RootNotary:", address(rootNotary));
        console.log("==========================");
    }
}