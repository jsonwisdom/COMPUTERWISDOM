import importlib.util,pathlib,unittest
p=pathlib.Path(__file__).resolve().parents[1]/'tools/auditnow/disclosure_first.py'
s=importlib.util.spec_from_file_location('auditnow',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class AuditNowTests(unittest.TestCase):
 def test_full_reducer(self):
  from itertools import product
  tally={'FAIL':0,'HOLD':0,'PASS':0}
  for states in product(m.LEVEL,repeat=8):
   c={'mandatory_tests':list(m.TESTS),'tests':dict(zip(m.TESTS,states)),'sources':[{'underlying_record_id':'A','independent':True,'inspection':'SCOPED_REVIEWED'},{'underlying_record_id':'B','independent':True,'inspection':'SCOPED_REVIEWED'}]}
   tally[m.reduce_claim(c)[0]]+=1
  self.assertEqual(tally,{'FAIL':6305,'HOLD':255,'PASS':1})
 def test_no_source_laundering(self):
  c={'mandatory_tests':['corroboration'],'tests':{'corroboration':'PASS'},'sources':[{'underlying_record_id':'HEARING','independent':True,'inspection':'SCOPED_REVIEWED'}]*2}
  self.assertEqual(m.reduce_claim(c)[0],'HOLD')
 def test_missing_profile(self):self.assertEqual(m.reduce_claim({'tests':{}})[0],'HOLD')
 def test_no_release_even_with_pass(self):
  c={'schema':'AUDITNOW_DISCLOSURE_V0_1','case_id':'TEST-001','canon':False,'authority_created':False,'disclosure':{k:'HUMAN_REVIEW_REQUIRED' if k=='release_permission' else 'PUBLIC_SAFE_METADATA_ONLY' if k=='privacy' else 'test' for k in m.FIELDS},'claims':[{'claim_id':'CLM-001','proposition':'a','sources':[{'underlying_record_id':'ONE'}],'mandatory_tests':['existence'],'tests':{'existence':'PASS'}}]}
  r=m.evaluate(c)
  self.assertEqual(r['joy_candidate'],'REVIEW_ONLY');self.assertFalse(r['joy_published']);self.assertFalse(r['public_release_authorized']);self.assertFalse(r['historical_truth_established'])
 def test_bad_privacy_blocks(self):
  r=m.evaluate({'schema':'AUDITNOW_DISCLOSURE_V0_1','case_id':'TEST-002','canon':False,'authority_created':False,'disclosure':{'privacy':'PRIVATE'},'claims':[]})
  self.assertEqual(r['case_state'],'BLOCKED')
