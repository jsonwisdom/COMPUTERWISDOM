"""Offline staging validator. Trust root must be pinned independently by operator."""
import argparse, hashlib, json, re
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
SCHEMA=Path(__file__).parent/'schemas/finding.schema.json'
class Invalid(ValueError): pass

def require(ok, msg):
    if not ok: raise Invalid(msg)
def digest(b): return hashlib.sha256(b).hexdigest()
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')
def read(p):
    def pairs(items):
        d={}
        for k,v in items:
            require(k not in d,'duplicate JSON key'); d[k]=v
        return d
    def bad(x): raise Invalid('floating point or nonfinite JSON number')
    return json.loads(p.read_text(encoding='utf-8'),object_pairs_hook=pairs,parse_float=bad,parse_constant=bad)
def valid_hash(h):
    return isinstance(h,str) and bool(re.fullmatch('[0-9a-f]{64}',h)) and not any(h==h[:n]*(64//n) for n in (1,2,4,8,16,32))
def artifact(root, ref, expected):
    require(valid_hash(expected),'invalid or placeholder digest')
    p=(root/ref).resolve(); require(p.is_relative_to(root.resolve()) and p.is_file(),'missing or unsafe artifact')
    require(digest(p.read_bytes())==expected,'hash mismatch')
    return p

def verify(root, anchor_sha):
    root=Path(root); schema=read(SCHEMA); Draft202012Validator.check_schema(schema)
    validator=Draft202012Validator(schema,format_checker=FormatChecker())
    anchor=read(artifact(root,'anchor.json',anchor_sha))
    findings=read(root/'findings.json'); receipts=read(artifact(root,'receipts.json',anchor['receipts_sha256']))
    require(isinstance(findings,list) and isinstance(receipts,dict),'invalid collection')
    streams={}
    for name in ('corrections','remedies'):
        old=read(artifact(root, f'baseline/{name}.json',anchor[name+'_sha256'])); new=read(root/f'{name}.json')
        require(isinstance(old,list) and isinstance(new,list) and new[:len(old)]==old,'history changed: '+name)
        ids=set()
        for e in new:
            require(isinstance(e,dict) and isinstance(e.get('event_id'),str) and e['event_id'] not in ids and isinstance(e.get('stream_id'),str),'invalid history event'); ids.add(e['event_id'])
        streams[name]=new
    seen=set(); results=[]
    for f in findings:
        validator.validate(f); fid=f['finding_id']; require(fid not in seen,'duplicate finding'); seen.add(fid)
        require(f['publication']=='HOLD','production authorization blocked')
        require(f['primary_lane_id'] not in f['cross_lane_ids'],'self lane')
        require(f['source_commit']==anchor['source_commit'],'unpinned source commit')
        for h in (f['previous_revision_sha256'],f['source']['sha256']):
            if h is not None: require(valid_hash(h),'placeholder digest')
        if f['revision']==1: require(f['previous_revision_sha256'] is None,'unexpected previous revision')
        else: raise Invalid('revision chain not implemented; fail closed')
        if f['source']['sha256'] is not None:
            artifact(root,'evidence/'+f['source']['sha256'],f['source']['sha256'])
        # Receipts bind exact claim, metrics, provenance and classification, not just an ID.
        subject=digest(canonical({k:f[k] for k in ('finding_id','revision','claim','source','metrics','source_commit','primary_lane_id','cross_lane_ids','jurisdiction')}))
        def receipt(rid,kind,verdict):
            require(rid in receipts,'missing receipt: '+kind); r=receipts[rid]
            require(r['kind']==kind and r['verdict']==verdict and r['subject_sha256']==subject and r['source_commit']==f['source_commit'],'receipt binding mismatch: '+kind)
            artifact(root,r['artifact'],r['sha256']); return r
        for kind, layer in f['verification'].items():
            if layer['status'] in ('PASS','FAIL'): receipt(layer['receipt_id'],kind,layer['status'])
        if f['verification_status']=='VERIFIED':
            receipt(f['replay_id'],'replay','PASS'); receipt(f['ci_receipt_id'],'ci','PASS')
        require(not any(x['status']=='FAIL' for x in f['verification'].values()) or f['verification_status']=='FAILED','failed layer must surface')
        results.append({'finding_id':fid,'status':f['verification_status'],'accountability':f['verification']['accountability']['status'],'publication':'HOLD'})
    for name, events in streams.items():
        allowed={f['correction_stream_id' if name=='corrections' else 'remedy_stream_id'] for f in findings}
        require(all(e['stream_id'] in allowed for e in events),'unresolved stream')
    return results
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('directory'); p.add_argument('--anchor-sha256',required=True); a=p.parse_args()
    try: print(json.dumps(verify(a.directory,a.anchor_sha256),indent=2))
    except Exception as e: p.exit(1,'FAIL: '+str(e)+'\n')
