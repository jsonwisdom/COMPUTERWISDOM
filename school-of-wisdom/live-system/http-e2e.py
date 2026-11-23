"""Real HTTPS requests to the fixture Worker. Credentials loaded locally, never logged."""
import json,concurrent.futures,uuid,urllib.request,urllib.error,time
from pathlib import Path
R=Path(__file__).resolve().parent
BASE='https://jasons-game-fixture-e2e.jaywisdom44.workers.dev'
TOKEN=(R/'test-token.private').read_text().strip()
BUILD=json.loads((R/'build.json').read_text())
RUN='jg-'+uuid.uuid4().hex
checks=[];attempts=[]
def request(path,body=None,key=None,auth=True):
 import subprocess
 args=['curl','--silent','--show-error','--max-time','8','-w','\nJG_STATUS:%{http_code}','-H','Cache-Control: no-cache','-H','Content-Type: application/json']
 if auth:args+=['-H','Authorization: Bearer '+TOKEN]
 if key:args+=['-H','Idempotency-Key: '+key]
 data=None
 if body is not None:
  args+=['--data-binary','@-'];data=json.dumps(body,separators=(',',':'))
 args+=[BASE+path]
 r=subprocess.run(args,input=data,capture_output=True,text=True,timeout=15)
 if '\nJG_STATUS:' not in r.stdout:raise RuntimeError('HTTP transport failed: '+r.stderr[:120])
 raw,status=r.stdout.rsplit('\nJG_STATUS:',1)
 return int(status),json.loads(raw)

def check(category,name,fn):
 try:
  evidence=fn();checks.append({'category':category,'name':name,'status':'PASS','actually_ran':True,'evidence':evidence})
 except Exception as e:checks.append({'category':category,'name':name,'status':'FAIL','actually_ran':True,'error':str(e)})
 print(name+': '+checks[-1]['status'],flush=True)
def eq(a,b):
 assert a==b,(a,b)
def payload(ch,ans,version=1,bundle=None):return {'challenge_id':ch,'version':version,'bundle_digest':bundle or BUILD['bundle_digest'],'answer':ans}
def submit(ch,ans,key=None):
 status,r=request('/attempt',payload(ch,ans),key or RUN+'-'+uuid.uuid4().hex)
 eq(status,201);attempts.append(r);return r
def health():
 s,b=request('/health',auth=False);eq(s,200);eq(b['build_sha'],BUILD['worker_sha256']);eq(b['bundle_digest'],BUILD['bundle_digest']);return b
check('integrity_checks','Live build and bundle identities',health)
def catalog():
 s,b=request('/catalog');eq(s,200);eq(len(b['catalog']),3);eq(len(b['challenges']),3)
 eq([x['sku'] for x in b['catalog']],[x['sku'] for x in b['challenges']]);eq(b['challenges'][0]['fixture']['synthetic'],True)
 raw=json.dumps(b);assert 'rubric' not in raw and '"private"' not in raw and 'private_key' not in raw and 'answers' not in raw
 return {'linked_fixture_challenges':3,'synthetic':True,'private_fields_excluded':True}
check('content_validation','Live fixture catalog linkage and public privacy projection',catalog)
check('http_integration','Missing credentials rejected',lambda:eq(request('/catalog',auth=False)[0],401))
def scoring():
 cases=[('CH-001',10,1),('CH-001',9,0),('CH-002',{'a':'DOCUMENTED','b':'ASSUMPTION','c':'SATIRE','d':'UNVERIFIED'},4),('CH-003','3/4',1),('CH-003','6/8',1),('CH-003','2/3',0)]
 for label in ['DOCUMENTED','ASSUMPTION','SATIRE','UNVERIFIED']:
  a={'a':'DOCUMENTED','b':'ASSUMPTION','c':'SATIRE','d':'UNVERIFIED'};k=next(k for k,v in a.items() if v==label);a[k]=next(v for v in a.values() if v!=label);cases.append(('CH-002',a,3))
 huge=10**100+1;cases += [('CH-003',f'{3*huge}/{4*huge}',1),('CH-003',f'{3*huge+1}/{4*huge}',0)]
 def one(case):
  ch,ans,expected=case;eq(submit(ch,ans)['attempt']['result']['earned'],expected)
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:list(pool.map(one,cases))
 return {'scored_receipts':len(attempts),'exact_large_integer_cases':2,'four_classifications_exercised':True}
