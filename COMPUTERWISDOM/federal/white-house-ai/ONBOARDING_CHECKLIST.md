# ONBOARDING_CHECKLIST

1. Create child folder:
   `federal-ai-observers/{PORTAL_NAME}/`

2. Copy:
   `federal-ai-observers/CHILD_TEMPLATE.json`

3. Replace:
   - `{PORTAL_NAME}`
   - `{TARGET_OFFICIAL}`
   - `{SYSTEM_ID}`
   - `{RECEIPT_PATH}`

4. Confirm locked fields:
   - `authority: "NONE"`
   - `is_federal_authority: false`
   - `mutates_existing_records: false`
   - `writes: "APPEND_ONLY_RECEIPTS"`

5. Add child to:
   `JAYWISDOM_MCP_REGISTRY_V1.json`

6. Run:
   `python3 scripts/verify_federal_observer_child.py path/to/child.json`

7. Only commit if verifier returns:
   `PASS`
