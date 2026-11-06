#!/usr/bin/env node
// Deterministic MMR core tests for Computer Wisdom Merkle Mountains v0.3
// Domain-separated SHA-256: 0x00 leaf, 0x01 parent, 0x02 bag.
// Authority: false. No silent promotion.

const crypto = require('crypto');
const fs = require('fs');

const scheme = 'CW-MMR-SHA256-DS-V0.3-RIGHT-BAG';

function sha256(bytes) {
  return crypto.createHash('sha256').update(bytes).digest();
}
function hex(buf) {
  return Buffer.from(buf).toString('hex');
}
function unhex(str) {
  if (!/^[a-f0-9]{64}$/i.test(str)) throw new Error('Invalid digest');
  return Buffer.from(str, 'hex');
}
function concat(...parts) {
  return Buffer.concat(parts);
}

async function leafHash(payload) {
  return hex(sha256(concat(Buffer.from([0]), Buffer.from(payload, 'utf8'))));
}
async function parentHash(left, right) {
  return hex(sha256(concat(Buffer.from([1]), unhex(left), unhex(right))));
}
async function bagHash(left, right) {
  return hex(sha256(concat(Buffer.from([2]), unhex(left), unhex(right))));
}

async function bag(peaks) {
  if (!peaks.length) return null;
  let acc = peaks[peaks.length - 1].hash;
  for (let i = peaks.length - 2; i >= 0; i--) {
    acc = await bagHash(peaks[i].hash, acc);
  }
  return acc;
}

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

function empty() {
  return { receipts: [], peaks: [], root: null };
}

async function appendTo(state, payload, declaredHash) {
  const obj = JSON.parse(payload);
  const idx = state.receipts.length;
  if (obj.seq !== idx || JSON.stringify(obj) !== payload) {
    throw new Error('Non-canonical payload');
  }
  const hash = await leafHash(payload);
  if (declaredHash !== undefined && hash !== declaredHash) {
    throw new Error('Leaf hash mismatch');
  }
  let node = { hash, height: 0, start: idx, end: idx, left: null, right: null };
  while (state.peaks.length && state.peaks[state.peaks.length - 1].height === node.height) {
    const left = state.peaks.pop();
    node = {
      hash: await parentHash(left.hash, node.hash),
      height: node.height + 1,
      start: left.start,
      end: node.end,
      left,
      right: node
    };
  }
  state.peaks.push(node);
  state.receipts.push({ payload, leafHash: hash });
  state.root = await bag(state.peaks);
  return state;
}

async function proof(state, index) {
  const peakIndex = state.peaks.findIndex(p => p.start <= index && index <= p.end);
  let n = state.peaks[peakIndex];
  const path = [];
  while (n.left) {
    if (index <= n.left.end) {
      path.push({ side: 'right', hash: n.right.hash });
      n = n.left;
    } else {
      path.push({ side: 'left', hash: n.left.hash });
      n = n.right;
    }
  }
  path.reverse();
  return {
    scheme,
    leafCount: state.receipts.length,
    leafIndex: index,
    leafPayload: state.receipts[index].payload,
    leafHash: state.receipts[index].leafHash,
    siblings: path,
    peakIndex,
    peaks: state.peaks.map(p => ({ height: p.height, start: p.start, end: p.end, hash: p.hash })),
    root: state.root
  };
}

async function verify(p, trustedRoot, overridePayload) {
  if (p.scheme !== scheme || !/^[a-f0-9]{64}$/i.test(trustedRoot)) {
    throw new Error('Invalid trusted root');
  }
  const ranges = expectRanges(p.leafCount);
  if (p.peaks.length !== ranges.length) throw new Error('Peak count mismatch');
  for (let i = 0; i < ranges.length; i++) {
    const x = p.peaks[i], r = ranges[i];
    if (x.height !== r.height || x.start !== r.start || x.end !== r.end) {
      throw new Error('Peak partition mismatch');
    }
  }
  const target = p.peaks[p.peakIndex];
  if (p.siblings.length !== target.height) throw new Error('Sibling length');
  let hash = await leafHash(overridePayload === undefined ? p.leafPayload : overridePayload);
  if (hash !== p.leafHash) throw new Error('FAIL: Leaf payload has changed');
  let relative = p.leafIndex - target.start;
  for (const s of p.siblings) {
    const expectedSide = relative % 2 === 0 ? 'right' : 'left';
    if (s.side !== expectedSide) throw new Error('Invalid sibling direction');
    hash = s.side === 'right' ? await parentHash(hash, s.hash) : await parentHash(s.hash, hash);
    relative = Math.floor(relative / 2);
  }
  if (hash !== target.hash) throw new Error('FAIL: Sibling path does not match its peak');
  const root = await bag(p.peaks);
  if (root !== trustedRoot.toLowerCase() || root !== p.root) {
    throw new Error('FAIL: Root mismatch');
  }
  return true;
}

