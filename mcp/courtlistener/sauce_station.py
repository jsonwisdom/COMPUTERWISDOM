from evidence_rules import r_j3,r_j5
def evaluate_flow(x):
    a=r_j3(x); b=r_j5(x,a)
    return {**a,**b,"prohibitions":[
        "PATH_REPLAYED != IMPROPER_PATH",
        "PATH_PARTIAL != CONCEALMENT",
        "FAST_NOTICE != COLLUSION",
        "UNEXPLAINED_HOP != inferred_hidden_communication"]}
