"""The requested E01-E30 conformance suite: entirely synthetic fixtures."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.conformance.inheritance_v0_1 import evaluate, derive_child_state, canonical_hash, reconcile_documented_pay

PARENT = {"id": "synthetic-parent", "digest": canonical_hash({"id": "synthetic-parent"}),
          "state": "OBSERVED", "claimed_parent_status": "APPROVED"}
PROFILE = {"revision": "v1", "required_types": ["Research"], "parent_scope": "CitizenRoot"}


def child(id="r", type="Research", evidence="verified", requirement="REQUIRED", **changes):
    obj = {"id": id, "type": type, "requirement": requirement,
           "parent_id": PARENT["id"], "parent_digest": PARENT["digest"],
           "evidence": evidence,
           "verification": {"verified": True, "scope": type,
                            "checks": ["input_hash", "method"]},
           "claimed_status": "APPROVED"}
    obj.update(changes)
    return obj


def witness(target_kind, target_id, scope, **changes):
    value = {"target_kind": target_kind, "target_id": target_id,
             "scope": scope, "authorized": True, "verified": True}
    value.update(changes)
    return value


class InheritanceConformance(unittest.TestCase):
    def test_E01_verified_required_no_parent_promotion(self):
        r = evaluate(PARENT, [child()], PROFILE)
        self.assertEqual((r["aggregate"], r["parent_state"]), ("VERIFIED_SCOPED", "OBSERVED"))

    def test_E02_required_hold(self):
        self.assertEqual(evaluate(PARENT, [child(evidence="missing")], PROFILE)["aggregate"], "HOLD")

    def test_E03_required_conflict(self):
        self.assertEqual(evaluate(PARENT, [child(evidence="conflict")], PROFILE)["aggregate"], "CONFLICT")

    def test_E04_optional_hold(self):
        r = evaluate(PARENT, [child(), child("optional", "Other", "missing", "OPTIONAL")], PROFILE)
        self.assertEqual((r["aggregate"], r["parent_state"]), ("VERIFIED_SCOPED", "OBSERVED"))

    def test_E05_informational_child_approval_no_parent_promotion(self):
        info = child("info", "Informational", requirement="INFORMATIONAL",
                     approval_witness=witness("child", "info", "Informational"))
        self.assertEqual(derive_child_state(info), "APPROVED")
        self.assertEqual(evaluate(PARENT, [child(), info], PROFILE)["parent_state"], "OBSERVED")

    def test_E06_all_required_verified(self):
        profile = {**PROFILE, "required_types": ["Research", "CoachesGambit"]}
        r = evaluate(PARENT, [child(), child("c", "CoachesGambit")], profile)
        self.assertEqual((r["aggregate"], r["new_parent_receipt"]), ("VERIFIED_SCOPED", None))

    def test_E07_conflict_outweighs_scoped_verification(self):
        r = evaluate(PARENT, [child(), child("c", evidence="conflict")], PROFILE)
        self.assertEqual(r["aggregate"], "CONFLICT")
        self.assertEqual(r["child_states"]["r"], "VERIFIED_SCOPED")

    def test_E08_hold_outweighs_scoped_verification(self):
        r = evaluate(PARENT, [child(), child("h", evidence="missing")], PROFILE)
        self.assertEqual(r["aggregate"], "HOLD")
        self.assertEqual(r["child_states"]["r"], "VERIFIED_SCOPED")

    def test_E09_claimed_approver_without_witness(self):
        self.assertEqual(derive_child_state(child(claimed_status="APPROVED")), "VERIFIED_SCOPED")

    def test_E10_valid_child_scoped_approval(self):
        c = child(approval_witness=witness("child", "r", "Research"))
        self.assertEqual(derive_child_state(c), "APPROVED")
        self.assertEqual(evaluate(PARENT, [c], PROFILE)["parent_state"], "OBSERVED")

    def test_E11_parent_witness_but_reducer_not_run(self):
        r = evaluate(PARENT, [child()], PROFILE,
                     parent_witness=witness("parent", PARENT["id"], "CitizenRoot"))
        self.assertIsNone(r["new_parent_receipt"])

    def test_E12_parent_scoped_witness_and_explicit_reducer(self):
        original = copy.deepcopy(PARENT)
        r = evaluate(PARENT, [child()], PROFILE, reducer=True,
                     parent_witness=witness("parent", PARENT["id"], "CitizenRoot"))
        self.assertEqual(r["new_parent_receipt"]["new_state"], "APPROVED")
        self.assertEqual(PARENT, original)

    def test_E13_input_hash_only_insufficient_for_method(self):
        c = child(verification={"verified": True, "scope": "Research", "checks": ["input_hash"]})
        self.assertEqual(evaluate(PARENT, [c], PROFILE)["aggregate"], "HOLD")

    def test_E14_research_not_citizen_root_parent_state(self):
        self.assertEqual(evaluate(PARENT, [child()], PROFILE)["parent_state"], "OBSERVED")

    def test_E15_old_parent_bytes_immutable_on_child_change(self):
        original = copy.deepcopy(PARENT)
        evaluate(PARENT, [child(evidence="missing")], PROFILE)
        evaluate(PARENT, [child()], PROFILE)
        self.assertEqual(PARENT, original)

    def test_E16_attempt_direct_parent_mutation_rejected(self):
        r = evaluate(PARENT, [child()], PROFILE, attempt_parent_mutation=True)
        self.assertEqual(r["error"], "REJECT_MUTATION")

    def test_E17_profile_revision_instability(self):
        r = evaluate(PARENT, [child()], PROFILE, current_profile_revision="v2")
        self.assertEqual((r["aggregate"], r["error"]), ("HOLD", "PROFILE_CHANGED"))

    def test_E18_incompatible_affirmative_evidence(self):
        r = evaluate(PARENT, [child("a"), child("b")], PROFILE, conflicts=[("a", "b")])
        self.assertEqual(r["aggregate"], "CONFLICT")

    def test_E19_absent_evidence_is_hold_not_conflict(self):
        self.assertEqual(evaluate(PARENT, [child(evidence="missing")], PROFILE)["aggregate"], "HOLD")

    def test_E20_byte_hash_only_not_scope_or_method(self):
        c = child(evidence="observed", byte_integrity=True)
        self.assertEqual(derive_child_state(c), "OBSERVED")

    def test_E21_approval_scope_mismatch(self):
        c = child(approval_witness=witness("child", "r", "Other"))
        self.assertEqual(derive_child_state(c), "VERIFIED_SCOPED")

    def test_E22_missing_parent(self):
        r = evaluate(PARENT, [child()], PROFILE, parent_exists=False)
        self.assertEqual((r["aggregate"], r["error"]), ("HOLD", "UNRESOLVED_PARENT"))

    def test_E23_duplicate_lineage_under_distinct_ids(self):
        r = evaluate(PARENT, [child("a", source_digest="same"), child("b", source_digest="same")], PROFILE)
        self.assertEqual(r["error"], "DUPLICATE_LINEAGE")

    def test_E24_supersession_requires_explicit_reducer_and_preserves_old(self):
        cs = [child("old", evidence="missing"), child("new")]
        before = evaluate(PARENT, cs, PROFILE)
        after = evaluate(PARENT, cs, PROFILE, supersessions={"old": "new"})
        self.assertEqual(before["aggregate"], "HOLD")
        self.assertEqual(after["aggregate"], "VERIFIED_SCOPED")
        self.assertEqual(after["retained_child_ids"], ["new", "old"])

    def test_E25_no_max_status_semantics(self):
        cs = [child("good", approval_witness=witness("child", "good", "Research")),
              child("bad", evidence="conflict")]
        self.assertEqual(evaluate(PARENT, cs, PROFILE)["aggregate"], "CONFLICT")

    def test_E26_claimed_parent_approved_cannot_override_reducer(self):
        r = evaluate(PARENT, [child()], PROFILE)
        self.assertEqual((r["aggregate"], r["parent_state"]), ("VERIFIED_SCOPED", "OBSERVED"))
        self.assertIsNone(r["new_parent_receipt"])

    def test_E27_one_approved_one_required_hold(self):
        cs = [child("a", approval_witness=witness("child", "a", "Research")),
              child("b", evidence="missing")]
        self.assertEqual(evaluate(PARENT, cs, PROFILE)["aggregate"], "HOLD")

    def test_E28_parent_child_cycle_rejected(self):
        cs = [child(id=PARENT["id"])]
        self.assertEqual(evaluate(PARENT, cs, PROFILE)["error"], "LINEAGE_CYCLE")

    def test_E29_wrong_parent_digest(self):
        r = evaluate(PARENT, [child(parent_digest="sha256:wrong")], PROFILE)
        self.assertEqual((r["aggregate"], r["error"]), ("HOLD", "WRONG_PARENT_BINDING"))

    def test_E30_order_invariant_reduction(self):
        cs = [child("a"), child("b")]
        self.assertEqual(evaluate(PARENT, cs, PROFILE), evaluate(PARENT, list(reversed(cs)), PROFILE))

    def test_M01_status_injection_isolated(self):
        base = evaluate(PARENT, [child()], PROFILE)
        for status in ("OBSERVED", "HOLD", "CONFLICT", "VERIFIED_SCOPED", "APPROVED"):
            self.assertEqual(evaluate(PARENT, [child(claimed_status=status)], PROFILE), base)

    def test_M02_domain_substitution_isolated(self):
        swapped = child(type="CoachesGambit")
        self.assertEqual(evaluate(PARENT, [swapped], PROFILE)["aggregate"], "HOLD")

    def test_J01_E0_is_not_an_enlisted_rate(self):
        a = reconcile_documented_pay([{"period_id": "synthetic1", "actual_grade": "E-0",
                                      "verified_due": True, "verified_paid": True,
                                      "documented_gross_due": 1000, "recorded_gross_paid": 0}])
        self.assertIsNone(a["fully_reconciled_shortfall"])
        self.assertEqual(a["unresolved_periods"], ["synthetic1"])

    def test_J02_missing_pay_period_is_not_zero(self):
        a = reconcile_documented_pay([{"period_id": "synthetic2", "actual_grade": "E-3",
                                      "verified_due": True, "verified_paid": False,
                                      "documented_gross_due": 1000}])
        self.assertIsNone(a["fully_reconciled_shortfall"])

    def test_J03_verified_pay_math_distinct_from_entitlement(self):
        a = reconcile_documented_pay([{"period_id": "synthetic3", "actual_grade": "E-3",
                                      "verified_due": True, "verified_paid": True,
                                      "documented_gross_due": 1500, "recorded_gross_paid": 1400}])
        self.assertEqual(a["fully_reconciled_shortfall"], 100)
        self.assertTrue(a["not_an_entitlement_decision"])

    def test_J04_missing_child_ranks_must_never_fabricate_pay(self):
        a = reconcile_documented_pay([{"period_id": "dependent", "actual_grade": "DEPENDENT",
                                      "verified_due": True, "verified_paid": True,
                                      "documented_gross_due": 500, "recorded_gross_paid": 0}])
        self.assertIsNone(a["fully_reconciled_shortfall"])


if __name__ == "__main__":
    unittest.main()
