import { test } from 'node:test';
import assert from 'node:assert/strict';
import { produce, replay } from '../src/replay.js';
import { EvidenceLedger, verifyLedger } from '../src/ledger.js';
import { buildProvenance } from '../src/finance.js';
import { checkAvailability } from '../src/adapters.js';
import { ApprovalStore } from '../src/approval.js';
import { validate } from '../src/validate.js';
import { SEED } from './helpers.js';

test('integration: replay reproduces identical rolls and packet digest', () => {
  const a = produce(SEED, 25), b = produce(SEED, 25);
  assert.equal(a.packetDigest, b.packetDigest);
  assert.deepEqual(replay(a, SEED), { ok: true, reasons: [] });
  assert.deepEqual(replay(a), { ok: true, reasons: [] });
});
test('negative: tampered roll in packet -> mismatch', () => {
  const p = structuredClone(produce(SEED, 5)); p.rolls[2].dice[0] = (p.rolls[2].dice[0] % 6) + 1;
  const r = replay(p, SEED); assert.equal(r.ok, false); assert.ok(r.reasons.length > 0);
});
test('negative: wrong seed -> mismatch', () => assert.equal(replay(produce(SEED, 3), 'other').ok, false));
test('integration+negative: ledger chain verifies; tamper detected', () => {
  const L = new EvidenceLedger();
  const p = produce(SEED, 2);
  L.append('REPLAY', p, 'SYNTHETIC');
  L.append('NOTE', { text: 'second' }, 'SYNTHETIC');
  L.append('NOTE', { text: 'third' }, 'SYNTHETIC');
  const e = L.entries();
  assert.ok(verifyLedger(e).ok);
  const t1 = structuredClone(e); t1[1].content.text = 'edited'; assert.equal(verifyLedger(t1).ok, false);
  const t2 = structuredClone(e); t2.splice(1, 1); assert.equal(verifyLedger(t2).ok, false);
  const t3 = structuredClone(e); [t3[1], t3[2]] = [t3[2], t3[1]]; assert.equal(verifyLedger(t3).ok, false);
  assert.throws(() => { L.entries()[0].seq = 99; if (L.entries()[0].seq === 99) throw new Error('mutable'); else throw new Error('copy'); }, /copy/);
});
test('integration: adapters default NOT_CONFIGURED / LIVE_UNAVAILABLE, no fetch attempted', async () => {
  let called = 0; const fetchImpl = async () => { called++; return { status: 200, ok: true }; };
  for (const a of ['FEC', 'OPENSECRETS', 'THIRD_SOURCE']) {
    const r = await checkAvailability(a, { env: {}, fetchImpl });
    assert.equal(r.availability, 'NOT_CONFIGURED'); assert.equal(r.dataLabel, 'LIVE_UNAVAILABLE');
    assert.equal(r.liveFinancialActivity, false); assert.ok(validate('SourceAvailability', r).ok);
  }
  assert.equal(called, 0);
});
test('integration: adapter status mapping with MOCK fetch (labeled MOCK in test only)', async () => {
  const env = { DD_ENABLE_HTTP: '1', DD_FEC_API_KEY: 'MOCK_KEY' };
  const st = async (status) => (await checkAvailability('FEC', { env, fetchImpl: async () => ({ status, ok: status < 300 }) })).availability;
  assert.equal(await st(200), 'AVAILABLE'); assert.equal(await st(429), 'RATE_LIMITED');
  assert.equal(await st(401), 'AUTH_REQUIRED'); assert.equal(await st(500), 'ERROR');
  assert.equal((await checkAvailability('FEC', { env, fetchImpl: async () => { throw new TypeError('x'); } })).availability, 'ERROR');
  assert.equal((await checkAvailability('OPENSECRETS', { env: { DD_ENABLE_HTTP: '1' } })).availability, 'AUTH_REQUIRED');
});
test('integration: finance provenance from unavailable sources is LIVE_UNAVAILABLE, not independent', async () => {
  const fec = await checkAvailability('FEC', { env: {} });
  const os = await checkAvailability('OPENSECRETS', { env: {} });
  const prov = buildProvenance({ subject: 'SYNTHETIC-CANDIDATE', claims: [{ field: 'receipts', value: null, sourceId: 'fec' }],
    sources: [{ sourceId: 'fec', adapter: 'FEC', availability: fec.availability, retrievedDigest: null, operator: 'U.S. Federal Election Commission' },
      { sourceId: 'os', adapter: 'OPENSECRETS', availability: os.availability, retrievedDigest: null, operator: 'OpenSecrets' }] });
  assert.equal(prov.dataLabel, 'LIVE_UNAVAILABLE'); assert.equal(prov.liveSpend, false); assert.equal(prov.walletSigning, false);
  assert.equal(prov.independence.distinctOperators, 2);
});
test('integration: approval recorded -> consumed once; identity NOT verified', () => {
  const s = new ApprovalStore(); const subject = { packet: produce(SEED, 1).packetDigest };
  const r = s.record({ subject, approver: 'jason (self-asserted)' });
  assert.equal(r.HUMAN_APPROVAL_RECORDED, true); assert.equal(r.CRYPTOGRAPHIC_IDENTITY_VERIFIED, false);
  const c = s.consume(r, subject); assert.equal(c.ok, true); assert.equal(c.AUTHORITY_CREATED, false);
  assert.equal(c.receipt.status, 'HOLD');
});
