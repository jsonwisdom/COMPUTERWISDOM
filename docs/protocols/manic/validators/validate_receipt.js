const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');

const schemaPath = path.join(__dirname, '..', 'schemas', 'manic_reference_receipt.v1.schema.json');
const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));

const ajv = new Ajv({ allErrors: true, strict: false });
const validate = ajv.compile(schema);

function fail(errors) {
  console.error('❌ VALIDATION FAILED: Structural Drift Detected');
  console.error(JSON.stringify(errors, null, 2));
  process.exit(1);
}

function validateReceipt(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  const receipt = JSON.parse(raw);

  const valid = validate(receipt);

  if (!valid) {
    fail(validate.errors);
  }

  console.log('✅ Receipt Validated: Structural Integrity Confirmed');
  return true;
}

if (require.main === module) {
  const filePath = process.argv[2];

  if (!filePath) {
    console.error('Usage: node validate_receipt.js <path-to-json>');
    process.exit(1);
  }

  validateReceipt(path.resolve(filePath));
}

module.exports = { validateReceipt };
