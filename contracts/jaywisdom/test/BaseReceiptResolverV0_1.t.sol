// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "forge-std/Test.sol";
import {
    BaseReceiptResolverV0_1,
    EASAttestationV0_1
} from "../src/BaseReceiptResolverV0_1.sol";

contract MockEASReceiptLookupV0_1 {
    mapping(bytes32 => EASAttestationV0_1) internal attestations;

    function setAttestation(
        bytes32 uid,
        EASAttestationV0_1 calldata attestation
    ) external {
        attestations[uid] = attestation;
    }

    function getAttestation(
        bytes32 uid
    ) external view returns (EASAttestationV0_1 memory) {
        return attestations[uid];
    }
}

contract BaseReceiptResolverV0_1Test is Test {
    MockEASReceiptLookupV0_1 internal eas;
    BaseReceiptResolverV0_1 internal resolver;

    bytes32 internal constant SOURCE_SCHEMA =
        keccak256("source-schema");
    bytes32 internal constant SOURCE_UID =
        keccak256("source-attestation");

    function setUp() external {
        vm.chainId(8453);

        eas = new MockEASReceiptLookupV0_1();
        resolver = new BaseReceiptResolverV0_1(address(eas));

        EASAttestationV0_1 memory source = EASAttestationV0_1({
            uid: SOURCE_UID,
            schema: SOURCE_SCHEMA,
            time: uint64(block.timestamp),
            expirationTime: 0,
            revocationTime: 0,
            refUID: bytes32(0),
            recipient: address(0xBEEF),
            attester: address(0xA11CE),
            revocable: true,
            data: ""
        });

        eas.setAttestation(SOURCE_UID, source);
    }

    function testAcceptsWellFormedReceipt() external {
        EASAttestationV0_1 memory candidate = _candidate(
            SOURCE_SCHEMA,
            SOURCE_UID,
            SOURCE_UID
        );

        vm.prank(address(eas));
        assertTrue(resolver.attest(candidate));
    }

    function testRejectsWrongRefUID() external {
        EASAttestationV0_1 memory candidate = _candidate(
            SOURCE_SCHEMA,
            SOURCE_UID,
            bytes32(uint256(123))
        );

        vm.expectRevert(
            BaseReceiptResolverV0_1.RefUIDMismatch.selector
        );
        vm.prank(address(eas));
        resolver.attest(candidate);
    }

    function testRejectsWrongSourceSchema() external {
        EASAttestationV0_1 memory candidate = _candidate(
            keccak256("wrong-schema"),
            SOURCE_UID,
            SOURCE_UID
        );

        vm.expectRevert(
            BaseReceiptResolverV0_1.SourceSchemaMismatch.selector
        );
        vm.prank(address(eas));
        resolver.attest(candidate);
    }

    function testRejectsNonEASCaller() external {
        EASAttestationV0_1 memory candidate = _candidate(
            SOURCE_SCHEMA,
            SOURCE_UID,
            SOURCE_UID
        );

        vm.expectRevert(BaseReceiptResolverV0_1.AccessDenied.selector);
        resolver.attest(candidate);
    }

    function _candidate(
        bytes32 sourceSchemaUID,
        bytes32 sourceAttestationUID,
        bytes32 refUID
    ) internal view returns (EASAttestationV0_1 memory) {
        bytes memory data = abi.encode(
            uint256(8453), // chainId
            sourceSchemaUID,
            sourceAttestationUID,
            keccak256("tx"), // txHash
            uint256(123456), // blockNumber
            keccak256("block"), // blockHash
            uint256(7), // transactionIndex
            address(0xA11CE), // from
            address(0xBEEF), // to
            uint256(100_000), // gasUsed
            uint256(500_000), // cumulativeGasUsed
            uint256(1 gwei), // effectiveGasPrice
            uint8(1), // status
            address(0), // contractAddress
            keccak256("logs") // logsHash
        );

        return
            EASAttestationV0_1({
                uid: bytes32(0),
                schema: keccak256("receipt-schema"),
                time: uint64(block.timestamp),
                expirationTime: 0,
                revocationTime: 0,
                refUID: refUID,
                recipient: address(0),
                attester: address(this),
                revocable: true,
                data: data
            });
    }
}
