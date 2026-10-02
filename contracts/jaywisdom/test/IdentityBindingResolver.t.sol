// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {AccessDenied, Attestation, InvalidEAS} from "@eas/Common.sol";
import {IEAS} from "@eas/IEAS.sol";

import {IdentityBindingResolver} from "../src/IdentityBindingResolver.sol";

interface IdentityVm {
    function expectRevert() external;
    function expectRevert(bytes4) external;
}

contract MockIdentityEAS {
    error ResolverRejected();

    function validateAttestation(
        IdentityBindingResolver resolver,
        Attestation memory attestation
    ) external returns (bool) {
        bool accepted = resolver.attest(attestation);
        if (!accepted) revert ResolverRejected();
        return true;
    }

    function validateRevocation(
        IdentityBindingResolver resolver,
        Attestation memory attestation
    ) external returns (bool) {
        bool accepted = resolver.revoke(attestation);
        if (!accepted) revert ResolverRejected();
        return true;
    }
}

contract IdentityBindingResolverTest {
    IdentityVm private constant vm =
        IdentityVm(address(uint160(uint256(keccak256("hevm cheat code")))));

    bytes32 private constant IDENTITY_SCHEMA = keccak256("JSONWISDOM_IDENTITY_SCHEMA_V1");
    bytes32 private constant BINDING_HASH =
        0x102e70b50594e412b8f15d311cc4e04f5126a4405fb3b1d02652e3d11afeaf5b;

    address private constant EXPECTED_ATTESTER = address(0xA11CE);
    address private constant WRONG_ATTESTER = address(0xBAD);
    address private constant SUBJECT = address(0xCAFE);

    MockIdentityEAS private eas;
    IdentityBindingResolver private resolver;

    function setUp() public {
        eas = new MockIdentityEAS();
        resolver = new IdentityBindingResolver(IEAS(address(eas)), EXPECTED_ATTESTER);
    }

    function testValidIdentityRootPasses() public {
        require(
            eas.validateAttestation(resolver, _validIdentity()),
            "valid identity root rejected"
        );
    }

    function testI1WrongAttesterRejected() public {
        Attestation memory identity = _validIdentity();
        identity.attester = WRONG_ATTESTER;
        _expectRejected(identity);
    }

    function testI2ZeroRecipientRejected() public {
        Attestation memory identity = _validIdentity();
        identity.recipient = address(0);
        _expectRejected(identity);
    }

    function testI3ZeroBindingHashRejected() public {
        Attestation memory identity = _validIdentity();
        identity.data = abi.encode(bytes32(0), "jaywisdom.base.eth", "jay-identity-v1", false);
        _expectRejected(identity);
    }

    function testI4EmptySubjectAnchorRejected() public {
        Attestation memory identity = _validIdentity();
        identity.data = abi.encode(BINDING_HASH, "", "jay-identity-v1", false);
        _expectRejected(identity);
    }

    function testI5EmptyArtifactIdRejected() public {
        Attestation memory identity = _validIdentity();
        identity.data = abi.encode(BINDING_HASH, "jaywisdom.base.eth", "", false);
        _expectRejected(identity);
    }

    function testI6AuthorityCreatedTrueRejected() public {
        Attestation memory identity = _validIdentity();
        identity.data = abi.encode(
            BINDING_HASH,
            "jaywisdom.base.eth",
            "jay-identity-v1",
            true
        );
        _expectRejected(identity);
    }

    function testI7NonzeroRefUidRejected() public {
        Attestation memory identity = _validIdentity();
        identity.refUID = keccak256("PARENT_NOT_ALLOWED");
        _expectRejected(identity);
    }

    function testMalformedPayloadFailsClosed() public {
        Attestation memory identity = _validIdentity();
        identity.data = hex"1234";

        vm.expectRevert();
        eas.validateAttestation(resolver, identity);
    }

    function testOnlyEASCanInvokeResolver() public {
        vm.expectRevert(AccessDenied.selector);
        resolver.attest(_validIdentity());
    }

    function testRevocationAllowedThroughEAS() public {
        require(
            eas.validateRevocation(resolver, _validIdentity()),
            "revocation unexpectedly rejected"
        );
    }

    function testResolverIsNotPayable() public view {
        require(!resolver.isPayable(), "resolver unexpectedly payable");
    }

    function testConstructorRejectsZeroEAS() public {
        vm.expectRevert(InvalidEAS.selector);
        new IdentityBindingResolver(IEAS(address(0)), EXPECTED_ATTESTER);
    }

    function testConstructorRejectsZeroExpectedAttester() public {
        vm.expectRevert(IdentityBindingResolver.InvalidExpectedAttester.selector);
        new IdentityBindingResolver(IEAS(address(eas)), address(0));
    }

    function testExpectedAttesterIsImmutableBinding() public view {
        require(resolver.expectedAttester() == EXPECTED_ATTESTER, "attester binding mismatch");
    }

    function _expectRejected(Attestation memory identity) private {
        vm.expectRevert(MockIdentityEAS.ResolverRejected.selector);
        eas.validateAttestation(resolver, identity);
    }

    function _validIdentity() private view returns (Attestation memory) {
        return Attestation({
            uid: keccak256("JAY_IDENTITY_ROOT_V1"),
            schema: IDENTITY_SCHEMA,
            time: uint64(block.timestamp),
            expirationTime: 0,
            revocationTime: 0,
            refUID: bytes32(0),
            recipient: SUBJECT,
            attester: EXPECTED_ATTESTER,
            revocable: true,
            data: abi.encode(
                BINDING_HASH,
                "jaywisdom.base.eth",
                "jay-identity-v1",
                false
            )
        });
    }
}
