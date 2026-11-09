import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Worker } from 'node:worker_threads';
import { ApprovalStore } from '../src/approval.js';

const subject = { action: 'SYNTHETIC_TEST_SUBJECT' };
test('security: approval reuse fails (ALREADY_CONSUMED)', () => {
  const s = new ApprovalStore(); const r = s.record({ subject, approver: 'tester' });
  assert.equal(s.consume(r, subject).ok, true);
  assert.equal(s.consume(r, subject).reason, 'ALREADY_CONSUMED');
});
test('security: forged MAC / tampered fields rejected', () => {
  const s = new ApprovalStore(); const r = s.record({ subject, approver: 'tester' });
  assert.equal(s.consume({ ...r, mac: 'hmac-sha256:' + '0'.repeat(64) }, subject).reason, 'BAD_MAC');
  assert.equal(s.consume({ ...r, approver: 'someone-else' }, subject).reason, 'BAD_MAC');
  assert.equal(s.consume({ ...r, AUTHORITY_CREATED: true }, subject).reason, 'BAD_MAC');
});
test('security: receipt from another store (different key) rejected', () => {
  const a = new ApprovalStore(), b = new ApprovalStore(); const r = a.record({ subject, approver: 'tester' });
  assert.equal(b.consume(r, subject).reason, 'UNKNOWN_APPROVAL');
});
test('security: subject substitution rejected', () => {
  const s = new ApprovalStore(); const r = s.record({ subject, approver: 'tester' });
  assert.equal(s.consume(r, { action: 'OTHER' }).reason, 'SUBJECT_MISMATCH');
  assert.equal(s.consume(r, subject).ok, true);
});
test('security: flipping CRYPTOGRAPHIC_IDENTITY_VERIFIED on a receipt does not create identity', () => {
  const s = new ApprovalStore(); const r = s.record({ subject, approver: 'tester' });
  const c = s.consume({ ...r, CRYPTOGRAPHIC_IDENTITY_VERIFIED: true }, subject);
  assert.equal(c.ok, true); assert.equal(c.receipt.CRYPTOGRAPHIC_IDENTITY_VERIFIED, false);
});
test('security: short HMAC key refused', () => assert.throws(() => new ApprovalStore({ key: Buffer.alloc(8) })));
test('concurrency: 500 concurrent async consumers -> exactly 1 success', async () => {
  const s = new ApprovalStore(); const r = s.record({ subject, approver: 'tester' });
  const results = await Promise.all(Array.from({ length: 500 }, () => new Promise((res) => setImmediate(() => res(s.consume(structuredClone(r), subject))))));
  assert.equal(results.filter((x) => x.ok).length, 1);
  assert.equal(results.filter((x) => x.reason === 'ALREADY_CONSUMED').length, 499);
});
test('concurrency: 8 worker threads racing on a shared-memory claim -> exactly 1 winner', async () => {
  // Models cross-thread single-use with Atomics.compareExchange on a SharedArrayBuffer slot.
  const sab = new SharedArrayBuffer(4);
  const src = `const { workerData, parentPort } = require('node:worker_threads');
    const a = new Int32Array(workerData.sab); parentPort.postMessage(Atomics.compareExchange(a, 0, 0, workerData.id) === 0);`;
  const wins = await Promise.all(Array.from({ length: 8 }, (_, i) => new Promise((res, rej) => {
    const w = new Worker(src, { eval: true, workerData: { sab, id: i + 1 } }); w.once('message', res); w.once('error', rej);
  })));
  assert.equal(wins.filter(Boolean).length, 1);
});
