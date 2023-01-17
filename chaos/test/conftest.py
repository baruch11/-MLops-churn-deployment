from chaos.infrastructure.connexion import Connexion
from churn.domain.churn_model import ChurnModelFinal
from chaos.infrastructure.customer_loader import CustomerLoader
import pytest


@pytest.fixture()
def mock_connexion(monkeypatch):
    def mock_connect(*args, **kwargs):
        return True
    monkeypatch.setattr(Connexion, "connect", mock_connect)


@pytest.fixture()
def mock_customer_loader_historicize(monkeypatch):
    def _mock_historicize(*args, **kwargs):
        return True
    monkeypatch.setattr(
        CustomerLoader,
        "historicize_api_calls",
        _mock_historicize)


@pytest.fixture()
def use_local_pkl(monkeypatch):
    """Remove requests.sessions.Session.request for all tests."""
    def _mock_load_model():
        return ChurnModelFinal().load()

    monkeypatch.setattr("chaos.application.server.load_churn_model",
                        _mock_load_model)
