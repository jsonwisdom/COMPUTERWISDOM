// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ClarityEngine} from "../src/ClarityEngine.sol";
import {JWIS} from "../src/JWIS.sol";
import {MockUSDC} from "../src/MockUSDC.sol";

interface Vm {
    function prank(address) external;
    function warp(uint256) external;
    function expectRevert(bytes4) external;
    function expectRevert(bytes calldata) external;
}

contract ClarityEngineTest {
    Vm private constant vm = Vm(address(uint160(uint256(keccak256("hevm cheat code")))));

    address private constant OWNER = address(0xA11CE);
    address private constant TREASURY = address(0xBEEF);
    address private constant FULFILLER = address(0xF011);
    address private constant CUSTOMER = address(0xCAFE);
    address private constant STRANGER = address(0xBAD);

    MockUSDC private usdc;
    ClarityEngine private engine;
    JWIS private jwis;

    function setUp() public {
        usdc = new MockUSDC(address(this), 1_000_000_000);
        engine = new ClarityEngine(
            address(usdc),
            OWNER,
            TREASURY,
            FULFILLER,
            keccak256("JAY_CLARITY_V0_1")
        );
        jwis = engine.jwisToken();

        usdc.transfer(CUSTOMER, 100_000_000);
        vm.prank(CUSTOMER);
        usdc.approve(address(engine), type(uint256).max);
    }

    function testOneDollarPriceUsesSixDecimalStablecoinUnits() public view {
        ClarityEngine.ServiceConfig memory config =
            engine.getServiceConfig(ClarityEngine.ServiceType.CLARITY_RUBRIC);
        _assertEq(config.price, 1_000_000, "wrong one-dollar price");
        _assertEq(config.jwisReward, 1 ether, "wrong JWIS reward");
    }

    function testPurchaseAndFulfillSettlesTreasuryAndMintsReward() public {
        uint256 orderId = _purchaseOneDollar();
        _assertEq(usdc.balanceOf(address(engine)), 1_000_000, "escrow missing");

        ClarityEngine.ClarityCommitment memory clarity = _validClarity();
        bytes32 resultHash = keccak256("human-and-machine-result");
        bytes32 humanUriHash = keccak256("ipfs://human");
        bytes32 machineUriHash = keccak256("ipfs://machine");

        vm.prank(FULFILLER);
        engine.fulfill(
            orderId,
            clarity,
            resultHash,
            humanUriHash,
            machineUriHash,
            ClarityEngine.FindingState.COMPLETE
        );

        _assertEq(usdc.balanceOf(TREASURY), 1_000_000, "treasury not paid");
        _assertEq(jwis.balanceOf(CUSTOMER), 1 ether, "JWIS reward missing");

        ClarityEngine.Order memory order = engine.getOrder(orderId);
        _assertEq(
            uint256(order.status),
            uint256(ClarityEngine.OrderStatus.FULFILLED),
            "order not fulfilled"
        );
        _assertEq(order.clarityScore, 100, "clarity score not complete");

        ClarityEngine.ReplayComparison comparison = engine.verifyReplay(
            orderId,
            clarity,
            resultHash,
            humanUriHash,
            machineUriHash,
            ClarityEngine.FindingState.COMPLETE
        );
        _assertEq(
            uint256(comparison),
            uint256(ClarityEngine.ReplayComparison.MATCH),
            "replay did not match"
        );
    }

    function testReplayDivergesWhenEvidenceChanges() public {
        uint256 orderId = _purchaseOneDollar();
        ClarityEngine.ClarityCommitment memory clarity = _validClarity();
        bytes32 resultHash = keccak256("result");
        bytes32 humanUriHash = keccak256("human");
        bytes32 machineUriHash = keccak256("machine");

        vm.prank(FULFILLER);
        engine.fulfill(
            orderId,
            clarity,
            resultHash,
            humanUriHash,
            machineUriHash,
            ClarityEngine.FindingState.COMPLETE
        );

        clarity.requiredEvidence = keccak256("changed-evidence");
        ClarityEngine.ReplayComparison comparison = engine.verifyReplay(
            orderId,
            clarity,
            resultHash,
            humanUriHash,
            machineUriHash,
            ClarityEngine.FindingState.COMPLETE
        );

        _assertEq(
            uint256(comparison),
            uint256(ClarityEngine.ReplayComparison.DIVERGE),
            "changed evidence should diverge"
        );
    }

    function testCustomerRefundsAfterDeadline() public {
        uint256 beforeBalance = usdc.balanceOf(CUSTOMER);
        uint256 orderId = _purchaseOneDollar();
        ClarityEngine.Order memory order = engine.getOrder(orderId);

        vm.warp(uint256(order.deadline) + 1);
        vm.prank(CUSTOMER);
        engine.refund(orderId);

        _assertEq(usdc.balanceOf(CUSTOMER), beforeBalance, "refund missing");
        _assertEq(usdc.balanceOf(address(engine)), 0, "escrow not cleared");
    }

    function testUnauthorizedFulfillerCannotSettleRevenue() public {
        uint256 orderId = _purchaseOneDollar();

        vm.expectRevert(ClarityEngine.NotFulfiller.selector);
        vm.prank(STRANGER);
        engine.fulfill(
            orderId,
            _validClarity(),
            keccak256("result"),
            keccak256("human"),
            keccak256("machine"),
            ClarityEngine.FindingState.COMPLETE
        );
    }

    function testMissingClarityFieldCannotFulfill() public {
        uint256 orderId = _purchaseOneDollar();
        ClarityEngine.ClarityCommitment memory clarity = _validClarity();
        clarity.controllingAuthority = bytes32(0);

        vm.expectRevert(
            abi.encodeWithSelector(ClarityEngine.MissingClarityField.selector, uint8(0))
        );
        vm.prank(FULFILLER);
        engine.fulfill(
            orderId,
            clarity,
            keccak256("result"),
            keccak256("human"),
            keccak256("machine"),
            ClarityEngine.FindingState.COMPLETE
        );
    }

    function testOnlyEngineCanMintJWIS() public {
        vm.expectRevert(JWIS.NotMinter.selector);
        vm.prank(STRANGER);
        jwis.mint(STRANGER, 1 ether);
    }

    function _purchaseOneDollar() internal returns (uint256 orderId) {
        vm.prank(CUSTOMER);
        orderId = engine.purchase(
            ClarityEngine.ServiceType.CLARITY_RUBRIC,
            keccak256("bounded customer question")
        );
    }

    function _validClarity()
        internal
        pure
        returns (ClarityEngine.ClarityCommitment memory clarity)
    {
        clarity = ClarityEngine.ClarityCommitment({
            controllingAuthority: keccak256("controlling authority"),
            lawfulPurpose: keccak256("lawful purpose"),
            responsibleActor: keccak256("responsible actor"),
            requiredEvidence: keccak256("required evidence"),
            instrumentsEnablements: keccak256("instruments and enablements"),
            trackingCustody: keccak256("tracking and custody"),
            remedyAppeal: keccak256("remedy and appeal")
        });
    }

    function _assertEq(uint256 observed, uint256 expected, string memory message) internal pure {
        require(observed == expected, message);
    }
}
