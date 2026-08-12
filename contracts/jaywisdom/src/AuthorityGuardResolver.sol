// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Attestation, IEAS} from "@eas/IEAS.sol";
import {SchemaResolver} from "@eas/resolver/SchemaResolver.sol";

/// @title AuthorityGuardResolver
/// @notice Fail-closed EAS resolver for the JSONWisdom on-chain resume integrity schema.
/// @dev This contract intentionally has no owner, proxy, upgrade hook, or mutable governance state.
///      The EAS address, identity schema UID, and identity attester are immutable constructor bindings.
contract AuthorityGuardResolver is SchemaResolver {
    error InvalidIdentitySchema();
    error InvalidIdentityAttester();

    uint8 public constant GIT_HASH_SHA1 = 1;
    uint8 public constant GIT_HASH_SHA256 = 2;

    bytes32 public immutable expectedIdentitySchema;
    address public immutable expectedIdentityAttester;

    /// @param eas Global EAS contract for the target chain.
    /// @param identitySchema UID of the identity/provenance schema that a resume attestation must reference.
    /// @param identityAttester Address authorized to issue the referenced identity/provenance attestation.
    constructor(IEAS eas, bytes32 identitySchema, address identityAttester) SchemaResolver(eas) {
        if (identitySchema == bytes32(0)) revert InvalidIdentitySchema();
        if (identityAttester == address(0)) revert InvalidIdentityAttester();

        expectedIdentitySchema = identitySchema;
        expectedIdentityAttester = identityAttester;
    }

    /// @dev Enforces the locked Resolver v3 gates.
    ///
    /// Resume schema payload:
    /// (bytes32 resumeHash, bytes32 gitCommit, uint8 gitHashAlg, string artifactId, bool authorityCreated)
    ///
    /// G1: authorityCreated == false
    /// G2: resumeHash != bytes32(0)
    /// G3: gitHashAlg is SHA-1 (1) or SHA-256 (2)
    /// G4: refUID != bytes32(0)
    /// G5: referenced identity attestation exists, uses the expected schema, is not revoked,
    ///     is not expired, and was issued by the expected attester.
    function onAttest(Attestation calldata attestation, uint256) internal view override returns (bool) {
        (
            bytes32 resumeHash,
            bytes32 gitCommit,
            uint8 gitHashAlg,
            string memory artifactId,
            bool authorityCreated
        ) = abi.decode(attestation.data, (bytes32, bytes32, uint8, string, bool));

        // Preserve the complete schema decoding even though these two values are not independent v3 gates.
        gitCommit;
        artifactId;

        // G1 — authority cannot be created by this schema.
        if (authorityCreated) return false;

        // G2 — an empty resume digest cannot be admitted.
        if (resumeHash == bytes32(0)) return false;

        // G3 — the Git object-id interpretation must be explicit and supported.
        if (gitHashAlg != GIT_HASH_SHA1 && gitHashAlg != GIT_HASH_SHA256) return false;

        // G4 — a resume integrity claim must reference an identity/provenance attestation.
        if (attestation.refUID == bytes32(0)) return false;

        // G5 — existence is not authorization. Validate the referenced attestation semantically.
        Attestation memory identity = _eas.getAttestation(attestation.refUID);
        if (identity.uid != attestation.refUID) return false;
        if (identity.schema != expectedIdentitySchema) return false;
        if (identity.revocationTime != 0) return false;
        if (identity.expirationTime != 0 && identity.expirationTime <= block.timestamp) return false;
        if (identity.attester != expectedIdentityAttester) return false;

        return true;
    }

    /// @dev Revocation is permitted when the registered schema itself is revocable.
    ///      No mutable owner or administrative exception exists here.
    function onRevoke(Attestation calldata, uint256) internal pure override returns (bool) {
        return true;
    }
}
