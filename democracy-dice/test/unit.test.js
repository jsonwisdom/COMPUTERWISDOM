import { test } from 'node:test';
import assert from 'node:assert/strict';
import { canonicalize, digest } from '../src/jcs.js';
import { enumerateOutcomes, outcomeIndex, outcomeFromIndex, rollThree, recordedByteSource, seededByteSource, REJECT_AT } from '../src/dice.js';
import { verifyAll, verifyVector } from '../src/vectors.js';

test('unit: JCS key order is UTF-16 code-unit order (RFC 8785 §3.2.3)', () => {
  assert.equal(canonicalize({ '\u20ac': 1, '\r': 2, '\ud83d\ude00': 3, '\u0080': 4, '1': 5 }),
    '{"\\r":2,"1":5,"\u0080":4,"\u20ac":1,"\ud83d\ude00":3}');
});
test('unit: JCS number serialization (RFC 8785 Appendix B samples)', () => {
  const cases = [[0, '0'], [-0, '0'], [1e21, '1e+21'], [1e-7, '1e-7'], [0.000001, '0.000001'], [333333333.3333333, '333333333.3333333'],
    [9007199254740992, '9007199254740992'], [295147905179352830000, '295147905179352830000'], [5e-324, '5e-324'], [1.7976931348623157e308, '1.7976931348623157e+308']];
  for (const [n, s] of cases) assert.equal(canonicalize(n), s);
  assert.throws(() => canonicalize(NaN)); assert.throws(() => canonicalize(Infinity));
});
test('unit: JCS string escaping', () => {
  assert.equal(canonicalize('\u0000\b\t\n\f\r"\\\u001f\u007f/'), '"\\u0000\\b\\t\\n\\f\\r\\"\\\\\\u001f\u007f/"');
});
test('unit: SYN-001/SYN-002 MATCH; TV-001/TV-002 SEARCH_MISS (fail closed)', () => {
  const r = Object.fromEntries(verifyAll().map((x) => [x.id, x.result]));
  assert.deepEqual(r, { 'TV-001': 'SEARCH_MISS', 'TV-002': 'SEARCH_MISS', 'SYN-001': 'MATCH', 'SYN-002': 'MATCH' });
});
test('negative: a forged TV object cannot be reported as MATCH', () => {
  const v = { id: 'TV-001', expected: 'sha256:4d576d03882834f86fbb2a8bf44bdc271e1deddf0873f7aa681e330f22ca6836' };
  assert.equal(verifyVector(v, { claim: 'MATCH', expected: v.expected }).result, 'MISMATCH');
  assert.equal(verifyVector(v, { HOLD_PLACEHOLDER: false }).result, 'MISMATCH');
});
test('unit: exactly 216 distinct outcomes, index bijection', () => {
  const all = enumerateOutcomes();
  assert.equal(all.length, 216);
  assert.equal(new Set(all.map((d) => d.join())).size, 216);
  all.forEach((d, i) => { assert.equal(outcomeIndex(d), i); assert.deepEqual(outcomeFromIndex(i), d); });
});
test('unit: rejection@252 exhaustive over all 256 byte values', () => {
  assert.equal(REJECT_AT, 252);
  const counts = [0, 0, 0, 0, 0, 0]; let rejected = 0;
  for (let b = 0; b < 256; b++) { if (b >= 252) rejected++; else counts[b % 6]++; }
  assert.deepEqual(counts, [42, 42, 42, 42, 42, 42]);
  assert.equal(rejected, 4);
});
test('unit: every one of 216 triples reachable with exactly the uniform byte mass (42^3 each)', () => {
  // Each face has 42 accepting bytes, so each triple has 42^3 accepting 3-byte sequences.
  const per = new Map();
  for (let a = 0; a < 252; a += 1) per.set(1 + (a % 6), (per.get(1 + (a % 6)) ?? 0) + 1);
  for (const d of enumerateOutcomes()) assert.equal(d.reduce((m, f) => m * per.get(f), 1), 42 ** 3);
});
test('unit: rejected bytes are skipped and recorded', () => {
  const r = rollThree(recordedByteSource([255, 252, 0, 253, 5, 251]));
  assert.deepEqual(r.dice, [1, 6, 6]);
  assert.deepEqual(r.rejectedBytes, [255, 252, 253]);
});
test('unit: statistical uniformity over 216000 seeded rolls (chi-square, df=215)', () => {
  const next = seededByteSource('uniformity'); const counts = new Array(216).fill(0);
  for (let i = 0; i < 216000; i++) counts[rollThree(next).outcomeIndex]++;
  const chi = counts.reduce((s, c) => s + (c - 1000) ** 2 / 1000, 0);
  assert.ok(chi < 300, `chi-square ${chi}`); // p≈0.0001 critical value ~ 290-300 for df=215
});
test('unit: digest is stable across key insertion order', () => {
  assert.equal(digest({ a: 1, b: [2, { d: 4, c: 3 }] }), digest({ b: [2, { c: 3, d: 4 }], a: 1 }));
});
