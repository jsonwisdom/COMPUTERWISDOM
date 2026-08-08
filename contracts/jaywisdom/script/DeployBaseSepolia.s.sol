// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ClarityEngine} from "../src/ClarityEngine.sol";

interface Vm {
    function envAddress(string calldata name) external returns (address value);
    function envBytes32(string calldata name) external returns (bytes32 value);
    function startBroadcast() external;
    function stopBroadcast() external;
}

contract DeployBaseSepolia {
    Vm private constant vm = Vm(address(uint160(uint256(keccak256("hevm cheat code")))));

    function run() external returns (ClarityEngine engine) {
        address paymentToken = vm.envAddress("PAYMENT_TOKEN");
        address initialOwner = vm.envAddress("JAY_OWNER");
        address treasury = vm.envAddress("JAY_TREASURY");
        address fulfiller = vm.envAddress("JAY_FULFILLER");
        bytes32 rubricVersion = vm.envBytes32("RUBRIC_VERSION");

        vm.startBroadcast();
        engine = new ClarityEngine(
            paymentToken,
            initialOwner,
            treasury,
            fulfiller,
            rubricVersion
        );
        vm.stopBroadcast();
    }
}
