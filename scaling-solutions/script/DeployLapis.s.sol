// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Script, console} from "forge-std/Script.sol";
import {LapisRootRegistry} from "../src/LapisRootRegistry.sol";

contract DeployLapis is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("DEPLOYER_PRIVATE_KEY");

        vm.startBroadcast(deployerPrivateKey);

        LapisRootRegistry registry = new LapisRootRegistry();
        console.log("LapisRootRegistry deployed at:", address(registry));

        bytes32 genesisRoot = vm.envBytes32("GENESIS_MERKLE_ROOT");
        registry.anchor(genesisRoot);

        vm.stopBroadcast();

        console.log("Genesis Root Anchored:", vm.toString(genesisRoot));
    }
}
