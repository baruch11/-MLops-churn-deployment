import pytest
from chaos.application.server import detect, Question


class TestServer(object):

    @pytest.mark.parametrize(
        "test_input, expected",
        [(Question(BALANCE=0), 0)])
    def test_route_example(self, test_input, expected):
        """Test route example."""
        ans = detect(test_input)
        print(f"test_route ans: {ans}")
        assert ans.answer == expected
