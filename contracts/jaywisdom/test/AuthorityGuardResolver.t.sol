// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {AccessDenied, Attestation, InvalidEAS} from "@eas/Common.sol";
import {IEAS} from "@eas/IEAS.sol";

import {AuthorityGuardResolver} from "../src/AuthorityGuardResolver.sol";

interface Vm {
    function expectRevert() external;
    function expectRevert(bytes4) external;
    function warp(uint256) external;
}

contract MockEAS {
    error ResolverRejected();

    mapping(bytes32 => Attestation) private attestations;

    function setAttestation(Attestation memory attestation) external {
        attestations[attestation.uid] = attestation;
    }

    function getAttestation(bytes32 uid) external view returns (Attestation memory) {
        return attestations[uid];
    }

    function validateAttestation(
        AuthorityGuardResolver resolver,
        Attestation memory attestation
    ) external returns (bool) {
        bool accepted = resolver.attest(attestation);
        if (!accepted) revert ResolverRejected();
        return true;
    }

    function validateRevocation(
        AuthorityGuardResolver resolver,
        Attestation memory attestation
    ) external returns (bool) {
        bool accepted = resolver.revoke(attestation);
        if (!accepted) revert ResolverRejected();
        return true;
    }
}

contract AuthorityGuardResolverTest {
    Vm private constant vm = Vm(address(uint160(uint256(keccak256("hevm cheat code")))));

    bytes32 private constant IDENTITY_SCHEMA = keccak256("JSONWISDOM_IDENTITY_V1");
    bytes32 private constant PARENT_UID = keccak256("JAY_IDENTITY_ATTESTATION");
    bytes32 private constant RESUME_SCHEMA = keccak256("JSONWISDOM_RESUME_INTEGRITY_V3");
    bytes32 private constant RESUME_HASH =
        0x44749d0791d036eb0503ec597692b940d3665f85d1ce0db5455a552fcbdf5216;
    bytes32 private constant GIT_SHA1_PADDED =
        0x000000000000000000000000b27ce3f87da34a1b2618194a709d2edbee956528;

    address private constant IDENTITY_ATTESTER = address(0xA11CE);
    address private constant WRONG_ATTESTER = address(0xBAD);
    address private constant SUBJECT = address(0xCAFE);
    address private constant OTHER_SUBJECT = address(0xB0B);

    MockEAS private eas;
    AuthorityGuardResolver private resolver;

    function setUp() public {
        eas = new MockEAS();
        resolver = new AuthorityGuardResolver(
            IEAS(address(eas)),
            IDENTITY_SCHEMA,
            IDENTITY_ATTESTER
        );
        eas.setAttestation(_validIdentity(PARENT_UID));
    }

    function testValidSha1ResumePasses() public {
        Attestation memory resume = _validResume(PARENT_UID);
        require(eas.validateAttestation(resolver, resume), "valid SHA-1 resume rejected");
    }

    function testValidSha256ResumePasses() public {
        Attestation memory resume = _validResume(PARENT_UID);
        resume.data = abi.encode(
            RESUME_HASH,
            keccak256("sha256-git-object-id"),
            uint8(2),
            "resume-v1",
            false
        );

        require(eas.validateAttestation(resolver, resume), "valid SHA-256 resume rejected");
    }

    function testG1AuthorityCreatedTrueRejected() public {
        Attestation memory resume = _validResume(PARENT_UID);
        resume.data = abi.encode(
            RESUME_HASH,
            GIT_SHA1_PADDED,
            uint8(1),
            "resume-v1",
            true
        );

        _expectRejected(resume);
    }

    function testG2ZeroResumeHashRejected() public {
        Attestation memory resume = _validResume(PARENT_UID);
        resume.data = abi.encode(
            bytes32(0),
            GIT_SHA1_PADDED,
            uint8(1),
            "resume-v1",
            false
        );

        _expectRejected(resume);
    }

    function testG3UnsupportedGitHashAlgorithmRejected() public {
        Attestation memory resume = _validResume(PARENT_UID);
        resume.data = abi.encode(
            RESUME_HASH,
            GIT_SHA1_PADDED,
            uint8(3),
            "resume-v1",
            false
        );

        _expectRejected(resume);
    }

    function testG4ZeroRefUidRejected() public {
        Attestation memory resume = _validResume(bytes32(0));
        _expectRejected(resume);
    }

    function testG5MissingParentRejected() public {
        Attestation memory resume = _validResume(keccak256("MISSING_PARENT"));
        _expectRejected(resume);
    }

    function testG5WrongSchemaRejected() public {
        Attestation memory identity = _validIdentity(PARENT_UID);
        identity.schema = keccak256("WRONG_SCHEMA");
        eas.setAttestation(identity);

        _expectRejected(_validResume(PARENT_UID));
    }

    function testG5RevokedParentRejected() public {
        Attestation memory identity = _validIdentity(PARENT_UID);
        identity.revocationTime = uint64(block.timestamp);
        if (identity.revocationTime == 0) identity.revocationTime = 1;
        eas.setAttestation(identity);

        _expectRejected(_validResume(PARENT_UID));
    }

    function testG5ExpiredParentRejected() public {
        Attestation memory identity = _validIdentity(PARENT_UID);
        identity.expirationTime = uint64(block.timestamp + 10);
        eas.setAttestation(identity);
        vm.warp(block.timestamp + 10);

        _expectRejected(_validResume(PARENT_UID));
    }

    function testG5WrongAttesterRejected() public {
        Attestation memory identity = _validIdentity(PARENT_UID);
        identity.attester = WRONG_ATTESTER;
        eas.setAttestation(identity);

        _expectRejected(_validResume(PARENT_UID));
    }

    function testG5ZeroResumeRecipientRejected() public {
        Attestation memory resume = _validResume(PARENT_UID);
        resume.recipient = address(0);
        _expectRejected(resume);
    }

    function testG5IdentityRecipientMismatchRejected() public {
        Attestation memory identity = _validIdentity(PARENT_UID);
        identity.recipient = OTHER_SUBJECT;
        eas.setAttestation(identity);

        _expectRejected(_validResume(PARENT_UID));
    }

    function testMalformedPayloadFailsClosed() public {
        Attestation memory resume = _validResume(PARENT_UID);
        resume.data = hex"1234";

        vm.expectRevert();
        eas.validateAttestation(resolver, resume);
    }

    function testOnlyEASCanInvokeResolver() public {
        vm.expectRevert(AccessDenied.selector);
        resolver.attest(_validResume(PARENT_UID));
    }

    function testRevocationAllowedThroughEAS() public {
        require(
            eas.validateRevocation(resolver, _validResume(PARENT_UID)),
            "revocation unexpectedly rejected"
        );
    }

    function testResolverIsNotPayable() public view {
        require(!resolver.isPayable(), "resolver unexpectedly payable");
    }

    function testConstructorRejectsZeroEAS() public {
        vm.expectRevert(InvalidEAS.selector);
        new AuthorityGuardResolver(IEAS(address(0)), IDENTITY_SCHEMA, IDENTITY_ATTESTER);
    }

    function testConstructorRejectsZeroIdentitySchema() public {
        vm.expectRevert(AuthorityGuardResolver.InvalidIdentitySchema.selector);
        new AuthorityGuardResolver(IEAS(address(eas)), bytes32(0), IDENTITY_ATTESTER);
    }

    function testConstructorRejectsZeroIdentityAttester() public {
        vm.expectRevert(AuthorityGuardResolver.InvalidIdentityAttester.selector);
        new AuthorityGuardResolver(IEAS(address(eas)), IDENTITY_SCHEMA, address(0));
    }

    function _expectRejected(Attestation memory resume) private {
        vm.expectRevert(MockEAS.ResolverRejected.selector);
        eas.validateAttestation(resolver, resume);
    }

    function _validIdentity(bytes32 uid) private view returns (Attestation memory) {
        return Attestation({
            uid: uid,
            schema: IDENTITY_SCHEMA,
            time: uint64(block.timestamp),
            expirationTime: 0,
            revocationTime: 0,
            refUID: bytes32(0),
            recipient: SUBJECT,
            attester: IDENTITY_ATTESTER,
            revocable: true,
            data: bytes("")
        });
    }

    function _validResume(bytes32 refUID) private view returns (Attestation memory) {
        return Attestation({
            uid: keccak256("JAY_WISDOM_RESUME_V1"),
            schema: RESUME_SCHEMA,
            time: uint64(block.timestamp),
            expirationTime: 0,
            revocationTime: 0,
            refUID: refUID,
            recipient: SUBJECT,
            attester: IDENTITY_ATTESTER,
            revocable: true,
            data: abi.encode(
                RESUME_HASH,
                GIT_SHA1_PADDED,
                uint8(1),
                "resume-v1",
                false
            )
        });
    }
}
