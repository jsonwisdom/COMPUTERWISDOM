// Schema + semantic validators. AUTHORITY_CREATED=false invariant enforced here.
import Ajv2020 from 'ajv/dist/2020.js';
import addFormats from 'ajv-formats';
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { join, dirname } from 'node:path';

const dir = join(dirname(fileURLToPath(import.meta.url)), '..', 'schemas');
const ajv = new Ajv2020({ allErrors: true, strict: true, allowUnionTypes: true });
addFormats(ajv);
for (const f of readdirSync(dir).filter((f) => f.endsWith('.json')).sort()) {
  ajv.addSchema(JSON.parse(readFileSync(join(dir, f), 'utf8')));
}
const IDS = {
  RollReceipt: 'roll-receipt', ReplayPacket: 'replay-packet', EvidenceLedgerEntry: 'evidence-ledger-entry',
  FinanceProvenance: 'finance-provenance', ApprovalReceipt: 'approval-receipt', SourceAvailability: 'source-availability',
};

function semantic(type, o) {
  const errs = [];
  // Global invariant: no emitted packet may claim authority.
  const walk = (v, p) => {
    if (v && typeof v === 'object') {
      for (const [k, x] of Object.entries(v)) {
        if (k === 'AUTHORITY_CREATED' && x !== false) errs.push(`${p}/${k} must be false`);
        walk(x, `${p}/${k}`);
      }
    }
  };
  walk(o, '');
  if (type === 'RollReceipt') {
    const idx = (o.dice[0] - 1) * 36 + (o.dice[1] - 1) * 6 + (o.dice[2] - 1);
    if (idx !== o.outcomeIndex) errs.push('outcomeIndex does not match dice');
    const accepted = o.rawBytes.filter((b) => b < 252).map((b) => 1 + (b % 6));
    if (accepted.join() !== o.dice.join()) errs.push('dice not derivable from rawBytes via rejection@252');
    if (o.rawBytes.filter((b) => b >= 252).join() !== o.rejectedBytes.join()) errs.push('rejectedBytes mismatch');
  }
  if (type === 'ApprovalReceipt') {
    // HUMAN_APPROVAL_RECORDED != CRYPTOGRAPHIC_IDENTITY_VERIFIED
    if (o.CRYPTOGRAPHIC_IDENTITY_VERIFIED && !(o.identityEvidence && o.identityEvidence.verifiedBy)) {
      errs.push('CRYPTOGRAPHIC_IDENTITY_VERIFIED=true requires identityEvidence.verifiedBy');
    }
  }
  if (type === 'FinanceProvenance') {
    const ids = new Set(o.sources.map((s) => s.sourceId));
    for (const c of o.claims) if (!ids.has(c.sourceId)) errs.push(`claim ${c.field} cites unknown source`);
    const ops = new Set(o.sources.map((s) => s.operator)).size;
    if (o.independence.distinctOperators !== ops) errs.push('distinctOperators does not match sources');
    if (o.independence.declared && ops < 2) errs.push('independence declared with <2 distinct operators');
    if (o.dataLabel === 'LIVE' && o.sources.some((s) => s.availability !== 'AVAILABLE' || !s.retrievedDigest)) {
      errs.push('LIVE label requires every source AVAILABLE with retrievedDigest');
    }
  }
  if (type === 'SourceAvailability' && o.dataLabel === 'LIVE' && o.availability !== 'AVAILABLE') {
    errs.push('LIVE label requires availability AVAILABLE');
  }
  return errs;
}

export function validate(type, obj) {
  const v = ajv.getSchema(IDS[type]);
  if (!v) throw new Error(`unknown type ${type}`);
  if (!v(obj)) return { ok: false, errors: v.errors.map((e) => `${e.instancePath} ${e.message}`) };
  const errors = semantic(type, obj);
  return { ok: errors.length === 0, errors };
}

export function assertValid(type, obj) {
  const r = validate(type, obj);
  if (!r.ok) throw new Error(`${type} invalid: ${r.errors.join('; ')}`);
  return obj;
}
