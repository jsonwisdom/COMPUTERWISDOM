const fs = require('fs');
const path = require('path');
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

  const required = [
    'node_id',
    'parent_root_id',
    'parent_hash',
    'source_locator',
    'transform_id',
    'content_hash',
    'constitutional_tags'
  ];

  for (const field of required) {
    if (!(field in node)) {
      fail(`Missing required field: ${field}`, { filePath });
    }
  }

  if (!/^RPL-\d{3}-[A-Z0-9]+-\d{5}$/.test(node.node_id)) {
    fail('Invalid replay node_id format', { node_id: node.node_id });
  }

  if (!node.parent_root_id.startsWith('ROOT_SOURCE_')) {
    fail('Node disconnected from ROOT_SOURCE', { parent_root_id: node.parent_root_id });
  }

  if (!/^sha256:[a-f0-9]{64}$/.test(node.parent_hash)) {
    fail('Invalid parent_hash format', { parent_hash: node.parent_hash });
  }

  if (!/^sha256:[a-f0-9]{64}$/.test(node.content_hash)) {
    fail('Invalid content_hash format', { content_hash: node.content_hash });
  }

  validateTransform(node);

  if (!Array.isArray(node.constitutional_tags) || !node.constitutional_tags.includes('OBSERVED')) {
    fail('Initial replay node must include OBSERVED tag', { constitutional_tags: node.constitutional_tags });
  }

  if (!node.source_locator || typeof node.source_locator !== 'object') {
    fail('Missing structural source_locator object');
  }

  const locatorValues = Object.values(node.source_locator).filter((value) => value !== null && value !== undefined && value !== '');

  if (locatorValues.length === 0) {
    fail('OFFSET_UNAVAILABLE', { source_locator: node.source_locator });
  }

  console.log(`✅ Replay Node ${node.node_id} validated against ${node.parent_root_id}`);
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
