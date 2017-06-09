import unittest
from ngt.game import Rules, Game


class TestGamePipeline(unittest.TestCase):

    def setUp(self):
        r1_info = {}
        self.r1 = Rules(**r1_info)
        g1_info = {'rules': self.r1}
        self.g1 = Game(**g1_info)

    def test_create_game(self):
        self.assertEqual(self.g1.rules, self.r1)
