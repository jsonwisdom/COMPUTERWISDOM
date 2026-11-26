import copy, json, tempfile, unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from verify import verify, digest, canonical
class Cases(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup); self.root=Path(self.tmp.name); (self.root/'baseline').mkdir(); (self.root/'evidence').mkdir()
        self.f=dict(schema_version='1.0',finding_id='test',revision=1,previous_revision_sha256=None,claim='Synthetic test only',primary_lane_id=1,cross_lane_ids=[2],jurisdiction={'scope':'FEDERAL','code':'US'},source={'uri':'https://example.org','acquired_at':None,'sha256':None},metrics=[],replay_id=None,verification_status='HOLD',verification={k:{'status':'UNKNOWN','receipt_id':None} for k in ('integrity','mathematics','authenticity','accountability')},correction_stream_id='c',remedy_stream_id='r',source_commit='a1'*20,ci_receipt_id=None,publication='HOLD')
        self.r={}; self.old=[{'event_id':'c1','stream_id':'c','note':'original'}]; self.write('baseline/corrections.json',self.old); self.write('baseline/remedies.json',[]); self.write('corrections.json',self.old); self.write('remedies.json',[])
    def write(self,p,x): (self.root/p).write_bytes(canonical(x))
    def anchor(self):
        self.write('receipts.json',self.r); self.write('anchor.json',dict(source_commit='a1'*20,receipts_sha256=digest((self.root/'receipts.json').read_bytes()),corrections_sha256=digest((self.root/'baseline/corrections.json').read_bytes()),remedies_sha256=digest((self.root/'baseline/remedies.json').read_bytes()))); return digest((self.root/'anchor.json').read_bytes())
    def runcheck(self): self.write('findings.json',[self.f]); return verify(self.root,self.anchor())
    def reject(self):
        with self.assertRaises(Exception): self.runcheck()
    def positive(self,lane=1):
        self.f['primary_lane_id']=lane; b=b'synthetic source'; h=digest(b); (self.root/'evidence'/h).write_bytes(b); self.f['source'].update(sha256=h,acquired_at='2026-11-26T01:00:00Z'); self.f.update(verification_status='VERIFIED',replay_id='replay',ci_receipt_id='ci'); subject=digest(canonical({k:self.f[k] for k in ('finding_id','revision','claim','source','metrics','source_commit','primary_lane_id','cross_lane_ids','jurisdiction')}))
        for kind in ('integrity','mathematics','authenticity','replay','ci'):
            p=kind+'.txt'; (self.root/p).write_bytes(kind.encode()); self.r[kind]=dict(kind=kind,verdict='PASS',subject_sha256=subject,source_commit=self.f['source_commit'],artifact=p,sha256=digest(kind.encode()))
            if kind in self.f['verification']: self.f['verification'][kind]=dict(status='PASS',receipt_id=kind)
    def test_hold(self): self.assertEqual(self.runcheck()[0]['status'],'HOLD')
    def test_verified(self): self.positive(); self.assertEqual(self.runcheck()[0]['accountability'],'UNKNOWN')
    def test_lane12(self): self.positive(12); self.runcheck(); del self.r['replay']; self.reject()
    def test_duplicate_lane(self): self.f['cross_lane_ids']=[1]; self.reject()
    def test_lane_range(self): self.f['primary_lane_id']=13; self.reject()
    def test_placeholder(self): self.f['source']['sha256']='ab'*32; self.reject()
    def test_hash_mismatch(self): self.positive(); (self.root/'evidence'/self.f['source']['sha256']).write_bytes(b'changed'); self.reject()
    def test_missing_replay(self): self.positive(); del self.r['replay']; self.reject()
    def test_stale_replay(self): self.positive(); self.r['replay']['source_commit']='b2'*20; self.reject()
    def test_changed_claim(self): self.positive(); self.f['claim']='changed'; self.reject()
    def test_history_edit(self): self.write('corrections.json',[dict(self.old[0],note='changed')]); self.reject()
    def test_history_delete(self): self.write('corrections.json',[]); self.reject()
    def test_history_append(self): self.write('corrections.json',self.old+[{'event_id':'c2','stream_id':'c'}]); self.runcheck()
    def test_remedy_edit(self): e={'event_id':'r1','stream_id':'r'}; self.write('baseline/remedies.json',[e]); self.write('remedies.json',[]); self.reject()
    def test_float(self): self.f['metrics']=[{'name':'x','atomic_value':1.5,'scale':0,'unit':'x','qualifier':'EXACT'}]; self.reject()
    def test_publication(self): self.f['publication']='AUTHORIZED'; self.reject()
    def test_anchor_tamper(self): self.write('findings.json',[self.f]); h=self.anchor(); self.write('receipts.json',{'fake':1}); self.assertRaises(Exception,verify,self.root,h)
if __name__=='__main__': unittest.main()