check('scoring_tests','All fixture scorers and exact integer edge cases over HTTPS',scoring)
def invalid():
 values=['3/0','-3/4','3/-4','0.75','3.0/4','3/4/5',' 3/4','3/4\n','NaN','Infinity','',None,True,0.75,{},'３/４','9'*129+'/4']
 def reject(v):eq(request('/attempt',payload('CH-003',v),RUN+'-'+uuid.uuid4().hex)[0],400)
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as p:list(p.map(reject,values))
 return {'invalid_fraction_inputs_rejected':len(values)}
check('scoring_tests','Malformed fraction requests rejected over HTTPS',invalid)
def tamper():
 eq(request('/attempt',payload('CH-003','3/4',bundle='0'*64),RUN+'-wrong-bundle')[0],409)
 eq(request('/attempt',payload('CH-003','3/4',version=2),RUN+'-wrong-version')[0],400)
 b=payload('CH-003','3/4');b['result']={'earned':1};eq(request('/attempt',b,RUN+'-forged-score')[0],400)
 return {'bundle_mismatch':409,'unknown_version':400,'forged_score':400}
check('integrity_checks','Wrong bundle/version and client score injection rejected',tamper)
def duplicate():
 key=RUN+'-duplicates';body=payload('CH-003','3/4')
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as p:results=list(p.map(lambda _:request('/attempt',body,key),range(8)))
 eq(sorted(s for s,_ in results),[200]*7+[201]);first=results[0][1];assert all(r==first for _,r in results)
 eq(request('/attempt',body,key),(200,first));attempts.append(first)
 return {'key':key,'statuses':[s for s,_ in results],'receipt_id':first['receipt_id'],'retry_preserved':True}
check('persistence_integration_tests','Eight simultaneous HTTP submissions preserve one D1 receipt',duplicate)
def conflicts():
 key=RUN+'-conflicts';answers=['3/4','2/3']*4
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as p:results=list(p.map(lambda a:request('/attempt',payload('CH-003',a),key),answers))
 eq(sum(s==201 for s,_ in results),1);eq(sum(s==409 for s,_ in results),4);winner=next(r for s,r in results if s==201)
 assert all(r==winner for s,r in results if s in (200,201));eq(request('/attempt',payload('CH-003',winner['attempt']['input']),key),(200,winner));attempts.append(winner)
 return {'key':key,'statuses':[s for s,_ in results],'receipt_id':winner['receipt_id'],'original_preserved':True}
check('persistence_integration_tests','Concurrent conflicting reuse returns HTTP 409',conflicts)
def replay():
 assert len(attempts)>=14, 'Insufficient persisted receipts for replay evidence'
 def one(r):
  s,b=request('/replay',{'receipt_id':r['receipt_id']});eq(s,200);eq(b['reproduced'],True);eq(b['result'],r['attempt']['result'])
 with concurrent.futures.ThreadPoolExecutor(max_workers=14) as pool:list(pool.map(one,attempts))
 return {'persisted_receipts_replayed':len(attempts)}
check('reproducibility_checks','Persisted D1 attempts recomputed via live HTTP',replay)
report={'run_id':RUN,'timestamp_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'url':BASE,'scope':'TEST_FIXTURES_ONLY','http_executed':True,'d1_worker_binding_executed':len(attempts)>0,'approved_content_validation':'PENDING','commerce':'HOLD','checks':checks,'receipt_count':len(attempts),'summary':{'passed':sum(c['status']=='PASS' for c in checks),'failed':sum(c['status']=='FAIL' for c in checks)}}
(R/'http-e2e-report.json').write_text(json.dumps(report,indent=2)+'\n');(R/'http-receipts.json').write_text(json.dumps(attempts,indent=2)+'\n');print(json.dumps(report['summary']))
raise SystemExit(bool(report['summary']['failed']))
