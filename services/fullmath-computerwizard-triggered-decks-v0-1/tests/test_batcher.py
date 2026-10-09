import copy
import hashlib
import json
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from batcher import (CANON_FREEZE, GateError, SCHEMA, PURPOSE, build_candidate, canonical,
                     merkle_root, no_duplicate_keys, strict_json, strict_png_size,
                     verify_candidate)


def png(w=3,h=4):
    def chunk(name,data):
        return len(data).to_bytes(4,'big')+name+data+(zlib.crc32(name+data)&0xffffffff).to_bytes(4,'big')
    hdr=w.to_bytes(4,'big')+h.to_bytes(4,'big')+bytes([8,6,0,0,0])
    rows=b''.join(b'\x00'+b'\xff\xff\xff\xff'*w for _ in range(h))
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',hdr)+chunk(b'IDAT',zlib.compress(rows))+chunk(b'IEND',b'')


class BatcherTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        image=png()
        (self.root/'fixture.png').write_bytes(image)
        self.manifest={'schema':SCHEMA,'purpose':PURPOSE,'operator':'JAY',
                       'mode':'DESIGN_CANDIDATE_ONLY','family_data':False,
                       'canon_policy':'SEPARATE_LINEAGE_NO_CANON_WRITE',
                       'cards':[{'card_id':f'CWTD-SYN-{i:03d}','asset_path':'fixture.png',
                                 'asset_sha256':hashlib.sha256(image).hexdigest(),
                                 'fiction_label':'FICTION / SATIRE — NOT PREDICTIONS OR FACTS',
                                 'source_class':'FICTION_SATIRE','instances':2,
                                 'caption':f'Synthetic test card {i}',
                                 'master_status':'CANDIDATE_NOT_APPROVED'} for i in range(3)]}

    def make(self,m=None): return build_candidate(self.manifest if m is None else m,self.root)

    def test_candidate_hold(self):
        c=self.make()
        self.assertEqual(c['instance_count'],6)
        self.assertEqual(c['production_status'],'HOLD')
        self.assertFalse(c['external_send'])
        self.assertFalse(c['target_1m_per_min_verified'])
        self.assertEqual(c['canon_freeze_unchanged'],CANON_FREEZE)
    def test_determinism(self): self.assertEqual(self.make(),self.make())
    def test_verify_replay(self): self.assertTrue(verify_candidate(self.manifest,self.root,self.make())['replay_verified'])
    def test_replay_tampering(self):
        x=self.make();x['instance_count']=999
        with self.assertRaisesRegex(GateError,'REPLAY_MISMATCH'):verify_candidate(self.manifest,self.root,x)
    def test_merkle_odd(self): self.assertEqual(merkle_root(['00'*32]*3),merkle_root(['00'*32]*3))
    def test_duplicate_json_keys(self):
        with self.assertRaisesRegex(GateError,'DUPLICATE_JSON_KEY'):strict_json(b'{"a":1,"a":2}')
    def test_denies_live_mode(self):
        m=copy.deepcopy(self.manifest);m['mode']='DEPLOY'
        with self.assertRaisesRegex(GateError,'PRODUCTION_OR_FAMILY_BLOCKED'):self.make(m)
    def test_denies_family_lane(self):
        m=copy.deepcopy(self.manifest);m['family_data']=True
        with self.assertRaisesRegex(GateError,'PRODUCTION_OR_FAMILY_BLOCKED'):self.make(m)
    def test_denies_wrong_operator(self):
        m=copy.deepcopy(self.manifest);m['operator']='JASON'
        with self.assertRaisesRegex(GateError,'WRONG_SCOPE'):self.make(m)
    def test_denies_canon_mutation(self):
        m=copy.deepcopy(self.manifest);m['canon_policy']='MODIFY_CANON'
        with self.assertRaisesRegex(GateError,'FROZEN_LINEAGE_BLOCKED'):self.make(m)
    def test_denies_missing_label(self):
        m=copy.deepcopy(self.manifest);m['cards'][0]['fiction_label']='real prediction'
        with self.assertRaisesRegex(GateError,'FICTION_LABEL_REQUIRED'):self.make(m)
    def test_denies_claim_promotion(self):
        m=copy.deepcopy(self.manifest);m['cards'][0]['source_class']='FACT'
        with self.assertRaisesRegex(GateError,'UNVERIFIED_MASTER_BLOCKED'):self.make(m)
    def test_denies_unapproved_master(self):
        m=copy.deepcopy(self.manifest);m['cards'][0]['master_status']='APPROVED'
        with self.assertRaisesRegex(GateError,'UNVERIFIED_MASTER_BLOCKED'):self.make(m)
    def test_denies_duplicate_card(self):
        m=copy.deepcopy(self.manifest);m['cards'][1]['card_id']=m['cards'][0]['card_id']
        with self.assertRaisesRegex(GateError,'CARD_ID_INVALID_OR_DUPLICATE'):self.make(m)
    def test_denies_wrong_card_count(self):
        m=copy.deepcopy(self.manifest);m['cards'].pop()
        with self.assertRaisesRegex(GateError,'CARD_BATCH_MUST_DIVIDE_BY_3'):self.make(m)
    def test_denies_hash_mismatch(self):
        m=copy.deepcopy(self.manifest);m['cards'][0]['asset_sha256']='0'*64
        with self.assertRaisesRegex(GateError,'ASSET_HASH_MISMATCH'):self.make(m)
    def test_denies_path_traversal(self):
        m=copy.deepcopy(self.manifest);m['cards'][0]['asset_path']='../secret.png'
        with self.assertRaisesRegex(GateError,'UNSAFE_PATH'):self.make(m)
    def test_denies_symlink(self):
        (self.root/'alias.png').symlink_to(self.root/'fixture.png')
        m=copy.deepcopy(self.manifest);m['cards'][0]['asset_path']='alias.png'
        with self.assertRaisesRegex(GateError,'SYMLINK_FORBIDDEN'):self.make(m)
    def test_denies_square_png(self):
        (self.root/'fixture.png').write_bytes(png(4,4))
        m=copy.deepcopy(self.manifest)
        for c in m['cards']:c['asset_sha256']=hashlib.sha256(png(4,4)).hexdigest()
        with self.assertRaisesRegex(GateError,'PORTRAIT_RATIO_REQUIRED'):self.make(m)
    def test_denies_truncated_png(self):
        with self.assertRaises(GateError):strict_png_size(png()[:-6])
    def test_denies_png_crc_failure(self):
        b=bytearray(png());b[24]^=1
        with self.assertRaisesRegex(GateError,'PNG_CRC_MISMATCH'):strict_png_size(bytes(b))
    def test_denies_extra_json_fields(self):
        m=copy.deepcopy(self.manifest);m['onchain']=True
        with self.assertRaisesRegex(GateError,'FIELDS_INVALID_MANIFEST'):self.make(m)
    def test_bool_instances_not_count(self):
        m=copy.deepcopy(self.manifest);m['cards'][0]['instances']=True
        with self.assertRaisesRegex(GateError,'INSTANCE_LIMIT'):self.make(m)
    def test_denies_run_over_budget(self):
        m=copy.deepcopy(self.manifest)
        for c in m['cards']:c['instances']=3000
        self.assertEqual(self.make(m)['instance_count'],9000)
        m['cards'][0]['instances']=3001
        with self.assertRaisesRegex(GateError,'INSTANCE_LIMIT'):self.make(m)

if __name__=='__main__':unittest.main()
