#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const CLAIM_CLASSES = new Set(['FACT_CLAIM','SELF_REPORT','RELATION_LABEL','INTENT_INFERENCE','MIXED']);
const SOURCE_STATUS = new Set(['OBSERVED','UNOBSERVED','INVALID','SEARCH_MISS']);
const OBJECT_STATUS = new Set(['OBSERVED','UNOBSERVED','INVALID']);
const TIME_STATUS = new Set(['OBSERVED','UNOBSERVED','INVALID']);
const ACTION_STATUS = new Set(['OBSERVED','UNOBSERVED','INVALID','ASSERTED_ONLY']);
const READBACK_STATUS = new Set(['MATCH','MISMATCH','UNAVAILABLE']);
const REPLAY_STATUS = new Set(['COMPLETE','PARTIAL','UNAVAILABLE']);
const ARTIFACT_CLASS = new Set(['RECEIPT','VISUALIZATION','DRAFT']);
const BINDINGS = ['SOURCE','OBJECT','TIME','ACTION','READBACK'];
const FORBIDDEN_CALLER_FIELDS = new Set(['derivedResult','burdenSatisfied','authority','internalFlags','reasons','verifier','inputDigest']);

function sha256(bytes) {
  return crypto.createHash('sha256').update(bytes).digest('hex');
}

function assertUnicodeScalarString(s) {
  for (let i = 0; i < s.length; i++) {
    const c = s.charCodeAt(i);
    if (c >= 0xd800 && c <= 0xdbff) {
      const n = s.charCodeAt(i + 1);
      if (!(n >= 0xdc00 && n <= 0xdfff)) throw new Error('LONE_HIGH_SURROGATE');
      i++;
    } else if (c >= 0xdc00 && c <= 0xdfff) {
      throw new Error('LONE_LOW_SURROGATE');
    }
  }
}

export function jcs(value) {
  if (value === null) return 'null';
  if (typeof value === 'boolean') return value ? 'true' : 'false';
  if (typeof value === 'number') {
    if (!Number.isFinite(value)) throw new Error('NON_FINITE_NUMBER');
    return JSON.stringify(value);
  }
  if (typeof value === 'string') {
    assertUnicodeScalarString(value);
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) return '[' + value.map(jcs).join(',') + ']';
  if (typeof value === 'object') {
    const keys = Object.keys(value).sort();
    return '{' + keys.map(k => {
      assertUnicodeScalarString(k);
      return JSON.stringify(k) + ':' + jcs(value[k]);
    }).join(',') + '}';
  }
  throw new Error('UNSUPPORTED_JSON_TYPE');
}

function nonEmptyString(v) { return typeof v === 'string' && v.length > 0; }
function isObject(v) { return v !== null && typeof v === 'object' && !Array.isArray(v); }

function validateBasic(input) {
  const errors = [];
  const required = ['standard','contractVersion','claimant','claim','claimClass','source','object','time','action','readback','receipts','replay'];
  for (const k of required) if (!(k in input)) errors.push(`MISSING_${k.toUpperCase()}`);
  if (input.standard !== 'GBS-BOXDEE-BURDEN-V001') errors.push('INVALID_STANDARD');
  if (input.contractVersion !== 'INPUT_EVIDENCE_V1') errors.push('INVALID_CONTRACT_VERSION');
  if (!nonEmptyString(input.claimant)) errors.push('INVALID_CLAIMANT');
  if (!nonEmptyString(input.claim)) errors.push('INVALID_CLAIM');
  if (!CLAIM_CLASSES.has(input.claimClass)) errors.push('INVALID_CLAIM_CLASS');
  if (!isObject(input.source) || !SOURCE_STATUS.has(input.source?.status) || !nonEmptyString(input.source?.surface)) errors.push('INVALID_SOURCE');
  if (!isObject(input.object) || !OBJECT_STATUS.has(input.object?.status)) errors.push('INVALID_OBJECT');
  if (!isObject(input.time) || !TIME_STATUS.has(input.time?.status)) errors.push('INVALID_TIME');
  if (!isObject(input.action) || !ACTION_STATUS.has(input.action?.status) || !nonEmptyString(input.action?.assertedTransition)) errors.push('INVALID_ACTION');
  if (!isObject(input.readback) || !READBACK_STATUS.has(input.readback?.status) || !('value' in (input.readback || {}))) errors.push('INVALID_READBACK');
  if (!Array.isArray(input.receipts)) errors.push('INVALID_RECEIPTS');
  if (!isObject(input.replay) || !REPLAY_STATUS.has(input.replay?.chainStatus) || !REPLAY_STATUS.has(input.replay?.replayStatus)) errors.push('INVALID_REPLAY');
  if (Array.isArray(input.receipts)) {
    for (const r of input.receipts) {
      if (!isObject(r) || !nonEmptyString(r.id) || !ARTIFACT_CLASS.has(r.class) || !nonEmptyString(r.binding) || !('value' in r)) errors.push('INVALID_RECEIPT');
      if (r.sha256 !== undefined && r.sha256 !== null && !/^[A-Fa-f0-9]{64}$/.test(r.sha256)) errors.push('INVALID_RECEIPT_SHA256');
    }
  }
  return [...new Set(errors)].sort();
}

