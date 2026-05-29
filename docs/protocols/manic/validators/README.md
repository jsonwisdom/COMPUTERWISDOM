# MANIC Validator Suite

This directory contains machine-executable validation scripts for the $MANIC protocol.

## Validator Philosophy

- **Zero tolerance for drift:** If an object does not align with its schema, validation must fail.
- **Fail loudly:** Validation errors must explicitly report mismatches such as missing fields, type errors, enum violations, and calculation mismatches.
- **No approximation:** Identifiers and hashes must match their declared formats exactly. No truncation or partial matches.
- **Replay before narrative:** Validators do not decide truth. They enforce whether a MANIC object is structurally replayable.

## Current Validators

- `validate_receipt.js` validates MANIC reference receipts against `../schemas/manic_reference_receipt.v1.schema.json`.
- `validate_opacity_release.js` validates Opacity Index releases against `../schemas/opacity_index_release.v1.schema.json` and checks composite score math.

## Usage

From this directory:

```bash
node validate_receipt.js ../examples/example_root_source.json
node validate_receipt.js ../examples/example_claim_node.json
node validate_receipt.js ../examples/example_disputed_branch.json
node validate_opacity_release.js ../examples/example_opacity_release.json
```

Validation failure is intentional when an object drifts from the constitutional schema.
