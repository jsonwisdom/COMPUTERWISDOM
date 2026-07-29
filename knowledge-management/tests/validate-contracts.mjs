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
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (error) {
    throw new Error(`Invalid JSON in ${path.relative(root, file)}: ${error.message}`);
  }
}

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(dir, entry.name);
    return entry.isDirectory() ? walk(full) : [full];
  });
}

// Phase 1: load every contract into memory and verify stable, unique identifiers.
const schemaEntries = walk(contracts)
  .filter((file) => file.endsWith('.json'))
  .sort()
  .map((file) => ({ file, schema: readJson(file) }));

const idOwners = new Map();
for (const { file, schema } of schemaEntries) {
  const relative = path.relative(root, file);
  if (typeof schema.$id !== 'string' || schema.$id.length === 0) {
    throw new Error(`Schema missing $id: ${relative}`);
  }
  if (idOwners.has(schema.$id)) {
    throw new Error(
      `Duplicate schema $id ${schema.$id}: ${idOwners.get(schema.$id)} and ${relative}`
    );
  }
  idOwners.set(schema.$id, relative);
}

// Phase 2: register all schemas before compiling any of them so cross-contract
// references resolve from the complete in-memory registry.
for (const { schema } of schemaEntries) {
  ajv.addSchema(schema);
}

// Compile every schema before fixture evaluation. This surfaces unresolved $refs
// and malformed contracts with the exact schema identifier that caused the failure.
for (const { file, schema } of schemaEntries) {
  try {
    const compiled = ajv.getSchema(schema.$id);
    if (!compiled) throw new Error('schema was not registered');
  } catch (error) {
    throw new Error(
      `Schema compilation failed for ${path.relative(root, file)} (${schema.$id}): ${error.message}`
    );
  }
}

console.log(`Registered ${schemaEntries.length} contracts with unique $id values.`);

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
  for (const filename of fs.readdirSync(dir).filter((file) => file.endsWith('.json')).sort()) {
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
