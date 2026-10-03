// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "forge-std/Test.sol";
import {BaseReceiptResolverV0_1, BaseReceiptPayloadV0_1, EASAttestationV0_1} from "../src/BaseReceiptResolverV0_1.sol";

contract MockEASReceiptLookupV0_1 {
    mapping(bytes32 => EASAttestationV0_1) internal attestations;

    function setAttestation(bytes32 uid, EASAttestationV0_1 calldata attestation) external {
        attestations[uid] = attestation;
    }

    function setRevocationTime(bytes32 uid, uint64 revocationTime) external {
        attestations[uid].revocationTime = revocationTime;
    }

    function getAttestation(bytes32 uid) external view returns (EASAttestationV0_1 memory) {
        return attestations[uid];
    }
}

/// @dev Shared fixtures. Payloads are encoded as a single static struct, which
///      is byte-identical to encoding the 15 fields as a flat tuple and avoids
///      the legacy-codegen "Stack too deep" error from a 15-argument abi.encode.
abstract contract BaseReceiptResolverFixtureV0_1 is Test {
    MockEASReceiptLookupV0_1 internal eas;
    BaseReceiptResolverV0_1 internal resolver;

    uint256 internal constant T0 = 1_700_000_000;

    address internal constant ATTESTER_A = address(0xA77E57A);
    address internal constant ATTESTER_B = address(0xA77E57B);
    address internal constant UNKNOWN_ATTESTER = address(0xBAD);
    address internal constant SOURCE_ATTESTER = address(0x5011CE);

    bytes32 internal constant SOURCE_SCHEMA = keccak256("source-schema");
    bytes32 internal constant SOURCE_UID = keccak256("source-attestation");
    bytes32 internal constant RECEIPT_UID = keccak256("receipt-attestation");

    function _deploy(uint256 chainId) internal {
        vm.chainId(chainId);
        vm.warp(T0);

        eas = new MockEASReceiptLookupV0_1();
        resolver = new BaseReceiptResolverV0_1(address(eas), chainId, _attesters());

        _storeSource(0, 0);
    }

    function _attesters() internal pure returns (address[] memory attesters) {
        attesters = new address[](2);
        attesters[0] = ATTESTER_A;
        attesters[1] = ATTESTER_B;
    }

    function _storeSource(uint64 expirationTime, uint64 revocationTime) internal {
        eas.setAttestation(
            SOURCE_UID,
            EASAttestationV0_1({
                uid: SOURCE_UID,
                schema: SOURCE_SCHEMA,
                time: uint64(T0 - 1),
                expirationTime: expirationTime,
                revocationTime: revocationTime,
                refUID: bytes32(0),
                recipient: address(0xBEEF),
                attester: SOURCE_ATTESTER,
                revocable: true,
                data: ""
            })
        );
    }

    function _payload() internal view returns (BaseReceiptPayloadV0_1 memory p) {
        p.chainId = block.chainid;
        p.sourceSchemaUID = SOURCE_SCHEMA;
        p.sourceAttestationUID = SOURCE_UID;
        p.txHash = keccak256("tx");
        p.blockNumber = 123456;
        p.blockHash = keccak256("block");
        p.transactionIndex = 7;
        p.from = address(0xA11CE);
        p.to = address(0xBEEF);
        p.gasUsed = 100_000;
        p.cumulativeGasUsed = 500_000;
        p.effectiveGasPrice = 1 gwei;
        p.status = 1;
        p.contractAddress = address(0);
        p.logsHash = keccak256("logs");
    }

    function _receipt(BaseReceiptPayloadV0_1 memory p) internal view returns (EASAttestationV0_1 memory) {
        return EASAttestationV0_1({
            uid: RECEIPT_UID,
            schema: resolver.RECEIPT_SCHEMA_UID(),
            time: uint64(block.timestamp),
            expirationTime: 0,
            revocationTime: 0,
            refUID: p.sourceAttestationUID,
            recipient: address(0),
            attester: ATTESTER_A,
            revocable: true,
            data: abi.encode(p)
        });
    }

    function _good() internal view returns (EASAttestationV0_1 memory) {
        return _receipt(_payload());
    }

    function _attestAsEAS(EASAttestationV0_1 memory a) internal returns (bool) {
        vm.prank(address(eas));
        return resolver.attest(a);
    }

    function _expectAttestRevert(EASAttestationV0_1 memory a, bytes memory err) internal {
        vm.expectRevert(err);
        vm.prank(address(eas));
        resolver.attest(a);
    }

    function _expectAttestRevert(EASAttestationV0_1 memory a, bytes4 selector) internal {
        _expectAttestRevert(a, abi.encodeWithSelector(selector));
    }

    function _status(bytes32 uid) internal view returns (uint8) {
        return uint8(resolver.receiptStatus(uid));
    }

    function _storeReceipt(EASAttestationV0_1 memory a) internal {
        eas.setAttestation(a.uid, a);
    }
}

