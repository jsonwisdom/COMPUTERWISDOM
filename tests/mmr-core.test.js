#!/usr/bin/env node
// Deterministic MMR core tests for Computer Wisdom Merkle Mountains v0.3
// Loads and exercises the real CW_MMR from the classroom HTML.
// Authority: false. No silent promotion.

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const htmlPath = path.resolve(__dirname, '../docs/classes-with-glasses/merkle-mountains/index.html');
const html = fs.readFileSync(htmlPath, 'utf8');

// Extract the CW_MMR script (the first <script> that defines it)
const scriptMatch = html.match(/<script>([\s\S]*?const CW_MMR = \([\s\S]*?\)\(\);[\s\S]*?)<\/script>/);
if (!scriptMatch) {
  console.error('FAIL: Could not extract CW_MMR script from HTML');
  process.exit(1);
}

const scriptSource = scriptMatch[1];

// Node 20+ provides globalThis.crypto with subtle
if (!globalThis.crypto?.subtle) {
  console.error('FAIL: Node crypto.subtle unavailable');
  process.exit(1);
}

const sandbox = {
  globalThis,
  console,
  TextEncoder,
  Uint8Array,
  JSON,
  Error,
  Math,
  Number,
  Array,
  Date,
  crypto: globalThis.crypto,
};
sandbox.globalThis = sandbox;

const context = vm.createContext(sandbox);
vm.runInContext(scriptSource, context);

const CW_MMR = sandbox.CW_MMR;
if (!CW_MMR || typeof CW_MMR.appendTo !== 'function') {
  console.error('FAIL: CW_MMR not available after evaluation');
  process.exit(1);
}

const scheme = CW_MMR.scheme;

function expectRanges(count) {
  let remain = count, at = 0, result = [];
  while (remain) {
    const height = Math.floor(Math.log2(remain));
    const size = 1 << height;
    result.push({ height, start: at, end: at + size - 1 });
    at += size;
    remain -= size;
  }
  return result;
}

async function runTests() {
  const receipt = {
    schema: 'COMPUTERWISDOM_MMR_CORE_TEST_RECEIPT_V0_2',
    scheme,
    source: 'docs/classes-with-glasses/merkle-mountains/index.html',
    authority: false,
    promotion: false,
    result: 'MATCH',
    checks: [],
    errors: [],
    timestamp: new Date().toISOString()
  };

  function check(name, ok, detail = '') {
    receipt.checks.push({ name, status: ok ? 'PASS' : 'FAIL', detail });
    if (!ok) {
      receipt.result = 'DIVERGE';
      receipt.errors.push({ name, detail });
    }
  }

  try {
    // Peak structure 1–16 leaves using the real CW_MMR
    for (let n = 1; n <= 16; n++) {
      const st = CW_MMR.empty();
      for (let i = 0; i < n; i++) {
        const rec = { seq: i, claim: `claim-${i}`, evidence: 'test', ts: '2026-01-01T00:00:00.000Z' };
        await CW_MMR.appendTo(st, JSON.stringify(rec));
      }
      const expected = expectRanges(n);
      const actualHeights = st.peaks.map(p => p.height);
      const expectedHeights = expected.map(r => r.height);
      const ok = JSON.stringify(actualHeights) === JSON.stringify(expectedHeights) && st.peaks.length === expected.length;
      check(`peak-structure-${n}-leaves`, ok, `heights ${actualHeights.join(',')}`);
    }

    // Inclusion proofs + altered-leaf rejection for 1–16
    for (let n = 1; n <= 16; n++) {
      const st = CW_MMR.empty();
      for (let i = 0; i < n; i++) {
        const rec = { seq: i, claim: `claim-${i}`, evidence: 'test', ts: '2026-01-01T00:00:00.000Z' };
        await CW_MMR.appendTo(st, JSON.stringify(rec));
      }
      for (let i = 0; i < n; i++) {
        const p = await CW_MMR.proof(st, i);
        const good = await CW_MMR.verify(p, st.root);
        check(`inclusion-${n}-${i}`, good);

        // Altered leaf must fail
        let alteredFailed = false;
        try {
          const rec = JSON.parse(p.leafPayload);
          rec.claim = rec.claim + '-TAMPERED';
          await CW_MMR.verify(p, st.root, JSON.stringify(rec));
        } catch (e) {
          alteredFailed = /Leaf payload has changed|FAIL/.test(e.message);
        }
        check(`altered-leaf-${n}-${i}`, alteredFailed);
      }
    }

    // Export replay using real snapshot + replay
    const st = CW_MMR.empty();
    for (let i = 0; i < 11; i++) {
      const rec = { seq: i, claim: `sample-${i}`, evidence: 'synth', ts: '2026-01-01T00:00:00.000Z' };
      await CW_MMR.appendTo(st, JSON.stringify(rec));
    }
    const snapshot = CW_MMR.snapshot(st);
    const replayed = await CW_MMR.replay(snapshot);
    const peaksMatch = JSON.stringify(replayed.peaks.map(p => ({ height: p.height, start: p.start, end: p.end, hash: p.hash }))) === JSON.stringify(snapshot.peaks);
    const rootMatch = replayed.root === snapshot.root;
    check('export-replay-11', peaksMatch && rootMatch);

    // Tampered export must fail
    let tamperFailed = false;
    try {
      const bad = JSON.parse(JSON.stringify(snapshot));
      bad.receipts[0].payload = bad.receipts[0].payload.replace('sample-0', 'TAMPER');
      await CW_MMR.replay(bad);
    } catch (e) {
      tamperFailed = true;
    }
    check('tampered-export-rejected', tamperFailed);

  } catch (err) {
    receipt.result = 'DIVERGE';
    receipt.errors.push({ name: 'uncaught', detail: err.message });
  }

  const outPath = path.resolve(__dirname, '../mmr-test-receipt.json');
  fs.writeFileSync(outPath, JSON.stringify(receipt, null, 2) + '\n');
  console.log(JSON.stringify(receipt, null, 2));
  process.exit(receipt.result === 'MATCH' ? 0 : 1);
}

runTests().catch(err => {
  console.error(err);
  process.exit(1);
});
