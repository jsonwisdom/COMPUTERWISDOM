#!/usr/bin/env python3
"""AuditNow: disclosure first, no network, no public release."""
import argparse, hashlib, json, pathlib, re
TESTS=('existence','provenance','integrity','content_match','corroboration','attribution','legal_significance','conclusion_fit')
LEVEL={'FAIL':0,'HOLD':1,'PASS':2}
FIELDS=('purpose','scope','known_limits','privacy','identity_boundary','not_claimed','release_permission')
def digest(v):
 return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def reduce_claim(c):
 required,states=c.get('mandatory_tests'),c.get('tests',{})
 if not isinstance(required,list) or not required or len(required)!=len(set(required)) or not isinstance(states,dict) or set(required)-set(TESTS) or set(states)-set(TESTS):
  return 'HOLD',['Invalid or absent eight-test profile']
 checks,flags=[],[]
 for name in required:
  state=states.get(name,'HOLD')
  if state not in LEVEL:
   state='HOLD';flags.append('Invalid/missing state for '+name)
  if name=='corroboration' and state=='PASS':
   distinct={s.get('underlying_record_id') for s in c.get('sources',[]) if isinstance(s,dict) and s.get('independent') is True and s.get('inspection')=='SCOPED_REVIEWED' and s.get('underlying_record_id')}
   if len(distinct)<2:
    state='HOLD';flags.append('Independent source groups are insufficient')
  checks.append(LEVEL[state])
 return ('FAIL' if min(checks)==0 else 'HOLD' if min(checks)==1 else 'PASS'),flags
def evaluate(case):
 errors=[]
 if case.get('schema')!='AUDITNOW_DISCLOSURE_V0_1' or not re.fullmatch('[A-Za-z0-9_-]{3,80}',str(case.get('case_id',''))):
  errors.append('Invalid schema/case id')
 d=case.get('disclosure')
 if not isinstance(d,dict):d={};errors.append('Disclosure absent')
 for field in FIELDS:
  if not d.get(field):errors.append('Disclosure missing: '+field)
 if d.get('privacy')!='PUBLIC_SAFE_METADATA_ONLY' or d.get('release_permission')!='HUMAN_REVIEW_REQUIRED':
  errors.append('Privacy/release gate not valid')
 if case.get('canon') is not False or case.get('authority_created') is not False:
  errors.append('Canon/authority gate invalid')
 claims=case.get('claims',[])
 if not isinstance(claims,list) or not claims:
  claims=[];errors.append('Claims absent')
 rows=[];ids=set()
 for c in claims:
  if not isinstance(c,dict):errors.append('Invalid claim');continue
  cid=c.get('claim_id','')
  if not isinstance(cid,str) or not re.fullmatch('[A-Za-z0-9_-]{3,80}',cid) or cid in ids:
   errors.append('Invalid/repeated claim id');continue
  ids.add(cid)
  state,flags=reduce_claim(c)
  if not c.get('proposition') or not c.get('sources'):
   state='HOLD';flags.append('Missing claim or source locator')
  records={str(s.get('underlying_record_id')) for s in c.get('sources',[]) if isinstance(s,dict) and s.get('underlying_record_id')}
  rows.append({'claim_id':cid,'declared_reducer':state,'underlying_record_count':len(records),'flags':flags,'source_content_verified_by_automation':False})
 status='BLOCKED' if errors else ('HOLD' if any(r['declared_reducer']!='PASS' for r in rows) else 'REVIEW_REQUIRED')
 return {'schema':'AUDITNOW_RESULT_V0_1','case_id':case.get('case_id'),'disclosure':d,'disclosure_first':True,'preflight_errors':errors,'case_state':status,'claims':rows,'external_sources_fetched':False,'historical_truth_established':False,'human_review_required':True,'public_release_authorized':False,'bot_dispatched':False,'joy_candidate':'REVIEW_ONLY' if status=='REVIEW_REQUIRED' else 'HOLD','joy_published':False,'triggerdeck_canon':False,'authority_created':False,'canon':False,'no_fake_green':True}
def render(r):
 lines=['# Disclosure first — '+str(r['case_id']),'','**PUBLIC-SAFE METADATA / NO PUBLICATION AUTHORIZED**','','## Disclosure, before evidence reduction','']
 for f in FIELDS:lines.append('- **'+f+'**: '+str(r['disclosure'].get(f,'MISSING')))
 lines+=['','## Scoped reducer results','', '| Claim | Declared reducer | Underlying records |','|---|---|---|']
 for c in r['claims']:lines.append('| '+c['claim_id']+' | '+c['declared_reducer']+' | '+str(c['underlying_record_count'])+' |')
 lines+=['','Case: '+r['case_state'],'','No sources fetched; source labels and states are unverified assertions until independently replayed.','JOY candidate: '+r['joy_candidate']+' (not published).','Card render: DRAFT only.','Human release and privacy checks are separate.','', 'Digest (canonical JSON): '+digest(r),'']
 return '\n'.join(lines)
def main():
 p=argparse.ArgumentParser();p.add_argument('--cases-dir',default='auditnow/cases');p.add_argument('--out',required=True);a=p.parse_args()
 output=pathlib.Path(a.out);output.mkdir(parents=True,exist_ok=True)
 files=sorted(pathlib.Path(a.cases_dir).glob('*.json'))
 if not files:raise SystemExit('No cases: HOLD')
 cases=[]
 for path in files:
  r=evaluate(json.loads(path.read_text(encoding='utf-8')))
  (output/(path.stem+'.json')).write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
  (output/(path.stem+'.md')).write_text(render(r),encoding='utf-8')
  cases.append({'case_id':r['case_id'],'state':r['case_state'],'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'result_sha256':digest(r)})
 (output/'manifest.json').write_text(json.dumps({'cases':cases,'release_authorized':False,'canonical_receipt_created':False,'joy_published':False},indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'case_count':len(cases),'states':[c['state'] for c in cases],'released':False}))
if __name__=='__main__':main()
