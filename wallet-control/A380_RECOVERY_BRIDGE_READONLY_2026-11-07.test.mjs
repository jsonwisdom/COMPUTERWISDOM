import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';

// Synthetic keys and fake wallet providers ONLY; no live credentials or network traffic.
const HTML = readFileSync(new URL('./A380_RECOVERY_BRIDGE_READONLY_2026-11-07.txt', import.meta.url), 'utf8');
const script = HTML.match(/<script>\s*([\s\S]+?)<\/script>/)?.[1];
assert.ok(script, 'Bridge inline script must exist');
const A380 = '0xa380552a27b0a5a2874ea7aa52cac09f542002e8';

function scenario({
  route='base',address=A380,chain='0x2105',origin='https://jsonwisdom.github.io',
  consent=false,coinbase=true,baseSDK=true
}={}) {
  const elements = {
    base:{disabled:false,addEventListener(_event, fn){this.click=fn}},
    coinbase:{disabled:false,addEventListener(_event, fn){this.click=fn}},
    receipt:{textContent:''}
  };
  const calls=[];
  const provider = {
    isCoinbaseWallet:coinbase,
    async request({method}) {
      calls.push(method);
      switch(method) {
        case 'eth_accounts': return consent?[]:[address];
        case 'eth_requestAccounts': return [address];
        case 'eth_chainId': return chain;
        default: throw Error('UNEXPECTED_RPC: '+method);
      }
    }
  };
  const window = {
    ethereum:provider,
    addEventListener(){},
    dispatchEvent(){}
  };
  if (baseSDK) window.createBaseAccountSDK = ()=>({getProvider:()=>provider});
  runInNewContext(script,{
    window,document:{getElementById:id=>elements[id]},
    location:{origin},Event:class Event {constructor(name){this.type=name}}
  },{timeout:1000});
  return {
    async click(){await elements[route].click()},
    observation(){return {...JSON.parse(elements.receipt.textContent),calls}}
  };
}

const cases = [
  ['A380 exact Base match', {}, 'PASS_TARGET_ADDRESS_RETURNED_NO_SIGNING_PROOF'],
  ['Base SDK wrong account', {address:'0x'+'57'.repeat(20)}, 'FAIL_DIFFERENT_WALLET_ADDRESS'],
  ['Current Coinbase provider wrong account', {route:'coinbase',address:'0x'+'57'.repeat(20)}, 'FAIL_DIFFERENT_WALLET_ADDRESS'],
  ['Historic direct owner only is not signer proof', {route:'coinbase',address:'0xe13c4abd8e4d3caf5a84238e047e1b7e8632d180'}, 'OWNER_ADDRESS_MATCH_ONLY_SIGNING_UNPROVEN'],
  ['Wrong website origin', {origin:'https://wrong.example'}, 'UNKNOWN_CONNECT_FAILED'],
  ['SDK not loaded', {baseSDK:false}, 'UNKNOWN_CONNECT_FAILED'],
  ['Non-Coinbase injected provider', {route:'coinbase',coinbase:false}, 'UNKNOWN_CONNECT_FAILED'],
  ['Consent for existing account', {consent:true}, 'PASS_TARGET_ADDRESS_RETURNED_NO_SIGNING_PROOF'],
  ['Wrong network', {chain:'0x1'}, 'FAIL_NOT_BASE_8453']
];
for(const [name,params,expected] of cases) {
  test(name, async () => {
    const x = scenario(params);
    await x.click();
    const result = x.observation();
    assert.equal(result.status,expected);
    assert.ok(result.calls.every(m=>['eth_accounts','eth_requestAccounts','eth_chainId'].includes(m)));
  });
}
test('CI-FIRST surface forbids sensitive and modifying methods',()=>{
  assert.doesNotMatch(HTML,/personal_sign|eth_signTypedData|eth_sendTransaction|eth_sendRawTransaction|wallet_sendCalls|wallet_switchEthereumChain|navigator\.credentials\.create|localStorage|sessionStorage|sendBeacon/);
  assert.match(HTML, /https:\/\/jsonwisdom\.github\.io/);
  assert.match(HTML, /sha384-Jcaa5XJIs34lC6Co7Ye\/mAuxCGLTEdUYQuIyl4UrwRduYb6mOmW7SUCOPX\/jdsKV/);
});
