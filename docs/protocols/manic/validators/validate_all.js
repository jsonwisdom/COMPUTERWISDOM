const fs = require('fs');
const path = require('path');
const { validateReceipt } = require('./validate_receipt');
const { validateOpacityRelease } = require('./validate_opacity_release');
const { validateReplay } = require('../replay/validate_replay');
const { validateDeterministicReceipt } = require('./validate_deterministic_receipt');

const EXAMPLES_DIR = path.join(__dirname, '..', 'examples');
const REPLAY_BRANCHES_DIR = path.join(__dirname, '..', 'replay', 'branches');
const REPLAY_RECEIPTS_DIR = path.join(__dirname, '..', 'replay', 'receipts');

function listJsonFiles(dir) {
  if (!fs.existsSync(dir)) {
    return [];
  }

  return fs.readdirSync(dir)
    .filter((file) => file.endsWith('.json'))
    .sort()
    .map((file) => path.join(dir, file));
}

function runValidator(label, filePath, validator) {
  try {
    validator(filePath);
    console.log(`✅ ${label}: ${path.basename(filePath)}`);
    return { label, file: filePath, result: 'PASSED' };
  } catch (error) {
    console.error(`❌ ${label}: ${path.basename(filePath)} failed`);
    console.error(error);
    process.exit(1);
  }
}

function runAll() {
  const results = [];

  const replayFiles = listJsonFiles(REPLAY_BRANCHES_DIR);
  for (const filePath of replayFiles) {
    results.push(runValidator('replay', filePath, validateReplay));
  }

  const deterministicReceiptFiles = listJsonFiles(REPLAY_RECEIPTS_DIR)
    .filter((filePath) => path.basename(filePath).startsWith('RCP-'));

  for (const filePath of deterministicReceiptFiles) {
    results.push(runValidator('deterministic_receipt', filePath, validateDeterministicReceipt));
  }

  const exampleFiles = listJsonFiles(EXAMPLES_DIR);
  if (exampleFiles.length === 0) {
    console.error('❌ VALIDATION FAILED: No MANIC example artifacts found');
    process.exit(1);
  }

  for (const filePath of exampleFiles) {
    if (path.basename(filePath).includes('opacity')) {
      results.push(runValidator('opacity', filePath, validateOpacityRelease));
    } else {
      results.push(runValidator('receipt', filePath, validateReceipt));
    }
  }

  console.log('MANIC validation complete.');
  return results;
}

if (require.main === module) {
  runAll();
}

module.exports = { runAll };
