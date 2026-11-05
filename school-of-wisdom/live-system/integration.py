import json,subprocess,concurrent.futures,time
from pathlib import Path
R=Path(__file__).resolve().parent
O='https://wisdom-live-observer.jaywisdom44.workers.dev';C='https://wisdom-catalog-curator.jaywisdom44.workers.dev'
checks=[]
def req(url,body=None,token=None,raw=False):
 args=['curl','-sS','--max-time','20','-w','\nW_STATUS:%{http_code}','-H','Cache-Control: no-cache']
 if token:args+=['-H','Authorization: Bearer '+token]
 if body is not None:args+=['-H','Content-Type: application/json','--data-binary','@-']
 r=subprocess.run(args+[url],input=json.dumps(body) if body is not None else None,capture_output=True,text=True,timeout=30)
 text,status=r.stdout.rsplit('\nW_STATUS:',1)
 return int(status),text if raw else json.loads(text)
def eq(a,b):assert a==b,(a,b)
def test(name,fn):
 try:detail=fn();checks.append({'name':name,'status':'PASS','executed':True,'detail':detail})
 except Exception as e:checks.append({'name':name,'status':'FAIL','executed':True,'error':str(e)})
 print(name+': '+checks[-1]['status'],flush=True)
def views():
 def one(view):
  s,b=req(C+'/inventory?view='+view);eq(s,200);eq(b['count'],500);eq(len({x['sku'] for x in b['records']}),500)
  return {'view':view,'records':b['count']}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as p:return list(p.map(one,['learning','readiness','commerce','provenance']))
test('All four inventory lenses preserve 500 unique SKU identities',views)
def proposal():
 s,b=req(C+'/health');eq(s,200);source=b['source_hashes']['001-050']
 body={'sku':'JASON-002','expected_source_sha256':source,'basis':'SYNTHETIC INTEGRATION TEST ONLY; not approved; no store mutation','changes':{'functions':['classify_supplied_claim']}}
 eq(req(C+'/proposals',body)[0],401)
 bad=dict(body);bad['expected_source_sha256']='0'*64;eq(req(C+'/proposals',bad,(R/'curator-token.private').read_text().strip())[0],409)
 s,r=req(C+'/proposals',body,(R/'curator-token.private').read_text().strip());eq(s,201);eq(r['receipt']['applied'],False);eq(r['receipt']['status'],'PROPOSED');(R/'proposal-test-receipt.json').write_text(json.dumps(r,indent=2)+'\n')
 eq(req(C+'/inventory?view=learning&sku=JASON-002')[1]['records'][0]['functions'],[])
 return {'proposal_id':r['receipt']['id'],'persisted_proposal':True,'applied':False,'catalog_unchanged':True}
test('Authenticated stale-safe metadata proposal with receipt; no application',proposal)
def observe():
 eq(req(O+'/audit',{})[0],401)
 s,b=req(O+'/audit',{},(R/'audit-token.private').read_text().strip());eq(s,200);assert len(b['checks'])>=8
 (R/'manual-audit-receipt.json').write_text(json.dumps(b,indent=2)+'\n')
 return {'receipt_id':b['receipt_id'],'checks':len(b['checks']),'statuses':{c['id']:c['status'] for c in b['checks']}}
test('Live observer executes bounded estate audit and records scoped results',observe)
def board():
 s,b=req(O+'/leaderboard');eq(s,200);eq(b['freshness'],'FRESH');eq(b['learner_rankings'],False);assert any(c['id']=='x402-payment-receipts' and c['status']=='HOLD' for c in b['checks']);assert any(c['id']=='authored-challenge-content' and c['status']=='HOLD' for c in b['checks'])
 (R/'live-leaderboard.json').write_text(json.dumps(b,indent=2)+'\n');return {'freshness':b['freshness'],'holds_visible':True,'receipt_id':b['receipt_id']}
test('Live system leaderboard preserves missing-evidence HOLDs',board)
def pages():
 s,html=req(O+'/',raw=True);eq(s,200);assert 'School of Wisdom' in html
 s,html=req(O+'/arena',raw=True);eq(s,200);assert "fetch('/inventory?view=learning')" in html;assert 'local synthetic-role game transcript' in html
 return {'dashboard':200,'arena':200,'real_catalog_fetch':True,'certified_learner_rankings':False}
test('Dashboard and free arena HTTP surfaces are live',pages)
report={'timestamp_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'checks':checks,'summary':{'passed':sum(x['status']=='PASS' for x in checks),'failed':sum(x['status']=='FAIL' for x in checks)}}
(R/'integration-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['summary']));raise SystemExit(bool(report['summary']['failed']))
