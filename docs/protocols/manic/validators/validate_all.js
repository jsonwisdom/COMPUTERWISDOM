const fs = require('fs');
const path = require('path');
const { validateReceipt } = require('./validate_receipt');
const { validateOpacityRelease } = require('./validate_opacity_release');

const EXAMPLES_DIR = path.join(__dirname, '..', 'examples');

function runAll() {
  const files = fs.readdirSync(EXAMPLES_DIR)
    .filter((file) => file.endsWith('.json'))
    .sort();

  if (files.length === 0) {
    console.error('❌ VALIDATION FAILED: No MANIC example artifacts found');
    process.exit(1);
  }

  for (const file of files) {
    const filePath = path.join(EXAMPLES_DIR, file);

    try {
      if (file.includes('opacity')) {
        validateOpacityRelease(filePath);
      } else {
        validateReceipt(filePath);
      }

      console.log(`✅ ${file}`);
    } catch (error) {
      console.error(`❌ ${file}: Validation Failed`);
      console.error(error);
      process.exit(1);
    }
  }

  console.log('MANIC validation complete.');
}

if (require.main === module) {
  runAll();
}

module.exports = { runAll };
