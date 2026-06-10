// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import "forge-std/Test.sol";
import "../contracts/CanonReceiptRegistryV0_1.sol";
import "../contracts/interfaces/ICanonReceiptRegistryV0_1.sol";

contract CanonReceiptRegistryV0_1Test is Test {
    CanonReceiptRegistryV0_1 registry;
    address deployer = address(0xA11CE);
    address actor1 = address(0xB0B);
    address actor2 = address(0xCAFE);
    bytes32 constant GENESIS_COMMIT = 0x0b58518ad17b73252be9a5fbfef7d74d8dc57254;

    event GenesisLocked(bytes32 indexed genesisCommit, address indexed operator);
    event ReceiptAnchored(
        bytes32 indexed receiptHash,
        address indexed actor,
        bytes32 indexed mergeCommit,
        string proofRef,
        string actionType,
        string status
    );
    event CanonSignalEmitted(
        bytes32 indexed targetReceipt,
        ICanonReceiptRegistryV0_1.CanonSignal signal,
        string reasonRef,
        address indexed emitter
    );

    function setUp() public {
        vm.prank(deployer);
        registry = new CanonReceiptRegistryV0_1();
    }

    function _mkReceipt(address _actor, bytes32 _mergeCommit) internal pure returns (ICanonReceiptRegistryV0_1.Receipt memory) {
        return ICanonReceiptRegistryV0_1.Receipt({
            actor: _actor,
            actionType: "PR_REPLAY",
            evidenceHash: keccak256("ipfs://evidence"),
            al: "PROTECT",
            joy: "WITNESS",
            computerWisdom: "APPEND_ONLY",
            proofRef: "PR_170",
            mergeCommit: _mergeCommit,
            status: "MERGED_REPLAYED_CLOSED"
        });
    }

    function test_anchor_before_genesis_reverts() public {
        ICanonReceiptRegistryV0_1.Receipt memory r = _mkReceipt(actor1, GENESIS_COMMIT);
        vm.prank(actor1);
        vm.expectRevert("Genesis required");
        registry.anchorReceipt(r);
    }

    function test_set_genesis_once_only() public {
        vm.prank(deployer);
        vm.expectEmit(true, true, false, true);
        emit GenesisLocked(GENESIS_COMMIT, deployer);
        registry.setGenesis(GENESIS_COMMIT);

        assertTrue(registry.genesisSet());
        assertEq(registry.genesisCommit(), GENESIS_COMMIT);

        vm.prank(deployer);
        vm.expectRevert("Genesis: locked_once");
        registry.setGenesis(GENESIS_COMMIT);
    }

    function test_zero_genesis_reverts() public {
        vm.prank(deployer);
        vm.expectRevert("Genesis: zero commit");
        registry.setGenesis(bytes32(0));
    }

    function test_anchor_receipt_after_genesis() public {
        vm.prank(deployer);
        registry.setGenesis(GENESIS_COMMIT);

        ICanonReceiptRegistryV0_1.Receipt memory r = _mkReceipt(actor1, GENESIS_COMMIT);
        vm.prank(actor1);
        vm.expectEmit(true, true, true, true);
        emit ReceiptAnchored(bytes32(0), actor1, GENESIS_COMMIT, "PR_170", "PR_REPLAY", "MERGED_REPLAYED_CLOSED");
        bytes32 hash = registry.anchorReceipt(r);

        assertTrue(registry.receiptExists(hash));
        assertEq(registry.receiptActor(hash), actor1);
        assertEq(registry.receiptCount(), 1);
    }

    function test_duplicate_receipt_reverts() public {
        vm.prank(deployer);
        registry.setGenesis(GENESIS_COMMIT);

        ICanonReceiptRegistryV0_1.Receipt memory r = _mkReceipt(actor1, GENESIS_COMMIT);
        vm.prank(actor1);
        registry.anchorReceipt(r);

        vm.prank(actor1);
        vm.expectRevert("Append_only: exists");
        registry.anchorReceipt(r);
    }

    function test_signal_unknown_receipt_reverts() public {
        vm.prank(deployer);
        registry.setGenesis(GENESIS_COMMIT);

        bytes32 fakeHash = keccak256("fake");
        vm.prank(actor2);
        vm.expectRevert("Target!exists");
        registry.emitCanonSignal(fakeHash, ICanonReceiptRegistryV0_1.CanonSignal.DISPUTED, "reason://test");
    }

    function test_signal_known_receipt_emits_overlay() public {
        vm.prank(deployer);
        registry.setGenesis(GENESIS_COMMIT);

        ICanonReceiptRegistryV0_1.Receipt memory r = _mkReceipt(actor1, GENESIS_COMMIT);
        vm.prank(actor1);
        bytes32 hash = registry.anchorReceipt(r);

        vm.prank(actor2);
        vm.expectEmit(true, false, false, true);
        emit CanonSignalEmitted(hash, ICanonReceiptRegistryV0_1.CanonSignal.PAUSED_FOR_REPLAY, "reason://replay", actor2);
        registry.emitCanonSignal(hash, ICanonReceiptRegistryV0_1.CanonSignal.PAUSED_FOR_REPLAY, "reason://replay");
    }

    function test_signal_does_not_change_anchored_status() public {
        vm.prank(deployer);
        registry.setGenesis(GENESIS_COMMIT);

        ICanonReceiptRegistryV0_1.Receipt memory r = _mkReceipt(actor1, GENESIS_COMMIT);
        vm.prank(actor1);
        bytes32 hash = registry.anchorReceipt(r);

        uint256 countBefore = registry.receiptCount();
        address actorBefore = registry.receiptActor(hash);

        vm.prank(actor2);
        registry.emitCanonSignal(hash, ICanonReceiptRegistryV0_1.CanonSignal.DISPUTED, "reason://dispute");

        assertEq(registry.receiptCount(), countBefore);
        assertEq(registry.receiptActor(hash), actorBefore);
        assertTrue(registry.receiptExists(hash));
    }

    function test_blocked_truths_revert() public {
        vm.prank(deployer);
        registry.setGenesis(GENESIS_COMMIT);

        string[4] memory blocked = ["VERIFIED", "FALSE", "FRAUD", "ADJUDICATED"];
        for (uint i = 0; i < 4; i++) {
            ICanonReceiptRegistryV0_1.Receipt memory r = _mkReceipt(actor1, GENESIS_COMMIT);
            r.status = blocked[i];
            vm.prank(actor1);
            vm.expectRevert("BlockedTruth");
            registry.anchorReceipt(r);
        }
    }

    function test_trinity_incomplete_reverts() public {
        vm.prank(deployer);
        registry.setGenesis(GENESIS_COMMIT);

        ICanonReceiptRegistryV0_1.Receipt memory r = _mkReceipt(actor1, GENESIS_COMMIT);
        r.al = "";
        vm.prank(actor1);
        vm.expectRevert("AL missing");
        registry.anchorReceipt(r);

        r = _mkReceipt(actor1, GENESIS_COMMIT);
        r.joy = "";
        vm.prank(actor1);
        vm.expectRevert("JOY missing");
        registry.anchorReceipt(r);

        r = _mkReceipt(actor1, GENESIS_COMMIT);
        r.computerWisdom = "MUTABLE";
        vm.prank(actor1);
        vm.expectRevert("CW must be APPEND_ONLY");
        registry.anchorReceipt(r);
    }

    function test_v0_1_actor_must_be_msg_sender() public {
        vm.prank(deployer);
        registry.setGenesis(GENESIS_COMMIT);

        ICanonReceiptRegistryV0_1.Receipt memory r = _mkReceipt(actor2, GENESIS_COMMIT);
        vm.prank(actor1);
        vm.expectRevert("V0_1: actor must be msg.sender");
        registry.anchorReceipt(r);
    }

    function test_first_receipt_must_match_genesis() public {
        vm.prank(deployer);
        registry.setGenesis(GENESIS_COMMIT);

        ICanonReceiptRegistryV0_1.Receipt memory r = _mkReceipt(actor1, bytes32(uint256(0xDEAD)));
        vm.prank(actor1);
        vm.expectRevert("First receipt must match genesis");
        registry.anchorReceipt(r);
    }

    function test_subsequent_receipts_can_diverge_commit() public {
        vm.prank(deployer);
        registry.setGenesis(GENESIS_COMMIT);

        ICanonReceiptRegistryV0_1.Receipt memory r1 = _mkReceipt(actor1, GENESIS_COMMIT);
        vm.prank(actor1);
        registry.anchorReceipt(r1);

        ICanonReceiptRegistryV0_1.Receipt memory r2 = _mkReceipt(actor2, bytes32(uint256(0xBEEF)));
        vm.prank(actor2);
        bytes32 hash2 = registry.anchorReceipt(r2);
        assertTrue(registry.receiptExists(hash2));
        assertEq(registry.receiptCount(), 2);
    }
}
