import json,subprocess,concurrent.futures
from pathlib import Path
r=Path(__file__).resolve().parent;receipts=json.loads((r/'http-receipts.json').read_text());token=(r/'test-token.private').read_text().strip()
def one(receipt):
 failures=[]
 for attempt in range(1,4):
  result=subprocess.run(['curl','-sS','--max-time','20','-w','\nR_STATUS:%{http_code}','-H','Authorization: Bearer '+token,'-H','Content-Type: application/json','--data-binary','@-','https://jasons-game-fixture-e2e.jaywisdom44.workers.dev/replay'],input=json.dumps({'receipt_id':receipt['receipt_id']}),capture_output=True,text=True,timeout=30)
  raw,status=result.stdout.rsplit('\nR_STATUS:',1)
  try:b=json.loads(raw)
  except json.JSONDecodeError:failures.append({'attempt':attempt,'status':status,'response_bytes':len(raw)});continue
  assert int(status)==200 and b['reproduced'] and b['result']==receipt['attempt']['result'],b
  return {'receipt_id':receipt['receipt_id'],'reproduced':True,'request_attempts':attempt,'transport_failures':failures}
 raise AssertionError('Replay transport failed after three bounded requests')
assert len(receipts)==14
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(one,receipts))
report={'scope':'Live read-only replay recheck after transient empty response; no new attempts written','passed':len(results),'failed':0,'results':results};(r/'replay-recheck.json').write_text(json.dumps(report,indent=2)+'\n')
base=json.loads((r/'http-e2e-final-transport-failure.json').read_text());checks=base['checks'];checks[-1]={'category':'reproducibility_checks','name':'Persisted D1 attempts recomputed via live HTTP','status':'PASS','actually_ran':True,'evidence':{'persisted_receipts_replayed':len(results),'recheck_file':'replay-recheck.json','prior_transport_failure_preserved':'http-e2e-final-transport-failure.json'}}
base['checks']=checks;base['summary']={'passed':sum(c['status']=='PASS' for c in checks),'failed':sum(c['status']=='FAIL' for c in checks)};base['execution_note']='Eight HTTP groups passed in the final suite; replay passed on a separate bounded read-only recheck. Initial failed batch retained.';(r/'final-validation-report.json').write_text(json.dumps(base,indent=2)+'\n');print(json.dumps(base['summary']))
