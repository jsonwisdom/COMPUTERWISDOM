import datetime as dt, unittest, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from ooda_receipt_gate import decide

def rc(p=("PASS", "aa"), r=("PASS", "aa")):
    return {"routes": [{"role": "PRIMARY", "http": 200, "status": p[0], "body_sha256": p[1]},
                       {"role": "REPLICA", "http": 200, "status": r[0], "body_sha256": r[1]}]}
T0 = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
def st(**k): return {"routes": {"PRIMARY": [200, "PASS", "aa"], "REPLICA": [200, "PASS", "aa"]}, "last_append_utc": "2026-01-01T00:00:00Z"}

class Gate(unittest.TestCase):
    def test_first(self): self.assertEqual(decide(rc(), None, 6, T0)[0], "APPEND")
    def test_unchanged_skips(self): self.assertEqual(decide(rc(), st(), 6, T0 + dt.timedelta(hours=1))[:2], ("SKIP", "unchanged_within_heartbeat"))
    def test_heartbeat(self): self.assertEqual(decide(rc(), st(), 6, T0 + dt.timedelta(hours=6))[:2], ("APPEND", "heartbeat"))
    def test_primary_change_only(self):
        d = decide(rc(p=("HOLD", "bb")), st(), 6, T0 + dt.timedelta(minutes=5))
        self.assertEqual((d[0], d[2]), ("APPEND", ["PRIMARY"]))
    def test_replica_change_only(self):
        d = decide(rc(r=("HOLD", None)), st(), 6, T0 + dt.timedelta(minutes=5))
        self.assertEqual((d[0], d[2]), ("APPEND", ["REPLICA"]))
    def test_both_change(self):
        self.assertEqual(decide(rc(("HOLD", "x"), ("HOLD", "y")), st(), 6, T0)[2], ["PRIMARY", "REPLICA"])
if __name__ == "__main__": unittest.main()
