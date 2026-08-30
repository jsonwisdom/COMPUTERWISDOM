# MICROSOFT_365_CUSTOMER_KEY_CUSTODY_RECEIPT_V0.2

CLASS: ASSERTION / VERIFICATION EVIDENCE
SCHEMA_VERSION: GIBSON_MICROSOFT_KEY_SOVEREIGNTY_V0.2
BINDS: Microsoft 365 Customer Key

## Bounded claim
Determine what Microsoft 365 Customer Key documentation proves about customer-controlled keys, the Microsoft-protected availability key, fallback behavior, and whether revoking customer keys proves Microsoft can no longer decrypt protected data.

## Documented findings

1. Microsoft 365 Customer Key uses two customer-managed root keys stored in Azure Key Vault or Managed HSM for supported DEP configurations.
2. Microsoft 365 also generates and protects an availability key. Customers cannot directly access it; Microsoft 365 service code can use it programmatically.
3. For Exchange and multi-workload DEPs, the DEP key is stored encrypted under each of the two customer keys and under the availability key.
4. For Exchange and multi-workload, if both customer-key unwrap attempts fail because of system errors, Microsoft 365 can fall back to the availability key. Access-denied failures do not automatically trigger fallback for ordinary user actions.
5. Microsoft documentation states internal operations such as indexing, anti-malware, eDiscovery, DLP, and mailbox moves may still fall back to the availability key while it remains available.
6. SharePoint/OneDrive uses a different hierarchy. The tenant intermediate key is protected by the two customer keys and an availability-key recovery copy, and availability-key use requires explicit recovery through Microsoft Support rather than transient fallback.
7. Microsoft documents that customers have authority to disable or destroy the availability key when leaving the service, but this receipt does not contain tenant-specific proof that such destruction has completed for any tenant.
8. NIST SP 800-57 Part 1 Rev. 5 treats key management as a lifecycle problem involving generation, storage, distribution, use, recovery, and destruction; therefore a claim of cryptographic separation requires evidence for the relevant lifecycle state, not only possession of customer-managed keys.

## Replay disposition

CLAIM: "Revoking both customer KEKs makes the tenant data unreadable to Microsoft."
STATUS: HOLD
REASON: Microsoft documents an availability-key path and workload-specific fallback/recovery behavior. Customer-key revocation alone does not prove completion of availability-key destruction or tenant-wide cryptographic erasure.

CLAIM: "Microsoft always continues to decrypt after customer KEK revocation."
STATUS: DELTA
REASON: Documentation distinguishes system-error fallback, access-denied behavior, internal operations, and workload-specific recovery. The behavior is not universal.

CLAIM: "Customer Key gives customers control over root keys."
STATUS: MATCH_WITH_SCOPE
REASON: Customers control their two customer-managed root keys, while Microsoft separately protects an availability key used for resilience/recovery according to workload-specific rules.

## Required evidence to move HOLD

- tenant-specific DEP identifier(s)
- workload(s) covered
- current customer-key status
- availability-key status
- documented disable/destroy completion or service-side purge/exit completion evidence
- replay timestamp and authoritative readback

## Sources

- Microsoft Learn: Learn about the availability key for Customer Key
- Microsoft Learn: Roll or rotate a Customer Key or an availability key
- Microsoft Learn: Overview of Customer Key
- NIST SP 800-57 Part 1 Rev. 5, Recommendation for Key Management: Part 1 – General

## Invariants

DOCUMENTED != INFERRED
CAPABILITY != AUTHORITY
HOSTING != OWNERSHIP
ACCESS != CUSTODY
REVOKE != PROOF_OF_BLINDNESS
WORKLOAD_A != WORKLOAD_B
ABSENCE != PROOF

facts_promoted: 0
authority_created: false
master_mutated: false
merge_performed: false
