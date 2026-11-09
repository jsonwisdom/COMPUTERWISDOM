import { createHash } from 'node:crypto';

/** CI-FIRST JSON profile v0.3: UTF-8, sorted object keys, no numbers outside safe integers,
 * no undefined/NaN/infinity, no cycles; all monetary values are integer micro-USD. */
export function canonical(value) {
  if (value === null || typeof value === 'boolean' || typeof value === 'string') return JSON.stringify(value);
  if (typeof value === 'number') {
    if (!Number.isSafeInteger(value)) throw Error('NONCANONICAL_NUMBER');
    return String(value);
  }
  if (Array.isArray(value)) return '[' + value.map(canonical).join(',') + ']';
  if (value && typeof value === 'object' && Object.getPrototypeOf(value) === Object.prototype) {
    return '{' + Object.keys(value).sort().map(k => JSON.stringify(k) + ':' + canonical(value[k])).join(',') + '}';
  }
  throw Error('NONCANONICAL_VALUE');
}
export function hash(value) { return createHash('sha256').update(Buffer.from(canonical(value), 'utf8')).digest('hex'); }
export function bytesHash(value) { return createHash('sha256').update(value).digest('hex'); }
export function insist(test, reason) { if (!test) throw Error(reason); }
export const HEX64 = /^[a-f0-9]{64}$/;
export const ID = /^[a-zA-Z0-9][a-zA-Z0-9_.:-]{2,95}$/;
export function decimalMicroUSD(str) {
  insist(typeof str === 'string' && /^(0|[1-9]\d*)(\.\d{1,6})?$/.test(str), 'PRICE_FORMAT');
  const [whole, fractional = ''] = str.split('.');
  const sum = BigInt(whole) * 1000000n + BigInt((fractional + '000000').slice(0, 6));
  insist(sum <= BigInt(Number.MAX_SAFE_INTEGER), 'PRICE_OVERFLOW');
  return Number(sum);
}
export function costMicroUSD(input, output, inRate, outRate) {
  const ceil = (n, rate) => (BigInt(n) * BigInt(rate) + 999n) / 1000n;
  const total = ceil(input, inRate) + ceil(output, outRate);
  insist(total <= BigInt(Number.MAX_SAFE_INTEGER), 'COST_OVERFLOW');
  return Number(total);
}
