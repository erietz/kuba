import unittest
from KubaGame import KubaGame

class TestReadme(unittest.TestCase):
    def test_readme_example(self):
        game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
        self.assertEqual(game.get_marble_count(), (8,8,13))
        self.assertEqual(game.get_captured('PlayerA'), 0)
        self.assertEqual(game.get_current_turn(), 'PlayerB') # because PlayerA has just played.
        self.assertIsNone(game.get_winner())
        self.assertTrue(game.make_move('PlayerA', (6,5), 'F'))
        self.assertFalse(game.make_move('PlayerA', (6,5), 'L'))
        self.assertEqual(game.get_marble((5,5)), 'W')
