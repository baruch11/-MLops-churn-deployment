from chaos.application.server import app, read_item, UnicornException
from fastapi.testclient import TestClient
import pytest


class TestWholeApi(object):
    """Those tests aims to use :
    -    Real production model (On GCP)
    -    Real Bdd (in a docker container)
    -    Real api calls, thanks to TestClient library,
            we can test data validation, error etc."""

    @pytest.mark.parametrize(
        "marketing",
        [{"BALANCE": 93259.57, "NB_PRODUITS": 3, "CARTE_CREDIT": "Yes",
            "SALAIRE": 141035.65, "SCORE_CREDIT": 581.0,
            "DATE_ENTREE": "2015-01-01 00:00:00", "NOM": "Mazzi",
            "PAYS": "Allemagne", "SEXE": "F", "AGE": 43,
            "MEMBRE_ACTIF": "No"}])
    def test_api_and_bdd_integration_test(self, marketing):
        with TestClient(app) as client:
            response = client.post(
                    "/detect/",
                    json=marketing
                )
            assert response.status_code == 200

    # We need to have a real bdd in order to raise UnicornException
    def test_raise_id_not_found(self):
        with pytest.raises(UnicornException):
            read_item("15688175")
