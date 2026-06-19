"""GDI Public Entrypoint V0.1.

Single external API surface for the GDI pipeline.
"""

from gdi_orchestrator import run_gdi_pipeline

__all__ = ["gdi"]


def gdi(events):
    if events is None:
        return []

    if not isinstance(events, (list, tuple)):
        events = list(events)

    return run_gdi_pipeline(events)
