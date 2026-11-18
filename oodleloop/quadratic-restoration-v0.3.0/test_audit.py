import json, unittest
from pathlib import Path
from audit import check

original=json.loads((Path(__file__).parent/'architecture.json').read_text())
class ArchitecturalTests(unittest.TestCase):
    def test_original_passes(self): self.assertEqual(check(original),[])
    def test_build_disabled_detected(self):
        d=json.loads(json.dumps(original)); d['build_authority']='DISABLED'; self.assertIn('build_disabled',check(d))
    def test_public_secrets_detected(self):
        d=json.loads(json.dumps(original)); d['rails']['public']['allowed'].append('publish_secrets'); self.assertIn('forbidden_capability_publish_secrets',check(d))
    def test_global_hold_detected(self):
        d=json.loads(json.dumps(original)); d['global_project_hold']=True; self.assertIn('global_hold',check(d))
    def test_wallet_conflation_detected(self):
        d=json.loads(json.dumps(original)); d['wallets']['a380']['address']=d['wallets']['pc']['address']; self.assertIn('wallet_conflation',check(d))
    def test_financial_authority_detected(self):
        d=json.loads(json.dumps(original)); d['continuity']['financial_actions']='AUTO'; self.assertIn('financial_authority',check(d))
if __name__=='__main__': unittest.main()
