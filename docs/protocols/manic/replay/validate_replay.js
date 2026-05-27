const fs = require('fs');
const path = require('path');
const Ajv2020 = require('ajv/dist/2020');
const ajv = new Ajv();

const schema = require('../schemas/replay_node.v1.schema.json');
const { validateTransform } = require('../validators/validate_transform');

function fail(message, extra = null) {
  console.error(`❌ REPLAY DRIFT: ${message}`);

  if (extra) {
    console.error(JSON.stringify(extra, null, 2));
  }

  process.exit(1);
}

function validateReplay(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  const node = JSON.parse(raw);

  const validate = ajv.compile(schema);

  if (!validate(node)) {
    fail('SCHEMA_FAILURE', {
      errors: validate.errors
    });
  }

  validateTransform(node);

  if (!node.source_locator || typeof node.source_locator !== 'object') {
    fail('Missing structural source_locator object');
  }

  const locatorValues = Object.values(node.source_locator).filter((value) => value !== null && value !== undefined && value !== '');

  if (locatorValues.length === 0) {
    fail('OFFSET_UNAVAILABLE', {
      source_locator: node.source_locator
    });
  }

  console.log(`✅ Replay Node ${node.node_id} passed dual-gate validation.`);

  return true;
}

if (require.main === module) {
  const filePath = process.argv[2];

  if (!filePath) {
    console.error('Usage: node validate_replay.js <path-to-json>');
    process.exit(1);
  }

  validateReplay(path.resolve(filePath));
}

module.exports = { validateReplay };
