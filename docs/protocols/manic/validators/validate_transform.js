const fs = require('fs');
const path = require('path');

const REGISTRY_PATH = path.join(
  __dirname,
  '..',
  'runtime',
  'REPLAY_TRANSFORM_REGISTRY_001.json'
);

function loadRegistry() {
  return JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));
}

function fail(message, extra = null) {
  console.error(`❌ REJECTED: ${message}`);

  if (extra) {
    console.error(JSON.stringify(extra, null, 2));
  }

  process.exit(1);
}

function validateTransform(node) {
  const registry = loadRegistry();

  const transform = registry.transforms.find((t) => t.id === node.transform_id);

  if (!transform) {
    fail('ERR_UNAUTHORIZED_TRANSFORM', {
      transform_id: node.transform_id
    });
  }

  if (transform.network_access !== false) {
    fail('ERR_NETWORK_ACCESS_FORBIDDEN', {
      transform_id: node.transform_id
    });
  }

  const interpretiveTags = ['INTERPRETED', 'SYNTHESIZED', 'DISPUTED', 'SUPERSEDED'];
  const foundInterpretiveTags = (node.constitutional_tags || [])
    .filter((tag) => interpretiveTags.includes(tag));

  if (transform.allow_interpretation === false && foundInterpretiveTags.length > 0) {
    fail('ERR_INTERPRETATION_FORBIDDEN', {
      transform_id: node.transform_id,
      interpretive_tags: foundInterpretiveTags
    });
  }

  console.log(`✅ Transform Admissible: ${node.transform_id}`);

  return {
    status: 'ADMISSIBLE',
    transform
  };
}

module.exports = { validateTransform };
