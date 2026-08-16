// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IEAS} from "@eas/IEAS.sol";
import {IdentityBindingResolver} from "../src/IdentityBindingResolver.sol";

interface Vm {
    function startBroadcast() external;
    function stopBroadcast() external;
}

/// @title DeployIdentityResolverBaseSepolia
/// @notice Fail-closed deployment script for the dedicated JSONWisdom identity resolver.
/// @dev The script contains no private key handling. The signer is supplied by the Foundry CLI.
contract DeployIdentityResolverBaseSepolia {
    error WrongChain(uint256 actualChainId);
    error DeploymentInvariantFailed();

    Vm private constant vm = Vm(address(uint160(uint256(keccak256("hevm cheat code")))));

    uint256 public constant BASE_SEPOLIA_CHAIN_ID = 84532;
    address public constant BASE_SEPOLIA_EAS = 0x4200000000000000000000000000000000000021;
    address public constant EXPECTED_ATTESTER = 0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5;

    function run() external returns (IdentityBindingResolver resolver) {
        if (block.chainid != BASE_SEPOLIA_CHAIN_ID) revert WrongChain(block.chainid);

        vm.startBroadcast();
        resolver = new IdentityBindingResolver(IEAS(BASE_SEPOLIA_EAS), EXPECTED_ATTESTER);
        vm.stopBroadcast();

        if (resolver.expectedAttester() != EXPECTED_ATTESTER) revert DeploymentInvariantFailed();
        if (resolver.isPayable()) revert DeploymentInvariantFailed();
    }
}
