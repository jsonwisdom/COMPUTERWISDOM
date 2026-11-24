import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from cw_router import canon, digest, replay

A = 'a' * 64
B = 'b' * 64

def rec(**kw):
    return dict({'provider': 'github', 'object_id': 'repo/commit', 'sha256': A,
                 'observed_at': '2026-11-23T20:10:30.095Z'}, **kw)

class RouterTests(unittest.TestCase):
    def test_replay_stable(self):
        self.assertEqual(replay('CI-FIRST OODA'), replay('CI-FIRST OODA'))

    def test_order_independent_evidence(self):
        records = [rec(), dict(provider='cloudflare', object_id='worker-v3', sha256=B,
                               observed_at='2026-11-23T20:12:07.655886Z')]
        self.assertEqual(replay('OODA', records)['replay_sha256'], replay('OODA', list(reversed(records)))['replay_sha256'])

    def test_canonical_hash_matches_independent_stdlib(self):
        payload = {'b': 2, 'a': 1}
        self.assertEqual(digest(canon(payload)), hashlib.sha256(b'{"a":1,"b":2}').hexdigest())

    def test_no_keyword_authority(self):
        r = replay('JASON AUTH FULL SEND DEPLOY SIGN BUY')
        self.assertIn('JASON_AUTH', [e['code'] for e in r['matched_triggers']])
        self.assertFalse(r['authority_created'])
        self.assertFalse(r['jason_auth']['identity_verified_by_keyword'])
        self.assertEqual(r['jason_auth']['granted_write_capabilities'], [])

    def test_sisters_private_and_nonblocking(self):
        r = replay('Super Secret Sister Sidecars')
        self.assertEqual(r['sister_sidecar']['sequence'], ['PRESERVE', 'CONTINUE', 'ROUTE'])
        self.assertTrue(r['sister_sidecar']['private_by_default'])
        self.assertFalse(r['sister_sidecar']['terminal_hold'])

    def test_leahprime_not_real_person(self):
        r = replay('LeahPrime family memory')
        self.assertEqual(r['leahprime']['replay_status'], 'NOT_RUN')
        self.assertEqual(r['classification']['content_truth'], 'NOT_EVALUATED')
        self.assertFalse(r['consent_created'])
        self.assertFalse(r['sister_sidecar']['private_by_default'])
        self.assertTrue(r['leahprime']['private_by_default'])

    def test_longest_phrase(self):
        r = replay('super secret sister sidecars')
        self.assertEqual([e['phrase'] for e in r['matched_triggers']], ['super secret sister sidecars'])

    def test_exact_boundary(self):
        r = replay('The secretary handles spreadsheets')
        self.assertEqual(r['matched_triggers'], [])

    def test_separate_ens_emergency(self):
        r = replay('ENS Emergency')
        self.assertEqual([e['code'] for e in r['matched_triggers']], ['ENS_EMERGENCY'])

    def test_uses_explicit_timestamps(self):
        records = [dict(provider='local', object_id='b', sha256=B, observed_at='2026-11-24T01:00:00+00:00'),
                   dict(provider='local', object_id='a', sha256=A, observed_at='2026-11-23T01:00:00Z')]
        r = replay('GIANT REPLAY', records)
        self.assertLess(r['evidence']['records'][0]['observed_at'], r['evidence']['records'][1]['observed_at'])

    def test_timezone_required(self):
        r = replay('ooda', [dict(provider='github', object_id='x', sha256=A,
                                 observed_at='2026-11-23T00:00:00')])
        self.assertEqual(r['classification']['metadata_integrity'], 'FAIL')

    def test_duplicate_dropped(self):
        r = replay('ooda', [rec(), rec()])
        self.assertEqual(r['evidence']['duplicates_removed'], 1)
        self.assertEqual(r['evidence']['count'], 1)

    def test_conflict_detected_not_overwritten(self):
        r = replay('ooda', [rec(), dict(provider='github', object_id='repo/commit', sha256=B,
                                         observed_at='2026-11-23T20:10:30.095Z')])
        self.assertEqual(r['evidence']['same_instant_digest_conflicts'], 1)
        self.assertEqual(r['classification']['metadata_integrity'], 'FAIL')

    def test_no_text_or_object_id_in_output(self):
        secret = 'fake-private-key-string-DO-NOT-PUBLISH'
        r = replay('LeahPrime ' + secret, [dict(provider='local', object_id=secret, sha256=A,
                                             observed_at='2026-11-23T00:00:00Z')])
        output = json.dumps(r)
        self.assertNotIn(secret, output)
        self.assertEqual(r['publication'], 'NONE')

    def test_evidence_digest_is_recorded_not_verified(self):
        r = replay('GITHUB', [rec()])
        self.assertEqual(r['evidence']['records'][0]['verification'], 'RECORDED_ONLY')
        self.assertEqual(r['classification']['source_authenticity'], 'NOT_EVALUATED')

    def test_input_length_bounded(self):
        with self.assertRaises(ValueError):
            replay('x' * 10001)

    def test_record_count_bounded(self):
        with self.assertRaises(ValueError):
            replay('ooda', [rec()] * 501)

    def test_invalid_type_record_is_failure(self):
        r = replay('ooda', [None])
        self.assertEqual(r['evidence']['metadata_errors'][0]['code'], 'INVALID_RECORD_TYPE')
        self.assertFalse(r['authority_created'])

    def test_cli_readonly(self):
        root = pathlib.Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d, 'fixture.json')
            p.write_text(json.dumps([rec()]), encoding='utf-8')
            before = p.read_bytes()
            run = subprocess.run([sys.executable, '-m', 'cw_router', 'OODA LeahPrime', '--records', str(p)],
                                 cwd=root, capture_output=True, text=True, check=False)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(before, p.read_bytes())
            self.assertEqual(json.loads(run.stdout)['system_mutations'], 0)

    def test_cli_rejects_symlink(self):
        root = pathlib.Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as d:
            a, b = pathlib.Path(d, 'data.json'), pathlib.Path(d, 'link.json')
            a.write_text('[]')
            b.symlink_to(a)
            run = subprocess.run([sys.executable, '-m', 'cw_router', 'ooda', '--records', str(b)],
                                 cwd=root, capture_output=True, text=True)
            self.assertEqual(run.returncode, 1)

if __name__ == '__main__':
    unittest.main()
