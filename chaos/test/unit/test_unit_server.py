import pytest
from chaos.application.server import detect, CustomerInput


class TestServer(object):

    @pytest.mark.parametrize(
        "test_input, expected",
        [(CustomerInput(BALANCE=0), 0.5)])
    def test_route_example(self, test_input, expected):
        """Test route example."""
        ans = detect(test_input)
        print(f"test_route ans: {ans}")
        assert ans.answer < expected
