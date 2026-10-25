import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validate } from '../src/validate.js';
import { produce } from '../src/replay.js';
import { SEED } from './helpers.js';

const roll = () => structuredClone(produce(SEED, 1).rolls[0]);
test('schema: produced RollReceipt validates', () => assert.ok(validate('RollReceipt', roll()).ok));
test('security: AUTHORITY_CREATED=true rejected', () => {
  const r = roll(); r.AUTHORITY_CREATED = true; assert.equal(validate('RollReceipt', r).ok, false);
});
test('security: status other than HOLD rejected', () => {
  const r = roll(); r.status = 'GREEN'; assert.equal(validate('RollReceipt', r).ok, false);
});
test('negative: dice not derivable from bytes rejected', () => {
  const r = roll(); r.dice = [r.dice[0] % 6 + 1, r.dice[1], r.dice[2]]; r.outcomeIndex = (r.dice[0] - 1) * 36 + (r.dice[1] - 1) * 6 + r.dice[2] - 1;
  assert.match(validate('RollReceipt', r).errors.join(), /rawBytes/);
});
test('negative: unknown property rejected (strict)', () => {
  const r = roll(); r.extra = 1; assert.equal(validate('RollReceipt', r).ok, false);
});
test('negative: data label outside LIVE|MOCK|SYNTHETIC|LIVE_UNAVAILABLE rejected', () => {
  const r = roll(); r.dataLabel = 'VERIFIED'; assert.equal(validate('RollReceipt', r).ok, false);
});
test('security: CRYPTOGRAPHIC_IDENTITY_VERIFIED=true without evidence rejected', () => {
  const a = { type: 'ApprovalReceipt', approvalId: '0'.repeat(32), subjectDigest: 'sha256:' + '0'.repeat(64), approver: 'jason',
    issuedAt: '2026-10-25T13:00:00Z', nonce: '1'.repeat(32), mac: 'hmac-sha256:' + '2'.repeat(64),
    HUMAN_APPROVAL_RECORDED: true, CRYPTOGRAPHIC_IDENTITY_VERIFIED: true, identityEvidence: null, consumed: false,
    status: 'HOLD', AUTHORITY_CREATED: false, FINAL_AUTHORITY: 'JASON' };
  assert.equal(validate('ApprovalReceipt', a).ok, false);
  a.CRYPTOGRAPHIC_IDENTITY_VERIFIED = false; assert.ok(validate('ApprovalReceipt', a).ok);
});
test('security: finance provenance cannot claim liveSpend or walletSigning', () => {
  const f = { type: 'FinanceProvenance', subject: 'x', claims: [], sources: [{ sourceId: 's', adapter: 'FEC', availability: 'NOT_CONFIGURED', retrievedDigest: null, operator: 'FEC' }],
    independence: { declared: false, distinctOperators: 1, basis: 'b' }, liveSpend: false, walletSigning: false, dataLabel: 'LIVE_UNAVAILABLE', AUTHORITY_CREATED: false };
  assert.ok(validate('FinanceProvenance', f).ok);
  assert.equal(validate('FinanceProvenance', { ...f, liveSpend: true }).ok, false);
  assert.equal(validate('FinanceProvenance', { ...f, walletSigning: true }).ok, false);
  assert.equal(validate('FinanceProvenance', { ...f, dataLabel: 'LIVE' }).ok, false, 'LIVE label without AVAILABLE source');
  assert.equal(validate('FinanceProvenance', { ...f, independence: { declared: true, distinctOperators: 1, basis: 'b' } }).ok, false);
});
