def _state(v, receipts):
    if v is None: return "missing"
    if v == "": return "empty_present"
    if v == "unknown": return "unknown"
    return "valid" if v in receipts else "not_in_source_list"

def r_j3(x):
    receipts=set(x.get("source_receipts",[])); events=x.get("events",[])
    origin=bool(x.get("request_created_at") and x.get("request_recipient"))
    missing=[]
    for e in events:
        st=_state(e.get("source_receipt"),receipts)
        if st!="valid":
            v=e.get("source_receipt")
            missing.append(v if st=="not_in_source_list" else f"{st}_for_{e['action']}")
    route=any(e.get("action")=="ROUTE" and
              _state(e.get("source_receipt"),receipts)=="valid" for e in events)
    subj=_state(x.get("subject_notification_source"),receipts)
    unexplained=[]
    if not events and x.get("subject_notification_at"):
        unexplained=["REQUEST->SUBJECT_AWARENESS"]
    if not origin or unexplained:
        status="PATH_UNKNOWN"
    elif missing or not route or subj!="valid":
        status="PATH_PARTIAL"
    else:
        status="PATH_REPLAYED"
    if "expected_route_receipt" in missing:
        missing=["expected_route_receipt"]
    return {"path_status":status,"missing_receipts":missing,
            "unexplained_hops":unexplained,"has_route_valid":route,
            "subject_receipt_state":subj}

def r_j5(x,r3):
    fire=(x.get("procedure_model_requires_route") is True
          and len(x.get("events",[]))>0
          and not r3["has_route_valid"]
          and r3["subject_receipt_state"]=="valid")
    return {"r_j5":"UNEXPLAINED_HOP" if fire else None,
            "classification":"RESEARCH_TARGET" if fire else None,
            "r_j5_basis":"procedure_model" if fire else None}