/// @notice Production chain path: Base mainnet, chain id 8453.
contract BaseReceiptResolverV0_1Test is BaseReceiptResolverFixtureV0_1 {
    function setUp() external {
        _deploy(8453);
    }

    // ------------------------------------------------------------------
    // Happy paths
    // ------------------------------------------------------------------

    function testAcceptsWellFormedReceipt() external {
        assertTrue(_attestAsEAS(_good()));
    }

    function testAcceptsSecondAuthorizedAttester() external {
        EASAttestationV0_1 memory a = _good();
        a.attester = ATTESTER_B;
        assertTrue(_attestAsEAS(a));
    }

    // ------------------------------------------------------------------
    // Constructor (S04 constructor zero-EAS rejection, S03, S05)
    // ------------------------------------------------------------------

    function testConstructorRejectsZeroEAS() external {
        vm.expectRevert(BaseReceiptResolverV0_1.InvalidEAS.selector);
        new BaseReceiptResolverV0_1(address(0), 8453, _attesters());
    }

    function testConstructorRejectsUnsupportedChainId() external {
        vm.chainId(1);
        vm.expectRevert(abi.encodeWithSelector(BaseReceiptResolverV0_1.UnsupportedChainId.selector, uint256(1)));
        new BaseReceiptResolverV0_1(address(eas), 1, _attesters());
    }

    function testConstructorRejectsSepoliaChainIdOnMainnet() external {
        vm.expectRevert(
            abi.encodeWithSelector(
                BaseReceiptResolverV0_1.DeploymentChainMismatch.selector, uint256(84532), uint256(8453)
            )
        );
        new BaseReceiptResolverV0_1(address(eas), 84532, _attesters());
    }

    function testConstructorRejectsEmptyAttesterSet() external {
        vm.expectRevert(BaseReceiptResolverV0_1.EmptyAttesterSet.selector);
        new BaseReceiptResolverV0_1(address(eas), 8453, new address[](0));
    }

    function testConstructorRejectsZeroAttester() external {
        address[] memory attesters = new address[](1);
        vm.expectRevert(abi.encodeWithSelector(BaseReceiptResolverV0_1.InvalidAttester.selector, address(0)));
        new BaseReceiptResolverV0_1(address(eas), 8453, attesters);
    }

    function testConstructorRejectsDuplicateAttester() external {
        address[] memory attesters = new address[](2);
        attesters[0] = ATTESTER_A;
        attesters[1] = ATTESTER_A;
        vm.expectRevert(abi.encodeWithSelector(BaseReceiptResolverV0_1.DuplicateAttester.selector, ATTESTER_A));
        new BaseReceiptResolverV0_1(address(eas), 8453, attesters);
    }

    function testPolicyGetters() external view {
        assertEq(resolver.EAS(), address(eas));
        assertEq(resolver.CHAIN_ID(), 8453);
        assertEq(resolver.ATTESTER_COUNT(), 2);
        assertTrue(resolver.isAuthorizedAttester(ATTESTER_A));
        assertTrue(resolver.isAuthorizedAttester(ATTESTER_B));
        assertFalse(resolver.isAuthorizedAttester(UNKNOWN_ATTESTER));
        assertFalse(resolver.isAuthorizedAttester(address(0)));
        assertTrue(resolver.RECEIPT_REVOCABLE());
        assertEq(resolver.RECEIPT_EXPIRATION_TIME(), 0);
        assertFalse(resolver.SOURCE_ATTESTER_CONSTRAINED());
        assertFalse(resolver.isPayable());
        assertEq(resolver.version(), "1.1.0");
    }

    // ------------------------------------------------------------------
    // S06 receipt-schema binding
    // ------------------------------------------------------------------

    function testReceiptSchemaUIDMatchesSchemaRegistryDerivation() external view {
        string memory schema = resolver.RECEIPT_SCHEMA();
        bytes32 expected = keccak256(abi.encodePacked(schema, address(resolver), true));
        assertEq(resolver.RECEIPT_SCHEMA_UID(), expected);
        assertTrue(resolver.RECEIPT_SCHEMA_UID() != keccak256(abi.encodePacked(schema, address(0), true)));
        assertTrue(resolver.RECEIPT_SCHEMA_UID() != keccak256(abi.encodePacked(schema, address(resolver), false)));
    }

    function testReceiptSchemaStringIsThe15FieldSchema() external view {
        assertEq(
            resolver.RECEIPT_SCHEMA(),
            "uint256 chainId,bytes32 schemaUID,bytes32 attestationUID,bytes32 txHash,uint256 blockNumber,bytes32 blockHash,uint256 transactionIndex,address from,address to,uint256 gasUsed,uint256 cumulativeGasUsed,uint256 effectiveGasPrice,uint8 status,address contractAddress,bytes32 logsHash"
        );
    }

    function testRejectsWrongReceiptSchema() external {
        EASAttestationV0_1 memory a = _good();
        a.schema = keccak256("receipt-schema");
        _expectAttestRevert(
            a,
            abi.encodeWithSelector(
                BaseReceiptResolverV0_1.WrongReceiptSchema.selector, a.schema, resolver.RECEIPT_SCHEMA_UID()
            )
        );
    }

    function testRejectsNonRevocableSchemaVariantUID() external {
        EASAttestationV0_1 memory a = _good();
        a.schema = keccak256(abi.encodePacked(resolver.RECEIPT_SCHEMA(), address(resolver), false));
        _expectAttestRevert(
            a,
            abi.encodeWithSelector(
                BaseReceiptResolverV0_1.WrongReceiptSchema.selector, a.schema, resolver.RECEIPT_SCHEMA_UID()
            )
        );
    }

    // ------------------------------------------------------------------
    // S03 attester policy
    // ------------------------------------------------------------------

    function testRejectsUnknownAttester() external {
        EASAttestationV0_1 memory a = _good();
        a.attester = UNKNOWN_ATTESTER;
        _expectAttestRevert(
            a, abi.encodeWithSelector(BaseReceiptResolverV0_1.UnauthorizedAttester.selector, UNKNOWN_ATTESTER)
        );
    }

    function testRejectsZeroAttester() external {
        EASAttestationV0_1 memory a = _good();
        a.attester = address(0);
        _expectAttestRevert(
            a, abi.encodeWithSelector(BaseReceiptResolverV0_1.UnauthorizedAttester.selector, address(0))
        );
    }

    function testSourceAttesterIsNotConstrained() external {
        // The stored source attester (SOURCE_ATTESTER) is not in the receipt
        // attester set; policy SOURCE_ATTESTER_CONSTRAINED = false.
        assertFalse(resolver.isAuthorizedAttester(SOURCE_ATTESTER));
        assertTrue(_attestAsEAS(_good()));
    }

    // ------------------------------------------------------------------
    // S07 receipt lifecycle policy
    // ------------------------------------------------------------------

    function testRejectsNonRevocableReceipt() external {
        EASAttestationV0_1 memory a = _good();
        a.revocable = false;
        _expectAttestRevert(a, BaseReceiptResolverV0_1.ReceiptMustBeRevocable.selector);
    }

    function testRejectsReceiptWithExpirationTime() external {
        EASAttestationV0_1 memory a = _good();
        a.expirationTime = uint64(T0 + 365 days);
        _expectAttestRevert(
            a,
            abi.encodeWithSelector(BaseReceiptResolverV0_1.ReceiptExpirationNotAllowed.selector, uint64(T0 + 365 days))
        );
    }

    // ------------------------------------------------------------------
    // S04 negative matrix: source attestation
    // ------------------------------------------------------------------

    function testRejectsNonexistentSourceUID() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.sourceAttestationUID = keccak256("missing-source");
        _expectAttestRevert(_receipt(p), BaseReceiptResolverV0_1.SourceAttestationNotFound.selector);
    }

    function testRejectsRevokedSource() external {
        _storeSource(0, uint64(T0 - 1));
        _expectAttestRevert(_good(), BaseReceiptResolverV0_1.SourceAttestationRevoked.selector);
    }

    function testRejectsExpiredSource() external {
        _storeSource(uint64(T0 - 1), 0);
        _expectAttestRevert(_good(), BaseReceiptResolverV0_1.SourceAttestationExpired.selector);
    }

    function testRejectsSourceAtExactExpirationBoundary() external {
        // now == expirationTime counts as expired.
        _storeSource(uint64(T0), 0);
        assertEq(block.timestamp, T0);
        _expectAttestRevert(_good(), BaseReceiptResolverV0_1.SourceAttestationExpired.selector);
    }

    function testAcceptsSourceOneSecondBeforeExpiration() external {
        _storeSource(uint64(T0 + 1), 0);
        assertTrue(_attestAsEAS(_good()));
    }

    function testFuzzSourceExpiryBoundary(uint64 expirationTime) external {
        _storeSource(expirationTime, 0);
        bool shouldPass = expirationTime == 0 || expirationTime > block.timestamp;
        if (shouldPass) {
            assertTrue(_attestAsEAS(_good()));
        } else {
            _expectAttestRevert(_good(), BaseReceiptResolverV0_1.SourceAttestationExpired.selector);
        }
    }

    function testRejectsWrongSourceSchema() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.sourceSchemaUID = keccak256("wrong-schema");
        _expectAttestRevert(_receipt(p), BaseReceiptResolverV0_1.SourceSchemaMismatch.selector);
    }

    function testRejectsWrongRefUID() external {
        EASAttestationV0_1 memory a = _good();
        a.refUID = bytes32(uint256(123));
        _expectAttestRevert(a, BaseReceiptResolverV0_1.RefUIDMismatch.selector);
    }

    function testRejectsZeroSourceSchemaUID() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.sourceSchemaUID = bytes32(0);
        _expectAttestRevert(_receipt(p), BaseReceiptResolverV0_1.MissingSourceReference.selector);
    }

    function testRejectsZeroSourceAttestationUID() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.sourceAttestationUID = bytes32(0);
        _expectAttestRevert(_receipt(p), BaseReceiptResolverV0_1.MissingSourceReference.selector);
    }

    // ------------------------------------------------------------------
    // S04 negative matrix: chain id (S05)
    // ------------------------------------------------------------------

    function testRejectsWrongPayloadChainId() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.chainId = 1;
        _expectAttestRevert(
            _receipt(p),
            abi.encodeWithSelector(BaseReceiptResolverV0_1.InvalidChainId.selector, uint256(1), uint256(8453))
        );
    }

    function testProductionRejectsSepoliaPayloadChainId() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.chainId = 84532;
        _expectAttestRevert(
            _receipt(p),
            abi.encodeWithSelector(BaseReceiptResolverV0_1.InvalidChainId.selector, uint256(84532), uint256(8453))
        );
    }

    function testProductionRejectsWhenExecutingOnSepolia() external {
        EASAttestationV0_1 memory a = _good();
        vm.chainId(84532);
        _expectAttestRevert(
            a, abi.encodeWithSelector(BaseReceiptResolverV0_1.InvalidChainId.selector, uint256(8453), uint256(84532))
        );
    }

    function testProductionRejectsSepoliaPayloadEvenOnSepoliaExecution() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.chainId = 84532;
        EASAttestationV0_1 memory a = _receipt(p);
        vm.chainId(84532);
        _expectAttestRevert(
            a, abi.encodeWithSelector(BaseReceiptResolverV0_1.InvalidChainId.selector, uint256(84532), uint256(84532))
        );
    }

    // ------------------------------------------------------------------
    // S04 negative matrix: receipt fields
    // ------------------------------------------------------------------

    function testRejectsZeroTxHash() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.txHash = bytes32(0);
        _expectAttestRevert(_receipt(p), BaseReceiptResolverV0_1.MissingReceiptHash.selector);
    }

    function testRejectsZeroBlockHash() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.blockHash = bytes32(0);
        _expectAttestRevert(_receipt(p), BaseReceiptResolverV0_1.MissingReceiptHash.selector);
    }

    function testRejectsZeroLogsHash() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.logsHash = bytes32(0);
        _expectAttestRevert(_receipt(p), BaseReceiptResolverV0_1.MissingReceiptHash.selector);
    }

    function testRejectsStatusTwo() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.status = 2;
        _expectAttestRevert(
            _receipt(p), abi.encodeWithSelector(BaseReceiptResolverV0_1.InvalidStatus.selector, uint8(2))
        );
    }

    function testRejectsStatusMax() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.status = type(uint8).max;
        _expectAttestRevert(
            _receipt(p), abi.encodeWithSelector(BaseReceiptResolverV0_1.InvalidStatus.selector, type(uint8).max)
        );
    }

    function testAcceptsStatusZero() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.status = 0;
        assertTrue(_attestAsEAS(_receipt(p)));
    }

    function testRejectsZeroFrom() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.from = address(0);
        _expectAttestRevert(_receipt(p), BaseReceiptResolverV0_1.InvalidSender.selector);
    }

    function testRejectsContractAddressOnNormalCall() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.contractAddress = address(0xC0DE);
        _expectAttestRevert(_receipt(p), BaseReceiptResolverV0_1.InvalidContractAddress.selector);
    }

    function testAcceptsContractCreation() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.to = address(0);
        p.contractAddress = address(0xC0DE);
        assertTrue(_attestAsEAS(_receipt(p)));
    }

    function testAcceptsFailedContractCreation() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.to = address(0);
        p.contractAddress = address(0);
        p.status = 0;
        assertTrue(_attestAsEAS(_receipt(p)));
    }

    function testRejectsGasUsedAboveCumulative() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.gasUsed = p.cumulativeGasUsed + 1;
        _expectAttestRevert(_receipt(p), BaseReceiptResolverV0_1.InvalidGasAccounting.selector);
    }

    function testAcceptsGasUsedEqualToCumulative() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.gasUsed = p.cumulativeGasUsed;
        assertTrue(_attestAsEAS(_receipt(p)));
    }

    function testRejectsMalformedPayload() external {
        EASAttestationV0_1 memory a = _good();
        a.data = hex"1234";
        vm.expectRevert();
        vm.prank(address(eas));
        resolver.attest(a);
    }

    // ------------------------------------------------------------------
    // S04 nonzero value rejection
    // ------------------------------------------------------------------

    function testAttestRejectsNonzeroValue() external {
        EASAttestationV0_1 memory a = _good();
        vm.deal(address(eas), 1 ether);
        vm.expectRevert(BaseReceiptResolverV0_1.InvalidValue.selector);
        vm.prank(address(eas));
        resolver.attest{value: 1}(a);
    }

    function testMultiAttestRejectsNonzeroMsgValue() external {
        (EASAttestationV0_1[] memory list, uint256[] memory values) = _list(_good(), _good());
        vm.deal(address(eas), 1 ether);
        vm.expectRevert(BaseReceiptResolverV0_1.InvalidValue.selector);
        vm.prank(address(eas));
        resolver.multiAttest{value: 1}(list, values);
    }

    function testMultiAttestRejectsNonzeroElementValue() external {
        (EASAttestationV0_1[] memory list, uint256[] memory values) = _list(_good(), _good());
        values[1] = 1;
        vm.expectRevert(BaseReceiptResolverV0_1.InvalidValue.selector);
        vm.prank(address(eas));
        resolver.multiAttest(list, values);
    }

    function testRevokeRejectsNonzeroValue() external {
        EASAttestationV0_1 memory a = _good();
        vm.deal(address(eas), 1 ether);
        vm.expectRevert(BaseReceiptResolverV0_1.InvalidValue.selector);
        vm.prank(address(eas));
        resolver.revoke{value: 1}(a);
    }

    function testMultiRevokeRejectsNonzeroMsgValue() external {
        (EASAttestationV0_1[] memory list, uint256[] memory values) = _list(_good(), _good());
        vm.deal(address(eas), 1 ether);
        vm.expectRevert(BaseReceiptResolverV0_1.InvalidValue.selector);
        vm.prank(address(eas));
        resolver.multiRevoke{value: 1}(list, values);
    }

    function testMultiRevokeRejectsNonzeroElementValue() external {
        (EASAttestationV0_1[] memory list, uint256[] memory values) = _list(_good(), _good());
        values[0] = 1;
        vm.expectRevert(BaseReceiptResolverV0_1.InvalidValue.selector);
        vm.prank(address(eas));
        resolver.multiRevoke(list, values);
    }

    function testReceiveRejectsEther() external {
        vm.deal(address(this), 1 ether);
        (bool ok, bytes memory ret) = address(resolver).call{value: 1}("");
        assertFalse(ok);
        assertEq(bytes4(ret), BaseReceiptResolverV0_1.InvalidValue.selector);
    }

    // ------------------------------------------------------------------
    // S04 multiAttest / revoke / multiRevoke paths and EAS-only access
    // ------------------------------------------------------------------

    function testRejectsNonEASCaller() external {
        EASAttestationV0_1 memory a = _good();
        vm.expectRevert(BaseReceiptResolverV0_1.AccessDenied.selector);
        resolver.attest(a);
    }

    function testMultiAttestAcceptsAllValid() external {
        EASAttestationV0_1 memory b = _good();
        b.attester = ATTESTER_B;
        (EASAttestationV0_1[] memory list, uint256[] memory values) = _list(_good(), b);
        vm.prank(address(eas));
        assertTrue(resolver.multiAttest(list, values));
    }

    function testMultiAttestRejectsIfAnyInvalid() external {
        EASAttestationV0_1 memory bad = _good();
        bad.attester = UNKNOWN_ATTESTER;
        (EASAttestationV0_1[] memory list, uint256[] memory values) = _list(_good(), bad);
        vm.expectRevert(abi.encodeWithSelector(BaseReceiptResolverV0_1.UnauthorizedAttester.selector, UNKNOWN_ATTESTER));
        vm.prank(address(eas));
        resolver.multiAttest(list, values);
    }

    function testMultiAttestRejectsLengthMismatch() external {
        (EASAttestationV0_1[] memory list,) = _list(_good(), _good());
        vm.expectRevert(BaseReceiptResolverV0_1.InvalidLength.selector);
        vm.prank(address(eas));
        resolver.multiAttest(list, new uint256[](1));
    }

    function testMultiAttestRejectsNonEASCaller() external {
        (EASAttestationV0_1[] memory list, uint256[] memory values) = _list(_good(), _good());
        vm.expectRevert(BaseReceiptResolverV0_1.AccessDenied.selector);
        resolver.multiAttest(list, values);
    }

    function testRevokeAcceptsReceiptSchema() external {
        EASAttestationV0_1 memory a = _good();
        vm.prank(address(eas));
        assertTrue(resolver.revoke(a));
    }

    function testRevokeRejectsForeignSchema() external {
        EASAttestationV0_1 memory a = _good();
        a.schema = keccak256("foreign");
        vm.expectRevert(
            abi.encodeWithSelector(
                BaseReceiptResolverV0_1.WrongReceiptSchema.selector, a.schema, resolver.RECEIPT_SCHEMA_UID()
            )
        );
        vm.prank(address(eas));
        resolver.revoke(a);
    }

    function testRevokeRejectsNonEASCaller() external {
        EASAttestationV0_1 memory a = _good();
        vm.expectRevert(BaseReceiptResolverV0_1.AccessDenied.selector);
        resolver.revoke(a);
    }

    function testMultiRevokeAcceptsReceiptSchema() external {
        (EASAttestationV0_1[] memory list, uint256[] memory values) = _list(_good(), _good());
        vm.prank(address(eas));
        assertTrue(resolver.multiRevoke(list, values));
    }

    function testMultiRevokeRejectsForeignSchema() external {
        EASAttestationV0_1 memory foreign = _good();
        foreign.schema = keccak256("foreign");
        (EASAttestationV0_1[] memory list, uint256[] memory values) = _list(_good(), foreign);
        vm.expectRevert(
            abi.encodeWithSelector(
                BaseReceiptResolverV0_1.WrongReceiptSchema.selector, foreign.schema, resolver.RECEIPT_SCHEMA_UID()
            )
        );
        vm.prank(address(eas));
        resolver.multiRevoke(list, values);
    }

    function testMultiRevokeRejectsLengthMismatch() external {
        (EASAttestationV0_1[] memory list,) = _list(_good(), _good());
        vm.expectRevert(BaseReceiptResolverV0_1.InvalidLength.selector);
        vm.prank(address(eas));
        resolver.multiRevoke(list, new uint256[](3));
    }

    function testMultiRevokeRejectsNonEASCaller() external {
        (EASAttestationV0_1[] memory list, uint256[] memory values) = _list(_good(), _good());
        vm.expectRevert(BaseReceiptResolverV0_1.AccessDenied.selector);
        resolver.multiRevoke(list, values);
    }

    // ------------------------------------------------------------------
    // S02 source validity remains enforced after attestation
    // ------------------------------------------------------------------

    function testReceiptValidAfterAttestation() external {
        EASAttestationV0_1 memory a = _good();
        assertTrue(_attestAsEAS(a));
        _storeReceipt(a);
        assertTrue(resolver.isReceiptValid(RECEIPT_UID));
        assertEq(_status(RECEIPT_UID), uint8(BaseReceiptResolverV0_1.ReceiptStatus.VALID));
    }

    function testReceiptInvalidAfterSourceRevoked() external {
        EASAttestationV0_1 memory a = _good();
        assertTrue(_attestAsEAS(a));
        _storeReceipt(a);
        assertTrue(resolver.isReceiptValid(RECEIPT_UID));

        vm.warp(T0 + 10);
        eas.setRevocationTime(SOURCE_UID, uint64(T0 + 10));

        assertFalse(resolver.isReceiptValid(RECEIPT_UID));
        assertEq(_status(RECEIPT_UID), uint8(BaseReceiptResolverV0_1.ReceiptStatus.SOURCE_REVOKED));
    }

    function testReceiptInvalidOnceSourceReachesExpiration() external {
        _storeSource(uint64(T0 + 100), 0);
        EASAttestationV0_1 memory a = _good();
        assertTrue(_attestAsEAS(a));
        _storeReceipt(a);

        vm.warp(T0 + 99);
        assertTrue(resolver.isReceiptValid(RECEIPT_UID));

        vm.warp(T0 + 100); // exact boundary: now == expirationTime
        assertFalse(resolver.isReceiptValid(RECEIPT_UID));
        assertEq(_status(RECEIPT_UID), uint8(BaseReceiptResolverV0_1.ReceiptStatus.SOURCE_EXPIRED));
    }

    function testReceiptInvalidAfterReceiptRevoked() external {
        EASAttestationV0_1 memory a = _good();
        _storeReceipt(a);
        eas.setRevocationTime(RECEIPT_UID, uint64(T0));
        assertFalse(resolver.isReceiptValid(RECEIPT_UID));
        assertEq(_status(RECEIPT_UID), uint8(BaseReceiptResolverV0_1.ReceiptStatus.RECEIPT_REVOKED));
    }

    function testReceiptStatusNotFound() external view {
        assertEq(_status(bytes32(0)), uint8(BaseReceiptResolverV0_1.ReceiptStatus.RECEIPT_NOT_FOUND));
        assertEq(_status(keccak256("unknown")), uint8(BaseReceiptResolverV0_1.ReceiptStatus.RECEIPT_NOT_FOUND));
        assertFalse(resolver.isReceiptValid(keccak256("unknown")));
    }

    function testReceiptStatusWrongSchema() external {
        EASAttestationV0_1 memory a = _good();
        a.schema = keccak256(abi.encodePacked(resolver.RECEIPT_SCHEMA(), address(0), true)); // zero-resolver schema
        _storeReceipt(a);
        assertEq(_status(RECEIPT_UID), uint8(BaseReceiptResolverV0_1.ReceiptStatus.WRONG_RECEIPT_SCHEMA));
        assertFalse(resolver.isReceiptValid(RECEIPT_UID));
    }

    function testReceiptStatusUnauthorizedAttester() external {
        EASAttestationV0_1 memory a = _good();
        a.attester = UNKNOWN_ATTESTER;
        _storeReceipt(a);
        assertEq(_status(RECEIPT_UID), uint8(BaseReceiptResolverV0_1.ReceiptStatus.UNAUTHORIZED_ATTESTER));
    }

    function testReceiptStatusReceiptExpired() external {
        EASAttestationV0_1 memory a = _good();
        a.expirationTime = uint64(T0);
        _storeReceipt(a);
        assertEq(_status(RECEIPT_UID), uint8(BaseReceiptResolverV0_1.ReceiptStatus.RECEIPT_EXPIRED));
    }

    function testReceiptStatusSourceNotFound() external {
        EASAttestationV0_1 memory a = _good();
        a.refUID = keccak256("missing-source");
        _storeReceipt(a);
        assertEq(_status(RECEIPT_UID), uint8(BaseReceiptResolverV0_1.ReceiptStatus.SOURCE_NOT_FOUND));

        a.refUID = bytes32(0);
        _storeReceipt(a);
        assertEq(_status(RECEIPT_UID), uint8(BaseReceiptResolverV0_1.ReceiptStatus.SOURCE_NOT_FOUND));
    }

    function _list(EASAttestationV0_1 memory a, EASAttestationV0_1 memory b)
        internal
        pure
        returns (EASAttestationV0_1[] memory list, uint256[] memory values)
    {
        list = new EASAttestationV0_1[](2);
        list[0] = a;
        list[1] = b;
        values = new uint256[](2);
    }
}

