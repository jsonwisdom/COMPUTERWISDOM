<!-- Observer Compliance badge pending first passing CI run -->

# REGISTRY_README_V1

Registry: JAYWISDOM_MCP_REGISTRY_V1  
Anchor Identity: jaywisdom.base.eth  
Authority: NONE  
Boundary: REGISTRY_IS_NOT_GOVERNMENT_AUTHORITY

## Purpose

This registry organizes public federal AI observer portals under a shared constitutional namespace.

It does not create offices.  
It does not issue policy.  
It does not represent government authority.  
It only records public signals and receipt paths.

## Four Inviolable Rules

1. OBSERVER_IS_NOT_OFFICE
2. MEDIA_REPORT_IS_NOT_BINDING_LAW
3. ADVISORY_APPOINTMENT_IS_NOT_EXECUTIVE_ORDER
4. CORROBORATION_IS_NOT_AUTHORITY

## Hard Brake Logic

Reject any child where:

- `is_federal_authority` is not `false`
- `mutates_existing_records` is not `false`
- `writes` is not `APPEND_ONLY_RECEIPTS`
- `.gov` / Federal Register confirmation is missing but authority is claimed

## Canon

Truth enters through receipts, not titles.
