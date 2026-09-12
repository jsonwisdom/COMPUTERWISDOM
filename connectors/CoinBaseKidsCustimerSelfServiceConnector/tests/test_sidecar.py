from app.sidecar import ComputerWisdomSidecar
from app.models import ProofState

def test_mutation_holds():
    r = ComputerWisdomSidecar().route(current_state="READY", attempted_branch="transfer", branch_available=True, safe_read_only=False, fallback="statement_export")
    assert r.result == ProofState.HOLD
    assert r.write is False
