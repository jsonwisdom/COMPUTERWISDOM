import json,subprocess,concurrent.futures
from pathlib import Path
r=Path(__file__).resolve().parent
a=json.loads((r/'historical-receipts-input.json').read_text());token=(r/'test-token.private').read_text().strip()
def one(receipt):
 args=['curl','-sS','--max-time','15','-H','Authorization: Bearer '+token,'-H','Content-Type: application/json','--data-binary','@-','https://jasons-game-fixture-e2e.jaywisdom44.workers.dev/replay']
 result=subprocess.run(args,input=json.dumps({'receipt_id':receipt['receipt_id']}),capture_output=True,text=True,timeout=25);b=json.loads(result.stdout);assert b['reproduced'] and b['result']==receipt['attempt']['result'];return {'receipt_id':receipt['receipt_id'],'reproduced':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=14) as p:results=list(p.map(one,a))
(r/'historical-live-replay.json').write_text(json.dumps({'scope':'Existing pre-upgrade real D1 receipts via live HTTP','results':results,'passed':len(results)},indent=2)+'\n');print('Historical receipts replayed:',len(results))
