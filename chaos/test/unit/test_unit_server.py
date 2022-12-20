import unittest
from chaos.application.server import Question, example, Answer


class TesttServer(unittest.TestCase):

    def test_route_example_no_exept(self):
        """Test route example."""
        req = Question()
        ans = example(req)
        self.assertTrue(ans != Answer(answer=-1.0))
