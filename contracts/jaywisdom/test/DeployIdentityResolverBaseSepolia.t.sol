// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {DeployIdentityResolverBaseSepolia} from "../script/DeployIdentityResolverBaseSepolia.s.sol";

interface VmDeployScriptTest {
    function expectRevert(bytes4) external;
}

contract DeployIdentityResolverBaseSepoliaTest {
    VmDeployScriptTest private constant vm =
        VmDeployScriptTest(address(uint160(uint256(keccak256("hevm cheat code")))));

    DeployIdentityResolverBaseSepolia private deployment;

    function setUp() public {
        deployment = new DeployIdentityResolverBaseSepolia();
    }

    function testLockedBaseSepoliaConstants() public view {
        require(deployment.BASE_SEPOLIA_CHAIN_ID() == 84532, "wrong chain id");
        require(
            deployment.BASE_SEPOLIA_EAS() == 0x4200000000000000000000000000000000000021,
            "wrong EAS address"
        );
        require(
            deployment.EXPECTED_ATTESTER() == 0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5,
            "wrong expected attester"
        );
    }

    function testRunFailsClosedOnWrongChain() public {
        if (block.chainid == 84532) return;

        vm.expectRevert(DeployIdentityResolverBaseSepolia.WrongChain.selector);
        deployment.run();
    }
}
