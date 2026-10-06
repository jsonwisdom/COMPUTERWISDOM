import fs from 'node:fs';

const path = 'wallet-control/index.html';
const html = fs.readFileSync(path, 'utf8');

function assert(condition, message) {
  if (!condition) {
    console.error('WALLET_CONTROL_VERIFY_FAIL:', message);
    process.exit(1);
  }
}

const inlineMatches = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
assert(inlineMatches.length === 1, `expected exactly one inline script, found ${inlineMatches.length}`);
const inline = inlineMatches[0][1];

// Syntax gate: compile without executing browser code.
try {
  new Function(inline);
} catch (err) {
  console.error('WALLET_CONTROL_VERIFY_FAIL: inline JavaScript syntax error');
  throw err;
}

// Regression gate: every named event-handler symbol must be declared.
const handlerRefs = [...inline.matchAll(/addEventListener\s*\([^,]+,\s*([A-Za-z_$][\w$]*)\s*\)/g)].map(m => m[1]);
const declared = new Set([
  ...[...inline.matchAll(/(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(/g)].map(m => m[1]),
  ...[...inline.matchAll(/\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=/g)].map(m => m[1])
]);
const missingHandlers = [...new Set(handlerRefs.filter(name => !declared.has(name)))];
assert(missingHandlers.length === 0, `undefined event handler(s): ${missingHandlers.join(', ')}`);

const required = [
  'personal_sign',
  'ERC1271_IS_VALID_SIGNATURE',
  'verification_block_tag',
  'verification_block_fallback',
  'challenge_block_call_error',
  'script_integrity',
  "a.download = 'wallet-control-observation-receipt-v0.1.json'",
  'receiptDownloadBtn',
  'transaction_hash:null',
  'trade:false',
  'transfer:false',
  'authority_created:false',
  'joins:0'
];
for (const token of required) assert(html.includes(token), `missing required token: ${token}`);

const forbidden = [
  'shareReceipt',
  'eth_sendTransaction',
  'wallet_sendCalls',
  'eth_sendRawTransaction'
];
for (const token of forbidden) assert(!html.includes(token), `forbidden or stale token present: ${token}`);

const sriChecks = [
  'integrity="sha384-Jcaa5XJIs34lC6Co7Ye/mAuxCGLTEdUYQuIyl4UrwRduYb6mOmW7SUCOPX/jdsKV"',
  'integrity="sha384-lApM4ELRuFNT7NgNqnXB2zFWgSDdhVvmnOHov2DPJz/2zuNpZImXBeklFr18ilvi"',
  'crossorigin="anonymous"'
];
for (const token of sriChecks) assert(html.includes(token), `missing script-integrity boundary: ${token}`);

console.log('WALLET_CONTROL_PAGE_VERIFY_PASS');
console.log(JSON.stringify({
  handler_count: handlerRefs.length,
  unique_handler_count: new Set(handlerRefs).size,
  replay_hardened_fields: true,
  download_receipt: true,
  transaction_methods_present: false
}, null, 2));
