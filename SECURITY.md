# Security Policy

## Status

```text
repository: jsonwisdom/COMPUTERWISDOM
authority: false
truth_claim: false
security_boundary: SECURITY_BOUNDARY.md
```

## Scope

This repository is operationally sensitive because it may contain signing logic, deployment preparation, KMS routing documentation, workflow gates, receipt manifests, revocation tooling, and access-control patterns.

It must not contain live private keys, seed phrases, wallet exports, service-account JSON files, or unreviewed payment adapters.

The canonical security boundary is maintained in:

```text
SECURITY_BOUNDARY.md
```

## Reporting Security Issues

Open a GitHub issue only for non-sensitive security hardening requests.

Do not publish secrets, private keys, service-account JSON, access tokens, wallet exports, or exploit material in public issues, pull requests, comments, screenshots, or logs.

For any suspected key exposure:

1. stop using the exposed key immediately;
2. rotate the key or credential;
3. record the rotation as a receipt without exposing the secret;
4. update `SECURITY_BOUNDARY.md` with the rotation event;
5. verify no workflow still depends on the revoked credential.

## Required Security Posture

```text
No committed keys.
No unreviewed live payment adapters.
No authority elevation by merge alone.
No production claim without receipt.
No secret remediation by history rewrite alone.
```

## Branch Protection Target

The intended branch-protection posture is:

- pull request required before merge;
- at least two approvals for protected production/root branches where available;
- required status checks for verifier workflows;
- signed commits preferred;
- rulesets mirrored into repo artifacts where possible.

Actual GitHub settings must be verified through GitHub repository settings and documented in `SECURITY_BOUNDARY.md` or a receipt artifact.

## Receipt Rule

Security changes should include a receipt with:

- commit hash;
- affected files;
- risk class;
- operator action;
- verification method;
- remaining limitations.
