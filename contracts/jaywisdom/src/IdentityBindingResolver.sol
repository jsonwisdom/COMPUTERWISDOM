// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Attestation, IEAS} from "@eas/IEAS.sol";
import {SchemaResolver} from "@eas/resolver/SchemaResolver.sol";

/// @title IdentityBindingResolver
/// @notice Fail-closed EAS resolver for the JSONWisdom dedicated identity-binding schema.
/// @dev No owner, proxy, upgrade hook, mutable allowlist, or governance setter exists.
contract IdentityBindingResolver is SchemaResolver {
    error InvalidExpectedAttester();

    address public immutable expectedAttester;

    /// @param eas Global EAS contract for the target chain.
    /// @param attester Immutable address permitted to issue identity-root attestations.
    constructor(IEAS eas, address attester) SchemaResolver(eas) {
        if (attester == address(0)) revert InvalidExpectedAttester();
        expectedAttester = attester;
    }

    /// @dev Identity schema payload:
    /// (bytes32 bindingHash, string subjectAnchor, string artifactId, bool authorityCreated)
    ///
    /// I1: attester == expectedAttester
    /// I2: recipient != address(0)
    /// I3: bindingHash != bytes32(0)
    /// I4: subjectAnchor is nonempty
    /// I5: artifactId is nonempty
    /// I6: authorityCreated == false
    /// I7: refUID == bytes32(0)
    function onAttest(Attestation calldata attestation, uint256) internal view override returns (bool) {
        (
            bytes32 bindingHash,
            string memory subjectAnchor,
            string memory artifactId,
            bool authorityCreated
        ) = abi.decode(attestation.data, (bytes32, string, string, bool));

        if (attestation.attester != expectedAttester) return false;
        if (attestation.recipient == address(0)) return false;
        if (bindingHash == bytes32(0)) return false;
        if (bytes(subjectAnchor).length == 0) return false;
        if (bytes(artifactId).length == 0) return false;
        if (authorityCreated) return false;
        if (attestation.refUID != bytes32(0)) return false;

        return true;
    }

    /// @dev Revocation remains available when the registered schema is revocable.
    function onRevoke(Attestation calldata, uint256) internal pure override returns (bool) {
        return true;
    }
}
