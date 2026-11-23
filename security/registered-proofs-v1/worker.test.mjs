import test from 'node:test';import assert from 'node:assert/strict';
import worker from './worker.mjs';
test('read-only GET proof listing no fake certification',async()=>{const r=await worker.fetch(new Request('https://proof.example/v1/proofs'));assert.equal(r.status,200);const j=await r.json();assert.equal(j.proofs.length,3);assert.ok(j.proofs.some(x=>x.ci_verdict==='UNKNOWN'));assert.equal(j.manifest.external_certification,false)});
test('specific hardware proof remains UNKNOWN',async()=>{const r=await worker.fetch(new Request('https://proof.example/v1/proofs/PC_TPM_INDEPENDENT_ATTEST_20261108'));assert.equal((await r.json()).record.ci_verdict,'UNKNOWN')});
test('POST cannot register or mutate',async()=>{const r=await worker.fetch(new Request('https://proof.example/v1/proofs',{method:'POST',body:'{}'}));assert.equal(r.status,405);assert.equal((await r.json()).authority_created,false)});
test('unknown proof not fabricated',async()=>{const r=await worker.fetch(new Request('https://proof.example/v1/proofs/MADEUP'));assert.equal(r.status,404)});
test('health is self-reported only',async()=>{const j=await (await worker.fetch(new Request('https://proof.example/v1/health'))).json();assert.equal(j.public_http_cryptographic_attestation,'UNKNOWN')});
