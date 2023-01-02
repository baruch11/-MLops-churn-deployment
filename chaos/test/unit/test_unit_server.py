import pytest
from churn.domain.domain_utils import get_test_set
from chaos.application.server import detect, CustomerInput, app
from fastapi.testclient import TestClient
from sklearn.metrics import f1_score
import logging

client = TestClient(app)


class TestServer(object):

    @pytest.mark.parametrize(
        "test_input, expected",
        [(CustomerInput(BALANCE=0), False)])
    def test_route_example(self, test_input, expected):
        """Test route example."""
        ans = detect(test_input)
        print(f"test_route ans: {ans}")
        assert (ans.answer > 0.5) == expected

    def test_perf(self):
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
        logging.error("F1 score %f", perf_api)
        assert perf_api > EXPECTED_F1_SCORE
