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

for (const file of walk(contracts).filter((f) => f.endsWith('.json'))) {
  ajv.addSchema(readJson(file));
}

const schemaByFixture = {
  'minimal-repository-evidence.json': 'https://jsonwisdom.example/contracts/JSONWisdom-Repository-Evidence.v0.1.0.json',
  'missing-authority.json': 'https://jsonwisdom.example/contracts/JSONWisdom-Repository-Evidence.v0.1.0.json',
  'trinity-confidence-without-evidence.json': 'https://jsonwisdom.example/contracts/JSONWisdom-Trinity-Classification.v0.1.0.json'
};

const expectedInvalidKeyword = {
  'missing-authority.json': 'required',
  'trinity-confidence-without-evidence.json': 'minItems'
};

let failures = 0;
for (const kind of ['valid', 'invalid']) {
  const dir = path.join(fixtures, kind);
  for (const file of fs.readdirSync(dir).filter((f) => f.endsWith('.json'))) {
    const schemaId = schemaByFixture[file];
    if (!schemaId) throw new Error(`No schema mapping for ${file}`);
    const validate = ajv.getSchema(schemaId);
    if (!validate) throw new Error(`Schema not loaded: ${schemaId}`);
    const ok = validate(readJson(path.join(dir, file)));

    if (kind === 'valid' && !ok) {
      failures += 1;
      console.error(`FAIL valid fixture ${file}`, validate.errors);
    } else if (kind === 'invalid' && ok) {
      failures += 1;
      console.error(`FAIL invalid fixture unexpectedly passed: ${file}`);
    } else if (kind === 'invalid') {
      const keyword = expectedInvalidKeyword[file];
      const observed = (validate.errors ?? []).some((error) => error.keyword === keyword);
      if (!observed) {
        failures += 1;
        console.error(`FAIL ${file}: expected keyword ${keyword}`, validate.errors);
      } else {
        console.log(`PASS invalid fixture ${file} failed as expected (${keyword})`);
      }
    } else {
      console.log(`PASS valid fixture ${file}`);
    }
  }
}

if (failures > 0) process.exit(1);
console.log('All auditor contract fixtures behaved as expected.');
