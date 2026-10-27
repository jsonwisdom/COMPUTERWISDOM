// CWaaS contract check. Node 20 built-ins only; no network, payment, or signing.
'use strict';
const fs=require('node:fs'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const dir='fixtures/cwaas/';
const fp=dir+'readonly-report-v0.1.json',sp=dir+'readonly-report-schema.json',hp=dir+'readonly-report-v0.1.sha256';
for(const f of [fp,sp,hp]) assert.ok(fs.existsSync(f),'MISSING: '+f);
const bytes=fs.readFileSync(fp), fixture=JSON.parse(bytes.toString('utf8')), schema=JSON.parse(fs.readFileSync(sp,'utf8'));
const expected=fs.readFileSync(hp,'utf8').trim();assert.match(expected,/^[a-f0-9]{64}$/,'bad digest shape');
assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),expected,'RAW-BYTES SHA256 mismatch');
const check=(x,s,path='$')=>{if(Object.hasOwn(s,'const'))assert.deepEqual(x,s.const,path);if(s.enum)assert.ok(s.enum.includes(x),path);if(s.type){assert.ok(s.type==='null'?x===null:s.type==='array'?Array.isArray(x):s.type==='object'?x!==null&&typeof x==='object'&&!Array.isArray(x):typeof x===s.type,path+' type');}if(s.pattern)assert.match(x,new RegExp(s.pattern),path);if(s.minLength!==undefined)assert.ok(x.length>=s.minLength,path);if(s.minItems!==undefined)assert.ok(x.length>=s.minItems,path);if(s.type==='object'){for(const k of s.required||[])assert.ok(Object.hasOwn(x,k),path+'.'+k+' missing');if(s.additionalProperties===false)for(const k of Object.keys(x))assert.ok(Object.hasOwn(s.properties,k),path+'.'+k+' extra');for(const [k,v]of Object.entries(s.properties||{}))if(Object.hasOwn(x,k))check(x[k],v,path+'.'+k);}if(s.type==='array')for(let i=0;i<x.length;i++)check(x[i],s.items,path+'['+i+']')};
check(fixture,schema);
assert.equal(fixture.authority,false);assert.equal(fixture.payment.status,'HOLD');assert.equal(fixture.receipt.payment_settlement,'NONE');assert.equal(fixture.reproducibility.external_requests,false);
const forbidden=/(?:PRIVATE.KEY|MNEMONIC|SEED.PHRASE|PAYMENT.SIGNATURE)/i;for(const s of [fs.readFileSync(fp,'utf8')])assert.ok(!forbidden.test(s),'credential/payment payload marker in fixture');
console.log('PASS fixture schema, explicit boundaries, raw bytes SHA-256 '+expected);
// Negative tests must fail closed, not merely validate the happy path.
for(const [label,modify] of [['authority',x=>x.authority=true],['settlement',x=>x.receipt.payment_settlement='LIVE'],['requests',x=>x.reproducibility.external_requests=true],['missing',x=>delete x.payment]]){const x=structuredClone(fixture);modify(x);assert.throws(()=>check(x,schema),label+' negative test failed');}console.log('PASS 4 negative schema tests');
