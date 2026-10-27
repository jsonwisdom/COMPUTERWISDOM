'use strict';
const assert=require('node:assert/strict'),http=require('node:http');
const {handler,load}=require('./readonly-api.cjs');
async function main(){const x=load();const server=http.createServer(handler);await new Promise(ok=>server.listen(0,'127.0.0.1',ok));const port=server.address().port;
async function request(url,method='GET'){return new Promise((resolve,reject)=>{const req=http.request({hostname:'127.0.0.1',port,path:url,method},res=>{let s='';res.on('data',d=>s+=d);res.on('end',()=>resolve({status:res.statusCode,body:s?JSON.parse(s):null}))});req.on('error',reject);req.end()})}
try{const r=await request('/v0/report');assert.equal(r.status,200);assert.equal(r.body.status,'FIXTURE_ONLY');assert.equal(r.body.report.payment.status,'HOLD');assert.equal(r.body.sha256,x.sha256);assert.equal((await request('/health')).status,200);assert.equal((await request('/v0/report','POST')).status,405);assert.equal((await request('/missing')).status,404);console.log('PASS: fixture API, hash, health, 405, 404')}finally{await new Promise(ok=>server.close(ok))}}
main().catch(e=>{console.error(e);process.exitCode=1});
