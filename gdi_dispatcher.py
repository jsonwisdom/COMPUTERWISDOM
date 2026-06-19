"""GDI Dispatcher V0.1.

Pure dispatcher for routing multiple events through the GDI coordinator.

Boundary:
- Pure forwarding only.
- No decisions.
- No mutation.
- No metadata.
- No authority.
"""

from gdi_coordinator import coordinate_event

__all__ = ["dispatch_events"]


def dispatch_events(events):
    """Return coordinator outputs for events while preserving order."""
    if events is None:
        return []

    if not isinstance(events, (list, tuple)):
        events = list(events)

    return [coordinate_event(event) for event in events]