function detectCallerInjection(input) {
  return Object.keys(input).filter(k => FORBIDDEN_CALLER_FIELDS.has(k)).sort();
}

function contradictionKeys(receipts) {
  const buckets = new Map();
  for (const r of receipts) {
    if (r.class !== 'RECEIPT') continue;
    if (!nonEmptyString(r.assertionKey)) continue;
    const key = `${r.binding}::${r.assertionKey}`;
    if (!buckets.has(key)) buckets.set(key, new Set());
    buckets.get(key).add(jcs(r.assertionValue));
  }
  return [...buckets.entries()].filter(([,vals]) => vals.size > 1).map(([k]) => k).sort();
}

function receiptCoverage(receipts) {
  const covered = new Set(receipts.filter(r => r.class === 'RECEIPT').map(r => r.binding));
  return BINDINGS.filter(b => !covered.has(b));
}

export function verify(input) {
  const canonicalInput = jcs(input);
  const inputDigest = sha256(Buffer.from(canonicalInput, 'utf8'));
  const reasons = [];

  const injections = detectCallerInjection(input);
  const schemaErrors = validateBasic(input);
  const contradictions = Array.isArray(input.receipts) ? contradictionKeys(input.receipts) : [];

  let hasInvariantViolation = injections.length > 0 || schemaErrors.length > 0;
  let hasContradictoryReceipts = contradictions.length > 0;
  let hasMismatch = input.readback?.status === 'MISMATCH';
  let hasPartialChain = input.replay?.chainStatus === 'PARTIAL';
  let hasPartialReplay = input.replay?.replayStatus === 'PARTIAL';

  if (injections.length) reasons.push('CALLER_RESULT_INJECTION');
  if (schemaErrors.length) reasons.push(...schemaErrors.map(e => `INPUT_${e}`));
  if (contradictions.length) reasons.push('CONTRADICTORY_ADMISSIBLE_RECEIPTS');
  if (hasMismatch) reasons.push('BOUND_READBACK_MISMATCH');
  if (hasPartialChain) reasons.push('PARTIAL_CHAIN');
  if (hasPartialReplay) reasons.push('PARTIAL_REPLAY');

  const missing = [];
  if (input.source?.status !== 'OBSERVED') missing.push('SOURCE');
  if (input.object?.status !== 'OBSERVED' || !nonEmptyString(input.object?.identifier)) missing.push('OBJECT');
  if (input.time?.status !== 'OBSERVED' || !nonEmptyString(input.time?.value)) missing.push('TIME');
  if (input.action?.status !== 'OBSERVED') missing.push('ACTION');
  if (input.readback?.status === 'UNAVAILABLE') missing.push('READBACK');
  if (input.replay?.chainStatus !== 'COMPLETE') missing.push('CHAIN');
  if (input.replay?.replayStatus !== 'COMPLETE') missing.push('REPLAY');
  const uncovered = Array.isArray(input.receipts) ? receiptCoverage(input.receipts) : BINDINGS;
  for (const b of uncovered) missing.push(`RECEIPT_${b}`);
  if (input.claimClass === 'MIXED') missing.push('ATOMIC_CLAIM');

  const hasMissingEvidence = missing.length > 0;
  if (hasMissingEvidence) {
    if (input.claimClass === 'MIXED') reasons.push('MIXED_REQUIRES_DECOMPOSITION');
    if (missing.some(x => x.startsWith('RECEIPT_'))) reasons.push('MISSING_BOUND_RECEIPT');
    if (input.source?.status === 'SEARCH_MISS') reasons.push('SEARCH_MISS_NOT_ABSENCE');
    if (input.readback?.status === 'UNAVAILABLE') reasons.push('READBACK_UNAVAILABLE');
  }

  const burdenSatisfied = !hasInvariantViolation && !hasContradictoryReceipts && !hasMismatch && !hasMissingEvidence && !hasPartialChain && !hasPartialReplay;

  let derivedResult;
  if (hasInvariantViolation || hasContradictoryReceipts) derivedResult = 'FAIL';
  else if (hasMismatch) derivedResult = 'DELTA';
  else if (hasMissingEvidence || hasPartialChain || hasPartialReplay || !burdenSatisfied) derivedResult = 'HOLD';
  else derivedResult = 'PASS';

  return {
    standard: 'GBS-BOXDEE-BURDEN-V001',
    verifier: 'P1_VERIFIER_SPEC_V1',
    claimClass: CLAIM_CLASSES.has(input.claimClass) ? input.claimClass : 'FACT_CLAIM',
    inputDigest,
    internalFlags: {
      hasInvariantViolation,
      hasContradictoryReceipts,
      hasMismatch,
      hasPartialChain,
      hasPartialReplay,
      hasMissingEvidence
    },
    burdenSatisfied,
    derivedResult,
    authority: false,
    reasons: [...new Set(reasons)].sort()
  };
}

