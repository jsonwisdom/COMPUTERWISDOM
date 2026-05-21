const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');

const schemaPath = path.join(__dirname, '..', 'schemas', 'opacity_index_release.v1.schema.json');
const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));

const ajv = new Ajv({ allErrors: true, strict: false });
const validate = ajv.compile(schema);

function fail(message, extra = null) {
  console.error(`❌ VALIDATION FAILED: ${message}`);

  if (extra) {
    console.error(JSON.stringify(extra, null, 2));
  }

  process.exit(1);
}

function validateOpacityRelease(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  const release = JSON.parse(raw);

  const valid = validate(release);

  if (!valid) {
    fail('Schema Drift Detected', validate.errors);
  }

  const calculated = release.axes.reduce((acc, axis) => {
    return acc + (axis.score * axis.weight);
  }, 0);

  const rounded = Math.round(calculated * 10) / 10;

  if (rounded !== release.composite_score) {
    fail('Opacity Math Mismatch', {
      expected: release.composite_score,
      calculated: rounded
    });
  }

  console.log('✅ Opacity Release Validated: Calculation Coherent');
  return true;
}

if (require.main === module) {
  const filePath = process.argv[2];

  if (!filePath) {
    console.error('Usage: node validate_opacity_release.js <path-to-json>');
    process.exit(1);
  }

  validateOpacityRelease(path.resolve(filePath));
}

module.exports = { validateOpacityRelease };
