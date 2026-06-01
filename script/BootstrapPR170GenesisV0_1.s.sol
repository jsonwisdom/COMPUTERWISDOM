// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import "forge-std/Script.sol";
import "../contracts/CanonReceiptRegistryV0_1.sol";

/// @notice Bootstrap script for V0_1. Sets genesis only. No signed receipt in V0_1.
/// @dev Per Deprecation Notice: V0_1 is scaffold only. Run after deployment.
contract BootstrapPR170GenesisV0_1 is Script {
    bytes32 constant GENESIS_COMMIT = 0x0b58518ad17b73252be9a5fbfef7d74d8dc57254;

    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        CanonReceiptRegistryV0_1 registry = new CanonReceiptRegistryV0_1();
        registry.setGenesis(GENESIS_COMMIT);

        vm.stopBroadcast();

        console.log("CanonReceiptRegistryV0_1 deployed at:", address(registry));
        console.log("Genesis locked to:", vm.toString(GENESIS_COMMIT));
    }
}
