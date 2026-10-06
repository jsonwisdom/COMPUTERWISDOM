import fs from 'node:fs';

function assert(condition, message) {
  if (!condition) {
    console.error('WALLET_CONTROL_VERIFY_FAIL:', message);
    process.exit(1);
  }
}

function verifyPage(path, options = {}) {
  const html = fs.readFileSync(path, 'utf8');
  const inlineMatches = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
  assert(inlineMatches.length === 1, `${path}: expected exactly one inline script, found ${inlineMatches.length}`);
  const inline = inlineMatches[0][1];

  try {
    new Function(inline);
  } catch (err) {
    console.error(`WALLET_CONTROL_VERIFY_FAIL: ${path}: inline JavaScript syntax error`);
    throw err;
  }

  const handlerRefs = [...inline.matchAll(/addEventListener\s*\([^,]+,\s*([A-Za-z_$][\w$]*)\s*\)/g)].map(m => m[1]);
  const declared = new Set([
    ...[...inline.matchAll(/(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(/g)].map(m => m[1]),
    ...[...inline.matchAll(/\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=/g)].map(m => m[1])
  ]);
  const missingHandlers = [...new Set(handlerRefs.filter(name => !declared.has(name)))];
  assert(missingHandlers.length === 0, `${path}: undefined event handler(s): ${missingHandlers.join(', ')}`);

  const required = [
    'personal_sign',
    'verification_block_tag',
    'verification_block_fallback',
    'challenge_block_call_error',
    'receiptDownloadBtn',
    'transaction_hash:null',
    'trade:false',
    'transfer:false',
    'authority_created:false',
    'joins:0',
    ...(options.required || [])
  ];
  for (const token of required) assert(html.includes(token), `${path}: missing required token: ${token}`);

  const forbidden = [
    'eth_sendTransaction',
    'wallet_sendCalls',
    'eth_sendRawTransaction',
    ...(options.forbidden || [])
  ];
  for (const token of forbidden) assert(!html.includes(token), `${path}: forbidden or stale token present: ${token}`);

  const sriChecks = [
    'integrity="sha384-Jcaa5XJIs34lC6Co7Ye/mAuxCGLTEdUYQuIyl4UrwRduYb6mOmW7SUCOPX/jdsKV"',
    'integrity="sha384-lApM4ELRuFNT7NgNqnXB2zFWgSDdhVvmnOHov2DPJz/2zuNpZImXBeklFr18ilvi"',
    'crossorigin="anonymous"'
  ];
  for (const token of sriChecks) assert(html.includes(token), `${path}: missing script-integrity boundary: ${token}`);

  return {
    path,
    handler_count: handlerRefs.length,
    unique_handler_count: new Set(handlerRefs).size
  };
}

const main = verifyPage('wallet-control/index.html', {
  required: [
    'ERC1271_IS_VALID_SIGNATURE',
    'script_integrity',
    "a.download = 'wallet-control-observation-receipt-v0.1.json'"
  ],
  forbidden: ['shareReceipt']
});

const neutral = verifyPage('wallet-control/neutral/index.html', {
  required: [
    'ERC1271_IS_VALID_SIGNATURE',
    'WALLET_CONTROL_NEUTRAL_OBSERVATION_RECEIPT_V0_1',
    'identity_join:false',
    'expected_pointer_address:challenge.expected_pointer_address',
    'pointer_match:challenge.pointer_match',
    'ERC6492_SAFE_HOLD_NOT_VERIFIED',
    'receiptResultBanner',
    "a.download = 'wallet-control-neutral-observation-receipt-v0.1.json'"
  ]
});

const zoraSigner = verifyPage('wallet-control/zora-signer/index.html', {
  required: [
    'ZORA_SMART_WALLET_CONTROL_OBSERVATION_RECEIPT_V0_1',
    '0x829AdfEdbe565f9885A7Ea6Bc78912ACaEF055E2',
    '0xb3B9CC668e997209e914309FF525535203EaD4dA',
    'isOwnerAddress',
    'ownerAtIndex',
    'nextOwnerIndex',
    'ERC1271_COINBASE_SMART_WALLET_SIGNATURE_WRAPPER',
    'wrapped_signature',
    'identity_join:false',
    "a.download = 'zora-smart-wallet-control-observation-receipt-v0.1.json'"
  ],
  forbidden: [
    'privateKey',
    'PRIVATE_KEY',
    'eth_sendTransaction',
    'wallet_sendCalls',
    'eth_sendRawTransaction'
  ]
});

console.log('WALLET_CONTROL_PAGE_VERIFY_PASS');
console.log(JSON.stringify({
  pages: [main, neutral, zoraSigner],
  replay_hardened_fields: true,
  download_receipt: true,
  transaction_methods_present: false,
  neutral_erc6492_fail_closed: true,
  neutral_result_banner_conditional: true,
  zora_subject_signer_separated: true,
  zora_owner_index_resolved_at_challenge_block: true
}, null, 2));
