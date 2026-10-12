from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parents[1]/"mcp"/"courtlistener"))
from sauce_station import evaluate_flow

def base():
    return dict(request_created_at="T0",request_recipient="CLERK",
                subject_notification_at="T2",source_receipts=[],
                events=[],procedure_model_requires_route=False)

def test_f1():
    x=base(); x["source_receipts"]=["a","r","c"]
    x["subject_notification_source"]="c"
    x["events"]=[{"action":"ACCESS","source_receipt":"a"},
                 {"action":"ROUTE","source_receipt":"r"}]
    y=evaluate_flow(x); assert y["path_status"]=="PATH_REPLAYED"; assert y["unexplained_hops"]==[]

def test_f2():
    x=base(); x["source_receipts"]=["c"]; x["subject_notification_source"]="c"
    x["events"]=[{"action":"ROUTE","source_receipt":"expected_route_receipt"}]
    y=evaluate_flow(x); assert y["path_status"]=="PATH_PARTIAL"; assert y["missing_receipts"]==["expected_route_receipt"]

def test_f3():
    x=base(); x["subject_notification_source"]="unknown"
    y=evaluate_flow(x); assert y["path_status"]=="PATH_UNKNOWN"; assert y["unexplained_hops"]==["REQUEST->SUBJECT_AWARENESS"]

def test_f4():
    x=base(); x["source_receipts"]=["a","c"]; x["subject_notification_source"]="c"
    x["events"]=[{"action":"ACCESS","source_receipt":"a"}]; x["procedure_model_requires_route"]=True
    y=evaluate_flow(x); assert y["path_status"]=="PATH_PARTIAL"; assert y["r_j5"]=="UNEXPLAINED_HOP"; assert y["classification"]=="RESEARCH_TARGET"
