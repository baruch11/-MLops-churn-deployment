from chaos.infrastructure.connexion import Connexion
import pytest


@pytest.fixture(autouse=True)
def mock_socio_eco(monkeypatch):
    def mock_connect(*args, **kwargs):
        return True
    monkeypatch.setattr(Connexion, "connect", mock_connect)