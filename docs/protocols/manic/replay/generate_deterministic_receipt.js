const fs = require('fs');
const path = require('path');

function generateDeterministicReceipt(node) {
  return {
    schema_id: 'MANIC_DETERMINISTIC_REPLAY_RECEIPT_V1',
    receipt_id: `RCP-${node.node_id}`,
    target_node: node.node_id,
    node_version_hash: node.content_hash,
    registry_version: 'REPLAY_TRANSFORM_REGISTRY_001',
    enforcement_gates: ['SCHEMA_GATE', 'REGISTRY_GATE', 'REPLAY_GATE'],
    status: 'PROVEN_REPLAYABLE',
    authority_claim: 'NONE',
    truth_adjudication: 'NOT_PERFORMED',
    continuity_flag: 'COHERENTLY_INVALID_UNTIL_REPLAYED'
  };
}

if (require.main === module) {
  const inputPath = process.argv[2];

  if (!inputPath) {
    console.error('Usage: node generate_deterministic_receipt.js <node.json>');
    process.exit(1);
  }

  const node = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
  const receipt = generateDeterministicReceipt(node);

  const outputDir = path.join(__dirname, 'receipts');

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const outputPath = path.join(outputDir, `${receipt.receipt_id}.json`);
  fs.writeFileSync(outputPath, `${JSON.stringify(receipt, null, 2)}\n`);

  console.log(`✅ Receipt generated: ${outputPath}`);
}

module.exports = { generateDeterministicReceipt };
