from churn.domain.domain_utils import get_test_set
from chaos.application.server import app
from fastapi.testclient import TestClient
from sklearn.metrics import f1_score


class TestServer(object):

    def test_perf(self, use_local_pkl):
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
