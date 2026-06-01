"""GDI Orchestrator V0.1.

Single public entrypoint for the GDI pipeline.

Responsibilities:
- Accept raw input events.
- Normalize iterable input without mutating original input.
- Forward to dispatch_events(events).
- Return dispatcher output unchanged.

Boundary:
- No decisions.
- No mutation.
- No metadata.
- No authority.
"""

from gdi_dispatcher import dispatch_events

__all__ = ["run_gdi_pipeline"]


def run_gdi_pipeline(events):
    """Return dispatcher outputs for events through the public GDI entrypoint."""
    if events is None:
        return []

    if not isinstance(events, (list, tuple)):
        events = list(events)

    return dispatch_events(events)
