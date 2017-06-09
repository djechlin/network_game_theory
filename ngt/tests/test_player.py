import unittest
from ngt.player import Player


class TestPlayerMethods(unittest.TestCase):

    def setUp(self):
        p1_info = {
            'name': 'Leo',
            'utility': None,
            'action_strategy': None,
            'reaction_strategy': None,
        }
        self.p1 = Player(**p1_info)

    def test_create_profile_with_kwargs(self):
        self.assertEqual(str(self.p1), 'Leo')
