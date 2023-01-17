from churn.domain.domain_utils import get_test_set
from chaos.application.server import app
from fastapi.testclient import TestClient
from sklearn.metrics import f1_score
from chaos.domain.customer import ModelNotLoaded
from chaos.application.server import HTTP_INTERNAL_SERVER_ERROR
from sqlalchemy.exc import OperationalError


class TestServer(object):

    def perf_test_api(self, use_local_pkl, mock_customer_loader_historicize):

        with TestClient(app) as client:
            EXPECTED_F1_SCORE = 0.61
            X_test, y_test = get_test_set()
            customers_list = X_test.to_dict(orient="records")
            y_pred = []
            for features in customers_list:
                response = client.post(
                    "/detect/",
                    json=features
                )
                assert response.status_code == 200
                y_pred.append(float(response.json().get('answer')) > 0.5)
            perf_api = f1_score(y_test, y_pred)
            print(f"F1 score {perf_api}")
            assert perf_api > EXPECTED_F1_SCORE

    def test_missing_model(self, monkeypatch):
        """Check error status if model is missing."""
        def _model_not_found():
            raise ModelNotLoaded

        monkeypatch.setattr("chaos.application.server.load_churn_model",
                            _model_not_found)

        with TestClient(app) as client:
            response = client.post("/detect/", json={"BALANCE": 0})
            assert response.status_code == HTTP_INTERNAL_SERVER_ERROR

    def test_missing_sql_connexion(self, use_local_pkl, monkeypatch):
        """Check error status if sql database is missing."""
        def _sql_not_found(query, engine):
            raise OperationalError(None, None, None)

        monkeypatch.setattr("chaos.infrastructure.customer_loader.pd.read_sql",
                            _sql_not_found)

        with TestClient(app) as client:
            response = client.get("/customer/11")
            assert response.status_code == HTTP_INTERNAL_SERVER_ERROR
            assert response.json().get('message') == 'No SQL connection'
