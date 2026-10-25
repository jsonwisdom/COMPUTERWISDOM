// Append-only, hash-chained evidence ledger.
import { digest } from './jcs.js';
import { assertValid, validate } from './validate.js';

export class EvidenceLedger {
  #entries = [];
  append(kind, content, dataLabel) {
    const prev = this.#entries.at(-1);
    const body = { type: 'EvidenceLedgerEntry', seq: this.#entries.length, prevDigest: prev ? prev.entryDigest : 'GENESIS',
      kind, contentDigest: digest(content), content: structuredClone(content), dataLabel, AUTHORITY_CREATED: false };
    const entry = Object.freeze(assertValid('EvidenceLedgerEntry', { ...body, entryDigest: digest(body) }));
    this.#entries.push(entry);
    return entry;
  }
  entries() { return this.#entries.map((e) => structuredClone(e)); }
  get head() { return this.#entries.at(-1)?.entryDigest ?? 'GENESIS'; }
}

export function verifyLedger(entries) {
  const reasons = [];
  entries.forEach((e, i) => {
    const v = validate('EvidenceLedgerEntry', e);
    if (!v.ok) reasons.push(`#${i} schema: ${v.errors.join(',')}`);
    if (e.seq !== i) reasons.push(`#${i} seq`);
    if (e.prevDigest !== (i === 0 ? 'GENESIS' : entries[i - 1].entryDigest)) reasons.push(`#${i} chain broken`);
    if (digest(e.content) !== e.contentDigest) reasons.push(`#${i} contentDigest mismatch`);
    const { entryDigest, ...body } = e;
    if (digest(body) !== entryDigest) reasons.push(`#${i} entryDigest mismatch`);
  });
  return { ok: reasons.length === 0, reasons };
}
