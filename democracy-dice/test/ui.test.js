import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
const html = readFileSync(new URL('../ui/index.html', import.meta.url), 'utf8');
const js = readFileSync(new URL('../ui/dice-ui.js', import.meta.url), 'utf8');
test('ui: accessibility basics present', () => {
  assert.match(html, /<html lang="en">/); assert.match(html, /<label for="topic">/);
  assert.match(html, /aria-live="polite"/); assert.match(html, /<button id="roll" type="button">/);
  assert.match(html, /focus-visible/);
});
test('ui: SYNTHETIC + HOLD + AUTHORITY_CREATED=false labeled; rejection@252 used', () => {
  assert.match(html, /SYNTHETIC/); assert.match(html, /STATUS=HOLD/); assert.match(html, /AUTHORITY_CREATED=false/);
  assert.match(js, /b < 252/); assert.match(js, /SYNTHETIC roll/);
  assert.doesNotMatch(js, /Math\.random/); assert.doesNotMatch(js, /fetch\(/);
});