async function runTests() {
  const receipt = {
    schema: 'COMPUTERWISDOM_MMR_CORE_TEST_RECEIPT_V0_1',
    scheme,
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
    // Peak structure 1–16 leaves
    for (let n = 1; n <= 16; n++) {
      const st = empty();
      for (let i = 0; i < n; i++) {
        const rec = { seq: i, claim: `claim-${i}`, evidence: 'test', ts: '2026-01-01T00:00:00.000Z' };
        await appendTo(st, JSON.stringify(rec));
      }
      const expected = expectRanges(n);
      const actualHeights = st.peaks.map(p => p.height);
      const expectedHeights = expected.map(r => r.height);
      const ok = JSON.stringify(actualHeights) === JSON.stringify(expectedHeights) && st.peaks.length === expected.length;
      check(`peak-structure-${n}-leaves`, ok, `heights ${actualHeights.join(',')}`);
    }

    // Inclusion proofs + altered-leaf rejection for 1–16
    for (let n = 1; n <= 16; n++) {
      const st = empty();
      for (let i = 0; i < n; i++) {
        const rec = { seq: i, claim: `claim-${i}`, evidence: 'test', ts: '2026-01-01T00:00:00.000Z' };
        await appendTo(st, JSON.stringify(rec));
      }
      for (let i = 0; i < n; i++) {
        const p = await proof(st, i);
        const good = await verify(p, st.root);
        check(`inclusion-${n}-${i}`, good);

        // Altered leaf must fail
        let alteredFailed = false;
        try {
          const rec = JSON.parse(p.leafPayload);
          rec.claim = rec.claim + '-TAMPERED';
          await verify(p, st.root, JSON.stringify(rec));
        } catch (e) {
          alteredFailed = /Leaf payload has changed|FAIL/.test(e.message);
        }
        check(`altered-leaf-${n}-${i}`, alteredFailed);
      }
    }

    // Export replay
    const st = empty();
    for (let i = 0; i < 11; i++) {
      const rec = { seq: i, claim: `sample-${i}`, evidence: 'synth', ts: '2026-01-01T00:00:00.000Z' };
      await appendTo(st, JSON.stringify(rec));
    }
    const snapshot = {
      scheme,
      authority: false,
      leafCount: st.receipts.length,
      receipts: st.receipts.map(r => ({ ...r })),
      peaks: st.peaks.map(p => ({ height: p.height, start: p.start, end: p.end, hash: p.hash })),
      root: st.root
    };
    // Replay by re-appending
    const replayed = empty();
    for (const item of snapshot.receipts) {
      await appendTo(replayed, item.payload, item.leafHash);
    }
    const peaksMatch = JSON.stringify(replayed.peaks.map(p => ({ height: p.height, start: p.start, end: p.end, hash: p.hash }))) === JSON.stringify(snapshot.peaks);
    const rootMatch = replayed.root === snapshot.root;
    check('export-replay-11', peaksMatch && rootMatch);

    // Tampered export must fail
    let tamperFailed = false;
    try {
      const bad = JSON.parse(JSON.stringify(snapshot));
      bad.receipts[0].payload = bad.receipts[0].payload.replace('sample-0', 'TAMPER');
      const badSt = empty();
      for (const item of bad.receipts) await appendTo(badSt, item.payload, item.leafHash);
    } catch (e) {
      tamperFailed = true;
    }
    check('tampered-export-rejected', tamperFailed);

  } catch (err) {
    receipt.result = 'DIVERGE';
    receipt.errors.push({ name: 'uncaught', detail: err.message });
  }

  const path = 'mmr-test-receipt.json';
  fs.writeFileSync(path, JSON.stringify(receipt, null, 2) + '\n');
  console.log(JSON.stringify(receipt, null, 2));
  process.exit(receipt.result === 'MATCH' ? 0 : 1);
}

runTests().catch(err => {
  console.error(err);
  process.exit(1);
});
