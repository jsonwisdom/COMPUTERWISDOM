import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';
import { webcrypto } from 'node:crypto';
import { Wallet, verifyTypedData, TypedDataEncoder, Interface } from 'ethers';

const JS=readFileSync(new URL('./jaywisdom.js',import.meta.url),'utf8');
const HTML=readFileSync(new URL('./jaywisdom.html',import.meta.url),'utf8');
const INDEX=JSON.parse(readFileSync(new URL('./recovery-index.json',import.meta.url),'utf8'));
const SYNTHETIC=new Wallet('0x'+'77'.repeat(32)); // public unfunded test-only key
const WRONG=new Wallet('0x'+'88'.repeat(32));
const REAL='0xa380552a27b0a5a2874ea7aa52cac09f542002e8';
const ERC1271=new Interface(['function isValidSignature(bytes32,bytes) view returns (bytes4)']);
const EXPECTED_DECL="const EXPECTED='"+REAL+"';";
function harness({owner=SYNTHETIC,wrong=false,smart=false,contractValid=true,abort=false,correctOrigin=true,initialChain='0x1'}={}){
  const ids=['connect','sign','notice','account','preview','previewWrap',
    'proofHero','proofAddress','proofMethod','proofDigest','index','indexList','indexStatus'];
  const els=Object.fromEntries(ids.map(id=>{
    const el={id,hidden:['sign','previewWrap','proofHero','index'].includes(id),
      disabled:id==='sign',textContent:'',className:'',style:{},
      listeners:{},children:[], addEventListener(name,fn){this.listeners[name]=fn},
      replaceChildren(){this.children=[]},appendChild(x){this.children.push(x)},
      append(...args){this.children.push(...args)},scrollIntoView(){this.scrolled=true}};
    return [id,el];
  }));
  const emitted={},calls=[];let address=owner.address,chain=initialChain;
  const source=JS.replace(EXPECTED_DECL,"const EXPECTED='"+owner.address.toLowerCase()+"';");
  assert.notEqual(source,JS,'Expected address substitution must occur only in CI harness');
  const provider={
    isCoinbaseWallet:true,
    on(name,fn){emitted[name]=fn;},
    removeListener(name){delete emitted[name];},
    async request({method,params}){
      calls.push({method,params});
      switch(method){
        case 'eth_requestAccounts':return [address];
        case 'eth_accounts':return [address];
        case 'eth_chainId':return chain;
        case 'wallet_switchEthereumChain':
          assert.equal(params[0].chainId,'0x2105');
          chain='0x2105';emitted.chainChanged?.(chain);return null;
        case 'eth_signTypedData_v4':{
          const td=JSON.parse(params[1]);
          assert.equal(td.domain.chainId,8453);
          assert.equal(td.message.origin,'https://wallet.jsonwisdom.com');
          assert.equal(td.message.basename,'jaywisdom.base.eth');
          assert.equal(td.domain.salt,'0xad2e9ab938f28c9491eca2dac2aa2e30322e9d71f71d8ba98f7de67cd2f3c0da');
          assert.equal(td.message.expiresAt-td.message.issuedAt,300);
          if(abort){address=WRONG.address;emitted.accountsChanged?.([address]);}
          return (wrong?WRONG:owner).signTypedData(td.domain,
            {JayWisdomControl:td.types.JayWisdomControl},td.message);
        }
        case 'eth_getCode':return smart?'0x60016000':'0x';
        case 'eth_call':{
          const decoded=ERC1271.decodeFunctionData('isValidSignature',params[0].data);
          assert.match(decoded[0],/^0x[0-9a-f]{64}$/);
          return ERC1271.encodeFunctionResult('isValidSignature',
            [contractValid?'0x1626ba7e':'0xffffffff']);
        }
        default:throw Error('Unexpected wallet operation '+method);
      }
    }
  };
  const window={ethereum:provider,ethers:{verifyTypedData,TypedDataEncoder,Interface},
    addEventListener(){},dispatchEvent(){}};
  const document={getElementById:id=>els[id],createElement(tag){
    return {tag,textContent:'',className:'',href:'',target:'',rel:'',style:{},
      children:[],append(...args){this.children.push(...args)}};
  }};
  const manifest={...INDEX,basename_controller:owner.address.toLowerCase()};
  const fetch=async()=>({ok:true,json:async()=>manifest});
  class Event{constructor(type){this.type=type}}
  runInNewContext(source,{window,document,Event,crypto:webcrypto,fetch,
    location:{origin:correctOrigin?'https://wallet.jsonwisdom.com':'https://phishing.invalid'},
    Date,BigInt,Uint8Array,Array,Buffer,console},{timeout:3000});
  return {els,calls,connect:()=>els.connect.listeners.click(),
    sign:()=>els.sign.listeners.click(),changeAccount(a){address=a;emitted.accountsChanged?.([a])},
    changeChain(c){chain=c;emitted.chainChanged?.(c)}};
}
test('M1 iPhone proof-first page is mobile-friendly and never contains secret entry or send controls',()=>{
  assert.match(HTML,/name="viewport"/);
  assert.match(HTML,/id="proofHero"/);
  assert.match(HTML,/id="index"/);
  assert.match(HTML,/src="\/jaywisdom.js"/);
  assert.doesNotMatch(JS,/eth_sendTransaction|personal_sign|wallet_sendCalls|eth_signTransaction|localStorage|sessionStorage/);
  assert.doesNotMatch(HTML,/<input[^>]*(seed|private|password|mnemonic)/i);
});
test('M2 connecting requires expected account, Base 8453 and one separate explicit signing click',async()=>{
  const h=harness();
  assert.equal(h.calls.filter(c=>c.method==='eth_signTypedData_v4').length,0);
  await h.connect();
  assert.equal(h.els.sign.disabled,false);
  assert.equal(h.els.sign.hidden,false);
  assert.equal(h.els.proofHero.hidden,true);
  assert.equal(h.calls.filter(c=>c.method==='wallet_switchEthereumChain').length,1);
  assert.equal(h.calls.filter(c=>c.method==='eth_signTypedData_v4').length,0);
  const td=JSON.parse(h.els.preview.textContent);
  assert.equal(td.message.account.toLowerCase(),SYNTHETIC.address.toLowerCase());
  assert.equal(td.domain.chainId,8453);
  assert.equal(td.message.expiresAt-td.message.issuedAt,300);
});
test('M3 real synthetic EOA EIP712 signature verifies and public provenance index cascades under proof',async()=>{
  const h=harness();await h.connect();await h.sign();
  assert.equal(h.els.proofHero.hidden,false);
  assert.equal(h.els.index.hidden,false);
  assert.equal(h.els.proofMethod.textContent,'EIP-712 / EOA RECOVERY');
  assert.match(h.els.proofDigest.textContent,/^0x[0-9a-f]{64}$/);
  assert.equal(h.els.indexList.children.length,INDEX.layers.length);
  assert.match(h.els.notice.textContent,/Locally verified/);
  assert.ok(!h.calls.some(x=>/sendTransaction|wallet_sendCalls|personal_sign/.test(x.method)));
});
test('M4 different private key returns rejection, with no hero or index',async()=>{
  const h=harness({wrong:true});await h.connect();await h.sign();
  assert.equal(h.els.proofHero.hidden,true);
  assert.equal(h.els.index.hidden,true);
  assert.match(h.els.notice.textContent,/does not recover/);
});
test('M5 deployed Base smart account accepts authentic ERC1271 magic and rejects alternate return',async()=>{
  const h=harness({smart:true});await h.connect();await h.sign();
  assert.equal(h.els.proofHero.hidden,false);
  assert.equal(h.els.proofMethod.textContent,'ERC-1271 / BASE ETH_CALL');
  assert.equal(h.calls.filter(x=>x.method==='eth_call').length,1);
  const bad=harness({smart:true,contractValid:false});
  await bad.connect();await bad.sign();
  assert.equal(bad.els.proofHero.hidden,true);
  assert.match(bad.els.notice.textContent,/Smart wallet rejected/);
});
test('M6 wrong wallet, wrong origin and account change during signing all fail closed',async()=>{
  const h=harness();h.changeAccount(WRONG.address);await h.connect();
  assert.equal(h.els.sign.hidden,true);
  assert.match(h.els.notice.textContent,/Different wallet selected/);
  assert.equal(h.calls.filter(x=>x.method==='eth_signTypedData_v4').length,0);
  const ph=harness({correctOrigin:false});await ph.connect();
  assert.equal(ph.els.sign.hidden,true);
  assert.match(ph.els.notice.textContent,/Wrong website origin/);
  const raced=harness({abort:true});await raced.connect();await raced.sign();
  assert.equal(raced.els.proofHero.hidden,true);
  assert.equal(raced.els.index.hidden,true);
});
test('M7 public JSON index distinguishes historical CI, claims, unsigned binding and payment HOLD',()=>{
  assert.equal(INDEX.schema,'COINBASEKID_PUBLIC_RECOVERY_INDEX_V1');
  assert.equal(INDEX.basename_controller,REAL);
  assert.equal(INDEX.reputation_status,'NOT_CERTIFIED');
  assert.equal(INDEX.append_only.cryptographically_enforced,false);
  assert.ok(INDEX.layers.some(x=>x.status==='USER_REPORTED_SUCCESS'));
  assert.ok(INDEX.layers.some(x=>x.status==='CI_PASS'));
  assert.ok(INDEX.layers.some(x=>x.status==='PENDING'));
  assert.ok(INDEX.layers.some(x=>x.status==='HOLD'));
  assert.ok(INDEX.layers.every(x=>/^https:\/\//.test(x.url)));
});
