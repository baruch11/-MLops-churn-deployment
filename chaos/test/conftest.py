from chaos.infrastructure.connexion import Connexion
from churn.domain.churn_model import ChurnModelFinal
import pytest


@pytest.fixture()
def mock_connexion(monkeypatch):
    def mock_connect(*args, **kwargs):
        return True
    monkeypatch.setattr(Connexion, "connect", mock_connect)


@pytest.fixture(autouse=True)
def use_local_pkl(monkeypatch):
    """Remove requests.sessions.Session.request for all tests."""
    def _mock_load_model():
        return ChurnModelFinal().load()

    monkeypatch.setattr("chaos.application.server.load_churn_model",
                        _mock_load_model)