function parseArgs(argv) {
  const out = {};
  for (let i = 2; i < argv.length; i += 2) out[argv[i]] = argv[i + 1];
  return out;
}

function requireArg(args, name) {
  if (!args[name]) throw new Error(`MISSING_ARGUMENT_${name}`);
  return args[name];
}

function verifyMemory(memoryPath, receiptDir, input) {
  const raw = fs.readFileSync(memoryPath);
  const memory = JSON.parse(raw.toString('utf8'));
  if (memory.standard !== 'GBS-BOXDEE-BURDEN-V001' || memory.contractVersion !== 'MEMORY_INDEX_V1') throw new Error('INVALID_MEMORY_INDEX');
  const inputHashes = new Set((input.receipts || []).map(r => r.sha256).filter(Boolean).map(v => v.toLowerCase()));
  const required = [];
  for (const locator of memory.requiredReceipts || []) {
    const target = path.join(receiptDir, locator.fileName);
    const bytes = fs.readFileSync(target);
    const actual = sha256(bytes);
    if (actual.toLowerCase() !== locator.sha256.toLowerCase()) throw new Error(`MEMORY_RECEIPT_BYTE_MISMATCH:${locator.id}`);
    if (!inputHashes.has(actual.toLowerCase())) throw new Error(`MEMORY_RECEIPT_NOT_BOUND_IN_INPUT:${locator.id}`);
    required.push({id: locator.id, fileName: locator.fileName, sha256: actual, byteLength: bytes.length, verified: true});
  }
  return {
    memoryId: memory.memoryId,
    rawMemorySha256: sha256(raw),
    canonicalMemorySha256: sha256(Buffer.from(jcs(memory),'utf8')),
    requiredReceipts: required,
    advisoryOnly: true
  };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  try {
    const args = parseArgs(process.argv);
    const inputPath = requireArg(args, '--input');
    const outputPath = requireArg(args, '--output');
    const canonicalInputPath = requireArg(args, '--canonical-input');
    const byteReceiptPath = requireArg(args, '--byte-receipt');

    const rawInput = fs.readFileSync(inputPath);
    const input = JSON.parse(rawInput.toString('utf8'));
    const canonicalInput = jcs(input);
    const result = verify(input);
    const canonicalOutput = jcs(result);

    let memoryResolution = null;
    if (args['--memory']) {
      const receiptDir = requireArg(args, '--receipt-dir');
      memoryResolution = verifyMemory(args['--memory'], receiptDir, input);
    }

    fs.mkdirSync(path.dirname(outputPath), {recursive:true});
    fs.mkdirSync(path.dirname(canonicalInputPath), {recursive:true});
    fs.mkdirSync(path.dirname(byteReceiptPath), {recursive:true});
    fs.writeFileSync(canonicalInputPath, canonicalInput);
    fs.writeFileSync(outputPath, canonicalOutput);

    const receipt = {
      schema: 'BOXDEE_BYTE_REPLAY_RECEIPT_V1',
      rawInputSha256: sha256(rawInput),
      rawInputByteLength: rawInput.length,
      canonicalInputSha256: sha256(Buffer.from(canonicalInput,'utf8')),
      canonicalInputByteLength: Buffer.byteLength(canonicalInput,'utf8'),
      canonicalOutputSha256: sha256(Buffer.from(canonicalOutput,'utf8')),
      canonicalOutputByteLength: Buffer.byteLength(canonicalOutput,'utf8'),
      memoryResolution,
      derivedResult: result.derivedResult,
      burdenSatisfied: result.burdenSatisfied,
      authority: false
    };
    fs.writeFileSync(byteReceiptPath, jcs(receipt));
    process.stdout.write(jcs(receipt) + '\n');
  } catch (err) {
    process.stderr.write(String(err?.stack || err) + '\n');
    process.exit(1);
  }
}