/// @notice S05 test path: Base Sepolia, chain id 84532.
contract BaseReceiptResolverV0_1SepoliaTest is BaseReceiptResolverFixtureV0_1 {
    function setUp() external {
        _deploy(84532);
    }

    function testSepoliaDeploymentBindsSepoliaChainId() external view {
        assertEq(resolver.CHAIN_ID(), 84532);
        assertEq(
            resolver.RECEIPT_SCHEMA_UID(),
            keccak256(abi.encodePacked(resolver.RECEIPT_SCHEMA(), address(resolver), true))
        );
    }

    function testSepoliaAcceptsSepoliaReceipt() external {
        assertEq(_payload().chainId, 84532);
        assertTrue(_attestAsEAS(_good()));
    }

    function testSepoliaRejectsMainnetPayloadChainId() external {
        BaseReceiptPayloadV0_1 memory p = _payload();
        p.chainId = 8453;
        _expectAttestRevert(
            _receipt(p),
            abi.encodeWithSelector(BaseReceiptResolverV0_1.InvalidChainId.selector, uint256(8453), uint256(84532))
        );
    }

    function testSepoliaConstructorRejectsMainnetChainId() external {
        vm.expectRevert(
            abi.encodeWithSelector(
                BaseReceiptResolverV0_1.DeploymentChainMismatch.selector, uint256(8453), uint256(84532)
            )
        );
        new BaseReceiptResolverV0_1(address(eas), 8453, _attesters());
    }

    function testSepoliaSourceValidityPath() external {
        EASAttestationV0_1 memory a = _good();
        assertTrue(_attestAsEAS(a));
        _storeReceipt(a);
        assertTrue(resolver.isReceiptValid(RECEIPT_UID));

        eas.setRevocationTime(SOURCE_UID, uint64(T0));
        assertFalse(resolver.isReceiptValid(RECEIPT_UID));
    }
}
