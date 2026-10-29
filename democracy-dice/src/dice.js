// Unbiased three-D6 selector. Rejection sampling at 252 (252 = 42*6, largest multiple of 6 <= 256).
import { createHash, randomBytes } from 'node:crypto';

export const REJECT_AT = 252;

/** Deterministic byte source: SHA-256(seed || ":" || counter) blocks. */
export function seededByteSource(seed) {
  let counter = 0, buf = Buffer.alloc(0), pos = 0;
  return () => {
    if (pos >= buf.length) {
      buf = createHash('sha256').update(`${seed}:${counter++}`).digest();
      pos = 0;
    }
    return buf[pos++];
  };
}

/** Recorded byte source: replays exactly the given bytes; throws if exhausted. */
export function recordedByteSource(bytes) {
  let i = 0;
  return () => {
    if (i >= bytes.length) throw new Error('recorded draws exhausted');
    return bytes[i++];
  };
}

/** OS CSPRNG source (non-replayable unless bytes are recorded). */
export function cryptoByteSource() { return () => randomBytes(1)[0]; }

export function drawDie(next, log) {
  for (;;) {
    const b = next();
    if (!Number.isInteger(b) || b < 0 || b > 255) throw new RangeError('byte out of range');
    log.raw.push(b);
    if (b >= REJECT_AT) { log.rejected.push(b); continue; }
    return 1 + (b % 6);
  }
}

export function rollThree(next) {
  const log = { raw: [], rejected: [] };
  const dice = [drawDie(next, log), drawDie(next, log), drawDie(next, log)];
  return { dice, outcomeIndex: outcomeIndex(dice), rawBytes: log.raw, rejectedBytes: log.rejected };
}

export function outcomeIndex([a, b, c]) { return (a - 1) * 36 + (b - 1) * 6 + (c - 1); }
export function outcomeFromIndex(i) {
  if (!Number.isInteger(i) || i < 0 || i > 215) throw new RangeError('index');
  return [1 + Math.floor(i / 36), 1 + (Math.floor(i / 6) % 6), 1 + (i % 6)];
}

/** Exhaustive enumeration of all 6^3 = 216 outcomes. */
export function enumerateOutcomes() {
  const out = [];
  for (let a = 1; a <= 6; a++) for (let b = 1; b <= 6; b++) for (let c = 1; c <= 6; c++) out.push([a, b, c]);
  return out;
}
