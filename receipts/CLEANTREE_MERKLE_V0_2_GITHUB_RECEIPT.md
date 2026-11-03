# CleanTree Merkle v0.2 GitHub Receipt

```json
{
  "artifact": "CLEANTREE_MERKLE_V0_2",
  "repository": "jsonwisdom/COMPUTERWISDOM",
  "branch": "agent/cleantree-merkle-v0-2-attestation",
  "verified_candidate_commit": "d6cc917c8e21d29ab4aea67a8d2eea9f7c015eb9",
  "powershell_patch": {
    "path": "tools/cleantree/Invoke-JSONWisdomCleanTreeMerkle.ps1",
    "bytes": 9707,
    "sha256": "594462292b688385f9c6a8018bdace01130e84df8bd5b42aba8d3756f5ae329d"
  },
  "regression_test": {
    "path": "tests/test_cleantree_merkle_vector.py",
    "bytes": 2386,
    "sha256": "7ff21e1d63f9ad45222cfb4ef6b44b4ba2fe4a41dd82a05f7c40cce7edc41b30",
    "result": "2/2_PASS"
  },
  "expected_fixture_root": "656020bb502588bf3cd0574a6890950ccec3c5ffd2f2e4551594c8d13e32677a",
  "rejected_windows_v0_1_root": "b5aff300e2fa84af1009df2ff97e13c395e718e7767bf2878cf281d8e7630d52",
  "windows_powershell_v0_2_rerun": "NOT_RUN",
  "onchain_attestation_submitted": false,
  "transaction_hash": null,
  "attestation_uid": null,
  "wallet_signature": "HUMAN_ONLY",
  "authority_created": false,
  "next_transition": "WINDOWS_RERUNS_SYNTHETIC_VECTOR"
}
```

## Evidence

The v0.1 Windows run used PowerShell 7.6.4. All three leaf hashes matched the independent vector, while culture-dependent case-insensitive ordering produced the rejected root. The v0.2 candidate converts repository/path UTF-8 bytes to an ASCII hexadecimal sort key before Merkle construction.

Two Python regression tests pass:

1. UTF-8 ordinal ordering produces the expected root.
2. The former Windows ordering reproduces the rejected root.

## Boundary

This receipt binds the GitHub code candidate and regression tests. It does not claim that v0.2 has passed on Windows, scanned a real repository, produced a real inventory root, signed a wallet payload, or submitted an on-chain attestation.

```text
PATCH_CANDIDATE_MATERIALIZED = TRUE
PYTHON_REGRESSION_TESTS      = 2/2_PASS
WINDOWS_V0_2_TEST            = NOT_RUN
REAL_INVENTORY               = NOT_RUN
ONCHAIN_ATTESTATION          = NOT_SUBMITTED
AUTHORITY_CREATED            = FALSE
```
