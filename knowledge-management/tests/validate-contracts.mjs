import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import Ajv2020 from 'ajv/dist/2020.js';
import addFormats from 'ajv-formats';

const root = process.cwd();
const contracts = path.join(root, 'knowledge-management', 'contracts');
const fixtures = path.join(root, 'knowledge-management', 'fixtures');
const ajv = new Ajv2020({ allErrors: true, strict: false });
addFormats(ajv);

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(dir, entry.name);
    return entry.isDirectory() ? walk(full) : [full];
  });
}

// Register every contract before compiling fixture validators. Sorting keeps shared
// definitions deterministic and makes failures reproducible across runners.
for (const file of walk(contracts).filter((f) => f.endsWith('.json')).sort()) {
  ajv.addSchema(readJson(file));
}

const schemaByFixture = {
  'minimal-repository-evidence.json': 'https://jsonwisdom.example/contracts/JSONWisdom-Repository-Evidence.v0.1.0.json',
  'missing-authority.json': 'https://jsonwisdom.example/contracts/JSONWisdom-Repository-Evidence.v0.1.0.json',
  'trinity-confidence-without-evidence.json': 'https://jsonwisdom.example/contracts/JSONWisdom-Trinity-Classification.v0.1.0.json',
  'auditor-claiming-authority.json': 'https://jsonwisdom.example/contracts/auditor/AuditorEvidenceBase.v0.1.0.json'
};

const expectedInvalidReason = {
  'missing-authority.json': { type: 'keyword', value: 'required' },
  'trinity-confidence-without-evidence.json': { type: 'keyword', value: 'minItems' },
  'auditor-claiming-authority.json': { type: 'authority-separation' }
};

function authoritySeparationViolation(data, relativeFilename) {
  const normalized = relativeFilename.split(path.sep).join('/');
  const isAuthorityGrant = normalized.includes('authority/JSONWisdom-Authority-Grant');

  if (data.authority === true && !isAuthorityGrant) {
    return `SECURITY VIOLATION: Non-authority file ${normalized} claims authority: true`;
  }
  if (data.authority === false && isAuthorityGrant) {
    return `SECURITY VIOLATION: Authority grant file ${normalized} must have authority: true`;
  }
  return null;
}

let failures = 0;
for (const kind of ['valid', 'invalid']) {
  const dir = path.join(fixtures, kind);
  for (const filename of fs.readdirSync(dir).filter((f) => f.endsWith('.json')).sort()) {
    const schemaId = schemaByFixture[filename];
    if (!schemaId) throw new Error(`No schema mapping for ${filename}`);

    const validate = ajv.getSchema(schemaId);
    if (!validate) throw new Error(`Schema not loaded: ${schemaId}`);

    const fullPath = path.join(dir, filename);
    const data = readJson(fullPath);
    const schemaValid = validate(data);
    const authorityViolation = authoritySeparationViolation(
      data,
      path.relative(root, fullPath)
    );

    if (kind === 'valid') {
      if (!schemaValid || authorityViolation) {
        failures += 1;
        console.error(`FAIL valid fixture ${filename}`, {
          schemaErrors: validate.errors,
          authorityViolation
        });
      } else {
        console.log(`PASS valid fixture ${filename}`);
      }
      continue;
    }

    const expectation = expectedInvalidReason[filename];
    if (!expectation) throw new Error(`No invalid expectation for ${filename}`);

    if (expectation.type === 'authority-separation') {
      if (!authorityViolation) {
        failures += 1;
        console.error(`FAIL ${filename}: expected authority-separation violation`, validate.errors);
      } else {
        console.log(`PASS invalid fixture ${filename} failed as expected (authority-separation)`);
      }
      continue;
    }

    const observedKeyword = (validate.errors ?? []).some(
      (error) => error.keyword === expectation.value
    );
    if (schemaValid || !observedKeyword) {
      failures += 1;
      console.error(`FAIL ${filename}: expected keyword ${expectation.value}`, {
        schemaValid,
        schemaErrors: validate.errors,
        authorityViolation
      });
    } else {
      console.log(`PASS invalid fixture ${filename} failed as expected (${expectation.value})`);
    }
  }
}

if (failures > 0) process.exit(1);
console.log('All auditor contract fixtures behaved as expected.');
