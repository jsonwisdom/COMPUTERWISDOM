#!/usr/bin/env python3
"""Apple Blossom deep audit state machine (read-only planner).

Consumes repo snapshot/audit JSON. It never invents purpose and never stops
merely because a lifecycle label exists.
"""
REQUIRED_SNAPSHOT_FIELDS = [
    "repo","default_branch","head_commit","tree_receipt","tree_entry_count",
    "canonical_tree_digest","high_signal_files_read","project_purpose",
    "purpose_receipts","execution_surfaces","identity_pointers",
    "external_pointers","open_gaps","snapshot_state"
]

def triggers(obj):
    t=[]
    if not obj.get("head_commit"): t.append("TRIGGER_A_ROOT_UNKNOWN")
    if not obj.get("tree_receipt"): t.append("TRIGGER_B_TREE_UNKNOWN")
    if not obj.get("project_purpose"): t.append("TRIGGER_C_PURPOSE_UNKNOWN")
    if obj.get("purpose_conflict"): t.append("TRIGGER_D_PURPOSE_CONFLICT")
    if not obj.get("lineage_checked"): t.append("TRIGGER_E_LINEAGE_UNKNOWN")
    if obj.get("identity_claim_material") and not obj.get("identity_checked"): t.append("TRIGGER_F_IDENTITY_UNKNOWN")
    if obj.get("execution_claimed") and not obj.get("execution_surfaces"): t.append("TRIGGER_G_EXECUTION_UNKNOWN")
    if obj.get("external_pointer_material") and not obj.get("external_pointers_checked"): t.append("TRIGGER_H_EXTERNAL_POINTER_UNKNOWN")
    if not obj.get("canonical_tree_digest"): t.append("TRIGGER_I_SNAPSHOT_MISSING")
    if obj.get("delta_detected") and not obj.get("delta_classified"): t.append("TRIGGER_J_DELTA_UNCLASSIFIED")
    return t

def terminal(obj):
    ts=triggers(obj)
    if ts:
        return {"terminal":"CONTINUE_AUDIT","triggers":ts,"route":"APPLE_BLOSSOM_DEEPEN"}
    gaps=[g for g in obj.get("open_gaps",[]) if g.get("affects_project_identity",True)]
    if gaps:
        return {"terminal":"CONTINUE_AUDIT","triggers":["OPEN_IDENTITY_GAPS"],"route":"APPLE_BLOSSOM_DEEPEN"}
    return {"terminal":"SNAPSHOT_ELIGIBLE","route":"FREEZE_PROJECT_SNAPSHOT"}

def delta_route(snapshot_head,current_head,history_rewrite=False):
    if history_rewrite:
        return "FULL_RESCAN"
    if snapshot_head==current_head:
        return "NO_CHANGE"
    return "DELTA_SCAN"
