from chaos.infrastructure.connexion import Connexion
import pytest


@pytest.fixture(autouse=True)
def mock_socio_eco(monkeypatch):
    def mock_connect(*args, **kwargs):
        return True
    monkeypatch.setattr(Connexion, "connect", mock_connect)


@pytest.fixture(autouse=True)
def use_local_pkl(monkeypatch):
    """Remove requests.sessions.Session.request for all tests."""
    def _mock_load_model():
        # explanation : the Customer __init__ method is expected to load
        # a default model when it model argument is None
        return None

    monkeypatch.setattr("chaos.application.server.load_churn_model",
                        _mock_load_model)
