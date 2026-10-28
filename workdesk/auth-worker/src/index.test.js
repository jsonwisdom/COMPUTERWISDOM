import test from 'node:test';
import assert from 'node:assert/strict';
import worker from './index.js';

function emptyDB() {
 return {prepare(sql) {
  if (!/^SELECT id,public_key,counter,transports FROM credentials$/.test(sql)) {
   throw new Error('Unexpected database query: ' + sql);
  }
  return {all: async () => ({results: []})};
 }};
}
const env = {AUTH_DB:emptyDB(),RP_ID:'jsonwisdom.com',EXPECTED_ORIGIN:'https://jsonwisdom.com'};
const call = (path, method='GET',headers={}) => worker.fetch(
 new Request('https://auth.jsonwisdom.com'+path,{method,headers}),env
);

test('unauthenticated private Workdesk is denied',async()=>{
 const response=await call('/private');
 assert.equal(response.status,403);
 assert.equal(response.headers.get('cache-control'),'no-store');
});
test('registration cannot start without bootstrap secret',async()=>{
 const response=await call('/register/options','POST',{'origin':'https://jsonwisdom.com'});
 assert.equal(response.status,403);
});
test('cross-origin authentication request denied',async()=>{
 const response=await call('/login/options','POST',{'origin':'https://example.com'});
 assert.equal(response.status,403);
});
test('missing Origin on authentication POST denied',async()=>{
 const response=await call('/login/options','POST');
 assert.equal(response.status,403);
});
test('login cannot start with zero enrolled credentials',async()=>{
 const response=await call('/login/options','POST',{'origin':'https://jsonwisdom.com'});
 assert.equal(response.status,503);
});
test('healthy response never implies authenticated',async()=>{
 const response=await call('/health');
 assert.equal(response.status,200);
 assert.deepEqual(await response.json(),{configured:true,authenticated:false});
});

test('wallet readiness cannot be fetched without Jason session',async()=>{
 const response=await call('/wallet/readiness');
 assert.equal(response.status,403);
});
test('read-only wallet endpoint rejects forged bearer authorization',async()=>{
 const response=await call('/wallet/readiness','GET',{authorization:'Bearer forged'});
 assert.equal(response.status,403);
});
test('public HTTP API does not offer wallet signing or payments',async()=>{
 for(const endpoint of ['/wallet/sign','/wallet/send','/x402/pay']){
  const response=await call(endpoint,'POST',{origin:'https://jsonwisdom.com'});
  assert.equal(response.status,404);
 }
});
