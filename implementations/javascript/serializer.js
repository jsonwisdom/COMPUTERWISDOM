"use strict";
// ReplayOS canonical snapshot serializer v1 (JavaScript).
// Independent implementation; RFC 8785-style JSON with signed-int53-only numbers.

const crypto = require("crypto");
const REQUIRED = new Set(["schema_version", "serializer_version", "builder_version", "lanes"]);
const FORBIDDEN = new Set(["wall_clock", "timestamp", "updated_at", "created_at", "now", "rng"]);

class CanonicalError extends Error {
  constructor(code) { super(code); this.code = code; }
}

function assertUnicode(text) {
  for (let i = 0; i < text.length; i++) {
    const code = text.charCodeAt(i);
    if (code >= 0xD800 && code <= 0xDBFF) {
      const next = text.charCodeAt(i + 1);
      if (!(next >= 0xDC00 && next <= 0xDFFF)) throw new CanonicalError("LONE_SURROGATE");
      i++;
    } else if (code >= 0xDC00 && code <= 0xDFFF) {
      throw new CanonicalError("LONE_SURROGATE");
    }
  }
}

function parseStrict(raw) {
  let i = 0;
  const ws = () => { while (/\s/.test(raw[i] || "")) i++; };
  const string = () => {
    const start = i++;
    let escaped = false;
    while (i < raw.length) {
      const c = raw[i++];
      if (escaped) { escaped = false; continue; }
      if (c === "\\") { escaped = true; continue; }
      if (c === '"') {
        let value;
        try { value = JSON.parse(raw.slice(start, i)); } catch { throw new CanonicalError("INVALID_JSON"); }
        assertUnicode(value);
        return value;
      }
      if (c.charCodeAt(0) < 0x20) throw new CanonicalError("INVALID_JSON");
    }
    throw new CanonicalError("INVALID_JSON");
  };
  const value = () => {
    ws();
    if (raw[i] === '"') return string();
    if (raw[i] === "{") {
      i++; const out = {}; const seen = new Set(); ws();
      if (raw[i] === "}") { i++; return out; }
      while (true) {
        ws(); if (raw[i] !== '"') throw new CanonicalError("INVALID_JSON");
        const key = string(); ws();
        if (seen.has(key)) throw new CanonicalError("DUPLICATE_KEY");
        seen.add(key);
        if (raw[i++] !== ":") throw new CanonicalError("INVALID_JSON");
        out[key] = value(); ws();
        if (raw[i] === "}") { i++; return out; }
        if (raw[i++] !== ",") throw new CanonicalError("INVALID_JSON");
      }
    }
    if (raw[i] === "[") {
      i++; const out = []; ws();
      if (raw[i] === "]") { i++; return out; }
      while (true) {
        out.push(value()); ws();
        if (raw[i] === "]") { i++; return out; }
        if (raw[i++] !== ",") throw new CanonicalError("INVALID_JSON");
      }
    }
    for (const [token, result] of [["true", true], ["false", false], ["null", null]]) {
      if (raw.startsWith(token, i)) { i += token.length; return result; }
    }
    const match = raw.slice(i).match(/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/);
    if (!match) throw new CanonicalError("INVALID_JSON");
    i += match[0].length;
    const number = Number(match[0]);
    if (!Number.isSafeInteger(number) || /[.eE]/.test(match[0])) throw new CanonicalError("ILLEGAL_NUMBER");
    return number;
  };
  const result = value(); ws();
  if (i !== raw.length) throw new CanonicalError("INVALID_JSON");
  return result;
}

function encode(value) {
  if (value === null) return "null";
  if (value === true) return "true";
  if (value === false) return "false";
  if (typeof value === "number") {
    if (!Number.isSafeInteger(value)) throw new CanonicalError("ILLEGAL_NUMBER");
    return String(value);
  }
  if (typeof value === "string") { assertUnicode(value); return JSON.stringify(value); }
  if (Array.isArray(value)) return "[" + value.map(encode).join(",") + "]";
  if (typeof value === "object") {
    return "{" + Object.keys(value).sort().map(k => encode(k) + ":" + encode(value[k])).join(",") + "}";
  }
  throw new CanonicalError("UNSUPPORTED_TYPE");
}

function validateEnvelope(value) {
  if (!value || Array.isArray(value) || typeof value !== "object") throw new CanonicalError("ENVELOPE_NOT_OBJECT");
  for (const key of Object.keys(value)) if (FORBIDDEN.has(key)) throw new CanonicalError("WALL_CLOCK_IN_SNAPSHOT");
  for (const key of Object.keys(value)) if (!REQUIRED.has(key)) throw new CanonicalError("UNKNOWN_FIELD");
  for (const key of REQUIRED) if (!(key in value)) throw new CanonicalError("VERSIONLESS_ENVELOPE");
  if (value.schema_version !== "replayos-snapshot/1") throw new CanonicalError("SCHEMA_VERSION_UNSUPPORTED");
  if (value.serializer_version !== "rfc8785-jcs-int53/1") throw new CanonicalError("SERIALIZER_VERSION_UNSUPPORTED");
  if (value.builder_version !== "replayos-snapshot-builder/1") throw new CanonicalError("BUILDER_VERSION_UNSUPPORTED");
  if (!value.lanes || Array.isArray(value.lanes) || typeof value.lanes !== "object") throw new CanonicalError("LANES_NOT_OBJECT");
}

function canonicalize(raw) {
  const value = parseStrict(raw);
  validateEnvelope(value);
  return Buffer.from(encode(value), "utf8");
}
function stateHash(data) { return crypto.createHash("sha256").update(data).digest("hex"); }
module.exports = { CanonicalError, canonicalize, stateHash };
