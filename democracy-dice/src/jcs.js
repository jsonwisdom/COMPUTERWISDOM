// RFC 8785 JSON Canonicalization Scheme.
// - Strings: ECMAScript JSON.stringify escaping (RFC 8785 §3.2.2.2).
// - Numbers: ECMAScript Number-to-String (§3.2.2.3); NaN/Infinity rejected.
// - Object keys sorted by UTF-16 code units (§3.2.3); JS default sort is UTF-16 code-unit order.
import { createHash } from 'node:crypto';

export function canonicalize(v) {
  if (v === null) return 'null';
  switch (typeof v) {
    case 'boolean': return v ? 'true' : 'false';
    case 'number':
      if (!Number.isFinite(v)) throw new TypeError('JCS: non-finite number');
      return Object.is(v, -0) ? '0' : String(v);
    case 'string': return JSON.stringify(v);
    case 'object':
      if (Array.isArray(v)) return '[' + v.map(canonicalize).join(',') + ']';
      return '{' + Object.keys(v).filter((k) => v[k] !== undefined).sort()
        .map((k) => JSON.stringify(k) + ':' + canonicalize(v[k])).join(',') + '}';
    default: throw new TypeError(`JCS: unsupported type ${typeof v}`);
  }
}

export function sha256Hex(s) { return createHash('sha256').update(s, 'utf8').digest('hex'); }
export function digest(obj) { return 'sha256:' + sha256Hex(canonicalize(obj)); }
