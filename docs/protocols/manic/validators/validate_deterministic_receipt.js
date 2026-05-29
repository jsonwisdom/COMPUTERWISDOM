const fs = require('fs');
const path = require('path');
const Ajv2020 = require('ajv/dist/2020');

const schemaPath = path.join(__dirname, '..', 'schemas', 'deterministic_replay_receipt.v1.schema.json');
const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
const ajv = new Ajv2020({ allErrors: true, strict: false });
const validate = ajv.compile(schema);

const FORBIDDEN_FIELDS = [
  'timestamp',
  'created_at',
  'updated_at',
  'generated_at',
  'system_time'
];

function fail(message, extra = null) {
  console.error(`❌ DETERMINISTIC RECEIPT VALIDATION FAILED: ${message}`);

  if (extra) {
    console.error(JSON.stringify(extra, null, 2));
  }

  process.exit(1);
}

function validateDeterministicReceipt(filePath) {
  const receipt = JSON.parse(fs.readFileSync(filePath, 'utf8'));

  const valid = validate(receipt);

  if (!valid) {
    fail('SCHEMA_DRIFT', validate.errors);
  }

  const presentForbidden = FORBIDDEN_FIELDS.filter((field) => Object.prototype.hasOwnProperty.call(receipt, field));

  if (presentForbidden.length > 0) {
    fail('NON_DETERMINISTIC_FIELD_DETECTED', { fields: presentForbidden });
  }

  if (receipt.authority_claim !== 'NONE') {
    fail('RECEIPT_AUTHORITY_OVERCLAIM', { authority_claim: receipt.authority_claim });
  }

  if (receipt.truth_adjudication !== 'NOT_PERFORMED') {
    fail('TRUTH_ADJUDICATION_DETECTED', { truth_adjudication: receipt.truth_adjudication });
  }

  console.log(`✅ Deterministic Receipt Validated: ${path.basename(filePath)}`);
  return true;
}

if (require.main === module) {
  const filePath = process.argv[2];

  if (!filePath) {
    console.error('Usage: node validate_deterministic_receipt.js <receipt.json>');
    process.exit(1);
  }

  validateDeterministicReceipt(path.resolve(filePath));
}

module.exports = { validateDeterministicReceipt };
