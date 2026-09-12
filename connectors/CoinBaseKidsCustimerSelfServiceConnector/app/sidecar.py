from __future__ import annotations
import uuid
from .models import ProofState, RouteReceipt

class ComputerWisdomSidecar:
    """Routing membrane only. No authority, no verification, no writes."""

    def route(self, *, current_state: str, attempted_branch: str,
              branch_available: bool, safe_read_only: bool,
              fallback: str | None = None) -> RouteReceipt:
        if branch_available and safe_read_only:
            return RouteReceipt(
                route_id=str(uuid.uuid4()),
                from_state=current_state,
                attempted_branch=attempted_branch,
                result=ProofState.PASS,
                reason="Read-only branch available.",
                next_safe_move=attempted_branch,
            )

        reason = "Branch unavailable." if not branch_available else "Branch is not read-only."
        return RouteReceipt(
            route_id=str(uuid.uuid4()),
            from_state=current_state,
            attempted_branch=attempted_branch,
            result=ProofState.HOLD,
            reason=reason,
            next_safe_move=fallback,
        )
