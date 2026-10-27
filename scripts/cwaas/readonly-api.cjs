'use strict';
// Loopback-only fixture viewer. Not a production service.
const http=require('node:http'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'../..');
const fixture=path.join(root,'fixtures/cwaas/readonly-report-v0.1.json');
const checksum=path.join(root,'fixtures/cwaas/readonly-report-v0.1.sha256');
function load(){
 const bytes=fs.readFileSync(fixture);
 const actual=crypto.createHash('sha256').update(bytes).digest('hex');
 if(actual!==fs.readFileSync(checksum,'utf8').trim())throw Error('digest mismatch');
 const report=JSON.parse(bytes.toString('utf8'));
 if(report.authority!==false||report.payment?.status!=='HOLD'||report.receipt?.payment_settlement!=='NONE'||report.reproducibility?.external_requests!==false)throw Error('policy mismatch');
 return {report,sha256:actual};
}
function handler(req,res){
 res.setHeader('Content-Type','application/json; charset=utf-8');
 res.setHeader('Cache-Control','no-store');
 const send=(status,payload)=>{res.statusCode=status;res.end(JSON.stringify(payload)+'\n')};
 if(req.method!=='GET'&&req.method!=='HEAD')return send(405,{status:'HOLD',reason:'read-only'});
 if(req.url!=='/v0/report'&&req.url!=='/health')return send(404,{status:'HOLD',reason:'not-found'});
 try{const x=load();const payload=req.url==='/health'?{status:'FIXTURE_ONLY',sha256:x.sha256,authority:false,payment:'HOLD'}:{status:'FIXTURE_ONLY',source:'CHECKED_IN_FIXTURE_NOT_LIVE_OBSERVATION',sha256:x.sha256,report:x.report};if(req.method==='HEAD'){res.statusCode=200;return res.end()}return send(200,payload)}catch(_){return send(503,{status:'HOLD',reason:'integrity-or-policy-error'})}
}
if(require.main===module){const port=Number(process.env.CWAAS_PORT||8788);http.createServer(handler).listen(port,'127.0.0.1',()=>console.log('CWaaS LOCAL FIXTURE: http://127.0.0.1:'+port+'/v0/report'));}
module.exports={handler,load};
