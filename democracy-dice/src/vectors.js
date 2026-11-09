import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { digest } from './jcs.js';
const FIX = join(dirname(fileURLToPath(import.meta.url)), '..', 'fixtures');

/** Fail-closed vector verification. MATCH only on byte-level digest equality. */
export function verifyVector(v, obj) {
  const actual = digest(obj);
  if (actual === v.expected) return { id: v.id, result: 'MATCH', actual };
  if (obj && obj.HOLD_PLACEHOLDER === true) return { id: v.id, result: 'SEARCH_MISS', actual };
  return { id: v.id, result: 'MISMATCH', actual };
}
export function verifyAll() {
  const { vectors } = JSON.parse(readFileSync(join(FIX, 'vectors.json'), 'utf8'));
  return vectors.map((v) => verifyVector(v, JSON.parse(readFileSync(join(FIX, v.file), 'utf8'))));
}
