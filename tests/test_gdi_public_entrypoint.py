from gdi_public_entrypoint import gdi


def test_gdi_returns_orchestrator_output(monkeypatch):
    expected = [{"authority": False}]

    def fake_pipeline(events):
        return expected

    monkeypatch.setattr("gdi_public_entrypoint.run_gdi_pipeline", fake_pipeline)

    assert gdi([{"event": "x"}]) == expected


def test_gdi_none_returns_empty_list():
    assert gdi(None) == []
