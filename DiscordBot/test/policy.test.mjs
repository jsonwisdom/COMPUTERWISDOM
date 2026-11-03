import test from "node:test";
import assert from "node:assert/strict";
import {
  AUTHORITY,
  enforceAuthorityFalse,
  normalizePrompt,
} from "../src/policy.mjs";

test("authority is permanently false", () => {
  assert.equal(AUTHORITY, false);
});

test("responses end with authority=false", () => {
  assert.equal(enforceAuthorityFalse("placed"), "placed\n\nauthority=false");
  assert.equal(enforceAuthorityFalse("placed\nauthority=false"), "placed\nauthority=false");
});

test("prompts are trimmed and bounded", () => {
  assert.equal(normalizePrompt("  hello  "), "hello");
  assert.equal(normalizePrompt("x".repeat(5000)).length, 4000);
});
